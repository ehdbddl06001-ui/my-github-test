#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  v15b_local.py — 로컬 자립 실행 (raw MIT-BIH → 캐시 → base vs base_psa2 → 200·222 판정)
#  옵션1: 재구현 특징(v14_core) + P극성(psa) + 자기대비 상대화(psa_rel).
#  목적: psa_rel 이 200·222 를 개선하는지 로컬 GPU 로 검증. 게이트(v14) 폐기.
#
#  실행:  python v15b_local.py            (기본: 캐시빌드 + 5seed 학습 + 판정)
#         python v15b_local.py --seeds 10 --epochs 25
#  결과는 results/ 에 저장 → 재실행 시 학습 건너뛰고 판정만.
# ═══════════════════════════════════════════════════════════════════════════
import os, sys, json, time, glob, argparse
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np
import keras
from keras import layers
from sklearn.metrics import (average_precision_score, roc_auc_score,
                             precision_recall_fscore_support, f1_score)
from sklearn.utils.class_weight import compute_class_weight

# ── 로컬 설정 ────────────────────────────────────────────────────────────────
RAW_DIR = "/home/user/work/v9/data/mitdb"      # ← raw .atr/.dat/.hea 있는 곳
CACHE   = "cache_v15b/mitdb"                    # ← 캐시 저장 위치(새로 빌드)
OUT     = "results"


# ===== v14_core (데이터빌드+프리미티브+학습) =====

# ══════════════════════════════════════════════════════════════════════════
#  0. 상수 (로컬 v13 globals 그대로)
# ══════════════════════════════════════════════════════════════════════════
FS          = 360
WIN_BEFORE, WIN_AFTER = 150, 150
INPUT_LEN   = 300
PWAVE_LO, PWAVE_HI = -0.22, -0.07          # P파 창 (초, R 기준)
QRS_LO, QRS_HI     = -0.08, 0.08
PRE_LO, PRE_HI     = -0.6, -0.1            # 적분 pre 구간
POST_LO, POST_HI   =  0.1,  0.6
RR_POW      = 2.0 / 3.0                    # RR^(2/3) 정규화 지수
REF_RR      = 0.8                          # 기준 RR (초)
LOCAL_K     = 10                           # 리듬 국소 창
N_PW, N_RHY, N_INT = 3, 5, 6
N_RR, N_SIM, N_CTX = 7, 9, 8
CTX_BEATS   = 9
N_CLASSES   = 3
CW_CAP      = 15.0

CLASSES = ["N", "S", "V"]; C2I = {c: i for i, c in enumerate(CLASSES)}
AAMI = {  # MIT-BIH 심볼 → AAMI 슈퍼클래스 (N/S/V 만 사용, F/Q 는 제외)
    "N":"N","L":"N","R":"N","e":"N","j":"N",
    "A":"S","a":"S","J":"S","S":"S",
    "V":"V","E":"V",
}
DS1 = ["101","106","108","109","112","114","115","116","118","119","122","124",
       "201","203","205","207","208","209","215","220","223","230"]
DS2 = ["100","103","105","111","113","117","121","123","200","202","210","212",
       "213","214","219","221","222","228","231","232","233","234"]


# ══════════════════════════════════════════════════════════════════════════
#  1. 데이터 빌드 (raw MIT-BIH → 특징 캐시)   ※ 재구현본
#     로컬 v13 의 pwave/rhythm/integral.py 와 수치가 정확히 같지는 않다.
#     노트북 안에서 모든 arm 이 이 캐시를 공유하므로 arm 간 비교는 유효.
# ══════════════════════════════════════════════════════════════════════════
def _bandpass(x, lo=0.5, hi=40, fs=FS):
    from scipy.signal import butter, filtfilt
    b, a = butter(3, [lo/(fs/2), hi/(fs/2)], btype="band")
    return filtfilt(b, a, x)

def _seg(sig, c, lo, hi):
    """R-peak(index c) 기준 [lo,hi]초 구간을 잘라 반환 (경계 클립)."""
    a = max(0, c + int(round(lo*FS))); b = min(len(sig), c + int(round(hi*FS)))
    return sig[a:b] if b > a else sig[c:c+1]

def build_cache(cache_dir, records=None, download=True):
    """PhysioNet 에서 mitdb 를 받아 record별 npz + meta.json 생성."""
    import wfdb
    os.makedirs(cache_dir, exist_ok=True)
    recs = records or (DS1 + DS2)
    meta = {}
    for r in recs:
        split = "DS1" if r in DS1 else ("DS2" if r in DS2 else None)
        if split is None:
            continue
        try:
            if download:
                wfdb.dl_database("mitdb", cache_dir, records=[r], overwrite=False)
            rec = wfdb.rdrecord(os.path.join(cache_dir, r))
            ann = wfdb.rdann(os.path.join(cache_dir, r), "atr")
        except Exception as e:
            print(f"  [{r}] 다운로드/읽기 실패: {e}"); continue

        sig = rec.p_signal.astype("float32")                 # (T, n_lead)
        n_lead = sig.shape[1]
        lead2 = sig[:, 1] if n_lead > 1 else sig[:, 0]
        s0 = _bandpass(sig[:, 0]); s1 = _bandpass(lead2)
        s0 = (s0 - s0.mean()) / (s0.std() + 1e-6)
        s1 = (s1 - s1.mean()) / (s1.std() + 1e-6)

        # 유효 비트만 (AAMI N/S/V)
        rpks, labs = [], []
        for pos, sym in zip(ann.sample, ann.symbol):
            if sym in AAMI and WIN_BEFORE <= pos < len(s0)-WIN_AFTER:
                rpks.append(int(pos)); labs.append(C2I[AAMI[sym]])
        if len(rpks) < 5:
            continue
        rpks = np.asarray(rpks); labs = np.asarray(labs, "int64")
        rr_all = np.diff(rpks) / FS                          # 초
        rr_all = np.concatenate([[rr_all[0]], rr_all])       # pre-RR (첫 비트 보정)
        post = np.concatenate([rr_all[1:], [rr_all[-1]]])    # post-RR

        beats, refs, rrf, simf = [], [], [], []
        pwf, pwf_n, rhyf, intf, intf_nn, ctxf = [], [], [], [], [], []

        # 정상 비트 템플릿(환자 median) — comparison/ref 용
        norm_idx = np.where(labs == 0)[0]
        def window(c):
            w0 = np.stack([s0[c-WIN_BEFORE:c+WIN_AFTER],
                           s1[c-WIN_BEFORE:c+WIN_AFTER]], -1)  # (300,2)
            return w0
        if len(norm_idx) > 0:
            templ = np.median(np.stack([window(rpks[i]) for i in norm_idx[:200]]), 0)
        else:
            templ = np.zeros((INPUT_LEN, 2), "float32")

        for k, c in enumerate(rpks):
            w = window(c).astype("float32")
            beats.append(w); refs.append(templ.astype("float32"))
            pre, po = rr_all[k], post[k]

            # rr (N_RR=7): pre, post, ratio, Δ, 국소평균, 국소편차, pre/local
            lo = max(0, k-LOCAL_K); loc = rr_all[lo:k+1]
            lm, ls = float(loc.mean()), float(loc.std()+1e-6)
            rrf.append([pre, po, po/(pre+1e-6), po-pre, lm, ls, pre/(lm+1e-6)])

            # sim (N_SIM=9): beat vs templ 상관/거리 (구간별)
            def corr(a, b):
                a = a.ravel()-a.mean(); b = b.ravel()-b.mean()
                return float((a@b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-6))
            qrs_a = _seg(s0, c, QRS_LO, QRS_HI)
            tq    = templ[WIN_BEFORE+int(QRS_LO*FS):WIN_BEFORE+int(QRS_HI*FS), 0]
            L = min(len(qrs_a), len(tq)); L = max(L, 1)
            simf.append([corr(w[:,0], templ[:,0]), corr(w[:,1], templ[:,1]),
                         corr(w[:,0], templ[:,1]),
                         float(np.mean((w[:,0]-templ[:,0])**2)),
                         float(np.mean((w[:,1]-templ[:,1])**2)),
                         corr(qrs_a[:L], tq[:L]),
                         float(np.abs(w[:,0]).max()), float(np.abs(w[:,1]).max()),
                         float(w[:,0].std())])

            # pw (N_PW=3): P파 창 에너지/진폭/기울기 — 고정창 vs RR정규화창
            def pw_feats(scale):
                lo_s = PWAVE_LO*scale; hi_s = PWAVE_HI*scale
                seg = _seg(s0, c, lo_s, hi_s)
                if len(seg) < 2: return [0.,0.,0.]
                return [float(np.abs(seg).mean()), float(seg.max()-seg.min()),
                        float(np.abs(np.diff(seg)).mean())]
            pwf.append(pw_feats(1.0))
            pwf_n.append(pw_feats((pre/REF_RR)**RR_POW))     # RR^(2/3) 정규화

            # rhy (N_RHY=5): 리듬 규칙성 (222형 겨냥)
            cv = ls/(lm+1e-6)
            short_long = float((pre < 0.85*lm)) - float((pre > 1.15*lm))
            rhyf.append([cv, short_long, (pre-lm)/(ls), (po-lm)/(ls),
                         float(np.abs(np.diff(loc)).mean()) if len(loc)>1 else 0.])

            # intg (N_INT=6): 적분(면적) 편차 vs 정상 — detrend 후 적분
            def integ(scale):
                out = []
                for (lo_, hi_) in [(PRE_LO,PRE_HI),(POST_LO,POST_HI),(QRS_LO,QRS_HI)]:
                    seg = _seg(s0, c, lo_*scale, hi_*scale).astype("float64")
                    if len(seg) > 2:                          # detrend (222 baseline)
                        t = np.linspace(0,1,len(seg)); A = np.vstack([t,np.ones_like(t)]).T
                        seg = seg - A @ np.linalg.lstsq(A, seg, rcond=None)[0]
                    out.append(float(np.trapz(seg)/FS))
                pre_i, post_i, qrs_i = out
                asym = (pre_i - post_i)
                ratio = pre_i/(post_i+1e-6)
                pwin = _seg(s0, c, PWAVE_LO*scale, PWAVE_HI*scale)
                pabs = float(np.abs(pwin).sum()/FS)
                return [pre_i, post_i, qrs_i, ratio, asym, pabs]
            intf.append(integ((pre/REF_RR)**RR_POW))          # 정규화 ON
            intf_nn.append(integ(1.0))                        # 정규화 OFF

            # ctx (CTX_BEATS,N_CTX): 미사용(uctx=False) — 0 채움
            ctxf.append(np.zeros((CTX_BEATS, N_CTX), "float32"))

        d = dict(
            beat=np.asarray(beats,"float32"), ref=np.asarray(refs,"float32"),
            rr=np.asarray(rrf,"float32"), sim=np.asarray(simf,"float32"),
            pw=np.asarray(pwf,"float32"), pw_norm=np.asarray(pwf_n,"float32"),
            rhy=np.asarray(rhyf,"float32"),
            intg=np.asarray(intf,"float32"), intg_nonorm=np.asarray(intf_nn,"float32"),
            ctx=np.asarray(ctxf,"float32"), y=labs)
        # NaN/inf 방어
        for k in d:
            if d[k].dtype.kind == "f":
                d[k] = np.nan_to_num(d[k], nan=0., posinf=0., neginf=0.)
        np.savez_compressed(os.path.join(cache_dir, f"{r}.npz"), **d)
        meta[r] = {"split": split, "n": int(len(labs)),
                   "nS": int((labs==1).sum()), "nV": int((labs==2).sum())}
        print(f"  [{r}] {split}  n={len(labs)}  S={meta[r]['nS']}  V={meta[r]['nV']}")
    json.dump(meta, open(os.path.join(cache_dir, "meta.json"), "w"), indent=1)
    print("meta.json 저장:", cache_dir)
    return meta


def load_split(cache, split):
    meta = json.load(open(os.path.join(cache, "meta.json")))
    recs = sorted(r for r, m in meta.items() if m["split"] == split)
    keys = ["beat","ref","rr","sim","pw","rhy","intg","intg_nonorm","pw_norm","ctx","y"]
    acc = {k: [] for k in keys}; pid = []
    for r in recs:
        d = np.load(os.path.join(cache, f"{r}.npz"))
        for k in keys: acc[k].append(d[k])
        pid.append(np.full(d["y"].size, int(r)))
    out = {k: np.concatenate(v, 0) for k, v in acc.items()}
    out["pid"] = np.concatenate(pid)
    return out


# ══════════════════════════════════════════════════════════════════════════
#  2. 모델 프리미티브 (재구현: _encoder / AbsLayer / PrototypeBank / metrics)
# ══════════════════════════════════════════════════════════════════════════
class AbsLayer(layers.Layer):
    def call(self, x): return keras.ops.abs(x)

class PrototypeBank(layers.Layer):
    """학습형 프로토타입 뱅크: z 에 대해 프로토타입 어텐션 가중합 반환(같은 차원)."""
    def __init__(self, n_proto=32, **kw):
        super().__init__(**kw); self.n_proto = n_proto
    def build(self, s):
        self.dim = s[-1]
        self.P = self.add_weight(shape=(self.n_proto, self.dim),
                                 initializer="glorot_uniform", trainable=True, name="proto")
    def call(self, z):
        att = keras.ops.softmax(keras.ops.matmul(z, keras.ops.transpose(self.P))
                                / (self.dim ** 0.5), axis=-1)      # (B, n_proto)
        return keras.ops.matmul(att, self.P)                       # (B, dim)
    def get_config(self):
        c = super().get_config(); c["n_proto"] = self.n_proto; return c

def _encoder(n_ch=2):
    """(INPUT_LEN, n_ch) → 64d 임베딩 1D-CNN. beat/ref 가 공유(Siamese)."""
    inp = layers.Input((INPUT_LEN, n_ch))
    x = layers.Conv1D(32, 7, padding="same", activation="relu")(inp)
    x = layers.BatchNormalization()(x); x = layers.MaxPool1D(2)(x)
    x = layers.Conv1D(64, 5, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x); x = layers.MaxPool1D(2)(x)
    x = layers.Conv1D(128, 3, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x); x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dense(64, activation="relu")(x)
    return keras.Model(inp, x, name="enc")

def metrics(y, prob):
    y = np.asarray(y); pred = prob.argmax(1)
    p, r, f, _ = precision_recall_fscore_support(y, pred, labels=[0,1,2],
                                                 zero_division=0, average=None)
    yS = (y == 1).astype(int)
    return dict(
        S_prauc = float(average_precision_score(yS, prob[:,1])) if yS.sum() else 0.,
        S_rocauc= float(roc_auc_score(yS, prob[:,1])) if 0 < yS.sum() < len(yS) else 0.,
        S_f1=float(f[1]), S_prec=float(p[1]), S_rec=float(r[1]),
        macro_f1=float(f1_score(y, pred, labels=[0,1,2], average="macro", zero_division=0)),
        N_f1=float(f[0]), V_f1=float(f[2]))


# ══════════════════════════════════════════════════════════════════════════
#  3. arm 정의
# ══════════════════════════════════════════════════════════════════════════
#          (use_compare, use_ctx, use_proto, use_pw, use_rhy, use_intg)
ARMS = {
    "base":         (True, False, True, True,  True,  False),
    "integ":        (True, False, True, True,  True,  True),
    "integ_full":   (True, False, True, True,  True,  True),
    "two_view_moe":    (True, False, True, True, True, True),   # 구조 A
    "two_view_2class": (True, False, True, True, True, True),   # 구조 B
}
RR_NORM = {                       # (적분정규화, pwave창정규화)
    "base":         (True,  False),
    "integ":        (True,  False),
    "integ_full":   (True,  True),
    "two_view_moe":    (True, True),
    "two_view_2class": (True, True),
}
def arm_inputs(arm):
    uc, uctx, upr, upw, urhy, uintg = ARMS[arm]
    keys = ["beat", "rr", "sim"]
    if uc: keys.insert(1, "ref")
    if upw: keys.append("pw")
    if urhy: keys.append("rhy")
    if uintg: keys.append("intg")
    if uctx: keys.append("ctx")
    return keys


# ══════════════════════════════════════════════════════════════════════════
#  4. build_model — 단일 concat arm + two_view 두 종류
# ══════════════════════════════════════════════════════════════════════════
def _mlp(inp, u1, u2):
    h = layers.Dense(u1, activation="relu")(layers.BatchNormalization()(inp))
    return layers.Dense(u2, activation="relu")(layers.Dropout(0.2)(h))

def _v_view(n_proto):
    """형태 view: beat/ref(Siamese)/sim/proto. 정규화 특징 안 닿음. → (repr, inputs)"""
    encV = _encoder(2)
    xi  = layers.Input((INPUT_LEN,2), name="beat")
    rfi = layers.Input((INPUT_LEN,2), name="ref")
    si  = layers.Input((N_SIM,), name="sim")
    zx, zr = encV(xi), encV(rfi)
    d = layers.Subtract()([zx, zr])
    mf = layers.Dense(64, activation="relu")(layers.Concatenate()([zx, zr, d, AbsLayer()(d)]))
    s  = layers.Dense(16, activation="relu")(layers.BatchNormalization()(si))
    vz = layers.Dense(64, activation="relu")(layers.Concatenate()([mf, s]))
    zb = PrototypeBank(n_proto)(vz)
    g  = layers.Dense(64, activation="sigmoid")(layers.Concatenate()([vz, zb]))
    vz = layers.Dropout(0.4)(layers.Add()([vz, layers.Multiply()([g, zb])]))
    return vz, {"beat":xi, "ref":rfi, "sim":si}

def _s_view():
    """타이밍·P파 view: rr/pw(norm)/rhy/intg(norm). → (repr, inputs)"""
    ri  = layers.Input((N_RR,), name="rr")
    pi  = layers.Input((N_PW,), name="pw")
    rhi = layers.Input((N_RHY,), name="rhy")
    ii  = layers.Input((N_INT,), name="intg")
    sz = layers.Dense(64, activation="relu")(layers.Concatenate()(
            [_mlp(ri,32,32), _mlp(pi,24,16), _mlp(rhi,24,16), _mlp(ii,24,16)]))
    sz = layers.Dropout(0.4)(sz)
    return sz, {"rr":ri, "pw":pi, "rhy":rhi, "intg":ii}

def build_model(arm="integ", n_proto=32, lr=1e-3):
    # ---------- two_view_moe : 확률공간 MoE 게이트 + view별 보조손실 ----------
    if arm == "two_view_moe":
        vz, vin = _v_view(n_proto); sz, sin = _s_view()
        v_prob = layers.Dense(N_CLASSES, activation="softmax", name="v_aux")(vz)
        s_prob = layers.Dense(N_CLASSES, activation="softmax", name="s_aux")(sz)
        g_V = layers.Dense(1, activation="sigmoid", name="gate_v")(vz)  # V-view 표현에서만
        final = layers.Add(name="final")([
            layers.Multiply()([g_V, v_prob]),
            layers.Multiply()([layers.Lambda(lambda t: 1.0 - t)(g_V), s_prob])])
        inp = {**vin, **sin}
        m = keras.Model([inp[k] for k in arm_inputs(arm)],
                        {"final":final, "v_aux":v_prob, "s_aux":s_prob}, name="tv_moe")
        m.compile(keras.optimizers.Adam(lr),
                  loss={"final":"sparse_categorical_crossentropy",
                        "v_aux":"sparse_categorical_crossentropy",
                        "s_aux":"sparse_categorical_crossentropy"},
                  loss_weights={"final":1.0, "v_aux":0.3, "s_aux":0.3},
                  metrics={"final":"accuracy"}, jit_compile=False)
        return m

    # ---------- two_view_2class : 계층 라우팅 (V=형태, S=타이밍) ----------
    if arm == "two_view_2class":
        vz, vin = _v_view(n_proto); sz, sin = _s_view()
        pV = layers.Dense(1, activation="sigmoid", name="v_aux")(vz)    # P(V)  ← 형태
        pS = layers.Dense(1, activation="sigmoid", name="s_gate")(sz)   # P(S | ¬V) ← 타이밍
        # 3-class 합성:  V=pV,  S=(1-pV)·pS,  N=(1-pV)·(1-pS)
        one = layers.Lambda(lambda t: 1.0 - t)
        PN = layers.Multiply()([one(pV), one(pS)])
        PS = layers.Multiply()([one(pV), pS])
        PV = pV
        final = layers.Concatenate(name="final")([PN, PS, PV])          # (B,3), 합=1
        final = layers.Lambda(lambda p: keras.ops.clip(p, 1e-7, 1.0),
                              name="final_clip")(final)
        inp = {**vin, **sin}
        m = keras.Model([inp[k] for k in arm_inputs(arm)],
                        {"final":final, "v_aux":pV}, name="tv_2class")
        m.compile(keras.optimizers.Adam(lr),
                  loss={"final":"sparse_categorical_crossentropy",   # 합성 확률에 NLL
                        "v_aux":"binary_crossentropy"},              # V 탐지기 보조
                  loss_weights={"final":1.0, "v_aux":0.3},
                  metrics={"final":"accuracy"}, jit_compile=False)
        return m

    # ---------- 단일 concat arm (base / integ / integ_full) ----------
    uc, uctx, upr, upw, urhy, uintg = ARMS[arm]
    enc = _encoder(2)
    xi = layers.Input((INPUT_LEN,2), name="beat")
    ri = layers.Input((N_RR,), name="rr"); si = layers.Input((N_SIM,), name="sim")
    z1 = enc(xi); parts = [z1]; inputs = [xi]
    if uc:
        rfi = layers.Input((INPUT_LEN,2), name="ref"); inputs.append(rfi)
        z2 = enc(rfi); d = layers.Subtract()([z1, z2]); parts += [z2, d, AbsLayer()(d)]
    inputs += [ri, si]
    mf = layers.Concatenate()(parts) if len(parts) > 1 else z1
    mf = layers.Dense(64, activation="relu")(mf)
    r = layers.Dense(32, activation="relu")(layers.BatchNormalization()(ri))
    r = layers.Dense(32, activation="relu")(layers.Dropout(0.2)(r))
    s = layers.Dense(16, activation="relu")(layers.BatchNormalization()(si))
    branches = [mf, r, s]
    if upw:
        pi = layers.Input((N_PW,), name="pw"); inputs.append(pi); branches.append(_mlp(pi,24,16))
    if urhy:
        rhi = layers.Input((N_RHY,), name="rhy"); inputs.append(rhi); branches.append(_mlp(rhi,24,16))
    if uintg:
        ii = layers.Input((N_INT,), name="intg"); inputs.append(ii); branches.append(_mlp(ii,24,16))
    if uctx:
        ci = layers.Input((CTX_BEATS,N_CTX), name="ctx"); inputs.append(ci)
        branches.append(layers.Dense(32,activation="relu")(layers.Bidirectional(layers.GRU(24))(ci)))
    z = layers.Dense(64, activation="relu")(layers.Concatenate()(branches))
    if upr:
        zb = PrototypeBank(n_proto)(z)
        g = layers.Dense(64, activation="sigmoid")(layers.Concatenate()([z, zb]))
        z = layers.Add()([z, layers.Multiply()([g, zb])])
    z = layers.Dropout(0.4)(z)
    out = layers.Dense(N_CLASSES, activation="softmax")(z)
    by = {i.name.split(":")[0]: i for i in inputs}
    m = keras.Model([by[k] for k in arm_inputs(arm)], out, name=f"v14_{arm}")
    m.compile(keras.optimizers.Adam(lr), "sparse_categorical_crossentropy",
              metrics=["accuracy"], jit_compile=False)
    return m


# ══════════════════════════════════════════════════════════════════════════
#  5. 학습 / 실행
# ══════════════════════════════════════════════════════════════════════════
def capped_cw(y):
    w = compute_class_weight("balanced", classes=np.arange(3), y=y)
    w = np.clip(w, 1.0/CW_CAP, CW_CAP)
    return {int(i): float(v) for i, v in enumerate(w)}

def val_patients(pid, y, seed, frac=0.2, min_train_S=200):
    pats = np.unique(pid)
    s_by = {p: int(((pid==p)&(y==1)).sum()) for p in pats}
    tot_S = max(sum(s_by.values()), 1); n_val = max(2, int(round(len(pats)*frac)))
    rng = np.random.default_rng(seed); best, bs = None, -1
    for _ in range(500):
        pick = rng.choice(pats, size=n_val, replace=False)
        vS = sum(s_by[p] for p in pick); tS = tot_S - vS
        if tS >= min_train_S and vS >= 1: return set(pick.tolist())
        sc = min(tS, min_train_S) - abs(vS - 30)
        if sc > bs: bs, best = sc, set(pick.tolist())
    return best

# two_view arm 의 보조 타깃 구성
def _targets(arm, y):
    if arm == "two_view_moe":
        return {"final":y, "v_aux":y, "s_aux":y}
    if arm == "two_view_2class":
        return {"final":y, "v_aux":(y==2).astype("float32")}  # V 탐지 이진
    return y

def train_one(cache, arm, seed, epochs=25, batch=128, verbose=0):
    keras.utils.set_random_seed(seed)
    tr = load_split(cache, "DS1"); te = load_split(cache, "DS2")
    keys = arm_inputs(arm)
    intg_norm, pw_norm = RR_NORM.get(arm, (True, False))
    def pick(d, k):
        if k == "intg": return d["intg" if intg_norm else "intg_nonorm"]
        if k == "pw" and pw_norm: return d["pw_norm"]
        return d[k]
    vp = val_patients(tr["pid"], tr["y"].astype(int), seed)
    vm = np.isin(tr["pid"], list(vp))
    Xtr = {k: pick(tr,k)[~vm] for k in keys}; Xva = {k: pick(tr,k)[vm] for k in keys}
    Xte = {k: pick(te,k) for k in keys}
    ytr, yva, yte = tr["y"][~vm].astype(int), tr["y"][vm].astype(int), te["y"].astype(int)
    W = capped_cw(ytr)
    sw = np.array([W[c] for c in ytr], "float32"); swv = np.array([W[c] for c in yva], "float32")
    m = build_model(arm)
    multi = arm.startswith("two_view")
    if multi:
        mon = "val_final_loss"
        # sample_weight: 모든 출력에 동일 가중(딕셔너리)
        okeys = ["final","v_aux"] + (["s_aux"] if arm=="two_view_moe" else [])
        sw_d  = {k: sw  for k in okeys};  swv_d = {k: swv for k in okeys}
        h = m.fit(Xtr, _targets(arm, ytr), sample_weight=sw_d,
                  validation_data=(Xva, _targets(arm, yva), swv_d),
                  epochs=epochs, batch_size=batch,
                  callbacks=[keras.callbacks.EarlyStopping(mon, mode="min", patience=6, restore_best_weights=True),
                             keras.callbacks.ReduceLROnPlateau(mon, mode="min", factor=0.5, patience=3)],
                  verbose=verbose)
        prob = m.predict(Xte, batch_size=1024, verbose=0)["final"]
    else:
        mon = "val_loss"
        h = m.fit(Xtr, ytr, validation_data=(Xva, yva, swv),
                  epochs=epochs, batch_size=batch, class_weight=W,
                  callbacks=[keras.callbacks.EarlyStopping(mon, patience=6, restore_best_weights=True),
                             keras.callbacks.ReduceLROnPlateau(mon, factor=0.5, patience=3)],
                  verbose=verbose)
        prob = m.predict(Xte, batch_size=1024, verbose=0)
    info = dict(params=m.count_params(), n_ep=len(h.history[mon]),
                best_ep=int(np.argmin(h.history[mon])),
                train_S=int((ytr==1).sum()), val_S=int((yva==1).sum()), w_S=round(W[1],2))
    return prob, yte, te["pid"], info

def run(cache, arms, seeds, out_dir, epochs=25, batch=128, verbose=0):
    os.makedirs(out_dir, exist_ok=True)
    for arm in arms:
        assert arm in ARMS, f"unknown arm {arm}"
        rows = []
        for sd in seeds:
            t0 = time.time()
            prob, y, pid, info = train_one(cache, arm, sd, epochs, batch, verbose)
            np.savez_compressed(os.path.join(out_dir, f"{arm}_s{sd}.npz"), prob=prob, y=y, pid=pid)
            mt = metrics(y, prob); mt.update(arm=arm, seed=sd, sec=round(time.time()-t0,1), **info)
            rows.append(mt)
            print(f"[{arm} s{sd}] S_PR-AUC={mt['S_prauc']:.4f} S_F1={mt['S_f1']:.4f} "
                  f"macro={mt['macro_f1']:.4f} V_F1={mt['V_f1']:.3f} | ep {mt['best_ep']}/{mt['n_ep']} "
                  f"valS={mt['val_S']} ({mt['sec']:.0f}s)", flush=True)
        json.dump(rows, open(os.path.join(out_dir, f"{arm}_metrics.json"), "w"), indent=1)
        pr = np.array([r["S_prauc"] for r in rows])
        print(f"  → {arm}: S PR-AUC {pr.mean():.4f}±{pr.std(ddof=1) if pr.size>1 else 0:.4f}\n")


# ===== v15 (P signed-area) =====
# ═══════════════════════════════════════════════════════════════════════════
#  v15 — P signed-area(극성) 특징 추가.  게이트 없이 base 에 덧셈 브랜치.
#  진단 확증: signed-area 가 222(AUC 0.762)·200(AUC 0.817) 을 동시에 분리.
#  v14 노트북(CELL 0~8)이 실행된 커널에서 이 셀 하나만 실행 → v15 확장 설치.
# ═══════════════════════════════════════════════════════════════════════════
import os, json, glob
# v14 전역 심볼 사용: FS, INPUT_LEN, WIN_BEFORE, PWAVE_LO/HI, RR_POW, REF_RR,
#   N_PW/RHY/INT/RR/SIM/CTX, CTX_BEATS, N_CLASSES, _seg, _encoder, _mlp,
#   AbsLayer, PrototypeBank, ARMS, RR_NORM, build_model, load_split, run

N_PSA = 4
TP_LO, TP_HI = -0.38, -0.26          # TP/PR segment (baseline 추정용, 초)

# ── learnable-baseline 프록시 + P signed-area 추출 ──────────────────────────
def _baseline(sig1d, c):
    """등전위선 추정: TP segment 중앙값 + QRS직전 전압을, TP 평탄도로 가중결합."""
    tp = _seg(sig1d, c, TP_LO, TP_HI)
    tp_bl = float(np.median(tp)) if len(tp) else 0.0
    pre = _seg(sig1d, c, -0.05, -0.02)
    pq_bl = float(np.median(pre)) if len(pre) else tp_bl
    flat = 1.0 / (1.0 + (float(np.std(tp)) if len(tp) else 1.0))
    return flat * tp_bl + (1 - flat) * pq_bl

def psa_feats(sig1d, c, pre_rr):
    """P파 창의 baseline 대비 signed-area(극성) 4종. RR^(2/3) 정규화."""
    scale = (max(float(pre_rr), 1e-3) / REF_RR) ** RR_POW   # pre_rr>0 보장(복소수 방지)
    bl = _baseline(sig1d, c)
    w = _seg(sig1d, c, PWAVE_LO * scale, PWAVE_HI * scale).astype("float64") - bl
    if len(w) < 3:
        return [0., 0., 0., 0.]
    trap = (np.trapezoid if hasattr(np,"trapezoid") else np.trapz)
    signed = float(trap(w) / FS)                          # 부호적분(극성)
    pos = float(trap(np.clip(w, 0, None)) / FS)
    neg = float(trap(np.clip(w, None, 0)) / FS)
    asym = (pos + neg) / (pos - neg + 1e-6)               # -1(완전inverted)~+1
    return [signed, pos, neg, asym]

# ── 기존 캐시에 psa 키만 추가 (재다운로드 불필요) ───────────────────────────
def migrate_add_psa(cache_dir):
    meta = json.load(open(os.path.join(cache_dir, "meta.json")))
    trap = (np.trapezoid if hasattr(np,"trapezoid") else np.trapz)
    n_done = 0
    for r in meta:
        p = os.path.join(cache_dir, f"{r}.npz")
        d = dict(np.load(p))
        if "psa" in d:
            continue
        beat, rr = d["beat"], d["rr"]; n = beat.shape[0]
        psa = np.zeros((n, N_PSA), "float32")
        for i in range(n):                                # 캐시 윈도우(R=WIN_BEFORE) 사용
            psa[i] = psa_feats(beat[i, :, 0], WIN_BEFORE, float(rr[i, 0]))
        d["psa"] = np.nan_to_num(psa, nan=0., posinf=0., neginf=0.)
        np.savez_compressed(p, **d); n_done += 1
    print(f"psa 마이그레이션: {cache_dir}  ({n_done}개 record 갱신, +{N_PSA}차원)")

# ── psa 포함 load_split ─────────────────────────────────────────────────────
def load_split_v15(cache, split):
    meta = json.load(open(os.path.join(cache, "meta.json")))
    recs = sorted(r for r, m in meta.items() if m["split"] == split)
    keys = ["beat","ref","rr","sim","pw","rhy","intg","intg_nonorm","pw_norm","ctx","psa","y"]
    acc = {k: [] for k in keys}; pid = []
    for r in recs:
        d = np.load(os.path.join(cache, f"{r}.npz"))
        for k in keys:
            acc[k].append(d[k] if k in d.files else np.zeros((d["y"].size, N_PSA), "float32"))
        pid.append(np.full(d["y"].size, int(r)))
    out = {k: np.concatenate(v, 0) for k, v in acc.items()}
    out["pid"] = np.concatenate(pid); return out

# ── arm / 모델 확장 ─────────────────────────────────────────────────────────
PSA_ARMS = {"base_psa", "integ_psa"}

def arm_inputs_v15(arm):
    uc, uctx, upr, upw, urhy, uintg = ARMS[arm]
    keys = ["beat", "rr", "sim"]
    if uc: keys.insert(1, "ref")
    if upw: keys.append("pw")
    if urhy: keys.append("rhy")
    if uintg: keys.append("intg")
    if uctx: keys.append("ctx")
    if arm in PSA_ARMS: keys.append("psa")
    return keys

def build_model_v15(arm="base_psa", n_proto=32, lr=1e-3):
    uintg = (arm == "integ_psa")
    enc = _encoder(2)
    xi = layers.Input((INPUT_LEN,2), name="beat")
    ri = layers.Input((N_RR,), name="rr"); si = layers.Input((N_SIM,), name="sim")
    z1 = enc(xi); inputs = [xi]
    rfi = layers.Input((INPUT_LEN,2), name="ref"); inputs.append(rfi)
    z2 = enc(rfi); d = layers.Subtract()([z1, z2])
    mf = layers.Dense(64, activation="relu")(layers.Concatenate()([z1, z2, d, AbsLayer()(d)]))
    inputs += [ri, si]
    r = layers.Dense(32, activation="relu")(layers.BatchNormalization()(ri))
    r = layers.Dense(32, activation="relu")(layers.Dropout(0.2)(r))
    s = layers.Dense(16, activation="relu")(layers.BatchNormalization()(si))
    branches = [mf, r, s]
    pi = layers.Input((N_PW,), name="pw"); inputs.append(pi); branches.append(_mlp(pi,24,16))
    rhi = layers.Input((N_RHY,), name="rhy"); inputs.append(rhi); branches.append(_mlp(rhi,24,16))
    if uintg:
        ii = layers.Input((N_INT,), name="intg"); inputs.append(ii); branches.append(_mlp(ii,24,16))
    psi = layers.Input((N_PSA,), name="psa"); inputs.append(psi)         # ★ v15
    branches.append(_mlp(psi, 16, 12))
    z = layers.Dense(64, activation="relu")(layers.Concatenate()(branches))
    zb = PrototypeBank(n_proto)(z)
    g = layers.Dense(64, activation="sigmoid")(layers.Concatenate()([z, zb]))
    z = layers.Add()([z, layers.Multiply()([g, zb])])
    z = layers.Dropout(0.4)(z)
    out = layers.Dense(N_CLASSES, activation="softmax")(z)
    by = {i.name.split(":")[0]: i for i in inputs}
    m = keras.Model([by[k] for k in arm_inputs_v15(arm)], out, name=f"v15_{arm}")
    m.compile(keras.optimizers.Adam(lr), "sparse_categorical_crossentropy",
              metrics=["accuracy"], jit_compile=False)
    return m

# ── 설치: 전역 심볼 교체 + psa arm 등록 ─────────────────────────────────────
ARMS["base_psa"]  = ARMS["base"]
ARMS["integ_psa"] = ARMS["integ"]
RR_NORM["base_psa"]  = (True, True)
RR_NORM["integ_psa"] = (True, True)

if not globals().get("_V15_INSTALLED", False):
    _orig_build_model_v15 = build_model
    _V15_INSTALLED = True

def arm_inputs(arm): return arm_inputs_v15(arm)
def load_split(cache, split): return load_split_v15(cache, split)
def build_model(arm="integ", n_proto=32, lr=1e-3):
    if arm in ("base_psa","integ_psa"): return build_model_v15(arm, n_proto, lr)
    return _orig_build_model_v15(arm, n_proto, lr)

print("v15 설치 완료.  arm_inputs(base_psa) =", arm_inputs("base_psa"))

# ===== v15b (자기대비 상대화 psa_rel) =====
# ═══════════════════════════════════════════════════════════════════════════
#  v15b — psa 자기대비 상대화 (개선 A).  base_psa2 arm.
#  각 환자 정상비트 median psa 를 빼서 "본인 정상 대비 P극성 이탈"로.
#  → 환자별 baseline 오프셋 상쇄 (v8 comparison 원리를 psa 에).
#  v15 셀(psa_feats, migrate_add_psa, N_PSA 등)이 이미 실행된 커널에서 이 셀 실행.
# ═══════════════════════════════════════════════════════════════════════════
import os, json, glob

# ── 캐시에 psa_rel(자기대비 상대 psa) 추가 ─────────────────────────────────
#   record 단위로 정상(y==0) 비트의 median psa 를 구해 전체 psa 에서 뺀다.
#   inter-patient 안전: 기준(median)은 그 환자 자신의 정상비트에서만 계산 →
#   test 환자도 자기 데이터 안에서 자기 기준을 쓰므로 라벨/누수 문제 없음
#   (정상비트는 압도적 다수라 비지도적으로 얻는다고 봐도 됨).
def migrate_add_psa_rel(cache_dir):
    meta = json.load(open(os.path.join(cache_dir, "meta.json")))
    n_done = 0
    for r in meta:
        p = os.path.join(cache_dir, f"{r}.npz")
        d = dict(np.load(p))
        assert "psa" in d, f"{r}: psa 없음 — 먼저 migrate_add_psa(CACHE) 실행"
        if "psa_rel" in d:
            continue
        psa = d["psa"]; y = d["y"]
        Nmask = (y == 0)
        # 이 환자 정상비트 median 을 기준선으로 (정상 없으면 전체 median)
        base_ref = np.median(psa[Nmask], axis=0) if Nmask.sum() >= 5 else np.median(psa, axis=0)
        d["psa_rel"] = (psa - base_ref).astype("float32")
        np.savez_compressed(p, **d); n_done += 1
    print(f"psa_rel 마이그레이션: {cache_dir}  ({n_done}개 record, 자기대비 상대화)")

# ── load_split 을 psa_rel 포함하도록 재정의 ─────────────────────────────────
def load_split_v15b(cache, split):
    meta = json.load(open(os.path.join(cache, "meta.json")))
    recs = sorted(r for r, m in meta.items() if m["split"] == split)
    keys = ["beat","ref","rr","sim","pw","rhy","intg","intg_nonorm","pw_norm",
            "ctx","psa","psa_rel","y"]
    acc = {k: [] for k in keys}; pid = []
    for r in recs:
        d = np.load(os.path.join(cache, f"{r}.npz"))
        for k in keys:
            acc[k].append(d[k] if k in d.files else np.zeros((d["y"].size, N_PSA), "float32"))
        pid.append(np.full(d["y"].size, int(r)))
    out = {k: np.concatenate(v, 0) for k, v in acc.items()}
    out["pid"] = np.concatenate(pid); return out

# ── arm / 모델 : base_psa2 = base + psa_rel 브랜치 (게이트 없음) ─────────────
PSA_ARMS  = {"base_psa", "integ_psa"}          # (v15) 절대 psa
PSA2_ARMS = {"base_psa2", "integ_psa2"}        # (v15b) 상대 psa_rel

def arm_inputs_v15b(arm):
    uc, uctx, upr, upw, urhy, uintg = ARMS[arm]
    keys = ["beat", "rr", "sim"]
    if uc: keys.insert(1, "ref")
    if upw: keys.append("pw")
    if urhy: keys.append("rhy")
    if uintg: keys.append("intg")
    if uctx: keys.append("ctx")
    if arm in PSA_ARMS:  keys.append("psa")
    if arm in PSA2_ARMS: keys.append("psa_rel")
    return keys

def build_model_v15b(arm="base_psa2", n_proto=32, lr=1e-3):
    uintg = arm in ("integ_psa", "integ_psa2")
    use_abs = arm in PSA_ARMS       # 절대 psa
    use_rel = arm in PSA2_ARMS      # 상대 psa_rel
    enc = _encoder(2)
    xi = layers.Input((INPUT_LEN,2), name="beat")
    ri = layers.Input((N_RR,), name="rr"); si = layers.Input((N_SIM,), name="sim")
    z1 = enc(xi); inputs = [xi]
    rfi = layers.Input((INPUT_LEN,2), name="ref"); inputs.append(rfi)
    z2 = enc(rfi); d = layers.Subtract()([z1, z2])
    mf = layers.Dense(64, activation="relu")(layers.Concatenate()([z1, z2, d, AbsLayer()(d)]))
    inputs += [ri, si]
    r = layers.Dense(32, activation="relu")(layers.BatchNormalization()(ri))
    r = layers.Dense(32, activation="relu")(layers.Dropout(0.2)(r))
    s = layers.Dense(16, activation="relu")(layers.BatchNormalization()(si))
    branches = [mf, r, s]
    pi = layers.Input((N_PW,), name="pw"); inputs.append(pi); branches.append(_mlp(pi,24,16))
    rhi = layers.Input((N_RHY,), name="rhy"); inputs.append(rhi); branches.append(_mlp(rhi,24,16))
    if uintg:
        ii = layers.Input((N_INT,), name="intg"); inputs.append(ii); branches.append(_mlp(ii,24,16))
    if use_abs:
        psi = layers.Input((N_PSA,), name="psa"); inputs.append(psi)
        branches.append(_mlp(psi, 16, 12))
    if use_rel:
        psr = layers.Input((N_PSA,), name="psa_rel"); inputs.append(psr)
        branches.append(_mlp(psr, 16, 12))
    z = layers.Dense(64, activation="relu")(layers.Concatenate()(branches))
    zb = PrototypeBank(n_proto)(z)
    g = layers.Dense(64, activation="sigmoid")(layers.Concatenate()([z, zb]))
    z = layers.Add()([z, layers.Multiply()([g, zb])])
    z = layers.Dropout(0.4)(z)
    out = layers.Dense(N_CLASSES, activation="softmax")(z)
    by = {i.name.split(":")[0]: i for i in inputs}
    m = keras.Model([by[k] for k in arm_inputs_v15b(arm)], out, name=f"v15b_{arm}")
    m.compile(keras.optimizers.Adam(lr), "sparse_categorical_crossentropy",
              metrics=["accuracy"], jit_compile=False)
    return m

# ── 설치 ────────────────────────────────────────────────────────────────────
ARMS["base_psa2"]   = ARMS["base"]
ARMS["integ_psa2"]  = ARMS["integ"]
RR_NORM["base_psa2"]  = (True, True)
RR_NORM["integ_psa2"] = (True, True)

if not globals().get("_V15B_INSTALLED", False):
    _prev_build_v15b = build_model     # 현재(=v15) build_model 을 원본으로
    _V15B_INSTALLED = True

def arm_inputs(arm): return arm_inputs_v15b(arm)
def load_split(cache, split): return load_split_v15b(cache, split)
def build_model(arm="integ", n_proto=32, lr=1e-3):
    if arm in ("base_psa2","integ_psa2","base_psa","integ_psa"):
        return build_model_v15b(arm, n_proto, lr)
    return _prev_build_v15b(arm, n_proto, lr)

print("v15b 설치 완료.  arm_inputs(base_psa2) =", arm_inputs("base_psa2"))

# ═══════════════════════════════════════════════════════════════════════════
#  200·222 판정
# ═══════════════════════════════════════════════════════════════════════════
def judge(out_dir, seeds):
    import statistics as st
    M = {}
    for a in ["base","base_psa2"]:
        p = os.path.join(out_dir, f"{a}_metrics.json")
        if os.path.exists(p): M[a] = {r["seed"]: r for r in json.load(open(p))}
    def mean(a,k): return st.mean(M[a][s][k] for s in seeds if s in M.get(a,{}))
    def paired(a,b,k):
        cs=[s for s in seeds if s in M.get(a,{}) and s in M.get(b,{})]
        if not cs: return None,0,0,0.0
        dz=[M[b][s][k]-M[a][s][k] for s in cs]
        return st.mean(dz), sum(x>0 for x in dz), len(cs), (st.pstdev(dz) if len(dz)>1 else 0.0)
    if not all(a in M for a in ["base","base_psa2"]):
        print("판정 불가 — metrics.json 부족"); return
    print("\n"+"="*64); print(f"전체 ({len([s for s in seeds if s in M['base']])}-seed)")
    print(f"{'arm':<12}{'S_prauc':>9}{'S_f1':>8}{'V_f1':>8}{'macro':>8}")
    for a in ["base","base_psa2"]:
        print(f"{a:<12}{mean(a,'S_prauc'):>9.3f}{mean(a,'S_f1'):>8.3f}{mean(a,'V_f1'):>8.3f}{mean(a,'macro_f1'):>8.3f}")
    md,w,n,sd = paired("base","base_psa2","S_prauc")
    ci = 1.96*sd/(n**0.5) if n>1 else 0
    print(f"\n  base→base_psa2  S_prauc Δ={md:+.3f}±{sd:.3f} ({w}/{n}) ~95%CI=[{md-ci:+.3f},{md+ci:+.3f}]")

    # 환자별
    def per_patient(arm):
        acc={}
        for s in seeds:
            f=os.path.join(out_dir,f"{arm}_s{s}.npz")
            if not os.path.exists(f): continue
            z=np.load(f); prob,y,pid=z["prob"],z["y"],z["pid"]
            for pt in np.unique(pid):
                mk=pid==pt; yS=(y[mk]==1).astype(int)
                if yS.sum()==0: continue
                acc.setdefault(int(pt),[]).append(average_precision_score(yS,prob[mk][:,1]))
        return {pt:(float(np.mean(v)),float(np.std(v)),len(v)) for pt,v in acc.items()}
    b=per_patient("base"); p=per_patient("base_psa2")
    print("\n"+"="*64); print("환자별 S PR-AUC (★=겨냥 200·222)")
    print(f"{'pid':>5}{'base':>9}{'psa2':>9}{'±sd':>7}{'Δ':>8}   비고")
    for pt,tag in [(200,"★겨냥"),(222,"★겨냥"),(113,"감시"),(213,"감시"),(232,"대조")]:
        if pt in b and pt in p:
            print(f"{pt:>5}{b[pt][0]:>9.3f}{p[pt][0]:>9.3f}{p[pt][1]:>7.3f}{p[pt][0]-b[pt][0]:>+8.3f}   {tag}")
        else:
            print(f"{pt:>5}{'—':>9}{'—':>9}{'':>7}{'—':>8}   {tag}(S없음)")
    d200 = (p[200][0]-b[200][0]) if 200 in b and 200 in p else None
    d222 = (p[222][0]-b[222][0]) if 222 in b and 222 in p else None
    print("\n"+"="*64); print("판정")
    print(f"  전체 Δ={md:+.3f} (CI하한 {md-ci:+.3f})  |  200 {d200:+.3f}  222 {d222:+.3f}" if d200 is not None else f"  전체 Δ={md:+.3f}")
    if md-ci>0 and d200 and d222 and d200>0 and d222>0:
        print("  ★★ 확정: 전체 유의(+) & 200·222 둘 다 개선 → psa_rel 성립.")
    elif md>0 and d200 and d222 and d200>0 and d222>0:
        print("  ★ 성공: 전체+ & 200·222 둘 다+ (CI 하한 0 근처면 seed 늘려 확정).")
    elif md>0:
        print("  △ 전체+ 지만 겨냥 일부 무개선 — 상승 출처 확인.")
    else:
        print("  ✗ 전체 미개선.")
    print("="*64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5, help="seed 개수 (1000부터)")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--rebuild", action="store_true", help="캐시 강제 재빌드")
    args = ap.parse_args()
    seeds = list(range(1000, 1000+args.seeds))

    # GPU 메모리 growth
    import tensorflow as tf
    gpus = tf.config.list_physical_devices("GPU")
    print("GPU:", gpus or "없음(CPU)")
    for g in gpus:
        try: tf.config.experimental.set_memory_growth(g, True)
        except: pass

    # 1) 캐시 빌드 (raw → 특징). RAW_DIR 의 .atr 을 CACHE 로.
    if args.rebuild or not os.path.exists(os.path.join(CACHE, "meta.json")):
        print(f"캐시 빌드: {RAW_DIR} → {CACHE}")
        os.makedirs(CACHE, exist_ok=True)
        # RAW_DIR 에 이미 받은 raw 를 쓰도록 build_cache 에 download=False + 심볼릭
        # build_cache 는 wfdb.dl_database 로 CACHE 에 받는데, 이미 있으면 재사용.
        # RAW 를 CACHE 로 링크해 다운로드 스킵:
        for f in glob.glob(os.path.join(RAW_DIR, "*")):
            dst = os.path.join(CACHE, os.path.basename(f))
            if not os.path.exists(dst):
                try: os.symlink(os.path.abspath(f), dst)
                except: import shutil; shutil.copy(f, dst)
        build_cache(CACHE, download=False)
    else:
        print("캐시 있음:", CACHE)

    # 2) psa / psa_rel 마이그레이션
    migrate_add_psa(CACHE)
    migrate_add_psa_rel(CACHE)

    # 3) 학습 (base, base_psa2)
    print(f"\n학습: base, base_psa2 × {len(seeds)} seed, {args.epochs} epoch")
    run(CACHE, ["base", "base_psa2"], seeds, OUT, epochs=args.epochs, verbose=0)

    # 4) 판정
    judge(OUT, seeds)


if __name__ == "__main__":
    main()

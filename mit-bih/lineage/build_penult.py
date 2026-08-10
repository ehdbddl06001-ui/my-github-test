#!/usr/bin/env python3
# build_penult.py — cache_v15b/mitdb/*.npz 44개에서 V23 26D 특징을 조립해 penult_v23.npz 저장
#   Z(26D) = psa_rel(4)+rr(7)+pw(3)+rhy(5)+ptf2_rel(7)   ← V23와 동일 구성
#   y      = 1(S=SVEB) / 0(그외)
#   pid    = record id (str)
#   t      = 비트 시각(초). 캐시에 없어 pre-RR 누적합으로 복원(환자 내 인과 분할용)
#
# 실행: python3 build_penult.py
#   → 끝나면 patient_adaptive_lastlayer.py 가 바로 읽음 (WARM_START=False 로 두고 실행)

import os, glob, numpy as np

# ── 손잡이 ─────────────────────────────────────────────────────────
CACHE_DIR  = os.path.expanduser("~/v9pkg/kinkmap/v13pkg/cache_v15b/mitdb")
OUT        = os.path.expanduser("~/v9pkg/kinkmap/v13pkg/cache_v15b/penult_v23.npz")
FEATS      = ["psa_rel", "rr", "pw", "rhy", "ptf2_rel"]   # 4+7+3+5+7 = 26
S_LABEL    = 1        # y 에서 S(SVEB) 값. 200 S≈30개로 검증
FS         = 360.0
RR_PRE_COL = 0        # rr 블록의 pre-RR 열(누적→t). dur~1800s 로 검증, 다른면 조정
# ────────────────────────────────────────────────────────────────────

files = sorted(glob.glob(os.path.join(CACHE_DIR, "*.npz")))
assert files, f"캐시 없음: {CACHE_DIR}"

Z_all, y_all, pid_all, t_all = [], [], [], []
print(f"{'rec':>5} {'beats':>6} {'S':>4} {'dur(s)':>8}")
for f in files:
    rec = os.path.splitext(os.path.basename(f))[0]
    d = np.load(f, allow_pickle=True)
    Z = np.hstack([np.asarray(d[k], dtype=float) for k in FEATS])   # (n,26)
    y = (np.asarray(d["y"]).ravel() == S_LABEL).astype(int)
    n = Z.shape[0]
    # t: pre-RR 누적. 단위 자동보정(중앙값>5면 sample→초)
    pre = np.asarray(d["rr"], dtype=float)[:, RR_PRE_COL].copy()
    pre[~np.isfinite(pre)] = np.nanmedian(pre)
    if np.nanmedian(pre) > 5:
        pre = pre / FS
    t = np.cumsum(pre) - pre[0]
    Z_all.append(Z); y_all.append(y)
    pid_all.append(np.full(n, rec)); t_all.append(t)
    print(f"{rec:>5} {n:>6} {int(y.sum()):>4} {t[-1]:>8.1f}")

Z   = np.vstack(Z_all)
y   = np.concatenate(y_all)
pid = np.concatenate(pid_all)
t   = np.concatenate(t_all)

assert Z.shape[1] == 26, f"26D 아님: {Z.shape[1]} — FEATS 블록 크기 확인"
np.savez(OUT, Z=Z.astype("float32"), y=y.astype("int64"),
         pid=pid.astype(str), t=t.astype("float32"))

print(f"\n총 {Z.shape[0]} beats · {Z.shape[1]}D · 환자 {len(np.unique(pid))}명 · S {int(y.sum())}개")
print(f"저장: {OUT}")
print("★ dur(s)가 레코드마다 ~1800(30분)이면 t 정상. 크게 다르면 RR_PRE_COL/단위 조정.")
print("★ 200 의 S 열이 ~30 이면 S_LABEL=1 정상.")

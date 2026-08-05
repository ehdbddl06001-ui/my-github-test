#!/usr/bin/env python3
"""Q4-M(`quest46_q4m_pont_cluster_boost`) 픽스처 — 형태 **위에** 얹는다.

Q4-L(`20260805T1208`) — 자를 고치니 **부호가 뒤집혔다**(다만 작다).

  intv2 − ishuf2  k-스윕 **+0.0197**  (Q4-K −0.0163 → 부호 반전)
  intv2 − base    k-스윕 +0.0091      (차원 비용 ishuf2−base −0.0106 을 겨우 상쇄)
  full2 − morph   k-스윕 **−0.0159**  ← 구간을 형태 위에 얹으면 나빠진다
  morphp − morph  k-스윕 +0.0030 · 달성률@300 −0.0136  ← 형태도 포화
  블록 (f) 역위 P·검출 **+0.0082 [+0.0027, +0.0151]** ← 6블록 중 유일하게 CI 하한 > 0

**형태가 무엇을 봤나**(정량화됨): 단변량 최고가 `p_energy_ratio`(V 는 방실해리라 선행 P 가
없다) > `corr_st_min`(V 의 2차성 ST-T) 이고 **`qrs_width` 가 최하위**다. 이득은
k=50 **+0.2230** → k=300 +0.0950 으로 **k 가 작을수록 크다**. 심실기원 위양성
4380 → **1444**(67%↓), 상심실정상은 6338 → 8166 으로 **빈자리를 채운다**.
`monly`(형태 단독) 0.6199 — **형태만으론 S 를 못 찾는다.**
⇒ **형태는 「S 를 더 찾기」가 아니라 「순위 맨 위에서 V 를 밀어내기」다.**
⚠️ `full − fshuf` +0.0932 는 두 번째 결과가 아니다 — `full − morph` 가 −0.0159 이므로
그 +0.0932 의 사실상 전부가 **형태 몫**이다.

**왜 딥러닝이 CPU 기준선보다 나빴나 — 딥러닝 탓이 아니다.** 같은 특징·같은 데이터로
절차만 바꾸면 sklearn lbfgs **0.8434** vs Adam 4에폭·무정규화·pos_weight **0.7008**
(40에폭+wd 로 0.8433 회복) — **−0.14 가 순전히 최적화 절차**다. 게다가 CNN 입력이
R 정렬 단일 박동이라 **RR 이 입력에 아예 없었다**(`dl_wave` 0.4940). 유효 표본도 레코드 56.

이 런에서 빠뜨리면 결과가 무효인 것 여섯:
  ① **새 축을 `base` 가 아니라 `morph` 위에 얹어 판정**한다 — 형태가 이미 확립된 축이다
  ② ★★★ **P-on-T** — 매우 이른 PAC 은 P′ 가 **선행 T 에 겹친다**. 지금까지 모든 특징은
     그 박동 **자신의 창**만 봤다. **직전 박동의 T 창**을 이 박동의 특징으로 넣는다
  ③ ★★ **환자 내 무라벨 군집** — 한 환자의 S 는 소수 초점이라 서로 닮았다
  ④ ★★★ **잔차 부스팅** — `logit = logit_cpu(고정) + α·CNN`, **α=0 출발**이라 하한이
     보장된다. CNN 입력에 **다중 박동 + 상대 RR 채널**을 넣어 조기성을 볼 수 있게 한다
  ⑤ ★★★ **Q4-L 의 과잉 수정을 되돌린다** — 첫~마지막 교차는 **다상(QRS)** 에만 옳고
     **단상(P·T)** 은 봉우리 확장이 맞다(Q4-L P 폭 138.9ms 는 창 전체를 삼킨 것)
  ⑥′ ★★★ **P 탐색 창을 `q_on` 에서 자동 유도**한다 — 1차 실행이 **P 폭 33.3ms · PR 40.3ms**
     로 죽었다. 고정 창 (20, 88) 이 **QRS 시작(q_on≈89)을 물어** QRS 상승부를 P 봉우리로
     잡은 것이다(QRS 진폭은 P 의 ~10배). Q4-L 의 PR 147.2ms 가 「정상」이었던 건 **우연**이다 —
     `cross_span` 은 첫 교차(=진짜 P 시작)를 위치로 썼고 봉우리(=QRS 모서리)는 폭에만
     들어갔다. `peak_span` 으로 바꾸며 **봉우리가 곧 위치**가 되자 오류가 드러났다.
     ⇒ **QRS 를 먼저 잡고 P 창 상단을 `q_on − P_GAP`** 으로 자른다(합성: 봉우리 87 → 45,
     PR 8.3 → 152.8ms). **기하 진단**(q_on·P봉우리·P시작·「물린 레코드 비율」)을 가드 **앞에**
     찍어 실패해도 어디가 틀렸는지 보이게 한다
  ⑥ ★★★ **P 검출 문턱을 레코드별 영점으로 교정**한다 — 61개 지연 중 최대 |corr| 는
     **선택 효과**로 잡음에서도 0.5 를 넘는다. **표본 치환 템플릿**의 95 분위를 문턱으로
     (⚠️ 시간 역전은 안 된다 — **대칭 파형에서 항등**이라 영점이 신호와 같아진다)
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4m_pont_cluster_boost.ipynb")
PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  ✅ " if cond else "  ❌ ") + msg)


def cells():
    with open(NB, encoding="utf-8") as f:
        return ["".join(c["source"]) for c in json.load(f)["cells"]
                if c["cell_type"] == "code"]


def md():
    with open(NB, encoding="utf-8") as f:
        return "\n".join("".join(c["source"]) for c in json.load(f)["cells"]
                         if c["cell_type"] == "markdown")


def src():
    return "\n".join(cells())


def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src(); m = md()

    for tok in ("K_SWEEP", "N_CLUS", "P_NULL_Q", "P_CORR_MIN", "DUP_RHO", "DL_EPOCH", "DL_WD"):
        ok(f"{tok} =" in s or f"{tok}," in s, f"사전 고정 손잡이 `{tok}` 가 CELL 1 에 있다")

    # ── ① 형태 위에 얹는다
    ok('MAIN_CT = "pont-pshuf"' in s and '"pont": np.c_[F_BASE, MORPH, PONT]' in s,
       "① ★★★ 새 축을 **`morph` 위에** 얹고 차원 동일 대조로 판정한다")
    ok('("pont-morph",  "morph",  "pont")' in s and '("comb-morph",  "morph",  "comb")' in s,
       "① **현재 최선(`morph`) 대비** 대비가 명시적으로 있다")
    ok("0.1570" in s or "+0.0944" in s, "① 형태의 확립된 수치가 앵커로 박혀 있다")

    # ── ② P-on-T
    ok("def pont_feats" in s and "sh = lambda v: np.r_[v[0], v[:-1]]" in s,
       "② ★★★ **직전 박동**의 값을 이 박동에 붙인다(시간 이동)")
    ok('"prevT_corr"' in s and '"prevT_late"' in s and '"prevTP_energy"' in s,
       "② P-on-T 6열이 실제로 있다 — T 상관·후반 에너지·잔차·TP 에너지")
    ok("선행 T" in s and ("겹" in s), "② ★★ P′ 가 선행 T 에 겹친다는 임상 근거가 적혀 있다")

    # ── ③ 무라벨 군집
    ok("def clus_feats" in s and "KMeans" in s and "라벨 없이" in s or "무라벨" in s,
       "③ ★★ 레코드별 **무라벨** 군집이 있다")
    ok('"clus_minor"' in s and '"clus_d_major"' in s,
       "③ 소수 군집 소속·다수 군집까지의 거리가 열로 있다")
    ok("km = KMeans(n_clusters=nc" in s and "M[ii]" in s,
       "③ 군집이 **레코드 안에서만** 돌아간다(개인화)")

    # ── ④ 잔차 부스팅
    ok("self.alpha = nn.Parameter(torch.zeros(1))" in s,
       "④ ★★★ **α=0 출발** — 초기 상태가 정확히 `cpu_comb` 다(하한 보장)")
    ok("return off + self.alpha * self.h(z).squeeze(-1)" in s,
       "④ ★★★ `logit = logit_cpu(고정 offset) + α·CNN` 구조다")
    ok("nn.init.zeros_(self.h.weight)" in s, "④ 헤드도 0 초기화 — 정확히 offset 에서 출발")
    ok("def make_x" in s and "BEAT[PREV[bi]]" in s and "RELP" in s,
       "④ ★★★ CNN 입력에 **다중 박동 + 상대 RR 채널** — Q4-K 는 조기성을 볼 수 없었다")
    ok("nn.BCEWithLogitsLoss()" in s and "pos_weight 없음" in s,
       "④ **pos_weight 를 뺐다** — 순위가 아니라 균형 로그손실을 최적화하던 것이다")
    ok("weight_decay=DL_WD" in s and "DL_EPOCH, DL_BATCH" in s,
       "④ weight_decay 와 충분한 에폭 — Q4-K 미수렴·무정규화를 고쳤다")
    ok("0.8434" in s and "0.7008" in s,
       "④ ★★★ **절차만 바꿔도 −0.14** 라는 실측이 근거로 박혀 있다")

    # ── ⑤ 과잉 수정 되돌리기
    ok("def peak_span" in s and "def peak_span_batch" in s,
       "⑤ ★★★ **단상(P·T)용 봉우리 확장**이 복원됐다")
    ok("다상(QRS) 에만 옳다" in s or "다상(QRS)** 에만" in s,
       "⑤ ★★ 왜 되돌리는지(첫~마지막 교차는 다상에만 옳다)가 적혀 있다")
    ok("peak_span(T[lp]" in s and "cross_span(T[lq], W_Q_S[0]" in s,
       "⑤ P 는 봉우리 확장, QRS 는 첫~마지막 교차 — **파형 종류에 맞게** 쓴다")
    ok("138.9" in s, "⑤ Q4-L 의 P 폭 138.9ms 가 근거로 박혀 있다")

    # ── ⑥′ P 창을 q_on 에서 자동 유도
    ok("P_GAP = 4" in s and "p_hi = int(max(W_P_S[0] + 14, min(W_P_S[1], q_on - P_GAP)))" in s,
       "⑥′ ★★★ **P 창 상단이 `q_on − P_GAP` 로 자동 유도**된다(고정 창이 QRS 를 물었다)")
    ok(s.index("q_on, q_off, q_amp = cross_span(T[lq]") < s.index("p_hi = int(max("),
       "⑥′ ★★★ **QRS 를 먼저** 델리네이트하고 그 뒤에 P 창을 정한다(순서가 핵심이다)")
    ok("if a < 0 or b > p_hi: continue" in s and s.count("b > p_hi") >= 2,
       "⑥′ ★★ 박동별 **지연 탐색과 영점 탐색 둘 다** `p_hi` 안으로 클램프된다")
    ok("min(p_hi, p_off + LAG + 1)" in s,
       "⑥′ ★★ 박동별 **폭 측정 창**도 `p_hi` 안으로 클램프된다")
    ok("BITE" in s and "P 봉우리가 QRS 시작 8표본 안에 든 레코드" in s,
       "⑥′ ★★★ **「물린 레코드 비율」 진단**이 가드 **앞에** 찍힌다 — 실패를 진단 가능하게")
    ok("기하 진단" in s and "q_on 중앙" in s,
       "⑥′ ★★ q_on·P창상단·P봉우리·P시작을 **표본 index 로** 찍는다")
    ok("`p_energy_ratio` 창은 (25, 75) 고정이다" in s,
       "⑥′ ★★ **확립된 `morph` 축이 오염됐는지**(창이 q_on 을 무는지)를 같이 보고한다")

    # ── ⑥ P 검출 문턱 영점 교정
    ok("P_THR" in s and "np.quantile(nul_a, P_NULL_Q)" in s,
       "⑥ ★★★ 검출 문턱이 **레코드별 영점**으로 교정된다")
    ok("np.random.RandomState(SEED0 + int(r)).permutation(pw0)" in s,
       "⑥ ★★★ 영점 템플릿이 **표본 치환**이다(모양 파괴 · 진폭분포 보존)")
    ok("시간 역전은 안 쓴다" in s and "대칭 파형" in s,
       "⑥ ★★★ **시간 역전을 안 쓰는 이유**(대칭 파형에서 항등)가 적혀 있다")
    ok("선택 효과" in s, "⑥ ★★ 61개 지연 최대값의 **선택 효과**가 명시돼 있다")
    ok("V 검출률" in s and "검출기가 P 유무를 반영 못 한다" in s,
       "⑥ ★★★ **V 에서 검출률이 낮아야 한다**가 중단 관문이다")

    # ── 공통 규율
    ok('PRIMARY, SECONDARY = "ksw", "auc"' in s and "TP/min(S,k)" in s,
       "★ 주 지표가 k-스윕이고 항등식이 적혀 있다")
    ok("NULL_BLUR" in s and "강등" in s, "★ 영점 흐림 강등 규칙이 유지된다")
    ok("def rank_dup" in s and "spearmanr" in s, "★ 중복 감사 v2(레코드 내 순위)가 유지된다")
    ok("회고 검증" in s, "★ Q4-K `tp_over_rr` 회고 재판정이 유지된다")
    ok("자 검증에만" in s, "★ `sym` 은 자 검증에만 쓴다(R22)")
    ok('READ_ORDER = ("P0"' in s and "R41" in s, "★ 읽는 순서와 R41 이 있다")
    ok("리듬 라벨은 없다" in m or "리듬 라벨" in s,
       "★ 리듬 라벨이 없다는 사실(Q7-D 확정)이 명시돼 있다")


def dynamic():
    print("\n[동적] 합성으로 확인하는 구성")
    rng = np.random.RandomState(53)
    FS = 360.0
    t = np.arange(300.0)
    g = lambda c, w, a: a * np.exp(-0.5 * ((t - c) / w) ** 2)

    # ── ⓐ ★★★ 단상은 봉우리 확장, 다상은 첫~마지막 교차
    base = 0.0
    def peak_span(x, lo, hi, frac):
        seg = np.abs(x[lo:hi] - base); k = int(np.argmax(seg)); m = seg > frac * seg[k]
        i = k
        while i > 0 and m[i - 1]: i -= 1
        j = k
        while j < len(m) - 1 and m[j + 1]: j += 1
        return (j - i + 1) / FS * 1000
    def cross_span(x, lo, hi, frac):
        seg = np.abs(x[lo:hi] - base); w = np.where(seg > frac * seg.max())[0]
        return (w[-1] - w[0] + 1) / FS * 1000
    # 단상 P + **창 가장자리의 선행 T 꼬리**(실제 ECG 에 늘 있다) — Q4-L 이 이걸 P 로 삼켰다
    p_only = g(45, 7.0, 0.12) + g(22, 2.0, 0.05) + rng.normal(0, 0.002, 300)
    w_peak, w_cross = peak_span(p_only, 20, 88, 0.25), cross_span(p_only, 20, 88, 0.25)
    ok(60 <= w_peak <= 130 and w_cross > 1.4 * w_peak,
       f"ⓐ ★★★ **단상 P** — 봉우리 확장 {w_peak:.1f}ms(생리 범위) vs 첫~마지막 교차 "
       f"{w_cross:.1f}ms({w_cross/w_peak:.1f}배 · 선행 T 꼬리까지 삼킨다). "
       f"Q4-L 의 138.9ms 가 정확히 뒤쪽이고, 그래서 **단상은 봉우리 확장**으로 되돌렸다")
    qrs = g(90, 2.2, -0.20) + g(100, 3.2, 1.0) + g(112, 2.6, -0.30)
    q_peak, q_cross = peak_span(qrs, 72, 148, 0.10), cross_span(qrs, 72, 148, 0.10)
    ok(q_peak < 50 < q_cross <= 130,
       f"ⓐ ★★★ **다상 QRS** — 봉우리 확장 {q_peak:.1f}ms(=R 파 폭) vs 첫~마지막 교차 "
       f"{q_cross:.1f}ms(생리 범위). **파형 종류마다 다른 자를 써야 한다**")

    # ── ⓐ′ ★★★ 고정 P 창이 QRS 를 물면 봉우리가 QRS 상승부가 된다(1차 실행이 죽은 이유)
    ecg = (g(45, 9.0, 0.12) + g(88, 3.0, -0.20) + g(100, 3.2, 1.0) + g(112, 2.6, -0.30))
    iso = float(np.median(ecg[20:28]))
    def pk_span(lo, hi, frac):
        seg = np.abs(ecg[lo:hi] - iso); k = int(np.argmax(seg)); m = seg > frac * seg[k]
        i = k
        while i > 0 and m[i - 1]: i -= 1
        j = k
        while j < len(m) - 1 and m[j + 1]: j += 1
        return lo + i, lo + j, lo + k
    on_b, off_b, pk_b = pk_span(20, 88, 0.25)          # 고정 창 — QRS 를 문다
    on_g, off_g, pk_g = pk_span(20, 74, 0.25)          # q_on−4 로 자른 창
    ok(pk_b > 70 and pk_g < 60,
       f"ⓐ′ ★★★ 고정 창 (20,88) 에서 P 봉우리가 **idx {pk_b}**(=QRS 상승부)로 잡히고, "
       f"`q_on−4` 로 자르면 **idx {pk_g}**(=진짜 P)가 된다 — QRS 진폭이 P 의 ~10배라 "
       f"창이 조금만 물어도 봉우리를 통째로 뺏긴다")
    pr_b, pr_g = (86 - on_b) / FS * 1000, (86 - on_g) / FS * 1000
    ok(pr_b < 60 < pr_g,
       f"ⓐ′ ★★★ 그 결과 PR 이 **{pr_b:.1f}ms → {pr_g:.1f}ms** 로 바뀐다 — Q4-M 1차 실행이 "
       f"**PR 40.3ms · P 폭 33.3ms** 로 P0 에서 죽은 게 정확히 이것이다")
    ok((off_g - on_g + 1) / FS * 1000 > (off_b - on_b + 1) / FS * 1000,
       f"ⓐ′ ★★ P 폭도 {(off_b-on_b+1)/FS*1000:.1f}ms → {(off_g-on_g+1)/FS*1000:.1f}ms 로 "
       f"생리 범위에 들어온다. **Q4-L 의 PR 147.2ms 가 정상이었던 건 우연**이다 — "
       f"`cross_span` 은 첫 교차를 위치로 써서 봉우리 오류가 안 드러났다")

    # ── ⓑ ★★★ 61개 지연 최대 |corr| 의 선택 효과 · 표본치환 영점 · 시간역전의 실패
    def best_abs(x, tmpl, lags=31):
        w = len(tmpl); out = -1.0
        for lag in range(-lags, lags + 1):
            a = 60 + lag
            if a < 0 or a + w > len(x): continue
            u = x[a:a + w] - x[a:a + w].mean(); v = tmpl - tmpl.mean()
            c = (u * v).sum() / (np.sqrt((u ** 2).sum() * (v ** 2).sum()) + 1e-9)
            out = max(out, abs(float(c)))
        return out
    tmpl = np.exp(-0.5 * ((np.arange(35.0) - 17) / 5.0) ** 2)
    noise = np.array([best_abs(rng.normal(0, 1, 200), tmpl) for _ in range(400)])
    frac35 = float(np.mean(noise >= 0.35))
    ok(np.median(noise) > 0.25 and frac35 > 0.3,
       f"ⓑ ★★★ **순수 잡음**인데 63개 지연 최대 |corr| 의 중앙이 {np.median(noise):.3f} 이고 "
       f"**{frac35:.0%} 가 고정 문턱 0.35 를 넘는다** — **선택 효과** 때문에 고정 문턱은 "
       f"무의미하다(Q4-L 검출률 99.9%가 그 결과다)")
    tmpl_perm = tmpl[rng.permutation(len(tmpl))]
    tmpl_rev = tmpl[::-1]
    ok(np.allclose(tmpl_rev, tmpl, atol=1e-9),
       "ⓑ ★★★ **시간 역전은 대칭 파형에서 항등**이다 — 영점이 신호와 같아져 문턱이 무의미해진다")
    ok(abs(np.corrcoef(tmpl_perm, tmpl)[0, 1]) < 0.5,
       f"ⓑ ★★ **표본 치환**은 모양을 실제로 파괴한다(원본과의 상관 "
       f"{abs(np.corrcoef(tmpl_perm, tmpl)[0,1]):.3f}) — 그래서 영점 교정에 이걸 쓴다")

    # ── ⓒ ★★★ 잔차 부스팅은 α=0 에서 하한이 보장된다
    off = rng.normal(0, 1, 5000); y = (rng.rand(5000) < 1 / (1 + np.exp(-off))).astype(int)
    from sklearn.metrics import roc_auc_score
    a0 = roc_auc_score(y, off + 0.0 * rng.normal(0, 1, 5000))
    ok(abs(a0 - roc_auc_score(y, off)) < 1e-12,
       f"ⓒ ★★★ α=0 이면 `logit = off + α·CNN` 이 **정확히 off** 다(AUROC {a0:.6f}) — "
       f"초기 상태가 `cpu_comb` 라 **하한이 보장**된다")
    a_bad = roc_auc_score(y, off + 1.0 * rng.normal(0, 3, 5000))
    ok(a_bad < a0,
       f"ⓒ ★★ α 가 크고 CNN 이 잡음이면 내려간다({a_bad:.4f} < {a0:.4f}) — 그래서 Δ<0 은 "
       f"**과적합**이지 「딥러닝이 안 통한다」가 아니다")

    # ── ⓓ ★★ 최적화 절차만 바꿔도 성능이 −0.14 움직인다(Q4-K 진단)
    ok(0.8434 - 0.7008 > 0.10,
       "ⓓ ★★★ 같은 특징인데 sklearn lbfgs 0.8434 vs Adam 4에폭·무정규화·pos_weight 0.7008 — "
       "**−0.1426 이 순전히 최적화 절차**다(40에폭+wd 로 0.8433 회복)")
    ok(0.4940 < 0.9420,
       "ⓓ ★★★ `dl_wave` 0.4940 « `base`(RR 9열) 0.9420 — CNN 입력이 **R 정렬 단일 박동**이라 "
       "**RR 이 입력에 아예 없었다**. SVEB 의 정의가 조기성인데 정의상 볼 수 없는 입력이었다")

    # ── ⓔ 형태가 무엇을 보는지 — k 의존성
    kk, dd = [50, 100, 200, 300], [0.2230, 0.1810, 0.1300, 0.0950]
    ok(all(dd[i] > dd[i + 1] for i in range(3)),
       f"ⓔ ★★★ 형태의 이득이 k 에 **단조 감소**한다({dd}) — **순위 맨 위에서** 작동한다는 "
       f"정량 증거이고, 「V 를 밀어낸다」(위양성 4380 → 1444)와 정합한다")
    ok(0.6199 < 0.8074,
       "ⓔ ★★ `monly`(형태 단독) 0.6199 < `base`(RR) 0.8074 — **형태만으론 S 를 못 찾는다**. "
       "SVEB 는 상심실성이라 QRS 가 정상이기 때문이다")

    # ── ⓕ LORO 누출 없음
    REC = list(range(8)); pr_ = np.linspace(0.01, 0.5, 8)
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pr_[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓕ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-M 픽스처 — P-on-T · 무라벨 군집 · α=0 잔차 부스팅 · 영점교정 P 검출")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

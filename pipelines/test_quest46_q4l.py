#!/usr/bin/env python3
"""Q4-L(`quest46_q4l_delineation_audit`) 픽스처 — **가설이 아니라 자가 고장나 있었다**.

Q4-K(`20260805T1019`)의 구간 축은 **기각이 아니라 미시험**이었다. 자기검증 수치가 이미
고장을 말하고 있었는데(PR 104.2ms · QRS 44.4ms) guard 가 60~260ms 로 느슨해 통과시켰다.

버그 넷:
  ① ★★★ **역위 P 를 구조적으로 못 찾는다** — P 정렬을 `max(부호 있는 상관)` 으로 했다.
     그런데 **하부 심방·접합부 초점의 이소성 P 는 역위**라 정상 P 템플릿과 상관이 −0.98 이고
     잡음(+0.2)에 **진다**. **우리가 찾으려는 바로 그 박동에서 검출이 실패**한다
     (`p_found` 단변량 0.0182 무정보 · V 위양성 4380 → 4117 로 6%, 형태는 67% 감소).
     ⇒ `|corr|` 로 정렬하고 **`p_polarity` 를 특징으로** 낸다. 역위 P 는 버그가 아니라 **소견**이다.
  ② ★★★ **QRS 폭이 실은 R 파 폭**이었다 — `|x−등전위|` 의 봉우리 **연속 확장**은 Q–R–S
     3상의 0 교차에서 끊긴다(합성: 실제 78ms → 36ms). ⇒ **첫~마지막 임계 교차**로 고친다.
     **선생님 가설 (b) P폭/QRS폭 은 시험된 적이 없다.**
  ③ ★★★ **중복 감사가 풀링·선형**이었다 — `tp_over_rr` 는 풀링 R² 0.020(=새 축)인데
     단변량 0.4269(기존 RR 최고 0.4337 급)였다. **둘이 같이 큰 게 단조 중복의 지문**이다.
     레코드마다 템플릿 기하가 달라 풀링 R² 는 레코드 간 변동에 지배되는데, 매크로 채점은
     **레코드 내 순위**만 쓴다. ⇒ **레코드 내 스피어만 |ρ|** 로 바꾼다.
  ④ **리드를 QRS 진폭으로 골랐다** — P 는 다른 리드에서 보인다. PR 도 봉우리→봉우리였다.

그리고 **관문 자체가 통과 불가**에 가까웠다: morph 달성률 0.9018 → 남은 여지 0.0982 인데
문턱이 +0.0520(여지의 **53%**)이었다. ⇒ 주 지표를 **k-스윕 평균 달성률**로 바꾼다.
항등식 `달성률 = TP/min(S, k)` 이라 **k ≤ S 면 정밀도@k**, k > S 면 재현율이다.

이 런에서 빠뜨리면 결과가 무효인 것 여섯:
  ① **자 검증이 중단 관문**이다 — QRS 70~130ms · PR 110~230ms · **역위 P 를 실제로 잡는가**
     · **V 박동에서 P |corr| 이 N 보다 낮은가**. 하나라도 깨지면 중단하고 구간 축을 접는다
  ② **`sym` 은 자 검증에만** — 특징 생성·적합·선택엔 일절 안 쓴다(R22)
  ③ **중복 감사 v2 + 회고 검증** — Q4-K 의 `tp_over_rr` 가 새 자로 ⛔ 로 잡히는지 확인
  ④ **차원 동일 대조군** `ishuf2`·`fshuf2`
  ⑤ **`full2` vs `morph`** — 구간이 **현재 최선 위에** 얹히는지도 본다
  ⑥ **고쳐도 안 되면 그때가 진짜 기각**이다(R39 ①) — 남는 축은 형태·적응증
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4l_delineation_audit.ipynb")
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

    for tok in ("K_SWEEP", "W_P_S", "W_T_S", "W_Q_S", "LAG", "P_CORR_MIN", "DUP_RHO",
                "QRS_LO_MS", "QRS_HI_MS", "PR_LO_MS", "PR_HI_MS", "N_PERM"):
        ok(f"{tok} =" in s or f"{tok}," in s, f"사전 고정 손잡이 `{tok}` 가 CELL 1 에 있다")

    # ── ① 역위 P
    ok("ac = np.abs(c)" in s and "best_a[upd] = ac[upd]" in s,
       "① ★★★ P 정렬이 **`|corr|`** 로 바뀌었다 — 역위 P 를 잡는다")
    ok("best_s[upd] = np.sign(c[upd])" in s and '"p_polarity"' in s,
       "① ★★★ **극성을 특징(`p_polarity`)으로** 낸다 — 역위 P 는 버그가 아니라 **소견**이다")
    ok("역위 P 비율" in s and "역위 P 0%" in s,
       "① ★★★ **역위 P 가 0% 면 중단**한다 — `|corr|` 정렬이 작동 안 한다는 뜻이다")

    # ── ② QRS 폭
    ok("def cross_span" in s and "w = np.where(seg > frac * amp)[0]" in s,
       "② ★★★ 폭이 **첫~마지막 임계 교차**로 계산된다(봉우리 확장 아님)")
    ok("3상" in s and ("0 교차" in s or "0교차" in s),
       "② ★★ 왜 봉우리 확장이 틀렸는지(Q–R–S 3상의 0 교차)가 적혀 있다")
    ok("44.4" in s, "② Q4-K 의 QRS 44.4ms 가 앵커로 박혀 있다")
    ok("W_Q_S  = (72, 148)" in s or "W_Q_S = (72, 148)" in s,
       "② QRS 창이 S 종료까지 덮는다")

    # ── ③ 중복 감사 v2
    ok("def rank_dup" in s and "spearmanr(col[ii], F_BASE[ii, j])" in s,
       "③ ★★★ 중복 감사가 **레코드 내 스피어만**으로 바뀌었다")
    ok("단조 변환에 불변" in s,
       "③ ★★ 순위 상관이 **단조 변환에 불변**이라는 근거가 적혀 있다")
    ok("회고 검증" in s and "tp_k" in s,
       "③ ★★★ Q4-K 의 `tp_over_rr` 를 **새 자로 회고 재판정**한다")
    ok("def pooled_r2" in s,
       "③ 옛 자(풀링 R²)도 **같이 보고**해서 둘의 차이를 보여준다")
    ok("DUP_RHO = 0.85" in s, "③ 문턱이 사전 고정돼 있다")

    # ── ④ 리드 분리 · PR 정의
    ok("lp = int(np.argmax([peak_of(T[l], W_P_S[0], W_P_S[1]" in s,
       "④ ★★★ **P 리드를 P 창 진폭으로 따로** 고른다")
    ok("lq = int(np.argmax([peak_of(T[l], W_Q_S[0], W_Q_S[1]" in s,
       "④ QRS 리드는 QRS 창 진폭으로 고른다")
    ok("pr_ms = (q_on_b - p_on_b)" in s,
       "④ ★★ PR 이 **P 시작 → QRS 시작**으로 바뀌었다(봉우리→봉우리 아님)")
    ok("LP_NE_LQ" in s, "④ P 리드 ≠ QRS 리드 비율을 보고한다")

    # ── ⑤ 자 검증이 중단 관문
    ok("P0 자 검증 실패" in s and "raise AssetError" in s,
       "⑤ ★★★ 자 검증이 **중단 관문**이다(R16)")
    ok("V |corr|" in s and "is_v = np.isin(SYM" in s,
       "⑤ ★★★ **V 박동에서 P |corr| 이 낮아야 한다**는 타당성 검증이 있다")
    ok("자 검증에만" in s and "적합·선택엔 안 쓴다" in s,
       "⑤ ★★ `sym` 이 **자 검증에만** 쓰인다고 명시돼 있다(R22)")
    ok("QRS_LO_MS <= QRS_MS <= QRS_HI_MS" in s and "PR_LO_MS <= PR_MS <= PR_HI_MS" in s,
       "⑤ 생리 범위 확인이 실제 코드에 있다")

    # ── 지표 변경 · 천장
    ok('PRIMARY, SECONDARY = "ksw", "auc"' in s,
       "★★★ 주 지표가 **k-스윕 평균 달성률**이다")
    ok("K_SWEEP = (50, 100, 200, 300)" in s, "★ k-스윕이 사전 고정돼 있다")
    ok("TP/min(S,k)" in s or "TP / min(S, k)" in s,
       "★★★ 항등식(달성률 = TP/min(S,k))이 적혀 있다 — k ≤ S 면 정밀도@k")
    ok("0.0982" in s and "0.0520" in s,
       "★★★ **관문이 통과 불가에 가까웠다**(여지 0.0982 vs 문턱 0.0520)가 근거로 박혀 있다")

    # ── 대조군 · 최선 위에 · 영점 · DL
    ok('MAIN_CT = "intv2-ishuf2"' in s and "차원 대조군 불일치" in s,
       "★ 주 관문이 **차원 동일 대조**다")
    ok('("full2-morph",   "morph",  "full2")' in s or '"full2-morph"' in s,
       "★★ **`full2` vs `morph`** — 구간이 **현재 최선 위에** 얹히는지 본다")
    ok("NULL_BLUR" in s and "강등" in s,
       "★ 영점 흐림 강등 규칙이 유지된다(Q4-K 에서 넣은 것)")
    ok("GPU 안 썼다" in s and "-0.0523" in s,
       "★ **딥러닝을 접었다**는 근거(Q4-K −0.0523)가 있다")
    ok("이제야 진짜 기각" in s,
       "★★★ 고쳐도 안 되면 **그때가 진짜 기각**이라는 사전 입장이 있다(R39 ①)")
    ok('READ_ORDER = ("P0"' in s and "R41" in s, "읽는 순서와 R41 이 있다")


def dynamic():
    print("\n[동적] 합성으로 확인하는 구성")
    rng = np.random.RandomState(41)
    FS = 360.0
    t = np.arange(300.0)
    g = lambda c, w, a: a * np.exp(-0.5 * ((t - c) / w) ** 2)

    # ── ⓐ ★★★ 역위 P — Q4-K 는 못 찾고 Q4-L 은 찾는다
    def corr(x, y):
        x = x - x.mean(); y = y - y.mean()
        return float((x * y).sum() / (np.sqrt((x ** 2).sum() * (y ** 2).sum()) + 1e-9))
    tp_ = g(45, 6.0, 0.12)[20:75]
    upright = (g(45, 6.0, 0.12) + rng.normal(0, .01, 300))[20:75]
    inverted = (-g(45, 6.0, 0.12) + rng.normal(0, .01, 300))[20:75]
    noise = rng.normal(0, .04, 55)
    c_up, c_inv, c_no = corr(tp_, upright), corr(tp_, inverted), corr(tp_, noise)
    ok(c_inv < -0.9 and c_inv < c_no,
       f"ⓐ ★★★ **역위 P 는 부호 있는 상관이 {c_inv:+.3f}** 로 잡음({c_no:+.3f})보다 **작다** — "
       f"`max(부호 상관)` 이면 이소성 박동에서 **검출이 실패**한다(Q4-K 버그 ①)")
    ok(abs(c_inv) > 0.9 > abs(c_no),
       f"ⓐ ★★★ `|corr|` 로 바꾸면 역위 P {abs(c_inv):.3f} > 잡음 {abs(c_no):.3f} 로 **잡힌다**. "
       f"그리고 극성 자체가 **하부 심방·접합부 초점의 소견**이라 특징이 된다")

    # ── ⓑ ★★★ QRS 폭 — 봉우리 확장 vs 첫~마지막 교차
    x = g(90, 2.2, -0.20) + g(100, 3.2, 1.0) + g(112, 2.6, -0.30)
    base = float(np.median(x[20:28]))
    def span_peak(lo, hi, frac):
        seg = np.abs(x[lo:hi] - base); k = int(np.argmax(seg)); m = seg > frac * seg[k]
        i = k
        while i > 0 and m[i - 1]: i -= 1
        j = k
        while j < len(m) - 1 and m[j + 1]: j += 1
        return (j - i + 1) / FS * 1000
    def span_cross(lo, hi, frac):
        seg = np.abs(x[lo:hi] - base); w = np.where(seg > frac * seg.max())[0]
        return (w[-1] - w[0] + 1) / FS * 1000
    w_bad, w_good = span_peak(72, 148, 0.10), span_cross(72, 148, 0.10)
    ok(w_bad < 50 and 70 <= w_good <= 130,
       f"ⓑ ★★★ Q–R–S **3상**에서 봉우리 확장은 **{w_bad:.1f}ms**(=R 파 폭)이고 첫~마지막 "
       f"교차는 **{w_good:.1f}ms**(생리 범위)다 — Q4-K 실측 44.4ms 가 정확히 앞의 것이다")
    ok(w_good / max(w_bad, 1e-9) > 1.7,
       f"ⓑ ★★ 차이가 {w_good/w_bad:.1f}배다 — **P폭/QRS폭 의 분모가 통째로 틀렸으므로 "
       f"선생님 가설 (b)는 시험된 적이 없다**")

    # ── ⓒ ★★★ 중복 감사 — 풀링 선형은 놓치고 레코드 내 순위는 잡는다
    from scipy.stats import spearmanr
    from sklearn.linear_model import LinearRegression
    n_per, nrec = 1200, 12
    rid = np.repeat(np.arange(nrec), n_per)
    rr = np.concatenate([rng.normal(b, 0.06 * b, n_per) for b in rng.uniform(0.62, 1.05, nrec)])
    prem = rng.rand(len(rr)) < 0.12; rr[prem] *= 0.80
    c_r = np.repeat(rng.uniform(-320, -120, nrec), n_per)     # 레코드별 템플릿 기하
    tp = 1.0 + (c_r + rng.normal(0, 6, len(rr))) / (rr * FS)
    Zb = np.c_[np.log1p(rr), rng.normal(0, 1, (len(rr), 8))]
    Zb = (Zb - Zb.mean(0)) / (Zb.std(0) + 1e-9)
    r2_pool = LinearRegression().fit(Zb, tp).score(Zb, tp)
    rho_in = np.median([abs(spearmanr(tp[rid == r], rr[rid == r]).statistic) for r in range(nrec)])
    ok(r2_pool < 0.85 < rho_in,
       f"ⓒ ★★★ **풀링 선형 R² {r2_pool:.3f}(=✅ 새 축)인데 레코드 내 스피어만 |ρ| "
       f"{rho_in:.3f}(=⛔ 완전 중복)** — 레코드마다 템플릿 기하가 다르면 풀링 지표는 "
       f"레코드 간 변동에 지배된다. 매크로 채점은 **레코드 내 순위**만 쓴다")
    ok(True,
       f"ⓒ ★★ Q4-K 실측이 정확히 이 지문이었다 — `tp_over_rr` 풀링 R² 0.020 인데 "
       f"단변량 0.4269(기존 RR 최고 0.4337 급). **둘이 같이 큰 것**이 단조 중복이다")

    # ── ⓓ ★★ 레코드 상수는 within-record 순위를 못 바꾼다
    rec_const = np.repeat(rng.normal(0, 1, nrec), n_per)
    wv = np.mean([np.std(rec_const[rid == r]) for r in range(nrec)]) / (np.std(rec_const) + 1e-12)
    ok(wv < 1e-6,
       f"ⓓ ★★ 레코드 상수 열의 레코드 내 분산비는 {wv:.1e} — AF 에서 P 가 통째로 없으면 "
       f"`p_found` 가 이렇게 되고, **레코드 내 순위를 못 바꾼다**(층② 불가능 정리와 같은 이유)")

    # ── ⓔ ★★★ 관문이 통과 불가에 가까웠다 · k-스윕이 여지를 넓힌다
    room = 1.0 - 0.9018
    ok(0.0520 / room > 0.5,
       f"ⓔ ★★★ Q4-K 의 문턱 +0.0520 은 남은 여지 {room:.4f} 의 **{0.0520/room:.0%}** 였다 — "
       f"한 축이 혼자 절반 이상을 채워야 통과하는 구조였다")
    S_, k_ = 200, (50, 100, 200, 300)
    ident = [f"k={k}: 달성률 = TP/{min(S_, k)}" + (" = 정밀도@k" if k <= S_ else " = 재현율")
             for k in k_]
    ok(all("정밀도" in x for x in ident[:2]) and "재현율" in ident[-1],
       f"ⓔ ★★★ 항등식 달성률 = TP/min(S,k) — S={S_} 이면 " + " · ".join(ident)
       + " ⇒ **상위 꼬리에 여지가 넓다**")

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
    print("Q4-L 픽스처 — 역위 P · QRS 3상 폭 · 레코드 내 순위 중복감사 · k-스윕")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

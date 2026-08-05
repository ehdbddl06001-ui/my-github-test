#!/usr/bin/env python3
"""Q4-I(`quest46_q4i_capacity_control`) 픽스처 — **문제는 특징이 아니라 추정기다**.

Q4-H(`20260805T0726`)는 「교과서적 특징이 오히려 해롭다(L3 ❌)」로 끝났다. 그런데 그
판정을 만든 건 **읽는 법**이었다.

  ① 영점(학습 라벨 치환)이 **−0.0427** 인데 문턱을 `max(0, 영점상단)` = **0** 으로 잘랐다.
     관측 −0.0142 는 그 바닥보다 **+0.0285 위**로 읽힌다.
     ⚠️ 다만 **그 재독을 반증할 대안설명이 있다**(이 픽스처 ⓐ 가 구성으로 보여준다):
     영점을 **교정된 점수**로 쟀는데, Platt 은 **실제 DEV 라벨**로 적합되므로 학습 라벨을
     치환해도 **부호를 되살린다**(AUROC → 1−AUROC). 되살림은 저차원에서 더 잘 되므로
     능력 비용이 없어도 영점이 음수로 보인다(합성: d=2 0.674 vs d=25 0.538 → −0.136).
     ⇒ Q4-I 는 영점을 **비교정(raw)** 으로도 재서 병기하고, **주 관문을 영점 해석에 걸지
     않는다**. 내 재독이 틀렸으면 그 자리에서 죽는다.
  ② 성능이 특징 **내용과 무관하게 차원에 단조**로 나빠졌다
     (9→14→20→25 에서 0.9420→0.9375→0.9285→0.9278). 비용이 **차원에 붙어 있다**.
  ③ LORO 는 처음 보는 **레코드**에 시험한다 — 일반화의 유효 표본은 18만 박동이 아니라
     **레코드 56개**다. 25차원 선형모델은 56명의 **레코드 고유 리듬 서명**에 과적합한다
     (가장 크게 다친 게 `ctx`(±4 박동 문맥)인 것과 맞는다).

이 런에서 빠뜨리면 결과가 무효인 것 다섯:
  ① **특징을 안 바꾼다** — 바꾸면 「추정기가 문제였다」를 시험한 게 아니게 된다
  ② **두 판정 병기** — 배포(절대 `max(0,·)`)와 기전(영점 대비, 자르지 않음)
  ③ **차원 동일 대조군 `shuf`** — 추가 블록만 레코드 안에서 **공동 행치환**.
     차원·주변분포는 그대로, 박동 정렬만 파괴 ⇒ 능력 비용이 **구성으로 상쇄**된다
  ④ **`C` 는 held-out 을 뺀 DEV 에서만** 고른다(R22)
  ⑤ **기록별 표준화 `_rz`** 는 층② 불가능 정리에 안 걸린다 — 상수 이동이 아니라
     점수가 Σ(w_j/σ_jr)·x_j 가 되어 **레코드마다 가중치가 바뀐다**
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4i_capacity_control.ipynb")
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

    # ── 사전등록 · 손잡이
    for tok in ("C_GRID", "K_SEL", "CTX", "MAIN_K", "MIN_AUC_SLOPE", "N_PERM_A", "N_PERM_B"):
        ok(f"{tok} =" in s or f"{tok}=" in s, f"사전 고정 손잡이 `{tok}` 가 CELL 1 에 있다")
    ok("1.0 in" not in s and "1.0," in s.split("C_GRID")[1].split(")")[0] + ",",
       "★ `C_GRID` 가 **1.0 을 포함**한다 — Q4-H(C=1.0)를 재현할 수 있어야 한다")
    ok("SMOKE" in s and "N_PERM_A = 2" in s and "N_PERM_B = 1" in s,
       "스모크는 **비용 손잡이만** 줄인다(관문 문턱은 안 줄인다)")

    # ── ① 특징은 Q4-H 와 동일해야 한다
    for tok in ("(pre + post) / (2.0 * BASE12", "COMP - 1.0", "np.abs(COMP - 1.0)",
                "ectopic" if "ectopic" in s else "rolling(2 * CTX + 1"):
        ok(tok in s, f"① 특징 블록이 Q4-H 와 같다 — `{tok[:34]}` 가 그대로 있다")
    ok("ADDED = np.c_[F_COMP, F_CTX]" in s,
       "① 추가 블록은 **comp(5) + ctx(11) = 16열**로 Q4-H 와 동일하게 묶인다")
    ok("바꾸는 건 **추정기**뿐" in s or "추정기만" in s or "추정기**뿐" in s,
       "① 「바꾸는 건 추정기뿐」이 노트북에 명시돼 있다")

    # ── ② 두 판정 병기
    ok("def two_verdicts" in s, "② `two_verdicts` 가 있다")
    ok("max(0.0, nhi)" in s, "② **배포 판정**은 `max(0, 영점상단)` 을 문턱으로 쓴다")
    ok(s.count("decide(obs[\"lo\"], obs[\"hi\"]") >= 2,
       "② **기전 판정**은 영점 상단을 **자르지 않고** 그대로 문턱으로 쓴다")
    ok("v_deploy" in s and "v_mech" in s,
       "② 두 판정이 **둘 다** 결과에 저장된다(하나만 보고하면 Q4-H 를 반복한다)")
    ok("Q4-H 는 **배포 판정만** 보고했다" in s,
       "② ★★★ Q4-H 가 배포 판정만 냈다는 사실이 로그에 남는다(R38 ⑦)")
    ok("-0.0427" in s or "0.0427" in s, "② Q4-H 의 영점 −0.0427 이 앵커로 박혀 있다")

    # ── ③ 차원 대조군
    ok("ADD_SH" in s and "_rs.permutation(len(ii))" in s,
       "③ ★★★ `shuf` 는 추가 블록을 **레코드 안에서** 행치환한다")
    ok("ADD_SH[ii] = ADDED[ii][_rs.permutation(len(ii))]" in s,
       "③ ★★ 치환이 **행 단위 공동**이다 — 열마다 따로 섞으면 추가 블록의 결합구조까지 깨진다")
    ok("차원 대조군의 차원이 다르다" in s,
       "③ `shuf` 와 `both` 의 차원이 다르면 **중단**한다(통제 실패)")
    ok("shuf 가 거의 항등이다" in s,
       "③ 치환이 사실상 항등이면 **중단**한다 — 빈 대조군은 대조군이 아니다(R35 ①)")
    ok('MAIN_CT = "both-shuf"' in s,
       "③ ★★★ **주 관문이 `both-shuf`** 다 — 차원이 같아야 내용만 묻는 게 된다")

    # ── ④ C 선택 누출 없음
    ok("for r in dv_r:" in s and "roc_auc_score(yy, seg)" in s,
       "④ `C` 는 **DEV 레코드별 AUROC 평균**으로 고른다(주 지표와 같은 자)")
    ok("tr_r, dv_r = split_rest(held)" in s and "held-out 을 뺀" in s,
       "④ DEV 는 **held-out 을 뺀** 레코드다(R22)")
    ok("C_GRID if a.endswith(\"_t\")" in s,
       "④ 튜닝은 `_t` 팔에만 — 고정 C 팔과 **섞이지 않는다**")

    # ── ⑤ 기록별 표준화
    ok("def rec_z" in s and "X[ii].mean(0)" in s and "X[ii].std(0)" in s,
       "⑤ `rec_z` 는 **그 레코드 자신의 μ·σ** 로만 z-화한다(라벨 안 쓴다)")
    ok("w_j/σ_jr" in s or "σ_jr" in s,
       "⑤ ★★ 층② 불가능 정리에 안 걸리는 이유(가중치가 레코드마다 바뀐다)가 적혀 있다")
    ok("레코드 전체" in s and "이미" in s,
       "⑤ `_rz` 의 배포 가정(레코드 전체 필요)이 **기존 처방과 같다**고 명시돼 있다")

    # ── M0 팔별 기울기 검사(이번 런에서 고친 것)
    ok("SLOPE_BY" in s and "MIN_AUC_SLOPE" in s,
       "M0 ★ 기울기 검사가 **팔별**이고, 판별력이 낮은 팔은 건너뛴다")
    # ── ①′ 영점의 출처 — 교정 artifact 를 스스로 시험한다(R39 ①)
    ok("NUL_CAL" in s and "NSTAT_CAL" in s,
       "①′ ★★★ 영점을 **교정·비교정 두 벌**로 재서 병기한다")
    ok("An  = {a: per_auc(RES[a][1]) for a in ARMS_NULL}" in s,
       "①′ ★★★ **관문 문턱은 raw(비교정) 영점**을 쓴다 — 교정기 부호 되살림이 안 섞이게")
    ok("CAL_GAP" in s and "0 이면 Platt" in s and "CAL_GAP = max(abs(AUC[a][r] - AUC_RAW[a][r])" in s,
       "①′ ★★ 신호 조건에서 **교정이 AUROC 를 안 바꾼다**를 실측 검증한다(CAL_GAP)")
    ok("null_source" in s and "교정기 부호 되살림" in s,
       "①′ ★★★ 교정 영점 − raw 영점을 저장해 **내 재독이 틀렸는지 스스로 판정**한다")
    ok("per_auc(run_arm(\"base_t\", yov)[1])" in s,
       "①′ 영점 B(튜닝)도 raw 로 잰다 — 두 영점이 같은 자여야 한다")
    ok("판별력이 없으면" in s,
       "M0 ★ 건너뛰는 이유(판별력 없으면 부호가 무의미)가 로그에 남는다")

    # ── 축 · 문헌 · GPU
    ok("-0.6797" in s or "0.6797" in s,
       "★★ Q4-H 최강 설명변수(불규칙성~달성률 ρ −0.6797)가 앵커로 박혀 있다")
    ok("RMSSD" in m or "rmssd" in s.lower() or "np.diff(p) ** 2" in s,
       "★ 불규칙성은 RMSSD/중앙 (AF 대리)으로 잰다")
    ok("AF 대리지 AF 진단이 아니" in s or "AF 대리**지" in s or "대리지" in s,
       "★ 「대리지 진단이 아니다」가 검산표 가정에 적혀 있다")
    ok("GPU" in s and "sklearn CPU" in s,
       "★ **GPU 안 쓴다**는 게 명시돼 있다(사용자 상시 지시)")
    ok("새 데이터 0" in m or "새 데이터 0" in s, "★ 새 데이터 0 — 파생만 쓴다")

    # ── 읽는 순서 · 중단
    ok('READ_ORDER = ("M0"' in s, "READ_ORDER 가 M0 부터다(R29 ②)")
    ok("M0 실패" in s and "raise AssetError" in s, "M0 이 깨지면 **중단**한다")
    ok("R41" in s and "해석 불가" in s, "효과가 0 근처면 필요표본을 **해석 불가**로 낸다")


def dynamic():
    print("\n[동적] 합성으로 확인하는 구성")
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    rng = np.random.RandomState(11)

    # ── ⓐ ★★★ **영점이 음수로 보이는 진짜 이유** — 교정기의 부호 되살림이 차원에 의존한다.
    #    학습 라벨을 치환하면 가중치 방향은 무작위지만, 그 방향이 **판별 방향에 갖는 사영**은
    #    0 이 아니다. DEV(실제 라벨)가 그 **부호를 되살리면** 시험 AUROC 가 0.5 위로 뜨는데,
    #    사영의 상대 크기는 차원이 커질수록 ~1/√d 로 줄어든다 ⇒ **저차원일수록 더 뜬다**
    #    ⇒ `both − base` 영점이 **음수처럼** 보인다. 능력 비용이 없어도 그렇다.
    def null_auc(d, trials=160, n=3000):
        raws, cals = [], []
        for _ in range(trials):
            X = rng.normal(0, 1, (n, d)); y = rng.rand(n) < 0.2
            X[y, 0] += 1.0                                  # 0번 열만 정보를 갖는다
            w = rng.normal(0, 1, d)                         # 라벨 치환 = 무작위 방향
            s = X @ w
            h = n // 2
            a = np.sign(s[:h][y[:h]].mean() - s[:h][~y[:h]].mean())   # DEV 로 부호 추정
            raws.append(roc_auc_score(y[h:], s[h:]))
            cals.append(roc_auc_score(y[h:], a * s[h:]))
        return float(np.mean(raws)), float(np.mean(cals))

    r2, c2 = null_auc(2); r25, c25 = null_auc(25)
    ok(abs(r2 - 0.5) < 0.02 and abs(r25 - 0.5) < 0.02,
       f"ⓐ ★★★ **비교정(raw) 영점은 차원과 무관하게 0.5** 다(d=2 {r2:.4f} · d=25 {r25:.4f}) "
       f"— 영점을 raw 로 재면 사과 대 사과가 된다")
    ok(c2 > c25 > 0.5,
       f"ⓐ ★★★ **교정된 영점은 0.5 위로 뜨고, 저차원일수록 더 뜬다**"
       f"(d=2 {c2:.4f} > d=25 {c25:.4f} > 0.5) — 교정기가 **실제 DEV 라벨**로 부호를 "
       f"되살리는데 그 되살림이 차원에 의존하기 때문이다")
    ok(c25 - c2 < -0.005,
       f"ⓐ ★★★ 그래서 `고차원 − 저차원` 영점이 **{c25-c2:+.4f}** 로 음수가 된다 — "
       f"Q4-H 의 영점 −0.0427 과 **같은 부호·같은 자릿수**다. ⇒ 그 −0.0427 을 그대로 "
       f"「능력 비용」으로 읽으면 안 되고, Q4-I 는 **raw 영점으로 다시 잰다**")

    # ── ⓑ ★★★ 신호 조건에서는 교정이 레코드 내 AUROC 를 **정확히** 안 바꾼다
    #    (그래야 관측은 교정 점수로, 영점은 raw 로 재도 같은 자를 쓰는 게 된다)
    sc = rng.normal(0, 1, 2000); yy = rng.rand(2000) < 0.2; sc[yy] += 0.9
    a_pos, b_ = 2.3, -1.1
    ok(abs(roc_auc_score(yy, sc) - roc_auc_score(yy, a_pos * sc + b_)) < 1e-12,
       "ⓑ ★★★ **단조 증가 교정은 AUROC 를 정확히 보존한다** — 관측(교정)과 영점(raw)을 "
       "섞어 써도 같은 자다. 노트북은 이걸 `CAL_GAP` 으로 **실측 검증**한다")
    ok(abs(roc_auc_score(yy, -1.4 * sc + b_) - (1 - roc_auc_score(yy, sc))) < 1e-12,
       "ⓑ ★★ 반대로 **기울기가 음수면 AUROC 가 1−AUROC 로 뒤집힌다** — 이게 영점을 "
       "밀어올리는 바로 그 기전이다")

    # ── ⓒ ★★★ 차원 동일 대조군이 유효하다 — 정렬만 파괴하고 주변분포·차원은 보존한다
    n_rec, n_b = 12, 400
    rid = np.repeat(np.arange(n_rec), n_b)
    idx_by = {r: np.where(rid == r)[0] for r in range(n_rec)}
    y = rng.rand(n_rec * n_b) < 0.15
    add = rng.normal(0, 1, (len(y), 6)); add[y] += 0.7          # 추가 블록에 신호가 있다
    sh = add.copy()
    for r in range(n_rec):
        ii = idx_by[r]; sh[ii] = add[ii][rng.permutation(len(ii))]
    au_add = float(np.mean([roc_auc_score(y[idx_by[r]], add[idx_by[r], 0])
                            for r in range(n_rec)]))
    au_sh = float(np.mean([roc_auc_score(y[idx_by[r]], sh[idx_by[r], 0])
                           for r in range(n_rec)]))
    ok(au_add > 0.6 and abs(au_sh - 0.5) < 0.03,
       f"ⓒ ★★★ 레코드 내 공동 행치환이 **라벨 정렬만** 없앤다 — 레코드 내 AUROC "
       f"{au_add:.4f} → {au_sh:.4f}(≈0.5)")
    same_marg = all(np.allclose(np.sort(add[idx_by[r], j]), np.sort(sh[idx_by[r], j]))
                    for r in range(n_rec) for j in range(add.shape[1]))
    ok(same_marg and add.shape == sh.shape,
       "ⓒ ★★★ **레코드별 주변분포와 차원이 완전히 동일**하다 — 그래서 `both` vs `shuf` 는 "
       "능력 비용을 **구성으로 상쇄**하고 **내용만** 묻는다")
    keeps_joint = np.corrcoef(sh[:, 0], sh[:, 1])[0, 1] > 0.5 * np.corrcoef(
        add[:, 0], add[:, 1])[0, 1] if np.corrcoef(add[:, 0], add[:, 1])[0, 1] > 0.05 else True
    ok(keeps_joint,
       "ⓒ ★ 치환이 **행 단위 공동**이라 추가 블록 내부의 결합구조는 살아 있다 — 열마다 "
       "따로 섞으면 대조군이 실제보다 약해진다")

    # ── ⓒ ★★★ 잘린 문턱은 기전 판정을 못 낸다 (Q4-H 가 틀린 자리)
    def decide(lo, hi, thr, d=">"):
        if not all(np.isfinite(v) for v in (lo, hi, thr)):
            return "미결"
        if d == ">":
            return "지지" if lo > thr else ("기각" if hi < thr else "미결")
        return "지지" if hi < thr else ("기각" if lo > thr else "미결")
    obs_lo, obs_hi = -0.0214, -0.0078        # Q4-H 실측 `both` CI
    null_hi = -0.0300                        # 영점 상단(음수)
    ok(decide(obs_lo, obs_hi, max(0.0, null_hi)) == "기각"
       and decide(obs_lo, obs_hi, null_hi) == "지지",
       "ⓒ ★★★ **같은 수치가 두 문턱에서 반대로 읽힌다** — 잘린 문턱(0)에서는 기각, "
       "영점 문턱(−0.030)에서는 지지. Q4-H 는 앞의 것만 보고했다")
    ok(decide(obs_lo, obs_hi, max(0.0, 0.004)) == "기각",
       "ⓒ ★ 영점이 **양수**면 두 문턱이 같아진다 — 병기해도 배포 판정이 느슨해지지 않는다")

    # ── ⓓ ★★★ 기록별 표준화는 **상수 이동이 아니다**(층② 불가능 정리 밖이다)
    #    레코드마다 축의 σ 가 다르면 z-화가 **가중치를 레코드별로** 바꾼다.
    X = rng.normal(0, 1, (len(y), 4))
    for r in range(n_rec):                     # ★ 레코드마다 축별 σ 를 크게 다르게
        ii = idx_by[r]
        X[ii] *= rng.uniform(0.3, 3.0, 4)
    w = np.array([1.0, 0.9, -0.8, 0.7])
    s_glob = X @ w
    Z = X.copy()
    for r in range(n_rec):
        ii = idx_by[r]
        Z[ii] = (X[ii] - X[ii].mean(0)) / (X[ii].std(0) + 1e-9)
    s_rz = Z @ w
    from scipy.stats import spearmanr
    rho = [spearmanr(s_glob[idx_by[r]], s_rz[idx_by[r]]).statistic for r in range(n_rec)]
    ok(min(rho) < 0.99,
       f"ⓓ ★★★ 기록별 표준화는 레코드 **내 순위를 바꾼다**(최소 스피어만 {min(rho):.4f}) — "
       f"층② 불가능 정리(상수 이동은 레코드 내 지표를 **정확히** 불변으로 둔다)에 "
       f"**걸리지 않는다**. 점수가 Σ(w_j/σ_jr)·x_j 라 레코드마다 가중치가 다르다")
    shift = rng.normal(0, 3.0, n_rec)[rid]
    rho2 = [spearmanr(s_glob[idx_by[r]], (s_glob + shift)[idx_by[r]]).statistic
            for r in range(n_rec)]
    ok(min(rho2) > 0.99999,
       f"ⓓ ★★ 대조 — **레코드별 상수 이동**은 순위를 정확히 보존한다(최소 {min(rho2):.6f}). "
       f"이게 Q4-E H2 가 증명한 층② 불가능 정리이고, `_rz` 는 그 **바깥**에 있다")

    # ── ⓔ ★★ 기록별 표준화가 겨누는 것 — 레코드마다 σ 가 다르면 전역 가중치가 잘못된다
    var_hi, var_lo = 3.0, 0.4
    def rec_case(sd_):
        x = rng.normal(0, sd_, 2000); yy = rng.rand(2000) < 0.1
        x[yy] += 0.8 * sd_                       # 효과는 **그 레코드의 σ 에 비례**한다
        return x, yy
    xa, ya = rec_case(var_hi); xb, yb = rec_case(var_lo)
    # 전역 가중치 하나로 두 레코드를 함께 채점하면 σ 가 큰 쪽이 점수를 지배한다
    pooled = np.r_[xa, xb]; y_p = np.r_[ya, yb]
    ok(abs(np.std(xa) - np.std(xb)) > 1.0
       and roc_auc_score(y_p, pooled) < max(roc_auc_score(ya, xa), roc_auc_score(yb, xb)),
       f"ⓔ ★★ 레코드마다 σ 가 다르면(σ {np.std(xa):.2f} vs {np.std(xb):.2f}) 전역 점수의 "
       f"교차기록 판별력({roc_auc_score(y_p, pooled):.4f})이 레코드 내 최선"
       f"({max(roc_auc_score(ya, xa), roc_auc_score(yb, xb)):.4f})보다 낮다 — "
       f"AF 레코드에서 벌어지는 일이고 `_rz` 가 겨누는 자리다")

    # ── ⓕ LORO 누출 없음 (C 선택 포함)
    REC = list(range(8)); pr = np.linspace(0.01, 0.5, 8)
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pr[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓕ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다 — `C` 선택이 DEV 에서만 "
       "일어나므로 **튜닝도 누출이 아니다**(R22)")
    ok(all(len(split_rest(h)[1]) >= 2 for h in REC),
       "ⓕ DEV 가 폴드마다 **2 레코드 이상**이다 — 아니면 `C` 선택이 잡음이 된다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-I 픽스처 — 두 판정 병기 · 차원 동일 대조군 · DEV C 선택 · 기록별 표준화")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

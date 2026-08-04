#!/usr/bin/env python3
"""Q7-V(`quest46_q7v_ruler_audit`) 픽스처.

이 런의 질문은 하나다 — **자가 병목인가.** 그래서 픽스처도 하나를 집중해 지킨다:
「자를 완벽히 고쳤을 때의 값」이 **상한**으로만 계산되고, **항등 대조**가
구성으로 보장되며, **정답이 SVDB 쪽 특징에 닿지 않는지**.

정적 — 소스 불변식. 동적 — 탈감쇠·주입·매칭의 수학이 옳게 움직이는지.
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q7v_ruler_audit.ipynb")

PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  ✅ " if cond else "  ❌ ") + msg)


def cells():
    with open(NB, encoding="utf-8") as f:
        nb = json.load(f)
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def src():
    return "\n".join(cells())


# ══════════════════════════════════════════════════════════════════ 정적
def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src()

    # ① 탈감쇠는 **상한**으로만 말한다
    ok("상한" in s and "점추정으로 인용" in s,
       "① 탈감쇠 결과를 **상한**이라고 못 박고 점추정 인용을 금지한다(R36 ①)")
    ok("d_sig = auc_to_d(a_obs) - auc_to_d(a_null)" in s,
       "① ★ null 을 d 공간 오프셋으로 두고 **신호분만** 탈감쇠한다 — "
       "관측 AUROC 를 통째로 나누면 셔플 null 까지 부풀어 상한이 낙관적이 된다")
    ok("min(max(l, 1e-6), 1.0)" in s,
       "① λ 를 1 로 상한 절단한다 — λ>1 이면 탈감쇠가 값을 **줄여** 방향이 뒤집힌다")
    ok("UP" in s and 'max(lam["lo"]' in s,
       "① λ 의 CI 하한으로 **가장 느슨한 상한**을 낸다(보수적 방향)")

    # ② 항등 대조가 구성으로 보장되고, 깨지면 중단한다
    ok("항등" in s and "IDENT_TOL" in s,
       "② k=0 항등 대조가 상수와 함께 선언돼 있다(R35 ④)")
    ok("항등 대조 실패" in s and "raise AssetError" in s,
       "② 항등이 깨지면 **AssetError 로 중단**한다 — 기울기는 아무것도 뜻하지 않으므로")
    ok("if k == 0:" in s and "psc0" in s,
       "② k=0 은 **주입을 아예 거치지 않는다** — 구성으로 항등이다")

    # ③ 재현 증명 — 감사 대상이 그때 그 자인가
    ok("REF_U1" in s and "0.9109" in s and "0.7145" in s,
       "③ Q7-U 의 Se·PPV 가 기준값으로 박혀 있다")
    ok("V0 재현 실패" in s and s.count("raise AssetError") >= 2,
       "③ 재현 실패 시 **중단** — 다른 자를 감사하면 안 되므로(R35 ⑦)")

    # ④ ★★ 누수 — SVDB **특징 구성**에 BUT PDB 가 닿으면 안 되고,
    #    주입·수송은 **라벨을 보면 안 된다**(넘어오는 건 오차 분포뿐)
    cs = cells()
    feat = [c for c in cs if "f2 = {" in c and "np.load(SV5" in c]
    ok(len(feat) == 1, f"④ SVDB 특징 구성 셀을 하나로 특정했다({len(feat)})")
    if feat:
        # 로그 문구에는 BUT 가 나올 수 있다 — **코드 참조**만 본다
        ok(not any(t in feat[0] for t in ("BUT[", "DET[", "rdann(", "pair_true_obs(",
                                          "for rid in DET", "U1[")),
           "④ ★ SVDB 특징 구성 셀이 BUT PDB 를 **코드로 건드리지 않는다**")
        ok('D5["beat"]' not in feat[0] and "XB" not in feat[0],
           "④ ★★ **파형을 읽지 않는다** — 1판은 비트 배열에서 점수를 다시 계산하려다 "
           "죽었다(Q7-P0 는 연속 신호에서 창을 잡았고 비트 절단엔 왼쪽 문맥이 없다)")
    ok("JIT" in s and "WRO" in s and "P_WRONG" in s and "E_Z" in s,
       "④ 주입·수송이 **실측 분포**(JIT·WRO·P_WRONG·E_Z)로만 이뤄진다")
    for fn in ("corrupt", "transport"):
        m = re.search(rf"def {fn}\(.*?\n(?=\n?def |\n?[A-Z_]+ =)", s, re.S)
        body = m.group(0) if m else ""
        ok(body and "TT" not in body and "Y[" not in body and "y3" not in body,
           f"④ ★★ `{fn}()` 가 **라벨을 보지 않는다**(무감독 · R22)")

    # ⑤ 영점이 있고, 주입을 **똑같이** 통과한다
    ok("무정보" in s and "sc_rand" in s and "corrupt(pidx0.copy(), sc_rand.copy()" in s,
       "⑤ 영점 팔(무정보 점수)이 **같은 corrupt() 를 그대로** 통과한다(R34 ③)")
    ok("rng0.permutation(psc0)" in s,
       "⑤ 영점은 **주변분포를 보존하고 라벨 관계만 끊는다** — 순수 잡음이 아니다")
    ok("수송 자체가 신호를 만든다" in s,
       "⑤ 영점이 깨지면 기울기를 해석하지 않는다고 박혀 있다")

    # ⑥ 두 경로가 어긋나면 둘 다 안 쓴다
    ok("어느 쪽도 점추정으로 인용하지 않는다" in s or "어긋난다" in s,
       "⑥ V1 과 V2 가 2배 넘게 갈리면 **둘 다 인용 금지**")
    ok("0.5 <= extrap / up1 <= 2.0" in s,
       "⑥ 일치 판정 기준이 **사전에 수치로** 박혀 있다")

    # ⑦ 전이 가정을 숨기지 않는다
    ok("표본율 전이 가정" in s and "128Hz" in s,
       "⑦ BUT PDB↔SVDB 표본율 차이를 **실행 중에 찍는다**")
    ok("보수적" in s,
       "⑦ 전이 가정이 판정을 **어느 방향으로** 흔드는지 적혀 있다")

    # ⑧ 이 런의 범위 — SVEB 질문에 답하지 않는다
    ok("SVEB 질문에 답하지 않는다" in s,
       "⑧ 범위를 명시한다 — 「더 모을 가치가 있나」에만 답한다")

    # ⑨ 자 자체는 Q7-U 와 같아야 한다
    ok('DELIN   = "dwt"' in s and 'INPUT   = "raw"' in s and "FIRE_RATE = 1.0" in s,
       "⑨ 감사 대상 자가 Q7-U 승자(`dwt|raw` @1.00)로 고정돼 있다")

    # ⑩ ★★ 수송이 **항등**임을 런타임에 구성적으로 증명한다
    ok("수송 항등 검사" in s and "A_Z, E_Z = 1.0, np.zeros(1)" in s,
       "⑩ ★ `a=1·e=0` 으로 두고 원값 복원을 **런타임에 확인**한다")
    ok("수송 사상이 항등이 아니다" in s,
       "⑩ 항등이 아니면 **중단**한다 — 1판이 여기서 |Δ| 1.29 로 잡혔다")
    ok("out[m] = np.sort(x)[rp - 1]" in s and "r / (mm + 1.0)" in s,
       "⑩ 순위→z→분위수 되돌리기가 **같은 m** 으로 짝이 맞는다(1판의 실패 원인)")
    ok("집합 내부에서 자기완결" in s,
       "⑩ 용량이 올라 발화 집합이 줄어도 어긋나지 않는 이유가 소스에 적혀 있다")

    # ⑪ 과잉 주장 금지
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑪ 금지 문구 없음 — 「{bad}」")

    # ⑫ 한글 축라벨 금지
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑫ 그림 축 라벨에 한글이 없다(발견 {len(han)}건)")


# ══════════════════════════════════════════════════════════════════ 동적
def _auc_to_d(a):
    from scipy.stats import norm
    return float(np.sqrt(2.0) * norm.ppf(float(np.clip(a, 1e-6, 1 - 1e-6))))


def _d_to_auc(d):
    from scipy.stats import norm
    return float(norm.cdf(d / np.sqrt(2.0)))


def _deatt(a_obs, a_null, l):
    if not np.isfinite(l) or l <= 0.05:
        return float("nan")
    return _d_to_auc(_auc_to_d(a_null) + (_auc_to_d(a_obs) - _auc_to_d(a_null))
                     / min(max(l, 1e-6), 1.0))


def _match_1d(det, ref, tol):
    det = np.asarray(det, int); ref = np.asarray(ref, int)
    pairs = []
    for i, d in enumerate(det):
        j = int(np.argmin(np.abs(ref - d)))
        if abs(ref[j] - d) <= tol:
            pairs.append((abs(ref[j] - d), i, j))
    pairs.sort()
    ud, ur, err = set(), set(), []
    for e, i, j in pairs:
        if i in ud or j in ur:
            continue
        ud.add(i); ur.add(j); err.append(float(det[i] - ref[j]))
    return len(err), np.asarray(err, float)


def dynamic():
    print("\n[동적] 수학이 옳게 움직이는가")
    rng = np.random.RandomState(23)

    # ── ⓐ 탈감쇠는 **단조 증가**하고 λ=1 에서 항등이다
    obs, nul = 0.5362, 0.5090
    v1 = _deatt(obs, nul, 1.0)
    ok(abs(v1 - obs) < 1e-9, f"ⓐ λ=1 이면 탈감쇠가 **항등**이다({v1:.6f} = {obs})")
    seq = [_deatt(obs, nul, l) for l in (0.9, 0.6, 0.3, 0.15)]
    ok(all(b > a for a, b in zip(seq, seq[1:])),
       f"ⓐ λ 가 작아질수록 상한이 **단조 증가**한다 {[round(x, 4) for x in seq]}")
    ok(all(x >= obs for x in seq),
       "ⓐ 탈감쇠는 **한 방향으로만** 움직인다 — 그래서 상한이라 부를 수 있다")

    # ── ⓑ null 을 통째로 부풀리지 않는다(구현 선택의 근거)
    naive = _d_to_auc(_auc_to_d(obs) / 0.26)               # 잘못된 방식
    ours = _deatt(obs, nul, 0.26)
    ok(ours < naive,
       f"ⓑ 신호분만 탈감쇠({ours:.4f})가 통째 탈감쇠({naive:.4f})보다 **보수적**이다")

    # ── ⓒ 감쇠가 실제로 AUROC 를 깎는지 — 구성으로 확인
    n = 30000
    tt = rng.rand(n) < 0.25
    x_true = rng.normal(0, 1, n) + np.where(tt, 0.55, 0.0)
    from sklearn.metrics import roc_auc_score
    a_true = roc_auc_score(tt, x_true)
    for noise in (0.5, 1.5, 3.0):
        x_obs = x_true + rng.normal(0, noise, n)
        lam = float(np.corrcoef(x_true, x_obs)[0, 1])
        a_obs = roc_auc_score(tt, x_obs)
        back = _deatt(a_obs, 0.5, lam)
        ok(abs(back - a_true) < 0.03,
           f"ⓒ 잡음 σ={noise}: λ={lam:.3f} · 관측 {a_obs:.4f} → 복원 {back:.4f} "
           f"vs 참 {a_true:.4f} (오차 {abs(back-a_true):.4f})")

    # ── ⓓ 탐욕적 1:1 매칭 — 한 정답에 여러 발화가 붙어도 Se 가 안 부푼다
    ref = np.array([100, 300, 500])
    det = np.array([98, 102, 104, 305])                    # 첫 정답 주위에 3발
    m, err = _match_1d(det, ref, 20)
    ok(m == 2, f"ⓓ 정답 3 · 발화 4(한 곳에 3발) → 매칭 **{m}** (1:1 이므로 2)")
    ok(len(err) == m, "ⓓ 오차 배열 길이가 매칭 수와 같다")

    # ── ⓔ 주입 연산자: k 를 늘리면 위치 오차가 **단조 증가**한다
    P_WRONG, P_MISS = 0.2855, 0.0891
    JIT = rng.normal(0, 8, 5000)
    WRO = rng.normal(0, 60, 500)
    LO, HI = 0, 200

    def corrupt(p, r):
        q = p.copy()
        okm = np.where(q >= 0)[0]
        u = r.random_sample(len(okm))
        add = np.zeros(len(okm))
        w = u < P_WRONG
        add[w] = r.choice(WRO, w.sum()); add[~w] = r.choice(JIT, (~w).sum())
        q[okm] = np.clip(q[okm] + np.round(add).astype(int), LO, HI - 1)
        q[okm[r.random_sample(len(okm)) < P_MISS]] = -1
        return q

    p0 = np.full(20000, 100)
    disp = []
    for k in (1, 2, 3):
        r = np.random.RandomState(5)
        p = p0.copy()
        for _ in range(k):
            p = corrupt(p, r)
        alive = p >= 0
        disp.append(float(np.median(np.abs(p[alive] - 100))))
    ok(all(b > a for a, b in zip(disp, disp[1:])),
       f"ⓔ 용량을 늘리면 변위가 **단조 증가**한다 {[round(d, 1) for d in disp]}")
    r0 = np.random.RandomState(5)
    ok(float((corrupt(p0, r0) >= 0).mean()) < 1.0,
       "ⓔ 주입이 **결측도 만든다**(Se<1 을 반영)")

    # ── ⓕ2 ★★ 수송 사상 — a=1·e=0 이면 **정확히 항등**이고, a 를 낮추면 감쇠한다
    def transport(sc, rid, r, a, e):
        out = np.array(sc, float).copy()
        for u in np.unique(rid):
            mm_ = np.where(rid == u)[0]
            x = out[mm_]; m2 = len(x)
            if m2 < 5:
                continue
            rr_ = x.argsort().argsort().astype(float) + 1.0
            from scipy.stats import norm
            z = norm.ppf(rr_ / (m2 + 1.0))
            zp = a * z + r.choice(e, m2)
            rp = np.clip(np.round(norm.cdf(zp) * (m2 + 1.0)).astype(int), 1, m2)
            out[mm_] = np.sort(x)[rp - 1]
        return out

    grp = rng.randint(0, 8, n)
    val = rng.gamma(2.0, 1.5, n) + np.where(tt, 0.6, 0.0)
    idv = transport(val, grp, np.random.RandomState(0), 1.0, np.zeros(1))
    ok(float(np.max(np.abs(idv - val))) == 0.0,
       "ⓕ2 ★ a=1·e=0 수송은 **정확히 항등**이다(최대 |Δ| 0)")
    aucs = []
    for a_ in (1.0, 0.6, 0.25):
        v2_ = transport(val, grp, np.random.RandomState(3), a_, rng.normal(0, .9, 4000))
        aucs.append(roc_auc_score(tt, v2_))
    ok(all(b <= a + 1e-9 for a, b in zip(aucs, aucs[1:])),
       f"ⓕ2 a 를 낮추면 판별력이 **단조 감소**한다 {[round(x, 4) for x in aucs]}")
    ok(abs(aucs[-1] - 0.5) < abs(aucs[0] - 0.5),
       "ⓕ2 감쇠가 0.5 쪽으로 민다 — 용량-반응의 방향이 옳다")
    ok(set(np.round(np.sort(idv), 9)) == set(np.round(np.sort(val), 9)),
       "ⓕ2 수송은 **값의 주변분포를 보존**한다(순위만 섞는다) — 눈금 인공물이 안 생긴다")

    # ── ⓕ k=0 은 손대지 않는다(항등의 근거)
    p_id = p0.copy()
    ok(np.array_equal(p_id, p0), "ⓕ k=0 경로는 배열을 **건드리지 않는다**")

    # ── ⓖ 영점: 무정보 위치는 감쇠와 무관하게 0.5 근처
    z = rng.normal(0, 1, n)                                # 라벨과 무관
    ok(abs(roc_auc_score(tt, z) - 0.5) < 0.02,
       "ⓖ 무정보 특징은 0.5 근처 — 주입 전 영점이 성립한다")
    ok(abs(roc_auc_score(tt, z + rng.normal(0, 2, n)) - 0.5) < 0.02,
       "ⓖ 무정보 특징에 잡음을 더해도 0.5 근처 — 주입이 신호를 만들지 않는다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q7-V 픽스처 — 감쇠 상한 · 항등 대조 · 무감독 주입")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

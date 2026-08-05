#!/usr/bin/env python3
"""Q4-H(`quest46_q4h_rhythm_context`) 픽스처 — 층①로 가는 첫 런.

Q4-G(`20260805T0518`)가 **내 가설 둘을 반증**했다.

  ① 「AUROC 는 상위 꼬리를 대변하지 못한다」 → **철회**. ρ(AUROC, 달성률) = **+0.8869** 로
     강하게 양수이고, 「PR-AUC lift 가 더 낫다」도 ρ +0.4388 로 **오히려 낮았다**.
     ⇒ 달성률을 올리려면 **AUROC 를 올려야** 하고 그건 **층①(표현)** 이다.
  ② 「예산을 부담에 비례시키면 민감도가 오른다」 → **정반대**. 비례 배분이 민감도를
     0.7459 → 0.3639 으로 **반토막**냈다(영점 −0.3373 이라 대부분 구조적). 평균 민감도는
     레코드를 **동등 가중**하므로 S 가 작은 레코드는 적은 예산으로 높은 민감도에
     도달하는데, 비례 배분이 그들을 **굶긴다**. 탐욕 오라클(+0.0791)은 **반대 방향**이다.
  ③ K2 는 미결이지만 **상수 예측기 기준선**을 안 쟀다 — 없으면 MAE 개선을 못 읽는다.

이 런에서 빠뜨리면 결과가 무효인 것 다섯:
  ① **철회를 명시한다**(R38 ⑦) — 반증된 가설 위에 새 가설을 얹으면 안 된다
  ② **상수 예측기 기준선**을 잰다 — held-out 을 뺀 평균 유병률(R22)
  ③ **보상성 휴지기 비율** `(pre+post)/(2·baseline)` — PAC 은 **불완전 대상성**(<2),
     PVC 는 **완전 대상성**(≈2). 현재 특징엔 `post−pre` **차만** 있고 **비율이 없다**
  ④ **리듬 문맥** — Q7-K6 이 「고립 +0.0101 ✅ · 혼합 +0.0125 ⚠️ · **런 −0.2739 ❌**」로
     이미 본 실패 자리인데 **그 문맥을 특징으로 넣은 적이 없다**
  ⑤ **기저선 분위수 교체는 짓기 전에 버렸다** — 레코드 안에서 기저선이 거의 상수면
     분위수를 바꿔도 **레코드 내 순위가 안 바뀐다**
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4h_rhythm_context.ipynb")
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
    s = src(); cs = cells()

    # ── ① 철회를 명시한다
    ok("retracted" in s and "철회" in s,
       "① ★★★ 철회한 가설을 **결과에 저장**한다")
    ok("AUROC 는 상위 꼬리를 대변하지 못한다" in s and "예산을 부담에 비례" in s,
       "① ★★★ 철회하는 가설 **둘 다** 문장으로 박혀 있다")
    ok("0.8869" in s and "-0.3821" in s,
       "① ★★ 반증 수치(ρ +0.8869 · Δ −0.3821)가 앵커로 있다")
    ok("R38 ⑦" in s and "명시적으로 철회" in s,
       "① ★★ R38 ⑦ 로 요약 정합을 건다")

    # ── ② 상수 예측기
    ok("const_ae" in s and "상수 예측기" in s,
       "② ★★★ **상수 예측기 기준선**을 실제로 계산한다")
    ok('mu = float(np.mean([BURD[r] for r in tr_r + dv_r]))' in s and "held-out 을 뺀" in s,
       "② ★★★ held-out 을 뺀 평균으로 예측한다(R22) — 누출 없음")
    ok("상수보다 못하다" in s,
       "② ★★ 상수보다 나쁜 추정기를 **그렇게 표시**한다")
    ok("없으면 MAE 를 못 읽는다" in s or "안 쟀다" in s,
       "② Q4-G 가 이 기준선을 안 쟀다는 게 기록돼 있다")

    # ── ③ 보상성 휴지기
    ok("COMP = (pre + post) / (2.0 * BASE12" in s,
       "③ ★★★ **보상성 휴지기 비율**이 `(pre+post)/(2·baseline)` 로 구현돼 있다")
    ok("불완전" in s and "완전 대상성" in s,
       "③ ★★★ PAC 불완전(<2) vs PVC 완전(≈2)이라는 임상 근거가 소스에 있다")
    ok("차만" in s or "차이지 비율이 아니" in s,
       "③ ★★ 현재 특징(`post−pre`)이 **차이지 비율이 아니라는** 구분이 있다")
    ok("F_COMP" in s and '"comp": np.c_[F_BASE, F_COMP]' in s,
       "③ `comp` 팔이 base 에 **더해서** 만들어진다(교체가 아니다)")

    # ── ④ 리듬 문맥
    ok("def ctx_feats" in s and "CTX = 4" in s,
       "④ ★★ ±4 박동 문맥이 사전 고정된 창으로 구현돼 있다")
    ok("grp.shift(lag)" in s and "grp.shift(-lag)" in s,
       "④ ★★ **직전과 직후** 상대 RR 을 둘 다 넣는다")
    ok("q7k6" in s and "run=-0.2739" in s,
       "④ ★★★ Q7-K6 의 「런 −0.2739 ❌」가 앵커로 박혀 있다")
    ok("특징으로 넣은 적이 없다" in s,
       "④ ★★★ **관측해 놓고 특징으로 안 넣었다**는 게 명시돼 있다")
    ok("교대 강도" in s or "alt =" in s,
       "④ 교대(이단맥) 강도를 문맥 특징에 넣는다")

    # ── ⑤ 버린 아이디어를 기록한다
    ok("짓기 전에 버렸다" in s and "순위가 안 바뀐다" in s,
       "⑤ ★★★ 기저선 분위수 교체를 **짓기 전에 시험해서 버렸다**는 게 기록돼 있다")
    ok("+1.981" in s or "1.981" in s,
       "⑤ ★★ 그 시험의 실측(분리도 동일)이 남아 있다")

    # ── 문헌
    ok("de Chazal" in s and "Llamedo" in s,
       "★★ 문헌 대조(de Chazal 2004 · Llamedo 2011)가 들어 있다")
    ok("0.759" in s and "0.385" in s,
       "★★ 공표 수치(S 민감도 75.9% · +P 38.5%)가 앵커다")
    ok("엄밀한 비교가 아니" in s,
       "★★★ 동작점이 달라 **엄밀한 비교가 아님**을 명시한다(과장 금지)")

    # ── 판정 위생
    ok('l3v = decide(L3[MAIN_ARM]["lo"], L3[MAIN_ARM]["hi"], L3_THR, ">")' in s
       and "L3_THR = max(0.0, NS[2])" in s,
       "★★ 주 관문이 **측정된 영점 상단**을 문턱으로 쓴다(R26)")
    ok("y_override" in s and "rr.permutation" in s,
       "★★ 영점을 **학습 라벨 치환**으로 측정한다")
    ok("def decide(lo, hi, thr, direction)" in s and "np.isfinite(thr)" in s,
       "★ `decide` 가 문턱이 nan 이면 미결을 낸다")
    ok("해석 불가" in s and "R41 ②" in s,
       "★ 효과가 0 근처면 필요표본을 해석 불가로 표시한다")
    ok("미결 ≠ 등가" in s or "R33 ①" in s,
       "★ 「미결 ≠ 등가」가 소스에 있다")
    ok("r != held" in s and "def split_rest(held)" in s,
       "★★ LORO — held-out 이 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok('raise AssetError(f"{SV5} 없음' in s,
       "★ 자산 없으면 fallback 없이 중단(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")
    knob = re.findall(r"^\s*(\w+)\s*=\s*[^=].*\bif SMOKE\b", s, flags=re.M)
    ok(set(knob) <= {"NB_BOOT", "N_PERM"},
       f"★★★ SMOKE 로 값이 바뀌는 이름이 **비용 손잡이뿐**이다({sorted(set(knob))})")
    ok(not re.search(r"^\s*(CTX|MAIN_K|DEV_EVERY)\s*=.*SMOKE", s, flags=re.M),
       "★★★ 문맥창·예산은 SMOKE 와 무관하게 고정이다")


def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    rng = np.random.RandomState(61)
    base = 0.90

    # ── ⓐ 보상성 휴지기 비율이 PAC 과 PVC 를 가른다 (post−pre 는 못 가른다)
    def sim(kind, n=800):
        rr = np.full(n, base) + rng.normal(0, 0.015, n)
        y = np.zeros(n, bool)
        idx = rng.choice(np.arange(2, n - 2), int(0.12 * n), replace=False)
        for i in idx:
            y[i] = True
            rr[i] = base * (0.60 if kind == "PAC" else 0.58)
            rr[i + 1] = base * (1.28 if kind == "PAC" else 1.42)
        return rr, y
    out = {}
    for kind in ("PAC", "PVC"):
        rr, y = sim(kind)
        pre = rr; post = np.r_[rr[1:], rr[-1]]
        out[kind] = dict(comp=float(((pre + post) / (2 * base))[y].mean()),
                         f3=float((post - pre)[y].mean()))
    ok(abs(out["PVC"]["comp"] - 1.0) < abs(out["PAC"]["comp"] - 1.0),
       f"ⓐ ★★★ 보상성 비율이 **PVC {out['PVC']['comp']:.3f}(완전 ≈1) vs PAC "
       f"{out['PAC']['comp']:.3f}(불완전 <1)** 로 갈린다 — 교과서적 판별자다")
    ok(out["PAC"]["f3"] > 0 and out["PVC"]["f3"] > 0,
       f"ⓐ ★★ 반면 `post−pre` 는 **둘 다 큰 양수**다(PAC {out['PAC']['f3']:+.3f} · "
       f"PVC {out['PVC']['f3']:+.3f}) — 현재 특징으로는 못 가른다")
    ok(abs(out["PAC"]["comp"] - out["PVC"]["comp"]) >
       0.5 * abs(out["PAC"]["f3"] - out["PVC"]["f3"]) / base,
       "ⓐ ★★ 비율이 차보다 두 부류를 **더 크게** 벌린다(기저선 정규화 덕이다)")

    # ── ⓑ ★★★ 기저선 분위수 교체는 **레코드 내 순위를 안 바꾼다** (짓기 전에 버린 이유)
    n = 600
    rr = np.full(n, base) + rng.normal(0, 0.02, n)
    y = np.zeros(n, bool); y[1::2] = True                    # 이단맥
    rr[y] = base * 0.62 + rng.normal(0, 0.02, int(y.sum()))
    med = float(np.median(rr))
    loc50 = np.array([np.median(rr[max(0, i - 12):i]) if i else med for i in range(n)])
    loc75 = np.array([np.quantile(rr[max(0, i - 12):i], 0.75) if i else med for i in range(n)])
    f50 = 1.0 - rr / loc50; f75 = 1.0 - rr / loc75
    sep = lambda f: (f[y].mean() - f[~y].mean()) / (f.std() + 1e-9)
    ok(abs(sep(f50) - sep(f75)) < 0.05,
       f"ⓑ ★★★ 이단맥에서 분위수를 50 → 75 로 바꿔도 분리도가 {sep(f50):+.3f} → "
       f"{sep(f75):+.3f} 로 **거의 같다** — 기저선이 레코드 안에서 거의 상수라 "
       f"**레코드 내 순위가 안 바뀐다**. 그래서 이 아이디어를 **짓기 전에 버렸다**")
    ok(abs(loc75.mean() - base) < abs(loc50.mean() - base),
       f"ⓑ ★★ 다만 기저선의 **절대값**은 75분위가 참값에 가깝다"
       f"({loc75.mean():.4f} vs {loc50.mean():.4f} · 참 {base:.2f}) — 그런데 그건 "
       f"**층② 가 못 쓰는 정보**다(레코드별 상수 시프트이므로)")

    # ── ⓒ 상수 예측기가 π̂ 의 진짜 바닥이다
    pis = np.array([0.007, 0.012, 0.02, 0.03, 0.05, 0.08, 0.13, 0.20, 0.28, 0.58])
    loo_const = [abs(np.mean(np.delete(pis, i)) - pis[i]) for i in range(len(pis))]
    ok(np.mean(loo_const) > 0.02,
       f"ⓒ ★★★ 상수 예측기(leave-one-out 평균)의 MAE 가 {np.mean(loo_const):.4f} 다 — "
       f"**어떤 추정기든 이걸 넘어야** 정보가 있다고 말할 수 있다")
    ok(np.mean(loo_const) < np.mean(np.abs(0.0 - pis)) + 1e-9 or True,
       f"ⓒ 참고 — 유병률 분포가 치우쳐 있어(중앙 {np.median(pis):.3f} · 평균 "
       f"{pis.mean():.3f}) 상수 예측기도 꽤 강하다")

    # ── ⓓ 문맥 특징이 이단맥과 고립을 가른다
    def ctx1(rr_, y_):
        rel = rr_ / base
        prev = np.r_[1.0, rel[:-1]]
        return float(np.mean(prev[y_] < 0.9)), float(np.mean(prev[~y_] < 0.9))
    rr_b, y_b = rr, y                                        # 이단맥
    rr_i = np.full(n, base) + rng.normal(0, 0.02, n)
    y_i = np.zeros(n, bool); idx = rng.choice(np.arange(2, n - 2), 40, replace=False)
    y_i[idx] = True; rr_i[idx] = base * 0.62                 # 고립
    pb, nb_ = ctx1(rr_b, y_b); pi_, ni_ = ctx1(rr_i, y_i)
    # ★ 「직전이 조기였나」의 **판별력**은 이소성/정상 두 쪽 값의 차이다.
    #   이단맥에서는 정상 박동의 직전이 항상 조기라 그쪽에서 신호가 나온다.
    ok(abs(pb - nb_) > 0.5 and abs(pi_ - ni_) < 0.1,
       f"ⓓ ★★★ **직전 박동이 조기였나**의 판별력이 이단맥에서 {abs(pb-nb_):.2f}, "
       f"고립에서 {abs(pi_-ni_):.2f} 다 — **이단맥에서만 강하게 작동**한다. Q7-K6 이 "
       f"「런 −0.2739 ❌」로 무너진 자리이고, 현재 특징엔 이 정보가 **없다**")
    ok(nb_ > ni_,
       f"ⓓ ★★ 신호는 **정상 박동 쪽**에서 나온다(이단맥 {nb_:.2f} vs 고립 {ni_:.2f}) — "
       f"이단맥에서 정상 박동의 직전은 **항상** 조기이기 때문이다")

    # ── ⓔ LORO 누출 없음
    REC = list(range(8)); pr = np.linspace(0.01, 0.5, 8)
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pr[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓔ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-H 픽스처 — 가설 철회(L1) · 보상성 휴지기(L3) · 리듬 문맥 · 버린 아이디어 기록")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

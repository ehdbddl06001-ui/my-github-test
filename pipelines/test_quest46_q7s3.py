#!/usr/bin/env python3
"""Q7-S″(`quest46_q7s3_recompute`) 픽스처.

정적 — 노트북 소스를 직접 뜯어 **설계 불변식**을 강제한다.
동적 — 구성한 코호트에서 **추정량이 옳게 움직이는지** 확인한다.

★ 이 런의 핵심은 셋이다.
  ① 필요 표본을 **우월 프레임**으로도 낸다(Q7-S′ 는 등가로만 냈고, 그래서 S3 를
     「도달 불가」로 오분류했다)
  ② 주 대비를 **영점 기준**(`palign − shuf5`)으로 — 옛 대비는 빈 것끼리였다
  ③ **`f1` 항등 대조** — 「정확 매칭」이 정말 정확한지 처음으로 잰다
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q7s3_recompute.ipynb")

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

    # ① 우월 프레임이 실제로 들어 있고, 등가와 **나란히** 나온다
    ok("def need_super" in s and "def need_equiv" in s,
       "① 필요 표본 함수가 **둘 다** 있다(등가·우월)")
    ok("2.04" in s,
       "① 검정력 80% 환산 계수 2.04 = (1.96+0.84)²/1.96² 가 명시돼 있다")
    ok(s.count('"sup50"') + s.count("sup50=") >= 2 and "sup80" in s,
       "① 우월 필요표본을 50%·80% **둘 다** 낸다")

    # ② 주 대비가 영점 기준이다
    ok('ZERO_ARM   = "shuf5"' in s or 'ZERO_ARM = "shuf5"' in s,
       "② 영점 팔이 `shuf5` 로 선언돼 있다")
    ok("D[GATE_ARM] - D[ZERO_ARM]" in s,
       "② 주 대비 W1 이 **짝지은 차** `palign − shuf5` 다")
    ok('DIFF["W1"]' in s,
       "② W1 이 판정 대상(DIFF)에 등록된다")
    # 옛 대비는 남되 **보조로 강등**돼야 한다
    ok("보조로 강등" in s and 'D["palign"] - D["pmorph"]' in s,
       "② 옛 대비(`palign − pmorph`)는 남기되 **보조로 강등**한다고 소스에 적혀 있다")
    # R36 ⑤ — 차이를 성분과 함께 찍는다
    ok("성분" in s and "a=float(np.nanmean(D[GATE_ARM]))" in s,
       "② 차이를 **성분과 함께** 기록한다(R36 ⑤)")

    # ③ f1 항등 대조
    ok("matched_stats(f1[idx], idx, w)" in s,
       "③ ★ **`f1` 자신**을 같은 매칭에 통과시킨다(항등 대조 · R35 ④)")
    ok("IDENTITY_TOL" in s,
       "③ 항등 허용치가 상수로 선언돼 있다")
    ok("MATCH_W" in s and "def match_key" in s,
       "③ 매칭 폭 곡선이 있다")
    # 항등 대조는 **잔차화하지 않은 원값**이어야 한다
    ok("resid(f1" not in s,
       "③ 항등 대조에 `resid(f1…)` 를 쓰지 않는다 — 잔차화하면 정의상 0 이 된다")
    ok("S3 를 철회" in s,
       "③ 항등 대조가 깨지면 **S3 를 철회**한다고 소스에 박혀 있다")

    # ④ 재현 증명이 **중단**으로 이어진다
    ok("raise AssetError" in s and "재현 증명 실패" in s,
       "④ W0 재현 실패 시 **AssetError 로 중단**한다(R35 ⑦)")
    ok("REF = {" in s and "20260804T0658" in s,
       "④ 기준값이 Q7-S′ 공식 실행 ID 와 함께 박혀 있다")

    # ⑤ 프로브 선택 편의 — Q7-S′ 가 자백한 것을 고쳤나
    ok("max_probe" in s and "선택 편의" in s,
       "⑤ 프로브를 **LORO 로** 고르고 max 선택과의 편의를 정량한다(R34 ②)")
    ok("np.nanmean(\n            [per_by_probe[p][o] for o in per_by_probe[p] if o != r]" in s
       or "if o != r] or [-np.inf])" in s,
       "⑤ LORO 선택이 **자기 레코드를 뺀** 평균으로 이뤄진다")

    # ⑥ 누수 — 개인 기준은 N 비트에서만 (Q7-S′ 에서 이어받은 불변식)
    ok("nmask = (Y == 0)" in s and "m & nmask" in s,
       "⑥ 개인 기준(pr_ref·sc_ref)을 **N 비트에서만** 잡는다(R22)")
    ok("np.setdiff1d(te0, used)" in s,
       "⑥ 개인화에 쓴 비트는 **양쪽 팔 모두** 평가에서 뺀다(R22)")

    # ⑦ 새 데이터 0 — 학습·다운로드가 없다
    ok("nk.ecg_delineate" not in s and "wfdb" not in s,
       "⑦ 이 런은 **새 자료를 만들지 않는다** — 구획·다운로드 코드가 없다")
    ok("torch" not in s and "keras" not in s,
       "⑦ 딥러닝이 없다 — 로지스틱 회귀만")

    # ⑧ R36 ① — 미결이면 상한을 쓴다
    ok("상한" in s and "R36 ①" in s,
       "⑧ 미결일 때 **CI 상단을 상한으로** 쓴다고 박혀 있다(R36 ①)")

    # ⑨ 과잉 주장 금지 (Q7-U 픽스처 ⑩b 계열 회귀)
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑨ 금지 문구 없음 — 「{bad}」")

    # ⑩ 한글 축라벨 금지(Colab 폰트 없음)
    import re
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑩ 그림 축 라벨에 한글이 없다(발견 {len(han)}건)")


# ══════════════════════════════════════════════════════════════════ 동적
def _matched(v, f1v, tt, w):
    """노트북 `matched_stats` 의 독립 재구현 — 같은 답을 내야 한다."""
    key = (np.floor(f1v / float(w) + 0.5) if w > 1 else np.round(f1v)).astype(int)
    win = tie = tot = 0.0
    for kk in np.unique(key):
        m = np.where(key == kk)[0]
        a = v[m[tt[m]]]; b = v[m[~tt[m]]]
        if not len(a) or not len(b):
            continue
        d = a[:, None] - b[None, :]
        win += float((d > 0).sum()); tie += float((d == 0).sum()); tot += float(d.size)
    return (win + 0.5 * tie) / tot if tot else float("nan")


def dynamic():
    print("\n[동적] 추정량이 옳게 움직이는가")
    rng = np.random.RandomState(11)

    # ── ⓐ 항등 대조가 **누출을 잡는가** — f1 이 완전 상수인 층이면 정확히 0.5
    n = 4000
    f1v = rng.randint(0, 12, n).astype(float)          # 정수 = 층 안에서 상수
    tt = rng.rand(n) < 0.3
    a = _matched(f1v, f1v, tt, 1)
    ok(abs(a - 0.5) < 1e-9,
       f"ⓐ 층 안에서 `f1` 이 상수면 항등 대조가 **정확히 0.5** ({a:.6f})")

    # ── ⓑ 층 **안에** 남은 조기성을 항등 대조가 잡는가 (이게 S3 를 무효화하는 시나리오)
    f1c = f1v + np.where(tt, 0.42, -0.42)              # 같은 층인데 S 가 미세하게 이르다
    leak1 = _matched(f1c, f1c, tt, 1)
    ok(leak1 > 0.9,
       f"ⓑ 층 안에 잔여 조기성이 있으면 항등 대조가 **크게 발화**한다({leak1:.4f}) — "
       "이 값이 0.5 를 뜨면 「정확 매칭」이 조기성을 통제한 적이 없다는 뜻")

    # ── ⓑ2 연속 `f1`(실제 자료의 모습)에서는 **폭이 넓어질수록** 누출이 커진다
    f1k = rng.normal(0, 6, n) + np.where(tt, 3.0, 0.0)  # S 가 평균적으로 이르다
    cur = [abs(_matched(f1k, f1k, tt, w) - 0.5) for w in (1, 4, 16, 64)]
    ok(all(b >= a - 1e-9 for a, b in zip(cur, cur[1:])),
       f"ⓑ2 연속 `f1` 에서 누출이 폭에 대해 **단조 증가**한다 "
       f"{[round(c, 4) for c in cur]} — 폭 곡선이 읽을 수 있는 구간을 정한다")

    # ── ⓒ 진짜 신호는 살아남는다 (기각기 전용이 아님)
    sig = rng.normal(0, 1, n) + np.where(tt, 0.8, 0.0)
    a_sig = _matched(sig, f1v, tt, 1)
    ok(a_sig > 0.6, f"ⓒ 층과 무관한 진짜 신호는 매칭 안에서도 살아남는다({a_sig:.4f})")

    # ── ⓓ 조기성 대리변수는 **정확 매칭에서 죽는다**(R24 정면)
    proxy = f1v * 3.0 + rng.normal(0, 0.01, n)         # f1 의 결정론적 함수
    a_px = _matched(proxy, f1v, tt, 1)
    ok(abs(a_px - 0.5) < 0.05,
       f"ⓓ `f1` 의 함수인 대리변수는 정확 매칭에서 **0.5 로 죽는다**({a_px:.4f})")

    # ── ⓔ 필요 표본: 등가 vs 우월이 **다른 답**을 낸다(이 런의 존재 이유)
    def need_equiv(nn, half, mean, margin=0.01):
        slack = margin - abs(mean)
        return None if slack <= 0 else nn * (half / slack) ** 2

    def need_super(nn, half, mean, p80=False):
        r = nn * (half / abs(mean)) ** 2
        return r * 2.04 if p80 else r

    # Q7-S′ S3 실측: n=34 · 초과 +0.0272 · 반폭 0.0531
    e = need_equiv(34, 0.0531, 0.0272)
    s50 = need_super(34, 0.0531, 0.0272)
    s80 = need_super(34, 0.0531, 0.0272, True)
    ok(e is None,
       "ⓔ S3 는 **등가 프레임에서 도달 불가**다(초과가 여유 0.01 밖) — Q7-S′ 재현")
    # ★ S3 의 단위는 **매칭 가능 레코드**다 — 총 레코드로 환산해야 풀(126/201)과 비교된다
    rate = 34 / 56
    ok(120 < s50 < 145,
       f"ⓔ 우월 50% 는 **매칭 가능 {s50:.0f}개** — 등가의 「도달 불가」와 완전히 다른 답")
    ok(200 < s50 / rate < 230 and 420 < s80 / rate < 460,
       f"ⓔ 총 레코드 환산 — 50% **{s50/rate:.0f}** · 80% **{s80/rate:.0f}**. "
       "★ 50% 는 풀링 201 에 근접하지만 **80% 는 못 넘는다** — "
       "프레임이 바꾸는 건 「불가능」→「비싸다」이지 「도달권」이 아니다")
    # S2 는 반대로 우월이 훨씬 비싸다
    e2 = need_equiv(56, 0.0143, 0.0035)
    s2 = need_super(56, 0.0143, 0.0035)
    ok(e2 is not None and s2 > 3 * e2,
       f"ⓔ S2 는 등가 {e2:.0f} 보다 우월 {s2:.0f} 가 훨씬 비싸다 — **프레임이 순위를 뒤집는다**")

    # ── ⓕ 짝지은 차가 짝 안 지은 차보다 좁은가(W1 을 짝지은 차로 만든 이유)
    base = rng.normal(0, 0.02, 56)                     # 레코드 공통 성분
    arm = base + rng.normal(0.004, 0.004, 56)
    zero = base + rng.normal(0.000, 0.004, 56)
    def half(v):
        b = [np.mean(v[rng.randint(0, len(v), len(v))]) for _ in range(2000)]
        return (np.percentile(b, 97.5) - np.percentile(b, 2.5)) / 2
    h_paired = half(arm - zero)
    h_naive = np.hypot(half(arm), half(zero))
    ok(h_paired < h_naive,
       f"ⓕ 짝지은 차의 CI 가 더 좁다({h_paired:.5f} < {h_naive:.5f}) — 공통 분산 상쇄")

    # ── ⓖ 빈 팔에서 빈 팔을 빼면 **아무것도 안 나온다**(옛 S5 의 문제)
    empty_a = rng.normal(0, 0.01, 56)
    empty_b = rng.normal(0, 0.01, 56)
    d = empty_a - empty_b
    hd = half(d)
    ok(abs(np.mean(d)) < hd,
       f"ⓖ 빈 것 − 빈 것 은 0 을 못 뗀다({np.mean(d):+.5f}, 반폭 {hd:.5f}) — "
       "옛 대비가 창 특이성을 증명 못 한 이유")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q7-S″ 픽스처 — 프레임 정정 · 영점 기준 대비 · `f1` 항등 대조")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

#!/usr/bin/env python3
"""Q7-AA(`quest46_q7aa_burden_target`) 픽스처.

**사전등록 단발**이라 지킬 것이 셋뿐이고, 셋 다 무겁다:
  ① 문턱은 **중앙값 하나** — 다른 문턱을 훑지 않는다(선택 편의 금지)
  ② **영점이 관문보다 먼저** — 부담 절단 자체가 값을 만들면 주 관문을 읽지 않는다
  ③ 결정 숫자는 **W1** 이고 **탈감쇠하지 않는다**(Q7-Z 가 그 모형을 기각했다)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q7aa_burden_target.ipynb")

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

    # ① 문턱은 중앙값 하나 · 단발
    ok('BURDEN_RULE = "cohort_median"' in s and "THR = float(np.median(" in s,
       "① 문턱이 **코호트 중앙값**으로 선언돼 있다")
    ok("문턱은 이것 하나뿐" in s and "다른 문턱을 훑지 않는다" in s,
       "① ★ 다른 문턱을 훑지 않는다고 소스에 박혀 있다(R34 ②)")
    ok("단발" in s and "문턱을 바꿔 다시 돌리지 않는다" in s,
       "① ★★ **단발**임이 명시돼 있다 — 결과로 문턱을 바꾸지 않는다")
    ok(s.count("np.median(list(BURD_ALL.values()))") == 1,
       "① 문턱 계산이 **한 곳뿐**이다 — 여러 군데서 다시 잡으면 훑는 것과 같다")
    ok("S3(매칭 가능" in s and "W1(판정" in s,
       "① ★ **같은 문턱**을 S3(매칭 가능)와 W1(판정 코호트)에 똑같이 적용한다")

    # ② 영점이 먼저
    ok('perm="stratum"' in s and "N_PERM = 50" in s,
       "② 영점이 **층내 치환**이고 reps=50 이다(Q7-Z 가 확정 · R39 ①)")
    ok("lo\"] <= 0.5 <= AA3" in s or "AA3[k][\"lo\"] <= 0.5 <= AA3[k][\"hi\"]" in s,
       "② ★ 판정이 **CI 가 0.5 를 덮는가** 다 — 절대 편차 문턱은 부분군 크기에 불공평")
    ok("AA1 을 읽지 않는다" in s and "⛔ 측정 불가" in s,
       "② ★★ 영점이 깨지면 **주 관문을 안 읽는다**(R29 ②)")
    ok("부담 절단 자체가 값을 만든다" in s,
       "② 왜 영점이 필요한지가 소스에 적혀 있다")

    # ③ 주 관문은 측정된 null 기준 · 저부담 대조가 있다
    ok('decide(d1["lo"], d1["hi"], NULL_HI, ">")' in s,
       "③ ★ AA1 판정이 **측정된 null 기준**이다 — 0.5 가 아니다")
    ok('decide(d2["lo"], d2["hi"], NULL_LO, ">")' in s,
       "③ 저부담 대조도 **자기 null 기준**으로 판정한다")
    ok("여기서도 오르면" in s and "추정 안정성" in s,
       "③ ★ 둘 다 오르면 부담이 아니라 **추정 안정성**이라고 미리 적혀 있다")

    # ④ 결정 숫자 — W1, 탈감쇠 금지
    ok("탈감쇠로 부풀릴 수 없다" in s,
       "④ ★★ Q7-Z 이후 **탈감쇠 금지**가 소스에 박혀 있다")
    ok("auc_to_d" not in s and "deatt" not in s and "/ lam" not in s,
       "④ ★★★ 코드에 **탈감쇠 연산이 아예 없다** — 기각된 모형을 다시 쓰지 않는다")
    ok("S3 는 기전" in s and "W1" in s,
       "④ S3(기전)와 W1(효용)을 구분해 적어 둔다")
    ok("CI 와 함께만" in s,
       "④ 결정 숫자를 **CI 와 함께만** 인용한다(R36 ①)")
    ok("shuf5" in s and 'lambda a, b: float(b.mean() - a.mean())' in s,
       "④ W1 이 `palign − shuf5` **짝지은 차**다")

    # ⑤ 종결 문장이 준비돼 있다
    ok("형태 갈래를 종결한다" in s and "ΔAUPRC ≤ +0.014" in s,
       "⑤ ★★ 미결일 때 쓸 **최종 문장**이 코드에 있다 — 나중에 지어내지 않는다")
    ok("λ 0.26→0.49" in s,
       "⑤ 종결 문장이 Q7-Z 의 근거를 함께 담는다")

    # ⑥ 재현 · 검산표 · 위생
    ok("AA0 실패" in s and "raise AssetError" in s,
       "⑥ Q7-Z 와 같은 계산이 아니면 **중단**한다")
    ok("CHECK = [" in s and "미검정" in s and "틀리면" in s,
       "⑥ **결론 검산표**가 코드에 있다(R38 ①)")
    ok("BUT" not in s.replace("BURD", "") or "but-pdb" not in s,
       "⑥ BUT PDB 를 쓰지 않는다 — λ 는 이 런의 질문이 아니다")
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑥ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑥ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 절차가 옳게 움직이는가")
    rng = np.random.RandomState(53)

    def matched(v, key, tt):
        win = tie = tot = 0.0
        for kk in np.unique(key):
            m = np.where(key == kk)[0]
            a = v[m[tt[m]]]; b = v[m[~tt[m]]]
            if not len(a) or not len(b):
                continue
            d = a[:, None] - b[None, :]
            win += float((d > 0).sum()); tie += float((d == 0).sum()); tot += float(d.size)
        return (win + 0.5 * tie) / tot if tot else np.nan

    # ── ⓐ ★★ 부담으로 자르면 **추정이 안정**되지만 **기댓값은 0.5** 다
    #    (그래서 AA2 대조와 AA3 영점이 둘 다 필요하다)
    def one_record(n_beat, burden, seed):
        r = np.random.RandomState(seed)
        key = r.randint(0, 25, n_beat)
        tt = r.rand(n_beat) < burden
        v = r.normal(0, 1, n_beat)                 # ★ 신호 **없음**
        return matched(v, key, tt)
    hi = [one_record(2400, 0.30, 100 + i) for i in range(200)]
    lo = [one_record(2400, 0.03, 300 + i) for i in range(200)]
    hi = np.array([x for x in hi if np.isfinite(x)])
    lo = np.array([x for x in lo if np.isfinite(x)])
    ok(abs(hi.mean() - 0.5) < 0.01 and abs(lo.mean() - 0.5) < 0.01,
       f"ⓐ 신호가 없으면 부담과 무관하게 **기댓값 0.5** (고 {hi.mean():.4f} · 저 {lo.mean():.4f})")
    ok(hi.std() < lo.std(),
       f"ⓐ ★★ 그런데 **고부담이 훨씬 안정적**이다(SD 고 {hi.std():.4f} < 저 {lo.std():.4f}) — "
       "그래서 부분군 비교는 **각자의 영점 기준**으로 해야 한다")

    # ── ⓑ 절대 편차 문턱은 부분군 크기에 **불공평**하다 (CI 기준으로 바꾼 이유)
    def half(v, seed):
        r = np.random.RandomState(seed)
        b = [v[r.randint(0, len(v), len(v))].mean() for _ in range(800)]
        return (np.percentile(b, 97.5) - np.percentile(b, 2.5)) / 2
    h_big, h_small = half(hi[:34], 1), half(hi[:9], 1)
    ok(h_small > h_big,
       f"ⓑ ★ 표본이 작으면 CI 가 넓다(n=9 {h_small:.4f} > n=34 {h_big:.4f}) — "
       "**절대 편차 0.005** 로 재면 작은 부분군만 부당하게 통과/탈락한다")

    # ── ⓒ 신호가 **고부담에만** 있으면 절차가 그걸 잡는가 (양성 대조)
    def one_signal(n_beat, burden, eff, seed):
        r = np.random.RandomState(seed)
        key = r.randint(0, 25, n_beat)
        tt = r.rand(n_beat) < burden
        v = r.normal(0, 1, n_beat) + np.where(tt, eff, 0.0)
        return matched(v, key, tt)
    sig_hi = np.array([one_signal(2400, 0.30, 0.25, 500 + i) for i in range(60)])
    sig_lo = np.array([one_signal(2400, 0.03, 0.00, 700 + i) for i in range(60)])
    ok(sig_hi.mean() > 0.53 and abs(sig_lo.mean() - 0.5) < 0.01,
       f"ⓒ ★ 고부담에만 신호를 심으면 고 {sig_hi.mean():.4f} · 저 {sig_lo.mean():.4f} — "
       "절차가 **부담 집중을 잡는다**(기각기 전용이 아니다)")

    # ── ⓓ 중앙값 문턱은 **한 번만** — 문턱을 훑으면 최댓값이 부풀려진다
    burd = rng.uniform(0.01, 0.35, 34)
    per = 0.5 + rng.normal(0, 0.05, 34)            # ★ 부담과 **무관**
    med_val = per[burd >= np.median(burd)].mean()
    best = max(per[burd >= t].mean() for t in np.quantile(burd, np.linspace(.1, .9, 17)))
    ok(best > med_val,
       f"ⓓ ★★ 신호가 없어도 문턱을 훑으면 최댓값이 부풀려진다"
       f"(중앙값 고정 {med_val:.4f} → 17개 훑기 최댓값 {best:.4f}) — **단발이어야 하는 이유**")

    # ── ⓔ 필요표본은 효과² 반비례이고, 부분군은 n 이 절반이다
    def need(n, half_, eff, p80=False):
        r = n * (half_ / abs(eff)) ** 2
        return r * 2.04 if p80 else r
    n_full = need(34, 0.0504, 0.0416)
    n_sub_same = need(17, 0.0504 * np.sqrt(2), 0.0416)      # 효과 같고 n 절반
    n_sub_2x = need(17, 0.0504 * np.sqrt(2), 0.0832)        # 효과 2배
    ok(abs(n_sub_same - n_full) < 1e-6,
       f"ⓔ ★★ 효과가 같으면 필요표본이 **정확히 같다**({n_full:.0f} = {n_sub_same:.0f}) — "
       "n 이 절반이면 CI 가 √2 넓어져 `n×(반폭/효과)²` 가 상쇄된다. "
       "**부분군으로 자르는 것 자체는 공짜도 손해도 아니다**")
    ok(n_sub_2x < n_full,
       f"ⓔ ★ 효과가 2배여야 비로소 이득이다({n_sub_2x:.0f} < {n_full:.0f}) — "
       "「부분군이니 싸진다」는 자동이 아니다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q7-AA 픽스처 — 사전등록 단발 · 영점 우선 · 결정 숫자는 W1")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

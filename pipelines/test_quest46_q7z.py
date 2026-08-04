#!/usr/bin/env python3
"""Q7-Z(`quest46_q7z_direct_test`) 픽스처.

이 런은 **모형을 검정한다**. 그래서 지킬 것도 그 검정의 성질이다:
  ① w 축 **하나만** 바뀐다(분모·창 공용) — 아니면 「점 vs 창」 비교가 아니다
  ② `w=0` 이 곧 `p_score` — **구성으로** 기준선이다
  ③ 주 통계량은 **차**다 — 비는 분모가 0 근처면 폭발한다
  ④ 예측을 **둘** 병기 — 사전등록(X1 고정 Δ) · 수정(실측 오차·128Hz 층)
  ⑤ 필요표본은 **두 값 병기** — null 기전이 안 갈렸다
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q7z_direct_test.ipynb")

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

    # ① w 축 하나만
    ok("def _win(" in s and "전 w 가 **같은 것**" in s,
       "① 창·분모가 **공용 함수**다 — w 축 하나만 바뀐다")
    ok("def score_w(" in s and "w_ms=0` 이면 **분자가 단일 표본**" in s,
       "① `score_w` 하나가 전 w 를 낸다 — 별도 함수로 갈라놓지 않는다")
    ok("W_MS = (0.0," in s,
       "② ★ 격자가 **w=0 을 포함**한다 — 그게 곧 `p_score` 기준선이다")
    ok("W_KEY" in s and "RATIO_PRED = 1.97" in s,
       "② 예측 기준점과 예측값이 **상수로 사전등록**돼 있다")

    # ③ 주 통계량은 차
    ok("주 통계량은 **차**다" in s and "boot_pair(base, key_, lambda a, b: float(b.mean() - a.mean())" in s,
       "③ ★ 주 통계량이 **짝지은 차**다")
    ok("abs(ea) > 1e-4" in s,
       "③ 비는 분모가 0 근처면 nan 을 낸다 — 폭발을 막는다")
    ok('decide(dlo, dhi, 0.0, ">")' in s,
       "③ 관문 판정이 **차의 CI** 로 이뤄진다")
    ok("비는 분모(w=0 초과)가 0 근처면 폭발한다" in s,
       "③ 이유가 소스에 적혀 있다")

    # ④ 예측 둘 병기 + 128Hz 층
    ok("PRED_128" in s and 'by_fs.get(128' in s.replace('["by_fs"]', 'by_fs'),
       "④ ★ 수정 예측을 **128Hz 층**에서 낸다 — SVDB 가 128Hz 다")
    ok("사전등록 **{RATIO_PRED}**" in s or "사전등록 **" in s,
       "④ 사전등록값과 수정값을 **둘 다** 찍는다")
    ok("LAM_REAL" in s and "실측 검출기 오차 분포" in s,
       "④ ★ λ_w 를 **실측 오차 분포** 하에서 잰다 — X1 은 고정 Δ 였다(검토 지적 ⑤)")

    # ⑤ 필요표본 병기
    ok("need=dict(null_old=(213, 435), null_new=(124, 253))" in s,
       "⑤ ★ 필요표본 **두 값**이 상수로 박혀 있다")
    ok("두 값 병기" in s and "하나만 실으면 그게 사실로 굳는다" in s,
       "⑤ 병기 이유가 소스에 적혀 있다")

    # ⑥ Z2 — null 기전
    ok("REPS = (3, 5, 10, 20, 50)" in s,
       "⑥ `reps` 사다리가 사전등록돼 있다")
    ok("drops" in s and "nan 드롭" in s,
       "⑥ ★ **nan 드롭 수**를 같이 찍는다 — 선택 효과 후보를 가르려고")
    ok("「MC 잡음」설명은 **틀렸다**" in s or "「MC 잡음」설명은 틀렸다" in s,
       "⑥ 틀린 설명을 **소스에 기록**한다(같은 실수 반복 방지)")

    # ⑦ Δ 를 샘플 단위로
    ok("D_SAMP = (0," in s and "Δ 를 **ms 가 아니라 샘플**" in s,
       "⑦ ★ Δ 가 **샘플 단위**다 — 128Hz 라운딩이 λ(11ms)도 오염했다")
    ok("표본율 층" in s or "by_fs" in s,
       "⑦ λ 를 표본율로 **층화**한다")

    # ⑧ 항등 대조
    ok("구성상 항등" in s and "λ(Δ=0 샘플) = 1.000000" in s,
       "⑧ λ(Δ=0) 항등이 **구성으로** 보장되고 로그에 찍힌다(R35 ④)")
    ok("λ(Δ=0) 이 1.0 이 아니다" in s and "raise AssetError" in s,
       "⑧ 항등이 깨지면 **중단**")
    # ⑨ ★★ Z0 은 **숫자 재현이 아니라 구성적 항등**이다
    ok("FIT = FIRE & (pidx0 >= HW)" in s and "구성적 항등 증명" in s,
       "⑨ ★ 창이 **온전히 들어가는** 비트를 따로 뽑아 항등을 증명한다")
    ok("c_fit > c_all" in s,
       "⑨ ★★ 불일치가 **잘린 비트에만** 있다는 것도 같이 요구한다"
       "(온전한 비트 corr > 전체 corr)")
    ok("asset_corr_v1bug" in s and "버그" in s and "앵커" in s,
       "⑨ ★★★ **Q7-V 1판의 0.7122 를 기준으로 쓰지 않는다** — 그 값은 창 중심을 "
       "`np.clip` 으로 옮기던 버그 코드의 출력이다. **버그 있는 코드의 출력에 재현 "
       "기준을 앵커하면 안 된다**")
    ok("Z0 실패" in s and "raise AssetError" in s,
       "⑨ 항등이 안 서면 **중단**한다")

    # ⑩ 결론 검산표
    ok("CHECK = [" in s and "미검정" in s and "틀리면" in s,
       "⑩ ★★ **결론 검산표**가 코드에 있다 — (a)근거 (b)미검정 가정 (c)틀리면(R38 ①)")
    ok("CI 없이 인용 금지" in s,
       "⑩ 점추정을 CI 없이 인용하지 말라고 검산표가 못 박는다")
    ok("5차원 중 1축만" in s,
       "⑩ W1 이 5차원 중 1축만 좋아진다는 한계가 검산표에 있다(검토 지적 ⑧)")

    # ⑪ 성적표 선택 경고
    ok("성적표에서 고른 값이라" in s,
       "⑪ 관측상 최량 w 는 **선택 편의**라고 명시한다(R34 ②)")

    # ⑫ Q7-Y 설계 — 두 팔 · max 위험
    ok("팔 B" in s and "최댓값은 잡음의 최댓값을 고른다" in s,
       "⑫ ★ 잡음 지배면 **max 가 위험**하다고 적고 팔 B(고정 위치)를 병행시킨다")
    ok("위치 정보 자체가 무용지물" in s,
       "⑫ 팔 B ≈ 팔 A 의 함의(분절기 사슬 불필요)가 적혀 있다")

    # ⑭ ★ 네트워크 견고성 — PhysioNet 502 로 런이 죽었다(실측)
    ok("def net(" in s and "NET_TRIES" in s and "NET_BASE ** (i + 1)" in s,
       "⑭ ★ 일시 오류를 **지수 백오프로 재시도**한다")
    ok("if not _is_transient(e) or i == NET_TRIES - 1:" in s,
       "⑭ 영구 오류(404 등)는 **즉시 올린다** — 무한 재시도하지 않는다")
    m3 = re.search(r"def resolve_rid\(.*?\n(?=\n?_res)", s, re.S)
    b3 = m3.group(0) if m3 else ""
    ok(b3 and "if _is_transient(e):" in b3 and "raise" in b3,
       "⑭ ★★ `resolve_rid` 가 일시 오류를 **삼키지 않는다** — 삼키면 "
       "「그 이름이 아니다」로 오해해 **조용한 레코드 손실**이 된다")
    ok("REC_FLOOR" in s and "바닥" in s and "AssetError" in s,
       "⑭ 적재가 바닥 미만이면 **중단** — 코호트가 줄면 λ 를 앞선 런과 못 견준다")
    ok("REC_EXPECT" in s and "코호트가 " in s,
       "⑭ 기대 레코드 수와 다르면 **경고하고 기록**한다")
    ok("skipped=[r for r, _ in SKIP]" in s and "name_fail=" in s,
       "⑭ 못 받은 레코드를 **config 에 남긴다** — 나중에 코호트 차이를 추적할 수 있게")

    # ⑬ 과잉 주장 금지 · 한글 축라벨 금지
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑬ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑬ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 검정이 옳게 움직이는가")
    rng = np.random.RandomState(41)
    fs = 360

    def detrend(v):
        t = np.arange(len(v), dtype=float)
        a, b = np.polyfit(t, v, 1)
        return v - (a * t + b)

    def score_w(x, qs, w_ms, half_ms=100.0):
        W = int(round(half_ms * fs / 1000.0)); h = int(round(w_ms * fs / 1000.0))
        out = []
        for q in qs:
            q = int(q)
            a, b = max(q - W, 0), min(q + W + 1, len(x))
            seg = detrend(x[a:b]); c = q - a
            den = float(np.median(np.abs(seg - np.median(seg)))) + 1e-12
            if h <= 0:
                out.append(abs(seg[c]) / den)
            else:
                u, v = max(c - h, 0), min(c + h + 1, len(seg))
                out.append(float(np.sqrt(np.mean(seg[u:v] ** 2)) / den))
        return np.array(out)

    # ── ⓐ w=0 이 정말 「분자 단일 표본」인가 (구성 확인)
    x = rng.normal(0, 1, 5000)
    q = np.array([2000])
    W = int(round(100.0 * fs / 1000.0))
    seg = detrend(x[2000 - W:2000 + W + 1])
    den = float(np.median(np.abs(seg - np.median(seg)))) + 1e-12
    ok(abs(score_w(x, q, 0.0)[0] - abs(seg[W]) / den) < 1e-9,
       "ⓐ ★ `w=0` 이 **정확히** |단일 표본|/MAD 다 — 구성으로 기준선이다")

    # ── ⓑ 잡음 지배 신호에서 적분이 λ 를 올린다 (X1b 의 재현)
    n_beat, span, c0 = 300, 1500, 700
    sig = rng.normal(0, 0.05, n_beat * span)
    qs = []
    for i in range(n_beat):
        t = np.arange(span) - c0
        amp = 0.15 + rng.normal(0, 0.04)
        sig[i * span:(i + 1) * span] += amp * np.exp(-(t ** 2) / (2 * 28.0 ** 2))
        qs.append(i * span + c0)
    qs = np.array(qs)
    lam = {}
    for w in (0.0, 20.0, 40.0):
        v0 = score_w(sig, qs, w)
        v1 = score_w(sig, qs + 4, w)          # 4 샘플 ≈ 11ms @360Hz
        lam[w] = float(np.corrcoef(v0, v1)[0, 1])
    ok(lam[40.0] > lam[0.0],
       f"ⓑ ★ 잡음 지배 신호에서 적분이 λ 를 올린다 "
       f"(w=0 {lam[0.0]:.4f} → w=40 {lam[40.0]:.4f})")

    # ── ⓒ ★★ **잡음이 없으면** λ 가 안 떨어진다 — 「순수 위치 민감도」 반증
    clean = np.zeros(n_beat * span)
    for i in range(n_beat):
        t = np.arange(span) - c0
        amp = 0.15 + rng.normal(0, 0.04)       # 진폭만 비트마다 다르다
        clean[i * span:(i + 1) * span] += amp * np.exp(-(t ** 2) / (2 * 28.0 ** 2))
    v0 = score_w(clean, qs, 0.0); v1 = score_w(clean, qs + 4, 0.0)
    lam_clean = float(np.corrcoef(v0, v1)[0, 1])
    ok(lam_clean > 0.99,
       f"ⓒ ★★ 잡음이 없으면 점 통계량도 λ≈1 이다({lam_clean:.4f}) — "
       "**순수한 위치 민감도만으로는 λ 가 떨어질 수 없다**(둘은 같은 현상이다)")

    # ── ⓓ 주 통계량으로 차를 쓴 이유 — 비는 분모가 0 근처면 폭발한다
    def boot(a, b, fn, seed, nb=1500):
        r = np.random.RandomState(seed); out = []
        for _ in range(nb):
            j = r.randint(0, len(a), len(a))
            try:
                out.append(float(fn(a[j], b[j])))
            except Exception:
                pass
        out = np.array([o for o in out if np.isfinite(o)])
        return (np.percentile(out, 97.5) - np.percentile(out, 2.5)) / 2 if len(out) > 50 \
            else np.nan
    base = 0.5 + rng.normal(0.002, 0.02, 34)   # 기준 초과가 0 근처
    key = base + rng.normal(0.010, 0.02, 34)
    h_d = boot(base, key, lambda a, b: b.mean() - a.mean(), 7)
    h_r = boot(base, key, lambda a, b: (b.mean() - 0.5) / (a.mean() - 0.5)
               if abs(a.mean() - 0.5) > 1e-4 else np.nan, 7)
    ok(np.isfinite(h_d) and (not np.isfinite(h_r) or h_r > 10 * h_d),
       f"ⓓ ★ 기준 초과가 0 근처면 **비의 CI 가 폭발**한다(차 반폭 {h_d:.4f} vs "
       f"비 반폭 {h_r:.2f}) — 그래서 주 통계량은 차다")

    # ── ⓔ 필요표본 두 값이 실제로 두 배 차이인가 (병기의 근거)
    def need(n, half, eff, p80=False):
        r = n * (half / abs(eff)) ** 2
        return r * 2.04 if p80 else r
    n_old = need(34, 0.0531, 0.5362 - 0.5090) / (34 / 56)
    n_new = need(34, 0.0531, 0.5362 - 0.5005) / (34 / 56)
    ok(200 < n_old < 225 and 115 < n_new < 135,
       f"ⓔ null 을 어느 쪽으로 잡느냐가 필요표본을 **{n_old/n_new:.2f}배** 움직인다 "
       f"(옛 {n_old:.0f} · 새 {n_new:.0f}) — 그래서 병기한다")
    ok(n_old > 126 and n_new < 126,
       "ⓔ ★ 그리고 그 차이가 **「풀 126 으로 도달 가능한가」의 답을 뒤집는다** — "
       "설명 없이 유리한 쪽을 고르면 안 되는 이유")

    # ── ⓗ ★ 두 경계 규약이 **다른 값**을 낸다 — Q7-V 1판이 왜 0.71 이었나
    xx = rng.normal(0, 1, 400)
    W2 = 36
    q_edge = 20                                   # 창 왼쪽이 배열 밖으로 나간다
    #  (a) Q7-P0 규약 — **자르고 중심 유지**
    a_, b_ = max(q_edge - W2, 0), min(q_edge + W2 + 1, len(xx))
    seg_a = detrend(xx[a_:b_]); c_a = q_edge - a_
    v_trunc = abs(seg_a[c_a]) / (float(np.median(np.abs(seg_a - np.median(seg_a)))) + 1e-12)
    #  (b) Q7-V 1판 버그 — **중심을 옮긴다**
    q_sh = int(np.clip(q_edge, W2, len(xx) - W2 - 1))
    seg_b = detrend(xx[q_sh - W2:q_sh + W2 + 1])
    v_clip = abs(seg_b[W2]) / (float(np.median(np.abs(seg_b - np.median(seg_b)))) + 1e-12)
    ok(abs(v_trunc - v_clip) > 1e-6,
       f"ⓗ ★★ 경계에서 **자르기 {v_trunc:.4f} ≠ 중심옮기기 {v_clip:.4f}** — "
       "규약이 다르면 다른 통계량이다. Q7-V 1판의 corr 0.71 은 **옮기기** 값이었다")
    #  창이 온전한 위치에서는 둘이 **같다**
    q_in = 200
    a2, b2 = q_in - W2, q_in + W2 + 1
    seg_c = detrend(xx[a2:b2])
    v_in = abs(seg_c[W2]) / (float(np.median(np.abs(seg_c - np.median(seg_c)))) + 1e-12)
    q_sh2 = int(np.clip(q_in, W2, len(xx) - W2 - 1))
    seg_d = detrend(xx[q_sh2 - W2:q_sh2 + W2 + 1])
    v_in2 = abs(seg_d[W2]) / (float(np.median(np.abs(seg_d - np.median(seg_d)))) + 1e-12)
    ok(abs(v_in - v_in2) < 1e-12,
       "ⓗ ★ 창이 **온전한** 위치에서는 두 규약이 정확히 같다 — "
       "그래서 거기서만 항등을 요구하는 게 옳다")

    # ── ⓖ 일시/영구 오류 분류가 옳은가 (재시도 대상 판별)
    TRANS = ("502", "503", "504", "Bad Gateway", "Service Unavailable",
             "Timeout", "timed out", "Connection", "Temporary")
    def is_trans(msg):
        return any(t in msg for t in TRANS)
    ok(is_trans("NetFileError: 502 Error: Bad Gateway for url: .../21.qrs"),
       "ⓖ ★ 실제로 런을 죽인 **502 Bad Gateway** 를 일시 오류로 분류한다")
    ok(is_trans("NetFileError: 503 Error: Service Unavailable"),
       "ⓖ 503 도 일시 오류다")
    ok(not is_trans("NetFileNotFoundError: 404 Error: Not Found for url: .../1.hea"),
       "ⓖ ★ **404 는 영구 오류**다 — 재시도하면 안 되고, `resolve_rid` 의 "
       "「그 이름이 아니다」 분기가 여기서만 돌아야 한다")
    ok(sum(2.0 ** (i + 1) for i in range(4)) == 30.0,
       "ⓖ 백오프 총 대기 2+4+8+16 = 30초 — 일시 장애를 넘기기에 충분하고 "
       "영구 장애로 런을 오래 붙잡지 않는다")

    # ── ⓕ 128Hz 라운딩이 Δ 를 뭉갠다 (샘플 단위로 바꾼 이유)
    def ms2s(ms, f):
        return int(round(ms * f / 1000.0))
    ok(ms2s(3, 128) == 0,
       "ⓕ 128Hz 에서 Δ=3ms 는 **0 샘플** — 아예 안 움직인다(λ=1 로 부풀린다)")
    ok(ms2s(5, 128) == ms2s(11, 128) == 1,
       "ⓕ ★ 128Hz 에서 Δ=5ms 와 11ms 가 **같은 1샘플**이다 — λ(11ms)도 오염됐다")
    ok(ms2s(11, 360) == 4 and ms2s(11, 360) != ms2s(11, 128),
       "ⓕ 360Hz 에서는 4샘플 — 층을 섞으면 물리적으로 다른 이동을 평균한다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q7-Z 픽스처 — 탈감쇠 직접 검정 · 차 vs 비 · 128Hz 층 · 필요표본 병기")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

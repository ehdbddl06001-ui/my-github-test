#!/usr/bin/env python3
"""Q7-X(`quest46_q7x_diagnostics`) 픽스처.

이 런은 **도구를 잰다**. 그래서 지킬 것도 도구의 성질이다:
  ① λ(Δ=0) 은 **구성상 1.0** — 아니면 점수 계산이 위치에 결정적이지 않다
  ② 두 통계량은 **분자만** 다르다(분모·창 동일) — 아니면 「점 vs 창」 비교가 아니다
  ③ 쌍 내 치환 null 은 **구성상 0.5** — 층 구조를 보존하므로
  ④ X5 두 팔은 **같은 순위상관 감쇠**로 구성 — 아니면 「크기가 같은가」를 못 묻는다
  ⑤ X4 는 **가설 생성**이다 — 이 런에서 부분군을 판정하지 않는다
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q7x_diagnostics.ipynb")

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

    # ① λ(Δ=0) 항등
    ok("LAM[sname][dm].append(1.0)" in s and "구성상 항등" in s,
       "① λ(Δ=0) 을 **구성으로** 1.0 으로 놓는다")
    ok("λ(Δ=0) 이 1.0 이 아니다" in s and "raise AssetError" in s,
       "① 항등이 깨지면 **중단**한다 — 곡선 전체가 무의미해지므로(R35 ④)")
    ok("0.0" in s and "DELTA_MS = (0.0," in s,
       "① Δ 격자가 0 을 포함한다(항등 대조 지점)")

    # ② 두 통계량은 분자만 다르다
    ok("def _win(" in s and "두 통계량이 **같은 창·같은 분모**" in s,
       "② 창·분모를 **공용 함수**로 뽑아 두 통계량이 같은 것을 쓴다")
    ok("def score_point" in s and "def score_energy" in s,
       "② 두 통계량이 정의돼 있다")
    m = re.search(r"def score_energy\(.*?\n(?=\n?def |\n?[A-Z_]+ =)", s, re.S)
    body = m.group(0) if m else ""
    ok(body and "_win(x, q, fs)" in body and "SCORE_HALF_MS" not in body,
       "② ★ `score_energy` 가 **분모를 새로 만들지 않는다** — `_win` 이 준 den 을 그대로 쓴다")
    ok("분자만" in s and "분모·창은" in s,
       "② 「분자만 바꿨다」가 소스에 명시돼 있다")

    # ③ 쌍 내 치환 null
    ok('perm == "stratum"' in s and "for kk in np.unique(key):" in s,
       "③ ★ 치환이 **매칭 층(`key`) 안에서** 이뤄진다 — 레코드 안이 아니다")
    ok("구성상 0.5" in s,
       "③ 쌍 내 치환이 왜 0.5 여야 하는지가 소스에 적혀 있다")
    ok('NUL = {"record": [], "stratum": []}' in s,
       "③ 옛 방식(레코드 안)과 **나란히** 잰다 — 오프셋의 출처를 가르려고")
    ok("추정량에 버그가 있다" in s,
       "③ 0.5 가 아니면 **추정량 버그**로 판정하고 S3 를 다시 본다")
    ok("관문 문턱을 0.5 가 아니라 측정된 null" in s,
       "③ ★ 문턱 교정이 소스에 박혀 있다(0.5 vs null 0.5090 버그)")

    # ④ X5 — 두 팔의 감쇠를 **구성으로** 맞춘다
    ok("rho_det = A_DET / np.sqrt(A_DET ** 2 + E_SD ** 2)" in s,
       "④ 검출기 수송이 남기는 순위상관을 **계산**한다")
    ok("sd_gen = float(np.sqrt(max(1.0 / rho_det ** 2 - 1.0, 1e-9)))" in s,
       "④ ★ 동등분산 잡음의 SD 를 **같은 ρ 가 나오도록 역산**한다(R34 ③)")
    ok("차이가 있다면 그건 크기가 아니라 **구조**" in s,
       "④ 대조의 의미가 소스에 적혀 있다")
    ok("효과의 취약성 측정" in s and "인용하지 않는다" in s,
       "④ 같이 죽이면 **V2 를 인용하지 않는다**고 박혀 있다")

    # ⑤ X4 는 판정하지 않는다
    ok("**판정 아님**" in s and "사전등록" in s,
       "⑤ ★ 부분군을 **탐색적**으로만 찍고 사전등록만 한다(R34 ②)")
    ok("라벨을 보기 전에" in s,
       "⑤ 다음 런의 문턱을 **라벨과 무관하게** 정한다고 박혀 있다")
    ok("표적 모집단을 바꾸지 않는다" in s,
       "⑤ 유의하지 않으면 모집단을 안 바꾼다")

    # ⑥ X0 — 두 보정을 병기하고 고전오차를 검정한다
    ok("√λ" in s and "test-retest" in s,
       "⑥ 나눗셈/√나눗셈 두 해석을 **둘 다** 설명한다")
    ok("upper_sqrt" in s,
       "⑥ ★ X6 에서 **√λ 대안도 같이 찍는다** — 2배짜리 갈림길이므로")
    ok("sigma_ratio" in s and "수축" in s,
       "⑥ 고전오차 가정(σ_obs ≥ σ_true)을 **검정**하고 위배 시 수축이라 적는다")

    # ⑦ 양방향 이동 — 비대칭 파형 왜곡 방지
    ok("for sgn in (+1, -1):" in s and "양방향 평균" in s,
       "⑦ Δ 를 **양방향으로** 흔들어 평균한다 — 한쪽만 보면 비대칭 파형에서 왜곡된다")

    # ⑧ 누수 — X1 은 검출기를 안 쓴다
    m2 = re.search(r"def true_p_positions\(.*?\n(?=\n?def |\n?[A-Z_]+ =|\nT1_)", s, re.S)
    b2 = m2.group(0) if m2 else ""
    ok(b2 and "DET" not in b2 and "detect" not in b2,
       "⑧ ★ X1 은 **정답 위치만** 쓴다 — 검출기와 섞이지 않는 게 요점이다")
    ok("검출기와 무관하다" in s,
       "⑧ 그 사실이 소스에 명시돼 있다")

    # ⑨ 재현 증명
    ok("S3 재현 실패" in s and "20260804T0658" in s or "REF = dict(" in s,
       "⑨ 앞선 공식 실행값을 기준으로 S3 재현을 확인한다")
    ok("나란히 놓을 수 없다" in s,
       "⑨ 재현이 깨지면 진단을 앞선 런과 나란히 놓지 않는다")

    # ⑩ 의사결정 숫자는 S3 가 아니라 W1
    ok("S3 가 아니라 **W1**" in s or "S3(기전)가 아니라" in s,
       "⑩ ★ 딥러닝 판단을 **W1(효용)** 으로 한다고 박혀 있다")
    ok("상한으로만" in s,
       "⑩ 탈감쇠를 **상한**으로만 읽는다(R36 ①)")

    # ⑪ 과잉 주장 금지
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑪ 금지 문구 없음 — 「{bad}」")

    # ⑫ 한글 축라벨 금지
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑫ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 도구가 옳게 움직이는가")
    rng = np.random.RandomState(31)
    fs = 1000

    def detrend(v):
        t = np.arange(len(v), dtype=float)
        a, b = np.polyfit(t, v, 1)
        return v - (a * t + b)

    def win(x, q, half_ms=100.0):
        w = int(round(half_ms * fs / 1000.0))
        a, b = max(q - w, 0), min(q + w + 1, len(x))
        seg = detrend(x[a:b])
        return seg, q - a, float(np.median(np.abs(seg - np.median(seg)))) + 1e-12

    def s_point(x, qs):
        return np.array([(lambda t: abs(t[0][t[1]]) / t[2])(win(x, int(q))) for q in qs])

    def s_energy(x, qs, sig_ms=40.0):
        h = int(round(sig_ms * fs / 1000.0))
        out = []
        for q in qs:
            seg, c, den = win(x, int(q))
            a, b = max(c - h, 0), min(c + h + 1, len(seg))
            out.append(float(np.sqrt(np.mean(seg[a:b] ** 2)) / den))
        return np.array(out)

    # ── ⓐ 합성 P 파 — 점 통계량이 창 통계량보다 **위치에 민감**해야 한다
    n_beat, span = 400, 1200
    x = rng.normal(0, 0.04, n_beat * span)
    qs = []
    for i in range(n_beat):
        c = i * span + 600
        t = np.arange(span) - 600
        amp = 0.18 + rng.normal(0, 0.05)
        x[i * span:(i + 1) * span] += amp * np.exp(-(t ** 2) / (2 * 30.0 ** 2))
        qs.append(c)
    qs = np.array(qs)
    lam = {}
    for nm, fn in (("point", s_point), ("energy", s_energy)):
        v0 = fn(x, qs)
        row = {}
        for d in (0, 11, 30):
            if d == 0:
                row[d] = 1.0; continue
            cs = [float(np.corrcoef(v0, fn(x, qs + sg * d))[0, 1]) for sg in (1, -1)]
            row[d] = float(np.mean(cs))
        lam[nm] = row
    ok(lam["point"][0] == 1.0 and lam["energy"][0] == 1.0,
       "ⓐ Δ=0 에서 두 통계량 모두 **정확히 1.0**(항등)")
    ok(lam["energy"][11] > lam["point"][11],
       f"ⓐ ★ Δ=11ms 에서 **적분이 점보다 강건**하다 "
       f"(energy {lam['energy'][11]:.4f} > point {lam['point'][11]:.4f})")
    ok(lam["point"][30] < lam["point"][11],
       f"ⓐ λ 가 Δ 에 대해 **단조 감소**한다 "
       f"({lam['point'][11]:.4f} → {lam['point'][30]:.4f})")

    # ── ⓑ 모양 분류 규칙이 세 경우를 옳게 가르는가
    def shape(l3, l11, hi=0.85):
        if l11 >= hi:
            return "위치 무관"
        return "지터 한계" if l3 >= hi else "SNR 한계"
    ok(shape(0.99, 0.95) == "위치 무관", "ⓑ 둘 다 높으면 **위치 무관**")
    ok(shape(0.90, 0.29) == "지터 한계", "ⓑ 작은 Δ 만 높으면 **지터 한계**")
    ok(shape(0.30, 0.25) == "SNR 한계", "ⓑ 작은 Δ 도 낮으면 **SNR 한계**")

    # ── ⓒ 쌍 내 치환 null 은 **기대값이 정확히 0.5**
    N = 6000
    key = rng.randint(0, 40, N)
    tt = rng.rand(N) < 0.28
    v = rng.normal(0, 1, N) + np.where(tt, 0.5, 0.0)      # 진짜 신호가 있어도

    def matched(vv, tta):
        win_ = tie = tot = 0.0
        for kk in np.unique(key):
            m = np.where(key == kk)[0]
            a = vv[m[tta[m]]]; b = vv[m[~tta[m]]]
            if not len(a) or not len(b):
                continue
            d = a[:, None] - b[None, :]
            win_ += float((d > 0).sum()); tie += float((d == 0).sum()); tot += float(d.size)
        return (win_ + 0.5 * tie) / tot
    obs = matched(v, tt)
    nul = []
    for s_ in range(40):
        r = np.random.RandomState(100 + s_)
        t2 = tt.copy()
        for kk in np.unique(key):
            m = np.where(key == kk)[0]
            t2[m] = t2[m][r.permutation(len(m))]
        nul.append(matched(v, t2))
    ok(obs > 0.6, f"ⓒ 진짜 신호는 매칭에서 살아남는다({obs:.4f})")
    ok(abs(np.mean(nul) - 0.5) < 0.01,
       f"ⓒ ★ **쌍 내 치환 null 이 0.5 다**({np.mean(nul):.4f}) — 층 구조를 보존하므로")

    # ── ⓓ 쌍 내 치환의 **핵심 성질**: 층이 극단적으로 불균형하고 값이 층과 상관돼도
    #    여전히 0.5 다. 이게 「측정된 null 을 문턱으로 쓸 수 있다」의 근거다.
    #    ⚠️ 우리는 Q7-S′ 의 0.5090 오프셋이 **어디서 왔는지 모른다** — 그걸 알아내는 게
    #       X3 의 목적이다. 여기서 기전을 안다고 가장하지 않는다.
    key2 = np.repeat(np.arange(40), N // 40)
    tt2 = np.zeros(N, bool)
    for kk in range(40):
        m = np.where(key2 == kk)[0]
        tt2[m[:max(1, int(len(m) * (0.02 + 0.9 * kk / 40)))]] = True   # 층마다 2%~92%
    v2 = rng.normal(0, 1, N) + key2 * 0.20                             # 값이 층과 강하게 상관
    key = key2
    strat = []
    for s_ in range(60):
        r = np.random.RandomState(300 + s_)
        t3 = tt2.copy()
        for kk in np.unique(key2):
            m = np.where(key2 == kk)[0]
            t3[m] = t3[m][r.permutation(len(m))]
        strat.append(matched(v2, t3))
    ok(abs(np.mean(strat) - 0.5) < 0.005,
       f"ⓓ ★ 층 비율 2~92% · 값이 층과 강상관인데도 쌍 내 치환 null 이 **0.5** "
       f"({np.mean(strat):.4f}) — 그래서 이걸 **문턱으로 쓸 수 있다**")

    # ── ⓓ2 동점 처리에 편의가 없는가 (0.5090 의 후보 하나를 배제한다)
    vt = np.round(rng.normal(0, 1, N) * 2) / 2.0          # 동점이 많은 값
    tie_null = []
    for s_ in range(40):
        r = np.random.RandomState(400 + s_)
        t4 = tt2.copy()
        for kk in np.unique(key2):
            m = np.where(key2 == kk)[0]
            t4[m] = t4[m][r.permutation(len(m))]
        tie_null.append(matched(vt, t4))
    ok(abs(np.mean(tie_null) - 0.5) < 0.005,
       f"ⓓ2 동점이 많아도 null 이 0.5 다({np.mean(tie_null):.4f}) — "
       "`tie×0.5` 처리에 편의가 없다(0.5090 의 후보 하나 배제)")

    # ── ⓔ X5 — 두 팔의 순위상관 감쇠를 같게 만드는 역산이 맞는가
    a_det, e_sd = 0.2419, 0.9322
    rho = a_det / np.sqrt(a_det ** 2 + e_sd ** 2)
    sd_gen = np.sqrt(1.0 / rho ** 2 - 1.0)
    rho_gen = 1.0 / np.sqrt(1.0 + sd_gen ** 2)
    ok(abs(rho - rho_gen) < 1e-9,
       f"ⓔ ★ 역산이 정확하다 — 검출기 ρ {rho:.6f} = 무작위 ρ {rho_gen:.6f}")
    z = rng.normal(0, 1, 200000)
    z_det = a_det * z + rng.normal(0, e_sd, 200000)
    z_gen = z + rng.normal(0, sd_gen, 200000)
    r1 = float(np.corrcoef(z, z_det)[0, 1]); r2 = float(np.corrcoef(z, z_gen)[0, 1])
    ok(abs(r1 - r2) < 0.01,
       f"ⓔ 실측으로도 같다 — 검출기 {r1:.4f} vs 무작위 {r2:.4f} "
       "(차이가 있다면 크기가 아니라 **구조**다)")

    # ── ⓕ 고전오차 검정 방향 — 가법이면 σ_obs ≥ σ_true, 수축이면 <
    t_ = rng.normal(0, 1, 50000)
    ok(np.std(t_ + rng.normal(0, .5, 50000)) > np.std(t_),
       "ⓕ 가법 잡음이면 σ_obs > σ_true — 고전 보정(÷λ)이 맞는 영역")
    ok(np.std(0.5 * t_ + rng.normal(0, .05, 50000)) < np.std(t_),
       "ⓕ 수축이면 σ_obs < σ_true — 그때는 고전 보정을 그대로 쓰면 안 된다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q7-X 픽스처 — λ(Δ) 항등 · 점 vs 창 · 쌍 내 치환 null · 동등감쇠 대조")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

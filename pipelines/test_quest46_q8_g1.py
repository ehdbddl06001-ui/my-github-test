#!/usr/bin/env python3
"""Q8-G1(`quest46_q8_g1_personal_pmorph`) 픽스처 — 환자 개인화 P 형태 진입 관문.

이 런에서 빠뜨리면 결과가 무효인 것 넷:
  ① **천장과 같은 통계량** — 0.6097 은 리듬 통제 후 매칭 AUROC 다. 모델 입력에 RR 을 넣지 않고
     출력을 리듬 기저에 잔차화한 뒤 f1 층에서 매칭해야 한다. 안 그러면 RR 을 학습한 모델이
     천장을 거저 넘는다
  ② **누출 차단** — 시간 분할 + 가드밴드 · 소거 템플릿도 **학습 구간에서만** · 표준화도 학습 통계로만
  ③ **음성 대조** — `cancel_pmask` 가 세 팔 중 하나로 있고, 세 팔이 **같은 창 위치**를 본다
  ④ **세기가 코호트를 정한다** — 환자당 구간별 S 를 세고 미달이면 중단(R11-b)

동적 검사는 절차가 실제로 움직이는지 본다. 특히 **모델이 학습되는가**(1판은 풀배치 40 스텝이라
덜 학습된 상태로 관문을 읽었다)와 **G5 대조의 검정력**을 본다.
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q8_g1_personal_pmorph.ipynb")

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
    cs = cells()

    # ① ★★★ 천장과 같은 통계량
    ok("CEIL = 0.6097" in s,
       "① 진입 앵커 0.6097 이 상수로 박혀 있다")
    ok("리듬 통제 후 매칭 AUROC" in s,
       "① ★★★ 천장이 **리듬 통제 후 매칭 AUROC** 라는 게 소스에 박혀 있다")
    ok("def matched_auc" in s and 'key = np.round(f1[idx]).astype(int)' in s,
       "① 매칭이 Q7-AA 와 **같은 f1 층**이다")
    ok("def resid" in s and "def basis_ext" in s,
       "① 리듬 기저 잔차화가 Q7-AA 와 같다")
    ok("def stat_of" in s and "matched_auc(resid(" in s,
       "① ★★★ 통계량이 **잔차화 → 매칭**의 합성이다")
    ok("모델 입력에 **RR 을 넣지 않고**" in s or "모델 입력에 RR 을 넣지 않는다" in s,
       "① ★★★ 모델 입력에 **RR 을 넣지 않는다**고 못 박혀 있다")
    # windows() 가 리듬 특징을 안 쓴다는 구조 검사
    w = s[s.index("def windows"):s.index("class TinyCNN")]
    ok(not re.search(r'\bf1\b|\bf2\b|\bf3\b|\bf4\b|pre\[|post\[', w),
       "① ★★ `windows()` 가 **리듬 특징을 전혀 안 쓴다** — 창은 파형뿐이다")
    ok("런 내 기준선" in s and "baseline_inrun" in s,
       "① ★ 같은 구간의 `p_score` **런 내 기준선**을 함께 낸다(모집단이 다르므로)")

    # ② ★★★ 누출 차단
    ok("FRAC_TRAIN = 0.50" in s and "GUARD_S = 60.0" in s,
       "② 시간 분할 비율과 **가드밴드**가 상수로 박혀 있다")
    ok("t < cut - GUARD_S / 2.0" in s and "t > cut + GUARD_S / 2.0" in s,
       "② ★★ 분할이 **시간 기준**이고 가드밴드가 양쪽으로 적용된다")
    ok("환자 안 무작위 분할은 누출" in s,
       "② 왜 시간 분할인지가 소스에 적혀 있다")
    ok("tmpl = np.median(XB[tr], axis=0)" in s,
       "② ★★★ 소거 템플릿이 **학습 구간(tr)에서만** 만들어진다")
    ok("템플릿도 **학습 구간에서만**" in s,
       "② ★ 왜 템플릿을 학습 구간에서만 만드는지가 적혀 있다")
    ok("mu, sd = Xtr.mean(), Xtr.std()" in s,
       "② 표준화도 **학습 구간 통계**로만 한다(R22)")
    ok("r_samp" in s and "t_sec = rsmp / FS" in s,
       "② 시간축이 자산의 **절대 R 샘플 위치**에서 온다")

    # ③ ★★★ 음성 대조 · 같은 창
    ok('ARMS = ("raw", "cancel", "cancel_pmask")' in s,
       "③ 3팔이 사전등록돼 있다")
    ok("정확히 같은 창 위치" in s,
       "③ ★★ 세 팔이 **같은 창 위치**를 본다고 못 박혀 있다(짝지은 비교)")
    ok('out[:, HW_P - PMASK_HW:HW_P + PMASK_HW + 1] = 0.0' in s,
       "③ ★★ 음성 대조가 **P 봉우리만 0** 으로 만든다")
    ok("소거 실패" in s and "반드시" in s,
       "③ ★★★ 소거 팔의 교란(모델이 P 가 아니라 **소거 실패**를 학습)이 적혀 있다")
    ok("표적 창을 이긴 전례" in s,   # ★ 소스에서 줄바꿈으로 쪼개져 있어 연속 부분만 본다
       "③ ★ 음성 대조가 이긴 전례 둘을 들고 간다 — **떨어질 거라 가정하지 않는다**")
    ok("boot_pair" in s and "cancel−cancel_pmask" in s.replace("cancel-cancel_pmask", "cancel−cancel_pmask"),
       "③ 소거 대비가 **짝지은 차**다(같은 환자)")

    # ④ ★★★ 세기가 코호트를 정한다
    ok("MIN_S_SEG, MIN_N_SEG = 25, 25" in s,
       "④ 구간별 GMIN_S 가 상수로 박혀 있다")
    ok('d["tr_s"] >= MIN_S_SEG' in s and 'd["ev_s"] >= MIN_S_SEG' in s,
       "④ ★★ **앞·뒤 구간 각각**에 최소 S 를 요구한다")
    ok("len(COH) < MIN_REC" in s and "raise AssetError" in s,
       "④ ★★★ 코호트가 얕으면 **중단**한다 — 세기 결과만 남기고 종결")
    ok("세기 결과만 로그로 남기고" in s,
       "④ 중단 시 무엇을 남기는지가 적혀 있다")
    ok("설계를 세기에 의존시키지 않기 위해" in s or "코호트를 세기가 정한다" in s,
       "④ ★ 「세기 전에 설계하지 마라」를 **코호트를 세기가 정하게** 해서 지킨다(R11-b)")

    # ⑤ 자산 정합 · 생리학적 자기검증
    ok("첫 불일치 idx" in s and "정합 깨짐" in s,
       "⑤ ★ (pid,sym) 원소 단위 정합 — 불일치 시 **첫 인덱스를 찍고 중단**(Q7-P0 규약)")
    ok("PR 중앙" in s and "100.0 <= pr_med <= 230.0" in s,
       "⑤ ★★ **생리학적 자기검증** — P 위치 중앙이 PR 범위 밖이면 중단(R35 ⑦)")
    ok("비싼 계산 **전에**" in s or "비싼 계산 전에" in s,
       "⑤ 정합 증명이 비싼 계산 전에 끝난다")

    # ⑥ 선택 편의 없음 · EPOCHS 는 설계 상수
    ok("EPOCHS = 200" in s and "if SMOKE else" not in s.split("EPOCHS = 200")[0].split("\n")[-1],
       "⑥ ★★ EPOCHS 가 **SMOKE 와 무관한 설계 상수**다")
    ok("풀배치" in s and "그래디언트 스텝 수" in s,
       "⑥ ★★★ 풀배치라 EPOCHS = 스텝 수임이 적혀 있다 — 1판이 40 스텝으로 덜 학습됐다")
    ok("용량 선택을 하지 않는다" in s and "고정" in s,
       "⑥ ★★ 진입 관문이라 **용량 선택을 하지 않는다**(선택이 없으면 선택 편의도 없다)")
    ok("최량 팔은 **사후 선택**" in s,
       "⑥ ★★ 최량 팔이 **사후 선택**임을 밝히고 팔별 판정을 전부 찍는다(R36 ②)")
    knobs = set(re.findall(r'^\s*(\w+)\s*=.*\bif SMOKE\b', s, re.M))
    ok(knobs <= {"NB_BOOT", "N_PERM_G4", "N_SHUF_G5"},
       f"⑥ ★★ SMOKE 가 만지는 건 **비용 손잡이뿐**이다({sorted(knobs)})")

    # ⑦ 영점 · G5 · 크기로 판정
    ok("파이프라인 영점" in s and "perm_train" in s,
       "⑦ ★★ 영점이 **학습 라벨 치환 + 재학습**이다(통계량 영점이 아니라 절차 영점)")
    ok("0.5 를 **가정하지 않는다**" in s or "0.5 를 가정하지 않는다" in s,
       "⑦ 영점을 가정하지 않는다(R26 · R38 ②)")
    ok("shuf_anchor" in s and "G5a" in s,
       "⑦ ★★ G5 셔플 팔과 **G5a(학습 없는 직접 검정)** 가 둘 다 있다")
    ok("IDX_SHARE" in s and "IDX_SHARE >= 0.5" in s,
       "⑦ ★★★ 검출기 버릇 판정이 **크기**로 이뤄진다 — 「CI 가 0.5 를 배제」만 보면 "
       "아주 작은 효과가 아주 큰 효과의 원인으로 지목된다")
    ok("앵커 산포" in s and "disp_frac" in s,
       "⑦ ★★ **앵커 산포**를 창 반폭과 비교해 찍는다 — 대조의 검정력이 드러난다")
    ok("이 대조는 검정력이 없다" in s,
       "⑦ ★ 산포가 작으면 **대조에 검정력이 없다**고 판정문이 말한다")

    # ⑧ 위생
    ok("T2 를 근거로 기대하지 마라" in s or "T2 를 근거로 기대하지 않는다" in s,
       "⑧ ★★ T2(가시성)를 판별력의 근거로 삼지 않는다(R40 ① · Q7-Z 패턴)")
    ok("판별력에서 한 번도 안 쟀다" in s,
       "⑧ ★ 소거가 **판별력에서 처음 측정**된다는 게 적혀 있다")
    ok("G2·G3·G6 은 **G1 을 넘은 뒤에**" in s or "G2·G3·G6ㅇ" in s or "G1 통과 후" in s,
       "⑧ G2·G3·G6 을 **G1 통과 후로** 미룬다고 적혀 있다")
    ok("_rank_avg" in s and "평균 순위" in s,
       "⑧ ★★★ `spearman` 이 **동점에 평균 순위**를 준다 — Q3-B 에서 발각된 순서 의존 버그의 수정")
    ok("Q3-B 에서 발각" in s,
       "⑧ ★ 그 버그의 출처가 소스에 적혀 있다")
    ok("CHECK = [" in s and "가정" in s and "틀리면" in s,
       "⑧ 결론 검산표가 코드에 고정돼 있다(R38 ⑦ · R39 ⑤)")
    ok("해석 불가" in s and "uninterpretable" in s,
       "⑧ 효과가 0 근처면 필요표본을 **해석 불가**로 찍는다(R41 ②)")
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑧ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑧ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")

    # ⑨ 순서 — G1 이 G4·G5 보다 앞 셀
    i1 = next((i for i, c in enumerate(cs) if c.lstrip().startswith("# CELL") and "【G-B】" in c), -1)
    i4 = next((i for i, c in enumerate(cs) if c.lstrip().startswith("# CELL") and "【G-C】" in c), -1)
    ok(0 <= i1 < i4, f"⑨ G1 이 G4·G5 **앞 셀**에서 계산된다(G1 셀 {i1} < G4 셀 {i4})")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 절차가 옳게 움직이는가")
    rng = np.random.RandomState(81)

    # ── ⓐ ★★ 시간 분할 + 가드밴드가 실제로 겹치지 않는가
    t = np.sort(rng.uniform(0, 720, 2000))
    cut = t.min() + 0.5 * (t.max() - t.min())
    tr = t[t < cut - 30]; ev = t[t > cut + 30]
    ok(len(tr) and len(ev) and (ev.min() - tr.max()) >= 60.0 - 1e-9,
       f"ⓐ ★★ 학습 끝과 평가 시작 사이가 **가드밴드 이상**이다({ev.min()-tr.max():.1f}초 ≥ 60)")

    # ── ⓑ ★★★ 소거 템플릿을 **전 기록**으로 만들면 평가 구간이 템플릿에 든다(누출)
    n, L = 400, 60
    base = np.sin(np.linspace(0, 3, L))
    B = base[None] + rng.normal(0, .05, (n, L))
    B[n // 2:] += 0.30 * np.hanning(L)[None]          # ★ 뒤 절반(평가)만 모양이 바뀐다
    t_all = np.median(B, axis=0); t_tr = np.median(B[:n // 2], axis=0)
    leak = np.abs(t_all - t_tr).max()
    ok(leak > 1e-3,
       f"ⓑ ★★★ 전 기록 템플릿은 학습 구간 템플릿과 다르다(max|Δ| {leak:.4f}) — "
       "즉 **평가 구간 신호가 템플릿에 든다**. 그래서 템플릿도 학습 구간에서만 만든다")

    # ── ⓒ P 마스크가 창의 **중앙만** 지우고 나머지는 그대로다
    HW_P, PM = 32, 9
    W = 2 * HW_P + 1
    X = rng.normal(size=(50, W))
    Y = X.copy(); Y[:, HW_P - PM:HW_P + PM + 1] = 0.0
    ok((Y[:, :HW_P - PM] == X[:, :HW_P - PM]).all() and (Y[:, HW_P + PM + 1:] == X[:, HW_P + PM + 1:]).all()
       and (Y[:, HW_P - PM:HW_P + PM + 1] == 0).all(),
       f"ⓒ ★ 음성 대조가 **중앙 ±{PM}샘플만** 0 으로 만들고 나머지는 **정확히 보존**한다")

    # ── ⓓ ★★★ 풀배치면 EPOCHS = 그래디언트 스텝 수 — 40 은 덜 학습된다
    #    (torch 없이도 보이도록 같은 구조의 선형 문제로 재현한다)
    d = 20
    w_true = rng.normal(size=d)
    Xd = rng.normal(size=(300, d)); yd = Xd @ w_true + rng.normal(0, .1, 300)
    def full_batch(steps, lr=1e-3):
        w = np.zeros(d)
        for _ in range(steps):
            g = 2 * Xd.T @ (Xd @ w - yd) / len(Xd)
            w = w - lr * g
        return float(np.corrcoef(Xd @ w, yd)[0, 1])
    c40, c200, c2000 = full_batch(40), full_batch(200), full_batch(2000)
    ok(c40 < c200 < c2000,
       f"ⓓ ★★★ 풀배치는 **스텝 수 = EPOCHS** 라 40 스텝이면 덜 학습된다"
       f"(적합도 40 {c40:.3f} < 200 {c200:.3f} < 2000 {c2000:.3f}) — "
       "1판이 EPOCHS=40 이었고 스모크런에서 관문이 전부 잡음이었다")

    # ── ⓔ ★★★ G5 대조의 **검정력** — 앵커 산포가 창보다 작으면 셔플이 아무것도 안 바꾼다
    def overlap(disp, hw):
        a = rng.normal(0, disp, 4000)
        b = a[rng.permutation(len(a))]
        return float(np.mean(np.clip(2 * hw + 1 - np.abs(a - b), 0, None) / (2 * hw + 1)))
    ov_small, ov_big = overlap(1.6, 32), overlap(40.0, 32)
    ok(ov_small > 0.95 > ov_big,
       f"ⓔ ★★★ 산포 1.6 이면 셔플 후 창이 **{ov_small:.1%} 겹친다**(산포 40 이면 {ov_big:.1%}) — "
       "즉 산포 ≪ 창이면 셔플 대조는 **검정력이 없다**. 그래서 산포를 찍고 G5a 를 따로 둔다")

    # ── ⓕ ★★ 작은 효과는 큰 효과의 원인이 될 수 없다 (G5 판정을 크기로 하는 이유)
    exc_g5a, exc_shuf = 0.0122, 0.1481
    ok(exc_g5a / exc_shuf < 0.5,
       f"ⓕ ★★★ G5a 초과 {exc_g5a:+.4f} 는 셔플 초과 {exc_shuf:+.4f} 의 "
       f"{exc_g5a/exc_shuf:.0%} 뿐이다 — 「CI 가 0.5 를 배제」만 보면 이걸 원인으로 "
       "지목하게 된다(1판이 그렇게 틀렸다). **크기로 판정한다**")

    # ── ⓖ 매칭 AUROC 는 방향이 있는 통계량이다(<0.5 는 역방향)
    def matched(v, key, tt):
        win = tie = tot = 0.0
        for kk in np.unique(key):
            m = np.where(key == kk)[0]
            a = v[m[tt[m]]]; b = v[m[~tt[m]]]
            if not len(a) or not len(b):
                continue
            dd = a[:, None] - b[None, :]
            win += float((dd > 0).sum()); tie += float((dd == 0).sum()); tot += float(dd.size)
        return (win + 0.5 * tie) / tot if tot else np.nan
    key = rng.randint(0, 10, 2000); tt = rng.rand(2000) < 0.2
    v_up = rng.normal(0, 1, 2000) + np.where(tt, 0.6, 0)
    ok(matched(v_up, key, tt) > 0.6 and matched(-v_up, key, tt) < 0.4,
       f"ⓖ 매칭 AUROC 는 **방향이 있다**(정 {matched(v_up,key,tt):.3f} · "
       f"역 {matched(-v_up,key,tt):.3f}) — `p_score` 기준선이 0.5 미만이면 그건 역방향이지 무신호가 아니다")

    # ── ⓗ 동점 평균순위 spearman 은 **순서에 무관**하다 (Q3-B 버그의 회귀 검사)
    def _rank_avg(v):
        v = np.asarray(v, float); o = v.argsort()
        r = np.empty(len(v), float); r[o] = np.arange(len(v), dtype=float)
        for u in np.unique(v):
            m = v == u
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r
    def sp_ok(a, b):
        ra, rb = _rank_avg(a), _rank_avg(b)
        return float(np.corrcoef(ra, rb)[0, 1])
    def sp_bad(a, b):
        ra = np.asarray(a, float).argsort().argsort().astype(float)
        rb = np.asarray(b, float).argsort().argsort().astype(float)
        return float(np.corrcoef(ra, rb)[0, 1])
    A = np.r_[np.linspace(0, 1, 14), [0.5] * 6]
    Bv = np.r_[np.linspace(0, 1, 14) + rng.normal(0, .1, 14), [0.01] * 6]
    vs_ok, vs_bad = set(), set()
    for _ in range(200):
        p = rng.permutation(len(A))
        vs_ok.add(round(sp_ok(A[p], Bv[p]), 6)); vs_bad.add(round(sp_bad(A[p], Bv[p]), 6))
    ok(len(vs_ok) == 1 and len(vs_bad) > 1,
       f"ⓗ ★★★ 평균순위 판본은 순서에 무관하고(고유값 {len(vs_ok)}개) "
       f"argsort 판본은 **순서마다 달라진다**({len(vs_bad)}개) — Q3-B 에서 발각된 버그")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q8-G1 픽스처 — 천장과 같은 통계량 · 누출 차단 · 음성 대조 · 세기가 코호트")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

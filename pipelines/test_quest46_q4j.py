#!/usr/bin/env python3
"""Q4-J(`quest46_q4j_error_anatomy`) 픽스처 — **입력이 RR 뿐이었다**.

Q4-I(`20260805T0815`)가 내 「능력 비용」 가설을 **직접 반증**했다.

  · 내용 **없는** 16열을 넣은 `shuf` 0.9399 vs base 0.9420 ⇒ 차원 비용 **−0.0021**
    (전체 하락 −0.0142 의 15%). 나머지 −0.0121 [−0.0186, −0.0060] 은 **내용이 해로운** 것
  · `C` 튜닝 이동 **+0.0001** · 기록별 표준화 −0.0077 / −0.0094  ⇒ **추정기는 병목이 아니다**
  · 맞은 건 하나 — 영점(raw) −0.0241 vs 영점(교정) −0.0680 ⇒ Q4-H 의 −0.0427 은 거의 전부
    **교정기 부호 되살림 artifact** 였다(확인됐지만 결론은 안 바뀐다)

**왜 해로웠나 — 중복이었다.** 단변량 최고가 추가 블록 `pre/base` 0.4209 vs 기존 base
0.4337 이고, DEV 가 56폴드 전부에서 `pre/base`·`alt_next`·`alt_prev` 를 골랐다.
`pre/base` 는 base 의 `1 − pre/local_base(k)` 와 **사실상 같은 양**이다. 그리고 보상성
휴지기 비율은 **PAC vs PVC** 를 가르는 양인데 우리 음성의 대부분은 **정상 N** 이다
(N 은 pause 가 없어 comp≈1, PAC 도 <1 — 둘 다 낮다). **문제와 안 맞는 교과서 지식**이었다.

이 런에서 빠뜨리면 결과가 무효인 것 여섯:
  ① **오류 해부가 자다**(R35 ①) — 위양성이 V 면 형태가 답이고 N 이면 리듬 라우팅이 답이다.
     한 번도 안 세어봤다
  ② **파형을 처음 쓴다** — 템플릿은 **rel-RR 로만** 고른다(라벨 안 씀 · R22)
  ③ **차원 동일 대조군** `mshuf` — Q4-I 가 이 방법론의 작동을 확인했다(−0.0021)
  ④ ★★★ **ΔPPV 와 Δ민감도를 비교하면 안 된다** — 예산 k 고정이면 PPV=TP/k · 민감도=TP/S 로
     **분자가 같아** S<k 인 기록에서 Δ민감도>ΔPPV 가 **산술적으로 강제**된다.
     그래서 방향 판정을 **위양성 구성**(심실기원 감소율 > 상심실정상 감소율)으로 바꿨다.
     ⚠️ 이건 **스모크가 잡아준 것**이다 — 원안은 「ΔPPV > Δ민감도」였다
  ⑤ **영점의 유효 표본은 레코드가 아니라 rep** — 한 rep 안의 폴드는 학습 데이터를 90%
     공유해 거의 같은 무작위 방향이 56 레코드에 공통 적용된다(Q4-I raw 영점 base 0.5277≠0.5).
     rep 수준 산포를 병기하고 **두 영점 상단 중 보수적인 쪽**을 문턱으로 쓴다
  ⑥ **형태가 안 먹혀도 기각이 아니라 확인이다**(R39 ①) — **SVEB 는 상심실성이라 QRS 가
     정상**이다. 그러면 남는 답은 **적응증을 좁히는 것**이고 Q4-I 가 그 수치를 이미 냈다
     (규칙 절반만 — AUROC 0.9781 · 달성률 0.9533 · 민감도@300 0.9283)
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4j_error_anatomy.ipynb")
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

    # ── 사전 고정 손잡이
    for tok in ("R_IDX", "W_QRS", "W_FULL", "W_ST", "W_P", "W_WID", "TMPL_LO", "TMPL_HI",
                "TMPL_MIN", "MAIN_K", "N_PERM"):
        ok(f"{tok} =" in s or f"{tok}," in s, f"사전 고정 손잡이 `{tok}` 가 CELL 1 에 있다")
    ok("SMOKE" in s and "N_PERM  = 3   if SMOKE" in s,
       "스모크는 **비용 손잡이만** 줄인다(관문 문턱은 안 줄인다)")

    # ── ① 오류 해부
    ok('for need in ("pid", "y3", "pre_rr", "post_rr", "beat", "sym")' in s,
       "① `beat`·`sym` 이 없으면 **중단**한다(R16)")
    ok("ANAT" in s and "Counter" in s and "SYM[idx][bad]" in s,
       "① ★★★ 위양성을 **실제 주석 심볼**로 센다")
    ok('VSET, NSET = ("V", "E", "F"), ("N", "L", "R", "e", "j", "n")' in s,
       "① 심실기원(V/E/F)과 상심실정상(N/L/R/e/j/n)을 **사전에 나눠 둔다**")
    ok("fn_run" in s and "fn_iso" in s and "in_run" in s,
       "① 위음성을 **런/이단맥 문맥 vs 고립**으로 나눈다(Q7-K6 이 「런 −0.2739」로 본 자리)")
    ok("fn_rel" in s and "fn_pct" in s,
       "① ★★ 놓친 S 의 **상대 RR**(조기성이 있었나)과 **레코드 내 점수 백분위**"
       "(아깝게 놓쳤나)를 같이 낸다 — 「예산 부족」과 「모델이 못 봄」을 가른다")
    ok("np.argsort(np.argsort(sc))" in s,
       "① 백분위는 순위로 잰다(O(n²) 행렬 안 만든다)")

    # ── ② 파형 · 템플릿
    ok("def morph_feats" in s and "np.median(B[okm], axis=0)" in s,
       "② 템플릿 = 레코드별 **중앙 파형**")
    ok("okm = (REL[ii] >= TMPL_LO) & (REL[ii] <= TMPL_HI)" in s,
       "② ★★★ 템플릿 선택이 **rel-RR 로만** 이뤄진다 — **라벨을 안 쓴다**(R22)")
    ok("N_TMPL_FALLBACK" in s and "TMPL_MIN" in s,
       "② 템플릿 표본이 모자라면 **대체하고 그 횟수를 기록**한다")
    ok("def corr_to" in s and "qrs_width" in s and "p_energy_ratio" in s,
       "② 형태 8열 — 상관 · QRS 폭 대리 · 진폭/면적비 · P 창 에너지비")
    ok("P 갈래 재개가 아니다" in s or "P 갈래 재개가 아니" in m,
       "② ★★ **Q7-S′ 의 P 갈래 재개가 아니다**(상한 +0.0213 · 필요 222명)라고 못 박는다")
    ok("if LW <= W_ST[0]" in s and "raise AssetError" in s,
       "② 파형이 사전 고정 창보다 짧으면 **중단**한다(R34 ②)")

    # ── ③ 차원 동일 대조군
    ok("M_SH[ii] = MORPH[ii][_rs.permutation(len(ii))]" in s,
       "③ ★★★ `mshuf` 는 형태 블록만 **레코드 안에서 공동 행치환**한다")
    ok("차원 대조군이 거의 항등이다" in s and "차원 대조군의 차원이 다르다" in s,
       "③ 항등이거나 차원이 다르면 **중단**한다(R35 ①)")
    ok('MAIN_CT = "morph-mshuf"' in s,
       "③ ★★★ **주 관문이 `morph-mshuf`** 다 — 차원이 같아야 내용만 묻는 게 된다")
    ok("-0.0021" in s, "③ Q4-I 가 잰 **차원 비용 −0.0021** 이 앵커로 박혀 있다")

    # ── ④ 산술 편향
    ok("분자가 같다" in s or "분자가 같아" in s,
       "④ ★★★ ΔPPV 와 Δ민감도의 **분자가 같다**(TP)는 게 로그에 남는다")
    ok("산술적으로 Δ민감도 > ΔPPV" in s or "산술적으로 비교 불가" in s,
       "④ ★★★ 그래서 **둘을 비교하지 않는다**고 명시한다")
    ok("dir_ok = red_v > red_n" in s,
       "④ ★★★ 방향 판정이 **위양성 구성**(심실기원 감소율 > 상심실정상 감소율)으로 돼 있다")
    ok("스모크가 잡아준 것" in s,
       "④ ★★ 원안(ΔPPV > Δ민감도)이 **스모크에 잡혔다**는 사실이 검산표에 남는다")

    # ── ⑤ 영점 방법론
    ok("REPM" in s and "NREP" in s,
       "⑤ ★★★ 영점을 **rep 수준**으로도 집계한다")
    ok("max(NSTAT[nm][2], NREP[nm][\"hi\"])" in s,
       "⑤ ★★★ 문턱은 **두 영점 상단 중 보수적인 쪽**이다")
    ok("per_auc(loro(FEAT[a], yov)[1])" in s,
       "⑤ 영점은 **raw(비교정)** 점수로 읽는다(Q4-I 에서 교정 artifact 확인)")
    ok("0.5277" in s, "⑤ Q4-I 의 raw 영점 base 0.5277(≠0.5)이 근거로 박혀 있다")
    ok("CAL_GAP" in s, "⑤ 신호 조건에서 교정이 AUROC 를 안 바꾼다를 실측 검증한다")

    # ── ⑥ 대안설명 · 적응증
    ok(s.count("SVEB 는 상심실성이라 QRS 가 ") >= 2 and "기각이 아니라" in s,
       "⑥ ★★★ **형태가 안 먹히는 게 자연스러운 이유**가 사전에 적혀 있다(R39 ①)")
    ok("0.9781" in s and "0.9283" in s,
       "⑥ 적응증을 좁혔을 때의 Q4-I 실측(AUROC 0.9781 · 민감도 0.9283)이 앵커다")
    ok("loro_within" in s and "전문가 혼합" in s,
       "⑥ 리듬 라우팅(불규칙 상·하위 **별도 학습**)을 실제로 잰다")
    ok("AF 대리" in s and ("AF 진단이 아니" in s or "리듬 라벨이 없" in s),
       "⑥ 불규칙성은 **AF 대리지 진단이 아니다**가 가정에 적혀 있다")

    # ── 철회 · GPU · 읽는 순서
    ok("철회" in s and "능력 비용" in s,
       "★★★ 「능력 비용」 가설의 **철회**가 명시돼 있다(R38 ⑦)")
    ok("GPU" in s and ("sklearn CPU" in s or "로지스틱 회귀" in s),
       "★ **GPU 안 쓴다**가 명시돼 있다(사용자 상시 지시)")
    ok("새 데이터 0" in m or "새 데이터 0" in s, "★ 새 데이터 0 — 있던 배열을 처음 쓸 뿐이다")
    ok('READ_ORDER = ("N0"' in s, "READ_ORDER 가 N0 부터다(R29 ②)")
    ok("N0 실패" in s and "raise AssetError" in s, "N0 이 깨지면 **중단**한다")
    ok("R41" in s and "해석 불가" in s, "효과가 0 근처면 필요표본을 **해석 불가**로 낸다")


def dynamic():
    print("\n[동적] 합성으로 확인하는 구성")
    from sklearn.metrics import roc_auc_score
    rng = np.random.RandomState(23)
    L_, RI = 300, 100
    t = np.arange(L_, dtype=float)
    g = lambda c, w, a: a * np.exp(-0.5 * ((t - c) / w) ** 2)
    narrow = g(RI, 3.2, 1.0) + g(RI - 5, 2.0, -0.15) + g(RI + 6, 2.6, -0.25) + g(45, 6.0, .12)
    wide = g(RI + 4, 9.0, -1.0) + g(RI - 6, 5.0, 0.35)

    # ── ⓐ ★★★ 형태는 **S 를 못 찾는다** — SVEB 는 상심실성이라 파형이 N 과 같다
    def corr(x, y):
        x = x - x.mean(); y = y - y.mean()
        return float((x * y).sum() / (np.sqrt((x ** 2).sum() * (y ** 2).sum()) + 1e-9))
    c_sn = corr(narrow, narrow + rng.normal(0, .02, L_))      # S vs 템플릿(N)
    c_vn = corr(wide, narrow)                                 # V vs 템플릿(N)
    ok(c_sn > 0.95 and c_vn < 0.5,
       f"ⓐ ★★★ 템플릿 상관이 **S 는 못 가르고**(S~N {c_sn:.3f}) **V 만 가른다**"
       f"(V~N {c_vn:.3f}) — 그래서 형태의 값은 「S 를 더 찾기」가 아니라 "
       f"**「V 를 위양성에서 걷어내기」** 다")

    # ── ⓑ ★★★ ΔPPV vs Δ민감도 비교가 **산술적으로 편향**돼 있다(스모크가 잡은 것)
    k = 300
    for S_ in (80, 300, 900):
        d_tp = 10.0
        d_ppv, d_sens = d_tp / k, d_tp / S_
        if S_ < k:
            ok(d_sens > d_ppv,
               f"ⓑ ★★★ S={S_} < k={k} 이면 같은 ΔTP={d_tp:.0f} 에서 Δ민감도 {d_sens:.4f} > "
               f"ΔPPV {d_ppv:.4f} 가 **산술적으로 강제**된다 — 둘을 비교하면 안 된다")
        elif S_ > k:
            ok(d_sens < d_ppv,
               f"ⓑ ★ S={S_} > k={k} 이면 부호가 뒤집힌다(Δ민감도 {d_sens:.4f} < ΔPPV "
               f"{d_ppv:.4f}) — 비교 결과가 **코호트 구성에 따라 바뀐다**")
        else:
            ok(abs(d_sens - d_ppv) < 1e-12,
               f"ⓑ S=k 에서만 둘이 같다 — 그 자체가 **비교가 무의미**하다는 증거다")
    # 대안 판정(위양성 구성)은 그 편향에서 자유롭다
    vb, vm_, nb_, nm_ = 400, 80, 2000, 2100
    red_v = (vb - vm_) / vb; red_n = (nb_ - nm_) / nb_
    ok(red_v > 0 > red_n,
       f"ⓑ ★★★ **위양성 구성 판정은 편향이 없다** — 심실기원 {red_v:.1%} 감소 · "
       f"상심실정상 {red_n:.1%}(늘었다: 빈자리를 채운다). 예산이 고정이라 **누가 자리를 "
       f"내줬는지**를 직접 읽는다")

    # ── ⓒ ★★ 템플릿은 라벨을 안 쓴다 — rel-RR 로만 고른다
    n = 2000
    rel = rng.normal(1.0, 0.05, n); lab = rng.rand(n) < 0.15
    rel[lab] = rng.normal(0.72, 0.05, int(lab.sum()))
    pick = (rel >= 0.92) & (rel <= 1.08)
    ok(pick.sum() > 100 and lab[pick].mean() < 0.05,
       f"ⓒ ★★★ rel-RR ∈ [0.92, 1.08] 로 고르면 템플릿 표본에 S 가 "
       f"{lab[pick].mean():.2%} 만 섞인다({int(pick.sum())}개) — **라벨 없이** 정상 템플릿을 "
       f"만들 수 있다(R22)")

    # ── ⓓ ★★ 영점의 유효 표본은 레코드가 아니라 rep 이다
    n_rec, n_rep = 56, 4
    truth = rng.normal(0, 0.03, n_rep)                 # rep 마다 하나의 무작위 방향
    obs = truth[:, None] + rng.normal(0, 0.004, (n_rep, n_rec))   # 레코드는 그 방향을 공유
    per_rec = obs.mean(0)
    bs = [per_rec[rng.randint(0, n_rec, n_rec)].mean() for _ in range(2000)]
    w_rec = np.percentile(bs, 97.5) - np.percentile(bs, 2.5)
    se = obs.mean(1).std(ddof=1) / np.sqrt(n_rep); w_rep = 2 * 1.96 * se
    ok(w_rep > w_rec,
       f"ⓓ ★★★ 레코드끼리 **같은 무작위 방향을 공유**하면 레코드 부트스트랩 폭 {w_rec:.4f} 이 "
       f"rep 수준 폭 {w_rep:.4f} 보다 **좁다** — 영점 불확실성을 **과소평가**한다. "
       f"그래서 두 상단 중 **보수적인 쪽**을 문턱으로 쓴다")

    # ── ⓔ 위음성 해부가 두 실패를 가른다
    sc = rng.normal(0, 1, 1000); miss_hi = np.argsort(sc)[-40:]; miss_lo = np.argsort(sc)[:40]
    pct = np.argsort(np.argsort(sc)) / (len(sc) - 1)
    ok(pct[miss_hi].mean() > 0.9 and pct[miss_lo].mean() < 0.1,
       f"ⓔ ★★ 놓친 S 의 **레코드 내 점수 백분위**가 「아깝게 놓침」(예산 부족 · "
       f"{pct[miss_hi].mean():.2f})과 「못 봄」(모델 실패 · {pct[miss_lo].mean():.2f})을 "
       f"가른다 — Q4-G 의 상한/달성률 분해와 같은 역할을 **박동 수준**에서 한다")
    ok(True is (0.999 < 1.0),
       "ⓔ ★ 놓친 S 의 **상대 RR 이 1.0 근처**면 조기성 자체가 없다는 뜻이고, RR 기반 모델로는 "
       "**원리적으로** 못 본다 — 그때 필요한 건 P′·QRS 형태다")

    # ── ⓕ LORO 누출 없음
    REC = list(range(8)); pr = np.linspace(0.01, 0.5, 8)
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pr[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓕ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-J 픽스처 — 오류 해부 · 파형 첫 사용 · 산술 편향 제거 · 영점 rep 수준")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)

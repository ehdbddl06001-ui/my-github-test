"""퀘스트46 Q7-I‴(정확 정합 · 정합기 감사) 픽스처.

이 실험의 존재 이유는 둘이다.

**① Q7-I″ 의 J1 은 인공물이었다.** 바닥을 개체별 `max(f1, STT)` 로 잡고 문턱을 0 으로
뒀는데, 잡음 둘의 최댓값은 위로 뜬다(실측 0.6440 vs 성분 0.5331·0.5708). 「기각
−0.0705」는 전부 그 팽창이었다(참고항과의 차 −0.0733). → **max 바닥을 폐기**하고
**각 팔을 자기 라벨셔플 영분포 위의 초과분**으로 환산해 비교한다.

**② 정합기 자체를 감사한 적이 없다.** `bw = max(BAND_MIN, bf·중앙RR)` 인데 `BAND_MIN`
이 묶으면 라벨 0.010 이 실제로는 더 넓다. 그리고 `pre_rr` 이 격자 위에 있으면 빈 하나에
서로 다른 RR 이 섞여 `f1` 이 0.5 로 안 간다. → **`pre_rr` 값 자체를 빈으로 쓰는 정확
정합**을 도입한다. 그러면 `f1` 은 **수학적으로 0.5**(동점뿐)여야 한다.

그래서 픽스처의 핵심도 둘이다:

    **정확 정합에서 `f1` 이 정확히 0.5 가 되는가**(안 되면 정합기 구현이 틀렸다)
    **`f2`(상대 조기성)는 정확 정합에서도 살아남는가**(절대 RR 정합의 사각지대)

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② ★ **`max` 로 만든 바닥이 코드에 없는가** — Q7-I″ 의 인공물을 승계하지 않는다
  ③ ★ **자기 라벨셔플 null 위 초과분**으로 비교하는가 (K4·K5)
  ④ ★ **정확 정합**(`pre_rr` 값 자체)이 K1 의 조건인가
  ⑤ **BAND_MIN 이 묶었는지 실측**하는가 — 빈폭/격자 비율을 낸다
  ⑥ 잔여 격차가 **짝 단위**인가 (집합 중앙 vs 집합 중앙이 아니라)
  ⑦ 대역 곡선을 **고정 코호트**로 그리는가
  ⑧ J4 를 **혼합/런 분리**해 재판정하고 `f6` 구제안을 병기하는가
  ⑨ 문턱·Bonferroni 가 CELL 1 상수인가 · 교차적합(R22)인가
  ⑩ 정확 정합 불가 시 **대역 정합으로 몰래 되돌리지 않는가**(R16) · 그림 라벨 ASCII

동적 검사 — 노트북의 함수를 **그대로 꺼내 합성 코호트로 실행**한다:
  ⑪ ★★ **정확 정합에서 `f1` 은 정확히 0.5** (동점뿐이라는 항등식)
  ⑫ ★★ **`f2` 는 정확 정합에서 살아남는다** — 국소 기저선이 흔들리는 코호트
  ⑬ ★ 결정적 짝 — **비보상성**(PAC 형) 코호트와 **완전 보상성** 코호트에서 `f3` 가 갈리는가
  ⑭ ★ **셔플 null 이 교차적합 바닥을 잡는가** — 라벨을 아예 무작위화한 코호트에서
     실측과 null 이 일치해야(초과분 ≈ 0) null 이 바닥 노릇을 한다
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7i3_match_exact.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


def starts(pfx):
    hit = [c for c in CODE if "".join(c["source"]).startswith(pfx)]
    assert len(hit) == 1, f"'{pfx}' 로 시작하는 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = starts("# CELL 1 ")
SRC_K0B = cell("【K-0b】")
SRC_A, SRC_B = cell("【K-A】"), cell("【K-B】")
SRC_C, SRC_D = cell("【K-C】"), cell("【K-D】")
SRC_E, SRC_F = cell("【K-E】"), cell("【K-F】")
SRC_FIG = cell("【K-G】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API · fallback
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert "MedKOSRun(" in SRC_SET, "❌ MedKOSRun 을 안 쓴다"
assert "fallback 없음" in SRC_A or "fallback 없음" in cell("【K-0a】"), "❌ R16 표기가 없다"
assert "except Exception" not in SRC_B and "try:" not in SRC_B, "❌ 정합 셀에 예외 삼킴"
print("  ✅ ① run.* API 정합 · fallback 부재(R16)")

# ── ② ★ max 바닥 폐기
assert "nanmax" not in ALL_SRC, "❌ Q7-I″ 의 `max` 바닥을 승계했다 — 그게 인공물의 원인이다"
assert "np.maximum(np.stack" not in ALL_SRC, "❌ 개체별 max 바닥이 남아 있다"
assert "max 바닥" in SRC_SET and "폐기" in SRC_D, "❌ max 바닥 폐기를 명시하지 않았다"
print("  ✅ ② `max` 로 만든 바닥이 코드에 없다 (Q7-I″ 인공물 미승계)")

# ── ③ ★ 자기 셔플 null 위 초과분
assert 'NULL["stt"]' in SRC_D, "❌ K4 가 STT 의 자기 null 을 안 쓴다"
assert 'NULL["lr_all"]' in SRC_D, "❌ K5 가 LR(전부) 의 자기 null 을 안 쓴다"
assert "EX[\"f3\"] - 0.5" in SRC_D, "❌ 순수 특징의 null 이 0.5 라는 게 코드에 없다"
assert "라벨셔플" in SRC_C and "permutation(tt)" in SRC_C, "❌ 라벨셔플 null 을 안 만든다"
assert "유병률 보존" in SRC_C, "❌ 셔플이 유병률을 보존한다는 표기가 없다"
print("  ✅ ③ 각 팔을 **자기 라벨셔플 null 위 초과분**으로 비교한다")

# ── ④ ★ 정확 정합
assert "def exact_key(" in SRC_B, "❌ exact_key 가 없다"
assert "np.unique(key, return_inverse=True)" in SRC_B, "❌ 값 자체로 빈을 안 만든다"
assert "EXACT_TIE" in SRC_SET and "EXACT_TIE" in SRC_D, "❌ 동점 문턱이 상수가 아니다"
assert re.search(r'decide\(lo1, hi1, EXACT_TIE, "<"\)', SRC_D), "❌ K1 이 상한 검정이 아니다"
print("  ✅ ④ K1 이 **정확 정합**(pre_rr 값 자체)을 조건으로 쓴다")

# ── ⑤ BAND_MIN 감사
assert "bw_over_grid" in SRC_K0B, "❌ 빈폭/격자 비율을 안 낸다"
assert "BAND_MIN 이 묶었다" in SRC_K0B, "❌ BAND_MIN 이 묶였는지 표시하지 않는다"
assert "np.median(np.diff(uq))" in SRC_K0B, "❌ pre_rr 격자를 실측하지 않는다"
print("  ✅ ⑤ BAND_MIN 이 실효 대역폭을 묶었는지 **실측**한다")

# ── ⑥ 짝 단위 잔여
assert "np.abs(ps[:, None] - pn[None, :])" in SRC_B, "❌ 잔여가 짝 단위가 아니다"
assert "집합 중앙 아님" in SRC_B, "❌ 짝 단위임을 명시하지 않았다"
assert "np.median(pre_v[~tt]) - np.median(pre_v[tt])" not in ALL_SRC, \
    "❌ Q7-I″ 의 집합-중앙 잔여 정의가 남아 있다"
print("  ✅ ⑥ 잔여 RR 격차가 **짝 단위**다")

# ── ⑦ 고정 코호트
assert "FIX = EOK" in SRC_E, "❌ 대역 곡선의 코호트를 고정하지 않는다"
assert "코호트가 바뀐 효과" in SRC_E or "코호트 변화" in SRC_E, "❌ 코호트 혼입 경고가 없다"
assert "용량-반응" in SRC_E, "❌ 용량-반응 조건을 명시하지 않았다"
print("  ✅ ⑦ 대역 곡선을 **고정 코호트**로 그린다")

# ── ⑧ J4 분리 + f6
assert "L_MIX" in SRC_F and "L_RUN" in SRC_F and "L_ISO" in SRC_F, "❌ 층을 안 나눈다"
assert '("혼합", L_MIX)' in SRC_F and '("런 우세", L_RUN)' in SRC_F, "❌ 혼합/런을 따로 안 잰다"
assert "lr_f1f6" in SRC_F and "f6" in SRC_A, "❌ f6 구제안이 없다"
assert "부호가 반대" in SRC_F, "❌ 두 층을 묶으면 안 되는 이유가 없다"
print("  ✅ ⑧ J4 를 혼합/런 **분리** 재판정하고 f6 을 병기한다")

# ── ⑨ 상수 · 교차적합
for nm in ("EXACT_TIE", "BONF2", "K_FOLD", "N_REPEAT", "N_SHUF", "BAND_MIN", "MIN_MATCH_REC"):
    assert re.search(rf"^\s*[\w, ]*\b{nm}\b[\w, ]*=", SRC_SET, re.M), f"❌ {nm} 가 CELL 1 상수가 아니다"
assert "BONF2" in SRC_D, "❌ 다중검정 보정을 관문에 안 쓴다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A, "❌ 교차적합(R22)이 아니다"
assert "sc[te] = lr.decision_function" in SRC_A, "❌ 겹 밖 점수가 아니다"
print("  ✅ ⑨ 문턱·Bonferroni 가 CELL 1 상수 · 교차적합(R22)")

# ── ⑩ 되돌리기 금지 · ASCII
assert "EXACT_OK" in SRC_B and "EXACT_OK" in SRC_D, "❌ 정확 정합 성립 여부를 관문이 안 본다"
assert "되돌리지 않는다" in SRC_B or "되돌리지 않는다" in SRC_SET, "❌ 대역 되돌리기 금지 문구가 없다"
assert "측정 불가" in SRC_D, "❌ 성립 안 할 때 판정을 비워두지 않는다"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑩ 정확 정합 불가 시 되돌리지 않는다 · 그림 라벨 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")


def grab(src, first, stop="run.log("):
    i = src.index(first)
    j = src.index(stop, i)
    return src[i:j]


NS = dict(np=np)
exec("import numpy as np\nfrom sklearn.linear_model import LogisticRegression\n"
     "from sklearn.metrics import roc_auc_score\n"
     "K_FOLD, N_REPEAT, SEED0 = 3, 1, 20260803\n"
     "MIN_BAND_S, MIN_BAND_N = 3, 3\nKS = (8, 16)\n", NS)
exec(grab(SRC_A, "def local_base("), NS)
exec(grab(SRC_B, "def grouped_auc("), NS)
rhythm_feats = NS["rhythm_feats"]; build_scores = NS["build_scores"]
grouped_auc = NS["grouped_auc"]; exact_key = NS["exact_key"]

GRID = 2.8125          # 128Hz 원본을 360Hz 로 올린 SVDB 의 RR 격자 (샘플)


def make_record(rng, n=1600, prev=0.12, base=280.0, sd=42.0, early=0.62,
                comp=None, drift=0.0, run_len=1, noise=0.8):
    """`pre_rr` 을 **격자 위에** 만든다(정확 정합이 성립하도록).

    comp  : S 의 (pre+post)/(2·국소기저선). **`1.0` = 완전 보상성 → `f3` 무신호**,
            `<1` = 비보상성(PAC 형) → `f3` 신호. `None` 은 post 를 다음 pre 로 두는데
            그건 무신호가 아니라 **최대 비보상**이라 영코호트로 쓰지 않는다.
    drift : 국소 기저선이 천천히 흔들리는 정도. >0 이면 **같은 절대 RR 인데
            국소 기저선이 다른** 비트들이 생긴다 → `f2` 가 `f1` 과 갈린다.
    """
    n_s = max(int(n * prev), 40)
    n_run = max(1, n_s // max(run_len, 1))
    t = np.zeros(n, bool)
    slots = rng.choice(np.arange(3, n - run_len - 3), size=n_run, replace=False)
    for st in np.sort(slots):
        t[st:st + run_len] = True
    if t.sum() > n_s:
        t[np.where(t)[0][n_s:]] = False
    loc = base * (1.0 + drift * np.sin(2 * np.pi * np.arange(n) / 220.0))
    pre = np.where(t, loc * early, loc) + rng.normal(0, sd, n)
    pre = np.round(np.clip(pre, 90.0, 600.0) / GRID) * GRID          # ★ 격자에 스냅
    if comp is None:
        post = np.r_[pre[1:], base]
    else:
        post = np.r_[pre[1:], base].copy()
        idx = np.where(t)[0]
        post[idx] = np.round(np.clip(2.0 * loc[idx] * comp - pre[idx], 90.0, 900.0) / GRID) * GRID
    B = rng.normal(0, noise, (n, 2, 85)).astype("float32")           # 형태 신호 없음
    return B, t, pre.astype(float), post.astype(float)


def cohort(seed, nrec=6, scramble=False, **kw):
    """`scramble=True` 면 **라벨을 무작위화**한다 — 어떤 특징도 정보가 없는 진짜 영코호트.
    이때 실측 AUROC 는 교차적합 바닥 그 자체이므로 셔플 null 과 일치해야 한다."""
    rng = np.random.RandomState(seed)
    out = []
    for _ in range(nrec):
        B, t, pre, post = make_record(rng, **kw)
        if scramble:
            t = rng.permutation(t)
        X, NAMES = rhythm_feats(pre, post, (8, 16))
        S = build_scores(X, NAMES, t, B, 20260803)
        assert S is not None, "합성 코호트에서 교차적합이 실패했다"
        out.append(dict(B=B, tt=t, pre=pre, X=X, NAMES=NAMES, S=S))
    return out


def macro_exact(recs, arm):
    v = []
    for r in recs:
        key = exact_key(r["pre"])
        a, ks_, pr_, nb_, gp = grouped_auc(r["S"][arm], r["tt"], key, 3, 3, pre_v=r["pre"])
        if pr_ >= 1:
            v.append((a, gp))
    assert v, f"{arm}: 정확 정합 빈이 하나도 없다 — 격자 가정이 깨졌다"
    return float(np.mean([x[0] for x in v])), float(np.median([x[1] for x in v])), len(v)


def shuffle_null(recs, arm, n_shuf=2):
    v = []
    for k, r in enumerate(recs):
        key = exact_key(r["pre"]); acc = []
        for s_ in range(n_shuf):
            rng = np.random.RandomState(4242 + 97 * s_ + k)
            ts = rng.permutation(r["tt"])
            Ss = build_scores(r["X"], r["NAMES"], ts, r["B"], 20260803 + 31 * (s_ + 1))
            if Ss is None:
                continue
            a, _, pr_, _, _ = grouped_auc(Ss[arm], ts, key, 3, 3)
            if pr_ >= 1:
                acc.append(a)
        if acc:
            v.append(float(np.mean(acc)))
    return float(np.mean(v)) if v else float("nan")


# ── ⑪ ★★ 정확 정합에서 f1 은 정확히 0.5
SIG = cohort(11, comp=0.85, drift=0.18)
f1m, gap, nok = macro_exact(SIG, "f1")
assert nok >= 4, f"❌ 정확 정합 가능 개체 {nok} — 픽스처 설계 실패"
assert abs(f1m - 0.5) < 1e-9, f"❌ 정확 정합인데 f1 이 {f1m:.9f} — 정합기 구현이 틀렸다"
assert gap < 1e-12, f"❌ 짝 단위 잔여가 {gap:.3e} — 정확 정합이면 0 이어야 한다"
print(f"  ✅ ⑪ 정확 정합에서 f1 = {f1m:.9f} (동점뿐) · 짝 잔여 {gap:.1e}")

# ── ⑫ ★★ f2 는 정확 정합에서 살아남는다
f2m, _, _ = macro_exact(SIG, "f2_16")
assert f2m > 0.60, (f"❌ 국소 기저선이 흔들리는데 f2_16 이 {f2m:.4f} — "
                    "「절대 RR 정합은 상대 조기성을 통제하지 못한다」를 픽스처가 못 만든다")
FLAT = cohort(12, comp=0.85, drift=0.0)
f2f, _, _ = macro_exact(FLAT, "f2_16")
assert f2f < f2m, f"❌ drift 없는 코호트에서도 f2 가 같다({f2f:.4f} vs {f2m:.4f})"
print(f"  ✅ ⑫ f2_16: drift 있음 {f2m:.4f} vs 없음 {f2f:.4f} — "
      "절대 RR 정합의 사각지대가 재현된다")

# ── ⑬ ★ 결정적 짝 — 비보상성 vs 완전 보상성
COMP = cohort(13, comp=1.0, drift=0.18)     # 완전 보상성 (pre+post = 2·국소기저선)
f3_sig, _, _ = macro_exact(SIG, "f3")
f3_cmp, _, _ = macro_exact(COMP, "f3")
assert f3_sig > 0.60, f"❌ 비보상성이 뚜렷한데 정확 정합 f3 가 {f3_sig:.4f}"
assert f3_sig - f3_cmp > 0.08, f"❌ 두 코호트가 안 갈린다 ({f3_sig:.4f} vs {f3_cmp:.4f})"
print(f"  ✅ ⑬ 정확 정합 f3 — 비보상성 {f3_sig:.4f} vs 완전보상 {f3_cmp:.4f} "
      "(후자는 역방향이라 0.5 아래일 수 있다 — 방향이 아니라 갈리는지를 본다)")

# ── ⑭ ★ 셔플 null 이 교차적합 바닥을 잡는가 (라벨 무작위화 코호트)
RND = cohort(14, scramble=True, comp=0.85, drift=0.18)
lr_rnd = macro_exact(RND, "lr_norr")[0]
lr_rnd_null = shuffle_null(RND, "lr_norr")
exc = lr_rnd - lr_rnd_null
assert np.isfinite(lr_rnd_null), "❌ 셔플 null 이 계산되지 않는다"
assert abs(exc) < 0.06, (f"❌ 라벨 무작위 코호트인데 LR(f3,f4) 초과분이 {exc:+.4f} — "
                         "셔플 null 이 교차적합 바닥을 못 잡는다")
lr_sig = macro_exact(SIG, "lr_norr")[0]
lr_sig_null = shuffle_null(SIG, "lr_norr")
assert lr_sig - lr_sig_null > abs(exc) + 0.05, \
    f"❌ 신호 코호트 초과분({lr_sig - lr_sig_null:+.4f})이 영코호트({exc:+.4f})와 안 갈린다"
print(f"  ✅ ⑭ 셔플 null — 라벨무작위 초과 {exc:+.4f} · 신호 초과 {lr_sig - lr_sig_null:+.4f}")

print("\n✅ Q7-I‴ 픽스처 14/14 통과")

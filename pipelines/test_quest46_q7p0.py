"""퀘스트46 Q7-P0(SVDB P-위치 표) 픽스처.

Q7-S′ 의 **전제 조건**을 만드는 자산 생성 런이다. 관문이 없으므로 픽스처가 지킬 것은
「가설 판정이 옳은가」가 아니라 **「만든 자산이 좌표상 옳은가」** 다.

핵심은 하나다 — **좌표 정합의 구성적 증명**.
`svdb_data5.npz` 에는 R 표본 위치가 없다. 그래서 `mit-bih/svdb_labels.py` 의 비트 절단
로직을 재현해 되살리는데, 재현이 조금이라도 어긋나면 P 위치가 **엉뚱한 비트에 붙는다**.
그리고 그건 조용히 틀린다 — 다운스트림에서 안 보인다. 그래서 `(pid, sym)` 수열 일치를
**중단 조건**으로 건다.

★ 이 퀘스트는 좌표로 두 번 데었다(Q7-T 가 주석 확장자·레코드 이름을 추측해 두 번 멈췄다).

정적 검사:
  ① `run.*` API(finish dict) · fallback 부재(R16)
  ② ★★★ **정합 증명이 강제인가** — 비트 수·`(pid, sym)` 수열이 어긋나면 **중단**하는가
  ③ ★★ npz 필드를 **추측하지 않는가** — `D5.files` 를 찍고, 없으면 무엇이 있는지 보이며 중단
  ④ ★★★ **절단 상수가 `mit-bih/svdb_labels.py` 와 같은가** — 실제 파일을 읽어 대조한다
       (그 파일이 바뀌면 이 픽스처가 깨져야 한다 — 조용한 좌표 어긋남 차단)
  ⑤ ★★ **연속 신호**에 구획기를 거는가 — 비트 되붙이기가 없는가(Q7-U 근거 병기)
  ⑥ ★ 구획기가 **라벨을 인자로도 안 받는가**(R22)
  ⑦ ★ 중간 저장·재개가 있는가(35분 셀 · Colab 세션 끊김 대비)
  ⑧ ★ **관문이 없다**는 표기 · 결론 분기 부재(R29 ②)
  ⑨ ★ 생리학적 자기검증(PR 120~200ms)을 **출력**하는가
  ⑩ 그림 ASCII · 저장 자산에 신원(`pid`·`sym`)이 함께 들어가는가

동적 검사 — 노트북 함수를 **그대로 꺼내** 돌린다:
  ⑪ ★★ `realign()` 이 `svdb_labels.py` 의 재정합과 **같은 값**을 내는가
  ⑫ ★★ 비트 좌표 복원 — 절대 P 위치 → `p_idx` 가 왕복하는가 · 창 밖은 −1 인가
  ⑬ ★ `score_at()` 건전성 — 국소 두드러짐이 진짜 봉우리에서 커지는가
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7p0_svdb_pdelin.ipynb")))
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


SRC_0, SRC_SET = starts("# CELL 0 "), starts("# CELL 1 ")
SRC_A, SRC_B = cell("【P0-A】"), cell("【P0-B】")
SRC_C, SRC_D = cell("【P0-C】"), cell("【P0-D】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)
MD_SRC = "".join("".join(c["source"]) for c in NB["cells"] if c["cell_type"] == "markdown")

print("### 정적 검사")

# ── ①
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ finish 에 dict 를 안 넘긴다"
assert re.search(r"if not os\.path\.exists\(SV5\):\s*\n\s*raise AssetError", SRC_A), \
    "❌ svdb_data5.npz 가 없어도 안 멈춘다(R16)"
assert re.search(r"if len\(RECS\) < 50:\s*\n\s*raise AssetError", SRC_B), \
    "❌ SVDB 다운로드 실패에도 안 멈춘다(R16)"
assert not re.search(r"except[^\n]*:\s*\n[^\n]*(synth|합성|randn|normal\()", ALL_SRC), \
    "❌ 실패를 합성으로 대체하는 경로가 있다(R16)"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★★★ 정합 증명이 강제인가 (이 런의 존재 이유)
assert re.search(r"if len\(R_ALL\) != NB5:\s*\n\s*raise AssetError", SRC_B), \
    "❌ **비트 수가 달라도 안 멈춘다** — 절단 로직이 어긋난 채로 진행한다"
assert "bad_p" in SRC_B and "bad_s" in SRC_B, "❌ pid·sym 불일치를 안 센다"
assert re.search(r"if bad_p or bad_s:\s*\n\s*i0 = int\(np\.argmax", SRC_B), \
    "❌ 수열이 어긋나도 안 멈춘다 — P 위치가 **엉뚱한 비트**에 붙는다"
assert "첫 어긋남 idx" in SRC_B, "❌ 어디서 어긋났는지 안 알려준다 — 고칠 수가 없다"
assert re.search(r"raise AssetError\(f\"수열 불일치", SRC_B), "❌ 중단이 AssetError 가 아니다"
assert "proven=True" in SRC_B, "❌ 증명 사실을 config 에 안 남긴다"
# 증명이 **구획 전에** 끝나는가 — 순서가 뒤집히면 헛돈다
assert CODE.index([c for c in CODE if "【P0-B】" in "".join(c["source"])][0]) < \
       CODE.index([c for c in CODE if "【P0-C】" in "".join(c["source"])][0]), \
    "❌ 정합 증명이 구획(35분) 뒤에 온다 — 어긋나면 35분을 버린다"
print("  ✅ ② 정합 증명이 **중단 조건** · 첫 어긋남 위치 보고 · **구획 전에** 끝난다")

# ── ③ ★★ npz 필드를 추측하지 않는가
assert "D5.files" in SRC_A, "❌ 보유 필드를 안 찍는다 — 추측하게 된다"
assert re.search(r'for need in \("beat", "pid", "sym", "y3"\)', SRC_A), \
    "❌ 필요한 필드를 명시적으로 요구하지 않는다"
assert "보유: {sorted(D5.files)}" in SRC_A, "❌ 없을 때 **무엇이 있는지** 안 보여준다"
assert re.search(r'if np\.asarray\(D5\["beat"\]\)\.shape\[1:\] != \(2, L\)', SRC_A), \
    "❌ 비트 모양을 검사하지 않는다"
print("  ✅ ③ npz 필드를 **확인**한다 — 보유 목록 출력 · 없으면 무엇이 있는지 보이며 중단")

# ── ④ ★★★ 절단 상수가 svdb_labels.py 와 같은가 (교차 파일 회귀)
LBL = open(os.path.join(ROOT, "mit-bih", "svdb_labels.py"), encoding="utf-8").read()
src_fs = re.search(r"^_FS_SRC, _FS_DST = (\d+), (\d+)", LBL, re.M).groups()
src_l = re.search(r"^_L, _RPRE = (\d+), (\d+)", LBL, re.M).groups()
nb_fs = re.search(r"^FS_SRC, FS_DST = (\d+), (\d+)", SRC_SET, re.M).groups()
nb_l = re.search(r"^L, RPRE = (\d+), (\d+)", SRC_SET, re.M).groups()
assert src_fs == nb_fs, f"❌ 샘플레이트 상수 불일치 — svdb_labels {src_fs} vs 노트북 {nb_fs}"
assert src_l == nb_l, f"❌ 비트 절단 상수 불일치 — svdb_labels {src_l} vs 노트북 {nb_l}"
src_beat = re.search(r'^BEAT_SYMS = set\("([^"]*)"\)', LBL, re.M).group(1)
nb_beat = re.search(r'^BEAT_SYMS = set\("([^"]*)"\)', SRC_SET, re.M).group(1)
assert set(src_beat) == set(nb_beat), \
    f"❌ BEAT_SYMS 불일치 — svdb_labels {sorted(set(src_beat))} vs 노트북 {sorted(set(nb_beat))}"
src_aami = dict(re.findall(r"'(.)': (\d)", LBL[LBL.index("AAMI5 = {"):LBL.index("CLS5 =")]))
nb_aami = dict(re.findall(r"'(.)': (\d)", SRC_SET[SRC_SET.index("AAMI5 = {"):
                                                 SRC_SET.index("BEAT_SYMS")]))
assert src_aami == nb_aami, f"❌ AAMI5 불일치 — 누락/추가 {set(src_aami) ^ set(nb_aami)}"
assert "50" in re.search(r"^RALIGN_MS = (\d+)", SRC_SET, re.M).group(1), "❌ 재정합 반경"
print(f"  ✅ ④ 절단 상수가 `svdb_labels.py` 와 **일치** — fs {nb_fs} · 비트 {nb_l} · "
      f"BEAT_SYMS {len(set(nb_beat))}종 · AAMI5 {len(nb_aami)}종")

# ── ⑤ ★★ 연속 신호에 건다 (되붙이기 금지)
assert "nk.ecg_delineate(x, rpeaks=bs" in SRC_C, "❌ 연속 신호에 구획기를 안 건다"
assert "x = sig[LEAD]" in SRC_C, "❌ 원 연속 신호가 아니라 다른 걸 먹인다"
for w in ("되붙", "0.7705", "0.6132"):
    assert w in SRC_C or w in MD_SRC, f"❌ 되붙이기를 왜 안 하는지 근거('{w}')가 없다"
assert "Voronoi" not in SRC_C, "❌ 구획 셀에 되붙이기 코드가 있다"
print("  ✅ ⑤ **원 연속 신호**에 구획 · 되붙이기 없음(Q7-U 실측 0.7705→0.6132 병기)")

# ── ⑥ ★ 구획기가 라벨을 안 본다 (R22)
_h = "for ri, (rec, sig, bs, _bsym, _keep) in sorted(SIGS.items()):"
dl = SRC_C[SRC_C.index(_h) + len(_h):]        # ★ 헤더의 튜플 언패킹은 제외하고 **본문만**
dl = dl[:dl.index("비트 좌표로 되돌린다")]
# ★ **주석은 뺀다** — 라벨을 왜 안 쓰는지 적은 문장까지 걸리면 근거를 못 적는다
dl_code = "\n".join(ln.split("#", 1)[0] for ln in dl.splitlines())
dl_code = dl_code.replace("_bsym", "").replace("_keep", "")
for w in ("Y3", "y3", "AAMI5", "bsym", "keep"):
    assert w not in dl_code, f"❌ 구획 루프 **본문 코드**가 라벨(`{w}`)을 본다(R22)"
assert "인자로도 안 받는다" in SRC_C, "❌ R22 근거가 없다"
assert "여기 안 넣는다" in SRC_C, "❌ 유효성 마스크를 구획 루프에서 뺀 근거가 없다"
assert "kp_ = keep" in SRC_C, "❌ 유효성을 복원 단계에서 안 붙인다"
print("  ✅ ⑥ 구획기는 **라벨을 인자로도 안 받는다** — R 위치만(R22)")

# ── ⑦ ★ 중간 저장·재개
assert "CKPT" in SRC_SET and "np.savez(CKPT" in SRC_C, "❌ 중간 저장이 없다"
assert re.search(r"if os\.path\.exists\(CKPT\):", SRC_C), "❌ 재개 경로가 없다"
assert re.search(r"if ri in CK:\s*\n\s*continue", SRC_C), "❌ 완료 레코드를 다시 돈다"
print("  ✅ ⑦ 레코드마다 중간 저장 · 끊기면 이어서 돈다(35분 셀)")

# ── ⑧ ★ 관문 없음 · 결론 분기 부재
assert "관문" in SRC_SET and "없음" in SRC_SET, "❌ 관문 없음이 사전등록에 없다"
assert "여기서 결론을 내지 않는다" in SRC_D, "❌ 진단에서 결론을 안 막는다"
assert "판정은 Q7-S′ 가 한다" in SRC_D or "Q7-S′ 가 한다" in SRC_D, "❌ 판정 주체가 없다"
for bad in ("✅ 지지", "❌ 기각", "⚠️ 미결"):
    assert bad not in ALL_SRC, f"❌ 판정 표식 '{bad}' 이 있다 — 관문 없는 런이다"
print("  ✅ ⑧ **관문 없음** — 판정 표식 부재 · 진단에서 결론을 명시적으로 막는다(R29 ②)")

# ── ⑨ ★ 생리학적 자기검증
assert "120~200ms" in SRC_D or "120-200" in SRC_D, "❌ 생리학적 PR 범위를 안 쓴다"
assert "좌표가 틀린 것이다" in SRC_D, "❌ 자기검증의 해석을 안 적었다"
assert "np.median(pos_ms)" in SRC_D, "❌ P 위치 중앙값을 안 낸다"
print("  ✅ ⑨ 생리학적 자기검증 — P 위치 중앙값 vs PR 120~200ms 를 출력·해석")

# ── ⑩ 저장 자산 신원 · 그림 ASCII
sv = SRC_D[SRC_D.index("np.savez(OUTNP"):SRC_D.index("run.log(f\"\\n  ✅ 저장")]
for f in ("p_idx", "p_score", "r_samp", "pid", "sym", "lead", "fs", "beat_len", "rpre"):
    assert f in sv, f"❌ 저장 자산에 `{f}` 가 없다 — 소비 측이 정합을 재확인 못 한다"
assert "다시 대조해 정합을 재확인" in SRC_D, "❌ 소비 측 재확인 안내가 없다"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_D)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
print("  ✅ ⑩ 저장 자산에 신원(pid·sym)·좌표 메타 포함 · 그림 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")

FS_DST = int(nb_fs[1]); L = int(nb_l[0]); RPRE = int(nb_l[1])
NS = dict(np=np)
exec("import numpy as np\nclass AssetError(RuntimeError): pass\n", NS)
NS.update(FS_DST=FS_DST, L=L, RPRE=RPRE, RALIGN_MS=50, P_LO_MS=-278.0, P_HI_MS=-42.0)
exec(SRC_B[SRC_B.index("def realign("):SRC_B.index("def load_rec(")], NS)
exec(SRC_C[SRC_C.index("def ms2s("):SRC_C.index("CK = {}")], NS)
realign, score_at, ms2s = NS["realign"], NS["score_at"], NS["ms2s"]

# ── ⑪ ★★ realign 이 svdb_labels.py 와 같은 값을 내는가
rng = np.random.RandomState(11)
T = 4000
sig = rng.normal(0, 0.01, (2, T))
true_R = np.arange(400, T - 400, 310)
for p in true_R:
    t = np.arange(p - 40, p + 40) - p
    sig[0, p - 40:p + 40] += 1.0 * np.exp(-0.5 * (t / 3.0) ** 2)
    sig[1, p - 40:p + 40] += 0.6 * np.exp(-0.5 * (t / 3.0) ** 2)


def realign_ref(sig, R, fs=FS_DST, ms=50):
    """`mit-bih/svdb_labels.py` 의 재정합을 **그대로 옮긴 참조 구현**."""
    w = int(fs * ms / 1000.0)
    a, b = max(0, R - w), min(sig.shape[1], R + w + 1)
    if b - a < 3:
        return R
    return a + int(np.argmax(np.sqrt(sig[0, a:b] ** 2 + sig[1, a:b] ** 2)))


jit = rng.randint(-12, 13, len(true_R))
got = np.array([realign(sig, int(p + j), T) for p, j in zip(true_R, jit)])
ref = np.array([realign_ref(sig, int(p + j)) for p, j in zip(true_R, jit)])
assert np.array_equal(got, ref), f"❌ 재정합이 참조 구현과 다르다 (첫 차이 {np.argmax(got != ref)})"
assert np.abs(got - true_R).max() <= 1, f"❌ 재정합이 R 로 안 모인다 {np.abs(got-true_R).max()}"
print(f"  ✅ ⑪ `realign()` ≡ svdb_labels 참조 구현 · 지터 ±12 → 오차 "
      f"{np.abs(got - true_R).max()}샘플")

# ── ⑫ ★★ 비트 좌표 복원 왕복
R_ = true_R.copy()
p_abs = R_ - 60                                        # R−167ms · P 창 안
rel = np.where(p_abs >= 0, p_abs - (R_ - RPRE), -1)
rel = np.where((rel >= 0) & (rel < L), rel, -1)
assert np.all(rel == RPRE - 60), f"❌ 왕복이 안 맞는다 {np.unique(rel)}"
assert np.all((rel - RPRE) / FS_DST * 1000 == -60 / FS_DST * 1000), "❌ ms 환산이 틀렸다"
# 창 밖(비트 시작 이전)은 −1 이어야 한다
far = R_ - (RPRE + 50)
rel_far = far - (R_ - RPRE)
rel_far = np.where((rel_far >= 0) & (rel_far < L), rel_far, -1)
assert np.all(rel_far == -1), "❌ 비트 창 **이전**의 P 를 −1 로 안 만든다"
beyond = R_ + L                                        # 비트 창 이후
rel_b = beyond - (R_ - RPRE)
rel_b = np.where((rel_b >= 0) & (rel_b < L), rel_b, -1)
assert np.all(rel_b == -1), "❌ 비트 창 **이후**의 P 를 −1 로 안 만든다"
lo, hi = ms2s(-278.0), ms2s(-42.0)
assert lo < hi <= 0 and RPRE + lo >= 0, f"❌ P 창 {lo}~{hi} 이 비트 안에 안 들어간다"
print(f"  ✅ ⑫ 비트 좌표 왕복 — P at R−60 → idx {RPRE-60} · 창 밖 전/후 모두 −1 · "
      f"P 창 idx {RPRE+lo}~{RPRE+hi}")

# ── ⑬ ★ score_at 건전성
x = np.zeros(3000)
Rs = np.arange(500, 2500, 310)
for p in Rs:
    t = np.arange(p - 100, p + 100) - p
    x[p - 100:p + 100] += 0.10 * np.exp(-0.5 * (t / 6.0) ** 2)
x += 0.003 * rng.randn(len(x))
assert "SCORE_HALF_MS" in SRC_C, "❌ 점수 창이 위치 중심이 아니다"
assert "창 정의가 다르다" in SRC_C, "❌ Q7-U 와 다르다는 근거가 없다"
s_peak = score_at(x, Rs)                                # 봉우리 위
s_flat = score_at(x, Rs + 150)                          # 봉우리 밖
assert np.median(s_peak) > 2.0 * np.median(s_flat), \
    f"❌ 봉우리에서 점수가 안 커진다 {np.median(s_peak):.2f} vs {np.median(s_flat):.2f}"
assert np.isfinite(score_at(x, np.array([0, len(x) - 1]))).all(), "❌ 경계에서 NaN"
print(f"  ✅ ⑬ `score_at()` — 봉우리 {np.median(s_peak):.2f} > 밖 {np.median(s_flat):.2f} · 경계 안전")

print("\n✅ Q7-P0 픽스처 13/13 통과")

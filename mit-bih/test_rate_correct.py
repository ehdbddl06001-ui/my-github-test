# =============================================================================
#  test_rate_correct.py — rate_correct_audit 의 논리 검증 (합성, 정답을 아는 상태)
#
#  왜 별도 파일인가: 이 감사는 "사용자가 제안한 시간축 델타 특징이 사실은 심박수
#  아닌가" 를 판정한다. 판정을 신뢰하려면 **정답을 아는 데이터**에서 먼저 맞는지
#  봐야 한다. 실제로 이 검증이 코드 결함 4개를 잡았다:
#    1) 완전 보정된(=상수) 특징의 부동소수 잡음을 순위 매겨 AUC 0.667 → '형태 정보
#       있음' 이라는 반대 결론
#    2) 교란 ρ 를 주변(marginal)으로 재서, 판별 AUC 1.000 인 순수 형태 특징을
#       '심박수 대리' 로 오판 (리듬이 심박수를 정하므로 좋은 판별자는 전부 걸린다)
#    3) 심박수 겹침 구간이 없을 때 band=None 을 넘겨 **비맞춤 AUC 로 조용히 되돌아감**
#    4) 적격 구간 1개 × 환자 3명의 AUC 0.667 을 '판별력' 으로 계상
#  ★결론적으로 |AUC-0.5| 의 고정 문턱으로 '독립' 을 선언하는 것 자체가 검증
#    불가능했다 → 감소율을 보고하고 애매하면 애매하다고 말하도록 바꿨다.
#
#  실행:  python test_rate_correct.py
# =============================================================================
import numpy as np, os, tempfile
g = {"__name__": "m"}
exec(compile(open("ecg_multidb.py").read(), "e", "exec"), g)
exec(compile(open("afib_bench.py").read(), "e", "exec"), g)   # win_starts
W = 128
base = tempfile.mkdtemp(); g["_BASE"] = base
rng = np.random.RandomState(0)

# ── 합성 코퍼스: 환자 60명, 리듬 3종, 심박수를 리듬과 **일부러 상관**시킨다 ──
rn = ["N", "AFIB", "AFL"]
PID = []; RHY = []; PRE = []
truth = {}
for p in range(60):
    r = p % 3
    nb = W * 12
    # AFIB 은 빠르고 N 은 느리게 → 심박수가 리듬의 대리변수가 되는 상황
    # ★심박수 분포가 리듬 간에 **겹치도록** 넓게 뽑는다(실제 데이터가 그렇다).
    #   겹치지 않으면 심박수와 형태를 원리적으로 분리할 수 없어 감사가 '판정 불가'다.
    hr_rr = float(np.clip({0: 0.90, 1: 0.72, 2: 0.78}[r] + 0.16 * rng.randn(),
                          0.45, 1.25))
    PID += [p] * nb; RHY += [r] * nb
    # ★환자 안에서도 심박수가 변한다(24시간 기록의 일주기 변동) → 맞춤이 가능해진다
    circ = 0.10 * np.sin(np.linspace(0, 4 * np.pi, nb))
    PRE += list(np.clip(hr_rr + circ + 0.03 * rng.randn(nb), 0.3, 2.0) * 360)
    truth[p] = (r, hr_rr)
d = dict(pid=np.array(PID), rhythm=np.array(RHY), pre_rr=np.array(PRE, "float32"),
         rhythm_names=np.array(rn))
np.savez(f"{base}/afib_rr.npz", **d)

# ── 합성 특징 2종 ─────────────────────────────────────────────────────────
# rt_pure : 순수 심박수 함수  rt = 0.30 * RR^0.5   (형태 정보 0)
# rt_morph: 심박수와 무관하고 리듬에만 의존         (형태 정보만)
names = ["rt_med", "pr_med"]
KEY = []; F = []
for p in np.unique(d["pid"]):
    idx = np.flatnonzero(d["pid"] == p)
    for s in g["win_starts"](len(idx), W, W):
        rr = float(np.median(d["pre_rr"][idx][s:s + W])) / 360.0
        r, _ = truth[int(p)]
        KEY.append((int(p), int(s)))
        F.append([0.30 * rr ** 0.5,                    # rt_med = 순수 심박수
                  0.16 + 0.04 * r])                    # pr_med = 순수 형태
np.savez(f"{base}/afib_atrial.npz", key=np.array(KEY, np.int64),
         feat=np.array(F, "float32"), names=np.array(names), W=W, stride=W)

out = g["rate_correct_audit"](W=W, min_win=3)
print("\n" + "=" * 72)
def verd(t, tag_sub):
    return [r for r in out[t]["rows"] if tag_sub in r["tag"]][0]
a_rt = out["rt_med"]["a_fit"]
print(f"검산 1  rt_med 는 0.30·RR^0.5 로 만들었다 → 추정 α 가 0.5 여야 한다: "
      f"{a_rt:.3f}  {'OK' if abs(a_rt-0.5)<0.05 else '✗실패'}")
r0 = verd("rt_med", "보정 없음"); rf = verd("rt_med", "추정")
print(f"검산 2  보정 전 |ρ|={r0['rho']:.3f} → 추정 α 보정 후 |ρ|={rf['rho']:.3f}  "
      f"{'OK' if rf['rho']<0.2 else '✗실패'}")
print(f"검산 3  rt_med 는 형태 정보가 0 이므로 보정 후 '판별력 소멸' 이어야 한다")
print(f"        보정 전 판정: {r0['verdict']}")
print(f"        보정 후 판정: {rf['verdict']}  "
      f"{'OK' if '소멸' in rf['verdict'] else '✗실패'}")
print(f"검산 3b 보정 없는 rt_med(순수 심박수)는 '독립' 으로 선언되면 안 된다")
print(f"        판정: {r0['verdict']}  "
      f"{'OK' if not r0['verdict'].startswith('★') else '✗실패'}")
p0 = verd("pr_med", "보정 없음"); pf = verd("pr_med", "α=0.500")
print(f"검산 4  pr_med 는 형태 정보만 있으므로 보정해도 판별력이 남아야 한다")
print(f"        보정 전: {p0['verdict']}   보정 후(α=0.5): {pf['verdict']}  "
      f"{'OK' if pf['verdict'].startswith('★') else '✗실패'}")

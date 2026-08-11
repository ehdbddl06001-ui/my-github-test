# Codex 과제 — Q5-D join 실패의 기전 규명 (진단 설계만, 실행·규칙완화 금지)

작성: 2026-08-11 · 작성자: Claude Code · 수신: Codex
근거: `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` Decision log
(2026-08-11 "DS1 gate, rerun under the corrected module — measured result" 절)
대상: 새 진단 명세 (아직 없음 — Codex 가 작성할지 여부부터 결정한다)

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. research/HANDOFF_2026-08-11_Q5D_v_class_join_failure_to_codex.md   ← 이번 지시서
3. experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md
   특히 Decision log 마지막 절(2026-08-11 DS1 gate 실측)
4. research/HANDOFF_2026-08-10_Q5D_preflight_result_to_codex.md  (RR 계약·44-record 대장)
5. research/PROVENANCE_2026-08-10_mamba_data_lineage.md

[상황]
Q5-D DS1 gate 가 실측으로 끝났다. 판정 JOIN_UNRESOLVED, first stopping reason
3_overall_coverage, failed leg LEG2_POSITIONAL_JOIN, 5/13. null 은 3 family x
10,000 완주했고 서로 다른 code sha 사이에서 bitwise 재현됐다.

등록된 규칙은 반증되지 않았고 자격도 얻지 못했다. 지금 필요한 것은 규칙을
고치는 것이 아니라 **왜 실패했는지를 규명하는 진단**이다.

[과제]
아래 §3 의 경쟁 가설 4개를 구별할 수 있는 진단 실험을 설계할지 판단하고,
설계한다면 새 명세를 experiments/specs/ 에 작성하라. 설계만 한다.
구현·실행은 하지 않는다.

[반드시 알아야 할 것 — 내가 기록해 둔 가설이 산술적으로 불충분하다]
Decision log 에 "PVC 의 넓은 QRS 가 detect_r() 위치를 이동시킨다"는 기전
가설을 남겨 뒀다. 그 가설만으로는 실측을 설명하지 못한다:
- record 208 은 cache 2,572 행 중 2,167 행(84.3%)이 실패했다. 어떤 MIT-BIH
  record 에서도 V 가 전체의 84%일 수는 없다 → 208 의 실패는 V 를 넘어선다.
- 개수 불일치 층의 총 결손은 -25 행인데 그 층의 실패는 6,648 행이다. 266배다
  → "검출기가 비트를 놓쳤다"만으로는 설명이 안 된다. 무언가 전파된다.
내 가설을 그대로 채택하지 말고 §3 의 넷을 대등하게 놓고 시작하라.

[구조적으로 중요한 것]
실패 24,341 건은 한 종류가 아니다. NO_CANDIDATE_EDGE 56.4% 와
EDGE_IN_NO_MAXIMUM_MATCHING 40.6% 는 서로 다른 병일 가능성이 높다. 하나의
기전으로 묶어 설명하려 하지 마라.

[실행 0 으로 지금 당장 가능한 것 — §4 의 M0]
기존 run bundle 의 unmatched_and_ambiguous.csv 에 이미 record ·
raw_atr_ordinal · raw_r_sample · mamba_aami · 양쪽 row index ·
drop_or_unmatched_reason 이 들어 있다. 새 실행 없이 실패의 class 구성과
record 내 위치 분포를 낼 수 있다. 진단 설계 전에 이것부터 볼지 판단하라.

[절대 하지 말 것]
- tolerance 를 넓혀 coverage 가 오르는지 보는 것. 결과를 본 뒤의 완화다.
- 진단 측정 결과로 새 tolerance 를 고르는 것. 새 규칙은 새 rule_fingerprint 와
  자기 null 을 갖는 별도 사전등록이어야 하고, 임계값은 그것이 만들어내는
  coverage 와 무관한 근거로 정해져야 한다.
- 개수 불일치 record 5개를 제외하고 다시 재는 것. equal-count 층도 0.856 으로
  0.95 에 미달이라 제외해도 규칙은 구제되지 않는다(§1).
- DS2 per-beat label · V10 확률 · association · 학습. 전부 봉인 유지다.
- 기존 Drive 산출물 수정·삭제. superseded 도 보존 대상이다.

[바꾸지 말 것]
과학적 질문 · DS1→DS2 inter-patient split · primary metric
(join_min_class_recall) · parent primary(S_PR_AUC) · 이미 확정된 join 규칙의
상수(tolerance·matcher·certification·gate·통계·seed·중단 규칙).
진단은 join 규칙을 관찰할 뿐 바꾸지 않는다.

[산출]
1) 진단을 할 가치가 있는지에 대한 판단과 근거. "하지 않는다"도 유효한 답이다.
2) 한다면 새 명세 초안(status: draft, design_owner: codex,
   implementation_owner: claude). §4 의 측정안은 제안일 뿐이니 채택·수정·기각을
   명시하라.
3) 각 측정 결과가 어느 가설을 지지/반증하는지 사전 등록. 측정 후에 해석을
   맞추지 않도록 먼저 적는다.
4) 진단이 무엇을 licence 하지 않는지 명시(특히 tolerance).
```

---

## 0. 한 줄 요약

Q5-D 는 **반증되지도 자격을 얻지도 못한 채(`JOIN_UNRESOLVED`) 끝났고**, 실패의
기전은 아직 모른다. 내가 남긴 PVC 가설은 산술적으로 불충분하다. 경쟁 가설 4개를
구별하는 진단이 필요한지, 필요하다면 무엇을 재야 하는지를 Codex 가 정해야 한다.

---

## 1. 측정된 사실 (전부 canonical run 실측, 추정 없음)

판정: `JOIN_UNRESOLVED` · first stop `3_overall_coverage` ·
failed leg `LEG2_POSITIONAL_JOIN` · gates **5 / 13**

| 항목 | 값 | 등록 임계 |
|---|---|---|
| overall coverage | 0.7594904156198691 | ≥ 0.95 |
| N / S / V coverage | 0.8097 / 0.7341101694915254 / **0.15776955602537** | 각 ≥ 0.90 |
| class_coverage_balance | 0.20773080578851555 | ≥ 0.80 |
| record 최악 / balance | 0.15746500777604977 / 0.42383354671362466 | ≥ 0.80 / ≥ 0.80 |
| class agreement (전체 / 최악) | 0.9998958143411559 / 0.998324958123953 | ≥ 0.995 / ≥ 0.98 |
| `J_min` TRUE | 0.15750528541226216 | — |
| q95 / q99 (family-wise max-null) | 0.1517 / 0.15618393234672304 | — |
| gate 9 `J_min > q99` | **PASS** | — |
| gate 10 `signal_to_null` | **FAIL** 1.0383275261324043 | ≥ 5.0 |
| gate 11 bootstrap 95% CI | **FAIL** [-0.05260925120498404, 0.13225229746939302] | 하한 > 0 |
| gate 12 S share inflation | **FAIL** 1.3621933621933622 | ≤ 1.25 |

certified 38,393 / cache 50,551. 실패 24,341 = mamba측 12,183 + cache측 12,158.

**실패의 구성 — 한 종류가 아니다:**

| 원인 | 개수 | 비중 | 뜻 |
|---|---|---|---|
| `LEG2_NO_CANDIDATE_EDGE` | 13,716 | 56.4% | 허용오차 안에 후보가 **아예 없다** |
| `LEG2_EDGE_IN_NO_MAXIMUM_MATCHING` | 9,887 | 40.6% | 후보는 있는데 최대 단조 사슬에 **못 들어간다** |
| `LEG2_AMBIGUOUS_RANK_CLASS` | 738 | 3.0% | 진짜 모호성 |

**사전 등록한 층:**

| 층 | records | cache rows | certified | ambiguous | coverage |
|---|---|---|---|---|---|
| equal_count | 17 | 38,261 | 32,751 | 157 | 0.8559891273097933 |
| mismatched_count | 5 | 12,290 | 5,642 | 305 | 0.4590724165988609 |

최악 record: **208** 0.15746500777604977 · **116** 0.5473508552357113 (둘 다 개수 불일치).

**null 은 서로 다른 code sha 사이에서 bitwise 재현됐다** (세 family + `J_null_max`,
각 10000/10000). gate 11 은 결함 구현에서 `[0.4824, 0.7195]` 였다가 수정 후
0 을 걸치는 구간이 됐다 — 옛 값은 gate 9 를 뒷받침했고 등록 통계량은 그러지 않는다.

---

## 2. 내가 기록해 둔 가설은 불충분하다 — 산술로 확인된다

Decision log 에 남긴 기전 가설은 이것이다: 고정 tolerance 가 흡수하는 것은
`e_j − e_{j−1}`(이웃 간 검출 오프셋 변화)인데, PVC 의 넓고 비정상적인 QRS 가
`detect_r()` 위치를 주석 대비 이동시켜 pre·post RR 을 함께 어긋내고 이웃의 RR 도
교란한다.

**이 가설만으로는 실측이 설명되지 않는다. 두 가지 산술 때문이다.**

**(a) record 208 의 실패는 V 를 넘어선다.**
208 은 cache 2,572 행 중 **2,167 행(84.3%)** 이 실패했다. MIT-BIH 어떤 record
에서도 V 가 전체의 84% 를 차지하지 않는다(208 은 PVC 가 많기로 유명한 record
지만 그래도 절반 안팎이다). 따라서 **208 에서는 N 비트도 대량으로 실패하고
있다.** class 수준 기전만으로는 record 수준 붕괴를 못 만든다.

**(b) 개수 결손과 실패 규모의 자릿수가 다르다.**
개수 불일치 층의 등록 결손은 `108:-1, 116:-14, 203:-2, 208:-7, 223:-1` = **총 -25 행**
이다. 그런데 그 층의 실패는 **6,648 행**이다. **266 배**다. "검출기가 비트를 몇 개
놓쳤다"는 그 자체로는 설명이 되지 않는다 — 작은 결손이 **전파되는** 기전이거나,
결손과 무관한 다른 기전이다.

내 가설을 기각하자는 게 아니라, **그것을 기본값으로 놓고 시작하면 안 된다**는
뜻이다. §3 의 넷을 대등하게 놓아야 한다.

---

## 3. 경쟁 가설과 서로 다른 예측

| | 가설 | 예측 (구별점) |
|---|---|---|
| **H1** | **tolerance 규모**: 실제 `e_j − e_{j−1}` 분포가 ±1 sample 보다 넓다 | 실패 비트의 **가장 가까운 후보가 2–5 sample 거리**에 존재한다. 실패가 **쌍으로** 발생한다(비트 j 의 post-RR = 비트 j+1 의 pre-RR). class 별로 V 가 오른쪽으로 이동한다 |
| **H2** | **상대의 부재**: 검출기가 그 비트를 아예 놓쳤다 | 가장 가까운 후보가 **없거나 매우 멀다**. 실패 수가 개수 결손과 같은 자릿수여야 한다 — **§2(b) 가 이미 반증에 가깝다**(25 대 6,648) |
| **H3** | **RR 의미 비대칭**: mamba 는 경계 필터 **후**·끝점 복제, V9/V10 은 경계 필터 **전**·끝점 `nan→0`. 한쪽만 버린 비트가 있으면 이웃의 RR 이 **한 박자 통째로** 달라진다 | 불일치가 1–5 sample 이 아니라 **RR 한 구간(수백 sample) 규모**다. 실패가 drop 지점 **이후로 이어지는 런**을 이룬다. 소규모 결손이 대규모 실패로 전파되는 유일한 후보 |
| **H4** | **단조 사슬 붕괴**: RR 이 정수로 양자화돼 동일 `(pre, post)` 쌍이 흔하면 후보 다중도가 커지고, forced-edge 인증이 거의 아무것도 확정하지 못한다 | `EDGE_IN_NO_MAXIMUM_MATCHING`(40.6%) + `AMBIGUOUS`(3.0%) 버킷에 집중된다. 실패 비트의 **후보 개수가 크다**. 심박이 안정된 구간일수록 나쁘다 |

**H3 과 H4 는 §2(b) 를 설명할 수 있고 H1·H2 는 그러지 못한다.** 그것만으로 순위를
매기지는 말되, 진단이 H3·H4 를 반드시 포함해야 한다는 근거로는 충분하다.

참고: 이미 확인된 계약 차이 — mamba 는 끝점 RR 을 **복제**하고 `feats[:,4]/[:,5]`
초 단위, V9/V10 `rr_features` 는 끝점을 `nan→0.0` 으로 두고 경계 필터 **이전**에
계산해 `rr[:,0]/[:,1]` 초 단위다. H3 은 이 확정된 사실 위에 서 있다.

---

## 4. 제안하는 측정 — **제안일 뿐이다. 채택·수정·기각은 Codex 가 한다**

### M0 — 실행 0. 기존 번들만으로 지금 낼 수 있다 [먼저 볼 것을 권함]

`unmatched_and_ambiguous.csv` 는 실패 24,341 건 전부에 대해 이미 다음을 담고 있다:
`record` · `raw_atr_ordinal` · `raw_r_sample` · `mamba_aami`(Leg 1 class) ·
`mamba_record_row` · `cache_record_row` · `drop_or_unmatched_reason` · `failed_leg`.

따라서 **새 실행 없이** 다음이 나온다:

- 실패의 **class 구성**을 원인 버킷별로 (mamba 측 12,183 행). V 가 `NO_EDGE` 에
  몰리면 H1/H2, `NOT_OPTIMAL` 에 몰리면 H4.
- record 208 의 실패가 정말 V 를 넘어서는지 **직접 확인** (§2(a) 의 산술 논증을
  실측으로 대체).
- `raw_r_sample` 로 record 내 **실패 위치 분포**와 **런 길이**. 흩어져 있으면 H1,
  긴 런이면 H3, 블록이면 H4.

한계: cache 측 12,158 행에는 class 가 없다(`mamba_aami: None`). 그쪽 class 는
processed 클래스 맵이 필요하므로 M0 로는 안 된다.

### M1 — 최근접 후보 거리 분포 [새 측정 필요]

인증되지 않은 각 cache 행에 대해, 국소 mamba 창(±W 행, W 는 사전등록) 안에서
`min over candidates of max(|Δpre|, |Δpost|)` 를 sample 단위로 계산해 분포를 낸다.
class · record · 층 · 원인 버킷별로 보고. 창 밖은 절단으로 표시.

→ H1(2–5 에 질량) 대 H2(비어 있음) 대 H3(수백 sample) 을 가른다.
**주의**: 이것은 "tolerance 를 k 로 하면 어떻게 되나"를 재는 것이 아니다. 분포를
보고하는 것이고, **그 분포로 새 tolerance 를 고르는 것은 금지다**(§5).

### M2 — 실패 인접성·런 길이 [M0 로 상당 부분 가능]

실패가 고립인지 런인지. V 비트가 실패했을 때 **바로 다음 비트도 실패했는지**.

→ H1 은 쌍, H3 은 drop 이후 런, H4 는 블록을 예측한다.

### M3 — 후보 다중도 [새 측정 필요]

각 cache 행의 후보 간선 수. 원인 버킷·class 별 분포.

→ 다중도가 크고 `NOT_OPTIMAL` 과 상관되면 H4.

### M4 — 116·208 의 결손 위치 대조 [새 측정 필요]

−14 와 −7 의 결손이 record 안 **어디에서** 발생하는지, 그리고 coverage 가 그
지점 **이후로** 붕괴하는지.

→ "작은 결손이 전파된다"(H3/H4) 대 "결손은 무관하다"를 직접 가른다. §2(b) 의
266 배를 설명할 수 있는 유일한 측정이다.

### M5 — 층 사이 대조

equal_count 17 record 안에서도 coverage 가 갈리는지(차트상 119·201·203·106 이
바닥). 갈린다면 "개수 불일치"는 원인이 아니라 **동반 증상**이다.

우선순위 제안: **M0 → M4 → M1 → M3**. M0 는 공짜이고, M4 는 가장 큰 미해명
(266 배)을 직접 겨눈다.

---

## 5. 절대 하지 말 것

- **tolerance 를 넓혀 coverage 가 오르는지 보는 것.** 결과를 본 뒤의 완화이며,
  이미 Decision log 에 "넓히지 않았다"로 기록돼 있다.
- **진단 측정으로 새 tolerance 를 고르는 것.** 새 규칙은 새 `rule_fingerprint`
  와 자기 null(3 family × 10,000)을 갖는 **별도 사전등록**이어야 하고, 임계값은
  그것이 만들어내는 coverage 와 **무관한 근거**로 정해져야 한다. 완화된 규칙이
  기존 null 의 컷오프를 물려받는 것은 `assert_null_matches_rule` 이 구조적으로
  막는다.
- **개수 불일치 record 5개를 빼고 다시 재는 것.** equal_count 층도 0.856 으로
  0.95 에 미달이다 — 빼도 규칙은 구제되지 않는다.
- **gate 재배열·재해석.** first-failure-wins 이고 첫 실패는 gate 3 이다. 더
  흥미로운 판정을 고르지 않는다.
- **DS2 per-beat label · V10 확률 · association · 학습.** 전부 봉인이다. 두 실행
  어디에서도 열지 않았고(`training_performed`·`model_scored`·
  `v10_probability_opened`·`association_performed` 전부 False) 진단도 열지 않는다.
- **기존 Drive 산출물 수정·삭제.** superseded 도 보존 대상이며 각각
  `SUPERSEDED.json` 을 달고 있다.

---

## 6. Codex 가 결정해야 할 것

1. **진단을 할 가치가 있는가.** "하지 않고 Q5-D 를 `JOIN_UNRESOLVED` 로 닫는다"도
   유효한 답이다. 그 경우 parent 경로(S PR-AUC association)에 무엇이 남는지 명시하라.
2. **M0 를 먼저 볼 것인가.** 실행 비용 0 이지만, 본 뒤에 진단을 설계하면 설계가
   결과에 오염될 수 있다. 사전등록 원칙과의 균형은 Codex 판단이다.
3. **§4 의 측정안 채택 여부와 정의.** 창 크기 W, 절단 규칙, 보고 층위.
4. **각 결과가 어느 가설을 지지/반증하는지 사전 등록.** 측정 후 해석을 맞추지
   않도록 먼저 적는다.
5. **진단의 중단 조건.** 무엇이 나오면 더 파지 않고 멈추는가.
6. **이 진단이 무엇을 licence 하지 않는지.** 특히 tolerance 와 gate.

---

## 7. 승인 경계 — 지금 상태

- Q5-D join 자체는 **실행 완료 · 판정 `JOIN_UNRESOLVED`**. 규칙은 반증되지도
  자격을 얻지도 않았다.
- 진단은 **아직 명세가 없다**. 설계 → 사용자 승인 → 구현 → 별도 실행 승인의
  기존 4단계가 그대로 적용된다.
- DS2 지지 gate 는 DS1 freeze + release token 이 필요한 별도 단계이고 **열리지
  않았다**.
- association 과 학습은 여전히 **승인되지 않았다**.

---

## 8. 근거 문서 위치

| 내용 | 파일 |
|---|---|
| 실측 결과·gate 표·전후 비교 | `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` Decision log |
| RR 계약 · 44-record 행 대장 | `research/HANDOFF_2026-08-10_Q5D_preflight_result_to_codex.md` |
| mamba 계보 | `research/PROVENANCE_2026-08-10_mamba_data_lineage.md` |
| 자산 등록 | `research/ASSETS.md` |
| 구현 | `mit-bih/q5d_order_preserving_beat_join.py` · `mit-bih/test_q5d_order_preserving_beat_join.py` |
| 실행 노트북 | `notebooks/quest54_q5d_order_preserving_beat_join.ipynb` |
| Drive 산출물 | `MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-007_q5d_beat_join_DS1_GATE/` (superseded 1건 포함, 각각 `SUPERSEDED.json`) |

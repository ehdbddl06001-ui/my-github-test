---
experiment_id: EXP-2026-006
stage_id: Q5-C
title: The shared error core — what do two lineages get wrong together?
status: approved_for_implementation
implementation_owner: claude-code
kind: preregistered_analysis_only
result_status: RESULT_NOT_RUN
run_id: null
measured: null
verdict: null
depends_on: EXP-2026-004
created: 2026-08-09
---

# EXP-2026-006 / Q5-C — 공유 실패 핵심

**상태: DESIGN / RESULT NOT RUN.** 이 문서·코드·notebook은 사전 등록이며 어떤
수치도 결과가 아니다.

## 0. 왜 이것인가

Q5-A는 `UNRESOLVED`(D5)로 끝나면서 **해석되지 않은 사실 하나**를 남겼다:
서로 다른 계보인 V10과 V9_BASE가 S beat 1,628개 중 **710개(43.6%)를 동시에**
틀린다. 그런데 같은 run에서 두 모델의 **worst 환자**는 거의 겹치지 않는다
(전 쌍 최소 overlap 0.333).

**환자 단위로는 지속되지 않는데 beat 단위로는 지속된다** — 이것은 Q5-A의 환자
블록이 서술하도록 만들어진 대상과 **다른 물건**이고, 아무도 들여다보지 않았다.

이 실험은 그것을 본다. 모델을 만들지 않고, 학습하지 않는다.

## 1. 시작 전에 바로잡는 두 가지

### (1) 43.6%는 설명해야 할 숫자가 아니다

그 수치는 **임계값 기반**이다 — Q5-A가 "prevalence-matched cut이 S beat의 2/3를
구조적으로 오류로 만든다"고 실측한 뒤 **강등한** 바로 그 정의다. 게다가 산수만으로
상당 부분이 설명된다:

| | |
|---|---|
| V10 오류율 | 0.528 |
| V9_BASE 오류율 | 0.551 |
| **독립이라면 공통 오류 기대치** | **0.291 (474박)** |
| 실제 | 0.436 (710박) |
| **초과** | **1.50배** |

즉 710박 중 **474박은 두 모델이 각자 나빠서 우연히 겹친 것**이다. 이름을 붙일
가치가 있는 것은 **초과분**이지 43.6%가 아니다.

### (2) record를 가로질러 beat를 비교하면 환자 효과가 다시 들어온다

Q5-A는 `B_PATIENT`가 1위 블록임을 이미 측정했다. beat를 record 경계 너머로
비교하면 그 효과가 그대로 섞여 들어온다. 그래서 이 실험의 **난이도는 record
안에서만 정의한다.**

## 2. 정의 (사전 등록)

- 각 record에 대해, 각 모델에 대해: 그 record의 **S beat들**을 Q5-A의 primary
  outcome(**within-record rank badness**)으로 정렬해 **나쁜 절반**을 그 모델의
  `hard`로 놓는다.
- 따라서 모델마다 record마다 정확히 절반이 `hard` 다 → **K개 모델 모두에서
  `hard` 일 우연 확률 = `0.5**K`**. K=4면 **0.0625**. 이 기준선은 적합(fitting)이
  아니라 구성상 참이다.
- `shared_hard` = 4개 모델 모두에서 hard · `shared_easy` = 4개 모두에서 easy ·
  나머지는 모델 특이적(비교에서 제외 — 양 극단만 대비한다).
- S beat가 `CORE_MIN_S_PER_RECORD = 8` 미만인 record는 "절반"이 의미 없으므로
  **제외**하고 제외 사실을 기록한다.
- 초과분의 신뢰구간은 **record(환자) bootstrap**으로 낸다. beat가 아니라 record가
  일반화 단위다. **점추정도 같은 추정량이어야 한다** — 보고하는 공유율은
  *record별 비중의 평균*(record-macro)이고, beat를 통합한 값은 그 옆에 함께
  적되 바꿔치기하지 않는다. 두 값 모두 독립 가정에서 기대치가 `0.5**K`라
  우연 기준선은 달라지지 않는다.

## 3. 무엇으로 설명을 시도하는가

**Q5-A가 이미 등록한 블록만 쓴다. 새 특징을 만들지 않는다.**

- `B_ATRIAL` · `B_RR` · `B_QUALITY`
- `B_SUBTYPE`은 **영구 종결**(EXP-2026-005)이므로 되살리지 않는다.
- `B_PATIENT`는 **일부러 뺀다** — 난이도를 이미 record 안에서 정의했으므로,
  환자 정체성 특징은 조건화로 제거된 변수를 설명하는 셈이 된다.

판별은 Q5-A의 **환자-grouped holdout** 기계를 그대로 쓴다: 일부 환자에서 적합하고
**남겨둔 환자에서 채점**한다. 적합에 쓴 beat로 채점하지 않는다.

## 4. 사전등록 decision tree

**D-C — `NO_SHARED_CORE`.** 초과분이 `EXCESS_MIN = 1.25` 미만이거나 환자
bootstrap CI 하한이 1.0을 넘지 못하면. → "공유 핵심"이라는 틀 자체를 폐기한다.
43.6%는 두 모델이 산수로 겹친 것이며 개입을 지목하지 않는다. **내가 이 실험을
제안하며 쓴 표현이 틀렸다는 판정이고, 그것도 결과다.**

**D-B — `SHARED_CORE_UNSTRUCTURED`.** 초과분은 실재하지만 등록된 블록이 환자
밖에서 판별하지 못하면(joint AUROC < `AUROC_MIN = 0.55` 또는 Δ의 CI 하한 ≤ 0
또는 셔플 대조군 실패, 또는 표본 부족). → **핵심은 실재하나 지금까지 측정한
무엇으로도 보이지 않는다.** 다음 단계는 **새 모델이 아니라 새 측정**(파형 수준)
이다. **맞을 때까지 특징을 넓혀 찾는 것을 금지한다.**

**D-A — `SHARED_CORE_STRUCTURED`.** 초과분이 실재하고 등록된 블록이 환자 밖에서
판별하며 셔플 대조군을 통과하면. → 후보 요인을 **지목**한다. **그러나 개입을
승인하지 않는다.** Q5-B는 여전히 별도 spec·단일 변수·음성대조군이 필요하다.

**`INSUFFICIENT_ARTIFACTS`** — 정렬된 예측을 못 얻으면.

`largest mean` 만으로는 아무것도 고르지 않는다. 서술용 특징 대비표
(`feature_contrast.csv`)는 **판정이 읽지 않는다**.

## 5. 음성대조군 (사전 등록)

- **셔플**: `shared_hard` 라벨을 **그 beat의 record 안에서** 섞는다. 진짜 구조라면
  판별력이 무너져야 한다(`SHUFFLE_MAX_RETAINED = 0.25`). 원래 Δ가 0 이하면
  "부술 것이 없음"으로 기록하고 판정을 만들어내지 않는다.
- **우연 기준선**: `0.5**K`는 대조군이자 D-C의 판정 기준이다.
- **집중도**: 두 가지를 **따로** 보고한다.
  ① **개수** 집중 — 핵심의 절반을 몇 개 record가 차지하는가. 이것은 *S beat가
  어디 있는가*를 따라갈 뿐이다. 한 record가 cohort S beat의 대부분을 갖고 있으면
  S beat 위에 정의된 무엇이든 그 record가 대부분을 갖는다.
  ② **비율** 균일성 — record마다 자기 S beat 중 핵심 비중이 비슷한가. **일반성을
  말해주는 것은 이쪽이다.** 개수만 읽으면 완벽히 균일한 효과를 "record 이야기"로
  오독한다. 보고서는 어느 줄을 읽어야 하는지 함께 적는다.

## 6. 허용 파일

- `mit-bih/q5c_shared_error_core.py`
- `mit-bih/test_q5c_shared_error_core.py`
- `notebooks/quest52_q5c_shared_error_core.ipynb`
- `experiments/specs/EXP-2026-006-q5c-shared-error-core.md`
- `research/ASSETS.md`
- `research/PROJECT_STATE.md`

**Q5-A·Q5-B-0 모듈은 수정하지 않는다.** cohort·freeze·정렬·outcome·블록·bootstrap은
전부 Q5-A의 것을 호출한다.

## 7. 저장 bundle

`runs/<ts>_EXP-2026-006_q5c_shared_error_core/` 에 `config.json` ·
`manifest.json` · `result.json` · `log.txt` · `core_membership.csv`(record별
핵심 비중) · `co_error_matrix.csv`(모델 쌍별) · `feature_contrast.csv`(서술용) ·
`decision.json` · `summary.md` · `figures/`(`co_error_excess` ·
`core_concentration` · `feature_contrast` · `core_decision`).
기존 폴더를 덮어쓰지 않는다.

## 8. 테스트 계약 (CPU; 학습·Drive 없음)

import 시 학습·Drive 접근 없음 · mode 정확히 하나 · **새 블록을 만들지 않음**
(`CORE_BLOCKS ⊆ Q5-A blocks`, `B_SUBTYPE`·`B_PATIENT` 제외 확인) · record별
정확한 중앙 분할 · S가 8박 미만인 record 제외 · **독립 모델은 우연 수준(CI가 1을
포함)**, 잠재 공유 모델은 초과 · 세 분기 모두 fixture로 도달 · 숨은 변수로 만든
핵심은 D-B(구조화로 승격되지 않음) · 셔플 대조군 · 표본 부족은 판정으로 기록 ·
bundle 스키마 · REPORT는 bundle을 쓰지 않음 · 언어 경계 문구 · **Q5-A 불변**.

## 9. 절대 금지 (사전 등록)

Q5-A/Q5-B-0의 금지 목록을 승계하고 셋을 더한다.

새 모델 학습 · 저장 확률 재생성 · residual CNN 재개 · INCART rescue ·
관찰 연관성을 인과로 승격 · P-wave proxy를 ground truth로 표현 · 기존 Drive 파일
덮어쓰기 · 결과 없이 MEASURED 표기 ·
**핵심을 설명하려고 새 특징을 만들어 넣기**(맞을 때까지 넓혀 찾기 금지) ·
**`B_SUBTYPE` 되살리기**(EXP-2026-005에서 종결) ·
**D-A가 나와도 그것만으로 Q5-B 개입을 시작하기.**

## 10. Q5-B-1 (여기서 만들지 않는다)

사용자와의 논의 기록: Q5-A의 사전등록 트리는 **patient-robust 분기를 선택하지
않았다**(D4 미발화 — worst quartile이 모델 간 비지속). 따라서 patient-CVaR pilot을
지금 돌리면 **트리가 고르지 않은 분기를 사람이 고르는 것**이 된다. Q5-C는 트리가
`UNRESOLVED`를 낸 바로 그 지점을 겨냥한 **측정**이며, 그 결과에 따라 Q5-B-1의
전제가 살아나거나 죽는다. **Q5-B-1의 spec·코드·학습 notebook은 이 브랜치에서
만들지 않는다.**

## Decision log

### 2026-08-09 — 집중도 지표 정정 + AUROC 영가설 추가 (deviation 기록 2; 판정 불변)

첫 실측에서 집중도가 "1개 record가 핵심의 80%"로 나와 내 사전등록 읽기 규칙대로면
"record 이야기"였다. 그런데 record별 표를 보면 **핵심 비율은 7개 record 전부에서
0.227–0.357**(우연 0.0625의 3.6–5.7배)로 **균일**했다. 개수가 한 record에 쏠린
이유는 그 record가 cohort **S beat의 86%** 를 갖고 있기 때문이지 현상이 거기
몰려서가 아니다.

즉 **내가 만든 집중도 지표가 개수만 재고 있었고, 그 규칙대로 읽으면 균일한 효과를
record 이야기로 오독한다.** 정정:

- 집중도를 **개수**와 **비율** 두 축으로 나눠 보고하고, record별 우연 대비 배수를
  표에 넣는다. 어느 줄을 읽어야 하는지 note에 적는다.
- 한 record가 S beat 대부분을 갖고 있어도 비율이 균일하면 record 이야기가 아님을
  fixture 테스트로 고정했다.
- **held-out AUROC에 라벨 셔플 영가설을 붙였다.** 없으면 0.73과 0.53이 지면에서
  같아 보인다. 셔플은 record 안에서 하므로 각 record의 핵심 비율은 보존된다.
- D-B 사유 문구가 "특징이 판별하지 못한다"라고 단정하던 것을 실제 값에 맞게
  고쳤다 — AUROC가 기준을 넘고 loss만 못 넘는 경우를 그렇게 쓰면 거짓이다.
- record가 하나도 분할 조건을 못 채우면 명시적 STOP(빈 배열 크래시 아님).

**판정 규칙은 하나도 바뀌지 않았다**(집중도는 분기가 읽지 않고, AUROC 기준·loss
기준·셔플 기준 모두 그대로). 모듈 v3.

### 2026-08-09 — 추정량 불일치 수정 (deviation 기록 1; 결과 없음)

첫 `ANALYZE` 실행이 그림 단계에서 `yerr must not contain negative values`로
멈췄다. 표면은 plotting 오류지만 원인은 **추정량 불일치**였다: 점추정은 beat를
통합한 평균인데 bootstrap은 *record별 평균의 평균*을 재고 있어서, 둘이 어긋나면
점추정이 자기 신뢰구간 밖으로 나간다. record 크기와 핵심 비중이 함께 움직이면
실제로 벌어지는 일이다.

수정(**결과를 보기 전에**; 크래시 지점이 그림 생성이라 어떤 수치도 저장되지
않았고 화면에도 나오지 않았다):

- 보고 공유율을 **record-macro**(bootstrap이 재표집하는 단위와 동일)로 통일하고,
  beat 통합값은 `observed_micro`로 **함께** 보고한다. 우연 기준선 `0.5**K`는
  두 추정량 모두에서 동일하므로 판정 기준은 바뀌지 않는다.
- 점추정이 자기 CI 안에 있음을 테스트로 고정했다.
- 그림은 구간이 점추정을 감싸지 않는 경우에도 그려지도록 방어한다 — **그림이
  측정 결과를 파괴할 수 없어야 한다**(이번에 실제로 파괴했다).

모듈 v2.

### 2026-08-09 — 설계 등록 (결과 없음)

Q5-B-0/0b가 `B_SUBTYPE`을 영구 종결한 뒤, 남은 선택지는 ① 트리가 고르지 않은
patient-CVaR pilot을 강행 ② Q5-A가 남긴 미해석 사실을 측정 ③ 종료 였다. 사용자가
②를 선택했다.

설계 중 가장 중요한 결정은 **설명 대상을 43.6%에서 "우연 초과분"으로 바꾼 것**이다.
43.6%를 그대로 물었다면 그 절반(474박)이 산수라는 사실을 놓친 채 "절반이 공통으로
틀린다"는 인상만 좇았을 것이다. 임계값 기반 정의를 within-record 중앙 분할로
바꾼 것도 같은 이유이며, 덤으로 우연 기준선이 `0.5**K`로 **계산 없이** 확정된다.

`B_PATIENT`를 블록에서 뺀 것도 사전 결정이다 — 난이도를 record 안에서 정의한
이상, 환자 특징으로 그것을 설명하는 것은 순환이다.

D-C(“공유 핵심 없음”)를 정식 분기로 넣었다. 이 실험을 제안한 것은 나이고, 내
표현이 틀렸다는 판정이 나올 통로를 트리에 미리 열어 두는 것이 맞다.

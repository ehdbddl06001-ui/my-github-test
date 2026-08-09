---
experiment_id: EXP-2026-005
stage_id: Q5-B-0
title: S-subtype key recovery for the Q5-A failure atlas
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

# EXP-2026-005 / Q5-B-0 — S 하위분류 키 복구

**상태: DESIGN / RESULT NOT RUN.** 이 문서·코드·notebook은 사전 등록이며 어떤
수치도 결과가 아니다. Colab에서 `RECOVER`(→ 통과 시 `REANALYZE`)를 실행하기
전까지 `result_status: RESULT_NOT_RUN`을 유지한다.

## 0. 왜 이것이 다음 실험인가

Q5-A(EXP-2026-004)는 사전등록 5개 블록 중 **4개만** 측정하고 `UNRESOLVED`(D5)로
끝났다. 다섯 번째 `B_SUBTYPE`은 점수조차 내지 못했다 — 동결 source의 시간열 `t`가
annotation sample index가 아니어서 `.atr` 조인이 **1.9%**(우연 수준)에 머물렀기
때문이다.

D5의 사전등록 next_step은 *"가장 저비용의 추가 측정 또는 artifact 보강"*이다.
따라서 다음 단계는 **모델이 아니라 측정**이다. 지금의 D5는 "근거가 없다"가 아니라
**"근거가 한 칸 비어 있고 나머지는 서로 비슷하다"** 이므로, 그 한 칸을 채우는 것이
가장 싸게 판정을 바꿀 수 있는 수다.

- 학습하지 않는다. 저장 확률을 다시 만들지 않는다. GPU가 필요 없다.
- 실패하면 `B_SUBTYPE`을 **영구 미측정**으로 종결한다. 그것도 결과다.
- 이 실험은 Q5-B **개입 실험이 아니다.** 개입(Q5-B-1)은 별도 승인 대상이다.

## 1. 언어 경계 (Q5-A에서 그대로 승계)

- 여기서 말할 수 있는 것은 `failure-associated factor`(**실패 연관 요인**)까지다.
  `원인`은 요인 하나만 바꾸는 개입과 음성대조군으로만 검증한다.
- P-wave proxy를 P-wave ground truth로 표현하지 않는다.
- residual CNN 경로는 closed이며 재개하거나 변형을 제안하지 않는다. INCART
  rescue run도 하지 않는다.

## 2. 고정된 질문

> 동결 atlas cohort(`mamba_data.npz`)의 **S beat**에 원 annotation symbol
> (A/a/J/S)을 **재학습 없이** 되붙일 수 있는가? 붙일 수 있다면 `B_SUBTYPE`을
> 포함해 Q5-A decision tree를 다시 평가한다.

방법은 고정하지 않는다. 고정하는 것은 **무엇을 만족해야 믿는가**(6절 gate)다.

## 3. 허용 파일 (이 브랜치의 변경 파일 전부)

- `mit-bih/q5b0_subtype_key_recovery.py`
- `mit-bih/test_q5b0_subtype_key_recovery.py`
- `notebooks/quest51_q5b0_subtype_key_recovery.ipynb`
- `experiments/specs/EXP-2026-005-q5b0-subtype-key-recovery.md`
- `research/ASSETS.md`
- `research/PROJECT_STATE.md`

**Q5-A의 코드(`mit-bih/q5a_patient_failure_atlas.py`)는 수정하지 않는다.**
재분석은 Q5-A의 `run_atlas`를 **그대로 호출**한다 — decision tree·블록 규칙·
임계값은 Q5-A가 측정되기 전에 등록된 그 값이며, 달라지는 것은 `B_SUBTYPE`에
데이터가 생겼다는 사실 하나뿐이다.

## 4. 입력

| 역할 | 파일 | 쓰는 것 |
|---|---|---|
| 동결 atlas cohort | `MyDrive/mitbih/mamba_data.npz` (id `1p3HvC…`) | `pid`·`y`·`t`(검증된 초 단위) → RR |
| symbol source | `MyDrive/mitbih/ecg_multi.npz` (id `1aSj_1j…`) | `pid`·`db`·`y5`·**`sym`**·`pre_rr`·`post_rr` |

`ecg_multi.npz`의 waveform(`beat`)은 **읽지 않는다**(파일 대부분이 그것이고 키에
필요 없다). 기존 Drive 파일·run bundle은 덮어쓰지 않는다.

선행 근거: Q4-Q PREP_DATA(run `20260808T1838`)가 두 파일의 MIT subset을 5-class
지문으로 대조해 **record 동일성**과 **S 총계 일치**를 이미 실측했다. 이 실험은 그
record 수준 대응을 **beat 수준**으로 내리는 작업이다.

## 5. 조인 방법 (사전 등록)

- **범위**: S beat만. `B_SUBTYPE`이 읽는 유일한 행이고, 양쪽 pool을 같은 class로
  좁혀야 배정이 작고 정확해진다.
- **키**: `(pre_rr, post_rr)` 초 단위. 두 파일 모두 같은 annotation sample에서
  RR을 계산하므로 참인 쌍은 sample 단위로 일치해야 한다. RR 단위는 사용 전에
  **검증**한다(초/샘플 중 정확히 하나만 생리학적 범위에 들어야 하며, 아니면 중단).
- **이웃 좌표를 쓰지 않는다.** 앞뒤 beat의 RR을 키에 넣으면 행 순서를 바꿨을 때
  키가 변한다 → "pool을 뒤섞어도 같은 결과"라는 유일하게 정직한 비-위치매칭
  증명이 원천적으로 불가능해진다. 키는 beat 자신의 성질만으로 만든다.
- **배정**: record별 전역 최적 1:1 배정. 채택 규칙 두 가지 —
  ① 비용 ≤ `RR_TOLERANCE_S = 0.005`s(360 Hz에서 1.8 sample),
  ② 차점 후보가 `RR_MARGIN_S = 0.005`s 이상 나쁠 것.
  ②를 못 채우면 **모호(ambiguous)** 로 세고 **매칭하지 않는다**. 첫 후보나 낮은
  인덱스를 고르는 식의 해소는 하지 않는다.
- **symbol은 매칭에 절대 쓰지 않는다.** 그래서 "매칭된 beat의 symbol이 AAMI S
  집합에 드는가"가 **독립 검증**이 된다(매처가 손댈 수 없는 값이다).
- **순서 기반 보충(ordinal fill)**: 모호해서 남은 beat는, 그 record의 **내용으로
  맞춘 anchor들이 정확히 ordinal 대응임을 실측으로 보였을 때에만**(그리고 anchor가
  그 record S beat의 50% 이상일 때에만) 순서로 채운다. 채운 개수는 따로 세고,
  채운 beat도 위의 symbol 검증을 함께 통과해야 한다. **가정이 아니라 검정이다.**

## 6. 사전등록 GO / NO-GO gate

| 검사 | 기준 |
|---|---|
| `s_match_fraction` | ≥ **0.95** |
| `records_at_or_above_record_floor` | record별 ≥ 0.90 을 만족하는 record가 ≥ 0.90 |
| `content_anchor_fraction` | ≥ 0.50 (키만으로 식별된 비율) |
| `ordinal_mapping_exact_where_used` | 순서 보충을 썼다면 ordinal 일치 = 1.0 |
| `symbol_in_aami_s_set` | ≥ **0.99** — 매처가 못 보는 값이므로 독립 검증 |
| `per_record_s_count_diff` | ≤ 10 (Q4-Q의 S 예산 그대로) |
| `permutation_invariance` | anchor가 **한 개도** 달라지지 않을 것 |
| `shift_control` | ≤ 0.20 |
| `wrong_record_control` | ≤ 0.05 |
| `signal_to_null_ratio` | ≥ 5.0 |
| `subtypes_present` | > 0 |

하나라도 실패하면 `NO_GO_SUBTYPE_CLOSED`. 그러면 symbols를 붙이지 않고 재분석도
돌리지 않는다. **없는 것을 추정으로 채우지 않고, 이것을 만들려고 재학습하지
않는다.** Q5-A의 `UNRESOLVED`(D5)는 4개 블록 위에서 그대로 유지된다.

### 음성대조군 (사전 등록)

1. **permutation** — symbol source의 행을 무작위로 섞고 다시 조인한다. 키가
   order-free이므로 content anchor는 **한 개도** 달라지면 안 된다. 순서 보충은
   설계상 순서 기반이므로 이 검사의 **범위 밖**이고, 대신 ordinal 검정과
   chronology chain으로 따로 정당화한다(그 경계를 코드와 보고서에 명시한다).
2. **shift** — cohort의 k번째 S beat를 source의 k+1번째와 짝지어 본다. 이
   **일부러 틀린** 대응이 tolerance 안에 들어오는 비율이 높다면 tolerance가 너무
   느슨해 아무것도 식별하지 못한다는 뜻이다.
3. **wrong-record** — 다른 record의 pool에서 찾는다. 여기서의 모든 매칭은 정의상
   거짓이므로 이 비율은 **조인 오매칭률의 상한**이다(실제 조인에서는 참 파트너가
   있어 배정에서 이긴다).
4. **shuffle (재분석 단계)** — 복구한 symbol을 record 안에서 섞어 `B_SUBTYPE`을
   다시 채점한다. 진짜 subtype 효과라면 무너져야 한다. 단, 원래 증분가치가 0 이하면
   **부술 효과가 없으므로 `not applicable`** 로 기록한다 — 잡음 두 개를 나눠
   판정을 만들어내지 않는다.

## 7. 중단 조건 (하나라도 발생 시 REANALYZE 금지, 보고)

- symbol source에 `sym`·RR·label 중 하나라도 없다
- RR 단위가 초/샘플 어느 쪽으로도 확정되지 않는다
- gate가 `NO_GO_SUBTYPE_CLOSED`
- 원본 bundle을 덮어써야만 진행 가능
- Q5-A 모듈을 고쳐야만 진행 가능(그러면 그것은 Q5-A 재개정이지 이 실험이 아니다)

## 8. 저장 bundle 계약

`RECOVER`: `runs/<ts>_EXP-2026-005_q5b0_subtype_key_recovery/` 에
`config.json` · `manifest.json` · `result.json` · `log.txt` ·
`recovery_audit.csv`(record별 매칭·모호·잔차·복구 symbol) ·
`recovery_controls.json` · `decision.json`(gate) · `summary.md` · `figures/`
(`recovery_gate_dashboard` · `rr_residual_hist` · `subtype_counts`).
**GO든 NO-GO든 전체 bundle을 쓴다.**

`REANALYZE`(GO일 때만): `runs/<ts>_EXP-2026-005_q5b0_subtype_reanalysis/` 에
**Q5-A의 17-file 계약 그대로** + `q5b0_recovery.json`(gate·대조군·복구 요약·
활성화된 블록 목록). 이 bundle의 `config.json`은 Q5-A 코드가 쓰므로 내부적으로
`EXP-2026-004`로 표기된다 — 재분석의 주체가 Q5-A의 atlas이기 때문이며,
`EXP-2026-005`는 다섯 번째 블록을 측정 가능하게 만든 **복구**를 가리킨다. 이
표기 관계를 `manifest.json`과 `q5b0_recovery.json`에 명시한다.

## 9. 재분석 후의 판정 규칙

Q5-A의 D0–D5를 **그대로** 다시 적용한다. 새 규칙을 만들지 않는다.

- `B_SUBTYPE`은 Q5-A에서 이미 **개입 분기가 없는 서술 블록**으로 등록돼 있다.
  따라서 `B_SUBTYPE`이 이겨도 자동으로 모델 실험이 되지 않고 D5(`descriptive
  block; it names no single manipulable variable`)로 간다. 이는 결과를 보고 만든
  규칙이 아니라 Q5-A에 이미 있던 규칙이다.
- 다른 블록이 자격을 얻으면 해당 분기(D1–D3)로, 아니면 D4/D5로 간다.
- 어떤 경우에도 두 가설을 한 모델에 동시에 넣지 않는다.

## 10. 테스트 계약 (CPU; 학습·Drive 없음)

`mit-bih/test_q5b0_subtype_key_recovery.py`가 검증한다: import 시 학습·Drive
접근 없음 · mode 정확히 하나 · symbol/RR/label 누락 시 hard fail · RR 단위 검증 ·
키가 order-free · tolerance/margin/1:1 규칙 · **충실한 source는 GO, 무관한
source는 NO-GO** · symbol을 전부 바꿔도 매칭 대상이 안 변함 · 대조군이 실제로
실패할 수 있음(구별 불가능한 beat는 shift control에서 탈락) · ordinal 보충은
anchor가 허락할 때만 · NO-GO면 attach·재분석 모두 거부 · GO/NO-GO 양쪽 bundle
스키마 · REPORT는 bundle을 쓰지 않음 · 재분석이 5개 블록을 채점하고 Q5-A의
17-file 계약을 지킴 · shuffle control이 심어둔 효과와 잡음을 구분함 · 언어 경계
문구 · **Q5-A 모듈이 그대로임**(v8, 임계값 불변).

## 11. 절대 금지 (사전 등록)

Q5-A의 금지 목록을 그대로 승계하고 두 가지를 더한다.

residual CNN 재개·변형 · 새 모델 학습 · 저장 확률 재생성 · artifact가 없다는
이유로 재학습 · DS2를 보고 임계값·규칙 수정 · INCART rescue run · P-wave proxy를
ground truth로 표현 · 관찰 연관성을 인과로 승격 · 두 가설을 한 모델에 투입 ·
기존 Drive 파일 덮어쓰기 · 결과 없이 MEASURED 표기 ·
**gate를 통과하지 못한 조인으로 symbol을 붙이기** ·
**사용자 승인 없이 Q5-B-1(개입 pilot)을 구현하거나 학습을 실행하기.**

## 12. Q5-B-1 (다음 후보 — 여기서 만들지 않는다)

이 실험이 끝난 뒤에도 자격 블록이 없고 `B_PATIENT`가 계속 1위라면, 다음 후보는
**objective 하나만** 바꾸는 DS1-only patient-CVaR pilot이다(architecture·입력·
전처리·seed·epoch 예산은 V10 그대로 동결, 음성대조군은 환자 라벨을 섞은 CVaR과
같은 계산량의 ERM 재실행). **그 spec·코드·학습 notebook은 이 브랜치에서 만들지
않는다.** 사용자 인수와 분기 승인이 먼저다.

## Decision log

### 2026-08-09 — record 동일성을 **가정에서 확립으로** (deviation 기록 1; 결과 없음)

첫 `RECOVER` 실행이 `Q5B0Error: no mitdb rows for records (100, 101, 103, …)`
로 중단됐다. 원인은 내 loader가 `ecg_multi.npz`의 `pid`를 MIT record 번호라고
**가정**하고 100–234로 필터한 것이다. Q4-Q PREP_DATA는 이미 그 반대를 실측해
뒀다 — 그 파일의 id는 ordinal일 수 있고, 그래서 Q4-Q는 id 동일성이 아니라
**5-class 지문 배정**으로 record를 짝지었다. 나는 그 결론을 코드에 반영하지
않았다.

수정(측정 전):

- db 필터만 적용하고 record 번호로는 거르지 않는다. id coding(`record_numbers` /
  `ordinal_or_other`)을 실측해 로그와 result에 남긴다.
- `resolve_record_mapping()`: ① id가 record 번호로 보이면 **먼저 검증한다** —
  per-record S 개수가 Q4-Q와 같은 예산(≤10) 안에서 일치할 때만 identity를 받아
  들인다. ② 아니면 Q4-Q의 `_fingerprint_match`(gate가 이미 통과한 그 코드)로
  배정한다.
- 매핑이 불가능하면 **예외가 아니라 NO-GO**다: 빈 recovery + 전체 bundle을 쓰고
  `record_identity_resolved` gate 검사에서 떨어진다. 근거 없이 멈추지 않는다.
- gate에 `record_identity_resolved` 항목을 추가했다(방법과 근거를 함께 기록).

임계값·조인 규칙은 하나도 바꾸지 않았다. 바뀐 것은 "record가 서로 같다"는 것을
**가정하지 않고 확립한다**는 점뿐이며, 이는 원 프롬프트의 "단순 array position /
row order 매칭 금지"와 같은 원칙의 record 판이다. 모듈 v2.

### 2026-08-09 — 설계 등록 (결과 없음)

Q5-A가 `UNRESOLVED`(D5)로 인수됐고, 사용자가 "Q5-B로 넘어간다"를 승인했다.
승인 시점에 제시된 권고 순서는 ① Q5-B-0(측정) ② 조건부 Q5-B-1(개입)이었고, 이
문서는 ①의 사전 등록이다.

설계 중 두 번, 코드가 스스로 설계 결함을 드러내 **측정 전에** 고쳤다. 둘 다
기록한다.

1. **이웃 RR을 키에서 뺐다.** 처음에는 `(pre, post, prev_pre, next_post)` 4좌표
   키를 등록했다. 합성 fixture에서 permutation 대조군이 즉시 실패했고, 이유는
   버그가 아니라 설계였다 — 이웃 좌표는 행 순서에 의존하므로 "pool을 섞어도 같은
   결과"가 성립할 수 없다. 키를 beat 자신의 `(pre, post)`로 줄이고, 잃은 식별력은
   1:1 배정 + margin + (검정된) ordinal 보충으로 되찾았다.
2. **`wrong_record` 임계값을 0.01 → 0.05 + 비율 5배로 바꿨다.** 0.01은 근거 없이
   고른 숫자였다. 이 대조군은 정의상 전부 거짓 매칭이므로 **오매칭률의 상한**이고,
   실제 조인은 참 파트너가 있어 더 낮다. 그래서 절대 상한(subtype 집계가 견딜 수
   있는 수준)과 신호/영가설 비율을 함께 요구하는 형태로 바꿨다. 두 값 모두 **실제
   데이터를 보기 전에** 정했다.

`shift` 대조군의 정의도 같은 이유로 바뀌었다: order-free 키에서는 pool을 굴리는
것이 permutation과 구별되지 않으므로, "**대응 자체가 한 칸 밀렸을 때** tolerance
안에 들어오는가"를 재는 형태로 등록했다.

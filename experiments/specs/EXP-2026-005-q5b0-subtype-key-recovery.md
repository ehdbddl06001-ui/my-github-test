---
experiment_id: EXP-2026-005
stage_id: Q5-B-0
title: S-subtype key recovery for the Q5-A failure atlas
status: measured_pending_acceptance
implementation_owner: claude-code
kind: preregistered_analysis_only
result_status: MEASURED
run_id: 20260809T1156_EXP-2026-005_q5b0_subtype_key_recovery
measured: 2026-08-09
verdict: NO_GO_SUBTYPE_CLOSED
depends_on: EXP-2026-004
created: 2026-08-09
---

# EXP-2026-005 / Q5-B-0 — S 하위분류 키 복구

**상태: MEASURED (2026-08-09).** 사전등록 gate 판정은 **`NO_GO_SUBTYPE_CLOSED`**
이고 근거 bundle은 `runs/20260809T1156_EXP-2026-005_q5b0_subtype_key_recovery`
다. 0~12절은 **측정 전에 등록된 설계 원문**이며 결과를 보고 고치지 않았다.
실측 결과는 「결과」 절에 따로 적는다. `REANALYZE`는 실행하지 않았다(gate가
막았고, 그것이 설계대로다).

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

## 결과 (2026-08-09 실측 · MEASURED)

run `20260809T1156_EXP-2026-005_q5b0_subtype_key_recovery` · 모듈 q5b0 v2 ·
`training_performed: false` · 31.4 s.

### 판정: `NO_GO_SUBTYPE_CLOSED`

| 검사 | 값 | 기준 | |
|---|---|---|---|
| `record_identity_resolved` | fingerprint_assignment | 확립될 것 | PASS |
| `s_match_fraction` | **0.2593** | ≥ 0.95 | **FAIL** |
| `records_at_or_above_record_floor` | 18/32 (0.56) | ≥ 0.90 | **FAIL** |
| `content_anchor_fraction` | **0.1981** | ≥ 0.50 | **FAIL** |
| `ordinal_mapping_exact_where_used` | 0.8846 | = 1.0 | **FAIL**(아래 정정) |
| `symbol_in_aami_s_set` | **1.0000** | ≥ 0.99 | PASS |
| `per_record_s_count_diff` | **0** | ≤ 10 | PASS |
| `permutation_invariance` | 0 differing | 0 | PASS |
| `shift_control` | 0.0426 | ≤ 0.20 | PASS |
| `wrong_record_control` | 0.0048 | ≤ 0.05 | PASS |
| `signal_to_null_ratio` | 54.42 | ≥ 5.0 | PASS |
| `subtypes_present` | 721 | > 0 | PASS |

따라서 **`B_SUBTYPE`은 이 사전등록 아래에서 종결**이고, Q5-A의 `UNRESOLVED`(D5)는
4개 블록 위에서 그대로 유지된다. symbols를 붙이지 않았고 재분석도 돌리지 않았다.
26%만 붙은 상태로 부분 사용하는 것도 하지 않는다 — 붙은 26%는 *RR이 일치한다는
조건으로 선택된 부분집합*이라 그 자체가 선택 편향이다.

### 붙은 것은 거의 확실히 옳다 — 그런데도 NO-GO다

이 둘은 모순이 아니라 이 실험의 핵심 관찰이다.

- 매칭된 721박의 symbol이 **100% A/a/J/S**(matcher가 볼 수 없는 값) ·
  wrong-record 영가설 0.48% · 신호/영가설 **54배** · 매칭 잔차 median
  **1.4 ms**, p95 4.2 ms.
- 복구된 분포도 임상적으로 말이 된다: **A 627 · a 32 · J 61 · S 1**(APB 우세).
- record 동일성은 5-class 지문 배정으로 44개 전부 확립됐고 leftover 4개는 paced
  record(102·104·107·217)다. **per-record S 개수 불일치 0**, 즉 두 파일은
  **같은 S beat 집합을 담고 있다**.
- 두 파일 모두 RR 체인이 완전히 시간순이다(`chronology_min = 1.0`).
- `ecg_multi`의 RR 단위는 **samples**(median 268 = 0.744 s)로 검증돼 초로 환산됐다.

즉 "다른 파일이라 못 붙였다"가 아니다. 같은 beat 집합인데 **80%의 beat에서 RR
값이 5 ms 안에 들어오지 않는다.**

### 기전: 첫 가설은 **크기가 맞지 않아 철회**했다

처음 세운 설명은 "mamba 전처리가 beat를 버려서, 앞 beat가 버려진 beat는 파생
`pre_rr`이 구멍을 건너뛰어 한 박자만큼 커진다"였다. 산수를 해보면 성립하지
않는다:

| | |
|---|---|
| ecg_multi(44 record) | 100,689박 |
| atlas cohort | 99,871박 |
| cohort에 없는 beat | **818박 = 0.81%** (그중 90%가 208·213) |
| 나머지 42 record 합계 | **82박** |
| 이웃 소실로 RR이 오염될 수 있는 생존 beat **상한** (= 2×drop) | **1.64%** |
| 실제 매칭 실패 | **74.1%** |

1.6% 상한으로 74%를 설명할 수 없다 — **45배 차이다.** 이 가설은 철회한다.

다만 이 계산에서 Q5-A에 중요한 사실 하나가 확정된다: **버려진 beat 중 S는
0박이다**(per-record S 불일치 0). 즉 Q5-A는 걸러진 S 집단을 채점한 것이 아니다.
v4는 이 drop map(record별·클래스별)을 `record_mapping.csv`로 bundle에 남긴다 —
지금까지는 배정 표를 계산하고도 버리고 있었다.

**남은 후보(미확인)** — v3/v4 진단이 가른다:

1. **검출 위치 지터**: cohort의 `t`가 annotation 위치가 아니라 **검출된 R-peak**
   위치라면(Q5-A가 `.atr` 조인 1.9%로 이미 `t` ≠ annotation sample을 보였다),
   RR 차이는 beat마다 수~수십 ms로 흩어진다. 그러면 5 ms 안에 드는 것은 소수뿐이고
   그 소수는 정확히 맞는다 — 관측(26%가 1.4 ms)과 잘 맞는다.
2. **이웃 소실**: 위에서 철회됐지만 208·213에 국한해서는 여전히 유효할 수 있다.
3. **RR로는 식별 불가**: 차이가 RR 전 범위에 균일.

판별 기준(측정 전에 명시): 못 붙인 beat의 **최근접 후보 거리**가
0.005~0.05 s 대에 퍼져 있으면 ①, 0.5~1.5 s 대(한 박자)면 ②, 균일하면 ③.
**ordinal 탐침**의 record 내 IQR이 수십 ms면 ①, 0에 가까운 상수 편차면 시간축
차이다.

진단은 gate를 바꾸지 않는다 — 판정은 이미 NO-GO다.

### 진단 실측 (run `20260809T1219`, 모듈 v4) — 답은 ①②③ 어느 것도 아니다

내가 미리 적어 둔 세 후보가 **전부 틀렸다.** 실측:

| 못 붙인 S beat 2,230박의 최근접 후보 거리 | |
|---|---|
| p10 | **0.00 ms** |
| p50 | **0.10 ms** |
| p90 | 6.90 ms |
| 허용치(5 ms)의 2배 안 | **93.8%** |

**못 붙인 beat들은 멀리 있지 않다 — 사실상 정확히 맞는 후보가 있다.**
거리 때문에 탈락한 것이 아니라 **margin 규칙 때문에 탈락했다.** 즉 최적 후보와
차점 후보가 5 ms 안에 함께 들어와서 "모호"로 분류되고 매칭이 거부된 것이다.

원인은 분해능이다. 360 Hz에서 1 sample = **2.78 ms** 이고 RR은 sample 단위로
양자화된다. 두 좌표 평균 위에서 5 ms margin은 **차점이 약 3.6 sample 이상 떨어질
것**을 요구하는데, 한 record 안에서 S beat의 coupling interval이 반복되면(이단맥
등) 그 요구를 만족할 수 없다. **내가 고른 margin이 데이터의 분해능에 비해 과했다.**

즉 이번 NO-GO는 "산출물이 조인을 지탱하지 못한다"가 아니라 **"내 규칙이 조인을
거부했다"** 이다. 판정은 그대로 유효하다(사전등록된 규칙 아래에서 측정된 결과다).
다만 종결의 성격이 다르다 — **영구 종결이 아니라 규칙 재설계 대상**이다.

### 같은 run에서 나온 별개의 확정: 버려진 818박은 **F(융합박)** 다

| 클래스 | N | S | V | **F** | Q |
|---|---|---|---|---|---|
| cohort에 없는 beat | 1 | **0** | 0 | **802** | 15 |

- **S와 V는 한 박도 버려지지 않았다.** Q5-A는 걸러진 S 집단을 채점한 것이 아니다.
- 버려진 것은 사실상 **융합박(F) 전량**이다. 즉 `mamba_data.npz`는 실질적으로
  F가 없는 데이터다.
- 최다 record는 208(374박)·213(362박)으로, **F 누락의 92%가 이 두 record에
  몰려 있다.** Q4-Q가 "stricter mamba preprocessing"이라며 미해명으로 남겨 둔
  208 −12.7% / 213 −11.1% 결손이 **이것으로 설명된다** — 두 record는 MIT-BIH에서
  융합박이 가장 많은 record다.
- Q5-A에 미치는 영향: S PR-AUC의 음성 pool에서 802박(약 0.8%)이 빠져 있다.
  작지만 인용 시 명시할 사실이며, 이제 `record_mapping.csv`에 record별로 남는다.

### 판정을 바꾸지 않는 결함 정정 1건

`ordinal_mapping_exact_where_used`는 이름과 달리 **모든 record**의 ordinal
일치도 최솟값으로 판정하고 있었다. 보충이 올바르게 발동하지 **않은** record까지
세는 셈이라, 검사가 주장하는 규칙("보충한 곳에서")보다 엄격했다. v3에서 보충이
실제로 일어난 record에 대해서만 판정하도록 고쳤다(`ordinal_consistency_min_
where_used`).

**이 정정으로 판정은 바뀌지 않는다**: `s_match_fraction` 0.2593과
`content_anchor_fraction` 0.1981이 기준에 크게 못 미쳐 단독으로 NO-GO다. 결과를
보고 유리하게 고친 것이 아님을 분명히 해 둔다.

### 다음: Q5-B-0b 제안 (승인 필요 — 여기서 구현하지 않음)

진단이 가리키는 것은 "산출물이 부족하다"가 아니라 **"동일성을 못 가리는 것과
답을 못 정하는 것을 내가 혼동했다"** 이다. 두 후보가 구별되지 않아도, **그 후보들이
같은 symbol을 갖고 있다면 답은 정해진다.** 참 파트너는 비용 ≈ 0으로 반드시 그
동점 집합 안에 있으므로(93.8%가 허용치 2배 안), 집합 전체가 한 symbol이면 어느
것을 골라도 결과가 같다. **이것은 추측이 아니라 추론이다.**

Q5-B-0b의 사전등록안:

- **규칙 변경 1개만**: 동점 집합(`best` + margin 안의 모든 후보)이 **한 symbol로
  일치하면** 그 symbol을 부여한다. 불일치하면 지금처럼 미매칭으로 남긴다.
  거리 tolerance·record 매핑·나머지 대조군은 **그대로 둔다.**
- **새 gate 항목 2개**(둘 다 통과해야 한다):
  1. `tie_set_symbol_agreement` — 동점 집합이 한 symbol로 일치한 비율. 이 값이
     낮으면 규칙 자체가 무의미하다.
  2. `subtype_distribution_agreement` — **ecg_multi가 record별 참 A/a/J/S 개수를
     알고 있으므로**, 복구된 분포가 그 참 분포를 재현하는지 검사한다. 흔한 A만
     회수하고 드문 a/J를 놓치면 블록이 편향되는데, 이 검사가 그것을 잡는다.
- **영가설을 같은 규칙으로 다시 계산한다** — wrong-record 대조군에도 동점-일치
  규칙을 적용해 오매칭률 상한을 재산출하고, 기존 gate(≤0.05, 비율 ≥5)를 **새 규칙
  아래에서 다시** 통과해야 한다. 규칙을 느슨하게 하면 영가설이 올라가므로 이것이
  "결과 보고 튜닝"과 가르는 선이다.
- 통과하지 못하면 `B_SUBTYPE`은 그때 **영구 종결**이다.

이번 NO-GO 판정은 철회하지 않는다. Q5-B-0b는 같은 질문에 대한 **별개의 사전
등록**이며, 자기 gate로 판정받는다. Q5-A의 판정은 4개 블록 위에서 유지되고,
Q5-B-1(개입 pilot)은 여전히 별도 승인 대상이다.

## Q5-B-0b 사전 등록 (2026-08-09 승인 · RESULT NOT RUN)

**이것은 Q5-B-0의 수정이 아니라 별개의 사전 등록이다.** Q5-B-0의
`NO_GO_SUBTYPE_CLOSED`(run `20260809T1219`)는 철회하지 않으며 그대로 재현
가능하다(모듈 기본값은 여전히 `strict_identity`). Q5-B-0b는 같은 질문을 다른
규칙으로 다시 묻고, **자기 gate로 판정받는다.**

### 왜 다시 묻는가

진단이 보여준 것은 산출물의 부족이 아니라 내 규칙의 과잉이었다. 못 붙인 beat의
93.8%가 허용치 2배 안에 정확한 후보를 갖고 있었고, 탈락 사유는 거리(tolerance)가
아니라 **차점이 너무 가깝다는 것(margin)** 이었다. 여기서 내가 혼동한 것이 있다:

> **어느 beat인지 못 가리는 것**과 **그 beat의 symbol을 못 정하는 것은 다르다.**

참 파트너는 비용 ≈ 0이므로 반드시 동점 집합 안에 있다. 그 집합의 구성원이 **모두
같은 symbol**을 갖고 있다면, 어느 것을 골라도 symbol은 같다. 이것은 추측이 아니라
추론이다.

### 규칙 (변경 1개)

- 엄격 규칙이 남긴 beat에 대해서만: 최적 비용이 tolerance 안이고 **동점 집합
  (`best` + margin 이내 후보 전부)이 한 symbol로 일치하면** 그 symbol을 부여한다.
  불일치하면 미매칭으로 남긴다.
- **1:1 제약은 이 beat들에 적용하지 않는다.** 동일성을 주장하지 않고 symbol만
  읽기 때문이다. 이 완화를 숨기지 않고 명시하며, 그 대가는 아래 gate가 받는다.
- tolerance(0.005 s) · margin(0.005 s) · record 매핑 · 나머지 대조군은 **그대로**.

### 추가 gate (둘 다 통과해야 한다)

| 검사 | 기준 | 무엇을 막나 |
|---|---|---|
| `tie_set_symbol_agreement` | 모호가 있으면 > 0 | 규칙이 무의미하게 아무것도 못 풀면 탈락 |
| `subtype_coverage_balance` | 최저 subtype 회수율 / 전체 회수율 ≥ **0.80** | **A만 회수하고 a/J를 놓치는 편향** |

`subtype_coverage_balance`가 핵심이다. symbol source는 record별 **참** A/a/J/S
개수를 알고 있으므로 편향을 직접 잴 수 있다. 흔한 A는 동점 집합이 전부 A라 잘
풀리고 드문 a/J는 혼합 집합에 갇혀 안 풀리면, 블록은 "S 하위분류"가 아니라 "A인가
아닌가"를 재게 된다. 20박 미만 subtype은 서술용으로만 보고하고 판정에 넣지 않는다.

### 영가설을 같은 규칙으로 다시 계산한다

`wrong_record_control`에도 동점-일치 규칙을 적용한다. 규칙을 느슨하게 하면 다른
record의 pool에서도 우연히 한 symbol로 일치하는 집합이 늘어나므로(특히 A 우세
때문에) **오매칭률 상한은 반드시 올라간다.** 그런데도 기존 기준(≤ 0.05, 신호/영
가설 ≥ 5)을 **새 규칙 아래에서** 통과해야 한다. 이것이 이 재등록을 "결과 보고
튜닝"과 가르는 선이다.

### 판정

- 전 항목 통과 → `GO`: symbols를 붙이고 Q5-A의 `run_atlas`를 **수정 없이** 재실행.
- 하나라도 실패 → `NO_GO_SUBTYPE_CLOSED`. 그때 `B_SUBTYPE`은 **영구 종결**이다.
  세 번째 규칙을 만들지 않는다.

### 실행

`notebooks/quest51_q5b0_subtype_key_recovery.ipynb` 의 `TIE_MODE`를
`"tie_symbol_agreement"` 로 두고 `RECOVER`. bundle은
`runs/<ts>_EXP-2026-005_q5b0b_subtype_key_recovery_tie/` 에 따로 쓴다 — Q5-B-0의
bundle을 덮어쓰지 않는다.

## Decision log

### 2026-08-09 — Q5-B-0b 사전 등록 (규칙 1개 변경 + gate 2개 추가; 결과 없음)

진단으로 "거리가 아니라 margin이 막았다"가 확정된 뒤, 사용자 승인을 받아 위
사전 등록을 추가했다. 임계값(coverage 비 0.80, 영가설 ≤0.05 / 비율 ≥5)은 **실제
데이터에 돌리기 전에** 정했고, Q5-B-0의 기본 동작과 기록된 판정은 건드리지 않았다
(모듈 기본값 `strict_identity`, gate에 새 검사는 `tie_symbol_agreement` 모드에서만
추가된다 — 회귀 테스트로 고정).

합성 fixture로 **규칙이 실패할 수 있음**을 먼저 확인했다: 드문 subtype이 혼합
동점 집합에만 존재하도록 만든 fixture에서 회수율 비가 0.27로 떨어져
`subtype_coverage_balance`가 탈락시킨다. gate가 장식이 아님을 코드로 고정했다.

### 2026-08-09 — NO-GO 인수 + 진단 추가 (deviation 기록 2; 판정 불변)

gate가 `NO_GO_SUBTYPE_CLOSED`를 냈다. 판정은 그대로 기록한다. v3에서 한 일은
두 가지뿐이고 **둘 다 판정을 바꾸지 않는다**:

1. `ordinal_mapping_exact_where_used`가 이름이 말하는 규칙을 판정하도록 정정
   (위 「결과」 참조). `s_match_fraction`·`content_anchor_fraction`이 단독으로
   NO-GO라 판정 불변.
2. **진단 추가(규칙 아님)**: 못 붙인 beat의 최근접 후보 거리 분포와 ordinal 가설
   탐침(record별 RR 차이의 중앙값·IQR·비율). 어떤 gate도 이 값을 읽지 않는다.
   목적은 "종결이 영구적인가, 아니면 별도 재등록이 가능한가"를 **데이터로**
   가르는 것이다.

임계값·조인 키·gate 기준은 하나도 바꾸지 않았다.

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

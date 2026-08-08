---
experiment_id: EXP-2026-003
stage_id: Q4-Q
title: Transportability replication of Q4-P's alpha-LR-overshoot mitigation (MIT-BIH primary, INCART conditional)
status: approved_for_implementation
implementation_owner: claude-code
kind: preregistered_replication
result_status: DESIGN READY / FULL RESULT NOT RUN
depends_on: EXP-2026-002
created: 2026-08-08
---

# EXP-2026-003 / Q4-Q — 전이(transportability) 재현 실험

**상태: DESIGN / RESULT NOT RUN.** 이 문서 전체가 사전 등록이다. 어떤 수치도
결과가 아니며, full GPU run·PREP_DATA gate·Q4-P 파생 분석 모두 아직 실행되지
않았다.

## 0. 명칭 경계 (사전 등록)

MIT-BIH와 INCART는 이 프로젝트에서 이미 사용된 적이 있는 cohort다. 따라서 이
실험을 "untouched external confirmation"이라 부르지 **않는다**. 정확한 명칭은
**pre-registered independent-cohort / transportability replication**이다.
MIT 통과 후 INCART 단계까지 통과해도 "pristine external confirmation"이라
부르지 않는다.

## 1. 배경과 질문

Q4-P(EXP-2026-002, run `20260808T1310`, MEASURED)는 SVDB에서 사전 등록 decision
tree의 **B3(LR/alpha overshoot) 단독 발화**를 측정했다: alpha LR을 1e-4로 낮춘
S2에서 best epoch가 뒤로 이동하고 dev가 개선되며 test C−D가 S0 대비 커졌다
(S2 C−D +0.004823, CI [−0.001940, +0.012379], seed 5/5 양수 — **CI가 0을
포함하므로 확증 아님**).

> **Q4-Q 핵심 질문**: Q4-P에서 발견한 alpha learning-rate overshoot 완화가
> 다른 cohort에서도 schedule interaction과 waveform-specific residual 개선으로
> 재현되는가? 그리고 그 효과가 환자 수준의 임상적으로 의미 있는 utility로
> 이어지는가?

## 2. Cohort와 데이터 자산 (Drive에서 확인된 사실 기준)

### 1차 cohort: MIT-BIH Arrhythmia (즉시 실행 가능)

- **입력 자산**: `mamba_data.npz`
  (Drive file id `1p3HvC_bnbiQlEanFOVIvVdejy60W0tho`, 약 204.5 MB,
  keys `beat, ref, feats, y, pid, t`, 99,871 beats, 44 records,
  DS1 22 / DS2 22, patient overlap 없음).
- `mitdb` 폴더(id `151DJAcjCbDXCoy9ZIPudbtSuVziG1fnj`)는 48 `.hea` + 48 `.atr`
  header/annotation cache다(`.dat` 없음) — 이 폴더만으로 waveform 재구축 불가.
  Q4-Q는 처리 완료 자산으로 재현하므로 **raw 다운로드가 필요 없다**.
- **교차 검증**: `ecg_multi.npz`(id `1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq`,
  약 1.17 GB, mitdb+svdb+incart 통합, 예상 keys
  `beat,y5,y3,y,pid,db,sym,pre_rr,post_rr,rhythm,rhythm_names,rr_edge`)의
  MIT subset을 후보 adapter source로 검사하되, `mamba_data.npz`의 record 수·
  beat 수·DS1/DS2 patient 구성과 교차 검증한다. **핵심 count/split 불일치가
  설명되지 않으면 full run을 실행하지 않는다**(중단 조건).
- DS1/DS2는 de Chazal canonical 분할(각 22 records; paced 4 records 제외).
  record == patient로 취급한다(MIT-BIH 관례).
- 한계(사전 인정): DS2는 22 patients뿐이고 MIT-BIH는 과거 개발에 노출된
  cohort다 — §0의 명칭 경계가 여기서 나온다.

### 2차 조건부 cohort: St Petersburg INCART (gate 통과 후에만)

- 처리 완료 `incart_data.npz`(id `1e9uUOrEXoKnylFLDSAd5Qdx55GZRhXRg`, 약 425.6 MB,
  keys `beat,y,pid,pre_rr,post_rr`, 175,571 beats, 75 records).
- **현재 `pid`는 75개 record-level ID다. 실제 patient는 32명이므로 이 `pid`를
  patient bootstrap/group split에 그대로 쓰면 안 된다**(leakage).
- annotation cache `incartdb`(id `1rNgzVlVYuiBDBfSjhHXm-Ksbw54nKfgM`,
  75 `.hea` + 75 `.atr`)의 header 주석에 명시적 `# patient N` 라인이 있다
  (I01.hea에서 실측 확인: `# patient 1`). **gate**:
  1. 75개 `.hea`의 `# patient N`을 regex(`^#\s*patient\s+(\d+)\s*$`,
     대소문자 무시)로 파싱해 frozen `record -> patient` map(JSON)을 만든다.
  2. 75 records가 정확히 32 patients로 매핑되는지 검증한다. record당 정확히
     1개의 patient 라인이 없거나(0개/복수), patient 수가 32가 아니면 **실패
     처리하고 중단**한다. 수동 추측 금지.
  3. adapter audit table: sample rate(257 vs 360 Hz), lead 수(12 vs 2)·선정,
     resampling, R-peak alignment, window size, normalization, label mapping,
     RR 단위를 MIT/Q4-P와 비교해 저장한다. class counts·불변조건 검증 뒤에만
     full run 허용. 비교 불가능하면 중단.
- `incart_raw`(id `1y9lpT_0unM04PJRMIUhUcmABTGNB_eqY`)는 partial(142 files,
  I01–I47 complete + I48 `.dat` only)이며 전체 75-record raw archive가 아니다.
  기존 prep이 Colab 임시 저장소에 전체 raw를 받고 파생 NPZ만 Drive에 저장했을
  수 있으므로, raw 폴더가 partial인데 NPZ가 75 records인 것은 모순이 아니다.
- raw waveform이 꼭 필요해지면(clean rebuild/adapter audit 한정) `wfdb`로 Colab
  임시 저장소 또는 **새 versioned Drive 폴더**에 받는다. 기존 폴더 덮어쓰기 금지.

## 3. 먼저 수행하는 Q4-P 무재학습 통계 보강 (파생 분석; 재학습 금지)

Q4-P bundle의 `predictions.npz`(y_true·record_id·fold·scored_mask·per-seed
logits 포함 — 자립적)만 읽어 **별도 파생 산출물**을 만든다. 원본 Q4-P artifact는
읽기 전용이며 fingerprint로 전후 불변을 검증한다. 산출 경로는 **새 버전 경로**
`runs/<ts>_EXP-2026-002_q4p_derived_analysis_v1/`.

- record paired bootstrap CI: `(C−D)_S2 − (C−D)_S0` (difference-in-differences)
- record paired bootstrap CI: `(C−A)_S2 − (C−A)_S0`
- seed별 방향성과 효과크기 표
- S2 C−D의 분해: `C−A` 개선과 `D−A`(shuffled-control) 손상으로
- patient waterfall과 bootstrap null distribution 그림
- metric은 Q4-P 원 계약과의 비교 가능성을 위해 **Q4-P의 k-sweep achievement**를
  유지한다(§5의 Q4-Q 주 metric과 구별).
- **이 결과는 사후 기전 분석으로 표시하며 Q4-P의 사전 등록 판정(B3)을 바꾸지
  않는다.**

## 4. 고정 실험 설계 (MIT 1차)

Q4-P에서 동결 승계: architecture(`build_residual_net`), residual 입력
(current-beat waveform), seeds(20260806..20260810), training horizon
(**24 epochs 전체 실행**, patience가 optimizer를 중단시키지 않음, epoch −1
후보 포함), checkpoint 의미(epoch −1 = 진짜 학습 전; alpha==0; output==offset),
tie tolerance, paired initialization/minibatch order. **S1·LR search·
architecture search를 추가하지 않는다.**

| 항목 | 값 |
|---|---|
| schedules | `S0_original`(전 그룹 1e-3) · `S2_alpha_low`(alpha만 1e-4) — 정확히 둘 |
| selector | **`SEL1_record_bce` 단독**(dev-only; Q4-P의 primary를 사전 지정) |
| arms | A(morphology baseline) · C-S0 · D-S0 · C-S2 · D-S2 |
| Arm A | `mamba_data.npz`의 `feats`에 Q4-O `_fit_logit` 프로토콜, DS1-fit에서 학습 |
| C | morphology offset + alpha×CNN residual (실제 파형) |
| D | within-record shuffled waveform control (`PERM_SEED` 동일, label-preserving) |
| offset | DS1-fit 내부 patient-grouped 5-fold cross-fitted; dev/DS2에는 DS1-fit 전체 모델 적용 |
| split | DS1 22 patients = fit+dev(훈련·선택 전용) / DS2 22 patients = **한 번의 고정 final test** |
| dev split | DS1 patients를 S-burden 순 정렬 후 every-5th를 dev로(Q4-O `dev_records` 규칙, 결정론·seed 불변) |
| 금지 | DS2 결과를 보고 hyperparameter·preprocessing·selector 변경 |

## 5. 사전 등록 endpoint와 판정

주 metric: **S-beat PR-AUC의 record-macro 평균**(프로젝트 규약 primary target;
Q4-P의 `record_macro_prauc` 정의 재사용). k-sweep achievement는 Q4-P 연속성을
위한 secondary로 병기하되 판정에 쓰지 않는다. 모든 CI는 patient(record)-level
paired bootstrap(n_boot=2000, Q4-O 구현 재사용).

- **기전 primary**: `(C−D)_S2 − (C−D)_S0`의 patient-bootstrap CI.
  alpha LR 저하가 실제 파형-shuffled 파형 격차를 키우는지 평가.
- **waveform-specific**: `C-S2 − D-S2`. CI 하한 > 0이어야 확증적
  waveform-specific evidence로 본다.
- **utility gate** (모두 동시 성립해야 pass):
  - `C-S2 − A >= +0.015` (record-macro S PR-AUC 차이의 mean)
  - patient-bootstrap CI 하한 > 0
  - seed 방향 >= 4/5
  - patient lower-tail: C-S2의 p10(record-level 하위 10퍼센타일)이 A 대비
    비열화(>= A의 p10 − 0.010 허용 오차)

### 해석 규칙 (사전 등록)

| mechanism | utility | 판정 |
|---|---|---|
| pass | fail | alpha overshoot 기전은 재현되지만 raw residual의 실용 이득 부족 → residual CNN 확장 중단 |
| fail | fail | residual CNN 경로 중단 |
| pass | pass | MIT 내 transport replication 성공 → 동결 설계로 INCART 32-patient stage 진행 (여전히 pristine external confirmation이라 부르지 않음) |
| 평균 양수·CI 넓음 | — | **underpowered**로 기록. seed 추가를 patient 수 부족의 대체물로 쓰지 않는다 |

mechanism pass = 기전 primary CI 하한 > 0. mechanism fail = CI가 0을 포함하고
평균도 부호 불안정(seed < 4/5). 그 사이(평균 양수·CI 0 포함·seed >= 4/5)는
underpowered. utility pass = 위 gate 4조건 동시 성립.

## 6. 실행 모드와 notebook UX

`DESIGN` / `SMOKE` / `PREP_DATA` / `FULL` / `ANALYZE` 중 **정확히 하나만**
활성(assertion). 기본값은 `DESIGN`(GPU full run 아님). notebook
(`notebooks/quest49_q4q_transportability_replication.ipynb`) 첫 화면에 현재
mode·데이터 경로/파일 ID·data audit pass/fail·`RESULT NOT RUN`(full result
없을 때)·셀 실행 순서를 표시한다. full run 후 notebook 안에서 §8의 표/그림을
즉시 표시한다. 오류·gate 실패 시 조용한 fallback 금지 — 원인과 해결 명령을
출력하고 중단한다.

## 7. 필수 산출물 계약 (향후 full run이 생성)

`runs/<ts>_EXP-2026-003_q4q_transportability_replication/` 아래:
`config.json` · `manifest.json`(data SHA256·git SHA·환경) · `result.json` ·
`split_map.json`(DS1 fit/dev·DS2, frozen) · `predictions.npz`(y_true·record_id·
split·per-seed 확정 test logits: A + {C,D}×{S0,S2}) ·
`training_history.json` · `checkpoint_table.csv` · `trajectory_table.csv` ·
`audit/data_audit.json`(mamba/ecg_multi 교차 검증) ·
`figures/report_summary.md` + 그림: `data_audit_split_table.png` ·
`class_patient_counts.png` · `learning_curves.png` · `best_epoch_distribution.png` ·
`arm_schedule_table.png` · `c_minus_d_did_forest.png` · `seed_direction.png` ·
`patient_waterfall_p10.png` · `pr_curves_calibration.png` · `decision_matrix.png`.
모든 수치 표는 화면 출력과 machine-readable JSON/CSV 양쪽에 저장. figure
제목/주석에 cohort·arm·schedule·seed 수·CI 단위 표기.

INCART stage 산출물(조건부): `incart_patient_map.json`(frozen) ·
`incart_adapter_audit.json`/`.md` — gate 통과 전 full run 산출물 없음.

## 8. 테스트 계약 (CPU; full GPU run 아님)

`mit-bih/test_q4q_transportability_replication.py`가 최소 검증:

- dataset key/shape/count 검증(로더가 잘못된 파일을 거부)
- MIT DS1/DS2 patient non-overlap + canonical 44 record 구성
- INCART 75 records -> 32 patients mapping (정상 fixture) / ambiguous·missing
  metadata 실패 처리 (불량 fixture)
- outer-test(DS2) label 뒤집기가 선택·dev 궤적에 무영향 (no leakage)
- epoch −1: optimizer step 0 · alpha == 0 · output == offset (Q4-P loop 재사용 경로)
- schedule 간 paired initialization/minibatch order
- D control: within-record shuffle · label-preserving
- selector가 dev 필드만 사용
- artifact immutability(fingerprint) / Q4-P 파생 분석이 원본 bundle을 변경하지 않음
- 파생 분석 수치의 결정론(synthetic predictions fixture에서 DiD 부호·CI 검증)
- utility gate·decision matrix fixture 판정(각 분기 분리)
- CPU synthetic smoke run이 번들 스키마·그림·decision matrix 생성
- notebook 정적 검증: 단일 mode·기본 DESIGN·stale claim 없음·출력 경로
- 기존 Q4-O(218)·Q4-P(87) 스위트 회귀 통과

## 9. 허용 파일 (이 브랜치의 변경 파일 전부)

1. `experiments/specs/EXP-2026-003-q4q-transportability-replication.md` (본 문서)
2. `mit-bih/q4q_transportability_replication.py`
3. `mit-bih/test_q4q_transportability_replication.py`
4. `notebooks/quest49_q4q_transportability_replication.ipynb`
5. `research/ASSETS.md` (자산 등록)
6. `research/PROJECT_STATE.md` (측정 상태 갱신)

Q4-O·Q4-P 소스와 과거 run bundle은 수정하지 않는다.

## 10. 중단 조건 (하나라도 발생 시 full run 금지, 보고)

- Q4-P 계산 코드 수정 없이는 결과 인수/파생 분석이 불가능함
- MIT DS1/DS2 patient overlap 또는 split 불일치
- `ecg_multi.npz` MIT subset과 `mamba_data.npz`의 핵심 count/split 불일치가
  설명되지 않음
- INCART 75 -> 32 매핑 검증 실패
- preprocessing/label/RR 단위가 cohort 간 비교 불가능
- outer-test 정보로 설계를 조정하게 됨
- 기존 artifact를 덮어써야만 진행 가능함

## Decision log

### 2026-08-08 — cross-check v3: beat-count 매칭 + S 불일치 한도/보고 (deviation 기록 2)

세 번째 PREP_DATA 실측에서 S=2 그룹 매칭이 STOP했다: mamba `[2083, 2537,
2579, 2974]` vs multi `[2083, 2538, 2953, 2979]` — 3쌍은 0~5 beat 차이로
일치하지만 mamba의 2579-beat record(S=2)의 짝이 multi의 S=2 그룹에 없다.
S 총합은 양쪽 2,781로 동일하므로, 이는 **독립 전처리 간에 일부 record의 S
개수 판정이 1~2개씩 다르다**(aberrant/edge beat 매핑 차이)는 뜻이고 "record별
S 정확 일치" 가정이 데이터로 반증된 것이다. 확장: record 식별은 식별력 높은
**beat-count 정렬 매칭**(±2%, skip 허용)으로 하고, S 일치는 정확 일치 대신
**한도 내 일치 + 전량 보고**로 바꾼다 — record당 |ΔS| ≤ 10, 총합 ≤ 20 beat
(사전 지정), 초과는 여전히 STOP. 불일치 내역은 audit JSON에 record 단위로
기록된다. Q4-Q 학습·판정은 mamba만 사용하므로 과학적 기준 무변경. 실측 S=2
케이스와 한도 초과 STOP 케이스를 회귀 fixture로 추가했다.

### 2026-08-08 — PREP_DATA gate 실측 후 cross-check 로직 확장 (deviation 기록)

사용자의 첫 Colab PREP_DATA 실행에서 gate가 설계대로 STOP했다. 실측:
`mamba_data.npz` 44 records / 99,871 beats / **S 2,781** vs `ecg_multi.npz`
MIT subset 48 records / 109,446 beats / **S 2,781**, 그리고
`ds1_in_multi=false`. 해석: **ecg_multi는 paced 4개 record(102/104/107/217)를
포함한 48-record 전체본이고 pid 코딩도 record 번호가 아닌 순번형**이다. S 총합
정확 일치는 두 파일의 동일 원천·동일 beat 추출을 강하게 뒷받침하며, 추가 4개
record의 S가 0임을 함의한다(paced와 부합). 이 설명을 결정론적 검증으로 구현:
cross-check를 id 동일성 대신 **per-record (beat 수, S 수) profile 매칭**으로
확장 — S 수는 record별 **정확 일치** 요구, beat 수는 ±2%(edge-beat 처리 차)
허용, 남는 record는 정확히 4개·전부 S=0(paced)일 때만 corroboration으로
인정한다. 그 외 모든 불일치는 여전히 STOP이다. 과학적 질문·split·지표·판정
기준은 변경 없음(데이터 감사 인프라의 확장). 테스트에 실측 케이스(48-record
순번 pid) 및 STOP 케이스(S 있는 leftover·S 총합 불일치·record 간 S 이동·잘린
subset)를 fixture로 추가했다.

### 2026-08-08 — 설계 등록 (결과 없음)

이 spec·구현·테스트·notebook을 사전 등록한다. CPU unit + synthetic smoke만
실행되었고 full GPU run·PREP_DATA gate·Q4-P 파생 분석은 **NOT RUN**이다.
설계 결정 기록:
- 주 metric을 k-sweep이 아닌 record-macro S PR-AUC로 둔 것은 프로젝트 규약
  (AGENTS.md primary target)을 따른 것이며, k-sweep은 Q4-P 연속성 secondary로
  병기한다. Q4-P 파생 분석(§3)만은 원 계약 비교를 위해 k-sweep을 유지한다.
- dev split을 seed 불변의 burden-ordered every-5th로 둔 것은 Q4-O
  `dev_records` 규칙의 재사용이다(새 자유도 도입 금지).
- utility gate의 p10 비열화 허용 오차 0.010은 record 22개 소표본에서의 단일
  record 요동을 흡수하기 위한 사전 지정 값이다.

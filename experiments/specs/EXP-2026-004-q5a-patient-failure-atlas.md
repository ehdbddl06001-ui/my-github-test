---
experiment_id: EXP-2026-004
stage_id: Q5-A
title: Patient-level S-beat failure atlas and causal-branch selection
status: approved_for_implementation
implementation_owner: claude-code
kind: preregistered_analysis_only
result_status: RESULT_NOT_RUN
run_id: null
measured: null
verdict: null
depends_on: EXP-2026-003
created: 2026-08-08
---

# EXP-2026-004 / Q5-A — 환자 수준 S-beat 실패 지도와 분기 선택

**상태: DESIGN / RESULT NOT RUN.** 이 문서·코드·notebook은 사전 등록이며 어떤
수치도 결과가 아니다. Colab에서 `INVENTORY` → `ANALYZE` → `REPORT`를 실행하기
전까지 `result_status: RESULT_NOT_RUN`을 유지한다.

## 0. 언어 경계 (사전 등록 — 가장 중요)

- Q5-A는 **관찰적 사후 분석**이다. 재학습하지 않고, 저장된 예측만 읽는다.
- 여기서 말할 수 있는 것은 `failure-associated factor`(실패 연관 요인)와
  `차기 개입 가설`까지다. **`cause`(원인)를 확정하지 않는다.**
- 실제 원인 여부는 Q5-B에서 **그 요인 하나만** 바꾸는 개입과 적절한
  음성대조군으로 검증한다.
- 근거가 불충분하면 `UNRESOLVED` / `INSUFFICIENT_ARTIFACTS` /
  `DATA_INTEGRITY_BLOCKED`를 **정식 판정**으로 기록한다. 억지로 다음 모델을
  고르지 않는다.
- `BLOCKED_MEASURED`도 실제 유효한 결과이며 숨기지 않는다.

## 1. 전제 상태 (2026-08-08 main 기준 실측 인용)

- **EXP-2026-003 / Q4-Q (MEASURED)** — run
  `20260808T1842_EXP-2026-003_q4q_transportability_replication`,
  기전 DiD `(C−D)_S2−(C−D)_S0` = −0.000441 [−0.001360, +0.000115] (seed 1/5),
  utility `C−A`(S2) −0.000533 [−0.001498, +0.000029] →
  **mechanism fail + utility fail → residual CNN 경로 중단**(PR #54 병합).
- Q4-P 사후 SVDB DiD +0.003434 [−0.000815, +0.008587] — B3 판정 불변, CI 0 포함.
- PREP_DATA: 44 matched · paced leftover 4 · **S 불일치 0 beat**;
  record 208·213은 mamba 전처리에서 각각 약 −12.7% / −11.1% beat 결손.
- INCART 75 records → 32 patients map 검증은 통과했으나 Q4-Q 규칙상 INCART full
  stage는 진행하지 않았다.
- **residual CNN은 closed direction**이다. Q5-A는 이를 재개하지 않으며 변형
  residual architecture도 제안하지 않는다. **INCART rescue run도 하지 않는다.**
- baseline 후보로 기록된 V9 `kink_noctx` S PR-AUC 약 0.597, V10 `pwave` 약
  0.660은 `research/PROJECT_STATE.md`에 **출판 전 run artifact로 검증 필요**라고
  적혀 있다 — Q5-A의 첫 임무가 이 검증이다.

## 2. 고정할 문제와 유동적으로 둘 방법

고정되는 것은 하나뿐이다.

> **새 환자에서 S-beat 성능의 환자별 하위 꼬리와 실패 환자를 개선한다.**

고정하지 않는 것: CNN architecture · residual 구조 · P-wave 가설 · RR 가설 ·
GroupDRO/CVaR · preprocessing/lead 선택. 방법은 Q5-A 결과에 따라 고른다.
residual CNN에 대한 sunk cost는 선택 근거가 될 수 없다.

## 3. 실험 정의

| 항목 | 값 |
|---|---|
| ID | `EXP-2026-004` |
| short name | `Q5-A` |
| kind | `preregistered_analysis_only` |
| 초기 상태 | `DESIGN READY / RESULT NOT RUN` |
| 학습 | **금지** (모듈에 학습 호출이 없음을 `assert_analysis_only()`가 검사) |
| 기존 checkpoint | 저장된 logits/probabilities를 **읽는 범위에서만** 재평가 |
| 원본 run bundle | **변경 금지** (전후 SHA256 fingerprint 비교) |
| DS2 정보로 hyperparameter/threshold/model 선택 | **금지** |

primary output은 새 성능 수치가 아니라 (1) 검증된 최신 baseline, (2) 환자·
record·beat 수준 실패 지도, (3) 데이터/매칭 완전성 판정, (4) 사전 정의된 실패
연관 요인별 근거, (5) Q5-B에서 검증할 **단 하나의** 개입 가설 또는 `UNRESOLVED`.

## 4. 허용 파일 (이 브랜치의 변경 파일 전부)

1. `experiments/specs/EXP-2026-004-q5a-patient-failure-atlas.md` (본 문서)
2. `mit-bih/q5a_patient_failure_atlas.py`
3. `mit-bih/test_q5a_patient_failure_atlas.py`
4. `notebooks/quest50_q5a_patient_failure_atlas.ipynb`
5. `research/ASSETS.md`
6. `research/PROJECT_STATE.md`

PR diff가 이 6개를 벗어나면 중단한다. **Q5-B spec·소스·notebook은 이 PR에서
만들지 않는다** — Q5-A가 `MEASURED`로 인수되고 사용자가 분기를 승인한 뒤 별도
PR에서 만든다.

## 5. 실행 모드와 Colab UX

`DESIGN` / `INVENTORY` / `ANALYZE` / `REPORT` 중 **정확히 하나**만 활성
(assertion). 기본값은 `DESIGN`.

| mode | 하는 일 |
|---|---|
| `DESIGN` | 파일·설정·예상 경로만 표시. 데이터 접근 없음 |
| `INVENTORY` | Drive mount 후 후보 run·prediction artifact 검색/검증. 분석 결과 없음 |
| `ANALYZE` | **모든 gate 통과 시에만** Q5-A 전체 분석 |
| `REPORT` | 저장된 Q5-A bundle만 읽어 표·그림·판정 재표시. 재계산 없음 |

notebook 첫 markdown 셀에 표시: `EXP-2026-004 / Q5-A` · 현재 lifecycle status ·
`ANALYSIS ONLY / NO TRAINING` · 원인 확정이 아니라 실패 연관 요인 탐색 ·
mode 실행 순서 · 결과 없으면 `RESULT NOT RUN` · residual CNN closed 및 INCART
rescue 금지.

Colab 실행 순서(고정): ① repo 준비 + commit SHA 표시 → ② Q4-O/Q4-P/Q4-Q(+Q5-A)
회귀 테스트 → ③ Drive mount → ④ `INVENTORY` → ⑤ inventory gate 결과 확인 →
⑥ `ANALYZE` → ⑦ `REPORT`.

gate 실패 시 조용한 fallback·위치 기반 억지 매칭 **금지**. 원인과 누락 파일을
표로 출력하고 중단한다.

## 6. 입력 자산 inventory와 baseline freeze

Drive root 후보: `MyDrive/MedKOS/ecg-model/` · `MyDrive/mitbih/`.
먼저 읽는 것: `research/ASSETS.md` · `registry.jsonl`(있으면 append-only 검사) ·
Q4-Q run folder `1ZCAYZCl4T4eoZzdFfV_IzkB0Mgbcqlw4` ·
`mamba_data.npz` `1p3HvC_bnbiQlEanFOVIvVdejy60W0tho` ·
`ecg_multi.npz` `1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq`.

> **2026-08-09 실측 반영**: baseline 집합은 primary `V10 = ablation_step9d/pwave`,
> paired control `BASE26 = ablation_step9d/base26`(같은 스크립트·seed, P파 특징만
> 다름), historical `V9 = kink_noctx`(**ARTIFACT_ABSENT** — 0.597 검증 불가)로
> 확정됐다. 상세 근거와 규칙은 Decision log 2026-08-09 참조.

V9/V10은 **이름만으로 하나를 임의 선택하지 않는다**. 후보를 전량 표로 만들고
각 행에 config/model name · git SHA 또는 notebook source · data SHA와 split ·
저장된 prediction/logit/probability 파일 · y_true/record_id/beat key ·
metric definition(beat micro인지 record/patient macro인지) · S class index와
label mapping · seed/fold · 실행 날짜 · 기록된 S PR-AUC를 남긴다.

freeze 규칙 (구현: `freeze_baseline()`):

- 동일 protocol·split·metric으로 **직접 비교 가능한** V9/V10 artifact만 baseline
  comparison에 포함한다.
- **DS2 성능이 높다는 이유로 후보를 고르지 않는다**(테스트: 기록된 S PR-AUC를
  뒤섞어도 선택이 바뀌지 않아야 한다).
- 역사적으로 명시된 모델명과 provenance가 일치하는 run을 선택한다.
- 후보가 여럿이고 식별 불가능하면 `AMBIGUOUS_BASELINE`으로 **중단**한다.
- probabilities나 안정적인 beat ID가 없으면 aggregate metric만 기록하고
  beat-level 비교에서 제외한다.
- 저장 artifact가 없는 모델을 Q5-A를 위해 **재학습하지 않는다**.
- split/metric/S index가 다르면 `INCOMPATIBLE_BASELINES`로 중단한다.

산출: `source_inventory.json` · `source_inventory.csv` · `baseline_freeze.json` ·
원본 bundle별 SHA256 fingerprint · 누락/모호성/호환성 표. 원본 fingerprint는
분석 전후 동일해야 한다(다르면 IMMUTABILITY VIOLATION으로 중단).

## 7. beat 정합성 및 데이터 gate

매칭 우선순위:

1. `(db, record_id, annotation_sample/index, beat_symbol)` 안정 키
2. 원 키가 없을 때만 이미 검증된 결정론적 waveform fingerprint(record 내 유일성
   검증 필수)
3. **단순 array position/row order 매칭 금지**(`assert_not_positional`)

각 모델/데이터 자산 쌍에 대해 matched · unmatched(left/right) · class별 mismatch ·
record별 mismatch · S-beat mismatch · duplicate key · label conflict를 보고한다.

hard stop: 동일 키의 label conflict 1건 이상 · 설명 없는 duplicate key ·
설명되지 않는 S-beat mismatch · record/patient split 불일치 · class mapping 불일치 ·
metric 동일 재계산 불가.

record 208·213은 **별도 감사표**: 각 source의 원래 beat 수와 matched 수, 제거된
symbol/class 분포, 제거된 S beat 수, 시간 위치·가능한 quality/rhythm annotation,
그 제거가 V9/V10/Q4-Q 비교를 편향시키는지. Q4-Q의 `S mismatch 0`은 **인용만 하지
않고 이번 입력 조합에 대해 다시 검증**한다.

## 8. 분석 집단과 leakage 경계

- MIT-BIH DS1/DS2 patient split을 명시하고 overlap 0을 검증한다(Q4-Q의 canonical
  집합을 그대로 import — 재정의 금지).
- DS2는 이미 반복 사용된 benchmark이므로 `untouched external test`라 부르지 않고
  **descriptive failure audit**으로 표시한다.
- threshold는 저장된 사전 지정 값 또는 **DS1에서만** 결정한다. DS1 row가 없으면
  DS1 S prevalence에 대응하는 **DS2 score 분위수**를 쓴다(DS2 label 미사용).
- bin은 생리적으로 사전 정의하거나 **DS1 quantile**로 정한 뒤 DS2에 고정 적용한다.
- DS2 label을 보고 threshold·bin edge·proxy 정의·실패 요인·branch rule을 바꾸지
  않는다(테스트: DS2 label 전량 반전 후에도 threshold/bin/proxy 값 불변).
- CI는 **환자/record 단위 bootstrap**. beat bootstrap으로 환자 수 부족을 숨기지
  않는다.
- S가 없는 record는 S PR-AUC에서 제외하되 전체 record 수 · S-bearing record 수 ·
  제외 record와 이유를 분리 보고한다.

## 9. 필수 실패 지도

**9.1 모델 성능 확정** — V9·V10(및 가능하면 Q4-Q baseline arm)에 대해 동일 코드로
beat-micro S PR-AUC · record/patient-macro S PR-AUC · patient median/p10/worst-5 ·
patient bootstrap CI · seed variability · DS1-locked threshold에서의 S
recall/precision/F1 · Brier · calibration/ECE를 재계산한다. PROJECT_STATE의
0.597/0.660과의 차이를 표로 보이고 **metric 단위 차이로 설명되는지** 확인한다.

**9.2 patient waterfall** — S-bearing patient마다 S count/전체 beat count,
V9·V10 S PR-AUC, paired delta, (가능하면) bootstrap 불확실성, S recall/precision,
대표 failure mode. V9→V10 이득이 소수 환자에서만 나는지 lower tail까지
움직이는지 분리한다.

**9.3 beat subtype** — AAMI S 내부 원 symbol `A`/`a`/`J`/`S`별 count · score
분포 · rank · FN rate. n이 작으면 CI와 `descriptive only`를 명시한다.

**9.4 RR/timing** — pre-RR · post-RR · local median RR · coupling ratio
(`pre_rr / local_median_rr`) · compensatory pause proxy · rhythm transition/edge
flag. bin별 S PR-AUC/FN rate와 환자 구성 변화를 보고하고, CI는 환자 단위 우선.

**9.5 atrial/P-wave visibility proxy** — P-wave annotation ground truth가 없으므로
단일 detector 출력을 `P-wave presence truth`라 부르지 않는다. 복수의 pre-QRS
proxy(atrial-window energy 대 isoelectric, local template correlation, pre-QRS
peak prominence, P-window morphology distance, 두 lead 간 concordance, QRS leakage
estimate)를 계산하고, 각 proxy가 V10이 쓰는 feature와 동일/파생 관계면 이를
표시해 독립 증거로 과장하지 않는다. proxy 간 일치도와 각 proxy의 실패 연관
방향을 함께 보고한다.

**9.6 signal quality·lead·preprocessing** — lead identity/availability · baseline
wander/noise proxy · saturation/flatline proxy · QRS alignment offset · beat-window
clipping/edge · mamba/ecg_multi inclusion 여부 · record 208·213 filtered 상태.

**9.7 calibration 대 ranking** — 오류가 (a) S score 순위 실패인지, (b)
threshold/calibration 실패인지, (c) N/S 혼동인지, (d) S/V·S/Q 혼동인지 분리한다.
threshold만 바꾸면 해결되는 것처럼 표현하지 않으며, closed direction인
alarm-rate dial을 재개하지 않는다.

**9.8 error gallery** — 공개 ECG record ID만 사용. confident FN · confident FP ·
V9 fail→V10 correct · V9 correct→V10 fail · 둘 다 실패 · 208·213
unmatched/filtered 예시. 각 plot에 record·beat key/time·true symbol·model
scores·RR·proxy·quality flag 표시. **정렬 기준과 상위 N을 코드에 사전 고정**해
cherry-picking을 막는다.

## 10. 실패 연관 요인 비교 방법

사전 고정 feature block: `B_ATRIAL` · `B_RR` · `B_QUALITY` · `B_SUBTYPE` ·
`B_PATIENT`. 목적은 인과 추론이 아니라 **오류 연관 구조 비교**다.

- outcome: S beat에서의 V10 error(DS1-locked threshold 기준 FN) 또는 low S score
- leave-one-patient-out(환자 ≤ 25) 또는 patient-grouped 5-fold
- 동일 base 위에 block을 하나씩 추가 → held-out log loss/AUROC의 incremental value
- patient bootstrap CI, 그리고 **다른 block 전부를 base에 넣은 adjusted 값**
- 가장 영향이 큰 record 2개를 빼도 효과가 남는지(`stable_after_record_drop`)
- 단변량 effect와 multivariable 결과를 모두 표시
- 복잡한 black-box explanation으로 원인을 대신하지 않는다. SHAP은 보조 시각화로만
  허용하며 branch 판정 기준으로 쓰지 않는다(이 구현은 SHAP을 쓰지 않는다).
- 오류 event 수가 `BLOCK_MIN_EVENTS`(30) 미만이면 **underpowered**로 기록한다.

## 11. 사전등록 decision tree

우선순위 순서대로 평가한다.

**D0 — ARTIFACT/DATA FAILURE.** baseline provenance 불명 · beat-level
predictions/stable key 부족 · 설명되지 않는 S mismatch/label conflict ·
split/metric 비호환 중 하나라도 → `INSUFFICIENT_ARTIFACTS` 또는
`DATA_INTEGRITY_BLOCKED`. 다음 일은 모델 실험이 아니라 artifact 복구/adapter 수정.

**D1 — QUALITY/PREPROCESSING ASSOCIATED** → `Q5B_QUALITY_GATE_OR_PREPROCESSING`.
조건: `B_QUALITY`가 patient-held-out error explanation에서 가장 큰 **안정적인**
incremental value, CI가 0을 넘고 방향이 환자 다수에서 일관, 특정 1–2 record 제거
시 사라지는지 별도 표기. 개입은 모델 구조가 아니라 품질 gate·lead 선택·
alignment/filtering 수정.

**D2 — ATRIAL EVIDENCE ASSOCIATED** → `Q5B_ATRIAL_EVIDENCE_BOTTLENECK`.
조건: 복수 atrial proxy가 예상 방향으로 일치(그중 최소 1개는 V10 feature와
독립), `B_ATRIAL`의 incremental value가 환자-held-out에서 안정, 단순 QRS
leakage/noise로 설명되지 않음. 개입은 residual CNN이 아니라 **독립 atrial-evidence
feature/gate**.

**D3 — RR/TIMING ASSOCIATED** → `Q5B_HIERARCHICAL_RR_ATRIAL_MODEL`.
조건: `B_RR`가 가장 강하고 안정적이며, atrial/quality block을 함께 넣어도(adjusted)
관계가 유지된다.

**D4 — DIFFUSE PATIENT SHIFT** → `Q5B_PATIENT_ROBUST_OBJECTIVE_PILOT`.
조건: 특정 block이 우세하지 않고, worst-patient failure가 모델 간 지속되며 환자
heterogeneity가 크고, 단일 subtype/record artifact로 설명되지 않는다. GroupDRO를
바로 확정하지 말고 **ERM 대 patient-CVaR/GroupDRO의 작은 DS1-only pilot**을 제안.

**D5 — UNRESOLVED.** 여러 block 근거가 비슷하거나 CI가 넓고 방향이 불안정하면
`UNRESOLVED`. 두 가설을 한 모델에 동시에 넣지 않는다. 가장 저비용의 추가 측정
또는 artifact 보강을 다음 단계로 제안한다.

**`largest mean`만으로 분기를 선택하지 않는다.** 선택에는 CI(0 초과), 환자 방향
일관성(≥ 0.60), 특정 record 의존성(상위 2개 제거 후 생존), 다른 block 보정 후
잔존(adjusted CI > 0), 그리고 차점 block 대비 **1.25배 margin**이 모두 필요하다.
동률이면 `UNRESOLVED`.

## 12. Q5-B 초안 생성 규칙

Q5-A `result.json`에는 선택된 branch와 **초안 재료만** 저장한다: selected branch ·
competing branches · evidence table · 반증 증거 · 필요한 입력/label/proxy ·
개입 변수 **하나** · 음성대조군 · 예상 위험 · go/no-go 기준 제안.
Q5-A가 측정되기 전에 특정 Q5-B architecture를 spec에 박아 넣지 않는다.

측정 후 결과 인수 작업에서 하는 일은 네 가지뿐이다: (1) spec/notebook/
PROJECT_STATE/ASSETS를 `MEASURED`로 정정, (2) 사전등록 decision tree 결과를 그대로
기록, (3) 별도의 `Q5-B design brief`를 결과 보고서에 생성, (4) **사용자 승인 전
Q5-B spec·코드·학습 notebook을 구현하지 않음**.

branch별 Q5-B 원칙(초안):

- **atrial**: V10 baseline 동결, 독립 atrial evidence만 추가, atrial-feature
  within-record shuffle과 temporal-window shift를 음성대조군으로.
- **RR**: RR/timing block만 개입, 동일 feature 수의 무관 timing control, atrial
  feature는 고정.
- **quality**: classifier 동결, deterministic quality/lead/alignment intervention,
  label을 쓰지 않는 선택 규칙.
- **patient-robust**: architecture 동결, objective만 ERM/CVaR/GroupDRO 사전등록
  비교, DS1 patient-grouped nested CV, 강한 regularization/early stopping.

어느 branch든 primary 목적은 평균 gain뿐 아니라 **patient p10/worst-patient
개선**이며 최소 gate: patient-macro S PR-AUC 개선 · patient-bootstrap CI ·
p10/worst-quartile 개선 또는 비열화 방지 · seed 방향 일관성 · 개입 대 음성대조군
차이 · **DS1에서 설계 확정 전 DS2/INCART 사용 금지**.

## 13. 저장 bundle 계약

`MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-004_q5a_patient_failure_atlas/`
(새 경로에만 저장, 기존 폴더 덮어쓰기 금지).

최소 파일: `config.json` · `manifest.json` · `result.json` · `log.txt` ·
`source_inventory.json`/`.csv` · `baseline_freeze.json` · `matching_audit.csv` ·
`patient_metrics.csv` · `subtype_metrics.csv` · `rr_timing_metrics.csv` ·
`atrial_proxy_metrics.csv` · `quality_metrics.csv` · `model_disagreement.csv` ·
`mechanism_evidence.csv` · `decision.json` · `summary.md` · `figures/` ·
source bundle fingerprint before/after.

beat-level table이 크면 parquet/npz로 저장하고 요약 CSV를 따로 만든다. 원본 ECG나
기존 probabilities를 불필요하게 복제하지 않는다.

`result.json` 상태: 모든 gate 통과·분석 완료 → `MEASURED` · artifact/data gate
실패 → `BLOCKED_MEASURED` · 사용자 미실행 → `RESULT_NOT_RUN` · 합성 smoke →
`SMOKE_NOT_A_RESULT`(실제 결과로 표시 금지).

## 14. 필수 시각화 (13개)

`inventory_gate_dashboard` · `baseline_comparison_table` ·
`patient_waterfall_paired_delta` · `patient_lower_tail_table` ·
`subtype_prauc_fn` · `rr_coupling_error_heatmap` · `atrial_proxy_vs_error` ·
`quality_and_208_213_audit` · `calibration_pr_curves` ·
`model_disagreement_matrix` · `block_evidence_forest` ·
`branch_decision_matrix` · `error_gallery`.

모든 figure에 cohort · split · model · n patients/records/beats · CI 단위를 적고,
소수 subtype은 n을 눈에 띄게 표시한다. notebook 마지막에는 자동 생성 한국어
요약(무엇이 확인됐는가 / 확인되지 않았는가 / 왜 `원인`이 아니라 `실패 연관
요인`인가 / selected branch 또는 unresolved / 다음 실험에서 조작할 단 하나의
변수 / next experiment 미실행 사실)을 표시한다.

## 15. 테스트 계약 (CPU; 학습·Drive 없음)

`mit-bih/test_q5a_patient_failure_atlas.py`가 검증한다:

모듈 import 시 학습/Drive 접근 없음 · source bundle immutability ·
stable beat-key matching 및 positional matching 금지 · duplicate/label conflict
hard fail · DS1/DS2 patient overlap 0 · DS2 label을 바꿔도 threshold/bin/proxy/
branch-rule 설정 불변 · S가 없는 record 처리 · record/patient bootstrap 단위 ·
metric 재계산 fixture · baseline ambiguity hard fail · V9/V10 metric
incompatibility hard fail · record 208·213 audit fixture · subtype mapping
fixture · P-wave proxy를 ground truth로 표시하지 않는 문구 검사 · decision tree
모든 분기 fixture · `largest mean`만으로 branch가 선택되지 않음 ·
`BLOCKED_MEASURED` bundle schema · ANALYZE 결과 bundle schema · REPORT mode는
저장 bundle을 읽기만 함 · notebook 기본 mode DESIGN · notebook 첫 화면
`RESULT NOT RUN` · residual CNN 재개·INCART rescue 금지 문구 검사 · 기존
Q4-O/Q4-P/Q4-Q 회귀 스위트 존속.

synthetic smoke는 실제 결과로 표시하지 않는다(`SMOKE_NOT_A_RESULT`).

## 16. 중단 조건 (하나라도 발생 시 ANALYZE 금지, 보고)

- baseline provenance가 모호하거나 후보가 식별 불가능(`AMBIGUOUS_BASELINE`)
- V9/V10의 split/metric/S index가 비호환(`INCOMPATIBLE_BASELINES`)
- beat-level predictions 또는 안정 키 부재
- 동일 키의 label conflict, 설명되지 않는 duplicate key 또는 S mismatch
- 원본 bundle을 덮어써야만 진행 가능
- DS2 정보를 보고 설계를 조정하게 됨

## 절대 금지 (사전 등록)

residual CNN 재개·변형 residual architecture 탐색 · Q5-A에서 새 모델 학습 ·
저장 probabilities/logits 재생성 · artifact가 없다는 이유로 재학습 · DS2를 보고
threshold/bin/proxy/branch rule 수정 · INCART residual CNN rescue run ·
P-wave proxy를 P-wave ground truth로 표현 · 관찰 연관성을 인과 원인으로 승격 ·
여러 실패 가설을 한꺼번에 넣은 새 모델 제안 · 기존 Drive 파일/run bundle 덮어쓰기 ·
결과가 없는데 spec/notebook을 MEASURED로 표시 · 사용자 승인 없이 Q5-B 구현 또는
full training 실행.

## Decision log

### 2026-08-09 — V9/V10 원 산출물 회수: 0.660·0.597 검증 완료 (deviation 기록 3)

사용자가 로컬에 보관 중이던 원 실행 패키지(`v9_results.zip`, `v10_results.zip`,
`v10.zip`, `S_PRAUC_0660_provenance.md`)를 제출했다. **arm × seed 확률 npz가
전부 보존돼 있었고, 재학습 없이 기록된 숫자를 전량 재현했다.**

| 패키지 | arm | 재계산(5시드 평균) | 기록 |
|---|---|---|---|
| V9 | v8_noc | 0.4258 | 0.426 |
| V9 | v8base | 0.5762 | 0.576 |
| V9 | kink_noproto | 0.4595 | 0.460 |
| V9 | **kink_noctx** | **0.5969 ± 0.0411** | **0.597 ± 0.041** |
| V9 | kink | 0.5341 | 0.534 |
| V10 | v8base | 0.5984 | 0.598 |
| V10 | base | 0.5732 | 0.573 |
| V10 | **pwave** | **0.6603** | **0.660** |
| V10 | pwave_noc | 0.5619 | 0.562 |
| V10 | full | 0.6541 | 0.654 |

확정된 사실 넷:

1. **0.660의 집계 단위는 "시드별 S PR-AUC의 평균"** 이다. 같은 확률을 시드
   앙상블한 뒤 PR-AUC를 재면 0.7717이 나온다 — 인용 시 단위를 반드시 명시해야
   한다. 이에 따라 `per_seed_mean_s_prauc`를 정식 metric 단위로 추가하고
   claim check가 beat-micro/record-macro와 함께 비교한다.
2. **`ablation_step9d/pwave`는 V10이 아니었다.** 또 다른 이름 충돌이며(앞선
   `exp2_pwave`와 같은 함정), 1차 ANALYZE가 동결한 것은 이 별개 계보였다.
   따라서 "저장 산출물에서 P파가 이득을 주지 않는다"는 1차 관찰은 **철회**한다 —
   진짜 V10에서는 `base 0.573 → pwave 0.660`(Δ+0.087, 5/5 시드)이다.
3. **V9는 존재한다 — `ARTIFACT_ABSENT` 판정 철회.** `kink_noctx`가 V9의 최고
   arm이고 0.597이 검증됐다. Drive에 없었을 뿐 로컬에 보관돼 있었다(앞선 한계
   기술 "다른 이름/로컬 보관 가능성"이 실제였다).
4. **V9와 V10의 DS2가 동일**하다(49,289박, N/S/V 44,232/1,837/3,220). 그리고
   atlas cohort와 **19/22 record가 (n, S, V)까지 정확히 일치**하며, 나머지 3개는
   N beat만 다르다(105 −1, 111 −1, 222 −4). S는 22개 record 전부 일치.

baseline 재동결(이후 run부터): primary **V10 = `pwave`** / **V9 = `kink_noctx`**,
짝 대조군은 **각자의 같은 패키지 안** `base` · `v8base`. `v8base`는 두 패키지에
모두 존재하므로 control은 **primary와 같은 디렉터리**로만 범위를 좁힌다(성능이
아니라 provenance 규칙). 이에 맞춘 코드 확장:

- **per-seed family**: `<arm>_s<seed>.npz` 묶음을 한 모델로 인식해 시드 축을
  복원한다. seed 파일 하나라도 cohort(record/label)가 다르면 STOP. 이로써
  그동안 "산출 불가"로 기록해온 **seed variability가 살아난다**.
- **행 대응 검증을 record 단위로 확장**: 전체 부분집합이 맞지 않아도, record별로
  beat 수와 **전체 label 벡터가 일치하면** 그 record만 검증 성립으로 인정하고,
  맞지 않는 record는 사유와 함께 **제외**한다(재정렬·보정 금지).

`ablation_step9d/*`는 별개 계보로 남기며 baseline에서 제외한다.

### 2026-08-09 — 첫 ANALYZE 실측 후 primary outcome 개정 (deviation 기록 2)

첫 `ANALYZE`(run `20260809T0808…`, `MEASURED`, 판정 `UNRESOLVED`)에서 §10의
outcome 정의가 **threshold에 갇혀 있음**이 드러났다. 산출물에 DS1 행이 없어
threshold가 "DS1 S prevalence(≈1.9%)에 대응하는 DS2 score 분위수"로 잡히는데,
DS2의 실제 S 비율은 3.7%(1,837/49,295)다. 즉 **정의상 S의 절반 이상이 자동으로
FN**이 된다(실측 FN rate 0.686, 그런데 S beat의 평균 순위는 94.1 퍼센타일).
이진 outcome이 이렇게 강제되면 block 비교의 신호가 희석된다 — 실제로 네 block
모두 Δlogloss 음수·환자 방향 ≤0.56·상위 2 record 제거 시 붕괴였다.

개정(사전 등록, 이후 run부터 적용):

- **primary outcome = `within_record_rank`** — 각 S beat가 **자기 record 안에서**
  얼마나 낮게 순위 매겨졌는지(1.0 = 그 record의 최하위). record 단위라 전역
  operating point가 개입할 수 없고, record별 단조 재척도에도 불변이다(회귀
  테스트로 고정). 평가는 patient-held-out **ridge 회귀의 MSE 개선**으로 하고,
  CI·환자 방향 일관성·record 제거 안정성·1.25배 margin 등 **판정 규칙은 그대로**다.
- **secondary = `fn_at_locked_threshold`(v1)** — 원 계약과의 비교 가능성을 위해
  같은 번들에 계속 기록한다(`mechanism_evidence.csv`의 `outcome` 열, `is_primary`
  플래그). 어느 것도 삭제하지 않는다.
- atrial proxy 일치도 표는 임의 threshold 대신 **"자기 record 안에서 나쁜 절반"**
  이진화를 쓴다.
- 이 개정은 DS2 label을 새로 들여다보고 만든 것이 **아니다** — 근거는 DS1/DS2의
  S prevalence 차이와 순위 분포라는 구조적 사실이다. 과학적 질문·split·주
  metric(S PR-AUC)·decision tree·branch 기준은 변경 없다.

같은 실측에서 `subtype_metrics.csv`가 A/a/J/S 전부 n=0으로 나왔다(1,837개가 전부
`other`) — `.atr` symbol 조인이 실패한 것이다. 경로(`raw_ann/mitdb`)는 정상이었고
원인은 `wfdb` 부재로 판단되어, notebook이 `wfdb`를 자동 설치하게 했다. 아울러
source의 `t`가 **초**로 저장돼 있어 sample로 되돌릴 때 부동소수 왕복 오차가 생길
수 있으므로, 조인에 **사전 선언한 ±2 sample(5.6 ms) 허용치**를 두고 record별
정확 일치 수와 거리 중앙값을 함께 보고한다. 조인율 0.95 미만이면 여전히 subtype
블록은 `unavailable`이다(근사 금지).

### 2026-08-09 — INVENTORY 실측 후 adapter 확장 (deviation 기록 1; 결과 없음)

사용자의 첫 Colab `INVENTORY` 실행에서 gate가 설계대로 **STOP**했다(185 후보 ·
beat-level 0 · `AMBIGUOUS_BASELINE`). 실측으로 드러난 사실 셋과 그에 따른 확장:

**(1) V9 `kink_noctx`는 존재하지 않는다 — 정식 결과.** Drive 전량 조회 결과
run 폴더·tag 폴더(`A/B/C/D`, `base26/combined42`, `base26/wst`, `A_gss/A_sgkf`,
`base_lf/film`, `base_clean/film_clean`, `base/temporal`, `base/dual`,
`base26/pwave`)·파일명·색인된 본문 어디에도 `kink`/`noctx`가 없다(유일한 hit은
이 실험이 오늘 만든 `baseline_freeze.json` 자신). repo 코드에도 없다. 따라서
**`V9 = ARTIFACT_ABSENT`, 기록된 0.597은 `UNVERIFIED`** 로 기록한다. 한계 명시:
Drive 색인은 `.npz` 내부를 읽지 않으므로 "다른 이름으로 저장된 V9"까지 배제하지는
못한다(사용자 로컬 PC 또는 미저장 가능성). **재학습으로 메우지 않는다.**

**(2) baseline 재정의.** primary는 `ablation_step9d/pwave`(= `colab_step9d_final.py`
의 `run_final("pwave")`), 짝 대조군은 **같은 폴더의 `base26`**(같은 스크립트·같은
seed(1000–1004)·같은 저울, `use_pw = tag=="pwave"` 한 줄만 다름)이다. `base26`이라는
이름은 `ablation_step11`·`step13`에도 있으므로, **paired control은 primary와 같은
parent run으로 범위를 좁혀서만** 선택한다(성능이 아니라 provenance 규칙). role 도입:
`primary`(부재 시 STOP) · `paired_control` · `historical_unverified`(부재는 결과이지
STOP이 아님). freeze 상태 `FROZEN_WITH_ABSENT_BASELINE` 추가 — gate는 통과시키되
absent 목록을 결과에 남긴다.

**(3) 예측 파일 인식은 파일명이 아니라 KEY로.** 2026-07/08 ablation 산출물은
`<run>/<tag>/ens.npz`에 `prob`/`y`/`pid`를 담는다. 최초 구현은 파일명에 `prob`가
들어간 것만 봤기 때문에 185개 run에서 beat-level 0이 나왔다(구현 결함). 확장:
npz의 **키 조합**으로 판정하고, tag 폴더를 독립 inventory 행으로 올린다.
`(n, n_class)` 확률 행렬 / `(n_seed, n)` 스택 / `(n,)` 점수를 `detect_score_layout`
으로 구분하며, 해석 불가한 shape은 추측 없이 오류다(S 열은 `S_COLUMN = 1` 고정).

**(4) 안정 키: 검증된 행 대응.** legacy 산출물에는 annotation index가 없다. 대신
동결 source(`mamba_data.npz`, SHA 고정, `t` 보유)의 부분집합과 **`pid`·`y`가 모든
행에서 일치하는지 전량 검증**하고(`verify_row_correspondence`), 통과한 경우에만
source의 `t`로 키 `(db, record, sample, symbol)`를 부여한다. 한 행이라도 어긋나면
STOP. 이는 금지된 "row order 매칭"이 아니라 **행 대응의 검증**이다 — 검증 실패 시
어떤 fallback도 없다. source 없이 legacy 산출물을 읽으면 즉시 오류다.

**(5) 모델 scope와 threshold.** legacy 산출물은 DS2만 채점한다. 따라서 (a) 매칭
감사는 **모델 자신의 record scope 안에서만** 불일치를 판정하고 scope 밖 record는
`records_not_covered`로 보고하며, (b) 분석 cohort는 모든 모델이 공통으로 덮는 DS2
record로 제한하고 제외 목록을 남긴다. (c) DS1 행이 없으므로 threshold는 **atlas
cohort의 DS1 주석에서 계산한 S prevalence**를 받아 DS2 score 분위수로 잠근다.
DS1 prevalence가 주어지지 않고 DS1 행도 없으면 오류다 — DS2 label로 threshold를
만드는 경로는 코드에 존재하지 않는다.

**(6) `.atr` 주석 경로 정정 + symbol 복구.** MIT-BIH 주석 캐시는
`mitbih/mitdb/`가 아니라 **`mitbih/raw_ann/mitdb/`**(folder id
`151DJAcjCbDXCoy9ZIPudbtSuVziG1fnj`)에 있다(`research/ASSETS.md` 정정). 키의
sample index로 `.atr`의 `(sample → symbol)`을 정확 조인해 원 symbol을 복구하고,
조인율이 `ANN_SYMBOL_MIN_MATCH`(0.95) 미만이거나 `wfdb`가 없으면 **subtype 블록을
unavailable로 기록**한다(근사 금지). RR은 source에 없으면 `t`에서 결정론적으로
계산한다(record 첫/마지막 beat는 미정의로 남긴다).

**(7) source 시간 열은 float이고 단위를 단정하지 않는다.** 첫 `ANALYZE` 실행에서
`mamba_data.npz`의 `t`가 **실수**(`0.0`)임이 드러났다(정수 sample index로 단정한
파싱이 `ValueError`로 중단). 단위를 추측하는 대신 **초/샘플 두 해석을 모두 계산해
중앙 beat 간격이 생리적 RR 범위(0.25–2.5 s)에 들어가는 쪽이 정확히 하나일 때만
채택**하고, 0개거나 2개면 측정값을 붙여 STOP한다(`infer_time_unit`). RR 유도와
`.atr` symbol 조인이 모두 이 검증된 단위를 쓴다. 아울러 키 생성 경로를
`format_beat_keys` **하나로 통일**했다 — legacy adapter가 `t`를 `int64`로 캐스팅해
`0.0`을 `0`으로 만들면 조인의 한쪽만 형식이 달라져 전량 불일치가 났을 것이다
(회귀 테스트로 고정).

과학적 질문·split·주 metric·decision tree·branch 기준은 **변경 없음**. 위는 전부
데이터 감사/adapter 인프라의 확장이며, 여전히 결과는 없다(`RESULT NOT RUN`).

### 2026-08-08 — 설계 등록 (결과 없음)

이 spec·구현·테스트·notebook을 사전 등록한다. CPU unit 테스트와 합성 fixture만
실행되었고 **Colab `INVENTORY`/`ANALYZE`/`REPORT`는 NOT RUN**이다. 설계 결정 기록:

- **baseline 선택에서 성능을 배제**: `freeze_baseline()`은 model name·git SHA·
  data SHA·split·metric definition만 본다. 기록된 S PR-AUC는 *검증 대상*으로만
  운반되며 tie-break에 쓰이지 않는다(회귀 테스트로 고정).
- **beat key 우선순위**: 원 annotation 키가 없을 때만 waveform fingerprint를
  쓰고, record 내 유일성 검증을 통과해야 한다. row order 매칭은
  `assert_not_positional()`로 원천 차단한다.
- **atrial template를 label-free로**: record별 정상 template를 `N` annotation이
  아니라 record 전체의 median pre-QRS 구간으로 잡았다. 이렇게 하면 proxy 값이
  DS2 label에 전혀 의존하지 않아 "DS2 label 반전 후 불변" 테스트가 값 수준에서
  성립한다(ectopic beat는 소수라 median은 정상 형태를 대표한다).
- **threshold fallback**: 저장 artifact가 DS2 row만 담고 있을 수 있으므로,
  DS1 label로 F1을 최적화할 수 없을 때는 DS1 S prevalence에 대응하는 DS2 **score**
  분위수를 쓴다. DS2 label은 어느 경로에서도 읽지 않는다.
- **branch margin 1.25배·환자 방향 0.60·상위 2 record 제거 후 생존·adjusted
  CI > 0**은 결과를 보기 전에 고정한 값이다. 동률은 `UNRESOLVED`로 간다.
- **block outcome**은 V10 error(FN)로 두었다. error event가 30건 미만이면
  block 비교를 하지 않고 underpowered로 기록한다.
- Q4-Q의 canonical DS1/DS2와 S index를 **import**해서 쓴다(재정의 금지 —
  cohort 정의가 실험 간에 갈라지지 않게).

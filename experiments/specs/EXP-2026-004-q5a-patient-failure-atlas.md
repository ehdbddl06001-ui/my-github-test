---
experiment_id: EXP-2026-004
stage_id: Q5-A
title: Patient-level S-beat failure atlas and causal-branch selection
status: measured_pending_acceptance
implementation_owner: claude-code
kind: preregistered_analysis_only
result_status: MEASURED
run_id: 20260809T1033_EXP-2026-004_q5a_patient_failure_atlas
measured: 2026-08-09
verdict: UNRESOLVED
depends_on: EXP-2026-003
created: 2026-08-08
---

# EXP-2026-004 / Q5-A — 환자 수준 S-beat 실패 지도와 분기 선택

**상태: MEASURED (2026-08-09).** 사전등록 decision tree 판정은 **`UNRESOLVED`
(D5)** 이고 근거 bundle은
`runs/20260809T1033_EXP-2026-004_q5a_patient_failure_atlas` 다. 아래 1~16절은
**측정 전에 등록된 설계 원문**이며 결과를 보고 고치지 않았다. 실측 결과와 Q5-B
design brief 는 「결과」·「Q5-B design brief」 절에 따로 적는다. Q5-B spec·코드·
학습 notebook 은 **사용자 인수·분기 승인 전까지 구현하지 않는다.**

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

## 결과 (2026-08-09 실측 · MEASURED)

run bundle: `MyDrive/MedKOS/ecg-model/runs/20260809T1033_EXP-2026-004_q5a_patient_failure_atlas`
(inventory run `20260809T1030_…_q5a_inventory`) · 모듈 `q5a v8` ·
`training_performed: false`.

**1. 무엇을 물었나.** "새 환자에서 S-beat 성능의 환자별 하위 꼬리와 실패 환자를
개선한다"는 고정된 문제에 대해, **재학습 없이** 저장된 예측만으로 어떤 요인이
실패와 연관되는지 지도를 만들고 사전등록 decision tree로 **다음에 조작할 단 하나의
변수**를 고른다. 방법(architecture)은 고정하지 않았다.

**2. 입력 자산과 baseline freeze.** 후보 185→203개 artifact를 스캔해 4개를 동결했다.
`FROZEN`: V10=`v10pkg_results/pwave_s{1000..1004}`, V10_BASE=`base_s*`(같은 부모
run의 짝 대조군), V9=`v9pkg_results/kink_noctx_s*`, V9_BASE=`v8base_s*`. 이름 충돌
(`pwave` 2건)은 **기록된 seed 계획**으로만 좁혔고, 같은 패키지가 두 번 풀려 생긴
중복은 content hash로 병합했다.

**3. 정합성 gate.** legacy 산출물에는 annotation index가 없으므로 동결 source
(`mamba_data.npz`, SHA `b1c16106…`)와 `pid`·`y`를 **전량 대조**해 행 대응을
검증했다(`per_record`, 42,123행, 모든 행에서 record id와 label 일치). 위치 기반
매칭은 쓰지 않았다. 시간축은 초 단위로 **검증**됐다(median RR 0.7958 s, fs 360).

**4. 분석 cohort.** 모든 모델이 공통으로 덮는 DS2 record **19개**
(`100 103 113 117 121 123 200 202 210 212 213 214 219 221 228 231 232 233 234`),
제외 3개(`105·111·222` — N beat만 −1/−1/−4). block 분석의 관측 단위는
**S beat 1,628개 · 환자 15명**(S가 있는 record만; `123 212 214 221` 제외).

**5. 기록된 주장 재현(claim check).** 4개 모두 **artifact 자신의 untrimmed
cohort**(22 record · 49,289 beat)에서 재계산해 `consistent` 로 확인했다.

| 모델 | artifact-native 시드별 평균 | 기록된 값 | (참고) 시드 앙상블 beat-micro | 분석 cohort beat-micro / record-macro / p10 |
|---|---|---|---|---|
| V10 (`pwave`) | **0.6603** | 0.660 | 0.7717 | 0.8651 / 0.4209 / 0.0569 |
| V9 (`kink_noctx`) | **0.5969** | 0.597 | 0.7358 | 0.8250 / 0.4112 / 0.0369 |
| V10_BASE (`base`) | 0.5732 | 0.573 | 0.7318 | 0.8202 / 0.4081 / 0.0697 |
| V9_BASE (`v8base`) | 0.5762 | 0.576 | 0.7157 | 0.8036 / 0.4208 / 0.0559 |

**단위 주의**: 0.660의 단위는 *시드별 PR-AUC의 평균*이다. 같은 확률을 시드
앙상블하면 0.7717이고, cohort를 19 record로 줄이면 0.8651이 된다 — 셋은 서로 다른
정의이며 섞어 쓰면 안 된다.

**6. 환자 수준 실패 지도.** 환자 간 산포가 크다(`p90−p10`: V10 0.886 · V9 0.799 ·
V10_BASE 0.786 · V9_BASE 0.815 → `heterogeneity_large: true`). 그러나 **worst
quartile은 모델 간에 일치하지 않는다**: 전 쌍 overlap 최소 0.333(V10|V9_BASE,
V9|V9_BASE), 최대 0.6 → `failure_persists_across_models: false`.
네 모델 모두의 worst quartile에 든 record 는 **219·231 둘뿐**이고(233은 4개 중 3개),
231은 어느 모델에서도 사실상 붕괴한다(S PR-AUC 0.0011–0.0024).
V10 대 V9_BASE의 S beat 1,628개 중 **710개(43.6%)는 두 모델 모두 틀린다**
(둘 다 맞음 581 · V10만 187 · V9_BASE만 150).

**7. subtype block — 측정 불가(정직한 공백).** `.atr` 조인 성공률이 1.9%로
**우연 수준과 같다**(최근접 주석까지의 중앙 거리 0.222×RR ≈ 무작위 기대 0.25×RR).
즉 동결 source의 `t`는 annotation sample index가 아니다. A/a/J/S 하위분류를
산출물에서 복구할 수 없으므로 `B_SUBTYPE`은 **평가하지 않았다**. 없는 것을 추정으로
채우지 않았다.

**8~10. block 증분가치(primary = `within_record_rank`, 환자-grouped holdout,
환자 bootstrap, n=1,628 S beat / 15명).**

| block | Δ | 95% CI | 다른 block 보정 후 Δ (adjusted CI) | 환자 방향 일관성 | 상위 2 record 제거 후 안정 | 자격 |
|---|---|---|---|---|---|---|
| `B_PATIENT` | **+0.0491** | [−0.0097, +0.0952] | +0.1009 [**+0.0233**, +0.2195] | 0.80 | ✔ | ✘ (raw CI가 0 포함) |
| `B_QUALITY` | +0.0173 | [−0.0017, +0.0374] | +0.0145 [−0.0203, +0.0546] | 0.67 | ✔ | ✘ |
| `B_RR` | −0.0300 | [−0.1602, +0.0639] | +0.0178 [−0.0679, +0.1016] | 0.67 | ✘ | ✘ |
| `B_ATRIAL` | −0.0955 | [−0.2738, +0.0165] | −0.0551 [−0.1987, +0.0571] | 0.40 | ✘ | ✘ |

secondary outcome(`fn_at_locked_threshold`)도 **순위가 같다**(B_PATIENT +0.108 ·
B_QUALITY +0.045 · B_RR −0.361 · B_ATRIAL −0.942) — 자격을 얻는 block은 역시 없다.

단변량 연관(증분가치가 아니라 **관측 연관**일 뿐이다): `pre_rr` 0.836 ·
`coupling_ratio` 0.796 · `atrial_window_energy_ratio` 0.724 · `patient_s_burden`
0.643 · `local_median_rr` 0.608, 반대 방향으로 `pre_qrs_peak_prominence` 0.288 ·
`compensatory_pause_ratio` 0.300 · `p_window_morph_distance` 0.369(AUROC:
오류 vs 특징). 품질 특징은 전부 0.42–0.56으로 거의 무정보다.
**RR·atrial 특징은 단변량으로는 강하게 연관되지만, 환자를 갈라놓고 보면 증분가치가
남지 않는다** — 즉 그 연관의 상당 부분은 환자 간 차이로 흡수된다.

**11. 사전등록 decision tree 판정 — `UNRESOLVED` (D5).**
`decision.json` 원문 그대로:

- ranked by delta logloss: `B_PATIENT 0.04911` · `B_QUALITY 0.01734` ·
  `B_RR −0.03003` · `B_ATRIAL −0.09545`
- qualified (CI>0, adjusted CI>0, direction>=0.6, stable): `[]`
- `no block qualifies and the diffuse-shift conditions are not met -> D5`
- reason: *evidence is similar across blocks or the CIs are wide with unstable
  direction* · next_step: *propose the cheapest additional measurement or
  artifact recovery; do not combine two hypotheses in one model*
- competing branches: 없음

D1/D2/D3는 자격 block이 없어 발화하지 않았다. **D4는 heterogeneity는 크지만
worst-patient 실패가 모델 간에 지속되지 않아(전 쌍 최소 overlap 0.333) 발화하지
않는다.** `B_PATIENT`가 순위 1위이고 adjusted CI가 0을 넘지만, 사전등록 규칙은
raw CI·adjusted CI·방향·record 안정성의 **AND**를 요구하므로 raw CI가 0을 포함하는
한 분기로 승격하지 않는다. 규칙을 결과에 맞춰 완화하지 않았다.

**12. 확인되지 않은 것 / 언어 경계 재확인.**
- 확인되지 않음: P-wave ground truth(없음), **인과관계**, S 하위분류별 실패 구조,
  DS2 밖의 일반화, 그리고 "어떤 block이 지배적인가"라는 질문 자체.
- 이 결과는 **원인이 아니라 `실패 연관 요인`** 이다. 실제 원인 여부는 Q5-B에서
  그 요인 **하나만** 바꾸는 개입과 음성대조군으로만 검증한다.
- residual CNN 경로는 여전히 closed이며 이 분석에서 재개하지 않았다. INCART
  rescue run도 하지 않았다. 새 모델 학습·확률 재생성 없음.
- **다음 실험(Q5-B)은 아직 실행하지도, 구현하지도 않았다.**

## Q5-B design brief (초안 — 미구현, 사용자 승인 대기)

D5의 사전등록 next_step은 "가장 저비용의 추가 **측정** 또는 artifact 보강"이다.
따라서 이 brief의 1순위는 **모델이 아니라 측정**이며, 모델 pilot은 2순위 조건부다.
두 가설을 한 모델에 동시에 넣지 않는다.

**Q5-B-0 (권고 1순위) — `B_SUBTYPE` 복구 측정 (학습 없음).**
- 문제: 5개 block 중 1개(`B_SUBTYPE`)를 재보지 못한 채 D5가 났다. 지금의 D5는
  "근거가 없다"가 아니라 **"근거가 한 칸 비어 있고 나머지는 서로 비슷하다"** 이다.
- 개입 변수 **하나**: 동결 source 행 ↔ 원 annotation 의 **키 복구** 하나뿐.
  경로는 `ecg_multi.npz`(`sym` 보유)와 `mamba_data.npz` 를 `pid`+waveform
  fingerprint 로 대조하는 것 — `t`를 sample index로 **가정하지 않는다**.
- 음성대조군: record 내 symbol 무작위 셔플(연관이 0으로 붕괴해야 함) ·
  N beat만으로 만든 가짜 subtype label.
- go/no-go: 조인 성공률 ≥ 95% 이고 record별 S 개수가 동결 source와 일치하면 GO.
  1.9%대에 머물면 `B_SUBTYPE`을 **영구 미측정**으로 종결하고 Q5-B-1로 간다.
- 비용: 분석 전용, GPU 불필요. 실패해도 잃는 것이 없다.

**Q5-B-1 (조건부 2순위) — patient-robust objective pilot.**
- 발동 조건: Q5-B-0 이후에도 자격 block이 없고 `B_PATIENT`가 계속 1위일 때만.
- 개입 변수 **하나**: objective(ERM vs patient-CVaR)만. architecture·입력·전처리·
  seed·epoch 예산은 V10 그대로 **동결**한다. GroupDRO를 미리 확정하지 않는다.
- 음성대조군: 환자 그룹 라벨을 무작위로 섞은 CVaR(진짜 환자 구조가 필요하다는 것을
  보이는 대조) · 같은 계산량의 ERM 재실행(seed 잡음 대조).
- 설계·중단 결정은 **DS1 patient-grouped nested CV에서만** 한다. DS2/INCART는 설계
  확정 전에 보지 않는다.
- primary gate: patient-macro S PR-AUC 개선 + patient-bootstrap CI가 0 초과 +
  **p10/worst-quartile 비열화** + seed 방향 일관성 + 개입 대 음성대조군 차이.
- 위험: 15명 규모에서 CVaR은 분산이 크다 → 사전에 seed 수와 중단 조건을 등록하고,
  실패하면 `NO-GO`로 기록한다(재시도 루프 금지).

**명시적으로 제안하지 않는 것**: residual CNN 재개·변형, atrial+RR 동시 투입 모델,
INCART rescue, 그리고 이번 결과를 근거로 한 어떤 인과 주장도 제안하지 않는다.

## Decision log

### 2026-08-09 — 재측정 완료: 판정 `UNRESOLVED` (D5) 확정 (deviation 아님 · 결과 기록)

모듈 v8(claim은 artifact-native cohort, D4 지속성은 전 쌍 최소 overlap)로 다시
측정한 run `20260809T1033` 이 최종 결과다. 직전 run `20260809T1009` 의
`Q5B_PATIENT_ROBUST_OBJECTIVE_PILOT` (D4) 판정은 **철회**한다 — 그 D4는 알파벳순
앞 두 라벨(V10과 그 짝 대조군 V10_BASE, 서로 feature block 하나만 다른 near-twin)의
overlap 0.6만 보고 발화했고, 전 쌍으로 계산하면 최소 overlap이 0.333이라 지속성
조건을 만족하지 않는다. 규칙을 결과에 맞춰 바꾼 것이 아니라, 규칙이 의도대로
계산되지 않던 것을 고친 뒤 다시 측정한 것이다(수정은 결과를 보기 전에 commit
`c305e35` 로 등록됐다). 같은 run에서 기록된 주장 4건(0.660·0.597·0.573·0.576)은
모두 artifact 자신의 cohort에서 `consistent` 로 확인됐다.

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

### 2026-08-09 — claim 검증은 artifact 자체 cohort에서, D4 지속성은 전 쌍 최소값으로 (deviation 기록 6)

첫 4-baseline `ANALYZE`(run `20260809T1009`, `MEASURED`, 판정 D4)에서 두 가지
결함이 드러났다.

**(1) 기록된 주장을 잘린 cohort와 비교하고 있었다.** 패키지와 mamba의 전처리가
record 105·111·222에서 N beat 몇 개(−1/−1/−4)만큼 달라 그 세 record가 통째로
제외됐는데, **222 하나에 S beat 209개(DS2 S의 11%)가 들어 있다.** 그 결과
V10의 beat-micro가 0.8651로 나왔다 — 기록된 0.660과 애초에 **다른 모집단**이다.
이대로면 claim check가 "재현 실패"로 찍히지만, 그건 주장이 틀려서가 아니라
cohort를 잘랐기 때문이다.

수정: **artifact 자체 cohort(자기 22 record 전량)에서 계산한 지표**를 따로 남기고
(`artifact_native_metrics`), **기록된 주장은 그 값과 비교**한다. feature 결합이
필요한 실패 지도만 검증된 19 record에서 계산한다. 두 수치를 같은 번들에 병기하고,
claim check 행에 어느 cohort인지(`cohort`, `n_beat`, `n_record`)를 적는다.

**(2) D4의 "모델 간 실패 환자 지속" 검사가 가장 약한 쌍만 봤다.** 라벨을 정렬해
앞의 둘만 비교했는데 그게 V10과 **자기 짝 대조군** V10_BASE였다 — P파 브랜치
하나만 다른 near-twin이라 거의 구조적으로 일치한다. 수정: **모든 모델 쌍의
겹침을 계산하고 그 최솟값**을 기준으로 삼는다(쌍별 값과 모델별 최악 사분위
명단도 함께 기록). 사전등록 임계값 0.50은 그대로다. 회귀 테스트로 near-twin 쌍이
단독으로 D4를 발화시키지 못함을 고정했다.

이 수정 전의 run `20260809T1009`의 D4 판정은 **(2) 때문에 재검토 대상**이다 —
수정된 규칙으로 다시 측정해야 확정된다.

### 2026-08-09 — 진짜 이름 충돌은 기록된 seed 계획으로 가른다 (deviation 기록 5)

병합·정확이름 수정 뒤에도 V10이 `AMBIGUOUS_BASELINE`으로 남았다. `ablation_step9d`
의 tag 폴더 이름이 **정확히 `pwave`** 라서, 패키지의 `pwave` arm과 이름만으로는
구분되지 않는다(내용이 다르므로 병합도 되지 않는다 — 올바른 동작이다).

성능으로 고르는 것은 금지이므로 **기록된 provenance**로 가른다. 역사 기록
(`v9_ECG.ipynb` / `v10_ECG.ipynb`의 `run(..., seeds=[1000..1004])`, 그리고
provenance 문서의 "5 arm × 5 시드, 확률 원값 npz 저장")은 **저장된 seed 계획이
1000–1004이고 시드별 파일이 남아 있어야 한다**고 말한다. 이를 target의
`require: {"seeds": [...]}` 로 명시하고, 후보가 둘 이상일 때만 적용한다.

- 이것은 **성능을 보지 않는다**. seed 계획은 실행 전에 기록된 사실이다.
- `require`를 제거하면 같은 입력에서 다시 `AMBIGUOUS_BASELINE`으로 STOP한다는
  회귀 테스트를 두어, 이 narrowing이 취향이 아니라 기록된 근거임을 고정했다.
- `ablation_step9d/pwave`(단일 `ens.npz`, seed 미보존)는 이 요건을 만족하지 않아
  자동으로 탈락한다.

아울러 병합 내역을 `reasons`에서 분리해 `collapsed_duplicates`로 옮겼다 — 사람이
읽는 STOP 메시지에는 실제 blocker만 남아야 한다.

### 2026-08-09 — 후보 매칭 정밀화: 정확 이름 우선 + 동일 산출물 병합 (deviation 기록 4)

패키지를 올린 뒤 첫 `INVENTORY`가 `AMBIGUOUS_BASELINE`으로 STOP했다(실측:
V10 후보 7개, V10_BASE 후보 22개). 원인 둘 다 **가짜 모호성**이었다.

1. **같은 패키지가 두 경로에 존재** — 직접 올린 `mitbih/v10pkg_results`와
   notebook이 푼 `mitbih/baseline_pkgs/v10pkg_results`. 같은 artifact인데 후보가
   둘로 세어졌다.
2. **토큰이 부분 문자열로 매칭** — `base`가 `base26`·`base_lf`·`base_clean`·
   `v8base`·`cnn_base`·`baseline_pkgs`까지, `pwave`가 `pwave_noc`까지 끌어왔다.

수정(사전등록 규칙 자체는 불변 — 여전히 성능으로 고르지 않는다):

- **정확한 model name 우선**: 토큰과 정확히 일치하는 후보가 있으면 그것만 쓰고,
  없을 때만 부분 문자열로 넓힌다.
- **동일 산출물 병합**: (model name, 파일명, 행 수)가 같으면 후보로 세기 전에
  **SHA256로 내용 동일성을 확인**하고 병합한다(해시는 충돌 시에만 계산). 이름과
  모양이 같아도 **바이트가 다르면 병합하지 않는다** — 그건 진짜 경쟁 후보이므로
  모호성 gate가 그대로 STOP한다. 병합 내역은 `reasons`에 남는다.
- notebook은 패키지가 이미 풀려 있으면 **두 번째 사본을 만들지 않고** 기존 경로를
  쓰며, 사본이 여러 곳에 있으면 경고를 출력한다.

같은 실측에서 `BLOCKED_MEASURED` 결과에는 `split` 키가 없어 notebook 출력 셀이
`KeyError`로 죽었다. 결과에 `ds2_analysis`·`ds2_excluded`를 담고, notebook은
`.get()`으로 읽으며 STOP 사유를 함께 출력하도록 고쳤다.

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

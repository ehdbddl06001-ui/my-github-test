# ECG research project state

Updated: 2026-08-08

## 다음 단계 (EXP-2026-004 / Q5-A — DESIGN, RESULT NOT RUN)

residual CNN 경로가 닫힌 뒤의 다음 단계는 **새 모델이 아니라 실패 지도**다.
`EXP-2026-004 / Q5-A`(`experiments/specs/EXP-2026-004-q5a-patient-failure-atlas.md`)
는 **재학습 없이** 저장된 예측만 읽어 어떤 환자·beat·상황에서 S-beat 분류가
실패하는지 지도로 만들고, 다음 실험에서 검증할 **단 하나의** 개입 가설을
사전등록 decision tree로 고른다.

- kind `preregistered_analysis_only` · 학습 금지 · 원본 run bundle 변경 금지 ·
  DS2 정보로 threshold/bin/proxy/branch rule 변경 금지.
- 언어 경계: Q5-A가 말하는 것은 **failure-associated factor(실패 연관 요인)**
  까지다. `원인`은 Q5-B에서 그 요인 하나만 바꾸는 개입 + 음성대조군으로 검증한다.
- 판정 후보: `Q5B_QUALITY_GATE_OR_PREPROCESSING` · `Q5B_ATRIAL_EVIDENCE_BOTTLENECK`
  · `Q5B_HIERARCHICAL_RR_ATRIAL_MODEL` · `Q5B_PATIENT_ROBUST_OBJECTIVE_PILOT` ·
  `UNRESOLVED` · `INSUFFICIENT_ARTIFACTS` / `DATA_INTEGRITY_BLOCKED`.
  근거가 부족하면 억지로 다음 모델을 고르지 않는다.
- 첫 임무는 아래 "Current benchmark"의 V9 0.597 / V10 0.660을 **실제 저장
  산출물과 대조해 확정하거나, 확정할 수 없는 이유를 기록**하는 것이다.
- 상태: **DESIGN READY / RESULT NOT RUN** — Colab `INVENTORY` → `ANALYZE` →
  `REPORT`가 아직 실행되지 않았다. Q5-B spec·코드·notebook은 Q5-A가 MEASURED로
  인수되고 사용자가 분기를 승인하기 전에는 만들지 않는다.

## Measured results (Q4-O / Q4-P) and the next step (Q4-Q)

- **EXP-2026-001 / Q4-O (MEASURED, NO-GO)** — SVDB leakage-free residual CNN.
  run `20260806T0923`, commit `624e987b`. Arm C가 25/25 (seed×fold)에서
  `best_epoch = 0`(첫 학습 epoch 완료 후) 체크포인트를 선택했고 utility 이득
  없음. epoch −1(학습 전)은 dev 후보로 평가되지 않았으므로 원인은 Q4-O만으로
  판정 불가였다.
- **EXP-2026-002 / Q4-P (MEASURED, verdict `B3_lr_or_alpha_overshoot`)** —
  run `20260808T1310`, code SHA `a4e24f4d…`, data SHA `892f6ae9…`. 사전 등록
  decision tree에서 **B3 단독 발화**: alpha LR만 1e-4로 낮춘 S2에서 best
  epoch가 뒤로 이동(1.88 vs 1.84), dev 개선(+0.00268), test C−D가 S0 대비 개선
  (+0.004823 vs +0.001389). epoch −1이 dev 최적인 비율 ~60–72%; 첫 epoch이
  dev를 개선한 비율 20%(train loss는 100% 감소). **경계**: S2 C−D CI
  [−0.001940, +0.012379]가 0을 포함 — waveform residual의 확증 아님(B6는 공식
  기준상 S0 C−D 검사로 미발화). seed 5/5 양수는 차기 실험 근거일 뿐이다.
- **EXP-2026-003 / Q4-Q (MEASURED, 판정: mechanism fail + utility fail →
  residual CNN 경로 중단)** — run `20260808T1842`, code SHA `579fed7`, data
  `mamba_data.npz` SHA `b1c16106…`, MIT-BIH DS1→DS2 (endpoint 16 records),
  L4 237.7s. 기전 DiD `(C−D)_S2−(C−D)_S0` = −0.000441 [−0.001360, +0.000115],
  seed 1/5 양수 — **SVDB의 Q4-P B3 기전이 MIT로 transport되지 않았다**(부호
  반전, 효과 ~1e-4로 사실상 0). utility `C−A`(S2) −0.000533 → gate fail.
  정성 패턴만 재현(S2에서 best epoch 후행 이동). PREP_DATA gate 통과(mamba↔
  ecg_multi 5-클래스 지문 corroboration, S 불일치 0 beat; INCART 75→32 map
  검증). Q4-P 사후 파생 DiD(SVDB) +0.003434 [−0.000815, +0.008587]는 B3 판정
  불변의 사후 지지 증거일 뿐. **INCART stage는 진행하지 않는다**(사전 등록
  규칙상 MIT pass 전제). 상세: `experiments/specs/EXP-2026-003-…md` §11.

## Current benchmark
- Dataset/task: MIT-BIH AAMI 5-class, de Chazal DS1→DS2 patient-independent evaluation.
- Primary metric: S-beat PR-AUC.
- Required supporting views: patient-level lower tail, patient macro metrics, seed variability, patient bootstrap.
- Historical path: V8 base CNN → V9 comparison/prototype → V10 explicit P-wave morphology.
- Recorded reference: V9 `kink_noctx` S PR-AUC about 0.597; V10 `pwave` about 0.660.
  **2026-08-09 검증 완료** — 원 실행 패키지(`v9_results` / `v10_results`)의 arm×seed
  확률 원값에서 재학습 없이 재현했다:
  - **V10 `pwave` 0.6603** (기록 0.660), 짝 대조군 `base` 0.5732 (0.573) → 같은
    실행 안에서 Δ+0.087, 5/5 시드
  - **V9 `kink_noctx` 0.5969 ± 0.0411** (기록 0.597 ± 0.041), 짝 대조군 `v8base`
    0.5762 (0.576)
  - **0.660의 단위는 "시드별 PR-AUC의 평균"** 이다. 같은 확률을 시드 앙상블하면
    0.7717이 나오므로 인용 시 단위를 반드시 붙인다.
  - 앞서 `ARTIFACT_ABSENT`로 기록했던 V9는 **철회** — Drive에 없었을 뿐 로컬
    보관본이 존재했다. `ablation_step9d/pwave`는 이름만 같은 **별개 계보**였고
    baseline에서 제외한다.
  - V9·V10의 DS2는 동일(49,289박)하고 atlas cohort와 19/22 record가 정확히
    일치한다 → V9↔V10 beat 수준 비교가 가능하며 seed variability도 복원된다.

## Current scientific focus
The next decision is driven by failure patients and lower-tail robustness, not a small mean-only gain.
P-wave/QRST work showed that QRST removal can improve P-wave ranking, but the tested detector did not establish independent P-wave presence evidence.

## Closed or non-beneficial directions
Previously recorded as ineffective, unstable, or harmful in the tested setting: SMOTE/oversampling, FiLM patient adaptation, patient embedding, metric learning, multi-beat context, 2D-DTW, and alarm-rate dial approaches.
2026-08-08 추가: **raw-waveform residual CNN 경로** — Q4-O NO-GO, Q4-P B3(탐색적), Q4-Q transportability replication에서 mechanism·utility 동시 fail로 사전 등록 규칙에 따라 중단(EXP-2026-003 §11).
A new spec must state why conditions differ before reopening one.

## Reproducibility requirements
- fixed patient split and recorded patient IDs;
- deterministic settings and environment manifest;
- multiple seeds or a predeclared seed plan;
- patient-level bootstrap;
- saved probabilities when practical, allowing re-evaluation without retraining;
- no final-test feedback into training.

## Latest known run reference
- Drive: `/content/drive/MyDrive/MedKOS/ecg-model/runs/20260808T1842_EXP-2026-003_q4q_transportability_replication`
- Notebook target: `notebooks/quest49_q4q_transportability_replication.ipynb` (실행본, MEASURED)
- Next: residual CNN 경로 중단이 확정되었으므로 차기 방향은 새 spec으로 —
  기존 closed 목록을 재개하려면 조건 차이를 명시해야 한다.
- 차기 spec은 `EXP-2026-004 / Q5-A`(분석 전용 실패 지도, DESIGN / RESULT NOT RUN).
  Q5-A 결과 bundle 예정 경로:
  `MyDrive/MedKOS/ecg-model/runs/<ts>_EXP-2026-004_q5a_patient_failure_atlas`
  (아직 없음). notebook: `notebooks/quest50_q5a_patient_failure_atlas.ipynb`.

## Immediate intake work
1. Inventory Drive assets without moving them.
2. Match each important run to its notebook, result, config, and probabilities.
3. Ingest missing executed notebooks/results.
4. Reconcile this summary with the newest ingested run.
5. Create the next experiment only after the inventory identifies the true latest baseline.

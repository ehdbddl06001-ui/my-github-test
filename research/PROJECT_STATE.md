# ECG research project state

Updated: 2026-08-08

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
- Recorded reference: V9 `kink_noctx` S PR-AUC about 0.597; V10 `pwave` about 0.660. Verify against ingested run artifacts before publication.

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

## Immediate intake work
1. Inventory Drive assets without moving them.
2. Match each important run to its notebook, result, config, and probabilities.
3. Ingest missing executed notebooks/results.
4. Reconcile this summary with the newest ingested run.
5. Create the next experiment only after the inventory identifies the true latest baseline.

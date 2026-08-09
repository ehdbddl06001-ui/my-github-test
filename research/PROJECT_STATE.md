# ECG research project state

Updated: 2026-08-09

## EXP-2026-004 / Q5-A — MEASURED (2026-08-09), 판정 `UNRESOLVED` (D5)

run `20260809T1033_EXP-2026-004_q5a_patient_failure_atlas` · 모듈 q5a v8 ·
`training_performed: false`. 사전등록 decision tree에서 **자격을 얻은 block이
하나도 없다**(`qualified: []`).

- block 순위(primary = `within_record_rank`, 환자-grouped holdout, S beat 1,628 ·
  환자 15): `B_PATIENT` **+0.0491** [−0.0097, +0.0952] (다른 block 보정 후
  +0.1009 [**+0.0233**, +0.2195], 환자 방향 0.80, record 제거에 안정) ·
  `B_QUALITY` +0.0173 · `B_RR` −0.0300 · `B_ATRIAL` −0.0955.
  1위인 `B_PATIENT`도 **raw CI가 0을 포함**해 분기 자격 미달 → D5.
- 환자 산포는 크지만(`p90−p10` 0.79–0.89) **worst quartile이 모델 간에 지속되지
  않는다**(전 쌍 최소 overlap 0.333) → D4 미발화. 네 모델 모두의 worst quartile에
  드는 record는 `219`·`231` 둘뿐이며 231은 어디서나 붕괴한다(S PR-AUC 0.001–0.002).
  V10 대 V9_BASE는 S beat 1,628개 중 **710개(43.6%)를 둘 다 틀린다**.
- `B_SUBTYPE`은 **측정 불가**: `.atr` 조인 성공률 1.9% = 우연 수준(최근접 주석까지
  중앙 거리 0.222×RR). 동결 source의 `t`는 annotation sample index가 아니다.
  없는 것을 추정으로 채우지 않았다.
- 단변량으로는 `pre_rr`(0.836)·`coupling_ratio`(0.796)·
  `atrial_window_energy_ratio`(0.724)가 오류와 강하게 연관되지만, **환자를 갈라
  놓으면 증분가치가 남지 않는다** — 연관의 상당 부분이 환자 간 차이로 흡수된다.
- 이것은 `원인`이 아니라 **실패 연관 요인**이다. 인과는 Q5-B에서 요인 하나만 바꾸는
  개입 + 음성대조군으로만 검증한다.
- **다음 단계(사전등록 D5 next_step: "가장 저비용의 추가 측정 또는 artifact 보강")**:
  ① `B_SUBTYPE` 복구 측정, ② 그 뒤에도 자격 block이 없고 `B_PATIENT`가 1위면
  objective 하나만 바꾸는 DS1-only patient-CVaR pilot. 자세한 내용은 spec의
  「Q5-B design brief」.

## EXP-2026-005 / Q5-B-0 — MEASURED (2026-08-09), 판정 `NO_GO_SUBTYPE_CLOSED`

run `20260809T1156_EXP-2026-005_q5b0_subtype_key_recovery` · 학습 없음.
**`B_SUBTYPE`은 이 사전등록 아래에서 종결**이고, Q5-A의 `UNRESOLVED`(D5)는 4개
블록 위에서 그대로 유지된다. symbols를 붙이지 않았고 재분석도 돌리지 않았다.

- 실패한 검사: `s_match_fraction` **0.2593**(≥0.95) · `content_anchor_fraction`
  **0.1981**(≥0.50) · record floor 18/32.
- 통과한 검사가 더 많은 것을 말해준다: 매칭된 **721박의 symbol이 100% A/a/J/S**
  (matcher가 볼 수 없는 값) · wrong-record 영가설 **0.48%** · 신호/영가설 **54배**
  · 매칭 잔차 median **1.4 ms** · 순서 뒤섞기 불변 · record 동일성 44개 확립
  (leftover 4개 = paced) · **per-record S 개수 불일치 0**.
- 복구된 분포도 임상적으로 타당: **A 627 · a 32 · J 61 · S 1**.
- 즉 **같은 S beat 집합인데 80%에서 RR이 5 ms 안에 안 들어온다.** 26%만 붙은 채
  부분 사용하는 것은 하지 않는다 — 그 26%는 RR 일치를 조건으로 뽑힌 부분집합이라
  선택 편향이다.
- **"버려진 beat 때문"이라는 첫 설명은 철회했다** — 크기가 45배 안 맞는다.
  cohort에 없는 beat는 818박(**0.81%**, 90%가 208·213)뿐이고, 이웃 소실로 RR이
  오염될 수 있는 생존 beat는 상한이 **1.64%** 인데 실제 실패는 **74.1%** 다.
- 대신 이 계산에서 확정된 것: **버려진 beat 중 S는 0박**(per-record S 불일치 0).
  즉 **Q5-A는 걸러진 S 집단을 채점한 것이 아니다.** v4가 이 drop map을
  record별·클래스별로 `record_mapping.csv`에 남긴다.
- 남은 후보(미확인): ① `t`가 annotation이 아니라 **검출된 R-peak** 위치여서 RR이
  beat마다 수~수십 ms 흩어짐(26%가 1.4 ms로 정확히 맞는 관측과 잘 맞음) ②
  이웃 소실(208·213에 국한) ③ RR로 식별 불가. 판별 기준은 못 붙인 beat의
  최근접 후보 거리: 0.005~0.05 s면 ①, 0.5~1.5 s면 ②, 균일하면 ③.
- 다음: v3 진단(최근접 후보 거리 분포 · ordinal 탐침)으로 **영구 종결인지 별도
  재등록이 가능한지**를 데이터로 가른다. 재등록한다면 좌표별 키와 **그 키로 다시
  계산한 wrong-record 영가설**을 함께 등록한다(느슨한 키는 영가설을 올리므로 같은
  gate를 새로 통과해야 한다).

### 사전 등록 원문 (2026-08-09 승인, 변경 없음)

사용자가 Q5-B 진행을 승인해 **①(측정)** 을 사전 등록했다:
`experiments/specs/EXP-2026-005-q5b0-subtype-key-recovery.md`.

- 하는 일: 동결 cohort(`mamba_data.npz`)의 **S beat**에 `ecg_multi.npz`의 원
  annotation symbol을 되붙인다. 키는 `(pre_rr, post_rr)` 초 단위 — **beat 자신의
  성질만** 쓴다(이웃 RR을 넣으면 행 순서에 의존해 "pool을 섞어도 같은 결과"를
  증명할 수 없다). symbol은 매칭에 쓰지 않으므로 "매칭된 beat의 symbol이 A/a/J/S에
  드는가"가 **독립 검증**이 된다.
- 음성대조군 4종을 사전 등록: permutation(anchor 불변) · shift(대응이 한 칸
  밀리면 tolerance 밖) · wrong-record(오매칭률 **상한**) · shuffle(복구 symbol을
  record 안에서 섞으면 `B_SUBTYPE` 효과가 무너져야 한다).
- gate 실패 = `NO_GO_SUBTYPE_CLOSED` → `B_SUBTYPE` **영구 종결**, Q5-A의
  `UNRESOLVED`(D5)는 4개 블록 위에서 유지. 추정으로 채우지 않고 재학습하지 않는다.
- GO면 Q5-A의 `run_atlas`를 **수정 없이** 다시 호출해 5개 블록으로 decision tree를
  재평가한다. `B_SUBTYPE`은 Q5-A에서 이미 **개입 분기가 없는 서술 블록**이므로,
  이겨도 자동으로 모델 실험이 되지 않는다(D5로 간다).
- 학습·GPU 없음. 테스트 155개 통과(CPU). **Q5-B-1(개입 pilot)은 여전히 승인 전까지
  만들지 않는다.**

## 설계 원칙 (Q5-A 사전등록 — 변경 없음)

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
- 첫 임무였던 "V9 0.597 / V10 0.660을 실제 저장 산출물과 대조해 확정"은 **완료**
  됐다 — 네 arm 모두 artifact 자신의 cohort에서 `consistent`(아래 Current
  benchmark 참조).
- 분기 선택 규칙은 `largest mean` 단독이 아니라 raw CI · adjusted CI · 환자 방향
  일관성(≥0.60) · 상위 2 record 제거 후 생존 · 차점 대비 1.25배 margin의 **AND**
  다. 이번 실측에서 이 AND를 통과한 block은 없었고, 규칙을 결과에 맞춰 완화하지
  않았다.

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
  - Q5-A run `20260809T1033`이 네 arm을 **artifact 자신의 cohort**에서 다시 확인
    (`consistent`). 같은 run의 환자 하위 꼬리(19 record cohort, record-macro / p10):
    V10 0.4209 / 0.0569 · V9 0.4112 / 0.0369 · V10_BASE 0.4081 / 0.0697 ·
    V9_BASE 0.4208 / 0.0559 — **평균에서 앞선 V10이 p10에서는 앞서지 않는다.**

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

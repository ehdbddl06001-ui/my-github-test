---
experiment_id: EXP-2026-002
stage_id: Q4-P
title: Cause separation for Q4-O's universal best_epoch=0 checkpoint selection
status: approved_for_implementation
implementation_owner: claude-code
kind: exploratory_diagnostic
result_status: DESIGN READY / FULL RESULT NOT RUN
depends_on: EXP-2026-001
created: 2026-08-08
---

# EXP-2026-002 / Q4-P — `best_epoch = 0` 원인 분리 진단

**상태: EXPLORATORY DIAGNOSTIC / RESULT NOT RUN.** 이 문서와 구현은 설계다.
어떤 수치도 결과가 아니며, full GPU run은 아직 실행되지 않았다.

## 1. 배경 — Q4-O가 판정할 수 없었던 것

EXP-2026-001 / Q4-O(run `20260806T0923`, commit `624e987b`, verdict NO-GO)에서
Arm C(morph + raw residual)는 25개 (seed × fold) **전부**에서 `best_epoch = 0`을
선택했다. Q4-O Phase A 정정이 확정했듯이:

- epoch 0은 **첫 번째 학습 epoch 완료 후**의 체크포인트다(batch 1024 기준 약
  77~79 optimizer step). 학습 전 상태가 아니다.
- 선택된 체크포인트의 `alpha`는 0이 아니라 대체로 `|0.078~0.101|`이다.
- Q4-O는 학습 전 체크포인트(epoch −1)를 dev 후보로 **평가하지 않았다**
  (`best_loss = inf` 초기화가 epoch 0을 무조건 채택). 따라서 "epoch 0이 정확한
  morphology baseline보다 나은가"는 Q4-O 데이터만으로 판정 불가다.

## 2. 고정 질문 (단 하나)

> Arm C의 `best_epoch = 0`은 (a) 학습 전 baseline보다 residual이 **즉시
> 유해**해서인가, (b) **첫 epoch 이후 과적합**해서인가, (c) learning-rate /
> alpha gate **overshoot**인가, 아니면 (d) pooled BCE checkpoint selector와
> patient-level 평가의 **불일치**인가?

architecture나 ECG 입력은 업그레이드하지 않는다. Transformer, 더 큰 fusion
모델, 새 feature는 금지된다(EXP-2026-001의 사전 등록된 중단 규칙 유지). 떠 있는
것은 **학습 trajectory와 checkpoint 정의**뿐이다.

## 3. 고정 조건 (Q4-O에서 동결 승계)

| 항목 | 값 |
|---|---|
| 데이터 | 동일 `svdb_data5.npz` (SHA256 `892f6ae9…`), scorable 56 records |
| 분할 | Q4-O와 동일 outer 5-fold / inner 5-fold, frozen fold map (동일 결정론 함수) |
| seeds | Q4-O의 5개: 20260806..20260810 |
| 입력 | 동일 current-beat two-lead waveform |
| Arms | **C**(정상 파형) · **D**(within-record shuffled, `PERM_SEED` 동일) · A는 paired 참조 |
| offset | 동일 morphology inner-cross-fitted offset (`cross_fitted_offsets` import) |
| 모델 | 동일 CNN(`build_residual_net` import), BCE, batch 1024, weight decay 1e-4 |
| 초기화/미니배치 | schedule 간 동일 (seed, fold) 초기 파라미터와 minibatch 순서 (paired) |
| 평가 경계 | outer-test label/metric은 schedule·checkpoint 선택에 사용 금지 |
| 실행 범위 | **이번 작업에서 full GPU run은 실행하지 않는다** — CPU unit + synthetic smoke만 |

구현은 `mit-bih/q4p_best_epoch_zero_diagnostic.py`가 Q4-O 모듈에서 데이터 로딩,
feature, fold map, model builder, leakage assertion, metric, bootstrap을
**import**한다(복사 금지 — 테스트가 재정의 부재를 검증). 진단용 training loop만
새로 둔다. Q4-O 소스는 이 브랜치에서 수정하지 않는다.

## 4. checkpoint 의미 (사전 등록)

- **`epoch = -1`**: 진짜 학습 전 상태. optimizer step 0, `alpha` 정확히 0,
  출력이 morphology offset과 **동일**(loop가 assert). 모든 selector의 후보.
- **`epoch = 0`**: 첫 전체 학습 epoch 완료 후.
- **`epoch >= 1`**: 이후 각 epoch 완료 후.

`best_loss = inf`로 epoch 0을 자동 채택하는 Q4-O 방식은 진단 loop에서 쓰지
않는다. Q4-O의 과거 결과·artifact는 소급 변경하지 않는다.

## 5. 사전 등록 trajectory와 schedules

조기 종료가 원인을 가리지 않도록 **모든 schedule이 고정 24 epoch를 전부
실행**하고 전체 trajectory를 저장한다. patience는 어떤 형태로도 optimizer
실행을 중단시키지 않는다(테스트가 checkpoint 수 = 24 + 1을 assert).

정확히 다음 **세 schedule만** 사용한다. 결과를 본 뒤 LR·scheduler·architecture
추가는 금지. `alpha=1`/zero-head 등 parameterization 변경은 차기 분기로만 남긴다.

| schedule | CNN trunk/head LR | alpha LR |
|---|---|---|
| `S0_original` | Adam `1e-3` | `1e-3` (Q4-O 원본과 수학적으로 동일) |
| `S1_global_low` | Adam `3e-4` | `3e-4` |
| `S2_alpha_low` | Adam `1e-3` | `1e-4` |

Arm C와 D 모두에 적용한다. weight decay는 전 그룹 `1e-4` 고정.

## 6. selectors (같은 trajectory 위에서, dev만으로)

| selector | 정의 | 역할 |
|---|---|---|
| `SEL0_pooled_bce` | pooled dev beat BCE 최소 | Q4-O 규칙 + epoch −1 후보화 |
| `SEL1_record_bce` | record별 BCE → record 간 단순 평균 최소 | **primary diagnostic** |
| `SEL2_record_ksweep` | dev record-level k-sweep 최대 | sensitivity only |

- 셋 모두 **epoch −1을 후보에 포함**한다.
- tie tolerance 사전 등록: BCE류 `1e-6`, k-sweep `1e-6`. tolerance 내 tie는
  **가장 이른 checkpoint**(−1 포함)를 선택한다.
- selector는 `dev_*` 필드만 읽는다(테스트가 test 필드 변조 불변성을 검증).

## 7. checkpoint별 필수 기록 (arm × schedule × seed × fold)

epoch −1 및 모든 epoch에 대해: optimizer step count · train pooled BCE ·
dev pooled BCE · dev record-balanced BCE · dev record k-sweep · dev record
macro PR-AUC · `alpha` 와 `|alpha|` · `effective_residual = alpha × cnn_residual`
의 mean / SD / mean-abs / p95-abs (dev) · offset과 effective residual의 상관 ·
wall time. 추가로 첫 **100 optimizer step**의 alpha/head/trunk gradient norm과
update norm, fit/dev prevalence·beat 수·record 수, GPU·package 정보(manifest).

**해석 규칙(사전 등록)**: `alpha`의 부호는 head 부호와 함께 뒤집힐 수 있으므로
부호 자체를 seed 불안정성으로 해석하지 않는다. 해석 대상은 effective residual.

## 8. test 평가 경계

schedule/selector checkpoint가 **dev만으로 확정된 후** outer-test를 평가한다.
per-checkpoint test logits 전체 trajectory는 저장하되 **exploratory**로 표시하고
schedule 선택이나 baseline 승격에 사용하지 않는다. 주요 비교(모두 Q4-O와 동일한
patient-level paired record bootstrap + hierarchical bootstrap + five-seed 집계):

- `C(schedule, selector) − A` · `D(schedule, selector) − A` · `C − D`
- `P(best_epoch = −1)` / `P(= 0)` / `P(> 0)` 분포
- S1/S2가 S0 대비 선택 epoch를 뒤로 이동시키는가
- 개선이 C 특이적인가, D에도 동일한가

여러 schedule 중 **test 최고값만 headline으로 선택하는 것을 금지**한다(보고서와
`c_vs_d_by_schedule.png`는 전체 schedule × selector를 항상 병기).

## 9. 사전 등록 원인 decision tree

`report_summary.md`와 `decision_matrix.png`는 아래 분기를 그대로 판정한다.
구현: `evaluate_decision_tree()` — 복수 발화는 `MULTIPLE_CAUSES`, 무발화는
`UNDECIDED`로 보고하며 하나를 억지로 선택하지 않는다(테스트가 fixture로 검증).

1. **B1 즉시 유해/신호 부족**: epoch −1이 C의 대부분(≥50%) seed×fold에서
   best이고 C−D도 개선되지 않음(≤0).
2. **B2 첫 epoch 후 과적합**: epoch 0이 −1보다 dev에서 좋고, train loss는
   감소하며, 이후 record-balanced dev loss가 악화(각 조건 과반).
3. **B3 LR/alpha overshoot**: S1 또는 S2에서 best epoch가 뒤로 이동하고 dev
   개선과 함께 test C−D가 S0보다 개선.
4. **B4 selector mismatch**: SEL1이 SEL0보다 patient-level dev와 paired
   outer-test 모두에서 일관되게 나음.
5. **B5 waveform 비특이적 schedule artifact**: schedule 개선이 C와 D에
   비슷하게 나타나고 C−D가 남지 않음.
6. **B6 실제 waveform residual 후보**: C가 D보다 일관되게 우수 — C−D CI 하한
   > 0, seed 방향 안정(≥4/5), lower-tail(p10) 미악화가 동시 성립.

## 10. 필수 산출물 계약 (향후 full run이 생성)

`config.json` · `manifest.json` · `result.json` · `fold_map.json` ·
`predictions.npz`(arm×schedule×selector 확정 test logits + Arm A) ·
`training_history.json`(전 trajectory) · `arms/<arm>/<schedule>/<selector>/probs.npy` ·
`checkpoint_table.csv` · `trajectory_table.csv` · `figures/report_summary.md` ·
그림 9종: `learning_curves_by_schedule.png` · `pretrain_vs_epoch0.png` ·
`best_epoch_distribution.png` · `alpha_and_effective_residual.png` ·
`gradient_update_diagnostics.png` · `selector_disagreement.png` ·
`c_vs_d_by_schedule.png` · `patient_delta_waterfall.png` · `decision_matrix.png`

표시 규칙: 평균만 그리지 않는다 — seed/fold 궤적과 분산을 표시한다. epoch −1과
epoch 0은 모든 표·그림에서 시각적으로 구분한다(빨강/주황 고정 팔레트).
reporting은 측정 artifact를 SHA256 fingerprint로 전후 비교하고 변화 시 raise.
history가 없는 과거 run(Q4-O `20260806T0923` 포함)에 `training_history.json`을
소급 생성하지 않는다.

## 11. 테스트 계약 (CPU에서 실행됨 — full GPU run 아님)

`mit-bih/test_q4p_best_epoch_zero_diagnostic.py`가 최소한 다음을 자동 검증한다:

- epoch −1 output == morphology offset · alpha == 0 · optimizer step == 0
- epoch 0 optimizer step > 0
- 모든 selector가 epoch −1을 후보에 포함, tolerance 내 tie는 최이른 checkpoint
- selector가 dev 정보만 사용(test 필드 변조 불변)
- best checkpoint == selector 정의의 argmin/argmax
- S2의 alpha LR(1e-4)과 CNN/head LR(1e-3) 정확성 — optimizer param group 검사
- schedule 간 paired initialization과 minibatch order(step-0 gradient 동일성)
- shuffled D가 record 경계를 넘지 않음
- outer-test label 뒤집기가 selection·dev 궤적·test logits에 무영향
- patience가 optimizer를 중단시키지 않음(checkpoint 수 = epochs + 1)
- reporting 전후 measured artifact 불변(fingerprint)
- history 없는 run에 history를 만들지 않음
- synthetic fixture가 B1~B6, MULTIPLE_CAUSES, UNDECIDED를 분리
- CPU synthetic smoke run이 전체 번들 스키마·그림·decision matrix를 생성

## 12. notebook UX (`notebooks/quest48_q4p_best_epoch_zero_diagnostic.ipynb`)

- 모드: `DESIGN_ONLY`(기본 True) / `SMOKE` / `FULL_RUN` / `ANALYZE_EXISTING_RUN`
  — **동시에 정확히 하나만** 활성(assertion).
- full run 전: data SHA · git SHA · output path · arm/schedule/seed/fold 수 ·
  예상 runtime을 출력하고, 진행률과 ETA를 표시한다.
- 실행 후 표·원인 판정·핵심 그림을 notebook 안에 즉시 표시한다.
- stale import, Drive mount 실패, incomplete bundle은 hard fail.
- 실제 실행 전 결과 칸은 **`NOT RUN`**이며 가짜 수치를 절대 표시하지 않는다.

## 13. Q4-O와의 경계

- Q4-O 측정 artifact(`config/manifest/result/fold_map/predictions/arms`)를
  수정·재생성하지 않는다. Q4-O 재학습 금지.
- 이 브랜치의 변경 파일은 정확히 4개 신규 파일뿐이다: 본 spec,
  `mit-bih/q4p_best_epoch_zero_diagnostic.py`,
  `mit-bih/test_q4p_best_epoch_zero_diagnostic.py`,
  `notebooks/quest48_q4p_best_epoch_zero_diagnostic.ipynb`.

## Decision log

### 2026-08-08 — 설계 등록 (결과 없음)

이 spec과 구현·테스트·notebook을 사전 등록한다. CPU unit + synthetic smoke
테스트만 실행되었고(파이프라인 배관 검증), **full GPU run은 실행되지 않았다**.
smoke의 어떤 수치도 과학적 의미가 없다. GO/NO-GO형 판정 자체가 없는 진단
실험이며, 산출물은 원인 분리 decision tree의 발화 패턴이다.

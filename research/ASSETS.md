# ECG assets registry

Do not move existing assets during inventory. Old Colab notebooks may contain hard-coded paths.
Record one row per asset or run. Add hashes for immutable files when feasible.

Drive root: `MyDrive/MedKOS/ecg-model/`

| Asset ID | Kind | Current Drive path | GitHub consumer | Status | Hash/version | Notes |
|---|---|---|---|---|---|---|
| run-20260806-q4n | run | `MyDrive/MedKOS/ecg-model/runs/20260806T0130_quest46_q4n_scope_rank_vector/` | `notebooks/quest46_q4n_scope_rank_vector.ipynb` | needs verification | pending | Latest known run reference |
| registry | run index | `MyDrive/MedKOS/ecg-model/registry.jsonl` | experiment intake | needs inventory | append-only | run_id, value, pass/fail, conclusion, folder |
| run-helper | library | `MyDrive/MedKOS/ecg-model/lib/medkos_run.py` | Colab notebooks | needs inventory | pending | shared run writer |
| run-20260806-q4o | run | `MyDrive/MedKOS/ecg-model/runs/20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn/` | `notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb` | verified (MEASURED, NO-GO) | run commit `624e987b917ec021c9fc2130f37f6f35e720601c` | Q4-O leakage-free residual; immutable — no retroactive `training_history.json` |
| run-20260808-q4p | run | `MyDrive/MedKOS/ecg-model/runs/20260808T1310_EXP-2026-002_q4p_best_epoch_zero_diagnostic/` (folder id `1qS8JxwlARByoZrJLMb6wxSIktQypiRTF`) | `notebooks/quest48_q4p_best_epoch_zero_diagnostic.ipynb` | verified (MEASURED, verdict B3) | code SHA `a4e24f4d662b3a93727f6a3413e594b51cc6205e` · data SHA `892f6ae9…5a85` | 56 scorable records, T4, 66.1 min; predictions.npz는 y_true/record_id 포함 자립적 — 파생 분석 입력 |
| data-svdb5 | dataset (processed) | `MyDrive/mitbih/svdb_data5.npz` | Q4-O/Q4-P 모듈 | frozen | SHA256 `892f6ae9635db9bf715272c323a3c0e62e71693608bf66ca4dc9b66b69915a85` (452,578,759 B) | SVDB 184,499 beats · 78 records; Q4-O/Q4-P의 유일 데이터 |
| data-mit-mamba | dataset (processed) | `MyDrive/mitbih/mamba_data.npz` (file id `1p3HvC_bnbiQlEanFOVIvVdejy60W0tho`) | Q4-Q (EXP-2026-003) 1차 cohort | frozen; audit PASS (2026-08-08) | SHA256 `b1c16106216522cb21291f990e7ab0e7f8dfd8135406db322f41cda3687f6c05` (204,504,913 B) | 99,871 beats · 44 records · DS1 22/DS2 22 · overlap 없음. 주의: record 208·213은 ecg_multi 대비 beat −12.7%/−11.1%(전처리 필터 차, 감사표 기록) |
| run-20260808-q4q | run | `MyDrive/MedKOS/ecg-model/runs/20260808T1842_EXP-2026-003_q4q_transportability_replication/` (folder id `1ZCAYZCl4T4eoZzdFfV_IzkB0Mgbcqlw4`) | `notebooks/quest49_q4q_transportability_replication.ipynb` | verified (MEASURED; mechanism+utility fail → residual CNN 중단) | code SHA `579fed7e72d1f4518a28fb2698249da1094cef3a` | MIT DS1→DS2, SEL1, S0/S2, L4 237.7s |
| run-20260808-q4q-prep | data audit | `MyDrive/MedKOS/ecg-model/runs/20260808T1838_EXP-2026-003_prep_data/` | Q4-Q PREP_DATA gate 기록 | verified (gate PASS) | — | cross-check 표(44 matched·4 paced·S 불일치 0)·INCART 75→32 map JSON |
| run-20260808-q4p-derived | derived analysis | `MyDrive/MedKOS/ecg-model/runs/20260808T1838_EXP-2026-002_q4p_derived_analysis_v1/` | Q4-P 사후 기전 분석 | verified (post-hoc; B3 판정 불변) | 원본 Q4-P bundle fingerprint 불변 확인 | DiD (C−D) S2−S0 +0.003434 [−0.000815, +0.008587] (SVDB k-sweep) |
| data-mitdb-cache | annotation/header cache | `MyDrive/mitbih/raw_ann/mitdb/` (folder id `151DJAcjCbDXCoy9ZIPudbtSuVziG1fnj`) | provenance 참조 · Q5-A symbol 복구 | verified (2026-08-09) | `.hea` + `.atr`, `.dat` 없음 | 360 Hz · 2 leads; 이 폴더만으로 waveform 재구축 불가. **경로 정정**: 이전 표기 `MyDrive/mitbih/mitdb/` 는 틀렸다 — 실제 부모는 `raw_ann`(folder id `1jJSQbAcaVzA1cw2vIL0h3A4cOT-PR-lb`). **2026-08-09 실측: `t`↔`.atr` sample 조인은 성공률 1.9% = 우연 수준**(최근접 주석까지 중앙 거리 0.222×RR)이므로 `t`는 annotation sample index가 아니다 → 이 경로로는 symbol 복구 불가. 대안 후보는 `ecg_multi.npz`의 `sym`을 waveform fingerprint로 대조하는 것(Q5-B-0 제안) |
| baseline-v10-pwave-run | model run (legacy ablation) | `MyDrive/mitbih/ablation_step9d/pwave/ens.npz` | `mit-bih/colab_step9d_final.py :: run_final("pwave")` | **별개 계보 — Q5-A baseline 아님** (2026-08-09 정정) | keys `prob`(n,3)·`y`·`pid`; seeds 1000–1004 앙상블 평균 | DS2만 채점 · annotation index 없음 → Q5-A가 `mamba_data.npz`(SHA `b1c16106…`)와 `pid`·`y` 전량 대조로 행 대응을 검증한 뒤 `t`로 키 부여. per-seed 미저장 → seed variability 산출 불가 |
| baseline-base26-control | model run (legacy ablation) | `MyDrive/mitbih/ablation_step9d/base26/ens.npz` | `colab_step9d_final.py :: run_final("base26")` | **별개 계보 — Q5-A baseline 아님** (2026-08-09 정정) | 동일 스크립트·seed·저울 | V10과 **P파 특징 블록만** 다른 짝 대조군(`use_pw = tag=="pwave"`). 이름이 같은 `ablation_step11/base26`·`ablation_step13/base26`과 혼동 금지 — Q5-A는 primary와 같은 parent run으로만 범위를 좁힌다 |
| data-ecg-multi | dataset (processed, 통합) | `MyDrive/mitbih/ecg_multi.npz` (file id `1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq`) | Q4-Q PREP_DATA 교차 검증 · **Q5-B-0 symbol source** | audit at PREP_DATA | ~1.17 GB · 예상 keys `beat,y5,y3,y,pid,db,sym,pre_rr,post_rr,rhythm,…` | mitdb+svdb+incart 통합; MIT subset을 mamba_data와 교차 검증 (불일치 미해명 시 중단). **`sym`을 가진 유일한 파일** → Q5-B-0가 `(pre_rr, post_rr)` 초 단위 키로 S beat만 조인해 원 symbol(A/a/J/S)을 복구하려는 대상. waveform(`beat`)은 읽지 않는다 |
| data-incart-npz | dataset (processed) | `MyDrive/…/incart_data.npz` (file id `1e9uUOrEXoKnylFLDSAd5Qdx55GZRhXRg`) | Q4-Q 2차 조건부 cohort | **blocked**: patient map gate | ~425.6 MB · keys `beat,y,pid,pre_rr,post_rr` | 175,571 beats · 75 records. **`pid`는 record-level(75) — 실제 32 patients와 다름. patient bootstrap/group split에 그대로 사용 금지** |
| data-incart-cache | annotation/header cache | `MyDrive/raw_ann/incartdb/` (folder id `1rNgzVlVYuiBDBfSjhHXm-Ksbw54nKfgM`) | Q4-Q INCART patient map | header-only | 75 `.hea` + 75 `.atr`, `.dat` 없음 | header 주석 `# patient N` 실측 확인(I01) — 75→32 map의 source of truth |
| data-incart-hea | header cache | `MyDrive/…/incart/` (folder id `1LEuS8hBbzN2kNMwqZaHWvYqZY5hGU979`) | 참조 | header-only | 75 `.hea` | 257 Hz · 12 leads · 462,600 samples |
| run-q5a-inventory | analysis input index | `MyDrive/MedKOS/ecg-model/runs/20260809T1030_EXP-2026-004_q5a_inventory/` | `notebooks/quest50_q5a_patient_failure_atlas.ipynb` (mode `INVENTORY`) | verified (gate PASS, 2026-08-09) | 모듈 q5a v8 | 203 후보 artifact 표(`source_inventory.json/csv`)와 `baseline_freeze.json`(4개 `FROZEN`). 읽기 전용 스캔 — 기존 폴더를 수정하지 않았다. 이전 run(`…T0037`·`…T0717`~`…T1009`)은 모듈 v2~v7 이력이며 결과 인용 금지 |
| run-q5a-atlas | derived analysis (no training) | `MyDrive/MedKOS/ecg-model/runs/20260809T1033_EXP-2026-004_q5a_patient_failure_atlas/` (folder id `1ZSXZnLbqpvxM0TStK_n8jYf0mAZRUwzB`) | `mit-bih/q5a_patient_failure_atlas.py` · `notebooks/quest50_q5a_patient_failure_atlas.ipynb` | **verified (MEASURED; 판정 `UNRESOLVED` / D5)** | 모듈 q5a v8 · `training_performed: false` | 17-file bundle. 자격 block 없음(`qualified: []`); 순위 `B_PATIENT` +0.0491 > `B_QUALITY` +0.0173 > `B_RR` −0.0300 > `B_ATRIAL` −0.0955. `B_SUBTYPE`은 `.atr` 조인 1.9%(우연 수준)로 측정 불가. worst-quartile 전 쌍 최소 overlap 0.333 → D4 미발화. 원본 bundle fingerprint 불변 확인 |
| baseline-v9-pkg | model run (원 실행 패키지) | `MyDrive/mitbih/baseline_pkgs/v9pkg_results/` (`<arm>_s<seed>.npz` 25개 + arm별 `metrics.json`) | `v9pkg/v9_ECG.ipynb` · Q5-A primary(V9) | **verified (2026-08-09)** | kink_noctx **0.5969 ± 0.0411** (기록 0.597 ± 0.041), v8base 0.5762, kink 0.5341, kink_noproto 0.4595, v8_noc 0.4258 | 5 arm × 5 seed(1000–1004) 확률 원값 보존 → **재학습 없이 전량 재현**. DS2 49,289박(N/S/V 44,232/1,837/3,220). 짝 대조군은 같은 패키지의 `v8base`. 로컬 보관본을 2026-08-09 업로드 |
| baseline-v10-pkg | model run (원 실행 패키지) | `MyDrive/mitbih/baseline_pkgs/v10pkg_results/` | `v10pkg/v10_ECG.ipynb` · Q5-A primary(V10) | **verified (2026-08-09)** | pwave **0.6603** (기록 0.660), full 0.6541, v8base 0.5984, base 0.5732, pwave_noc 0.5619 | **0.660의 단위 = 시드별 PR-AUC의 평균**(같은 확률의 시드 앙상블 PR-AUC는 0.7717 — 혼동 금지). 짝 대조군은 같은 패키지의 `base`. V9와 DS2 동일, atlas와 19/22 record 일치(105·111·222는 N beat만 −1/−1/−4) |
| run-q5b0-recovery | derived analysis (no training) | `MyDrive/MedKOS/ecg-model/runs/<ts>_EXP-2026-005_q5b0_subtype_key_recovery/` | `mit-bih/q5b0_subtype_key_recovery.py` · `notebooks/quest51_q5b0_subtype_key_recovery.ipynb` (mode `RECOVER`) | **planned — NOT RUN** | — | S beat ↔ `ecg_multi.npz` 조인 + 음성대조군(permutation·shift·wrong-record) + GO/NO-GO gate. `recovered_symbols.npz`로 복구 symbol을 보존해 재분석이 별도 run으로 성립한다. **GO든 NO-GO든 전체 bundle을 쓴다** — NO-GO면 `B_SUBTYPE` 영구 종결 |
| run-q5b0-reanalysis | derived analysis (no training) | `MyDrive/MedKOS/ecg-model/runs/<ts>_EXP-2026-005_q5b0_subtype_reanalysis/` | 위와 동일 (mode `REANALYZE`) | **planned — NOT RUN (GO 조건부)** | — | Q5-A의 `run_atlas`를 **그대로** 호출해 5개 블록으로 decision tree 재평가. bundle은 Q5-A의 17-file 계약 + `q5b0_recovery.json`. 내부 `config.json`이 `EXP-2026-004`로 표기되는 것은 재분석 주체가 Q5-A atlas이기 때문 |
| data-incart-raw | raw (partial) | `MyDrive/…/incart_raw/` (folder id `1y9lpT_0unM04PJRMIUhUcmABTGNB_eqY`) | 필요 시 adapter audit | **partial** | 142 files: I01–I47 triplets + I48 `.dat` only | 전체 75-record raw archive 아님. 필요 시 wfdb로 Colab 임시/새 versioned 폴더에 다운로드 — 이 폴더 덮어쓰기 금지 |

## Intake checklist
For every important run, confirm:
- `config.json`
- `manifest.json`
- `result.json`
- `log.txt`
- `figures/`
- `arms/<arm>/probs.npy`
- matching executed GitHub notebook
- matching ingested log card

## Migration rule
Create a dedicated migration spec before changing any registered path. It must list every consumer, old/new paths, copy-first procedure, validation, and rollback. Delete or retire the old location only after all consumers pass.

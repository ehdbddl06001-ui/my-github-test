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
| data-mit-mamba | dataset (processed) | `MyDrive/mitbih/mamba_data.npz` (file id `1p3HvC_bnbiQlEanFOVIvVdejy60W0tho`) | Q4-Q (EXP-2026-003) 1차 cohort | frozen; audit at PREP_DATA | ~204.5 MB · keys `beat,ref,feats,y,pid,t` | 99,871 beats · 44 records · DS1 22/DS2 22 · overlap 없음. raw 재다운로드 불필요 |
| data-mitdb-cache | annotation/header cache | `MyDrive/mitbih/mitdb/` (folder id `151DJAcjCbDXCoy9ZIPudbtSuVziG1fnj`) | provenance 참조 | header-only | 48 `.hea` + 48 `.atr`, `.dat` 없음 | 360 Hz · 2 leads; 이 폴더만으로 waveform 재구축 불가 |
| data-ecg-multi | dataset (processed, 통합) | `MyDrive/mitbih/ecg_multi.npz` (file id `1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq`) | Q4-Q PREP_DATA 교차 검증 | audit at PREP_DATA | ~1.17 GB · 예상 keys `beat,y5,y3,y,pid,db,sym,pre_rr,post_rr,rhythm,…` | mitdb+svdb+incart 통합; MIT subset을 mamba_data와 교차 검증 (불일치 미해명 시 중단) |
| data-incart-npz | dataset (processed) | `MyDrive/…/incart_data.npz` (file id `1e9uUOrEXoKnylFLDSAd5Qdx55GZRhXRg`) | Q4-Q 2차 조건부 cohort | **blocked**: patient map gate | ~425.6 MB · keys `beat,y,pid,pre_rr,post_rr` | 175,571 beats · 75 records. **`pid`는 record-level(75) — 실제 32 patients와 다름. patient bootstrap/group split에 그대로 사용 금지** |
| data-incart-cache | annotation/header cache | `MyDrive/raw_ann/incartdb/` (folder id `1rNgzVlVYuiBDBfSjhHXm-Ksbw54nKfgM`) | Q4-Q INCART patient map | header-only | 75 `.hea` + 75 `.atr`, `.dat` 없음 | header 주석 `# patient N` 실측 확인(I01) — 75→32 map의 source of truth |
| data-incart-hea | header cache | `MyDrive/…/incart/` (folder id `1LEuS8hBbzN2kNMwqZaHWvYqZY5hGU979`) | 참조 | header-only | 75 `.hea` | 257 Hz · 12 leads · 462,600 samples |
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

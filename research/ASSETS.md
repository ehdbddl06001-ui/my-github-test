# ECG assets registry

Do not move existing assets during inventory. Old Colab notebooks may contain hard-coded paths.
Record one row per asset or run. Add hashes for immutable files when feasible.

Drive root: `MyDrive/MedKOS/ecg-model/`

| Asset ID | Kind | Current Drive path | GitHub consumer | Status | Hash/version | Notes |
|---|---|---|---|---|---|---|
| run-20260806-q4n | run | `MyDrive/MedKOS/ecg-model/runs/20260806T0130_quest46_q4n_scope_rank_vector/` | `notebooks/quest46_q4n_scope_rank_vector.ipynb` | needs verification | pending | Latest known run reference |
| registry | run index | `MyDrive/MedKOS/ecg-model/registry.jsonl` | experiment intake | needs inventory | append-only | run_id, value, pass/fail, conclusion, folder |
| run-helper | library | `MyDrive/MedKOS/ecg-model/lib/medkos_run.py` | Colab notebooks | needs inventory | pending | shared run writer |

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

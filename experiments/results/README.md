# Drive experiment intake

This directory stores only small, versionable summaries. Raw datasets, checkpoints, and large probability arrays remain in Google Drive.

## Intake procedure

1. Mount Drive in Colab.
2. Select one run from `MyDrive/MedKOS/ecg-model/registry.jsonl`.
3. Verify its complete bundle and matching executed notebook.
4. Copy only the small `result.json` to a temporary Colab working path if required.
5. Commit the executed notebook under `notebooks/`.
6. Run:

```bash
python pipelines/ingest_run.py --results result.json --notebook notebooks/<executed>.ipynb
```

7. Update `research/ASSETS.md` and `research/PROJECT_STATE.md` through the same PR.

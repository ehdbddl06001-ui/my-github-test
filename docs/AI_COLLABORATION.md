# AI collaboration workflow

## Shared loop

1. Codex writes an experiment spec in `experiments/specs/`.
2. The user approves the design or requests changes.
3. The named implementation owner (Claude Code or Codex) creates its own branch.
4. The owner implements code and tests without changing the scientific question silently.
5. The user runs GPU experiments in Colab.
6. Colab saves the complete run bundle in Google Drive.
7. The executed notebook and `result.json` are ingested into GitHub.
8. Codex reviews statistics, leakage, reproducibility, and failure patients.
9. Findings and the project state are updated through a PR.

## Task ownership

| Work | Default owner |
|---|---|
| Hypothesis, comparator, stopping rule, statistics | Codex |
| Initial implementation from an approved spec | Claude Code |
| Small fixes, tests, refactors | Either, one owner per task |
| Colab GPU execution | User |
| Result interpretation and next experiment | Codex |
| Implementation revision | Claude Code or assigned owner |

## Handoff contract

A coding request is ready only when its spec includes:
- exact input and output paths;
- dataset and patient split;
- baseline and changed variable;
- primary/secondary metrics;
- seeds and reproducibility controls;
- acceptance and stopping criteria;
- expected Drive run directory;
- files allowed to change;
- implementation owner.

Claude Code must write implementation notes and test commands into the same spec's Decision log or PR.
Codex must not declare an experiment successful until it reads an executed notebook and measured result.

## Branches

- `codex/<task>`: Codex-owned design or implementation
- `claude/<task>`: Claude Code implementation
- `agent/<task>`: shared infrastructure or maintenance
- `main`: reviewed, reproducible state

Never let two agents work in the same branch at the same time. Exchange work through commits or PRs.

## Google Drive and Colab

Drive root: `/content/drive/MyDrive/MedKOS/ecg-model/`

New run layout:

```text
runs/<timestamp>_<experiment_id>/
  config.json
  manifest.json
  result.json
  log.txt
  figures/
  arms/<arm>/probs.npy
```

Append one summary record to `registry.jsonl`: run_id, primary value, pass/fail, one-line conclusion, and run folder.
Keep large files in Drive. Commit only small results, executed notebooks, source code, and references to Drive assets.
Existing assets stay in place until a migration spec is approved.

## VS Code quick use

Open the cloned repository folder in VS Code. Use one integrated terminal per agent, but never run both agents on the same branch.
Before starting either agent:

```bash
git switch main
git pull origin main
```

For Claude Code:

```bash
git switch -c claude/<task>
claude
```

For Codex:

```bash
git switch -c codex/<task>
codex
```

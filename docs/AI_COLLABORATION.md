# AI collaboration workflow (ecg-lab)

## Two repositories, one user

| Repository | Contains | Agents work on |
|---|---|---|
| `ehdbddl06001-ui/ecg-lab` (this one) | ECG experiments, specs, research state | experiment code, specs, reviews |
| `ehdbddl06001-ui/my-github-test` (MedKOS) | study content, pipelines, homepage | study cards, pipelines, site |

One task lives in one repository. If a task needs both — for example an AI-lab quest card in
MedKOS that queues an experiment here — split it into two tasks and link them by URL. Never
open a PR that touches both repositories, and never copy experiment code into MedKOS.

## Shared loop

1. Codex writes an experiment spec in `experiments/specs/`.
2. The user approves the design or requests changes.
3. The named implementation owner (Claude Code or Codex) creates its own branch.
4. The owner implements code and tests without changing the scientific question silently.
5. The user runs GPU experiments in Colab.
6. Colab saves the complete run bundle in Google Drive.
7. The executed notebook and `result.json` are committed here.
8. Codex reviews statistics, leakage, reproducibility, and failure patients.
9. Findings and `research/PROJECT_STATE.md` are updated through a PR.

## Task ownership

| Work | Default owner |
|---|---|
| Hypothesis, comparator, stopping rule, statistics | Codex |
| Initial implementation from an approved spec | Claude Code |
| Small fixes, tests, refactors | Either, one owner per task |
| Colab GPU execution | User |
| Result interpretation and next experiment | Codex |
| Implementation revision | Claude Code or assigned owner |
| Acceptance review of an implementation | Codex (review only, no execution) |

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

Claude Code must write implementation notes and test commands into the same spec's Decision
log or PR. Codex must not declare an experiment successful until it reads an executed
notebook and a measured result.

Handoffs are committed as `research/HANDOFF_<date>_<topic>_to_<recipient>.md`, built from the
templates in `prompts/`. That file is the record — do not hand off only in chat.

## Branches

- `codex/<task>`: Codex-owned design or implementation
- `claude/<task>`: Claude Code implementation
- `agent/<task>`: shared infrastructure or maintenance
- `main`: reviewed, reproducible state

Never let two agents work in the same branch at the same time. Exchange work through commits
or PRs. No direct pushes to `main` in this repository.

## Google Drive and Colab

Drive root: `/content/drive/MyDrive/MedKOS/ecg-model/`
(The Drive path keeps the `MedKOS` name after the repository split — old notebooks depend on
it. Renaming it requires a migration spec.)

Run layout:

```text
runs/<timestamp>_<experiment_id>/
  config.json
  manifest.json
  result.json
  log.txt
  figures/
  arms/<arm>/probs.npy
```

Append one summary record to `registry.jsonl`: run_id, primary value, pass/fail, one-line
conclusion, and run folder. Keep large files in Drive. Commit only small results, executed
notebooks, source code, and references to Drive assets. Existing assets stay in place until a
migration spec is approved.

## VS Code quick use

Open the cloned repository folder in VS Code. Use one integrated terminal per agent, but
never run both agents on the same branch.

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

Running both repositories at once? Open them as **two separate VS Code windows**, one folder
each. A single window with both folders lets an agent write across the split by accident.

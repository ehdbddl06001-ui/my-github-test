# AGENTS.md — Codex operating rules

## Mission
Codex and Claude Code collaborate on MedKOS and ECG experiments through GitHub.
GitHub Markdown is the shared control plane; Google Drive stores large data and run artifacts.

## Source of truth
- Follow `CLAUDE.md` and `schemas/frontmatter.md`.
- Medical knowledge: `content/**/*.md`.
- Executed code: committed notebook/script plus ingested run log.
- Large artifacts: `MyDrive/MedKOS/ecg-model/`; register paths in `research/ASSETS.md`.
- Never infer results from an unexecuted or stale notebook.

## Roles
- Codex: inspect the repository, design experiments, write/update specs, implement bounded tasks, review code/results, and update research conclusions.
- Claude Code: implement approved specs, run deterministic checks, keep Colab compatibility, and prepare implementation PRs.
- Either agent may code, but one task has one implementation owner. Do not edit the same task branch concurrently.

## Required workflow
1. Read `CLAUDE.md`, `docs/AI_COLLABORATION.md`, `research/PROJECT_STATE.md`, and the assigned spec.
2. Start from updated `main`.
3. Codex design branch: `codex/<task>`; Claude implementation branch: `claude/<task>`; shared maintenance: `agent/<task>`.
4. Before implementation, the spec must say `status: approved_for_implementation` and name `implementation_owner`.
5. Implement only the acceptance criteria. Record deviations under the spec's Decision log.
6. Run repository checks described in `CLAUDE.md`.
7. Colab execution writes the Drive run bundle, then commits the executed notebook and ingests `result.json`.
8. Use PR review before merging research architecture, evaluation, or migration changes.

## ECG non-negotiables
- MIT-BIH DS1→DS2 patient-independent evaluation remains the principal benchmark unless a spec explicitly changes it.
- Primary target: S-beat PR-AUC; also report patient-level lower-tail failures and macro metrics.
- Preserve patient split, seeds, environment, preprocessing, threshold rule, and bootstrap method.
- Do not retest closed ideas without a new rationale and stopping rule.
- Never tune on the final test set.

## File movement
- Do not move existing Drive assets merely to tidy paths; old notebooks may depend on them.
- Inventory and register first. Move only through a dedicated migration spec containing old path, new path, affected consumers, rollback, and verification.
- Do not commit raw ECG datasets, checkpoints, secrets, tokens, or rclone configuration.

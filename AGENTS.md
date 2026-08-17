# AGENTS.md — Codex operating rules (MedKOS)

## Mission
This repository is MedKOS: a personal medical knowledge platform (KMLE/USMLE questions,
paper cards, anatomy, disease/drug cards, and the AI-lab **study** track) plus the
deterministic pipelines and the static site that publish it.

ECG arrhythmia **research** moved to `ehdbddl06001-ui/ecg-lab` on 2026-08-17.
Experiment specs, experiment code, research handoffs and quest notebooks live there.

## Repository boundary — read this first

| Task | Repository |
|---|---|
| Study card, exam question, paper card, anatomy set | **here** |
| Pipeline, indexer, exporter, site, skill, routine | **here** |
| AI-lab weekly card, run log, quest roadmap, mentor note | **here** (`content/ailab/`) |
| Experiment spec, experiment code, measured result, research conclusion | **ecg-lab** |

One task lives in one repository. Never open a PR that touches both. If an AI-lab quest card
here needs a real experiment, queue it here and link the ecg-lab spec **by URL** — relative
paths do not resolve across repositories.

## Source of truth
- Follow `CLAUDE.md` and `schemas/frontmatter.md`. `CLAUDE.md` wins on conflict.
- Medical knowledge: `content/**/*.md`. `db/` and Google Drive are derived.
- Executed code: the committed notebook plus its ingested run log (`kind: log`).
- Never infer results from an unexecuted or stale notebook. `pipelines/ingest_run.py`
  writes measured numbers; an LLM does not type them in.

## Non-negotiables
- Every `.md` carries frontmatter per `schemas/frontmatter.md`.
- Deterministic work — parsing, DB writes, ID issuing, counting, file moves — goes through
  `pipelines/*.py`. An agent does not do it by hand.
- Exam questions keep answers separated from the stem (`answer_separated: true`).
- Never write to the database directly. Never store content outside `content/`.
- Never reuse or roll back an id.
- Anatomy source PDFs, page images and masks stay in `.private/` and are never committed.
- Conflicting sources: keep source/edition/date and lower `confidence` instead of picking one.

## Required workflow
1. Read `CLAUDE.md`, and the spec if the task names one.
2. Start from updated `main`.
3. Codex branch: `codex/<task>`; Claude Code branch: `claude/<task>`; shared: `agent/<task>`.
   Two agents never edit the same branch or the same file concurrently.
4. Publish with one command: `python pipelines/publish.py -m "<message>"`.
   It validates frontmatter, rebuilds the index and the `docs/` bundle, merges `main`, and
   pushes. Doing the steps by hand drops one of them — that has actually happened.
5. `publish.py` splits lanes by path. Content (`content/**`, `docs/**`, `notebooks/**`,
   `state/ailab_progress.json`) pushes to `main` directly. Code (`pipelines/**`,
   `.claude/**`, `CLAUDE.md`, `schemas/**`, everything else) is refused on `main` — use
   `--branch claude/<task>` or `codex/<task>`, open a PR, and **merge it in the same
   session**. An unmerged PR means the next day's routine rebuilds the same files from
   scratch (measured 2026-08-17).
6. Exam questions are never published on a branch — that path is blocked on purpose, because
   PR-routed questions caused duplicate id issuance.

## Tests
```bash
python pipelines/indexer.py --check     # frontmatter validation
python pipelines/test_anatomy.py
python pipelines/test_state.py
python pipelines/test_datasets.py
python pipelines/test_deepen.py
python pipelines/test_landmark.py
python pipelines/merge_state.py --selftest
python pipelines/publish.py --selftest
```

## File movement
- Do not move Drive assets merely to tidy paths; old notebooks depend on them.
  Drive root `MyDrive/MedKOS/ecg-model/` keeps its name after the repository split.
- Do not commit secrets, tokens, rclone configuration, raw datasets, or checkpoints.
- `db/*.sqlite` is derived and gitignored — rebuild with `indexer.py`, never commit.

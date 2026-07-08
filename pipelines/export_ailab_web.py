"""
export_ailab_web.py — content/ailab/**/*.md(원본) + datasets.py(오픈데이터·주차)를
홈페이지 🤖 AI랩 피드용 JS 번들로 내보낸다.

MedKOS 원칙: Markdown이 원본, docs/ailab.js는 파생물. export_papers_web.py 와 대칭이되,
'이번 주 주제'와 '오픈 데이터 카탈로그'는 결정론 코드(datasets.py)에서 그대로 실어 온다.

산출물: window.AILAB (docs/ailab.js)
  { generated, repo, branch, weekly{...}, modalityLabels{...},
    datasets[ {...} ], cards[ { id, topic, subtopic, kind, framework, arch, modality,
    level, projectUrl, dataset, datasetUrl, colabUrl, notebook, week, tags[], sections{...} } ] }

사용: python pipelines/export_ailab_web.py
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from frontmatter import load
from datasets import DATASETS, MODALITY_LABELS, weekly_topic

ROOT = Path(__file__).resolve().parent.parent
AILAB_DIR = ROOT / "content" / "ailab"
OUT = ROOT / "docs" / "ailab.js"

REPO = "ehdbddl06001-ui/my-github-test"
BRANCH = "main"

# 본문에서 뽑아 웹 카드에 넣을 섹션(순서 = 화면 표시 순서)
SECTIONS = [
    "Overview", "Architecture", "Data", "Code walkthrough",
    "Instructions", "Exercises", "Resources", "My notes",
]


def section(body: str, name: str) -> str:
    """'## name' 섹션 본문을 다음 '## '까지 추출. 자리표시자 주석은 버린다."""
    marker = f"## {name}"
    if marker not in body:
        return ""
    rest = body.split(marker, 1)[1]
    lines: list[str] = []
    for line in rest.splitlines()[1:]:
        if line.startswith("## "):
            break
        if line.strip().startswith("<!--"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def build_card(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    sections = {name: section(d.body, name) for name in SECTIONS}
    sections = {k: v for k, v in sections.items() if v}  # 빈 섹션 제거
    return {
        "id": d.id,
        "topic": m.get("topic", "") or "",
        "subtopic": m.get("subtopic", "") or "",
        "kind": m.get("kind", "") or "",
        "framework": m.get("framework", "") or "",
        "arch": m.get("arch", "") or "",
        "modality": m.get("modality", "") or "",
        "level": m.get("level", "") or "",
        "projectUrl": m.get("project_url", "") or "",
        "dataset": m.get("dataset", "") or "",
        "datasetUrl": m.get("dataset_url", "") or "",
        "colabUrl": m.get("colab_url", "") or "",
        "notebook": m.get("notebook", "") or "",
        "week": m.get("week"),
        "date": str(m.get("date", "") or ""),
        "confidence": m.get("confidence", "") or "",
        "tags": [str(t) for t in (m.get("tags", []) or [])],
        "sections": sections,
    }


def load_cards() -> list[dict]:
    cards = []
    if AILAB_DIR.exists():
        for p in sorted(AILAB_DIR.rglob("*.md")):
            c = build_card(p)
            if c:
                cards.append(c)
    # roadmap/concept를 먼저, 그다음 최신순
    kind_rank = {"roadmap": 0, "concept": 1, "project": 2, "weekly": 3}
    cards.sort(key=lambda c: (kind_rank.get(c["kind"], 9), c["date"]), reverse=False)
    return cards


def main() -> int:
    cards = load_cards()
    payload = {
        "generated": date.today().isoformat(),
        "repo": REPO,
        "branch": BRANCH,
        "weekly": weekly_topic(),
        "modalityLabels": MODALITY_LABELS,
        "datasets": DATASETS,
        "cards": cards,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/ailab/**/*.md + pipelines/datasets.py\n"
        "//   →  `python pipelines/export_ailab_web.py`로 재생성\n"
        "window.AILAB = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    print(f"생성: {OUT.relative_to(ROOT)}  카드 {len(cards)}개 · "
          f"데이터셋 {len(DATASETS)}개 · 이번주 ISO {payload['weekly']['week']}주차")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

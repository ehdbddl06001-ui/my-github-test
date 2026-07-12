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
import re
from datetime import date
from pathlib import Path

from frontmatter import load
from datasets import (
    DATASETS, MODALITY_LABELS, weekly_topic, topic_for_week, TOTAL_WEEKS,
)
from state import ailab_progress

ROOT = Path(__file__).resolve().parent.parent
AILAB_DIR = ROOT / "content" / "ailab"
OUT = ROOT / "docs" / "ailab.js"

REPO = "ehdbddl06001-ui/my-github-test"
BRANCH = "main"

def parse_sections(body: str) -> dict[str, str]:
    """본문의 모든 '## ' 섹션을 **저작 순서대로** {제목: 본문}으로 담는다.

    화이트리스트를 두지 않으므로 카드마다 자유로운 섹션(한국어 포함)을 쓸 수 있고,
    JSON/JS 모두 삽입 순서를 보존하므로 홈페이지가 저작 순서 그대로 렌더한다.
    자리표시자 주석(<!-- ... -->, 여러 줄 포함)은 통째로 제거하고, 그러고도 빈 섹션은 버린다.
    (예: 멘토 노트의 `## 내 답변`은 사용자가 채우기 전엔 안내 주석뿐이라 웹에 나오지 않는다.)
    """
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    out: dict[str, str] = {}
    name: str | None = None
    buf: list[str] = []

    def flush() -> None:
        if name is None:
            return
        text = "\n".join(buf).strip()
        if text:
            out[name] = text

    for line in body.splitlines():
        if line.startswith("## "):
            flush()
            name = line[3:].strip()
            buf = []
        elif name is not None:
            buf.append(line)
    flush()
    return out


def build_card(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    sections = parse_sections(d.body)
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
        # 실행 로그(kind: log)용 필드 — 주차별 진도 목록이 점수 배지를 그릴 때 쓴다.
        "split": m.get("split", "") or "",
        "metric": m.get("metric", "") or "",
        "value": m.get("value"),
        "passed": bool(m.get("passed", False)),
        "sections": sections,
    }


def load_cards() -> list[dict]:
    cards = []
    if AILAB_DIR.exists():
        for p in sorted(AILAB_DIR.rglob("*.md")):
            c = build_card(p)
            if c:
                cards.append(c)
    # mentor(최신 논의)를 맨 위, 그다음 deepdive(주차 심화)·roadmap/concept/project/weekly,
    # 각 그룹 내 최신순. 안정 정렬을 이용: 먼저 최신순(내림차순)으로 둔 뒤, kind 우선순위로 재정렬.
    kind_rank = {"mentor": 0, "deepdive": 1, "roadmap": 2, "concept": 3,
                 "project": 4, "weekly": 5, "log": 6}
    cards.sort(key=lambda c: (c["date"], c["id"]), reverse=True)
    cards.sort(key=lambda c: kind_rank.get(c["kind"], 9))
    return cards


def main() -> int:
    cards = load_cards()
    # 12주 커리큘럼 전체(진도 목록용) — 홈페이지가 '현재 주차'만이 아니라 모든 주차를 보여준다.
    curriculum = [topic_for_week(i) for i in range(1, TOTAL_WEEKS + 1)]
    payload = {
        "generated": date.today().isoformat(),
        "repo": REPO,
        "branch": BRANCH,
        "weekly": weekly_topic(),
        "curriculum": curriculum,          # 주차별 목표·게이트·완료여부
        "progress": ailab_progress(),      # {week, done{주차:{date,metric,value}}}
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
    w = payload["weekly"]
    print(f"생성: {OUT.relative_to(ROOT)}  카드 {len(cards)}개 · "
          f"데이터셋 {len(DATASETS)}개 · 현재 {w['week']}/{w.get('total', 12)}주차")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

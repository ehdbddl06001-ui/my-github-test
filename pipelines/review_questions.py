"""
review_questions.py — 생성 후 **내용 검토지**를 만든다(판정하지 않는다).

형식은 lint_questions.py 가 코드로 확인한다. 하지만 「단일 최선의 답이 성립하는가」「정상·음성 소견의 의미를
과장하지 않았는가」 같은 의학적 타당성은 키워드 검사로 검증할 수 없다(2026-09-18 사용자 지시). 이 스크립트는
그 판단을 대신하지 않고, 검토자가 볼 순서대로 한 장에 모아 준다:

  - 문항이 평가하려는 것(design.target·decision)과 혼동 대안·구분 소견
  - 정보 역할 표(결정적 단서 / 의미 있는 정상·음성 / 치료 선택에 영향 / 비중 낮음)와 **역할이 없는 자료**
  - 내용 검토 신호(question_design.review_flags) — 먼저 볼 곳일 뿐, 없다고 통과가 아니다
  - 여섯 가지 검토 질문(체크박스)

검토를 끝낸 문항만 사람이 frontmatter 에 `review_status: reviewed`·`reviewed_by`·`review_note` 를 적는다.
근거를 확인하지 못한 주장이 있으면 `needs_revision` 으로 둔다. 생성 모델의 `confidence` 는 출처 신뢰도일 뿐
검토 완료의 대체물이 아니다.

사용:
  python pipelines/review_questions.py content/kmle/2026/kmle-2026-1063.md          # 표준 출력
  python pipelines/review_questions.py --out review.md <파일들...>
  python pipelines/review_questions.py --date 2026-09-19                            # 그날 생성분 전부
"""
from __future__ import annotations

import sys
from pathlib import Path

from frontmatter import load, QUESTION_TYPES
from question_design import (REVIEW_QUESTIONS, ROLE_LABEL, _norm, _roles_of, review_flags,
                             review_status)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


def _cell(v) -> str:
    return str(v if v is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def sheet(path: Path) -> str:
    d = load(path)
    m = d.meta
    out = [f"## {d.id} — {m.get('topic', '')} · {m.get('subtopic', '')}", ""]
    out.append(f"- 검토 상태: **{review_status(m)}**"
               + (f" (검토자 {m.get('reviewed_by')})" if m.get("reviewed_by") else ""))
    out.append(f"- 난이도 {m.get('difficulty', '?')} · confidence {m.get('confidence', '?')} "
               f"(confidence 는 출처 신뢰도 — 의학적 검증 아님)")
    out.append(f"- 질문: {str(m.get('stem', '')).strip()[-120:]}")
    choices = m.get("choices") or []
    out.append(f"- 정답: {m.get('answer')} — {next((c for c in choices if str(c).startswith(str(m.get('answer', '')) + '.')), '')}")
    des = m.get("design")
    if not isinstance(des, dict):
        out += ["", "> design 이 없는 문항(기존 형식) — 아래 검토 질문만 적용한다.", ""]
    else:
        out += ["", f"**평가 대상** {des.get('target', '')} · 판단 {des.get('steps', '?')}단계",
                f"**핵심 판단** {des.get('decision', '')}",
                f"**혼동 대안** {des.get('rival', '—')} · **구분 소견** {des.get('discriminator', '—')}", "",
                "| 정보 | 역할 | 이유 |", "|---|---|---|"]
        cited = set()
        for f in des.get("findings") or []:
            if not isinstance(f, dict):
                continue
            roles = [ROLE_LABEL.get(r, r) for r in _roles_of(f)]
            out.append(f"| {_cell(f.get('item'))} | {_cell(', '.join(roles))} | {_cell(f.get('why'))} |")
            cited.add(_norm(f.get("item", "")))
        uncited = [f"{l.get('name')}" for l in (m.get("labs") or [])
                   if isinstance(l, dict) and not any(_norm(l.get('name', '')) in c or c in _norm(l.get('name', ''))
                                                      for c in cited if c)]
        if uncited:
            out += ["", f"역할이 적히지 않은 검사: {', '.join(uncited)} — 그 상황에서 실제로 주어질 자료인지 확인"]
        if des.get("switch"):
            sw = des["switch"]
            out.append(f"조건 전환: ({sw.get('choice')}) {sw.get('condition')}")
    flags = review_flags(m)
    out += ["", "**내용 검토 신호**(판정 아님):"]
    out += [f"- [{c}] {msg}" for c, msg in flags] or ["- (없음 — 신호가 없다고 검증된 것은 아니다)"]
    out += ["", "**검토 질문**"]
    out += [f"- [ ] {q}" for q in REVIEW_QUESTIONS]
    out += ["", "검토 메모: ", "", "---", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    out_path = None
    date = None
    files: list[Path] = []
    it = iter(argv)
    for a in it:
        if a == "--out":
            out_path = Path(next(it))
        elif a == "--date":
            date = next(it)
        else:
            files.append(Path(a))
    if date:
        for sub in ("kmle", "usmle", "imaging"):
            for p in sorted((CONTENT / sub).rglob("*.md")):
                d = load(p)
                if d.type in QUESTION_TYPES and str(d.meta.get("date", "")) == date:
                    files.append(p)
    if not files:
        print(__doc__)
        return 2
    text = f"# 내용 검토지 — {len(files)}문항\n\n" + "\n".join(sheet(p) for p in files)
    if out_path:
        out_path.write_text(text, encoding="utf-8")
        print(f"검토지: {out_path} ({len(files)}문항)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

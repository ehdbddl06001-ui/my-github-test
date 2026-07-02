# 루틴 프롬프트 — USMLE (얇게 유지)

화·목요일 USMLE 생성용. 세부 규칙은 프롬프트에 적지 않는다 —
CLAUDE.md 와 .claude/skills/ 가 자동 로드되므로 그걸 따르게만 한다.

--------------------------------------------------------------------
오늘 날짜로 USMLE 콘텐츠를 생성한다.

- 세부 규칙(frontmatter, step·exam_subject, 중복 방지, ID 규칙, 저장 경로, 검증,
  색인, 웹 번들 재생성, 커밋)은 전부 CLAUDE.md 와 .claude/skills/daily-run 을 따른다.
- 오늘 목표: USMLE 6문항 = Step 1 3문항 + Step 2 3문항. 과목을 회전시키고,
  `recent_topics('usmle', 14)` 로 나온 최근 주제는 제외한다.
- 저장: content/usmle/{id}.md  (id는 state.next_id('usmle')).
- 완료 후: `python pipelines/indexer.py --check` → `python pipelines/indexer.py`
  → `python pipelines/export_usmle_web.py` (docs/questions_usmle.js 재생성).
  새 .md + state/*.json + docs 번들을 claude/ 브랜치에 커밋·푸시하고 PR로 올린다.
--------------------------------------------------------------------

## 참고
- USMLE는 self-verify 한계가 있어 main 직접 커밋이 아니라 PR로 사람이 검수한다.
- 규칙을 프롬프트에 복사하지 않는다. 규칙이 여러 벌로 갈라지면 관리가 무너진다.

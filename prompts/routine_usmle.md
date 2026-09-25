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
  새 .md 와 docs 번들은 `python pipelines/publish.py -m "USMLE <날짜>: …"` 로 main 에 올린다(문항은 PR 로 올리지 않는다 — daily-run 7단계).
--------------------------------------------------------------------

## 참고
- 문항 PR 은 병합이 늦으면 `next_id()` 가 같은 ID 를 다시 발급한다 — 문항은 main 으로 바로 올리고, 사람 검토는 `review_status` 로 표시한다.
- 규칙을 프롬프트에 복사하지 않는다. 규칙이 여러 벌로 갈라지면 관리가 무너진다.

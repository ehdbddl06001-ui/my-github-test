# 루틴 프롬프트 템플릿 (얇게 유지)

아래를 Claude Routine 입력창에 붙여 넣는다. 세부 규칙은 프롬프트에 적지 않는다 —
CLAUDE.md 와 .claude/skills/ 가 자동 로드되므로 그걸 따르게만 한다.

--------------------------------------------------------------------
오늘 날짜로 KMLE 콘텐츠를 생성한다.

- 세부 규칙(과목 수, 문항 수, frontmatter, 중복 방지, ID 규칙, 저장 경로,
  검증, 색인, 커밋)은 전부 CLAUDE.md 와 .claude/skills/daily-run 을 따른다.
- 오늘 목표: KMLE 16과목 × 2문항 = 32문항.
- 완료 후 `python pipelines/indexer.py --check` 와 `python pipelines/indexer.py`
  를 실행하고, 새 .md 와 state/*.json 을 함께 main 에 커밋·푸시한다.
--------------------------------------------------------------------

## 요일 분산 (권장 스케줄)
Claude Routine을 요일별로 나눠 각 프롬프트를 붙인다.
- **월·수·금**: 위 KMLE 프롬프트(이 파일).
- **화·목**: `prompts/routine_usmle.md` (USMLE 6문항, Step 1·2 분산, PR로).
- **일**: "오늘의 논문 3편을 gen-paper 규칙으로 요약", 커밋은 PR로.

USMLE는 생성 후 `python pipelines/export_usmle_web.py` 로 웹 번들을 재생성해야
개인 페이지(docs/)에 새 문항이 뜬다 — 이 단계는 daily-run 스킬에 포함돼 있다.

## 참고 (왜 이렇게 얇은가)
루틴이 늘어나도 규칙은 repo 한 곳(CLAUDE.md)에서만 관리된다.
프롬프트에 규칙을 복사해 두면 나중에 규칙이 여러 벌로 갈라져 관리가 무너진다.

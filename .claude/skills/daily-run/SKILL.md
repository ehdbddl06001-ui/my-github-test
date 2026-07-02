---
name: daily-run
description: 하루치 MedKOS 콘텐츠를 생성·저장·색인·커밋하는 오케스트레이터. 매일 도는 루틴이 이 스킬을 호출한다. "오늘 콘텐츠 생성", "daily run", "오늘 문제 만들어" 같은 요청에 트리거.
---

# 하루치 실행 절차

인자로 콘텐츠 타입과 개수를 받을 수 있다(없으면 KMLE 기본).
예: "오늘 KMLE 32문항", "오늘 USMLE 10문항", "오늘 논문 3편".

## 순서 (반드시 이 순서를 지킬 것)

1. **상태 로드** — 최근 다룬 주제를 확인해 중복을 피한다.
   ```
   python -c "from pipelines.state import recent_topics; print(recent_topics('kmle', 14))"
   ```
   여기서 나온 주제는 오늘 생성에서 제외 힌트로 쓴다.

2. **생성** — 타입에 맞는 스킬 규칙을 따른다.
   - KMLE/USMLE → `/gen-kmle` 규칙
   - 논문 → `/gen-paper` 규칙
   - 질환/약물 카드 → `/gen-card` 규칙
   각 항목마다 `state.next_id(<type>)` 로 id를 발급받는다.

3. **저장** — `schemas/frontmatter.md` 규격의 `.md` 로 올바른 `content/` 폴더에 저장.

4. **주제 기록** — 생성한 각 주제를 기록한다.
   ```
   python -c "from pipelines.state import record_topic; record_topic('kmle', '<주제>')"
   ```

5. **검증 + 색인**
   ```
   python pipelines/indexer.py --check   # 실패하면 여기서 멈추고 원인 보고
   python pipelines/indexer.py
   ```

6. **커밋** — 새 `.md` + `state/*.json` 을 함께 커밋.
   - KMLE: main 직접 커밋 허용
   - paper/disease/drug: PR 생성

## 주의
- 검증(5번)에서 실패하면 커밋하지 말고 무엇이 틀렸는지 보고한다.
- 실행 한도를 고려해, 한 번에 한 타입만 처리하는 것을 기본으로 한다.

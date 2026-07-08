---
name: ai-mentor
description: 사용자의 AI·코딩 학습(content/ailab, notebooks)을 검토해 심화 학습 방향·코드 보완·새 기능 아이디어를 제안하고, repo에 쌓이는 '논의 노트'로 남긴다. 사용자와 클로드가 비동기로 토론(왕복)하는 통로. "멘토", "내 학습 봐줘", "심화 아이디어", "코드 보완 제안", "ai mentor", "다음에 뭐 하지" 요청에 트리거.
---

# AI 학습 멘토 · 논의 노트

클로드와 **심화 학습·코드 보완·새 기능**을 토론하는 통로. 대화를 채팅으로 흘려보내지 않고
**repo에 쌓이는 Markdown 논의 노트**로 남긴다(MedKOS 원칙: 쌓일수록 자산·임시 컨테이너 안전).

## 무엇을 하나
1. 최근 학습 상태를 읽는다: `content/ailab/*.md`(특히 `## My notes`), `notebooks/`,
   `pipelines/datasets.py`(이번 주 주제). 최근 논의는 `content/ailab/mentor/`의 최신 노트.
2. 아래 4가지를 **구체적으로**(파일·줄·근거와 함께) 제안한다.
   - 🔬 **심화 학습**: 지금 카드에서 한 걸음 더 갈 개념·논문·실험(왜 지금 이걸 보는지).
   - 🛠 **코드 보완**: repo 코드(pipelines/·notebooks/·docs/)의 개선점. 파일 경로로 지목.
   - 💡 **새 기능 아이디어**: MedKOS/AI랩에 더하면 좋을 기능(우선순위·난이도 표기).
   - ➡️ **다음 주 추천**: `datasets.py` 커리큘럼과 사용자의 관심을 맞춘 다음 실습.
3. `## 내 답변`을 **빈 칸**으로 남긴다(사용자가 답을 적으면 다음 회차에 이어받는다).

## 왕복(토론) 방식
- 사용자는 노트의 `## 내 답변`에 직접 적거나, 홈페이지 🤖 AI랩에서 메모 → 카드에 반영한다.
- 다음 `/ai-mentor` 실행 시 **직전 노트의 `## 내 답변`을 먼저 읽고** 그 맥락을 이어
  답한다(끊긴 대화가 아니라 연속된 스레드).
- 사용자가 특정 주제(예: "3D 분할 성능 올리는 법")를 주면 그걸 그 회차의 초점으로 삼는다.

## 생성 규칙
1. **ID**: `python -c "from pipelines.state import next_id; print(next_id('ailab'))"`
2. **파일**: `content/ailab/mentor/mentor-YYYY-Www.md` (ISO 연도-주차). 같은 주 재실행이면
   기존 노트를 이어 쓰되 새 회차 섹션을 추가하거나, 초점이 다르면 새 파일.
3. **frontmatter**: `type: ailab`, `kind: mentor`, `topic: AI Mentorship`, `week: <ISO주차>`,
   `date`(KST 오늘), `confidence: medium`(제안·해석이므로), 관련 카드 id를 `related`에.
4. **본문 섹션 순서**(웹이 저작 순서 그대로 렌더): `## Overview` → `## 심화 학습` →
   `## 코드 보완` → `## 새 기능 아이디어` → `## 다음 주 추천` → `## 내 답변`(빈칸) → `## Resources`.
5. **정직성**: 코드 보완은 **실제 파일을 열어 확인**하고 제안한다(추측 금지). 확실치 않으면
   "확인 필요"로 표시. 의학·모델 주장은 근거(링크/논문)를 붙이고 없으면 confidence를 낮춘다.

## 커밋 전 마무리
```
python pipelines/indexer.py --check
python pipelines/indexer.py
python pipelines/export_ailab_web.py     # 논의 노트가 홈페이지 🤖 AI랩 맨 위에 뜨게
python pipelines/export_search_web.py
```
새 `.md` + `state/*.json` + `docs/` 번들을 같은 커밋에. 신규 타입이므로 **claude/ 브랜치 →
PR**로 올려 사람이 검수한다(사용자가 main 직접 커밋을 허용하면 예외).

## 주의
- 코드 보완 제안 중 **작고 확실한 것은 직접 고쳐 같은 PR에 담아도 좋다**(예: 오타·주석·
  작은 리팩터). 크거나 애매하면 노트의 아이디어로만 남기고 사용자에게 판단을 넘긴다.
- 한 회차에 너무 많이 던지지 말 것. 각 섹션 2~4개, 우선순위를 매겨 실행 가능하게.

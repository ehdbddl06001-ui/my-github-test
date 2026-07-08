---
name: ai-weekly
description: 매주 도는 의료 AI 실습 오케스트레이터. pipelines/datasets.py가 정한 이번 주 주제(오픈 데이터 + 모델구조)를 받아 실습 카드를 생성하고 Colab 노트북과 연결한다. "이번 주 AI 실습", "주간 AI 주제", "ai weekly", "이번주 데이터셋 뭐야" 요청에 트리거.
---

# 주간 AI 실습 절차

의료 AI를 매주 하나씩 직접 돌려보게 만드는 얇은 루틴. **무엇을 할지는 코드가 정한다**
(ISO 주차 기준, LLM 아님). 규칙은 여기, 결정론은 `pipelines/datasets.py`.

## 순서
1. **이번 주 주제 확인 (결정론)**
   ```
   python pipelines/datasets.py         # 이번 주 목표·모델·데이터셋 + 카탈로그
   ```
   출력의 `goal / arch / dataset_key / dataset_url / access`를 이번 주 대상으로 삼는다.

2. **중복 회피** — 최근 다룬 ailab 주제 확인:
   ```
   python -c "from pipelines.state import recent_topics; print(recent_topics('ailab', 21))"
   ```
   이미 최근에 만든 주제면 커리큘럼의 다음 항목으로 옮기거나, 심화 각도로 변주한다.

3. **카드 생성** — `/gen-ailab` 규칙으로 `kind: weekly` 카드를 만든다.
   - frontmatter의 `dataset`은 `datasets.py`의 key와 일치, `week`는 이번 ISO 주차.
   - `notebook`은 `notebooks/ailab_template.ipynb`(또는 주제 전용 노트북) 경로.
   - Architecture 도식 + Instructions(지시어 해설) 표를 반드시 포함.

4. **노트북 연결** — 새 구조가 필요하면 `notebooks/`에 노트북을 추가하고 `colab_url`을
   frontmatter에 링크(`https://colab.research.google.com/github/<repo>/blob/main/notebooks/<file>`).
   기존 템플릿으로 충분하면 그대로 링크한다.

5. **검증·색인·번들**
   ```
   python pipelines/indexer.py --check
   python pipelines/indexer.py
   python pipelines/export_ailab_web.py
   python pipelines/export_search_web.py
   ```

6. **주제 기록 + 커밋** — `record_topic('ailab', '<goal>')` 후, 새 `.md` + `state/*.json`
   + `docs/` 번들 + (있다면)새 노트북을 **같은 커밋**에. **claude/ 브랜치 push → PR**.

## 주의
- 실습 데이터가 `credentialed`(🔴, 예: MIMIC)면 카드에 접근 절차를 명시하고, 바로 못 받는
  주라도 '읽고 설계'하는 과제로 대체한다.
- 한 번에 한 주제만. 카드엔 **재현 가능한 결과 한 줄**을 남길 자리(`## My notes`)를 둔다.
- 요일 분산 예: 주 1회(예: 토) 이 스킬을 돌려 그 주 카드를 올린다.

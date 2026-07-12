---
name: gen-quest
description: 12주 커리큘럼과 직교하는 '독립 심화 퀘스트' 카드(kind: quest)를 만든다. 어떤 실습에서 나온 발견이 한 주차로 끝낼 수 없는 열린 문제일 때(예: inter-patient 일반화, 특정 클래스 붕괴), 논문급 방법(SMOTE·도메인적응·self-supervised·파운데이션 모델 등)을 로드맵으로 큐잉한다. "퀘스트 만들어", "이건 따로 심화 트랙으로", "독립 심화", "gen quest", "일반화 심화" 요청에 트리거.
---

# 심화 퀘스트(quest) 카드 생성 규칙

주차(week)는 **선형 진도**, 퀘스트는 **직교하는 열린 심화 트랙**이다. 한 실습에서 나온 발견이
"한 주차 숙제로 끝낼 수 없다"고 판단되면(예: inter-patient에서 macro-F1이 0.83→0.35로 무너짐),
그걸 억지로 그 주차에 욱여넣지 말고 **별도 퀘스트로 큐**에 넣는다. 여기서는 SMOTE·도메인
적응·self-supervised 사전학습·파운데이션 모델 같은 **요즘 방법**을 제대로 다룬다.

## 언제 만드나
- 통과(게이트)는 했는데 **더 깊은 문제**가 남았고, 그게 여러 방법/논문을 요구할 때.
- 사용자가 "이건 따로 심화 트랙으로"라고 할 때.
- 원천이 되는 **실행 로그(kind: log)나 심화 카드(kind: deepdive)**가 있으면 그 수치를 출발점으로.

## 입력
- 문제의 원천(예: `ailab-2026-0010` inter 로그, `ailab-2026-0007` 심화 카드).
- 없으면 사용자가 준 주제(예: "부정맥 inter-patient 일반화").

## 순서
1. **ID**: `python -c "import sys; sys.path.insert(0,'.'); from pipelines.state import next_id; print(next_id('ailab'))"`
2. **파일**: `content/ailab/quests/ailab-YYYY-NNNN.md`
3. **frontmatter**: `type: ailab`, `kind: quest`, `topic`, `subtopic`(퀘스트 이름), `modality`,
   `level`(보통 advanced), `related`(원천 로그·심화 카드), `date`(KST 오늘), `confidence`
   (해석·전망이 섞이면 medium). `week`는 넣지 않는다(넣으면 '출발점 주차' 참조용일 뿐).
4. **본문 섹션**(웹이 저작 순서 렌더):
   `## Overview` → `## 왜 독립 퀘스트인가`(왜 한 주차로 안 되나) → `## 문제 정의`(무엇을,
   무슨 지표로) → `## 접근 로드맵`(난이도 순, 각 방법이 **무슨 한계를 푸는지** + 근거 논문) →
   `## Architecture`(Mermaid 도식 필수) → `## 실험 큐`(노트북에서 돌릴 실험 + 합격 기준 —
   돌리면 `ingest_run.py`로 로그) → `## Resources` → `## My notes`(빈칸).
5. **정직성**: 방법이 무엇을 개선하는지 **근거(논문/링크)**를 달고, 전망성 주장은 medium.
   숫자는 지어내지 말고 실행 로그로 확인하게 큐잉한다.
6. **주제 기록**: `python -c "import sys; sys.path.insert(0,'.'); from pipelines.state import record_topic; record_topic('ailab','<quest name>')"`

## 공통 마무리 (커밋 전 필수)
```bash
python pipelines/indexer.py --check
python pipelines/indexer.py
python pipelines/export_ailab_web.py     # 홈페이지 '실습 진도'의 🎯 심화 퀘스트 블록에 뜬다
python pipelines/export_search_web.py
```
새 `.md` + `state/*.json` + `docs/` 번들을 **같은 커밋**에. 신규 해석 카드라 **claude/ 브랜치**에
push(사용자 검수).

## 진척 갱신 루프 (MedKOS에서 '결과 + 다음 목표'가 보이게 — 매우 중요)
퀘스트는 한 번 만들고 끝이 아니라, 실험을 하나씩 하며 **갱신**된다. 사용자가 실험 결과를 주면:
1. **결과를 퀘스트에 귀속시켜 로그**:
   ```bash
   python pipelines/ingest_run.py --quest <퀘스트id> --step "<실험명>" \
     --week <출발점주차> --split inter --metric macro_f1 --value <값> \
     --note "<한 줄 관찰>" --notebook notebooks/<파일>.ipynb
   ```
   → `content/ailab/logs/`에 `quest`·`step`이 붙은 로그가 쌓인다(같은 퀘스트의 다른 실험은
   `step`이 달라 별도로 쌓인다). 지어내지 말 것 — 사용자가 준 실측값만.
2. **퀘스트 카드의 `next_goal`을 다음 실험으로 갱신**(끝낸 실험은 `## 실험 큐`에서 ✅ 표시).
   필요하면 `status`도 갱신(`done`이면 완료).
3. **번들 재생성**: `export_ailab_web.py` → 홈페이지 🎯 심화 퀘스트에 **결과 목록 + 다음 목표**가
   함께 뜬다.

## 주의
- 퀘스트는 **열린 트랙**이라 게이트(target)가 없다. 진척은 `## 실험 큐`의 항목을 로그로 채우며
  쌓는다(매번 하나씩 — 완벽주의로 다 하려 하지 말 것).
- 한 퀘스트 = 한 주제. 새 발견마다 **새 퀘스트를 추가**한다(사용자 요청: "따로 할 때마다 추가").

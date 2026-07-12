---
name: deepen-week
description: 이미 통과(check_week)한 AI랩 주차를 되돌아보며 '심화(deep-dive) 카드'를 만든다. 원 실습 카드·노트북을 실측해 A)무엇을 했나 B)구조·문제점 C)다른 구조·대안 D)모델 심화 E)자율학습 로드맵을 정리한다. 매주 도는 루틴이 완료 주차를 하나씩 자동으로 집는다. "주차 심화", "1주차 더 파줘", "deep dive", "deepen", "통과했지만 제대로 알고 싶어" 요청에 트리거.
---

# 주차 심화(deep-dive) 카드 생성 규칙

통과(`check_week.py`)는 진도를 **앞으로** 빼는 게이트다. 하지만 통과 ≠ "제대로 안다".
이 스킬은 **이미 완료한 주차를 되돌아보며 깊이를 채우는** 별도 축이다(논문의 recency ↔
impact 두 축과 같은 구조). 결정론(무엇을 심화할지 선택)은 `pipelines/deepen.py`가 하고,
실제 A~E 분석은 여기(LLM)가 카드로 쓴다.

## 대상 선정 — 코드가 정한다(직접 세지 말 것)
```bash
python pipelines/deepen.py            # 다음 심화 대상(작업지시서)
python pipelines/deepen.py --json     # 스킬이 파싱할 JSON(week·source_card·achieved·notebook_hint)
python pipelines/deepen.py --list     # 완료 주차별 심화 여부 큐
```
- 대상 = **완료(done)했지만 아직 deepdive 카드가 없는 가장 이른 주차**. 큐가 비면(모두 심화됨)
  "심화할 게 없다"고 알리고 끝낸다(새 주차를 통과하면 다시 대상이 생긴다).
- 특정 주차를 강제하려면 `--week N`(작업지시서만 바뀔 뿐, 규칙은 같다).

## 무엇을 읽나(정직한 출발점)
작업지시서의 `source_card`와 `notebook_hint`가 가리키는 **실제 파일을 연다**:
1. `content/ailab/<source_card>.md` — 원 실습 카드(특히 `## My notes`의 회고).
2. `notebooks/ailab_weekNN_*.ipynb` — **셀 단위로** 실제 코드(분할·정규화·모델·학습·평가).
3. `achieved`(통과 당시 metric·value) — "무엇으로 통과했는지"를 그대로 인용.
> ⚠️ 사용자의 **구글 코랩/드라이브에는 접근하지 못한다**. 카드 A절에 이 한계를 명시하고,
> repo 노트북과 통과 기록에서 역산했음을 밝힌다. 코랩에서 셀을 바꿨다면 사용자 확인이 필요.

## 본문 섹션(요청 A~E를 그대로 골격으로)
`export_ailab_web.py`가 **모든 `## ` 섹션을 저작 순서대로** 싣는다. 순서:
`## Overview` → `## A. …(무엇을 했나)` → `## B. …(문제점·단점)` → `## C. …(다른 구조·대안)`
→ `## D. …(모델 심화)` → `## E. …(자율학습 로드맵)` → `## Architecture`(Mermaid, 필수)
→ `## Exercises` → `## Resources` → `## My notes`(사용자가 채우는 빈칸, 왕복용).

작성 원칙:
- **A·B는 코드 실측에 근거**(어느 셀에서 무엇을 했는지). 추측 금지 — 확실치 않으면 "확인 필요".
- **B는 "왜 그 점수를 곧이곧대로 믿으면 안 되는가"**를 우선순위로. data leakage/분할 표준 여부/
  지표 함정/누락된 feature를 구체적으로.
- **C는 효과/난이도**를 붙여 실행 가능하게(B의 문제 번호와 연결).
- **D는 도식(Mermaid) + 근거 계산**(예: 수용영역)으로 "왜 그 약점이 구조상 필연인지" 보인다.
- **E는 노트북에서 바로 돌릴 실험 + 합격 기준**으로. 이게 '자동으로 이어 공부할' 큐다.
- 의학·모델 주장엔 근거(논문/링크)를 달고, estimate·해석이 섞이면 `confidence: medium`.

## 생성 규칙
1. **ID**: `python -c "import sys; sys.path.insert(0,'.'); from pipelines.state import next_id; print(next_id('ailab'))"`
2. **파일**: `content/ailab/ailab-YYYY-NNNN.md`
3. **frontmatter**: `type: ailab`, `kind: deepdive`, `week: <대상 주차>`, `topic`(원 실습과 같은
   대주제), `modality`·`dataset`(작업지시서 값), `arch`(원본 → 대안), `level: intermediate`,
   `notebook`·`dataset_url`·`colab_url`, `related`에 `source_card`와 관련 멘토 노트, `date`(KST 오늘),
   `confidence`(A·B 사실이면 high, C~E 해석 섞이면 medium).
4. **주제 기록**: `python -c "import sys; sys.path.insert(0,'.'); from pipelines.state import record_topic; record_topic('ailab','weekNN deepdive')"`

## 공통 마무리 (커밋 전 필수)
```bash
python pipelines/deepen.py --list            # 대상 주차가 '심화됨'으로 바뀌었는지 확인
python pipelines/test_deepen.py              # 큐 불변식 검사
python pipelines/indexer.py --check          # frontmatter 검증(실패 시 중단)
python pipelines/indexer.py                  # SQLite 재빌드
python pipelines/export_ailab_web.py         # → docs/ailab.js (홈페이지 🤖 AI랩)
python pipelines/export_search_web.py        # → docs/search-index.js
```
새 `.md` + `state/*.json`(id_counter·seen_topics) + 재생성된 `docs/` 번들을 **같은 커밋**에.

## 커밋 정책 · 루틴
- `ailab`는 신규 타입이라 self-verify 한계 → **claude/ 브랜치에 push**(사용자가 검수/PR).
- **루틴화**: KMLE/USMLE 일일 루틴과 같은 방식으로, 주간 Claude 루틴이 이 스킬을 호출하면
  된다(예: 매주 1회). 완료 주차가 쌓일 때마다 큐가 자동으로 다음 대상을 내주므로, 루틴
  프롬프트는 "`/deepen-week` 실행"처럼 **얇게** 유지한다(대상 선정은 `deepen.py`가 한다).
- 심화할 게 없으면(큐 빔) 조용히 종료 — 억지로 만들지 않는다.

## 주의
- 한 회차에 한 주차만. A~E를 다 채우되 각 절은 실행 가능하게(장황함 < 구체성).
- 원 실습 카드를 **수정하지 말고**(원본 보존), 별도 deepdive 카드로 쌓는다. `related`로 잇는다.

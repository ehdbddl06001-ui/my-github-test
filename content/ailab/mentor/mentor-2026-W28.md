---
id: ailab-2026-0004
type: ailab
topic: AI Mentorship
subtopic: 논의 노트 · 2026 W28
kind: mentor
level: intermediate
week: 28
source: "MedKOS AI랩 멘토(/ai-mentor)"
confidence: medium
date: 2026-07-08
tags: [mentor, discussion, roadmap, code-review, ideas]
related: [ailab-2026-0001, ailab-2026-0002, ailab-2026-0003]
---

## Overview
AI랩 첫 회차 논의 노트. 방금 세운 구조(로드맵·Keras 뇌종양 분할 분석·Colab/Drive 셋업·
오픈데이터 레지스트리)를 검토하고, **심화 학습 / 코드 보완 / 새 기능**을 제안한다.
이 노트는 클로드와의 **비동기 토론 스레드**다 — 아래 `## 내 답변`에 답을 적으면 다음
`/ai-mentor` 회차가 그 맥락을 이어받는다.

지금 상태 한눈에: ailab 카드 3장 + 논의 1장, 오픈데이터 16종, 노트북 2개, 스킬
`/gen-ailab`·`/ai-weekly`·`/ai-mentor`. 이번 주(ISO 28) 코드 선정 주제 = 피부병변 분류(HAM10000).

## 심화 학습
지금 뇌종양 분할 카드(`ailab-2026-0002`)에서 **한 걸음 더** 갈 지점들. 우선순위 순.

1. **[높음] 분할 손실을 제대로 이해하기** — Dice만 알고 넘어가지 말고 IoU·Tversky·
   Focal-Tversky를 비교하라. 종양이 작을수록(클래스 불균형) Tversky의 α/β로 위양성·위음성을
   저울질하는 감각이 실전에서 성능을 가른다. → 실험: 손실만 바꿔 검증 Dice 곡선 3개 겹쳐 보기.
2. **[높음] 환자 단위 분리(data leakage)** — 같은 환자의 슬라이스가 train/val에 섞이면
   점수가 부풀려진다. 3D 볼륨은 케이스 단위로 split해야 한다. 왜 중요한지 한 문단으로 정리해
   카드에 남겨라(임상 연구로 그대로 이어지는 개념).
3. **[중간] 패치 학습 → 전체 볼륨 추론 '스티칭'** — 128³로 학습하고 추론 때 겹쳐가며 이어
   붙일 때 경계 아티팩트를 줄이는 법(Gaussian weighting). MONAI의 `sliding_window_inference`가
   이걸 한다 — 코드로 한 번 읽어보면 개념이 박힌다.
4. **[중간] 평가지표 Dice + Hausdorff** — 겹침(Dice)과 경계 오차(HD95)를 같이 봐야 한다.
   왜 둘 다 필요한지(작은 오분류 vs 큰 경계 이탈).

## 코드 보완
실제 파일을 열어 확인한 개선점. **작고 확실한 건 표시**해 두었다(원하면 바로 반영).

1. **[확실·작음] `pipelines/datasets.py`에 정합성 테스트 없음** — `CURRICULUM`의 각
   `dataset` 키가 `DATASETS`에 실제로 존재하는지 아무도 검증하지 않는다. 오타 하나면 조용히
   깨진다. → 작은 `pipelines/test_datasets.py`(키 유일성 + 커리큘럼↔데이터셋 존재 + `weekly_topic`
   결정성)를 추가하면 안전하다. **이번 회차에 함께 넣자고 제안**(아래 새 기능 1번과 연결).
2. **[논의 필요] `weekly_topic()`이 달력 주차(`week % 12`)로 선정** — 로드맵은 '신호→3D' 순인데,
   연중 아무 때나 시작하면 커리큘럼 중간(예: 지금은 5번 피부)으로 튄다. 입문자는 1번(신호)부터
   순서대로 가는 게 맞다. → **선택지**: (a) 지금처럼 달력 순환 유지, (b) `state/`에 '내 진도(주차
   인덱스)'를 저장해 순서대로 진행, (c) 둘 다 지원하고 사용자가 고른다. 어느 쪽을 원하는지 답을
   주면 그 방식으로 `datasets.py`를 고치겠다.
3. **[확실·작음] Colab 링크가 `main` 브랜치 고정** — 노트북/카드의 `colab_url`이 `.../blob/main/...`
   이라, 아직 머지 안 된 작업은 못 연다. 지금은 머지됐으니 OK지만, 규칙으로 남겨두자(주간 카드는
   머지 후에 링크 유효).
4. **[확실·작음] `docs/ailab-app.js`의 CDN 의존** — marked/mermaid를 CDN에서 불러오고 실패 시
   텍스트로 폴백하도록 이미 처리했지만, 버전 고정(SRI 해시)까지 하면 재현성이 올라간다. 우선순위 낮음.

## 새 기능 아이디어
MedKOS/AI랩에 더하면 좋을 것. (난이도 / 가치)

1. **실습 진도 추적 + 홈페이지 진행바** (쉬움/높음) — `state/ailab_progress.json`에 완료 주차를
   기록하고, 홈페이지 🤖 AI랩에 "12주 중 n주 완료" 진행바. 코드 보완 2번(순서 진행)과 자연스레 묶임.
2. **주차별 스타터 노트북 자동 생성** (중간/높음) — `datasets.py`의 이번 주 `arch`·`dataset`을
   받아 `notebooks/week_NN.ipynb`를 파라미터로 찍어내는 `gen_notebook.py`. 매주 빈손으로 시작하지
   않게.
3. **지식 그래프 연결(ailab ↔ kmle/paper)** (중간/중간) — 뇌종양 분할 카드를 신경종양 KMLE 문항·
   관련 논문과 `related`로 잇는다. 이미 `relations` 테이블·`related` 필드가 씨앗으로 있다 →
   "이 모델이 푸는 임상 문제"로 공부가 연결된다.
4. **결과 로그 왕복(notebook → 카드)** (중간/중간) — 노트북이 `results.json`(Dice/AUROC)을 Drive에
   쓰고, 파이프라인이 그 값을 카드 상단 배지로 끌어온다(논문 `apply_notes.py` 왕복과 같은 패턴).
5. **모델 구조 도감(model zoo) 카드 타입** (쉬움/중간) — U-Net·ResNet·ViT·Transformer를 Mermaid
   도식 + '언제 쓰나'로 한 장씩. `/gen-ailab kind:concept`로 찍어내면 됨.

## 다음 주 추천
- 이번 주 코드 선정은 **HAM10000 피부병변 분류**(불균형 처리·클래스 가중치·증강). 입문 난이도로
  좋다. `notebooks/ailab_template.ipynb`로 시작 → 결과 한 줄을 이 노트 아래 `## 내 답변`에 남겨라.
- 만약 뇌종양(3D)로 먼저 가고 싶다면 코드 보완 2번의 '순서 진행' 방식을 켜자(그럼 9주차 3D U-Net
  입문부터 순서대로). **원하는 쪽을 답해 달라.**

## 내 답변
<!-- 여기에 답을 적으면 다음 /ai-mentor 회차가 이어받는다.
     예: "코드 보완 2번은 (b) 순서 진행으로 해줘", "새 기능 1번부터 만들자",
         "이번 주 실습 결과: HAM10000 val acc 0.78" 등 -->

## Resources
- 검토 대상: `content/ailab/ailab-2026-0001~0003.md`, `pipelines/datasets.py`, `notebooks/`
- Tversky loss: Salehi 2017 · Focal-Tversky: Abraham 2019
- MONAI sliding-window inference: https://docs.monai.io/
- 이 노트를 만든 스킬: `/ai-mentor` (`.claude/skills/ai-mentor/SKILL.md`)

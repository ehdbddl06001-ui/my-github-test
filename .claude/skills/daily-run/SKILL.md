---
name: daily-run
description: 하루치 MedKOS 콘텐츠를 생성·저장·색인·커밋하는 오케스트레이터. 매일 도는 루틴이 이 스킬을 호출한다. "오늘 콘텐츠 생성", "daily run", "오늘 문제 만들어" 같은 요청에 트리거.
---

# 하루치 실행 절차

인자로 콘텐츠 타입과 개수를 받을 수 있다(없으면 KMLE 기본).
예: "오늘 KMLE 32문항", "오늘 USMLE 10문항", "오늘 논문 3편".

**해부학(anatomy)은 이 스킬이 처리하지 않는다** — 인자가 `anatomy`이면
`/anatomy-daily` 스킬로 위임하고 종료한다(PDF 처리·일정·마스킹 규칙이 달라서
별도 오케스트레이터를 쓴다).

## 순서 (반드시 이 순서를 지킬 것)

1. **상태 로드** — 최근 다룬 주제를 확인해 중복을 피한다. (타입 인자에 맞춰 조회)
   ```
   python -c "from pipelines.state import recent_topics; print(recent_topics('kmle', 14))"
   python -c "from pipelines.state import recent_topics; print(recent_topics('usmle', 14))"
   ```
   여기서 나온 주제는 오늘 생성에서 제외 힌트로 쓴다.

2. **생성** — 타입에 맞는 스킬 규칙을 따른다.
   - KMLE/USMLE → `/gen-kmle` 규칙 (USMLE는 `step`·`exam_subject` 필수)
     · **자료 다양성**: 세트에 **심전도 판독 문항 ≥1개**를 넣고 `figure`(합성 `type:ecg`
       기본, 모양형은 커밋된 `type:ecg12` 에셋)로 실제 파형을 붙인다 — export가 자동 렌더.
   - 기초의학 → `/gen-basic` 규칙 (생리·생화·약리 개념을 임상과 연결)
   - 논문 → `/gen-paper` 규칙
   - 질환/약물 카드 → `/gen-card` 규칙
   각 항목마다 `state.next_id(<type>)` 로 id를 발급받는다.

2-b. **내 오답의 이론 정리본** — 내가 틀린 문항 가운데 정리본이 없는 주제를 그날 채운다(2026-09-20 사용자 지시).
   ```
   python pipelines/concept_queue.py --limit 3
  큐에 `[note]`·`[link]` 가 하나도 없으면 `[gap]`(기본틀에서 아직 비어 있는 자리)을 **하루 1개**까지 쓴다 —
  오답이 없는 날에도 해리슨 순서대로 한 칸씩 메워 과별 학습서가 이어지게 한다(2026-09-21).
   ```
   - `[note]` 는 정리본을 쓰고, `[link]` 는 그 문항들에 `objective` 를 붙인 뒤 정리본이 없으면 이어서 쓴다.
     `[touch]` · `[variant]`(틀린 문항마다 변형 2개) · `[dist]`(고른 오답 보기 설명)는 전용 루틴 「오답 정리본 06:00·18:00」이
     주로 처리한다 — 여기서는 시간이 남을 때만. 규칙은 모두 `/gen-concept`.
     이 루틴에서는 **하루 상한: 정리본 3개 · 목표 연결 10문항** — 넘으면 큐에 남겨 둔다(전용 루틴은 시간 예산만 쓴다).
   - 큐가 비어 있으면 이 단계는 건너뛴다(학습 기록이 아직 저장소에 안 왔을 때가 대부분이다 — 정상).
   - 보고에 「정리본 N개 · 목표 연결 M문항 · 큐 잔여 K건」을 남긴다.

3. **저장** — `schemas/frontmatter.md` 규격의 `.md` 로 올바른 `content/` 폴더에 저장.
   - `date` 는 **한국시간(KST) 기준 오늘**로 적는다: `TZ=Asia/Seoul date +%F` 로 확인.
     (루틴 컨테이너는 UTC이고 스케줄이 20:00 UTC=05:00 KST라, UTC 날짜로 찍으면
     하루 밀려 웹 '오늘의 문항'에 안 잡힌다. 웹도 KST 기준으로 오늘을 판단한다.)

4. **주제 기록** — 불필요(파생물화). 주제는 저장한 카드의 `topic`/`subtopic` frontmatter가
   SoT이고 `recent_topics()`가 여기서 계산한다. `record_topic()`은 호환용 no-op이라 굳이
   부르지 않아도 된다.

5. **검증 + 색인**
   ```
   python pipelines/indexer.py --check              # frontmatter 계약 검증(필수)
   python pipelines/concepts.py                    # 정리본·문항 학습 목표 계약(정리본을 건드린 날 필수)
   python pipelines/lint_questions.py <오늘 만든 .md들>   # 문항 품질 린트(문제형만) — ERROR 0, 그리고 끝의 mix WARN
                                                     # (정답 순서 순환·치료+다음 처치 편중·3단계 비율)과 qualifier-tell·
                                                     # subtopic-conclusion WARN 은 고치고 커밋한다(2026-09-25 감사 — 답이 문항 밖으로 샌다)
   python pipelines/review_questions.py --date <오늘> --out /tmp/review.md   # 내용 검토지(판정 아님 — 보고에 경로·REVIEW 신호 수를 남긴다)
   python pipelines/indexer.py                       # SQLite 재빌드
   ```
   - `--check` 나 린터 **ERROR** 가 나면 여기서 멈추고 원인 보고 후 문항을 고친다.
   - 린터는 에포님 떠먹임·활력징후 부재·정답 보기 누설·오답감별 뭉침 등 '시험 감각'
     결함을 KMLE·USMLE 공통으로 잡는다(기준: `/gen-kmle` 「정상 소견·배경 정보」·「문항 감사 규칙」).

6. **웹 번들 재생성** — 개인 페이지(docs/)에 새 콘텐츠가 뜨게 하려면 필수.
   - USMLE를 생성했다면: `python pipelines/export_usmle_web.py` → `docs/questions_usmle.js`
   - **KMLE를 생성했다면(content/kmle SoT): `python pipelines/export_kmle_web.py`**
     → `docs/questions_kmle_content.js` (인터랙티브 퀴즈에 오늘 문항이 뜨게 함). 웹은
     이 번들을 레거시 `docs/questions.js`(quiz.py 트랙)와 합쳐서 KMLE 덱을 만든다.
   - 정리본을 만들었거나 문항에 `objective` 를 붙였다면: `python pipelines/export_concepts_web.py`
     → `docs/concepts.js` (앱의 오답 뒤 학습 흐름이 그 정리본을 연다)
   - **어떤 타입이든**(basic·paper·disease·drug 포함): `python pipelines/export_search_web.py`
     → `docs/search-index.js` (통합검색·대시보드 갱신). 매 실행 항상 재생성한다.
   생성된 번들을 **같은 커밋에 포함**한다.

7. **커밋** — 새 `.md` + 재생성된 `docs/` 번들을 함께 커밋. (id_counter·seen_topics·
   seen_papers 는 파생물이라 커밋하지 않는다 — `.gitignore`. AI랩 진도를 바꿨을 때만
   `state/ailab_progress.json` 포함.)
   - **KMLE / USMLE(시험 문항): `python pipelines/publish.py -m "<메시지>"` 로 main 에
     직접 올린다. PR 을 만들지 말 것**(허용이 아니라 금지다). 문항 타입은 KMLE·USMLE
     동일하게 취급해 생성 즉시 사이트에 반영한다. `publish.py` 가 이를 강제한다 —
     문항만 바뀐 변경을 `--branch` 로 올리려 하면 거부한다.

     이유: `next_id()` 는 main 의 `content/` 에서 다음 번호를 계산한다. 병합 안 된 문항 PR 이 있으면
     다음 루틴이 같은 ID 를 다시 발급해, 나중에 병합할 때 문항을 덮어쓴다.

   - paper / disease / drug 도 콘텐츠 레인이다 — 같은 `publish.py` 로 main 에 올린다(CLAUDE.md 「커밋 전 필수 순서」).
     사람 검토가 필요하면 `review_status` 로 표시한다.

## 주의
- 검증(5번)에서 실패하면 커밋하지 말고 무엇이 틀렸는지 보고한다.
- 실행 한도를 고려해, 한 번에 한 타입만 처리하는 것을 기본으로 한다.
- 요일 분산(권장): 월·수·금 KMLE, 화·목 USMLE, 일 논문. 프롬프트는 `prompts/` 참고.

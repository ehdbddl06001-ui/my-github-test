# MedKOS — 개인 의료 지식 운영체제

의대~국시~수련~연구까지 쓸 개인 의료 지식 플랫폼. 이 파일은 매 세션·매 루틴 실행에
자동 로드된다. 규칙은 여기에 두고, 루틴 프롬프트는 얇게 유지한다.

## 대원칙
- `content/**/*.md` 가 유일한 Source of Truth. `db/`·Google Drive는 파생물이다.
- 모든 `.md` 는 `schemas/frontmatter.md` 규격의 frontmatter를 반드시 갖는다.
- 결정론적 작업(파싱·DB쓰기·동기화·ID발급)은 `pipelines/*.py` 를 호출한다.
  숫자 세기·파일 이동 같은 일을 LLM이 직접 하지 않는다.
- 문제(kmle/usmle)는 정답·해설을 stem과 분리한다(`answer_separated: true`).
- 출처가 충돌하면 임의로 고르지 말고 source/edition/date를 남기고 confidence를 낮춘다.

## 임시 컨테이너(루틴) 대응 — 매우 중요
- 실행 시작: `python pipelines/state.py` 관점으로, 최근 주제(`recent_topics`)를 읽어
  중복을 피하고, ID는 `next_id()` 로만 발급한다.
- 실행 끝: `state/id_counter.json`, `state/seen_topics.json` 을 갱신해 **같은 커밋에 포함**.
- `db/medkos.sqlite` 는 커밋하지 않는다(.gitignore). 커밋 전 `indexer.py`로 재빌드만.

## 저장 위치
- KMLE → `content/kmle/{연도}/`   USMLE → `content/usmle/`
- 기초의학 → `content/basic/`      논문 → `content/papers/{연도}/`
- 질환 카드 → `content/diseases/`  약물 카드 → `content/drugs/`
- AI·코딩 학습(ailab) → `content/ailab/`  (실습 노트북은 `notebooks/`, Colab+Drive 연동)
  · 오픈 데이터 목록·주차 선정 같은 **결정론**은 `pipelines/datasets.py`가 맡는다(카드는 해석).

## 커밋 전 필수 순서
1. `python pipelines/indexer.py --check`  (frontmatter 검증, 실패 시 중단)
2. `python pipelines/indexer.py`          (SQLite 재빌드)
3. 상태 파일과 새 `.md` 를 함께 커밋
4. 신규 타입(paper/disease/drug)은 self-verify 한계를 고려해 **PR로** 올린다.
   KMLE는 흐름이 안정적이면 main 직접 커밋 허용.

## 금지
- DB에 직접 write. `content/` 밖에 콘텐츠 저장. frontmatter 없는 `.md` 생성.
- id 재사용/역행. 임시 컨테이너 메모리에만 의존하는 상태 관리.

## 스킬
- `/daily-run` : 하루치 콘텐츠 생성 오케스트레이터(루틴이 이걸 호출)
- `/gen-kmle` `/gen-paper` `/gen-card` : 타입별 생성
- `/scrape-papers` : PubMed 최신 논문 스크랩(recency, 매일)
- `/landmark-papers` : 파트별 고인용 '꼭 봐야 하는' 논문 정리(impact, 주간). iCite 인용랭킹.
- `/gen-ailab` : 의료 AI·코딩 학습 카드(공개 프로젝트 분석·도식·지시어 해설) 생성
- `/ai-weekly` : 이번 주 실습 주제(`datasets.py`)를 받아 카드·Colab 노트북 연결(주간)
- `/ai-mentor` : 학습(content/ailab·notebooks) 검토 → 심화학습·코드보완·새기능 제안을
  repo에 쌓이는 '논의 노트'(`content/ailab/mentor/`)로 남김. `## 내 답변`으로 왕복 토론
- `/ai-debug` : Colab/ML 에러를 원인·최소수정·재발방지로 설명하고, 반복 에러는 '디버그
  로그' 카드(`content/ailab/`)에 쌓아 개인 트러블슈팅 FAQ로 축적
- `/index-db` : 색인 재빌드/검증

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
- 실행 시작: 최근 주제(`recent_topics`)를 읽어 중복을 피하고, ID는 `next_id()` 로만 발급한다.
- **상태는 `content/` 파생물이다(충돌 원천 제거)**: `next_id`·`recent_topics`·`paper_seen`
  은 저장된 `content` 카드에서 그때그때 계산한다. `state/id_counter.json`·`seen_topics.json`·
  `seen_papers.json` 은 **더는 만들지도 커밋하지도 않는다**(.gitignore). 따라서 두 루틴이
  같은 상태 파일을 건드려 충돌날 일이 없다. `next_id` 는 content 최댓값을 바닥으로 삼고
  gitignore 된 컨테이너 캐시(`state/.id_cache.json`)로 같은 실행 내 단조 발급만 보장한다.
- 유일하게 커밋되는 상태는 `state/ailab_progress.json`(주간 단일트랙 진도)뿐이고, 혹시
  갈라져도 머지 드라이버가 union 한다. `record_topic`·`mark_paper_seen` 은 호환용 no-op.
- `db/medkos.sqlite` 는 커밋하지 않는다(.gitignore). 커밋 전 `indexer.py`로 재빌드만.

## 저장 위치
- KMLE → `content/kmle/{연도}/`   USMLE → `content/usmle/`
- 기초의학 → `content/basic/`      논문 → `content/papers/{연도}/`
- 질환 카드 → `content/diseases/`  약물 카드 → `content/drugs/`
- AI·코딩 학습(ailab) → `content/ailab/`  (실습 노트북은 `notebooks/`, Colab+Drive 연동)
- 해부학(3Q) → `content/anatomy/{sources,pages,concepts,questions,daily,answers}/`
  · 원본 PDF·페이지 이미지·마스크는 **`.private/anatomy/`(git 무시)** — 공개 repo 커밋 금지.
  · 일정 단일 기준은 `pipelines/anatomy_schedule.py`(2026 시간표). Drive 계획서 날짜 사용 금지.
  · **2026 담당은 문용석·김홍태 둘뿐**(`SESSION_DETAILS`). 업로드 스캔 파일명의 다른 교수명은
    **과거 학기 값**이라 올해 수업과 무관하다 — `pipelines/legacy_sources.py` 가 그 자리에
    꼬리표를 붙이고, 표시 없는 이름이 남으면 `test_legacy_professor_names_are_marked` 가 잡는다.
  · **회차 배정은 교수명·파일명 날짜가 아니라 「부위」로 한다.** 과거 학기 자료는 담당교수와
    날짜가 지금과 다르다 — 그 자료가 다루는 부위를 2026 실습주제에 맞춘다. 결정론은
    `anatomy_schedule.session_for_region()`(회귀: `test_region_not_professor_decides_session`).
  · 루틴 종료일 **2026-10-19**(Tagging 2). 이후 anatomy 생성·커밋 금지(completed no-op).
  · 모든 문항은 `scheduled_dates` 를 반드시 갖는다 — 없으면 회차 필터·일일 큐에서 영영
    안 뽑힌다. 빠진 게 생기면 `pipelines/backfill_sessions.py`(부위 기준)로 채운다.
  · 서브노트(`kind: study_guide`)는 `mnemonics:`(두문자·대조, 5줄 이상)를 갖는다.
    빈칸 채우기·자가 점검 페이지는 본문의 `==하이라이트==`·`### 소제목`에서 **자동 파생**
    되므로, 외울 것은 반드시 `==...==` 로 표시한다(회귀: `test_subnotes_carry_memory_aids`).
  · 오픈 데이터 목록·주차 선정 같은 **결정론**은 `pipelines/datasets.py`가 맡는다(카드는 해석).

## 커밋 전 필수 순서

**한 명령으로 끝낸다 — `python pipelines/publish.py -m "<커밋 메시지>"`.**
아래 1~4단계를 순서대로 돌리고 main 에 푸시한다. 손으로 나눠 하면 한 단계가 빠지고
(번들 미생성 → 홈페이지 안 바뀜, main 미동기화 → 푸시 거절), 그 사고가 실제로 났다.
`publish.py` 는 **경로로 레인을 가른다**:
- **콘텐츠 레인**(`content/**` · `docs/**` · `notebooks/**` · `state/ailab_progress.json`)
  → 검증·번들·병합·**main 직접 푸시**. 매일 도는 루틴은 여기만 건드리므로 늘 자동이다.
- **코드 레인**(`pipelines/**` · `.claude/**` · `CLAUDE.md` · `schemas/**` · 그 외)
  → main 직접 푸시를 **거부**한다. `--branch claude/<작업>` 으로 올리고 PR 을 연 뒤
  테스트를 확인하고 **같은 세션에서 병합**한다. 열어 두고 끝내지 않는다 — PR 이 안
  병합되면 다음 날 루틴이 같은 파일을 처음부터 다시 만든다(2026-08-17 실측).

<details><summary>publish.py 가 대신 해 주는 순서(직접 할 때의 체크리스트)</summary>

1. **main 동기화(충돌 예방)**: push/PR 직전에 `git fetch origin main` 후 `git merge origin/main`.
   상태를 content 파생으로 바꾼 뒤로 kmle/usmle·논문 스크랩은 공유 커밋 파일이 없어
   충돌하지 않지만, 그래도 최신 main 위에서 번들을 만들도록 병합한다. 병합으로 남의
   `content/`가 딸려 들어왔으면 2단계 재색인·번들 재생성을 다시 돌려 `docs/` 번들이 그
   신규 콘텐츠까지 반영하게 한다(병합 직후 번들은 낡아 있음).
2. `python pipelines/indexer.py --check`  (frontmatter 검증, 실패 시 중단)
3. `python pipelines/indexer.py`          (SQLite 재빌드) → 이어서 `docs/` 번들 재생성
   (도해·트리 SVG를 건드렸으면 `python pipelines/export_diagrams_web.py` 도 함께 —
    자산은 검색 색인에 안 잡혀 별도 매니페스트가 갤러리·새 자료 목록의 근거다)
4. 새 `.md` 와 재생성된 `docs/` 번들을 함께 커밋(id_counter·seen_topics·seen_papers 는
   파생물이라 커밋 대상이 아니다; ailab 진도를 바꿨다면 `state/ailab_progress.json` 만 포함).
5. 콘텐츠(anatomy·kmle·usmle·paper·disease·drug·ailab)는 **main 직접 커밋**이 기본이다.
   PR이 병합되지 않으면 `docs/` 번들이 main에 못 올라가 홈페이지에 안 뜨기 때문이다.
   판단이 필요한 변경(파이프라인·스킬·규칙)만 PR로 올리고, 그 PR도 **같은 세션에서 병합**한다.

</details>

### 상태 충돌 방지: content 파생 + 머지 드라이버(이중 안전망)
1차 방어는 **파생물화**다: id_counter·seen_topics·seen_papers 를 커밋하지 않고 `content`
에서 계산하므로(→ `pipelines/state.py`), 두 루틴이 같은 상태 파일을 건드릴 일이 없다.
2차 방어(백스톱)는 **머지 드라이버**다: 유일하게 남은 커밋 상태 `state/ailab_progress.json`
(과 혹시 로컬에 재등장하는 `state/*.json`)이 갈라지면, `.gitattributes`(`state/*.json
merge=medkos-state`) + `pipelines/merge_state.py`(union/최댓값)가 자동 병합한다. 드라이버는
`.claude` SessionStart 훅이 매 컨테이너에서 `git config`로 등록한다(임시 컨테이너 안전).
주의: 드라이버는 **로컬 git 병합**에만 작동한다 → GitHub 서버 병합은 위 1단계(로컬
`git merge origin/main` 후 push)로 해소. 회귀 테스트: `python pipelines/merge_state.py --selftest`,
`python pipelines/test_state.py`.

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
- `/deepen-week` : **통과한 주차를 되돌아보며 심화 카드 생성**(주간 루틴 가능). 대상 선정
  결정론은 `pipelines/deepen.py`(완료했지만 아직 안 판 주차를 자동 선택), 실습 카드·**실제
  노트북**을 실측해 A)무엇을 했나 B)문제점 C)대안 D)모델 심화 E)자율학습 로드맵을 `kind:
  deepdive` 카드로. **낡은 repo 노트북 예측 금지 — 실행 로그(`kind: log`)의 `notebook`이 진짜.**
- `/anatomy-daily` : **해부학(3Q) 일일 학습 세트** 생성 오케스트레이터(매일 05:00 KST
  루틴이 호출, ~2026-10-19). Drive 증분 확인 → 결정론 큐(`anatomy_daily.py`) → 출처
  강제 카드/문항 → 검증 → `docs/anatomy-data.js` 재생성. `/daily-run anatomy`도 위임됨.
- `/gen-quest` : **주차 밖 독립 '심화 퀘스트'(`kind: quest`) 생성**. 한 주차로 못 끝낼 열린
  문제(예: inter-patient 일반화)를 SMOTE·도메인적응·self-supervised·파운데이션 모델 로드맵으로
  큐잉. `content/ailab/quests/`. 진척은 실험을 `ingest_run.py` 로그로 채우며 쌓는다.

## 실행 로그 루프 (예측 방지 — 매우 중요)
클로드가 "네가 실제로 한 것"을 낡은 repo 노트북으로 **추측**하면 틀린다. 그래서 실제 코드·
수치의 Source of Truth를 repo에 박는다:
1. Colab에서 실습 → 노트북과 `result.json`(CELL이 Drive에 저장)을 얻는다.
2. **실제 노트북을 `notebooks/`에 커밋**하고, `python pipelines/ingest_run.py --results
   result.json --notebook notebooks/<파일>.ipynb` 로 **실행 로그 카드**(`content/ailab/logs/`,
   `kind: log`)를 결정론적으로 만든다(수치는 실측 — LLM이 안 지어냄).
3. `deepen.py`는 심화할 때 이 로그의 `notebook`·`value`를 **glob 추정보다 우선**해서 읽는다.
   → `/deepen-week`가 예측 없이 실제 코드로 A~E를 쓴다.
- 같은 주차라도 `split`(intra 통과용 / inter 실전)별로 로그를 따로 쌓는다.
- `/ai-debug` : Colab/ML 에러를 원인·최소수정·재발방지로 설명하고, 반복 에러는 '디버그
  로그' 카드(`content/ailab/`)에 쌓아 개인 트러블슈팅 FAQ로 축적
- `/index-db` : 색인 재빌드/검증


## Codex ↔ Claude Code 협업
- 공통 규칙은 `AGENTS.md`와 `docs/AI_COLLABORATION.md`를 먼저 읽는다.
- 구현은 `experiments/specs/`의 명세가 `status: approved_for_implementation`일 때 시작한다.
- 명세의 `implementation_owner`가 현재 작업 주체와 일치해야 한다.
- Claude Code 브랜치는 `claude/<task>`, Codex 브랜치는 `codex/<task>`를 사용한다.
- 두 에이전트가 같은 브랜치·같은 작업 파일을 동시에 수정하지 않는다.
- Codex가 작성한 명세를 구현할 때 과학적 질문·split·지표·중단 조건을 임의로 바꾸지 말고, 필요한 변경은 Decision log에 남긴다.
- Drive의 기존 ECG 자산은 정리 목적으로 이동하지 않는다. 먼저 `research/ASSETS.md`에 등록하고, 별도 migration spec 승인 후 이동한다.

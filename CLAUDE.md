# MedKOS — 개인 의료 지식 운영체제

국시(KMLE)·USMLE 대비용 개인 문항·오답·학습서 플랫폼. 이 파일은 매 세션·매 루틴 실행에 자동 로드된다.
규칙은 여기와 `.claude/skills/` 에 두고, 루틴 프롬프트는 얇게 유지한다(프롬프트 원문은 `prompts/`).
사용자는 본2 — **MedKOS 는 국시·USMLE 전용**이다. 학교 내신 기준·문항은 넣지 않는다(학교 정리본은 드라이브 `의대_정리본_제작`).

## 먼저 볼 곳 — 작업별 길잡이

| 하려는 일 | 규칙 | 핵심 명령 · 파일 |
|---|---|---|
| KMLE·USMLE 문항 만들기 | `/gen-kmle`(품질 규칙·2026-09-25 감사 규칙), `/daily-run` | `lint_questions.py <파일들>` (ERROR 0 · 세트 mix WARN 해소) |
| 오답 정리본 쓰기·손질·판형 2로 옮기기 | `/gen-concept`(판형 2 · 본보기 `cn.derm.pityriasis-versicolor.treatment`) | `concept_queue.py --limit N` → `concepts.py`(오류 0) |
| 과별 PDF 학습서 | 아래 「오답 뒤 학습 흐름」 | `.github/workflows/books.yml`, `build_books.py --only <과> --out <임시>` |
| 판단 도식 | `decision_diagram.py`(배치는 코드가 정한다) | 노드 글 판단 ≤ 30자 — 안 들어가면 `concepts.py` ERROR |
| 오픈데이터 영상 문항 | **여기서 만들지 않는다** — 빌더(`exam-builder`)의 `opendata medkos-export` | `content/imaging/`, `export_imaging_web.py` |
| 해부학(3Q, ~2026-10-19) | `/anatomy-daily` + **`docs/ANATOMY_RULES.md` 먼저** | `docs/ANATOMY_VISUALS.md` |
| AI·코딩 학습 | `/gen-ailab` `/ai-weekly` `/deepen-week` `/gen-quest` `/ai-mentor` `/ai-debug` | 아래 「실행 로그 루프」 |
| 커밋 | `python pipelines/publish.py -m "…"` (콘텐츠 = main, 코드 = `--branch claude/…` + PR) | 아래 「커밋 전 필수 순서」 |

### 루틴(Claude Routine, 클라우드) — 무엇이 언제 도나
| 루틴 | 시각(KST) | 하는 일 | 프롬프트 |
|---|---|---|---|
| 매일 하루 KMLE 문항 제작 | 월·수·금 05:00 | 16과목 × 2문항 + 정리본 큐 조금 | `prompts/routine_kmle.md`(얇음 → `/daily-run`) |
| USMLE 콘텐츠 생성 | 화·목 05:00 | Step 1·2 각 3문항 | `prompts/routine_usmle.md` |
| 오답 정리본 06:00·18:00 | 매일 | 정리본 큐 전부(50분 예산) → `[restyle]` → `[gap]` | `prompts/routine_concepts.md` |
| 오픈데이터 영상 세트 | 매일 05:00 | exam-builder → MedKOS 내보내기 | exam-builder 저장소 |
| anatomy-daily | 매일 05:00(~10-19) | 해부 서브노트 | `/anatomy-daily` |

GitHub Actions: `books.yml`(학습서, cron 06:30 이지만 **실제 발화는 2시간 넘게 늦다** — 09-23·24 모두 08:50 무렵),
`wrong-sync.yml`(오답 동기화), `drive-sync.yml`, `scrape-papers.yml`·`landmark-papers.yml`, `pages.yml`.
루틴 컨테이너는 **PubMed·doi.org·NCBI 를 막는다**(출처 원문 대조·PMID 찾기는 PC 세션이나 Actions 가 한다).

### 검증 — 무엇을 돌리나
| 명령 | 무엇을 막나 | 관문 |
|---|---|---|
| `python pipelines/indexer.py --check` | frontmatter 계약 | 커밋 전 필수 |
| `python pipelines/lint_questions.py <파일>` | 문항 품질(ERROR)·세트 구성·정답 순서(WARN) | 문항 커밋 전 |
| `python pipelines/concepts.py` | 정리본 계약·**도식이 한 쪽에 들어가는가**·출처·판형 2 예산 | 정리본 커밋 전 |
| `python pipelines/test_learning_books.py` | 코드 회귀(도식 배치·학습 상태 JS/Python 일치·PDF·드라이브) — **고정 픽스처만** | books.yml 관문 |
| `python pipelines/test_content.py` | 실제 정리본·문항 전수(계약·도식 크기) | books.yml 에서 따로 — 실패해도 다른 책은 만든 뒤 작업을 실패로 알림 |
| `python pipelines/test_question_design.py` | 출제 설계·린트 규칙 | 코드 변경 시 |

코드 시험이 실제 콘텐츠를 읽게 만들지 않는다 — 루틴이 쓴 정리본 하나가 모든 책을 멈춘다(2026-09-23·24 실패).

## 대원칙
- `content/**/*.md` 가 유일한 Source of Truth. `db/`·Google Drive는 파생물이다.
- 모든 `.md` 는 `schemas/frontmatter.md` 규격의 frontmatter를 반드시 갖는다.
- 결정론적 작업(파싱·DB쓰기·동기화·ID발급·배치)은 `pipelines/*.py` 를 호출한다.
  숫자 세기·파일 이동·도식 좌표 같은 일을 LLM이 직접 하지 않는다.
- 문제(kmle/usmle)는 정답·해설을 stem과 분리한다(`answer_separated: true`).
- 문제는 **출제 설계(`design`)를 먼저 정하고** 쓴다 — 무엇을 평가하는지·핵심 판단·혼동 대안·정보 역할.
  정상 소견·배경 정보는 의도된 설계라 「길다」는 이유로 빼지 않는다(규칙: `/gen-kmle`).
  답은 **문항 안의 판단으로만** 가려져야 한다 — subtopic·정답 위치 순환·한정어·보기 길이로 새지 않게(2026-09-25 감사).
  `confidence` 는 출처 신뢰도이고 의학적 검증이 아니다 — 검토 완료는 사람이 `review_status: reviewed` 로만 표시한다.
- 출처가 충돌하면 임의로 고르지 말고 source/edition/date를 남기고 confidence를 낮춘다.
  출처는 실제로 확인한 것만, 논문·지침은 `pmid` 를 붙인다(DOI 만 두지 않는다).

## 임시 컨테이너(루틴) 대응
- 실행 시작: 최근 주제(`recent_topics`)를 읽어 중복을 피하고, ID는 `next_id()` 로만 발급한다.
- 날짜는 **KST**(`TZ=Asia/Seoul date +%F`). 컨테이너는 UTC 라 그대로 쓰면 하루 밀린다.
- **상태는 `content/` 파생물이다(충돌 원천 제거)**: `next_id`·`recent_topics`·`paper_seen`
  은 저장된 `content` 카드에서 그때그때 계산한다. `state/id_counter.json`·`seen_topics.json`·
  `seen_papers.json` 은 **더는 만들지도 커밋하지도 않는다**(.gitignore). `next_id` 는 content 최댓값을 바닥으로 삼고
  gitignore 된 컨테이너 캐시(`state/.id_cache.json`)로 같은 실행 내 단조 발급만 보장한다.
- 커밋되는 상태: `state/ailab_progress.json`(머지 드라이버가 union), 사용자 데이터(`state/wrong_sync/`·`state/learning_sync/`),
  학습서 기록(`state/books/`·`state/source_checks.json`). `record_topic`·`mark_paper_seen` 은 호환용 no-op.
- `db/medkos.sqlite` 는 커밋하지 않는다(.gitignore). 커밋 전 `indexer.py`로 재빌드만.
- Windows PC 에서는 항상 `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`(publish.py 가 cp949 디코딩에서 죽는다).

## 저장 위치
- KMLE → `content/kmle/{연도}/`   USMLE → `content/usmle/`
- 기초의학 → `content/basic/`      논문 → `content/papers/{연도}/`
- 질환 카드 → `content/diseases/`  약물 카드 → `content/drugs/`
- 개념 정리본(학습 목표 단위) → `content/concepts/<과>/cn.<과>.<주제>.<목표>.md` — 웹 오답 뒤 학습 흐름과
  과별 PDF 학습서가 **같은 원본**을 쓴다(`pipelines/concepts.py`). 계약: `schemas/frontmatter.md` concept.
- AI·코딩 학습(ailab) → `content/ailab/`  (실습 노트북은 `notebooks/`, Colab+Drive 연동)
- 오픈데이터 영상 문항(imaging) → `content/imaging/{연도}/` + 영상 `docs/assets/imaging/`.
  · **여기서 직접 만들지 않는다** — exam-builder 의 `opendata medkos-export` 가 세트를 옮긴다
    (`schemas/frontmatter.md` imaging 계약). 원본은 빌더 run, 카드는 파생물. 문항 수정은 빌더에서
    폐기 후 재생성. 웹 번들은 `pipelines/export_imaging_web.py`(publish.py 가 자동 실행).
- 해부학(3Q) → `content/anatomy/…` — 규칙 전부는 **`docs/ANATOMY_RULES.md`**(원본 PDF·이미지는 `.private/anatomy/`, 커밋 금지).

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

## 홈페이지 = PWA(핸드폰 앱) · 오답 동기화
- `docs/` 는 GitHub Pages 와 Cloudflare Pages 둘 다에서 뜨도록 **전부 상대경로**다(manifest·sw.js 포함).
  절대경로(`/x`)를 쓰지 않는다. `docs/sw.js` 가 껍데기·번들·영상을 캐시하고, `docs/pwa.js` 가
  설치 버튼·새 자료 토스트를 띄운다. 새 페이지를 추가하면 `sw.js` 의 SHELL 목록에도 넣는다.
- 오답 동기화는 Cloudflare Pages Function `functions/api/wrong.js` → `state/wrong_sync/<exam>.json`
  커밋 → `.github/workflows/wrong-sync.yml` 이 `pipelines/import_wrong_sync.py` 로 오답노트 .md 를
  다시 쓴다. `state/wrong_sync/` 는 **사용자 데이터**라 커밋한다(파생 상태가 아님). 시크릿
  (`GITHUB_TOKEN`·`SYNC_KEY`)은 Cloudflare 대시보드에만 두고 repo 에 절대 넣지 않는다.
- **동기화 키는 기기마다 따로다(2026-09-23)** — 손으로 넣지 않은 기기의 기록은 그 기기에만 쌓였다. 이제 키가 있는
  기기의 「동기화 설정 ▸ 다른 기기 연결 링크」(`https://my-github-test.pages.dev/#k=<키>`)를 새 기기에서 한 번 열면
  `docs/synckey.js` 가 키를 저장하고 주소에서 지운다. 앱은 켜질 때 `functions/api/status.js` 로 키 상태만 묻고(키 값은
  돌려주지 않음) 없거나 틀리면 첫 화면에 경고를 띄운다. 동기화는 연 덱만이 아니라 기록이 있는 모든 시험을 보낸다.
  회귀: `python pipelines/test_sync_key.py`.

## 오답 뒤 학습 흐름 · 과별 PDF 학습서 (2026-09-18~)
- 앱: `docs/learn.js` 가 채점 뒤에만 오답 확인·보기 비교·정리본·판단 도식(createElementNS — innerHTML 없음)·
  인출 확인·변형 문제·복습 목록을 그린다. 학습 기록은 localStorage `medkos_learning_events` 에 **덧붙이기만** 한다.
  상태(복습 필요·복습 중·재확인 완료)는 기록에서 계산하고, 규칙은 `pipelines/learning_log.py` 와 **같아야 한다**
  (`test_learning_books.py` 의 JS/Python 일치 시험 — PC 엔 node 가 없어 Actions 에서 돈다). 열람은 학습 증거가 아니다 —
  재확인 완료는 다음 날 이후 같은 목표의 다른 문항·변형 문제를 맞혔을 때만.
- 문항 머리표의 subtopic 은 **채점 뒤에만** 보인다(`docs/app.js tagText` — 답을 말해 버리는 subtopic 이 많았다).
- 기록 → 저장소: Cloudflare `functions/api/learning.js`(eid 합집합 → `state/learning_sync/events.json`, 사용자 데이터라
  커밋) 또는 앱의 「학습 기록 내보내기」 파일을 드라이브 `MedKOS/학습기록` 에 두면 books.yml 이 가져와 합친다.
- **다시 풀 날 · 변형 · 보정(2026-09-23 사용자 채택)**: ① `learning_log.schedule()` = learn.js `schedule()` — 틀린 날 +1일·+7일
  (기본값일 뿐 최적값이 아니다, 앱 「개념 복습」에서 바꿈)에 「오늘 다시 풀 것」, 그 문항에서 나온 변형(`variants[].of`)을 먼저 낸다.
  ② `concept_queue.py` — `[note]`·`[link]`·`[touch]`·`[variant]`(틀린 문항마다 flip true/false 2개)·`[dist]`(고른 오답 보기 설명)·
  `[restyle]`(판형 2로 옮길 옛 정리본)·`[gap]`(기본틀 빈 자리). 규칙은 모두 `/gen-concept`.
  ③ 판단 사슬 `design.chain`(2026-09-24 이후 필수) · 하루 세트 구성(3단계 이상 40 %↑, 한 목표 50 %↓, 치료+다음 처치 55 %↓,
  정답 순서 순환 금지 — `lint_questions.py` 끝 WARN). ④ `item_stats.py` — 학습자 1명이라 **문항별 통계는 내지 않고** 묶음(20↑)만 판정.
- **정리본 판형 2(2026-09-25, `note_form: 2`)**: 결론·시험 단서·왜 → 틀린 보기별 pitfalls → 표·도식 → 목표에 맞춘 본문.
  옛 정리본은 `[restyle]` 로 하나씩 옮긴다(재배치만, 새 사실 추가 없음). 본보기와 예산은 `/gen-concept` 「판형 2」.
- 학습서: `.github/workflows/books.yml`(cron 06:30 KST) → 코드 시험(관문) → `test_content.py`(실제 콘텐츠, 비관문) →
  `check_sources.py`(pmid → PubMed 정정·철회 지문, DOI 만이면 PMID 를 찾아 기억, 없으면 doi.org 등록만) →
  `build_books.py`(바뀐 책만, 렌더 후 검증 통과한 것만 — 한 책 실패는 그 책의 이전 PDF 를 유지) →
  `drive_books.py`(폴더 ID `pipelines/books_config.yaml`, 같은 파일 ID 갱신, archive/ 사본,
  드라이브 쪽이 바뀌었으면 필기 보호로 덮어쓰지 않음, 아무것도 지우지 않음). 판 기록 `state/books/`.
- `MedKOS/content` 는 drive-sync 의 `rclone sync` 대상이라 거기엔 아무것도 두지 않는다(지워진다).
- **학습서 판형(2026-09-18, 이전 PDF 요구보다 우선)**: 의학 내용만 싣는다 — 들어온 이유·오답 날짜·문항 번호·열람/복습 상태·
  스스로 묻기·변형 문제 안내·내부 ID·경로·사용법은 PDF 에서 빼고 앱·원본에 둔다(오답 혼동은 `pitfalls` 로 일반화).
  A4 가로 2단, 넓은 표·큰 도식만 두 단 전체, 강제 쪽 나눔 없음. `build_books.py` 가 렌더 뒤 빈 단·고립 제목·도식 크기를
  검사하고, 빈 공간이 생기면 도식·기준표 위치를 바꿔 다시 렌더한다. 판형·도식 배치를 바꾸면 `books_config.yaml template_version` 을
  올린다(8 = 2026-09-25 도식 층 배치). PDF 에 실리지 않는 학습 기록(메모·열람)만 바뀌면 책을 다시 만들지 않는다.
- **판단 도식 배치(2026-09-25)**: `decision_diagram.layout` 은 층 배치다 — 긴 선은 층마다 경유점으로 노드 사이를 곧게 지나고,
  층 안 순서는 교차가 가장 적은 것, 가로 위치는 포트 정렬 최소제곱, 틈마다 가로선 트랙을 나누고, 조건 라벨은 판단 노드 바로 아래.
  geometry 형식은 웹(learn.js)과 PDF 가 같이 쓴다. 회귀: `test_skip_edges_do_not_overlap_cross_or_hide_labels`.
- **단원 순서 = 기본틀(2026-09-21)**: `content/outline/subjects.yaml` 이 과마다 「어떤 순서로 쌓일지」를 정한다.
  순서의 뼈대는 해리슨 21판 목차 `content/outline/harrison_toc.json`(`harrison_toc.py` 가 PDF 에서 한 번 뽑았다 —
  **순서를 정하려고 교과서를 다시 열지 않는다**). 정리본은 frontmatter `outline: <슬롯 id>` 로 자리를 밝히고,
  `build_books.py` 가 그 순서로 정렬하며 차례에 해리슨 절 이름을 머리글로 넣는다. 비우면 맨 뒤 「배치 대기」(WARN).
  해리슨의 한 장은 **한 과에만** 넣는다(`outline.py` 가 빠진 장·중복을 검사). 해리슨에 없는 과(산부인과·소아과·외과·
  정형외과·비뇨·예방의학·기초의학)는 손으로 적은 슬롯을 쓴다. 근거를 확인할 때는 `harrison_read.py --slot <id>` 로
  **그 장만** 읽고 인쇄쪽을 인용한다(본문은 저장소에 저장하지 않는다). 루틴은 드라이브 `교과서/Harrison_21e_장별` 문서를 읽는다.

## 금지
- DB에 직접 write. `content/` 밖에 콘텐츠 저장. frontmatter 없는 `.md` 생성.
- id 재사용/역행. 임시 컨테이너 메모리에만 의존하는 상태 관리.
- 코드 시험(`test_learning_books.py`)이 실제 콘텐츠를 읽게 하기. 없는 출처·안 본 쪽수 만들기. 모델이 `reviewed` 표시하기.

## 스킬
- `/daily-run` : 하루치 콘텐츠 생성 오케스트레이터(루틴이 이걸 호출)
- `/gen-kmle` `/gen-paper` `/gen-card` : 타입별 생성
- `/scrape-papers` : PubMed 최신 논문 스크랩(recency, 매일)
- `/landmark-papers` : 파트별 고인용 '꼭 봐야 하는' 논문 정리(impact, 주간). iCite 인용랭킹.
  · **논문 탭은 최신:랜드마크 = 50:50 을 지향한다.** 최신은 매일, 랜드마크는 주간이라
    편수를 고정하면 비율이 영영 안 맞는다 → `--target-ratio 0.5` 가 저장된 코퍼스에서
    **부족분을 역산**해 그만큼만 채운다(`--max-run` 은 한 실행 상한).
  · 인용지표(iCite)를 못 읽으면 `citations` 를 0 으로 눌러쓰지 말 것. 0 으로 채우면
    장애가 "고인용 후보 없음"이라는 정상 메시지로 위장돼 **5주간 랜드마크 0편**이었다
    (2026-07~08 실측). 지금은 지표 0건·전 주제 실패 시 `exit 1` 로 CI 가 빨개진다.
    회귀: `python pipelines/test_landmark.py`.
  · PMID 목록은 150개씩 배치로 요청한다(한 URL 에 몰면 `HTTP 414`).
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

## 실행 로그 루프 (예측 방지)
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


## ECG 실험은 여기가 아니다 — `ecg-lab` repo (2026-08-17 분리)
논문을 목표로 하는 ECG 부정맥 실험(`mit-bih/`·`experiments/specs/EXP-*`·`research/`·
quest 노트북)은 **`ehdbddl06001-ui/ecg-lab`** 로 떼어냈다. 여기는 **공부**, 거기는 **연구**다.
- **이 repo에서 실험 코드를 만들지 않는다.** 반대로 거기서 `content/` 카드를 만들지 않는다.
  한 과제는 한 repo 안에서 끝낸다 — 두 repo를 함께 건드리는 PR을 열지 않는다.
- AI 학습 트랙은 **여기 남는다**: `content/ailab/`(주차 카드·`kind: log`·`kind: quest`
  로드맵·mentor 노트), `notebooks/week*`·`ailab_*`, `/gen-ailab` `/ai-weekly`
  `/deepen-week` `/gen-quest` `/ai-mentor` `/ai-debug`, 그리고 실행 로그 루프 전체.
- 다리는 **퀘스트 카드**다. `kind: quest` 카드는 "한 주차로 못 끝낼 열린 문제"를 큐잉하고,
  그 문제를 실제로 파는 실험은 ecg-lab 의 `experiments/specs/EXP-*` 가 맡는다.
  퀘스트 카드에서 대응 실험을 가리킬 땐 **URL로** 건다(상대경로는 여기서 깨진다).
- Codex 와의 협업 규칙(`AGENTS.md`·`docs/AI_COLLABORATION.md`·과제 프롬프트 템플릿)은
  ecg-lab 으로 옮겼다. 실험 과제를 받았다면 그 repo 를 열고 거기 규칙을 따른다.
- Drive `MyDrive/MedKOS/ecg-model/` 은 **이름 그대로 둔다** — 옛 노트북이 그 경로에
  의존한다. 정리 목적의 이동 금지, migration spec 승인 후에만.

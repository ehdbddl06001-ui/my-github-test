# MedKOS — 개인 의료 지식 운영체제

국시(KMLE)·USMLE 대비용 개인 문항·오답·학습서 플랫폼. 이 파일은 매 세션·매 루틴 실행에 자동 로드된다.
규칙은 여기와 `.claude/skills/` 에 두고, 루틴 프롬프트는 얇게 유지한다(프롬프트 원문은 `prompts/`).
사용자는 본2 — **MedKOS 는 국시·USMLE 전용**이다. 학교 내신 기준·문항은 넣지 않는다(학교 정리본은 드라이브 `의대_정리본_제작`).
- **예외(2026-09-28 사용자 결정) — 전문의급 문항**: `의대_정리본_제작` 의 `BOARD` 세트(전문의 시험급, 내신이 아니라 표준의학으로 답하는 문항)는 `work/board_to_medkos.py` 로 `content/kmle/` 에 옮길 수 있다. 조건 셋 — ① 학교 자료 근거(`[L]`·`[S]`·`[필기]`)·교수 이름·강의/수업/내신/정리본 표기·쟁점 번호를 모두 뺀다 ② 출처는 표준 근거만(해리슨 인쇄쪽·지침·논문은 PMID) ③ 그림은 오픈데이터 영상만(강의 슬라이드·교과서 그림 금지 — kmle 카드에는 싣지 않고 소견을 글로 적는다). 태그 `전문의급`·`board`, `source: "전문의급 · <날짜>"`, `review_status: unreviewed`.

## 먼저 볼 곳 — 작업별 길잡이

| 하려는 일 | 규칙 | 핵심 명령 · 파일 |
|---|---|---|
| KMLE·USMLE 문항 만들기 | `/gen-kmle`(품질 규칙·2026-09-25 감사 규칙), `/daily-run` | `lint_questions.py <파일들>` (ERROR 0 · 세트 mix WARN 해소) |
| 함정 계열(보기를 가르는 함정) 등록·조회 | `/gen-kmle` 「함정 계열」 — 파악되면 등록하고 루틴이 두 쪽(trap·mirror) 문항을 채운다 | `traps.py similar/list/queue/check`, 등록부 `content/traps/`, 문항 `design.trap` |
| 오답 정리본 쓰기·손질·판형 2로 옮기기 | `/gen-concept`(판형 2 · 본보기 `cn.derm.pityriasis-versicolor.treatment`) | `concept_queue.py --limit N` → `concepts.py`(오류 0) |
| 기초의학 정리본 · 기초 뿌리 잇기 | `/gen-concept` 「[root]」 — 기전 단위 · 학문별 책 · 앞으로 틀리는 것부터 | `concepts.py --basic`(있는 기초 정리본) · 큐 `[root]` · `books_config.yaml` `disciplines`·`textbooks` |
| 과별 PDF 학습서 | 아래 「오답 뒤 학습 흐름」 | `.github/workflows/books.yml`, `build_books.py --only <과> --out <임시>` |
| 판단 도식 | `decision_diagram.py`(배치는 코드가 정한다) | 노드 글 판단 ≤ 30자 — 안 들어가면 `concepts.py` ERROR |
| 정리본 그림(심전도·조직·영상) | `/gen-concept` 「[figure]」 — **확실한 라벨만**(전문가 데이터셋 라벨·논문 그림 설명) | `concept_figures.py find/add/want/none/reject/status` · 수확은 exam-builder `opendata demand` |
| 오픈데이터 영상 문항 | **여기서 만들지 않는다** — 빌더(`exam-builder`)의 `opendata medkos-export` | `content/imaging/`, `export_imaging_web.py` |
| 매일 심전도(🫀 덱) | 여기서 만들지 않는다 — 빌더의 매일 심전도 트랙(`ecg_daily.yaml` · `opendata ecg-plan`, run `일일심전도_<날짜>`). 덱 = 영상 카드 중 `modality: ECG`, 오답은 `wrong_imaging` 공유 | `docs/app.js` `ECG` · `deckWrong()` |
| AI·코딩 학습 | `/gen-ailab` `/ai-weekly` `/deepen-week` `/gen-quest` `/ai-mentor` `/ai-debug` | 아래 「실행 로그 루프」 |
| 커밋 | `python pipelines/publish.py -m "…"` (콘텐츠 = main, 코드 = `--branch claude/…` + PR) | 아래 「커밋 전 필수 순서」 |

### 루틴(Claude Routine, 클라우드) — 무엇이 언제 도나
| 루틴 | 시각(KST) | 하는 일 | 프롬프트 |
|---|---|---|---|
| 매일 하루 KMLE 문항 제작 | 월·수·금 05:00 | 16과목 × 2문항 + 정리본 큐 조금 | `prompts/routine_kmle.md`(얇음 → `/daily-run`) |
| USMLE 콘텐츠 생성 | 화·목 05:00 | Step 1·2 각 6문항(과목마다 1개, 2026-11-03~) | `prompts/routine_usmle.md` |
| 오답 정리본 06:00·18:00 | 매일 | 정리본 큐 전부(50분 예산, `[root]` 새 기초 정리본은 실행당 2개) → `[figure]` → `[restyle]` → `[gap]` | `prompts/routine_concepts.md` |
| 오픈데이터 영상 세트 | 매일 05:00 | exam-builder → MedKOS 내보내기 | exam-builder 저장소 |

GitHub Actions: `books.yml`(학습서, cron 06:30 이지만 **실제 발화는 2시간 넘게 늦다** — 09-23·24 모두 08:50 무렵),
`wrong-sync.yml`(오답 동기화), `drive-sync.yml`, `scrape-papers.yml`·`landmark-papers.yml`, `pages.yml`.
`tests.yml`(2026-11-10) — **PR 마다 코드 시험**(books.yml 관문 묶음 + `test_question_design.py`·`test_state.py`·`indexer.py --check`). 실제 콘텐츠 전수 검사는 넣지 않는다.
루틴 컨테이너는 **PubMed·doi.org·NCBI 를 막는다**(출처 원문 대조·PMID 찾기는 PC 세션이나 Actions 가 한다).

### 검증 — 무엇을 돌리나
| 명령 | 무엇을 막나 | 관문 |
|---|---|---|
| `python pipelines/indexer.py --check` | frontmatter 계약 | 커밋 전 필수 |
| `python pipelines/lint_questions.py <파일>` | 문항 품질(ERROR)·세트 구성·정답 순서(WARN) | 문항 커밋 전 |
| `python pipelines/concepts.py` | 정리본 계약·**도식이 한 쪽에 들어가는가**·출처·판형 2 예산·분량·중복(WARN) | 정리본 커밋 전 |
| `python pipelines/test_learning_books.py` | 코드 회귀(도식 배치·학습 상태 JS/Python 일치·PDF·드라이브) — **고정 픽스처만** | books.yml 관문 |
| `python pipelines/test_content.py` | 실제 정리본·문항 전수(계약·도식 크기) | books.yml 에서 따로 — 실패해도 다른 책은 만든 뒤 작업을 실패로 알림 |
| `python pipelines/test_question_design.py` | 출제 설계·린트 규칙 | 코드 변경 시 |
| `python pipelines/traps.py check` | 함정 계열 등록부(패턴·출처)·`design.trap` 표시 문항 | 등록부를 고쳤을 때(publish.py 가 자동) |

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
- 함정 계열 등록부 → `content/traps/<id>.yaml`(YAML 하나 = 계열 하나 — 문항 `design.trap` 이 가리킨다, `/gen-kmle` 「함정 계열」).
  외부 문항(학교 시험 등) 원문은 넣지 않는다 — 함정의 구조(단서·오답 계열·정답 계열·반대쪽 조건)만.
- AI·코딩 학습(ailab) → `content/ailab/`  (실습 노트북은 `notebooks/`, Colab+Drive 연동)
- 오픈데이터 영상 문항(imaging) → `content/imaging/{연도}/` + 영상 `docs/assets/imaging/`.
  · **여기서 직접 만들지 않는다** — exam-builder 의 `opendata medkos-export` 가 세트를 옮긴다
    (`schemas/frontmatter.md` imaging 계약). 원본은 빌더 run, 카드는 파생물. 문항 수정은 빌더에서
    폐기 후 재생성. 웹 번들은 `pipelines/export_imaging_web.py`(publish.py 가 자동 실행).
- 해부학(3Q · 임상해부학술기 시험용) 자료는 **2026-11-15 사용자 지시로 모두 지웠다** — `content/anatomy/` · `docs/anatomy*` · `docs/assets/anatomy/` ·
  `pipelines/anatomy_*.py` 와 도해 · 계보 · 실사 복원 스크립트 · `/anatomy-daily`. 되살릴 일이 있으면 git 기록에서 꺼낸다. **3D 아틀라스(`docs/atlas3d*`)는 남아 있다.**

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
4. 새 `.md` 와 재생성된 `docs/` 번들을 함께 커밋(id_counter·seen_topics·seen_papers 는
   파생물이라 커밋 대상이 아니다; ailab 진도를 바꿨다면 `state/ailab_progress.json` 만 포함).
5. 콘텐츠(kmle·usmle·paper·disease·drug·ailab)는 **main 직접 커밋**이 기본이다.
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
- **필기(2026-11-15)** — `docs/ink.js`. 필기장 = 위에 문항 · 내 답 · 정답 · 해설(접힘), 아래 줄 여백, 그 위에 펜슬로 쓴다(펜 = 쓰기 · 손가락 = 넘기기).
  여는 곳 넷: 오답노트의 「✍ 필기」 · 문항 화면의 「✍ 펜으로 풀기」(필기장 안에서 보기를 톡 쳐 채점 → 다음 문항 — 채점 · 학습 기록 ·
  오답노트 저장은 앱의 보기 단추가 그대로 한다 · 전에 쓴 필기는 채점 뒤에 보인다) · 개념 정리본의 「✍ 이 정리본에 필기」(학습서의 단위 —
  학습서 PDF 는 매일 다시 만들어지므로 PDF 가 아니라 정리본에 쓴다 · 절마다 덩이 이름을 붙여 정리본이 고쳐져도 다른 절 필기가 안 밀린다) ·
  첫 화면의 「✍ 필기 모음」. 맞힌 문항은 「★ 정리본에 넣기」(표시 `want_note`)로 개념 복습 · 정리본 큐에 넣는다(`LEARN.setFlag`). 획은 벡터로 기기 안(IndexedDB)에 바로 저장하고, 동기화 키가 있으면
  `functions/api/ink.js` 로 올린다 — **저장소가 공개라서 동기화 키로 잠근 암호문만** 나간다(AES-GCM). 서버는 열지 못하므로
  합치기는 기기가 한다(획 id 합집합 · 지운 획은 묘비 · sha 가 낡으면 409 → 다시 받아 합쳐 재시도).
  저장 위치는 main 이 아니라 **가지 `ink-data`** 의 `state/ink_sync/<exam>/<id>.json`(첫 저장 때 부모 없는 커밋으로 생긴다 ·
  커밋 글머리 `[CF-Pages-Skip]` = Pages 빌드 생략). **이 가지를 main 에 병합하지 않고, 루틴 · 파이프라인은 읽지 않는다**(열 수 없다).
  동기화 키를 바꾸면 옛 필기는 옛 키로만 열린다. 덩이(문항 · 보기 · 해설 · 여백) 폭은 820 고정이고 획은 **덩이 왼쪽 위에서 잰 좌표** —
  그래서 가로 화면의 「나란히」(문항 옆에 여백)와 세로로 쌓기가 같은 필기를 같은 자리에 그린다. 덩이 **안** 모양을 화면 폭에 따라
  바꾸는 CSS 를 넣지 않는다(`.ink-sheet` 재정의 참고). 3판(2026-11-15 써 본 뒤): 획은 가운데 → 가운데 곡선을 잘게 나눠 굵기(압력 · 빠르기)를
  바꿔 가며 그린다 — **쓰는 동안과 다시 그릴 때가 같은 식**(`piece` · `widthsOf`)이어야 한다 · 색 12 + 형광펜 5 + 굵기 5 · 직선(단추 또는
  긋다가 멈춤) · 펜 기본은 고른 굵기 · 지우개 범위 원. **로그인**(앱을 열 때 키가 없으면 로그인 화면 · 「동기화 설정」의 로그인/로그아웃 · 필기장의 「🔑 로그인」 — 기록을 맞추는 문이지 잠금장치가 아니다:
  문항 · 앱은 공개라 화면을 가려도 막지 못하므로 「로그인 없이 쓰기」를 둔다): 아이디 · 비밀번호에서 기기가 동기화 키를
  계산한다(`loginKey` — PBKDF2 · 아이디가 소금) → 어느 기기에서나 같은 키, 연결 링크 불필요. 비밀번호 · 키는 서버로 가지 않고, 「맞는지」는
  확인용 암호문 `ink-data:state/ink_sync/meta/login-check.json` 이 그 키로 열리는지로 본다(없으면 처음 만드는 로그인). 이 방식에서는
  Cloudflare 의 `SYNC_KEY` 를 **넣지 않는다**(넣으면 계산한 키와 달라 401). 비밀번호를 잊으면 필기를 되찾을 수 없다.
  **학습서 필기(2026-11-15 · 같은 날 2차 「항상 최신판 위에 필기」)** — 메뉴 줄 「📖 학습서 필기」: 정리본을 PDF 학습서와 같은 책 이름(과목 →
  `books_config.yaml` 의 `books`, `ink.js` 의 `BOOKS` 와 같아야 한다)으로 묶어 늘어놓고 눌러서 쓴다. 종이는 **늘 최신 정리본**이고 필기는
  절 제목을 따라 그 위에 남는다 — 「내 필기본」 같은 구분은 두지 않는다(사용자: 여러 번 볼 것이라 나눌 까닭이 없다). 필기할 때의 판은
  조용히 떠 두었다가(`doc.n = { at, ver, updated, hash, c }`) 정리본의 지문(`hash`)이 달라지면 머리띠로 「정리본이 고쳐졌습니다 · 바뀐 곳」을
  알리고, 「확인」(떠 둔 판을 지금 판으로) · 「전에 쓴 판 보기」(읽기만 — 필기가 맞던 글)를 고르게 한다. 정리본이 목록에서 빠지면 떠 둔 판을 그린다.
  드라이브의 PDF 에 직접 쓰는 방식은 권하지 않는다 — 매일 다시 만들어져 쪽이 밀리고, 드라이브 쪽 파일이 바뀌면 `drive_books.py` 의
  「필기 보호」로 그 책의 새 판이 올라오지 않는다.
  **선명도 · 한 쪽 보기(5판)** — 필기 캔버스(`.ink-layer`)는 transform 을 건 종이(`.ink-sheet`)의 **형제**다. 종이 안에 캔버스나 스스로
  스크롤하는 상자(`overflow:auto` 표 · 그림 · 도식)가 있으면 Safari 가 종이를 통째로 저해상도 그림으로 굳힌 뒤 늘려 글자가 흐려진다 — 종이 안에
  그런 것을 다시 넣지 않는다. 조각 캔버스는 화면 512 px 격자(`TPX`)라 확대해도 화소 밀도가 유지된다. 정리본은 두 단(`▥ 두 단` · 단 사이 56 →
  둘째 단 덩이의 기준점이 정확히 820 · 덩이는 단 사이에서 쪼개지 않는다)으로 한 화면에 담고, 두 손가락(또는 Ctrl + 휠)으로 확대 · 축소한다.
  모든 화면의 메뉴 줄에 「📖 학습서 필기」가 있고(`index.html?view=shelf`), 「✍ 필기 모음」은 그 안의 단추다 — 첫 화면 단추 줄에는 필기 단추를 두지 않는다.
  필기 모음은 종류(KMLE · USMLE · 정리본 · 논문 — 영상 · 변형은 필기가 있을 때만) → 분야(책 이름) 순으로 묶고, KMLE · USMLE 는 틀린 문항(지금
  오답노트에 있는 것) / 맞힌 문항을 따로 본다. 논문 칸은 펜 필기가 아니라 논문 화면의 메모(`medkos_paper_notes`, 이 기기)다.
  회귀: `python pipelines/test_ink.py`.

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
  **퀴즈 덱(2026-11-10)**: 첫 화면 「🔔 오늘 다시 풀 것 N개 풀기」 = 학습 구역 `due`(`docs/app.js` `dueList()` → learn.js `pickRetest`,
  종목 선택과 무관 · 오래 밀린 순, 홈 화면 바로가기 `?mode=due`). 그 전에는 개념 복습 화면에서 하나씩 눌러야만 나와
  예정 74개가 전부 밀리고 끝난 것이 0이었다 — 복습 흐름을 고칠 때는 「일정이 실제로 소화되는가」를 `item_stats`·기록으로 본다.
  **과목 돌림(2026-11-23 사용자 선택 「덜 푼 과목 먼저」)**: 「문항 순서 섞기」를 켜지 않은 「최신 세트」·「안 푼 문항」은
  `docs/app.js` `orderedList()` → `balanceBySubject()` 가 최신 날짜 묶음부터, 그 안에서 **지금까지 푼 문항이 적은 과목부터
  한 문항씩 번갈아** 낸다(푼 수가 같으면 그날 날짜가 씨앗 — 같은 날엔 같은 순서). `due`·오답노트·푼 문항·기간·전체는 그대로.
  그 전에는 번들이 id 내림차순(= 하루 세트의 과목 영어 이름 역순)이라 늘 류마티스 → 호흡기 → … → 순환기로 나와, 푼 문항이
  류마티스 14 · 순환기 1 로 쏠리고 오답 정리본도 그 과에만 쌓였다 — **순서를 정하는 곳에는 「어느 과가 늘 앞에 오는가」를 본다.**
  ② `concept_queue.py` — `[note]`·`[link]`·`[touch]`·`[root]`(기초 뿌리, 2026-11-21)·`[variant]`(틀린 문항마다 flip true/false 2개)·`[dist]`(고른 오답 보기 설명)·
  `[restyle]`(판형 2로 옮길 옛 정리본)·`[gap]`(기본틀 빈 자리)·`[verify]`(미대조 표시 보강 — 루틴 밖). 규칙은 모두 `/gen-concept`.
  `[gap]` 의 책 순서는 **정리본이 적은 책 먼저**(같으면 기본틀 순서, 정리본 0개인 책 · 기초의학 학문별 책은 제외 — 오답 · `[root]` 가 이끈다, 2026-11-23).
  많은 책 먼저였을 때 06시 루틴이 맨 앞 하나만 써서 한 과만 불었다(10월 류마티스 12개 · 11월 순환기 23개).
  **국시 핵심 공백 과목 먼저(2026-11-23 사용자 결정)** — `books_config.yaml` `gap_priority` 의 여섯 책(혈액종양 · 소화기 · 신경 · 감염 ·
  내분비 · 외과) 가운데 정리본이 12개 미만인 책이 앞 묶음이고 그 안에서도 적은 책부터다. 12개가 된 책은 일반 순서로 내려가고,
  여섯 책이 모두 12개가 되면 전체 「적은 책 먼저」와 같아진다. 책 목록 · 기준 수는 코드가 아니라 그 설정에서 바꾼다.
  `[verify]`(2026-11-23 사용자 결정) — 원고에 미대조 표시(`[[?출처]]` · 손으로 적은 `†`)가 남은 정리본. **PC 세션 · Actions 전용**이다
  (루틴은 PubMed · 지침 원문을 못 연다): 기본 출력에는 건수 한 줄만, 목록은 `concept_queue.py --verify`(JSON 에는 늘 있다).
  `concepts.py` 의 분량 · 중복 린트(본문 3,200자 · `diagram_notes` 4줄 · summary↔`## 판단` 되풀이 · 변형 없음)는 **WARN 만** 낸다 — 관문은 막지 않는다.
  ③ 판단 사슬 `design.chain`(2026-09-24 이후 필수) · 하루 세트 구성(3단계 이상 40 %↑, 한 목표 50 %↓, 치료+다음 처치 55 %↓,
  정답 순서 순환 금지 — `lint_questions.py` 끝 WARN). ④ `item_stats.py` — 학습자 1명이라 **문항별 통계는 내지 않고** 묶음(20↑)만 판정.
- **기초 뿌리 · 기초의학 학문별 책(2026-11-21 사용자 결정)**: 임상 정리본(판단) 밑의 기초 기전을 **기초 정리본**(`layer: basic`)으로 따로 쓰고,
  임상 정리본이 `roots` 로 가리킨다(기초 기전이 없는 목표는 `roots_none: "<이유>"` — 검진 주기 · 법규 · 역학 계산 · 지침 수치). 기초 정리본은
  **기전 단위**라 임상 정리본 여러 개가 하나를 함께 가리킨다 — 문항마다 만들지 않고, 있으면 잇기만 한다(`concepts.py --basic`).
  「기초의학」 한 권은 **일곱 권**(생리학 · 병리학 · 약리학 · 생화학·유전 · 미생물학 · 면역학 · 해부·조직·발생)으로 나눴다 — topic → 책은
  `books_config.yaml` `books`(`docs/ink.js` `BOOKS` 와 같아야 한다), 학문 꼬리표 → 책은 `disciplines`. 임상 책에 실린 기초 성격 정리본은
  옮기지 않고 `discipline` 꼬리표만 달아 학문별 책 목차 쪽 「다른 책에 실린 단원」에 제목을 적는다. **소급하지 않는다** — 큐 `[root]` 는
  `ROOTS_FROM`(2026-11-21) 이후에 틀린 목표만 낸다. **예외(2026-11-23 사용자 결정)** — 반복 오답 상위 20개 임상 정리본
  (2회 이상 틀린 것 · 오답 수 → 우선순위 → id, `concept_queue.ROOT_BACKFILL_TOP`)만 그 전 오답이라도 `[root]` 에 「상위 20 소급」으로 올린다.
  상위 20 은 뿌리가 붙었는지와 무관하게 뽑으므로 21위가 빈자리를 채우지 않는다 — 나머지 옛 정리본은 다시 틀릴 때만. 전공 교과서(`textbooks` — Robbins Basic 10e · Katzung 14e · Junqueira 13e, 드라이브 `교과서/`)는
  아직 읽기 도구가 없어 `textbook_check: pending`, 교과서가 없는 학문은 `unavailable` — 둘 다 해리슨 22판으로 대조하고 학습서에
  「전공 교과서 미대조」가 붙는다. 교과서가 낡은 곳의 최근 10년 고인용 종설 · 합의문 보강은 PC 세션 몫이다(루틴은 PubMed 를 못 연다) —
  본문에 섞지 않고 `## 최근 근거` 절과 「시험 쟁점」 새 근거로. 남은 일: 교과서 장별 문서 · 읽기 도구(2단계), 최근 근거 흐름 · 앱 연결(3단계).
- **정리본 판형 2(2026-09-25, `note_form: 2`)**: 결론·시험 단서·왜 → 틀린 보기별 pitfalls → 표·도식 → 목표에 맞춘 본문.
  옛 정리본은 `[restyle]` 로 하나씩 옮긴다(재배치만, 새 사실 추가 없음). 본보기와 예산은 `/gen-concept` 「판형 2」.
- 학습서: `.github/workflows/books.yml`(cron 06:30 KST) → 코드 시험(관문) → `test_content.py`(실제 콘텐츠, 비관문) →
  `check_sources.py`(pmid → PubMed 정정·철회 지문, DOI 만이면 PMID 를 찾아 기억, 없으면 doi.org 등록만) →
  `build_books.py`(바뀐 책만, 렌더 후 검증 통과한 것만 — 한 책 실패는 그 책의 이전 PDF 를 유지) →
  `drive_books.py`(폴더 ID `pipelines/books_config.yaml`, 같은 파일 ID 갱신, archive/ 사본,
  드라이브 쪽이 바뀌었으면 필기 보호로 덮어쓰지 않음, 아무것도 지우지 않음). 판 기록 `state/books/`.
- **정리본 ↔ 스크랩 논문(2026-11-15)** — `pipelines/export_related_web.py` → `docs/related.js`(publish.py 번들 단계가 매일 다시 만든다).
  정리본의 영어 용어(id 둘째 마디 · `condition` 괄호 안)가 논문 **제목**에 있으면 잇고, 초록만이면 여러 번 나와야 한다. 약어는 제목에서만 ·
  긴 용어가 글에 함께 있을 때만, 제목 끝의 발행 기관 이름은 뺀다. **글자가 겹친다는 사실만** 적는다(의미 판단 ✗ · 화면에도 그렇게 적는다 —
  틀린 연결은 없는 것보다 나쁘다). 정리본 화면 「관련 논문」 → `papers.html?id=` · 논문 카드 「관련 정리본」 → `index.html?concept=`.
  회귀: `python pipelines/test_related.py`.
- `MedKOS/content` 는 drive-sync 의 `rclone sync` 대상이라 거기엔 아무것도 두지 않는다(지워진다).
- **학습서 판형(2026-09-18, 이전 PDF 요구보다 우선)**: 의학 내용만 싣는다 — 들어온 이유·오답 날짜·문항 번호·열람/복습 상태·
  스스로 묻기·변형 문제 안내·내부 ID·경로·사용법은 PDF 에서 빼고 앱·원본에 둔다(오답 혼동은 `pitfalls` 로 일반화).
  **판형 10(2026-09-27, 사용자 선택)**: A4 **세로 2단(해리슨식)**, 본문 8.4pt·좁은 여백(아이패드에서 확대해 읽는다).
  1쪽 = 목차만(두 단), 본문은 2쪽부터. 표·그림은 모두 한 단(92 mm) 안 — 3칸 넘는 표·기준은 「항목 머리줄 + 이름|내용」 표
  (`record_table`), 줄이 이상하게 꺾이면 **글씨를 줄인다**(칸 수별 7.3/6.9pt, 이름 칸 nowrap, 낱말 중간 끊기 금지).
  단원 머리(제목·학습 목표·한눈에)는 한 덩어리. 도식은 항목 경계에서만 줄바꿈(`dd.phrase_wrap`)하고, 한 단에서 글자가 너무
  작아지면 **두 단 전체**(`diablock` — 「도식에 담기지 않은 조건·예외」까지 붙여 쪼개지 않음). 검증: 빈 단·고립 제목·도식 크기 +
  **두 단 도식 위·아래 좁은 띠(<20%, 좌→우→다음 쪽으로 오가며 읽힘)**. 배치 탐색은 두 단 도식을 먼저 0.88·0.76배로 줄여 보고
  (글자 ≥ 5.6pt), 아래 여백(14·28·42 mm)으로 좁은 띠를 다음 쪽으로 넘기거나 한 단으로 바꿔 보고(한 단 ≥ 5.2pt), 다음에 자리를 옮긴다.
  그림도 같은 절 안 자리 → 0.85·0.75배 축소를 시도한다. 단원 머리는 제목+학습 목표만 붙이고 긴 「한눈에」는 쪽을 넘길 수 있다(판형 11). 약·약군 이름은 **english(한글)**(단원 첫 등장, 그 뒤 english) — `pipelines/english_terms.py`,
  표는 `content/glossary/drugs_ko_en.yaml` → `python pipelines/verify_glossary.py`(약 = RxNorm, 약군 = MeSH 로 확인된 것만
  `verified.json` 에 들어가고 조판은 그것만 쓴다. 새 약 이름은 표에 넣고 확인 — 영어를 지어내지 않는다). 원고는 한글로 둔다.
  판형·도식 배치를 바꾸면 `books_config.yaml template_version` 을 올린다. PDF 에 실리지 않는 학습 기록(메모·열람)만 바뀌면
  책을 다시 만들지 않는다. 약 이름 표가 바뀌면 책 해시가 바뀌어 다시 만든다.
- **판단 도식 배치(2026-09-25)**: `decision_diagram.layout` 은 층 배치다 — 긴 선은 층마다 경유점으로 노드 사이를 곧게 지나고,
  층 안 순서는 교차가 가장 적은 것, 가로 위치는 포트 정렬 최소제곱, 틈마다 가로선 트랙을 나누고, 조건 라벨은 판단 노드 바로 아래.
  geometry 형식은 웹(learn.js)과 PDF 가 같이 쓴다. 회귀: `test_skip_edges_do_not_overlap_cross_or_hide_labels`.
- **단원 순서 = 기본틀(2026-09-21)**: `content/outline/subjects.yaml` 이 과마다 「어떤 순서로 쌓일지」를 정한다.
  순서의 뼈대는 해리슨 21판 목차 `content/outline/harrison_toc.json`(`harrison_toc.py` 가 PDF 에서 한 번 뽑았다 —
  **순서를 정하려고 교과서를 다시 열지 않는다**). 정리본은 frontmatter `outline: <슬롯 id>` 로 자리를 밝히고,
  `build_books.py` 가 그 순서로 정렬하며 차례에 해리슨 절 이름을 머리글로 넣는다. 비우면 맨 뒤 「배치 대기」(WARN).
  해리슨의 한 장은 **한 과에만** 넣는다(`outline.py` 가 빠진 장·중복을 검사). 해리슨에 없는 과(산부인과·소아과·외과·
  정형외과·비뇨·예방의학·기초의학)는 손으로 적은 슬롯을 쓴다. 근거를 확인할 때는 `harrison_read.py --slot <id>` 로
  **그 장만** 읽고 인쇄쪽을 인용한다(본문은 저장소에 저장하지 않는다).
  **대조는 해리슨 22판 DB(2026-10-31 사용자 지시)** — 드라이브 `교과서/Harrison_22e_장별/H22_<장>` 문서. 슬롯 id 는 21판 장 번호 그대로 두고
  `content/outline/harrison22.json`(`harrison22_build.py`)의 대응표로 22판 장을 찾는다 → `outline.py --harrison <슬롯>` 이 22판 장·인쇄쪽·문서 ID·
  인용 `[[harrison-22: 장 p.N]]` 을 준다. 22판에 없는 21판 장(7·417·484)만 21판 문서(`Harrison_21e_장별`)로. 기존 `harrison-21` 인용은 유효하다.
  **문항(KMLE·USMLE·영상)의 해리슨 인용도 22판(2026-11-02 사용자 지시)** — `harrison_cite.py --find <주제>` 로 22판 장 번호·제목을 찾아
  `Harrison's Principles of Internal Medicine, 22e. <장>장 <제목>` 으로 쓴다(장 번호를 기억으로 쓰지 않는다 — 판마다 다르다).
  `lint_questions.py` 가 2026-11-03 이후 문항의 21판 인용·장 번호 오류를 ERROR 로 막는다. 규칙 `/gen-kmle` 「해리슨 인용」.

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

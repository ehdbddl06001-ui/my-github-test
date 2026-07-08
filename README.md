# MedKOS — Medical Knowledge Operating System

의대~국시~수련~연구까지 10년 이상 쓸 **개인 의료 지식 플랫폼**.
"AI가 공부를 도와주는 프로그램"이 아니라, 데이터가 쌓일수록 자산이 되는
**의료 지식 운영체제**를 목표로 한다.

## 한 줄 철학
> **Markdown이 진실의 원본(Source of Truth), SQLite는 언제든 다시 만들 수 있는 색인,
> Google Drive는 백업.** 루틴은 얇게, 규칙은 repo에.

이 구조는 특정 AI 서비스·DB에 종속되지 않는다. 원본은 항상 사람이 읽는
Markdown이고, SQLite/벡터DB는 그 원본에서 재생성되는 파생물이다.

## 계층 (Data → Knowledge → Learning → Research → Clinical reasoning)

```
Claude Code (매일 자동 실행: 루틴 / GitHub Actions)
      │
      ├──► GitHub          코드·프롬프트·규칙 버전관리 (이 repo)
      ├──► Google Drive    원본(Markdown/PDF/이미지) 백업
      └──► SQLite (FTS5)   검색용 색인 (재빌드 가능) → 이후 ChromaDB/RAG로 확장
              │
              ├── CLI:  pipelines/search.py    (FTS5 직접 조회 + 대시보드)
              └── 웹:   docs/search.html       (content/→search-index.js 통합검색)
```

## 통합검색 · 대시보드

쌓인 콘텐츠(kmle/usmle/basic/paper/disease/drug)를 한곳에서 찾는다. 원본은 언제나
`content/**/*.md`, 검색은 그 파생 색인을 쓴다.

```bash
python pipelines/search.py 심부전             # 전문검색(FTS5)
python pipelines/search.py SGLT2 --type kmle   # 타입/주제/태그 필터
python pipelines/search.py --stats            # 대시보드: 무엇이 얼마나 쌓였나
python pipelines/export_search_web.py          # content/ → docs/search-index.js (웹 검색·대시보드)
```

- **CLI**는 `db/medkos.sqlite`(FTS5)를 직접 조회한다. 색인이 없으면 자동 재빌드(파생물).
- **웹**(`docs/search.html`)은 정적 GitHub Pages라 SQLite를 못 쓰므로, `content/`에서
  내보낸 `docs/search-index.js`를 브라우저에서 검색한다(퀴즈·논문 번들과 같은 방식).

## 저장소 구조

```
.
├── CLAUDE.md                 # 매 세션·매 루틴에 자동 로드되는 규칙 (핵심)
├── .claude/
│   ├── settings.json         # 파이프라인 실행 권한
│   └── skills/               # 타입별 생성 + 색인 스킬 (자동/슬래시 호출)
│       ├── daily-run/        # 하루치 오케스트레이터 (루틴이 호출)
│       └── gen-kmle/  gen-basic/  gen-paper/  gen-card/  index-db/
├── schemas/frontmatter.md    # 저장 규격(계약). 모든 .md가 따름
├── pipelines/                # 결정론적 작업(파싱·색인·ID·상태)은 파이썬이 담당
│   ├── frontmatter.py        # frontmatter 파싱·검증
│   ├── indexer.py            # content/ → SQLite(FTS5) 재빌드
│   ├── search.py             # SQLite(FTS5) 조회 CLI + 대시보드(--stats) — 색인의 소비자
│   ├── state.py              # ID 발급 + N일 중복방지 (ephemeral 컨테이너 대응)
│   ├── export_usmle_web.py   # content/usmle/*.md → docs/questions_usmle.js (웹 퀴즈용)
│   ├── export_search_web.py  # content/**/*.md → docs/search-index.js (웹 통합검색·대시보드)
│   ├── scrape_papers.py      # PubMed 최신 논문 → content/papers/**/*.md (매일 자동)
│   ├── export_papers_web.py  # content/papers/**/*.md → docs/papers.js (홈페이지 논문 피드)
│   ├── apply_notes.py        # 홈페이지 노트(.json) → 카드의 ## My Ideas 반영(왕복)
│   ├── fixtures/             # 오프라인 테스트용 PubMed XML 샘플
│   └── db_schema.sql
├── content/                  # ★ 원본 (kmle/usmle/basic/papers/diseases/drugs)
├── state/                    # id_counter.json, seen_topics.json (커밋됨)
├── prompts/routine_kmle.md   # 얇은 루틴 프롬프트 템플릿
├── db/                       # medkos.sqlite (gitignore, 재빌드됨)
├── .github/workflows/
│   ├── drive-sync.yml        # content/ push 시 rclone로 Drive 백업
│   ├── scrape-papers.yml     # 매일 PubMed 스크랩 → 카드 커밋(→ Drive·Pages 자동 연쇄)
│   └── pages.yml             # docs/ 웹 퀴즈·논문·통합검색을 GitHub Pages로 배포
│
├── kmle/                     # [기존] JSON 기반 KMLE 퀴즈 세트 (현재 Learning 계층)
│   ├── quiz/                 # quiz.py 실행기 + questions/*.json (단일 소스)
│   ├── 문항/  오답노트/       # JSON에서 생성된 읽기용 .md + 오답 기록
└── docs/                     # GitHub Pages (퀴즈 + 논문 + 통합검색)
    ├── index.html            #   🧠 퀴즈 (KMLE + USMLE, 클릭으로 풀기)
    ├── papers.html           #   📄 논문 피드
    ├── search.html           #   🔍 통합검색 · 대시보드
    ├── questions.js          #   KMLE 번들 (quiz.py --export)
    ├── questions_usmle.js    #   USMLE 번들 (export_usmle_web.py)
    └── search-index.js       #   통합검색 색인 (export_search_web.py)
```

## USMLE 웹 퀴즈 (Step 1 / Step 2)

`content/usmle/*.md`(원본)를 웹에서 바로 풀 수 있다. 원본을 고친 뒤 번들만 재생성한다.

```bash
python pipelines/export_usmle_web.py   # content/usmle/*.md → docs/questions_usmle.js
```

- 웹 퀴즈 상단에서 **시험(KMLE/USMLE)**을 고르고, USMLE는 **Step 1(기초의학)·Step 2(임상)**
  로 나눠 과목을 선택해 푼다. 채점·오답노트는 시험별로 분리 저장된다.
- 현재 USMLE는 Step 1·Step 2 **각 6과목 × 2문항 = 24문항**.
  - Step 1: Pharmacology · Immunology · Biochemistry · Microbiology · Pathology · Physiology
  - Step 2: Internal Medicine · Surgery · Neurology · Pediatrics · Obstetrics & Gynecology · Psychiatry

### CLI로도 풀기 (`quiz.py`)

`quiz.py`는 KMLE·USMLE를 모두 지원한다(USMLE는 A~E 입력, Step 필터).

```bash
cd kmle/quiz
python3 quiz.py                          # KMLE (①~⑤)
python3 quiz.py --exam usmle             # USMLE 전체 (A~E)
python3 quiz.py --exam usmle --step 1     # USMLE Step 1(기초의학)만
python3 quiz.py --exam usmle --step 2 --all# USMLE Step 2(임상) 전 과목 연속
python3 quiz.py --exam usmle --review     # USMLE 오답만 다시 풀기
```

USMLE 오답은 `usmle/오답노트/<과목>.md` 에 자동 기록된다(KMLE는 `kmle/오답노트/`).

## 논문 자동 스크랩 → Google Drive 저장 → 홈페이지 피드

매일 PubMed에서 관심 주제의 최신 논문을 긁어와 `content/papers/{연도}/*.md` 카드로 저장하고,
그 카드가 **자동으로 Google Drive에 백업**되며 **홈페이지 논문 피드**에 뜬다. 새 코드 없이
기존 설계(Markdown=원본, Drive=백업, SQLite=색인)에 그대로 얹혔다.

```
scrape-papers.yml (cron 매일 20:00 UTC = KST 05:00) — 자기완결형
  └─ python pipelines/scrape_papers.py       PubMed(esearch+efetch) → content/papers/**/*.md
       └─ python pipelines/indexer.py --check 검증
       └─ python pipelines/export_papers_web.py  → docs/papers.js
       └─ git commit → main
       └─ rclone sync content/ → Google Drive(gdrive:MedKOS/content)   ← 같은 실행 안에서 백업
  (완료 후) pages.yml  → workflow_run 으로 이어받아 docs/ 를 홈페이지로 배포
```

> **왜 백업을 같은 워크플로 안에서 하나?** GitHub Actions는 기본 `GITHUB_TOKEN`으로 만든
> 커밋(=이 봇의 push)이 다른 워크플로(`drive-sync.yml`·`push` 트리거)를 다시 발동시키지
> 못한다(무한루프 방지). 그래서 논문 커밋만으로는 Drive 백업이 자동으로 안 돈다.
> → `scrape-papers.yml`이 스크랩·커밋에 이어 **직접 rclone 백업**까지 하고, 홈페이지 배포는
> `pages.yml`이 `workflow_run`으로 이어받는다. `drive-sync.yml`은 사람이 `content/`를 직접
> 커밋했을 때를 위한 경로로 남긴다.

- **스크랩 카드**는 사실 메타데이터(저널·DOI·PMID·저자·게재일) + **원문 초록**만 담고
  `confidence: medium`. 해석(Summary/Clinical Impact/My Ideas)은 이후 `/gen-paper`로 채운다.
- **중복 방지**는 `state/seen_papers.json`(PMID 단위)로만 판정 → 임시 컨테이너에서 매일 돌아도
  같은 논문을 두 번 저장하지 않는다. id는 `state.next_id('paper')`로만 발급.
- **관심 주제**(8개)는 `pipelines/scrape_papers.py`의 `TOPICS` 딕셔너리에서 조정한다: 심장학·
  감염내과·신장내과·혈액종양내과·병리학·진단검사의학·소아청소년과·외과. 저널 한정은 검색어에
  `AND "Circulation"[Journal]`처럼 덧붙인다.

### 직접 돌려보기

```bash
python pipelines/scrape_papers.py --dry-run           # 무엇을 가져올지만 확인(저장 안 함)
python pipelines/scrape_papers.py --days 7 --max 1    # 스크랩 → 카드 저장(주제당 1편 = 8편)
python pipelines/export_papers_web.py                 # → docs/papers.js 재생성

# 네트워크 없이 파이프라인 검증(오프라인):
python pipelines/scrape_papers.py --fixture pipelines/fixtures/pubmed_sample.xml --topic Cardiology --dry-run
```

홈페이지 상단 내비게이션에서 **🧠 퀴즈 ↔ 📄 논문**을 오간다. 논문 피드는 주제 필터·검색·
초록 펼치기·PubMed 원문 링크를 제공한다(순수 정적, `docs/papers.js`만 읽음).

### 논문 읽고 내 생각·아이디어 적기 (노트)

논문 카드를 열면 **💡 내 생각/아이디어** 입력란이 있다. 읽으면서 적으면 **그 브라우저에 즉시
자동 저장**된다(localStorage, 서버 불필요). 다만 이대로는 그 기기에만 남으므로, 영구 보관·다른
기기 동기화·Drive 백업을 하려면 **카드의 `## My Ideas`로 반영**하는 왕복 경로를 쓴다.

```
홈페이지에서 메모(자동저장)
  → '🗒 내 노트 내보내기(.json)' 클릭 → medkos-notes.json 다운로드
  → python pipelines/apply_notes.py medkos-notes.json   # 각 카드의 ## My Ideas 에 써넣음
  → python pipelines/indexer.py --check && python pipelines/export_papers_web.py
  → git commit → main  (→ Drive 백업, 홈페이지에 '저장됨'으로 표시)
```

- `apply_notes.py`는 노트의 논문 id로 카드 파일을 찾아 `## My Ideas`를 교체하고 frontmatter에
  `updated:`를 남긴다. `--dry-run`으로 미리 확인 가능.
- 빠른 백업만 원하면 '📄 내 노트 미리보기(.md)'로 사람이 읽는 마크다운 한 장을 받아 Drive에
  그대로 둘 수도 있다(카드 반영과는 별개).
- 카드에 이미 반영된 노트는 피드에서 **My Ideas (저장됨)**으로 보이고, 입력란은 새 초안용이다.

### 준비물 (한 번만)

- **Google Drive 백업** — repo Secret **`RCLONE_CONF_BASE64`** 하나만 설정한다.
  1) 로컬에서 `rclone config`로 이름이 **`gdrive`**인 Google Drive 원격을 만든다(브라우저 로그인).
  2) 설정 파일을 **base64로 인코딩**해 그 값을 Secret에 넣는다.
     (텍스트 그대로 넣으면 토큰 JSON의 따옴표·줄바꿈이 전달 중 깨져 `invalid character …`
     오류가 난다. base64는 특수문자가 없어 안전하다.)
     ```bash
     # macOS/Linux
     base64 -w0 ~/.config/rclone/rclone.conf   # 출력 전체를 복사
     ```
     ```powershell
     # Windows PowerShell (클립보드로 바로 복사)
     [Convert]::ToBase64String([IO.File]::ReadAllBytes("$env:APPDATA\rclone\rclone.conf")) | Set-Clipboard
     ```
  3) GitHub ▸ Settings ▸ Secrets and variables ▸ Actions ▸ New repository secret →
     Name `RCLONE_CONF_BASE64`, 값에 붙여넣기.
  - Secret이 없으면 스크랩·커밋은 정상 진행되고 백업 단계만 건너뛴다.
- **홈페이지**: Settings ▸ Pages ▸ Source = "GitHub Actions" (기존 퀴즈와 동일).
- **스크랩 권한**: `scrape-papers.yml`은 `contents: write`로 main에 직접 커밋한다.
  (GitHub Actions 러너는 외부망이 열려 있어 PubMed 접근에 별도 설정이 필요 없다.)

## 🤖 AI랩 — 의료 AI·코딩 실습 (공개 프로젝트 분석 → 오픈데이터 실습)

의대 공부와 별개로 **의료 AI·코딩을 직접 해보며** 익히는 기둥. 공개 프로젝트(예: Keras
[뇌종양 분할](https://keras.io/examples/vision/brain_tumor_segmentation/))을 뜯어보고,
오픈 의료 데이터로 **매주 하나씩** 모델을 돌린다. 기존 설계에 그대로 얹혔다 —
Markdown(`content/ailab/`)이 원본, 결정론(데이터·주차)은 `pipelines/datasets.py`, 실습은
`notebooks/`(Colab)에서, 홈페이지 `🤖 AI랩` 탭이 색인이다.

```
content/ailab/*.md      학습 카드(원본): 프로젝트 분석·구조 도식(Mermaid)·지시어 해설·실습과제
pipelines/datasets.py   오픈 데이터 레지스트리 + 12주 커리큘럼 + '이번 주 주제' 결정론 선정
notebooks/*.ipynb       Colab 노트북(Google Drive 마운트 → 데이터·체크포인트 재사용)
docs/ailab.html         홈페이지 🤖 AI랩 (이번주 주제 + 오픈데이터 카탈로그 + 학습카드)
```

**1) 공개 프로젝트 분석** — 카드 하나에 `## Overview / Architecture(도식) / Data /
Code walkthrough / Instructions(지시어→무엇을 시키는가 표) / Exercises / Resources`를 담는다.
예: `content/ailab/ailab-2026-0002.md`(Keras 3D U-Net 뇌종양 분할).

**2) Colab + Google Drive 실습** — `notebooks/`의 노트북이 GitHub에서 Colab으로 바로 열리고,
첫 셀이 Drive를 마운트해 데이터·체크포인트를 `MyDrive/MedKOS/`에 재사용한다. 셋업·코드 읽는
법은 `content/ailab/ailab-2026-0003.md`.

**3) 오픈 데이터 + 매주 실습** — EKG(PTB-XL·MIT-BIH), 3D 뇌 MRI(BraTS·MSD·IXI), 흉부
X선·CT·병리·피부·안저·EHR까지 접근조건(🟢open/🟡가입/🔴심사)과 함께 정리. **이번 주 주제는
코드가** 정한다(ISO 주차 기준, LLM 아님):

```bash
python pipelines/datasets.py                 # 이번 주 주제 + 오픈 데이터 카탈로그
python pipelines/datasets.py --modality ecg   # 양식별 필터
python pipelines/export_ailab_web.py          # content/ailab + datasets.py → docs/ailab.js
```

매주 도는 흐름은 `/ai-weekly`, 새 프로젝트 분석 카드는 `/gen-ailab` 스킬이 만든다(신규
타입이라 self-verify 한계 → claude/ 브랜치 push 후 PR로 검수).

**4) 클로드와 토론(멘토)** — `/ai-mentor`는 최근 학습(`content/ailab/`·`notebooks/`)을 검토해
**심화 학습·코드 보완·새 기능 아이디어**를 제안하고, 채팅으로 흘리지 않고 **repo에 쌓이는
논의 노트**(`content/ailab/mentor/mentor-YYYY-Www.md`)로 남긴다. 노트의 `## 내 답변`에 답을
적으면 다음 회차가 그 맥락을 이어받는 **비동기 토론 스레드**가 된다(홈페이지 🤖 AI랩 맨 위 표시,
Drive 백업). 결정론 검증은 `python pipelines/test_datasets.py`로 커밋 전 돌린다.

## 지금 상태 (1단계 스캐폴드)

이 커밋은 **큰 틀(구조)**을 세운 것이다. 아직 대량 콘텐츠 마이그레이션은 하지 않았다.

- **MedKOS 코어**: `content/`·`pipelines/`·`schemas/`·`state/`·`.claude/skills/`가
  자리를 잡았고, `content/kmle/2026/kmle-2026-0001.md` 예시 1개가 규격대로 들어있다.
- **기존 KMLE 퀴즈**(`kmle/`, `docs/`)는 그대로 **살려 둔다.** 지금은 실제로 매일
  돌아가는 Learning 계층이며, 아래 마이그레이션 순서에 따라 점진적으로 `content/`로
  옮겨간다. 한 번에 갈아엎지 않고 작은 diff로 조정한다.

## 설치 / 동작 확인

```bash
pip install -r requirements.txt          # pyyaml
python pipelines/indexer.py --check      # frontmatter 검증
python pipelines/indexer.py              # SQLite 재빌드 → db/medkos.sqlite 생성
```

## 매일 도는 흐름 (루틴)

1. Claude Routine이 `prompts/routine_kmle.md`의 **얇은 프롬프트**로 실행
2. `/daily-run` 스킬을 따라: 최근 주제 확인 → 생성 → `.md` 저장 → 주제 기록 →
   `indexer.py`로 검증·색인 → 커밋·푸시
3. `content/`가 push되면 GitHub Action이 Google Drive로 백업

세부 규칙은 전부 `CLAUDE.md`와 `.claude/skills/`에 있으므로 **루틴 프롬프트에 규칙을
복사하지 않는다.** 이것이 이 설계의 핵심이다.

## 기존 JSON 퀴즈 → MedKOS 마이그레이션 (작은 diff부터)

기존: `루틴 → 과목별 JSON 문항 생성 → 웹/CLI 퀴즈 → 오답노트`

1. **출력 포맷** — JSON 대신 `schemas/frontmatter.md` 규격의 `.md`로 저장.
   메타는 frontmatter, 문제 본문은 마크다운 본문에.
2. **ID·중복을 state로** — 프롬프트에서 세던 일련번호/lookback을 `state.py`로 이관.
   임시 컨테이너에서도 일관됨.
3. **커밋 전 색인** — 커밋 직전 `indexer.py --check && indexer.py`. (CLAUDE.md에 명시)
4. **루틴 얇게** — `prompts/routine_kmle.md`로 교체.
5. **타입 확장** — USMLE/논문/카드는 요일 분산으로 루틴 복제.

퀴즈 UI(`kmle/quiz/quiz.py`, `docs/`)는 마이그레이션이 끝난 뒤 `content/`(또는
SQLite 색인)을 읽도록 연결하면 된다. 그 전까지는 두 체계가 공존한다.

## 임시 컨테이너(루틴) 대응이 왜 중요한가

루틴은 매번 새 컨테이너에서 돈다. 그래서:
- SQLite/일련번호/최근주제는 컨테이너 메모리가 아니라 **repo 파일**에서 읽는다.
  → `state/*.json`은 커밋한다. `db/*.sqlite`는 커밋하지 않고 매번 재빌드한다.
- Google Drive 자격증명을 컨테이너에 넣지 않는다.
  → Drive 백업은 GitHub Action(rclone)으로 분리한다.

## 다음 단계 (2·3단계 예고)

- 2단계: 검색 UI/대시보드, 복습(SRS), 태그 정리
- 3단계: 임베딩 + ChromaDB로 의미 검색(RAG), 가이드라인 비교, 지식 그래프
  → `documents`/`relations` 테이블과 frontmatter의 `related`가 이미 그 씨앗이다.

## 검색해 보기 (FTS5, 무료·내장)

```sql
SELECT d.id, d.type, d.topic, d.subtopic
FROM docs_fts f JOIN documents d ON d.id = f.id
WHERE docs_fts MATCH 'SGLT2 OR 심부전' ORDER BY rank LIMIT 20;
```

## 보안

- API 키·자격증명은 `.env`에 두고 `.gitignore`로 제외(이미 설정됨).
- 의학 콘텐츠는 self-verify에 한계가 있다. 신규 타입(paper/disease/drug)은 PR로 검수.

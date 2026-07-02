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
```

## 저장소 구조

```
.
├── CLAUDE.md                 # 매 세션·매 루틴에 자동 로드되는 규칙 (핵심)
├── .claude/
│   ├── settings.json         # 파이프라인 실행 권한
│   └── skills/               # 타입별 생성 + 색인 스킬 (자동/슬래시 호출)
│       ├── daily-run/        # 하루치 오케스트레이터 (루틴이 호출)
│       └── gen-kmle/  gen-paper/  gen-card/  index-db/
├── schemas/frontmatter.md    # 저장 규격(계약). 모든 .md가 따름
├── pipelines/                # 결정론적 작업(파싱·색인·ID·상태)은 파이썬이 담당
│   ├── frontmatter.py        # frontmatter 파싱·검증
│   ├── indexer.py            # content/ → SQLite(FTS5) 재빌드
│   ├── state.py              # ID 발급 + N일 중복방지 (ephemeral 컨테이너 대응)
│   └── db_schema.sql
├── content/                  # ★ 원본 (kmle/usmle/basic/papers/diseases/drugs)
├── state/                    # id_counter.json, seen_topics.json (커밋됨)
├── prompts/routine_kmle.md   # 얇은 루틴 프롬프트 템플릿
├── db/                       # medkos.sqlite (gitignore, 재빌드됨)
├── .github/workflows/
│   ├── drive-sync.yml        # content/ push 시 rclone로 Drive 백업
│   └── pages.yml             # docs/ 웹 퀴즈를 GitHub Pages로 배포
│
├── kmle/                     # [기존] JSON 기반 KMLE 퀴즈 세트 (현재 Learning 계층)
│   ├── quiz/                 # quiz.py 실행기 + questions/*.json (단일 소스)
│   ├── 문항/  오답노트/       # JSON에서 생성된 읽기용 .md + 오답 기록
└── docs/                     # [기존] GitHub Pages 웹 퀴즈 (클릭으로 풀기)
```

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

# SPEC anatomy-3q-2026 — 2026-2학기 임상해부학술기(3Q) 개인 학습 시스템

```yaml
spec_id: anatomy-3q-2026
status: approved_for_implementation   # 사용자 프롬프트(2026-08-12)가 승인한 구현 요청
implementation_owner: claude
branch: claude/anatomy-3q-2026-okgos4   # claude/<task> 규약; 실행 하네스가 지정한 브랜치
created: 2026-08-12
kind: product_feature (not an ECG experiment — MedKOS 콘텐츠 플랫폼 확장)
```

## 1. 목표

Google Drive의 해부학 강의 PDF(해부1·해부2)와 답만 있는 `tagging 2차.pdf`를
페이지 단위 학습 데이터로 바꾸고, **2026-10-19 Tagging 2 종료일까지** 매일
05:00 KST에 오늘의 학습 세트를 생성하는 루틴·정적 웹 화면을 MedKOS에 추가한다.

## 2. 확정 입력 (2026-08-12 Drive 실측)

| 폴더 | 파일 | file ID | 크기 |
|---|---|---|---|
| 해부1 | 2회차(0818) 김홍태pf.pdf | `1SrTdEEy8ay95nl2Pqoa7NAwRYCGGFLmm` | 38.4MB |
| 해부1 | 3회차(0825) 허미선pf.pdf | `1_2A2hJdNEXEsAxR9jMdnS_fjG5XD2pzG` | 38.1MB |
| 해부1 | 4회차(0828) 허미선pf.pdf | `1n7KICVjUyEI4OYyd1aTZO2GMErC-Ye1T` | 30.1MB |
| 해부1 | 5회차(0829) 김홍태pf.pdf | `1qLFsMNerkM4ZuCSBc7qDryowUF6boVTB` | 42.4MB |
| 해부1 | 6회차(0901) 문용석pf.pdf | `1geCFG3Icgh-_nH6nHvEHacTEeWCiCwLf` | 57.2MB |
| 해부1 | 7회차(0904) 문용석pf.pdf | `11INApFHsemvqLWZi5CCsxDwc7P3YHQwV` | 6.1MB |
| 해부2 | 9차시(0911) 김홍태pf.pdf | `1nuT1hKVN4R3tvK7kqBZEwyfc1iDbfQlp` | 29.9MB |
| 해부2 | 10차시(0918) 허미선pf.pdf | `1HlXe71Yv3uMIhM6_UNWHqmtrw-K0MOBT` | 19.2MB |
| 해부2 | 11차시(0922) 허미선pf.pdf | `1vTTFerg-qAFnYV0ofiolfcj5RDefrwml` | 28.5MB |
| 해부2 | 12차시(0925) 문용석pf.pdf | `1m_zNU7EJ3593L-9R-5sXjoeOnKVJq8G5` | 7.0MB |
| 해부2 | 13차시(0929) 김홍태pf.pdf | `1fqcNIy-Z2BnysPlRCl8F8cSaMl-2SLh3` | 25.9MB |
| 해부2 | 14차시(0930) 문용석pf.pdf | `1w9YssObls08gA35da5nZXiBt9rDXQpV-` | 3.7MB |
| 해부2 | 15차시(1013) 허미선pf.pdf | `1R3MQ_-tL_XMnzmqrJhgugvRFIfWW_EEB` | 19.9MB |
| 해부2 | tagging 2차.pdf (답만 있음) | `1v5m2IeMpb2JwaotIYJa_vILdUg5JRIxP` | 2.6MB |
| 해부2 | 해부 수업계획서.xlsx (과거 학기) | `1mS-P7LNNkZbpBOB_eyJjqKiotpGWZ5gx` | 7.9MB |

- **누락(missing_source)**: 1회차 원본, 8회차/Tagging 1 원본은 어느 폴더에도 없다.
  추측 생성 금지 — inventory가 `missing_source`로 기록만 한다.
- 파일명·수업계획서의 날짜는 **과거 학기** 날짜다. 일정의 단일 기준은 §3의 2026 표다.

## 3. 2026 일정 (단일 기준 — `pipelines/anatomy_schedule.py`에 하드코딩)

사용자가 제공한 2026-2학기 시간표가 유일한 일정 소스다. Drive 계획서와 충돌하면
이 표가 우선한다. 전체 표는 `anatomy_schedule.py` `SCHEDULE_2026` 참조. 핵심:

- Tagging 1: **2026-09-10** / Tagging 2(종료일): **2026-10-19**
- 자동 생성 종료: **2026-10-19 23:59:59 KST**. 10-20부터는 `completed` no-op.
- 단계: `~09-09` T1 준비 → `09-10` rapid review → `09-11~10-12` T2 신규+T1 취약점
  → `10-13~10-18` mock/혼합 → `10-19` final rapid review → 이후 no-op.

## 4. 아키텍처

```text
Drive PDF ──(수동/텍스트 스냅샷)──▶ .private/anatomy/   ← git 무시, 원본·파생 이미지
                                        │
content/anatomy/sources/*.md  ◀── anatomy_inventory.py (listing JSON → source_doc 카드)
content/anatomy/pages/**.md   ◀── anatomy_ingest.py / anatomy_extract.py / anatomy_classify.py
content/anatomy/answers/*.md  ◀── anatomy_answers.py (tagging 2차 답-전용 파싱)
content/anatomy/concepts/**   ◀── LLM(스킬)이 출처 페이지 근거로 생성 (id는 next_id)
content/anatomy/questions/**  ◀── 〃 (answer_separated, source_refs 강제)
content/anatomy/daily/*.md    ◀── anatomy_daily.py (결정론 선택)
docs/anatomy-data.js          ◀── export_anatomy_web.py (publishable만)
docs/anatomy.html/-app.js     ◀── 정적 웹(순수 JS, 기존 디자인 재사용)
```

- `type: anatomy` 공식화. `kind`: `source_doc`·`source_page`·`concept`·`question`·
  `daily_plan`·`answer_list`. frontmatter 계약은 `schemas/frontmatter.md` §anatomy.
- ID는 `state.next_id('anatomy')` (`anatomy-2026-NNNN`)로만 발급.
- 마스킹: 텍스트 레이어 bbox → mask JSON(원본 불변) → quiz render → OCR 재검사.
  전부 `.private/anatomy/` 산출, `publishable: true` 검수분만 `docs/assets/anatomy/`.

## 5. 수용 기준 (acceptance)

1. `indexer.py --check` ERROR 0, 기존 타입 export 회귀 없음.
2. 같은 입력 재실행 시 중복 ID/파일 0 (idempotent).
3. 모든 concept/question에 `source_refs`(file id + page 또는 text-lane 마커) 존재.
4. 2026 일정이 Drive 과거 날짜로 오염되지 않음(테스트 고정).
5. 마스킹 fixture 테스트: label 100% 마스크 내 또는 review 격리, 원본 불변,
   마스크 밖 정답 문자열 잔존 0.
6. `publishable: false` 자산이 `docs/`·git에 나타나지 않음.
7. 10-20 이후 실행은 콘텐츠를 만들지 않고 `completed`를 보고.
8. 웹: 기존 페이지 정상, anatomy 페이지 작동, localStorage 키 충돌 없음
   (`medkos_anatomy_*` 네임스페이스).

## 6. 변경 허용 파일

`schemas/frontmatter.md`, `pipelines/frontmatter.py`, `pipelines/state.py`,
`pipelines/anatomy_*.py`(신규), `pipelines/export_anatomy_web.py`(신규),
`pipelines/test_anatomy*.py`(신규), `content/anatomy/**`(신규),
`docs/anatomy*.{html,js}`(신규), `docs/*.html`(nav 링크 한 줄),
`docs/style.css`(추가만), `.claude/skills/anatomy-daily/**`(신규),
`prompts/routine_anatomy.md`(신규), `.gitignore`(.private 추가),
`docs/ANATOMY_OPERATIONS.md`(신규), 이 spec.
ECG 실험 파일·기존 콘텐츠는 건드리지 않는다.

## 7. Decision log

- **D1 (2026-08-12)**: 루틴 컨테이너에서 Drive PDF **바이너리**를 받을 수 없음을 실측
  (MCP `download_file_content`는 base64를 컨텍스트로 반환 → 수 MB PDF 불가;
  `drive.google.com` 직접 HTTP는 프록시 정책으로 차단, curl exit 56).
  → **이중 레인 설계**: ① binary lane — 사용자가 `.private/anatomy/originals/`에
  넣은(또는 로컬 rclone 동기화한) PDF를 페이지 분해·bbox·마스킹까지 처리(합성
  fixture로 테스트). ② text lane — Drive MCP 텍스트 추출 스냅샷을 정본 텍스트로
  인제스트. text lane은 **페이지 번호가 보존되지 않으므로** `source_page: null` +
  `extraction: drive-mcp-text` + `section` 필드로 정직하게 기록한다(페이지를 지어내지
  않음). 바이너리 확보 시 같은 source의 레코드를 페이지 단위로 승격한다.
- **D2**: Drive 목록 조회도 MCP 전용이므로 `anatomy_inventory.py`는 세션이 저장한
  **listing JSON**을 입력으로 받는 결정론 스크립트로 설계(스크립트 자체는 Drive
  인증 없음). 네트워크 부재 시 기존 manifest를 지우지 않는다.
- **D3**: 강의 원문 전문(全文)은 저작권상 공개 repo에 커밋하지 않는다. 커밋되는
  source_page 카드는 **구조물 용어 목록 + 관계 요약(자체 작성)**만 담고, 원문
  텍스트 스냅샷은 `.private/anatomy/text/`(gitignore)에 둔다.
- **D4**: inventory manifest는 별도 JSON 상태 파일 대신 `content/anatomy/sources/`
  의 `kind: source_doc` 카드로 커밋한다(CLAUDE.md "content가 SoT, 상태는 content
  파생" 원칙 준수; 루틴 간 충돌 원천 제거).
- **D5**: `tagging 2차.pdf`의 번호 항목은 `answer_only_candidate: true`,
  `priority: high`로만 기록. 원 질문·핀 위치를 복원한 척하지 않는다. 새 문항은
  강의 텍스트에서 같은 구조가 확인될 때만 `confidence: medium+`로 공개 덱에 들어가고,
  근거 페이지가 없으면 `confidence: low` + `needs_review: true`로 격리된다.
- **D6**: OCR 엔진(tesseract)은 이 컨테이너에 없다. 마스킹의 OCR fallback과 재검사는
  PDF 텍스트 레이어 기반으로 구현하고, OCR 부재 시 해당 페이지를 자동 공개하지 않고
  review queue로 보낸다(안전 기본값 false).
- **D7**: 예약은 Claude Code Remote의 Routine(trigger)으로 등록한다 —
  cron `0 20 * * *` UTC = 매일 05:00 KST, 새 세션 스폰, `prompts/routine_anatomy.md`
  실행. 종료일 제어는 cron이 아니라 `anatomy_schedule.py`가 한다(10-20부터 no-op).
  자동 커밋은 이 spec의 PR이 main에 병합된 뒤에만 활성화(그 전 실행은 보고만).
- **D8**: 브랜치는 하네스 지정 `claude/anatomy-3q-2026-okgos4`를 사용(프롬프트의
  `claude/anatomy-3q-2026`과 이름이 다른 것은 실행 환경 제약이며 `claude/<task>`
  규약은 동일).

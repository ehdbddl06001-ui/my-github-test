# 해부학(3Q) 운영 문서 — 공개/비공개 자산과 루틴

spec: `experiments/specs/anatomy-3q-2026.md` · 웹: `docs/anatomy.html`
**시각 자료 제작 규격(두 lane·QA·함정): `docs/ANATOMY_VISUALS.md`**

## 1. 공개/비공개 경계 (절대 규칙)

이 repo와 GitHub Pages는 **공개**다. `docs/`에 들어가면 인터넷에 공개된 것으로 간주한다.

| 자산 | 위치 | 공개 여부 |
|---|---|---|
| 원본 강의 PDF | Google Drive + `.private/anatomy/originals/` | ❌ 커밋 금지(gitignore) |
| 페이지 PNG·추출 JSON·마스크·QA 시트 | `.private/anatomy/{pages,extract,masks,render,qa}/` | ❌ |
| 텍스트 스냅샷(MCP 추출 전문) | `.private/anatomy/text/` | ❌ (저작권 — 전문 커밋 금지) |
| 용어 목록·분류·관계 요약·자작 문항 | `content/anatomy/**` | ✅ (자체 작성 파생물만) |
| 웹 번들 | `docs/anatomy-data.js` | ✅ (needs_review 제외, file ID·URL 미포함) |
| 검수 완료 문제 이미지 | `docs/assets/anatomy/` | ✅ **사람이 `publishable: true`로 승인한 것만** |

- 자동화는 `publishable`을 **절대 true로 만들지 않는다**(안전 기본값 false).
- 카데바 사진에 식별 표식·명찰·얼굴·메타데이터가 있으면 공개하지 않는다.
- 정적 페이지의 자바스크립트 비밀번호는 보안이 아니다 — 올리면 공개다.
- 원본 이미지는 절대 덮어쓰지 않는다: 원본 / mask JSON / quiz render 3분리.

## 2. 이미지 마스킹 흐름 (binary lane — 로컬에서)

루틴 컨테이너는 Drive 바이너리를 받을 수 없다(spec D1). PDF 처리 원하면 사용자가:

```bash
# 1) 로컬 PC에서 Drive 파일을 .private/anatomy/originals/<source-id>.pdf 로 복사
#    (source-id는 content/anatomy/sources/의 카드 파일명: a1-s02 … a2-s15, a2-tagging2)
python pipelines/anatomy_ingest.py                     # 해시 비교 → 페이지 분해
python pipelines/anatomy_extract.py --source-id a2-s14 # 텍스트 블록+bbox
python pipelines/anatomy_classify.py --source-id a2-s14 # 페이지 카드(페이지 번호 승격)
python pipelines/anatomy_mask.py --source-id a2-s14 --contact-sheet
# 2) .private/anatomy/qa/의 contact sheet(전/후/경계)를 눈으로 검수
# 3) 공개하고 싶은 render만 docs/assets/anatomy/로 복사하고, 해당 question 카드에
#    publishable: true + web_asset: assets/anatomy/<파일> 을 직접 기록
```

- 텍스트 레이어가 없는 페이지(OCR 엔진 부재)는 자동으로 review queue
  (`.private/anatomy/review/`)로 가고 공개되지 않는다.
- `anatomy_mask.py`는 마스크 밖에 정답 문자열이 남으면 `leak`으로 표시하고
  종료 코드 1을 낸다 — leak 상태는 절대 공개 금지.
- **자연 패치(기본, 2026-08-12~)**: 가림은 중립색 박스 대신 주변 배경색을
  샘플링(중앙값)한 불투명 패치 + 결정론 번호핀(위→아래·왼→오른 순 1..N)으로
  렌더된다(`--style box`로 과거 방식 선택 가능). 채움은 항상 완전 불투명이라
  정답이 비칠 수 없고, leak 검증은 종전과 동일하게 텍스트 레이어로 수행한다.
- **재작화(redraw) lane**: 가린 면적이 페이지의 8%를 넘거나 라벨이 12개를
  넘으면 mask JSON에 `redraw_recommended: true`가 붙는다(패치로도 어색함이
  남는 경우). 이때는 원본 이미지를 게시하지 말고 **클로드가 원본을 보고 자체
  제작 SVG로 재작화**한다 — `asset_origin: claude-drawn-svg`, 원본 페이지를
  `source_refs`에 남기고, 스킬 4b 렌더 QA 루프를 반드시 통과시킨다. 사람이
  contact sheet 검수에서 "어색하다"고 판단한 페이지도 같은 lane으로 보낸다.

## 2b. 그림 자료 — 가능/불가능 실측표 (2026-08-12)

| 경로 | 가능? | 근거·조건 |
|---|---|---|
| Drive MCP로 PDF **이미지** 추출 | ❌ | MCP는 텍스트 표현만 반환. 바이너리(base64)는 수 MB에서 불가(spec D1) |
| 인터넷에서 해부도 다운로드 | ❌ | 프록시가 외부 이미지 호스트 차단(Wikimedia도 차단 실측). 가능하더라도 Netter·e-Anatomy 등은 저작권상 공개 repo 게시 불가 |
| **PDF를 세션에 직접 업로드** | ✅ | 업로드 파일은 컨테이너 디스크에 저장됨 → binary lane(페이지 분해→bbox→마스킹→leak 검증) 전체 작동. 단 강의 슬라이드 파생 이미지의 **공개(publishable) 여부는 사람이 결정**(저작권·카데바 민감성) — 기본은 비공개 |
| 로컬 PC에서 binary lane 실행 | ✅ | §2 절차. 결과물 검수 후 선별 공개 |
| **클로드 자체 제작 SVG 모식도** | ✅ 기본 경로 | 저작권 문제 없음 → 공개 가능. 2026-08-12 리메이크: 교과서 표준 구도(반골반 안쪽면·위에서 본 골반바닥)를 따라 뼈 실루엣 위에 구조를 배치하고 **전 라벨 한·영 병기**. 강의에서 확인된 관계만 담는다(특정 교과서 도판의 복제는 저작권상 불가 — 구도만 참고). `asset_origin: claude-drawn-svg`로 표기, 라벨판(개념용)과 번호핀 퀴즈판(spotter용)을 분리 제작 |

해부1 실측 특성(2026-08-12 인제스트): 김홍태·허미선 회차(2·3·5회차)는 **필기 스캔**이라
텍스트 추출이 단편적(needs_review 격리됨) — 이 회차들은 이미지가 본체이므로 학습 자료로
쓰려면 **PDF 업로드 또는 로컬 binary lane**이 필요하다. 문용석 회차(7·14차시)는 타이핑
텍스트가 풍부해 text lane으로 충분하다. 6회차(57MB)는 MCP 추출이 빈 응답 — binary lane 전용.

## 3. 일일 루틴

- 예약: **매일 05:00 Asia/Seoul (= 20:00 UTC), 2026-08-13 ~ 2026-10-19**,
  새 세션에서 `prompts/routine_anatomy.md` 실행(Claude Code Routine).
- 종료 제어: 10-20부터 `anatomy_daily.py`가 `completed` no-op — 콘텐츠 생성·커밋 금지.
  10-19가 지나면 루틴을 삭제한다(claude.ai/code의 Routines 화면 또는 세션에서
  "해부학 루틴 삭제해줘").
- 수동 dry-run:
  ```bash
  python pipelines/anatomy_daily.py --date 2026-08-13 --plan   # 쓰기 없음
  python pipelines/anatomy_inventory.py --listing state/.anatomy_listing.json --dry-run
  python pipelines/test_anatomy.py
  ```
- GitHub Actions fallback(선택지, 기본 비활성): 텍스트 카드 재검증·번들 재생성만
  가능하고 Drive 접근·LLM 생성은 불가. 원하면 별도 워크플로를 요청할 것 —
  **secret(RCLONE 등) 생성·변경은 사용자 명시 승인 없이 하지 않는다.**

## 4. 데이터 흐름 요약

```
Drive(원본) ─MCP listing→ state/.anatomy_listing.json ─inventory→ content/anatomy/sources/
Drive(텍스트) ─MCP read→ .private/anatomy/text/ ─ingest/classify→ content/anatomy/pages/
tagging 2차 ─answers→ content/anatomy/answers/ (번호=답 후보, 원 질문 복원 금지)
강의 근거 + 답 후보 ─LLM(/anatomy-daily)→ concepts/·questions/ (source_refs 강제)
anatomy_daily.py ─결정론→ daily/ ─export→ docs/anatomy-data.js ─Pages→ 웹
```

## 5. 사용자가 해야 할 일

1. 이 PR 병합 → GitHub Pages에 `anatomy.html` 배포됨(main의 pages.yml이 처리).
2. 루틴은 이미 등록됨(§3) — PR 병합 전 실행분은 "보고만" 하고 커밋하지 않는다.
3. (선택) 이미지 spotter를 원하면 §2 binary lane을 로컬에서 1회 실행.
4. (선택) 해부1 텍스트도 학습에 넣으려면 세션에 "해부1 PDF들 텍스트 인제스트해줘"
   라고 요청 — MCP 추출 → 스냅샷 → 카드 생성까지 자동.
5. Tagging 1 원본(8회차)·1회차 자료가 Drive에 올라오면 inventory가 자동 반영한다.

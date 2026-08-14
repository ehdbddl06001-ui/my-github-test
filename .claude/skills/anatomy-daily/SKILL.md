---
name: anatomy-daily
description: 2026-2학기 임상해부학술기(3Q) 일일 학습 세트를 생성·검증·커밋하는 오케스트레이터. 매일 05:00 KST 루틴이 호출한다. "오늘 해부학", "해부 데일리", "anatomy daily", "태깅 대비 오늘 세트" 요청에 트리거. 2026-10-19 이후에는 completed no-op만 보고한다.
---

# 해부학 일일 실행 절차

spec: `experiments/specs/anatomy-3q-2026.md`. 아래 순서를 **반드시** 지킨다.

## 0. 중단 조건 — **이 둘만** 생성을 막는다

1. `TZ=Asia/Seoul date +%F` 로 KST 오늘 확인. **2026-10-19 이후면**:
   `python pipelines/anatomy_daily.py` 가 `completed`를 출력한다 → 그대로 보고 후
   종료(생성·커밋 금지). 이 경우 사용자에게 루틴 삭제를 안내한다.
2. `pipelines/anatomy_daily.py` 를 끝내 못 구하는 경우(아래 0b 복구까지 실패) —
   상태만 보고한다.

**그 외 어떤 실패도 생성을 건너뛰는 사유가 아니다.** 특히 Drive 미접근(2단계)은
증분 확인이 안 될 뿐이고, 3·4단계(큐 계산·카드/문항 생성)는 repo 콘텐츠만으로
완결된다 — 반드시 진행한다.

## 0b. 저장소 없음 복구 (루틴 컨테이너 필수 점검 — 2026-08-14 실측)

루틴이 만드는 컨테이너에는 **저장소가 안 붙어 있을 수 있다**(트리거 설정에
git source가 없으면 작업 디렉터리가 빈 채로 뜬다). 이때 "환경 문제"로 보고하고
끝내지 말고 **직접 클론해서 진행한다** — 토큰(`GITHUB_TOKEN`)과 프록시는 주입돼
있어 클론이 된다:

```
ls CLAUDE.md 2>/dev/null || {
  cd ~ && git clone https://github.com/ehdbddl06001-ui/my-github-test && \
  cd my-github-test
}
```

클론까지 실패하면 그때 실패로 보고한다(사유·명령 출력 포함).

## 1. 동기화·상태

```
git fetch origin main && git merge origin/main   # 커밋 전 충돌 예방(CLAUDE.md 1단계)
python pipelines/anatomy_schedule.py             # phase·D-day 확인
```

## 2. Drive 증분 확인 (MCP)

- Google Drive MCP `search_files`로 해부1(`1rX4UqwqNFu0ouitHRMe6LR1vsfL7fBbN`)·
  해부2(`1W2n8WcClRMRufMcooPPgnToyItMTBGOF`) 폴더를 조회해
  `state/.anatomy_listing.json`(gitignore) 갱신 →
  `python pipelines/anatomy_inventory.py --listing state/.anatomy_listing.json`
- **새 파일/변경 파일만** 처리한다(source_doc 카드의 status가 `listed`/`stale`인 것).
  텍스트는 MCP `read_file_content`로 스냅샷을 떠서
  `.private/anatomy/text/<source-id>.txt`에 저장 후:
  ```
  python pipelines/anatomy_ingest.py --text-snapshot <파일> --source-id <sid>
  python pipelines/anatomy_classify.py --source-id <sid>
  ```
  (바이너리 PDF는 이 컨테이너에서 못 받는다 — spec D1. 페이지 번호를 지어내지 말 것.)
- **Drive는 선택 단계다.** MCP 도구가 없거나(루틴 컨테이너에는 보통 없다) 접근이
  실패하면 기존 자료를 지우지 말고 **이 단계만 건너뛴 뒤 3단계로 계속 진행**한다.
  보고에 "Drive 미접근 — 증분 확인 생략"을 한 줄 남기면 된다. 여기서 실행을
  끝내면 안 된다.

## 3. 오늘 큐 계산 (결정론) + 밀린 날 따라잡기

```
python pipelines/anatomy_daily.py --date <KST 오늘> --backlog   # 밀린 날 확인
python pipelines/anatomy_daily.py --date <KST 오늘> --plan
```

- **backlog가 비어 있지 않으면**(주간 이용 한도 초과 등으로 루틴이 못 돈 날):
  `python pipelines/anatomy_daily.py --date <KST 오늘> --catch-up 3` 으로
  **오래된 날부터 최대 3일치**를 먼저 따라잡는다(계획 카드에 `made_up: true`
  자동 표기). 3일을 넘게 밀렸으면 다음 실행이 이어서 따라잡는다 — 한 번에 다
  만들려고 이용량을 태우지 않는다. 따라잡은 날짜와 남은 backlog를 보고에 포함.
- 따라잡기 계획에서 나온 `gaps`도 오늘 것과 합쳐 4단계에서 생성하되, 생성
  총량이 과하면(문항 20개+) 오늘 것 우선, 나머지는 다음 실행으로 미룬다.

`gaps`가 비어 있지 않으면 그 슬롯만큼 카드/문항을 **생성**한다(4단계).

## 4. 카드·문항 생성 규칙 (LLM 파트)

- id는 반드시 `python -c "from pipelines.state import next_id; print(next_id('anatomy'))"`.
- **출처 강제**: 모든 concept/question의 `source_refs`에 실제 source_file_id +
  (page 또는 text-lane section). 근거 페이지를 못 찾으면 `confidence: low` +
  `needs_review: true`(공개 덱 자동 제외).
- `tagging 2차.pdf`의 번호 항목(`answer_only_candidate: true`)은 고우선 출제
  근거지만, **원 질문을 아는 척 금지** — 강의 자료에서 같은 구조가 확인될 때만
  문항화한다.
- 문항 스타일 균형: spotter/layer-order/branch-tree/course-tracing/relation/
  distinction/clinical-application 을 섞는다. 객관식 보기는 같은 부위·같은
  구조 종류로 동질 구성. `answer_separated: true` 필수.
- 분지·주행 개념 카드에는 `tree:` frontmatter(웹이 트리로 렌더)를 넣는다.
- 과거 학기 날짜(파일명·수업계획서)를 2026 일정으로 쓰지 않는다 —
  일정은 `anatomy_schedule.py`가 유일 기준.

## 4a. 시각 자료 필수 (사용자 요구 — 2026-08-14)

> 제작 규격·작화 규칙·실측 함정은 **`docs/ANATOMY_VISUALS.md`** 에 있다. 새 회차
> 시각 자료를 만들기 전에 그 문서를 먼저 읽는다(두 lane을 섞지 않기 위해).

**텍스트만 있는 학습자료는 미완성으로 본다.** 회차 종합정리(`study_guide`)와 개념
카드는 아래 3종 시각 자료를 반드시 동반한다(해당 회차 범위에 존재하는 것만):

1. **근육층 도해** — 얕은층→깊은층 순서, 각 층의 지배신경 규칙을 색으로 구분
   (예: 등은 얕은·중간층=척수신경 앞가지, 깊은층=뒤가지).
2. **신경 도해** — 분지·주행·지배 근육. 감각/운동 구분 표시.
3. **혈관 분지 도해** — 모동맥 → 가지 트리. 문합(anastomosis)은 닫힌 고리로 그린다.

추가로 각 도해는 **라벨판 + 퀴즈판 쌍**으로 만든다:
- `*-labeled.svg` — 전 구조 한·영 병기 라벨.
- `*-quiz.svg` — 라벨을 지우고 **번호핀만** 남긴 마스킹판. 대응 문항 카드의 정답
  순서와 번호가 1:1(임의 변경 금지). 이게 태깅 연습의 본체다.

자체 제작 SVG는 `docs/assets/anatomy/`, `asset_origin: claude-drawn-svg`,
`publishable: true` 가능(카데바 사진과 달리 저작권·존엄 문제 없음). 반드시 4b의
QA 루프를 거친다.

**회차 서브노트가 학습자료의 기본 형태다 — 도해와 표를 한 파일에 합친다.**
frontmatter `layout: split` 으로 **A4 가로 2단**: 섹션마다 왼쪽에 도해(`!fig`),
오른쪽에 근육표·혈관표·신경표·공간표 + 콜아웃(기출/교수강조/주의/임상/TIP/암기),
마지막에 자가 점검 질문. 도해를 따로 보내지 말고 **이 한 파일로** 전달한다.

```
python pipelines/anatomy_subnote.py --card content/anatomy/notes/<카드>.md \
    --output .private/anatomy/pdf/subnote-sNN.pdf
```

문법·조판 함정은 `docs/ANATOMY_VISUALS.md` §6. 텍스트 카드 자체는 Drive Docs
업로드도 가능하다(도해는 PDF 안에만 들어간다).

## 4b. SVG 도해 자체 QA 루프 (필수 — 모델 불문)

`docs/assets/anatomy/*.svg`를 새로 만들거나 수정했으면 **커밋 전에 반드시**
렌더링해서 눈으로 검사하고, 어색한 부분을 고친 뒤 재렌더한다(최소 1회 왕복):

```
/opt/pw-browsers/chromium --headless --disable-gpu --no-sandbox \
  --screenshot=/tmp/qa.png --window-size=880,660 --hide-scrollbars \
  file://$PWD/docs/assets/anatomy/<파일>.svg
```

체크리스트: ① 라벨-선 겹침(후광 `<style>text{paint-order:stroke;...}</style>` 유지)
② 텍스트가 상자·캔버스 밖으로 넘침 ③ 번호핀 숫자 가독(원문자 글리프 ①② 금지 —
원 도형 + 일반 숫자) ④ 해부학적 위치관계가 카드 본문 설명과 모순 없는지
⑤ 좌우대칭 도해는 미러(`<use>`) 깨짐. 스크린샷 확인 없이 SVG를 커밋하지 않는다.
퀴즈판 번호 배정은 대응 문항 카드의 정답 순서와 1:1 — 임의 변경 금지.

**마스킹 어색함 자동 복구(재작화 lane)**: binary lane 마스킹은 기본이 자연
패치(주변색 메움+번호핀)지만, `anatomy_mask.py`가 `redraw_recommended`를
보고하거나 contact sheet에서 가림 자국이 어색하면 그 페이지는 원본 게시 대신
**원본을 보고 자체 제작 SVG로 재작화**해 문항·자료를 만든다(위 QA 루프 적용,
`asset_origin: claude-drawn-svg`, 원본 페이지를 `source_refs`로). 원본 래스터를
직접 수정("그림 위에 덧그리기")하지 않는다 — 원본 불변 원칙(spec §8-1).

## 4c. 실사 복원 lane (업로드 필기 스캔 → spotter 문항)

사용자가 필기 스캔 PDF를 올렸을 때의 흐름 (`pipelines/restore_scan.py`):
페이지 선정 → 필기 색 검출 + 검정 손글씨 bbox 지정(시각 판단) → 복원
→ quiz판(정답 라벨 inpaint + **좌상단 타이틀 존은 무조건 검은 박스** + 번호핀)
→ 4b QA 루프 → 문항 카드(`publishable: false` 고정 — 카데바·영상 캡처 파생물).

- **복원은 donor 우선(블라인드 방지 — 2026-08-12 실측)**: 확산 인페인팅만 쓰면
  지운 자리가 주변보다 뭉개져 보인다. 같은 영상의 **인접 페이지(앞뒤 1~3장)를
  함께 렌더해 같은 카메라 구도의 깨끗한 프레임을 찾아 `"donor"`로 지정**하면
  ECC 정렬 + 광도 매칭으로 진짜 조직 질감이 복사된다(고정 카메라라 대부분
  성립). donor 자신의 필기·자막·손 위치 차이는 자동 제외되지만, 검정/흰색
  마킹은 색 검출이 안 되므로 QA 루프에서 `donor_bad_boxes`로 정리한다.
  donor가 없을 때만 인페인팅+질감 매칭 폴백.

- **페이지 선정 기준(3Q 개요 실측)**: 땡시는 1차 30문항(카데바 5구)·2차
  36문항(카데바 5구+장기 테이블), 카데바당 좌우 3개씩 **큼직하고 중요한
  구조물** 위주 출제. 옵세한 구조물·이름 없는 정맥은 패싱, **위치·생김새가
  아니라 해부학적 관계**를 물을 수 있는 그림만 고른다. `tagging 2차.pdf`
  번호 항목과 겹치는 구조물 최우선.
- **예습시험 모드(수업일 연동 — 최우선)**: 예습시험은 **수업당 10문제**,
  그날 배울 **회차 범위에서만** 출제된다. 회차 매핑: 업로드 스캔 파일명의
  "N회차" = `SCHEDULE_2026`의 N번째 항목 = source card `session_no`
  (사용자 엑셀 시간표 반영본 — 어긋나면 사용자에게 확인).
  `anatomy_daily.py --plan`의 **`preview_exams` 필드가 결정론 신호**다:
  - `prepare`(D-2): 그 회차 범위 문항 생성 시작(스캔 있으면 실사 포함)
  - `finalize`(D-1): **이 실행이 마감** — 수업 **전날 아침 루틴 종료 시점까지**
    15~20문항(시험의 1.5~2배) 세트를 완성해 daily plan에 포함. 부족분은
    이 실행에서 반드시 채운다. 루틴은 주말 포함 매일 05:00에 돌므로
    **월요일 수업의 마감은 일요일 아침 실행**이다.
  - `class-day`(D-0): 신규 생성 없이 완성된 세트 복습 안내만.
  구성: 실사 spotter 6~8개(그 회차 스캔 페이지, donor 복원) + 나머지는
  텍스트 관계형(인제스트된 pages 카드 근거, 토큰 저렴). 기존 문항 재사용
  우선, 부족분만 신규 생성.
- **스캔 공급 규칙**: 루틴 컨테이너는 Drive에서 PDF 바이너리를 못 받으므로
  실사 문항은 **사용자가 대화 세션에 올린 스캔**에서만 나온다. 해당 회차
  스캔이 **수업 D-2까지** 업로드·처리돼 있지 않으면 finalize는 텍스트
  문항만으로 세트를 완성하고, 보고에 "회차 N 스캔 미공급 — 실사 제외"를
  명시한다(추측으로 이미지를 만들지 않는다).
- **평시 페이스**: 수업 없는 날은 실사 문항 **하루 2개**(쉬움 1 + 어려움 1),
  땡시 D-14부터 하루 4개로 램프업. 근거: 해부는 2학점(개요: "해부에 힘 빼지
  말 것"), 땡시 총 66문항. 20개 파일을 전부 처리하지 말고 태깅·예습시험
  후보만 선별한다. 밀리면 3단계 catch-up이 흡수.
- **회차 산출물은 서브노트 한 파일로 합친다(기본)**: 도해 + 표 + **실사 태깅 문항·정답**까지
  하나의 PDF. 카드 frontmatter에 `layout: split` 과 `scan_questions: [{card, quiz_image,
  clean_image}]` 를 넣고:
  ```
  python pipelines/anatomy_subnote.py --card content/anatomy/notes/<카드>.md \
      --output .private/anatomy/pdf/subnote-sNN.pdf
  ```
  실사 이미지를 합본하므로 그 카드는 `publishable: false`, 출력은 `.private/` 아래.
  (문제만 빠르게 풀 용도의 `anatomy_pdf.py --manifest` 문제집은 보조 산출물.)
  페이지 밀도는 frontmatter로 조절한다 — `quiz_per_page`(기본 2, 가로 페이지에 두 문항)
  · `answers_per_page`(기본 3, 정답부 썸네일). 회차당 문항이 12~15개로 늘었으므로
  **한 페이지 한 문항으로 돌리지 말 것**(아래 절반이 빈다).

- **매일 전달 — 이것이 일일 루틴의 마무리 단계다**:
  1. 오늘 갱신된 회차의 서브노트 PDF를 만든다(위 명령).
  2. **`SendUserFile` 로 사용자에게 보낸다.** 루틴 세션도 이 도구를 쓸 수 있다.
     사용자가 받은 파일을 Drive 폴더에 저장한다(한 번의 동작).
  3. Google Drive MCP를 **쓸 수 있으면** 텍스트 동반본(서브노트 카드 본문)을
     `MedKOS-해부-복원자료`(id `1W2AYQSr-zzKseja7ppukc1uLMh6CgOGl`)에 Docs로 올린다.
     MCP가 없으면 이 단계만 건너뛰고 보고에 한 줄 남긴다(실행을 멈추지 않는다).
  - **PDF·이미지를 MCP로 직접 업로드하지 않는다**: `base64Content` 로 기능은 되지만
    파일을 읽어 다시 출력해야 해 **파일 크기의 약 2배**가 토큰으로 나간다
    (1.2MB 서브노트 ≈ 90만 토큰 규모, 2026-08-14 실측). 매일 돌릴 수 없는 비용이라
    기본값은 "올리지 않는다" 이고, 사용자가 명시적으로 요청할 때만 예외다.

### 답안 표기 규정 (확정본 학습평가 시트 — 문항 answer 필드에 적용)

`pipelines/anatomy_schedule.py::ANSWER_RULES` 참조. 요약: 공인 한글용어 또는
원어 중 하나(인정 교재 5종), 근육은 **~근 / ~ muscle(또는 m.)**, 허용 약자
a. v. n. m. lig. sup. inf. ant. post. med. lat.(마침표 필수). 문항 카드의
`answer`는 "한글용어 (원어)" 병기 형식을 유지하면 자동으로 이 규정을 만족한다.

### 회차 상세(확정본) 활용

`SESSION_DETAILS[회차]`에 담당교수·실습지침 페이지·**e-Anatomy 영상 구간**·
응용과제가 있다(2026-08-12 확정본 실측). 업로드 스캔의 회차 매핑이 애매하면
스캔 속 영상 제목·구간을 이 표와 대조해 결정한다. 응용과제는 study_guide의
임상 포인트·관계형 문항 소재로 우선 사용한다.

## 4d. 학습자료 PDF (다운로드 산출물)

회차 단위로 [표지 → 학습 개요 → 문제(퀴즈판) → 정답·해설(복원판)] PDF를
`pipelines/anatomy_pdf.py`로 만든다(레이아웃·조판은 전부 결정론, LLM은
manifest의 개요 본문과 문항 목록만 작성).

```
python pipelines/anatomy_pdf.py --manifest .private/anatomy/pdf/sNN_manifest.json
```

- **출력·manifest 모두 `.private/anatomy/pdf/` 아래에만** 둔다. 카데바·
  e-Anatomy 파생 이미지가 들어가므로 **PDF는 절대 repo 커밋·웹 게시 금지**
  (스크립트가 `.private` 밖 출력을 거부한다). Drive MCP 업로드도 금지
  (base64 토큰 폭탄) — **채팅 파일 전송으로 전달**하고 사용자가 Drive
  `MedKOS-해부-복원자료`에 보관.
- manifest의 `questions[*].card`는 기존 문항 카드(.md)를 가리키고 stem/
  answer/explanation은 frontmatter에서 읽는다 — PDF 본문을 따로 쓰지 않는다
  (Source of Truth 유지). `quiz_image`/`clean_image`는 `.private` 렌더 산출물.
- **개요(overview) 본문에는 정답 노출 주의가 없다**(문제 섹션과 분리된
  학습자료이므로 구조·신경지배·임상 포인트를 정상 서술). 단, 문제 페이지
  stem에는 정답 단서를 넣지 않는 기존 규칙 유지.
- 생성 시점: 예습시험 `finalize`(D-1) 실행에서 그 회차 세트가 완성되면
  함께 생성해 전달. 평시에는 사용자가 요청할 때 또는 회차 문항이 4개 이상
  쌓였을 때 갱신.
- 렌더 QA: 생성 후 표지·개요·문제 1·정답 마지막 페이지를 72dpi로 렌더해
  눈으로 확인(4b와 동일한 원칙 — 텍스트 잘림·이미지 고아 블록 없어야 함).

## 4e. 종합 학습 정리 (study_guide — 사용자 1순위 산출물)

사용자 요구(2026-08-12): 문항보다 **회차 범위 전체의 해부학적 내용 정리**가
우선이다. 회차마다 `kind: study_guide` 카드(`content/anatomy/notes/`)를 만든다.

- **내용 구성**: 범위 전체의 ① 근육표(이는곳·닿는곳·신경·작용, 한·영 병기)
  ② 혈관·신경 분지/주행 ③ 관계도(코드블록 ASCII 트리) ④ 임상·태깅 포인트
  (SESSION_DETAILS 응용과제 반영) ⑤ 예습시험 체크리스트 10개.
- **전달 3경로(자동)**:
  1. repo 커밋(Source of Truth, `publishable: true` 가능 — 텍스트 지식 정리는
     카데바 파생물이 아님),
  2. `anatomy_pdf.py --study <카드> --output .private/anatomy/pdf/...` 로 PDF
     조판(마크다운→표·트리 렌더) 후 채팅 전송,
  3. **Drive 업로드**: 카드 본문을 `text/markdown`으로 `MedKOS-해부-복원자료`
     폴더에 create_file → Google Docs 자동 변환(표·제목 유지). 이미지가 없는
     텍스트라 토큰 부담 없음. 429(quota) 나면 다음 실행에서 재시도.
- **범위 표기는 `–`(en dash)** — `C7–T12`, `0:00–11:08`. `~`는 Docs 변환에서
  **취소선으로 오해석**되므로 study_guide 카드·Drive 업로드 본문에 금지
  (2026-08-12 실측: "C7~T3 … 2~5" 구간이 취소선으로 렌더됨).
- **생성 시점**: 예습시험 `prepare`(D-2)에 초안, `finalize`(D-1)에 완성판.
  실사 문항 세트와 같은 마감(수업 전날 아침)을 공유한다.
- 문항 lane(4c)은 계속 돌리되, 이 study_guide가 회차 산출물의 1순위다.

## 5. 계획 확정 + 검증

```
python pipelines/anatomy_daily.py --date <KST 오늘>    # daily_plan 카드 작성
python pipelines/indexer.py --check                     # ERROR 0 필수
python pipelines/test_anatomy.py                        # 10개 회귀 테스트
```

실패하면 커밋하지 말고 원인을 보고한다.

## 6. 번들 재생성 + 커밋

```
python pipelines/indexer.py
python pipelines/export_anatomy_web.py
python pipelines/export_search_web.py
```

- 새 `.md` + `docs/anatomy-data.js` + `docs/search-index.js`를 **같은 커밋**에.
- **공개 이미지가 포함되거나 review 항목이 새로 생겼으면 자동 커밋 금지** — PR로.
- 안정 흐름(텍스트 카드·문항·daily plan)은 main 직접 커밋 허용(KMLE와 동일 취급 —
  병합 안 되면 홈페이지 '오늘의 학습'에 안 뜬다). 단 **아키텍처 PR 병합 전에는
  전부 보고만**.

## 7. 보고 형식

- 오늘 phase · 다음 수업/시험까지 D-day
- 생성한 카드/문항 수와 id, 사용한 출처(파일명·섹션)
- needs_review 대기 항목과 이유
- Drive 신규/변경/누락(missing_source) 현황

### 조용한 무작업 종료 금지 (필수)

한 번의 실행은 **둘 중 하나로 끝나야 한다**:

1. **산출물** — 커밋(또는 PR) + 그 안에 최소 오늘자 daily plan 카드. 또는
2. **명시적 사유** — 왜 아무것도 안 만들었는지 보고 첫 줄에 한 문장으로.
   0단계의 두 중단 조건(종료일 경과 / 파이프라인 확보 실패) 외의 사유라면
   그건 버그다 — 사유와 함께 실패한 명령·출력을 남긴다.

"확인했지만 만들 게 없었다"는 사유가 될 수 없다. `anatomy_daily.py` 의 `gaps`가
비어 있으면 daily plan 카드만이라도 커밋해 그날 루틴이 돌았다는 흔적을 남긴다.

---
name: anatomy-daily
description: 2026-2학기 임상해부학술기(3Q) 일일 학습 세트를 생성·검증·커밋하는 오케스트레이터. 매일 05:00 KST 루틴이 호출한다. "오늘 해부학", "해부 데일리", "anatomy daily", "태깅 대비 오늘 세트" 요청에 트리거. 2026-10-19 이후에는 completed no-op만 보고한다.
---

# 해부학 일일 실행 절차

spec: `experiments/specs/anatomy-3q-2026.md`. 아래 순서를 **반드시** 지킨다.

## 0. 활성 조건 (하나라도 실패하면 보고만 하고 종료)

- `TZ=Asia/Seoul date +%F` 로 KST 오늘 확인. **2026-10-19 이후면**:
  `python pipelines/anatomy_daily.py` 가 `completed`를 출력한다 → 그대로 보고 후
  종료(생성·커밋 금지). 이 경우 사용자에게 루틴 삭제를 안내한다.
- main에 `pipelines/anatomy_daily.py`가 없으면(아키텍처 PR 미병합) 자동 커밋을
  하지 않고 상태만 보고한다.

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
- Drive 접근 실패 시: 기존 자료를 지우지 말고 "Drive 미접근"으로 보고만.

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
  "N회차" = source card `session_no` = `anatomy_schedule.py`의 수업 날짜
  (사용자 엑셀 시간표 반영본 — 어긋나면 사용자에게 확인). **수업 D-1과 당일
  루틴은 해당 회차 범위에서 15~20문항**(시험의 1.5~2배)을 최우선으로 준비:
  실사 spotter 6~8개(그 회차 스캔 페이지에서) + 나머지는 텍스트 관계형
  (이미 인제스트된 pages 카드 근거, 토큰 저렴). 기존 문항 재사용 우선,
  부족분만 신규 생성.
- **평시 페이스**: 수업 없는 날은 실사 문항 **하루 2개**(쉬움 1 + 어려움 1),
  땡시 D-14부터 하루 4개로 램프업. 근거: 해부는 2학점(개요: "해부에 힘 빼지
  말 것"), 땡시 총 66문항. 20개 파일을 전부 처리하지 말고 태깅·예습시험
  후보만 선별한다. 밀리면 3단계 catch-up이 흡수.
- **Drive 저장**: 문항 텍스트 카드는 Drive 폴더 `MedKOS-해부-복원자료`
  (id `1W2AYQSr-zzKseja7ppukc1uLMh6CgOGl`)에 Google Docs로 업로드.
  **이미지는 MCP로 업로드하지 않는다** — base64가 이미지당 10만+ 토큰을
  태우는 것을 실측(2026-08-12). 이미지는 채팅 파일 전송으로 전달하고
  사용자가 보관/Drive 저장.

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

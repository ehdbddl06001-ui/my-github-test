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

## 3. 오늘 큐 계산 (결정론)

```
python pipelines/anatomy_daily.py --date <KST 오늘> --plan
```

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

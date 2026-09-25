# 해부학(3Q) 작업 규칙 — CLAUDE.md 에서 옮김(2026-09-25, 내용 그대로)

해부학 루틴(/anatomy-daily, ~2026-10-19)이나 해부 콘텐츠를 만질 때 먼저 읽는다.

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
  · **실사 블랭크(쪽지시험 형태)가 최우선 lane.** 스캔 페이지 → 라벨 가림 + 번호핀은
    `pipelines/scan_triage.py` 가 한다(`--dir uploads-sNN --build`). 규칙: ①어두운 배경의
    흰 손글씨·②표본 위 인쇄 캡션·③좌상단 타이틀·④자막 띠(영상별로 재서 정함)를 **전부**
    가리고, **지운 라벨은 전부 문항으로 삼는다**(2026-08-30 사용자 지시 — 표본 위에
    얹힌 캡션·필기는 지시선이 없어도 그 자리를 묻는다. 복원되므로 구조가 남는다).
    **검은 여백 위 자막·타이틀만 예외** — 지우면 가리킬 구조가 없어 문항이 안 된다.
    만든 뒤 같은 검출기로 되훑어 글자가 남으면 그 박스를 더 가리고 다시 만든다.
  · **카데바 위 글자는 검게 덮지 말고 복원한다**(2026-08-19 사용자 지적). 표본 위에
    검은 박스를 얹으면 물어볼 구조까지 사라진다 → `split_by_bg` 가 가림 박스를 밑바탕
    기준으로 쪼개, **표본 위 조각은 `label_boxes`(donor 앞뒤 프레임 → 점진 인페인팅 →
    질감 매칭)**, **검은 여백 위 조각만 `black_boxes`**. 자막 띠는 화면 UI 라 늘 검은 박스.
    핀이 가리는 자리가 검은 박스면 그 페이지는 버리고, 복원되는 자리면 통과시킨다.
  · **자동만으로는 안 끝난다 — `--sheet` 대지를 사람이 보고 `--reject` 로 뺀다.**
    표본 결에 섞인 흐린 캡션·손글씨는 검출기가 놓친다(실측: F027 '귀밑샘관', F038
    '가쪽코동맥'). 뺀 페이지는 `content/anatomy/restore/<dir>/_rejected.json` 에 이유와
    함께 남아 다음 실행이 같은 것을 다시 만들지 않는다(회귀: `test_scan_blanks_hide_every_label`).
    캡션이 구조 **위에** 얹힌 영상(7회차)은 답을 가리면 물어볼 자리까지 덮여 이 방식이 안 된다.
  · 서브노트의 `scan_questions:` 는 손으로 유지하지 말 것 —
    `python pipelines/restore_store.py --sync-subnote <서브노트 카드>` 가 문항에서 다시 만든다.
  · 오픈 데이터 목록·주차 선정 같은 **결정론**은 `pipelines/datasets.py`가 맡는다(카드는 해석).

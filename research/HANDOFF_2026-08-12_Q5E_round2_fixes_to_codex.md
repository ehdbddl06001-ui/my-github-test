# Codex 과제 — Q5-E 교정 구현 3차 인수검사 (검토만, 실행 금지)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: approved_for_implementation` · `design_owner: codex` ·
`implementation_owner: claude`)
근거: PR #115(2차 교정 구현). 직전 단계: 2차 인수검사 = `IMPLEMENTATION_BLOCKED`,
blocker 7개.

승인 체인상 위치: **2차 인수검사(BLOCKED, 7 blocker) → 교정 구현 → Codex 3차
인수검사(지금) → 사용자 실행 승인.**

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md 전체.
   특히 M4.0 조건 1~3, M4.1 anchor 규칙(±54 tolerance, offset 배치),
   M5 고정 strata, Decision log 의 2026-08-12 "second corrective
   implementation (I1 round 2)" 항목.
3. mit-bih/q5e_leg2_failure_mechanism_audit.py
4. mit-bih/test_q5e_leg2_failure_mechanism_audit.py
5. notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb
6. mit-bih/q5d_order_preserving_beat_join.py — 읽기 전용. 절대 수정하지 마라.
7. PR #115 의 diff 전체

[네 역할]
설계자로서 **3차 구현 인수검사**만 한다. 코드를 고치지 말고, 명세의 과학적
내용을 바꾸지 마라. 등록 데이터를 열지 마라. 실행하지 마라.

[A. 2차 blocker 7개가 실제로 닫혔는가]
각각 CLOSED / NOT_CLOSED / PARTIAL 로 판정하고, 근거가 되는 파일·함수·라인을
대라. "주장"이 아니라 "코드 경로"로 답하라.

A1 (blocker 1) Production M4.
   - load_all_inputs() 가 load_frozen_rr()·build_detector_replay()·
     anchors builder 를 실제로 채우는가. 빈 dict/None 이 남아 있지 않은가.
   - DetectorReplay 가 digest 검증된 V10 frontend.py 를 producer 로 로드하고
     22개 DS1 record 에 detect_r() 를 재실행하는가.
   - match_peaks_to_annotations() 가 source 자신의 규칙(tol=int(0.15*fs)=54,
     greedy nearest + used set, AAMI 선택, p±150 cut)만 쓰는가. **새 detector·
     새 tolerance·수동 anchor 가 없는가.**
   - mitdb_dir 가 실제 M4 입력인가(신호 + .atr). Leg 1 identity attach 가
     anchor 배치의 전제로 실제로 쓰이는가.
   - anchors 가 replay 이후에만 만들어지는 것이 구조적으로 강제되는가.
   - **가장 중요:** 실행 승인 후 guard 한 줄만 제거하면 조건 2 전체가 실제로
     평가되는가. 아직 배선이 남아 있으면 어디인지 지목하라.

A2 (blocker 2) M5.
   - stratified_statistic() 가 class/reason/record/count_stratum/116/208/
     pooled 각각에서 hypothesis 통계를 실제로 계산하는가.
   - hypothesis_strata() 가 H1/H2/H3/H4 각각에 대해 **그 hypothesis 의
     population** 을 쓰는가(H1=distance gate rows, H4=cache-side graph rows,
     H2/H3=mamba failure positions). 잘못된 unit 을 쓴 곳이 없는가.
   - has_stratified_evidence() 로 pooled-only gate 가 이름이 아니라 실제
     수치를 요구하는가.

A3 (blocker 3) Bundle.
   - assert_bundle_inputs_complete() 가 os.makedirs 이전에 도는가.
   - staging → verify → rename 이 atomic 한가. 실패 시 최종 경로와 staging
     둘 다 남지 않는가.

A4 (blocker 4) Figures.
   - 7개 kind 가 전부 다른가. figure_data() 가 각 그림의 등록된 의미대로
     panel 을 만드는가(side panels / 22x3 heatmap / 208 raster +
     raw-ordinal sensitivity / run-length hist + summary / fixed-bin
     distance hist + censor·endpoint bars / side별 violin+ECDF +
     decisional label / anchor curve + Control C band).
   - render_figures() 의 중복 데이터 거부가 충분한 안전망인가.

A5 (blocker 5) Fixture seam.
   - qa_fixture 가 explicit synthetic input 에서만 오는가.
   - production run_audit 가 QA_TARGETS_REGISTERED 가 아니면 **쓰기 전에**
     거부하는가.
   - result/config/manifest/summary + SYNTHETIC_FIXTURE.json 각인이 충분한가.

A6 (blocker 6) Discovery.
   - MIT-BIH 가 SHA256SUMS.txt publisher checksum 으로 검증되는가.
     checksum 파일이 없는 tree 를 거부하는가.
   - V10 source 가 등록된 7파일 expected set + aggregate 로 매칭되는가
     (frontend.py 는 V9/V10 동일하므로 그것만으로는 부족하다).
   - run_audit 가 discovery stamp 없는 입력을 거부하는가.
   - **내가 발견해 고친 결함을 확인해 달라:** 이전 구현은
     load_all_inputs() 가 등록 상수(M4_INPUT_CONTRACT aggregate)를
     *관측값* 으로 넘겨서 identity sub-gate 가 상수를 자기 자신과 비교했고
     따라서 절대 실패할 수 없었다. 지금은 observed_m4_identity() 가 마운트된
     바이트에서 매번 다시 계산한다. 이 진단이 맞는지, 수정이 충분한지
     판정하라. 비슷한 자기참조 검증이 다른 gate 에도 남아 있는지 확인하라.

A7 (blocker 7) Test runner.
   - AST 기준 선언/수집 일치, 테스트별 assertion 최소 1회 증가가 강제되는가.
   - assertion 총수를 고정 숫자로 과장하지 않는가.

[B. 새로 판단이 필요한 지점]
B1. `match_peaks_to_annotations()` 는 등록 `data.py` 의 규칙을 **텍스트 계약
    으로부터 재구현**한 것이다(원본을 import 하지 않는다). greedy nearest 의
    순회 순서, used set 의 소비 시점, AAMI 선택과 boundary cut 의 상대 순서가
    원본과 어긋나면 22/22 count 재현이 실패한다. 이 재구현을 승인하는가,
    아니면 등록 `data.py` 의 `build_record` 를 직접 import 해 호출해야 하는가.
    후자라면 그 함수의 시그니처·부작용을 명세에 어떻게 고정할지 지정하라.
B2. `_rr_columns()` 는 replay 의 `rr_features()` 출력이 (n,7) 이 아니면
    거부한다(reshape/pad/select 하지 않음). 이 강경한 처리가 맞는가.
B3. MIT-BIH aggregate 를 명세에 전체 64-hex 로 등록할 것인가. 지금은 절단형
    (`0b46a411…`)만 있어 publisher checksum 검증으로 대체했다.

[C. 회귀]
C1. 합성 end-to-end 테스트가 실제 production M4 경로(build_detector_replay +
    anchors_by_record + load_frozen_rr)를 지나는지, 주입된 것은 producer 와
    두 reader 뿐인지 확인하라.
C2. 등록 자산을 여는 테스트가 하나도 없는지 확인하라.
C3. q5d 모듈이 code SHA-256
    6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226
    로 불변인지, q5d 테스트가 894 passed 인지 확인하라.

[절대 하지 마라]
- 등록 데이터 접근, M0~M4 집계, detect_r() 실행, beat join 재실행
- DS2 per-beat label · V10 probability · association / S PR-AUC 접근
- 학습, 기존 Drive bundle · null shard 수정
- q5d_order_preserving_beat_join.py 및 그 테스트 수정
- status 를 approved_for_execution / RUNNING / MEASURED / COMPLETE 로 변경
- terminal execution guard 제거, 노트북 실행, 명세에 결과 수치 기입
- 규칙 완화 · fallback runtime · partial record pass 도입

[출력 형식]
1. A1~A7 각각 CLOSED / NOT_CLOSED / PARTIAL + 근거(파일·함수·라인)
2. B1~B3 각각 승인 / 조건부 승인(조건 명시) / 철회(대안 명시)
3. C1~C3 판정
4. 남은 blocker 를 번호를 붙여 나열
5. 최종 판정 하나:
   - IMPLEMENTATION_ACCEPTED → 사용자에게 실행 승인을 요청해도 되는 상태
   - IMPLEMENTATION_BLOCKED → 남은 blocker 와 함께 재교정 요구
6. 승인 시, 실행 승인 PR 이 건드려도 되는 범위를 한 줄로 못박아라
7. 판정과 근거를 명세 Decision log 용 문단으로 정리하라(결과 수치 금지)
```

---

## 참고 — 이번 PR 에서 바뀐 파일 (정확히 4개)

- `mit-bih/q5e_leg2_failure_mechanism_audit.py`
- `mit-bih/test_q5e_leg2_failure_mechanism_audit.py`
- `notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb`
- `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
  (Decision log 항목 추가만; `status` 및 frontmatter 불변)

## 참고 — 검증 결과 (실행 없이 얻은 것)

- Q5-E 합성 테스트: 71 test functions · 555 assertions 통과
- Q5-D 회귀: 894 passed · 0 failed
- runner 안전망 2종을 실제로 깨뜨려 확인: runner 뒤에 붙인 테스트 → 실패,
  assertion 없는 테스트 → 실패
- `git diff --check` clean · `indexer.py --check` 통과
- 노트북 미실행: code cell 10개, outputs 전부 빈 값, `execution_count` 전부 null
- `q5d_order_preserving_beat_join.py` code SHA-256 불변
- `run_audit()` 내 terminal guard 가 loader·pipeline 양쪽보다 앞섬을 확인


---

# 3차 검토 대응 (2026-08-12, PR #115 갱신)

3차 판정 `IMPLEMENTATION_BLOCKED` (A1 PARTIAL · A6 NOT_CLOSED) 의 지시를 적용했다.
아래는 Codex 4차 검토용 요약이며, 프롬포트는 위 본문을 그대로 재사용하되
다음 항목을 추가로 확인하면 된다.

## 적용한 설계 판정

- **B1** — 독립 adapter 유지(등록 `build_record` 전체 호출 안 함). 산문이 열어두던
  제어흐름 결정을 `SOURCE_MATCH_CONTRACT` 에 전부 고정: 양쪽 순회 순서, 거리 동률
  규칙, 최근접이 이미 used 일 때 **차순위로 내려감**, used 추가 시점, used 가 AAMI
  선택·boundary cut **보다 먼저** 소비됨. 반례 fixture 6종 추가.
  등가성은 주장하지 않는다 — `source_match_equivalence_status()` 가
  `SOURCE_MATCH_EQUIVALENCE_REQUIRED` 를 보고하고 adapter fingerprint 와 등록
  `data.py` digest 를 고정한다. **22/22 count 재현은 필요조건일 뿐**이라고 코드가
  스스로 기록한다.
- **B2** — 2차원 여부, 모든 행 폭 7, 행 수 = kept peak 수를 전부 검증.
  ragged / 1-D / (n,6) / (n,8) / row-count mismatch 각각 `M4_RR_MISMATCH` 로 거부.
- **B3** — 전체 64-hex 값이 repo·인계문·preflight 어디에도 **없다.**
  추측·복원하지 않고 `MITDB_TREE_AGGREGATE = None` 으로 두고 gate 가
  `INPUT_IDENTITY_REGISTRATION_REQUIRED` 를 보고한다.

## 추가 blocker 대응

- **1 (stamp)** — `DISCOVERY_VERIFIED` 상수와 `assert_discovered_identity()` 를
  **삭제**했다. `run_audit` 이 실행 직전 모든 입력을 바이트에서 재검증한다.
  위조 mapping 거부 회귀 테스트 추가.
- **2 (problems)** — `hash_file_set` 의 missing/unexpected 를 identity gate 와
  discovery 양쪽에서 실패로 취급. aggregate 는 맞지만 unexpected file 이 있는
  fixture 가 실패하는 테스트 추가. problem 목록은 result 의 identity audit 에 보존.
- **3 (bundle 내용 신원)** — 5개 파일 per-file SHA-256 검증 도입. 등록값이 없으므로
  `SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED` 로 중단. 1-byte 변경이 검증을 깨는 회귀
  테스트 포함(등록값을 지어내지 않고 주입으로 비교 로직만 시험).
- **4 (duplicate)** — EXP-2026-007 선례를 따라 0건 실패 / 동일 digest 사본은
  deterministic 선택 + audit 기록 / 서로 다른 digest 는 병합 금지.
  Drive 파일 삭제·이동을 요구하지 않는다.

## 이번 라운드에서 발견한 잠재 결함 (보고)

Q5-E 와 Q5-D 의 **execution approval token 이 서로 다른데**, Q5-E 가 자기 토큰을
frozen module 의 reader 들에 그대로 넘기고 있었다. 실행 승인 후 production 의 모든
등록 read(mamba·cache·classes·`.atr`·`hash_file_set`)가 frozen module 에서 거부됐을
것이고, 그 사실은 **실행 시점에야** 드러났을 것이다. `frozen_module_approval()` 로
명시적 번역을 넣었다(Q5-E 승인 선행 필수, 미승인 호출자는 Q5-E 쪽 거부를 받음).

## 남은 open item (실행 전 반드시 해소)

1. `INPUT_IDENTITY_REGISTRATION_REQUIRED` — MIT-BIH tree 전체 aggregate 등록
2. `SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED` — canonical Q5-D bundle 5파일 digest 동결
3. `SOURCE_MATCH_EQUIVALENCE_REQUIRED` — adapter ↔ 등록 `data.py` differential

셋 다 **별도 사용자 승인을 받은 read-only PREP** 이 필요하다. 지금 Drive 를 열어
계산하지 않았다.

# Codex 과제 — Q5-E 교정 구현 2차 인수검사 (검토만, 실행 금지)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: approved_for_implementation` · `design_owner: codex` ·
`implementation_owner: claude`)
근거: PR #113(I1 교정 구현), main `4888fc1` 에 병합됨.
직전 단계: PR #112 = Codex 1차 인수검사(I1 = 7개 blocker, I2~I4 결정).

승인 체인상 위치: **1차 인수검사(I1~I4) → I1 교정 구현 병합 완료 →
Codex 2차 인수검사(지금) → 사용자 실행 승인.**
2차 인수검사를 통과해야만 사용자에게 실행 승인을 요청한다.

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md 전체.
   특히 Decision log 의 2026-08-12 "corrective implementation of the I1
   blockers; never executed" 항목과, 그 앞의 I1~I4 인수검사 기록.
3. mit-bih/q5e_leg2_failure_mechanism_audit.py
4. mit-bih/test_q5e_leg2_failure_mechanism_audit.py
5. notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb
6. mit-bih/q5d_order_preserving_beat_join.py — 읽기 전용이다. 절대 수정하지 마라.
7. PR #112(너의 1차 인수검사)와 PR #113(이번 교정 구현)의 diff

[네 역할]
너는 설계자다. 이번 과제는 **2차 구현 인수검사**이며, 검토만 한다.
코드를 고치지 말고, 명세의 과학적 내용(질문·H1~H4·split·지표·중단 조건·
association 경계)을 바꾸지 마라. 등록 데이터를 열지 마라. 실행하지 마라.

[이번에 확인해야 할 것 — A. I1 7개 blocker 가 실제로 닫혔는가]
아래를 코드에서 직접 확인하고 각각 CLOSED / NOT_CLOSED / PARTIAL 로 판정하라.
"주장"이 아니라 "코드 경로"를 근거로 답하라.

A1 (I1.1) run_audit() 이 approval → runtime → canonical bundle →
    terminal guard → load_all_inputs() → run_pipeline() 순서인가.
    실행 승인 PR 이 terminal guard 한 줄만 제거하면 되는 상태인가,
    아니면 아직 과학 로직이 처음 배선되는 부분이 남아 있는가.
A2 (I1.2/I1.5) cache_partition() 이 certified cache beat(= join map 에서
    certified mamba row 로만 존재하는 것)를 cache-side 분모에 포함하는가.
    Control A 입력 벡터가 processed-class map 에서만 오고 mamba_aami 가
    어떤 경로로도 섞이지 않는가.
A3 (I1.3) m3_graph() 의 QA 가 양쪽 side 를 row 단위로 대조하고 reason
    count 까지 일치를 요구하는가. 합계만 맞으면 통과하는 구멍이 없는가.
A4 (I1.4) M4_GATE_ORDER 에 input_identity 가 등록된 위치에 있고,
    detector replay 가 앞의 3개 sub-gate 통과 전에는 불가능한가.
A5 (I1.6) M5 strata 가 실제로 materialise 되는가. pooled 만 보고된 근거가
    Holm 유의해도 flag 를 못 켜는가.
A6 (I1.7) required_outputs() 가 기록 전에 계산되고, 불완전 번들이
    기록되지 않고 거부되는가. figure 가 실제 파일로 렌더링되는가.
A7 실행 봉인이 전부 유지되는가: 등록 데이터 미개봉, M0~M4 미집계,
    detect_r() 미호출, beat join 미재실행, DS2 per-beat label · V10
    probability · association / S PR-AUC 미접근, 학습 없음, 기존 Drive
    번들 · null shard 미수정, q5d 모듈 code SHA-256 이
    6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226
    로 불변, status 가 approved_for_implementation 유지,
    terminal execution guard 존치, 노트북 미실행.

[이번에 확인해야 할 것 — B. 교정 과정에서 새로 들어온 판단 2가지]
이 둘은 blocker 목록에 없던 것이고, 내가 판단해서 넣었다.
설계자로서 승인 / 조건부 승인 / 철회를 명확히 결정하라.

B1. **fixture QA target seam.**
    합성 end-to-end 테스트가 QA 단계를 통과하려면 등록 QA target(24,341 등)을
    재현할 수 없으므로, verify_qa_targets() / run_pipeline() 에
    qa_fixture 인자를 추가했다. 기본값은 등록 target 이고, production
    (run_audit) 은 이 인자를 절대 넘기지 않으며 그 사실을 회귀 테스트가
    고정한다. fixture 로 만든 결과는 q5e_result.json 에
    qa_target_set = FIXTURE · synthetic_fixture = true 로 각인되고
    summary.md 에 "NOT A Q5-E RESULT" 배너가 박힌다.
    질문: 이 seam 이 "규칙 완화 / 우회 경로"인가, 아니면 허용 가능한
    fixture 경계인가. 승인한다면 그 경계를 명세 어디에 고정할지 지정하라.
    반대한다면 대안(예: end-to-end 테스트가 QA 단계를 건너뛰도록 축소,
    혹은 등록 target 자체를 주입 불가로 두고 QA STOP 경로만 검증)을
    명시하라.

B2. **digest 기반 입력 탐색(discover_registered_inputs /
    run_audit_from_mount).**
    "deterministic Drive path 구성" 요구를 만족시키기 위해, 노트북이 경로를
    타이핑하지 않고 mount root 하나 아래에서 등록 digest 로 입력을 찾도록
    했다. canonical bundle 은 manifest code_sha256, mamba_data.npz 는
    BJ.MAMBA_SHA256, V10 cache 는 45파일 aggregate, V10 source map 은 두
    파일 digest 로 식별한다. 0건·2건·SUPERSEDED 마커는 모두 거부한다.
    MIT-BIH publisher tree 는 명세가 aggregate 를 절단형(0b46a411…)으로만
    고정하고 Q5-E 가 열지도 않으므로, digest 를 새로 만들어 박지 않고
    등록 파일 집합의 완전성으로만 매칭했다.
    질문: (a) 이 탐색이 "path 가 아니라 digest 로 identity 를 세운다"는
    명세 원칙과 일치하는가. (b) MIT-BIH 를 완전성으로만 매칭한 것이
    수용 가능한가, 아니면 전체 aggregate 를 명세에 등록해야 하는가.
    (c) 탐색 자체가 등록 자산을 해싱하므로 approval 뒤에 있어야 하는데,
    실제로 approval → discovery 순서인지 확인하라.

[이번에 확인해야 할 것 — C. 테스트가 진짜로 도는가]
C1. 이전 커밋에서 runner 뒤에 붙은 테스트들이 수집되지 않은 채 suite 가
    "통과"를 출력하던 결함이 있었다. run_all() 이 이제 파일의
    `def test_` 선언 수와 수집 수를 비교해 불일치 시 실패한다.
    이 방식이 충분한가, 아니면 더 강한 보증(예: 각 테스트가 최소 1개
    assertion 을 올렸는지 확인)이 필요한가.
C2. 합성 end-to-end 테스트가 실제로 M4_OK 까지 가서 Control C · H2 · H3 ·
    m4_anchors.csv · figure 7장을 전부 통과하는지, 그리고 fixture 가
    frozen matcher 로 생성되어 "정답 암기"가 불가능한지 확인하라.
C3. 이 테스트가 여는 파일이 하나도 없는지(open tripwire)를 확인하라.

[절대 하지 마라]
- 등록 데이터 접근, M0~M4 집계, detect_r() 실행, beat join 재실행
- DS2 per-beat label · V10 probability · association / S PR-AUC 접근
- 학습, 기존 Drive 번들 · null shard 수정
- mit-bih/q5d_order_preserving_beat_join.py 및 그 테스트 수정
- status 를 approved_for_execution / RUNNING / MEASURED / COMPLETE 로 변경
- terminal execution guard 제거
- 노트북 실행, 명세에 결과 수치 기입
- 규칙 완화 · fallback runtime · partial record pass 도입

[출력 형식]
1. A1~A7 각각 CLOSED / NOT_CLOSED / PARTIAL + 근거가 되는 파일·함수·라인
2. B1, B2 각각 승인 / 조건부 승인(조건 명시) / 철회(대안 명시)
3. C1~C3 판정
4. 남은 blocker 가 있으면 I1 때와 같은 형식으로 번호를 붙여 나열
5. 최종 판정 하나:
   - IMPLEMENTATION_ACCEPTED → 사용자에게 실행 승인을 요청해도 되는 상태
   - IMPLEMENTATION_BLOCKED → 남은 blocker 목록과 함께 재교정 요구
6. 승인 시, 실행 승인 PR 이 건드려도 되는 범위를 한 줄로 못박아라
   (예: "terminal execution guard 제거와 노트북 스위치 2개 변경만").
7. 판정과 근거를 명세 Decision log 에 넣을 문단으로 정리해 제시하라
   (결과 수치는 넣지 마라).
```

---

## 참고 — 이번 PR 에서 바뀐 파일 (정확히 4개)

- `mit-bih/q5e_leg2_failure_mechanism_audit.py`
- `mit-bih/test_q5e_leg2_failure_mechanism_audit.py`
- `notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb`
- `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
  (Decision log 항목 추가만; `status` 및 frontmatter 불변)

## 참고 — 검증 결과 (실행 없이 얻은 것)

- Q5-E 합성 테스트: 59 test functions · 438 assertions 통과
- Q5-D 회귀: 894 passed · 0 failed
- `git diff --check` clean · `indexer.py --check` 통과
- 노트북 미실행: code cell 10개, outputs 전부 빈 값, `execution_count` 전부 null
- `q5d_order_preserving_beat_join.py` code SHA-256 불변
  (`6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226`)
- `run_audit()` 내 terminal guard 가 loader 와 pipeline 양쪽보다 앞섬을 확인

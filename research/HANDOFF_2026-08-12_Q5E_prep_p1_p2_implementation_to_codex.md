# Codex 과제 — Q5-E PREP P1·P2 구현 인수검사 (검토만, 실행 금지)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-prep-p1-p2-execution-contract.md`
(`status: approved_for_implementation`)
상위 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
근거: PR #116 (draft), branch `claude/q5e-prep-p1-p2-implementation`,
tip `7d308fcac735384fed84af8dfadf6f04a015f0c8`

승인 체인상 위치: **PR #115 병합 완료 → P1·P2 구현(지금) → Codex 구현 인수검사
→ 사용자 read-only 실행 승인 → P1·P2 실행 → Codex 결과 인수 → 별도 등록 PR →
P3 → 그 뒤에만 Q5-E 실행 승인 판단.**

이번 PR 은 **구현만** 이다. 등록 자산 미개봉, Drive API 미호출, 실제 digest
미계산, 등록값 미기입, P3 범위 밖.

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-prep-p1-p2-execution-contract.md 전체
3. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md
   (특히 세 terminal gate 와 Decision log 의 4~6차 검토 항목)
4. research/HANDOFF_2026-08-12_Q5E_prep_p1p2p3_to_codex.md (P1·P2·P3 설계 초안)
5. research/ASSETS.md 의 data-mitdb-raw-100 행
6. mit-bih/q5e_prep_p1_p2_asset_identity.py
7. mit-bih/test_q5e_prep_p1_p2_asset_identity.py
8. notebooks/quest56_q5e_prep_p1_p2_asset_identity.ipynb
9. mit-bih/q5e_leg2_failure_mechanism_audit.py (읽기 전용 참조)
10. mit-bih/q5d_order_preserving_beat_join.py — 읽기 전용. 절대 수정하지 마라.
11. PR #116 전체 diff

[네 역할]
설계자로서 **P1·P2 구현 인수검사**만 한다. 코드를 고치지 말고, 명세의 과학적
내용을 바꾸지 마라. 등록 데이터를 열지 마라. Drive API 를 호출하지 마라.
실행하지 마라. P3 는 이번 범위가 아니다.

[A. P1 이 계약대로인가]
각 항목을 CLOSED / NOT_CLOSED / PARTIAL 로 판정하고 파일·함수·라인을 대라.

A1. gate 순서가 expected_file_set → checksum_file_digest →
    publisher_checksums → tree_aggregate 인가. 첫 실패에서 중단하는가.
A2. **aggregate 가 앞의 세 gate 통과 뒤에만 계산되는가.** 실패한 tree 가
    등록 후보로 오해될 숫자를 내놓지 않는가. (실패 경로에서
    tree_aggregate 가 None 인지 확인하라. MITDB_IDENTITY_DIVERGED 만
    예외적으로 관측값을 보존하는데, 그 처리가 맞는가.)
A3. BJ.mitdb_expected_files() 를 **그대로** 쓰는가. SHA256SUMS.txt 를 따로
    append 하지 않는가.
A4. 147/147 을 "146 publisher-listed + 목록 파일 자체" 로 정확히 표현하는가.
    checksum 파일 digest 가 틀리면 publisher list 를 **신뢰하지 않고** 즉시
    중단하는가(그 뒤 gate 를 아예 실행하지 않는가).
A5. checked=146 이 아니면 hash mismatch 가 0 이어도 거부하는가.
A6. aggregate fold 가 기존 canonical convention 과 **동일**한가.
    (`test_p1_aggregate_matches_the_frozen_fold_convention` 이
    BJ.hash_file_set 의 aggregate 와 일치를 확인한다. 이 방식이 충분한가.)
A7. 절단형 0b46a411 을 prefix 비교로만 쓰고, 복원·추측하지 않는가.

[B. P2 가 계약대로인가]
B1. folder id 로만 조회하는가. folder **name** 검색 경로가 어디에도 없는가.
    run_prep 이 등록 folder id 외의 id 를 거부하는가.
B2. gate 순서가 folder_id_inventory → inventory_unambiguous →
    directory_contract → superseded_absent → canonical_bytes_bridge →
    manifest_identity → input_identity 인가.
B3. duplicate name · 하위 폴더 · shortcut · trashed · nameless 를 전부
    ambiguity 로 거부하는가. 놓친 모호성 유형이 있는가.
B4. **bridge 규칙이 충분한가.** file-id 스트림이면 bridge 불필요로 처리하고,
    마운트는 exact name/size/count + provider checksum 으로만 연결하며,
    실패 시 P2_FOLDER_ID_BRIDGE_UNRESOLVED 로 중단하는가.
    폴더 이름 일치가 bridge 를 대신할 수 있는 경로가 정말 없는가.
B5. directory contract(12파일)와 input identity(5파일)가 분리되어 있고,
    나머지 7파일이 input identity 에서 unexpected 로 취급되지 않는가.
B6. manifest 의 code SHA 와 rule fingerprint 를 둘 다 검증하는가.
B7. 바이트 해시만 하고 parquet 을 파싱하거나 내용을 집계하지 않는가.
    QA count 를 신원 근거로 쓰지 않는가.

[C. 독립성과 등록 경계]
C1. P1 실패가 P2 판정을 덮어쓰지 않고, 그 반대도 아닌가. 각 first_failure 가
    따로 보존되는가. 둘 다 실패하면 MULTIPLE_PREP_FAILURES 인가.
C2. 하나라도 실패하면 **통과한 쪽의 관측값도** 등록 후보로 제시하지 않는가.
    이 처리가 맞는가, 아니면 통과한 gate 의 값은 기록해도 되는가.
C3. registration_candidates 가 소스·명세를 자동 수정하지 않는가.
    MITDB_TREE_AGGREGATE / SOURCE_BUNDLE_FILE_SHA256 가 이 PR 에서
    여전히 미등록인가.

[D. 안전장치]
D1. import 만으로 데이터·네트워크에 닿지 않는가. OPEN_REGISTERED_DATA 기본
    False 인가. PREP 토큰이 Q5-E audit 토큰과 다른가(달라야 한다).
D2. terminal guard 가 모든 reader/API 호출보다 앞인가. 이번 PR 에서
    해제되지 않았는가.
D3. Drive adapter seam 이 read-only 인가. production adapter 가 import 시
    client 를 만들지 않는가. files().create/update/delete/copy 가 없는가.
D4. 인증정보·로컬 경로가 bundle 에 들어갈 수 없는가.
    normalise_child 가 identity 필드만 남기는가. assert_no_credentials 의
    키 목록이 충분한가.
D5. synthetic 결과가 SYNTHETIC_FIXTURE / NOT A Q5-E RESULT 로 각인되고
    ingestable=false 인가. production bundle 로 승격될 경로가 없는가.
D6. bundle 이 원자적으로 published 되는가. 계약 외 파일이 조용히 남을 수
    없는가.

[E. bundle identity — 자기참조 금지]
E1. prep_payload_sha256 가 manifest.json 을 제외하는가.
E2. manifest 자체 SHA-256 이 bundle 안 **어느 파일에도** 없는가.
    (테스트가 전 파일을 훑는다. 이 확인이 충분한가.)
E3. P3 전용 payload 파일(oracle_harness_identity.json ·
    fixture_results.json)을 가짜 값 대신 not_applicable seal 로 채운 판단이
    맞는가. 아니면 P1·P2 전용 payload 집합을 따로 정의해야 하는가.
E4. PREP_PAYLOAD_FILES 를 Q5E.PREP_PAYLOAD_FILES 의 **superset** 으로 두고
    registration_candidates.json 을 identity 안에 포함시킨 판단이 맞는가.
    (Q5-E 모듈을 수정하지 않으려고 이렇게 했다. 대신 fold 함수는 동일
    convention 을 쓰고 회귀 테스트가 일치를 확인한다.)

[F. 회귀·구조]
F1. 테스트가 등록 자산을 하나도 열지 않는가. P1 fixture 의 publisher list 가
    fixture 자신의 바이트에서 생성되어 실제 digest 를 외우지 않는가.
F2. _PatchedRegistration 이 fixture 경계를 명시적으로 만드는 방식이 맞는가.
    (합성 run 은 합성 등록값으로 측정해야 하므로 상수를 fixture 값으로
    바꾼다. 이게 편법인지 정당한 경계인지 판정하라.)
F3. runner 가 선언된 test function 을 모두 수집하는지, assertion 0 인 테스트를
    거부하는지 확인하라.
F4. 파일명·문서 위치가 repo convention 과 맞는가.
    실행계약을 Q5-E 명세의 한 절이 아니라 **별도 문서**로 둔 판단이 맞는가.

[G. 내가 판단해서 넣은 것 — 승인/철회를 명확히 하라]
G1. PREP 전용 execution token 을 Q5-E audit token 과 **분리**했다.
    (읽기 전용 PREP 승인이 audit 승인으로 번지지 않게 하려는 것.)
G2. run_prep 이 등록 folder id 가 아니면 **즉시 거부**한다.
    (id 를 인자로 받으면서 등록값만 허용하는 게 과한지 판단하라.)
G3. 실패 시 통과한 gate 의 관측값도 withhold 한다(C2).
G4. mount bridge 에서 provider checksum 이 있으면 그것도 대조한다.
G5. bundle 을 staging → 검증 → rename 으로 원자 publish 한다.

[절대 하지 마라]
- 등록 Drive 자산 접근, Drive API 호출, 실제 digest 계산
- P1·P2 실행, P3 구현·실행
- detect_r() 실행, M0~M4 집계, beat join 재실행
- DS2 per-beat label · V10 probability · association · S PR-AUC 접근
- 학습, 기존 Drive bundle · null shard 수정
- q5d_order_preserving_beat_join.py 및 그 테스트 수정
- MITDB_TREE_AGGREGATE · SOURCE_BUNDLE_FILE_SHA256 ·
  SOURCE_MATCH_ORACLE_RECORD 에 값 기입
- status 를 approved_for_execution / RUNNING / MEASURED / COMPLETE 로 변경
- terminal guard 제거, 노트북 실행, PR #116 병합

[출력 형식]
1. A1~A7 / B1~B7 / C1~C3 / D1~D6 / E1~E4 / F1~F4 각각
   CLOSED / NOT_CLOSED / PARTIAL + 근거(파일·함수·라인)
2. G1~G5 각각 승인 / 조건부 승인(조건 명시) / 철회(대안 명시)
3. 남은 blocker 를 번호를 붙여 나열
4. 최종 판정 하나:
   - PREP_IMPLEMENTATION_ACCEPTED → 사용자에게 read-only 실행 승인을
     요청해도 되는 상태
   - PREP_IMPLEMENTATION_BLOCKED → 남은 blocker 와 함께 재교정 요구
5. 승인 시, read-only 실행 승인 PR 이 건드려도 되는 범위를 한 줄로 못박아라
   (예: "terminal guard 제거와 노트북 스위치 2개 변경만")
6. 실행 뒤 결과 인수검사에서 무엇을 볼지 미리 명시하라
   (bundle 파일 집합 · payload fold · manifest 자체 digest 동결 위치 ·
    P1/P2 각 gate 결과 · registration_candidates 의 eligible 여부)
7. 판정과 근거를 실행계약 Decision log 용 문단으로 정리하라(결과 수치 금지)
```

---

## 참고 — 이번 PR 에서 추가된 파일 (4개, 기존 모듈 수정 0)

- `mit-bih/q5e_prep_p1_p2_asset_identity.py`
- `mit-bih/test_q5e_prep_p1_p2_asset_identity.py`
- `notebooks/quest56_q5e_prep_p1_p2_asset_identity.ipynb`
- `experiments/specs/EXP-2026-008-q5e-prep-p1-p2-execution-contract.md`

## 참고 — 검증 결과 (실행 없이 얻은 것)

- PREP 합성 테스트: **31 test functions · 245 assertions** 통과
- Q5-E 회귀: **106 tests · 843 assertions** (matplotlib 有) — 이 PR 로 불변
- Q5-D 회귀: **894 passed · 0 failed** — 이 PR 로 불변
- `git diff --check` clean · `indexer --check` 통과 · `indexer` 787개 성공 0 실패
- 노트북 미실행: code cell 10개, outputs 0, non-null `execution_count` 0
- `q5d_order_preserving_beat_join.py` diff 0, LF-normalized SHA-256
  `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226`
- Q5-E 세 stop 그대로: `MITDB_TREE_AGGREGATE = None` ·
  `SOURCE_BUNDLE_FILE_SHA256 = {}` · `SOURCE_MATCH_ORACLE_RECORD = None`

## 참고 — 구현 중 fixture 가 잡아낸 것

decoy 폴더 테스트가 처음에 실패했다. 원인은 fake adapter 가 폴더마다 같은
file id(`file-0`…)를 써서 조회가 **엉뚱한 폴더의 바이트** 를 돌려준 것이었다.
실제 Drive id 는 고유하므로 fixture 쪽 결함이었고 폴더별 id prefix 로 고쳤다.
P2 가 막으려는 혼동이 정확히 이 형태라서, 이 반례는 유지할 가치가 있다.

# Q5-E 실행 전 필수 PREP 3건 — 설계 초안 (P1 · P2 · P3)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex / 사용자
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: approved_for_implementation` 유지)
근거: Codex 4차 인수검사. PR #115 에서 셋 다 **terminal gate** 로 구현했고,
값은 하나도 만들지 않았다.

## 이 문서의 성격

**설계 초안이다.** 여기 적힌 어떤 PREP 도 아직 실행되지 않았고, 이번 PR 에서
실행하지 않는다. 각 PREP 는 **별도 사용자 승인 + 별도 브랜치/PR** 이 필요하다.
셋이 모두 끝나기 전에는 Q5-E 실행 승인을 요청할 수 없다.

세 항목은 코드에서 실제로 실행을 막는다:

| 항목 | 상수 / 게이트 | 막는 지점 |
|---|---|---|
| P1 | `MITDB_TREE_AGGREGATE is None` → `INPUT_IDENTITY_REGISTRATION_REQUIRED` | `verify_mitdb_identity()` — discovery 와 실행 직전 재검증 |
| P2 | `SOURCE_BUNDLE_FILE_SHA256 == {}` → `SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED` | `verify_bundle_content_identity()` — 실행 직전 재검증 |
| P3 | `SOURCE_MATCH_ORACLE_RECORD is None` → `SOURCE_MATCH_EQUIVALENCE_REQUIRED` | `verify_source_match_equivalence()` — **M4.0 sub-gate, detector 이전** |

---

## P1 — MIT-BIH publisher tree 전체 aggregate 등록

**입력**
- 등록된 MIT-BIH publisher tree (`mitdb-1.0.0`), Drive 마운트
- `BJ.mitdb_expected_files()` (48 record × 3 + metadata)
- `BJ.MITDB_CHECKSUM_FILE` (`SHA256SUMS.txt`)

**절차**
1. publisher `SHA256SUMS.txt` 대조로 147/147 PASS 를 **선행 확인**한다.
   실패하면 즉시 중단하고 aggregate 를 계산하지 않는다.
2. `BJ.hash_file_set()` 의 기존 digest convention 을 그대로 써서 전체 fold 를
   계산한다. 새 convention 을 만들지 않는다.
3. 관측된 전체 64-hex 가 기존 절단형 `0b46a411…` 과 접두 일치하는지 확인한다.
   불일치면 `MITDB_IDENTITY_DIVERGED` 로 중단한다.

**출력**
- 전체 64-hex aggregate 1개, 파일 수, 총 바이트
- 명세와 `MITDB_TREE_AGGREGATE` 에 **동시에** 등록

**중단 규칙**
- publisher checksum 이 147/147 이 아니면 중단
- 절단형과 접두 불일치면 중단
- 값을 절단형에서 복원·추측하지 않는다

**승인 경계** — read-only. `detect_r()` 실행, M0~M4 집계, 신호 해석 금지.

---

## P2 — canonical Q5-D bundle 5파일 digest 동결

**입력** — 정확히 이 run 하나:
- `20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE`
- folder id `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd`
- 파일: `unmatched_and_ambiguous.csv`, `join_map.parquet`,
  `record_class_coverage.csv`, `decision.json`, `manifest.json`

**절차**
1. **folder id 로** 대상을 고정한다. 같은 `code_sha256` 을 가진 임의 폴더를
   canonical 로 고르지 않는다 — 이것이 이 PREP 가 존재하는 이유다.
2. `SUPERSEDED.json` 부재를 확인한다.
3. 5파일 각각의 SHA-256 과 바이트 수를 기록하고, 전체 fold 도 함께 보존한다.
4. `manifest.json` 의 `code_sha256` 이 `6b098c67…` 인지, `rule_fingerprint`
   가 `31c4be9f…` 인지 확인한다.

**출력**
- `SOURCE_BUNDLE_FILE_SHA256` 5개 항목 + 전체 fold
- 명세와 모듈에 동시 등록

**중단 규칙**
- folder id 로 대상을 특정할 수 없으면 중단
- `SUPERSEDED.json` 이 있으면 중단
- code SHA 또는 rule fingerprint 불일치면 중단
- QA count 일치를 신원 근거로 쓰지 않는다

**승인 경계** — read-only. parquet 내용 집계·해석 금지(바이트만 읽는다).

---

## P3 — candidate adapter ↔ registered `data.py` differential

가장 무겁고, 가장 중요하다. **22/22 count 재현은 증명이 아니며 구현 선택
기준도 아니다.**

**입력**
- 등록 V10 source package (7파일), `data.py` SHA-256
  `20cde66b01d1172926aa1b84cbb70b70ea28bb20c2e958a2c26bd01d03497ada`
- 현재 adapter fingerprint (`Q5E.source_match_adapter_fingerprint()`)
- 반례 fixture: 현재 6종 + PREP 중 필요해지는 추가분

**선행조건**
- `data.py` 실제 바이트가 등록 digest 와 일치할 것. 불일치면 즉시 중단.

**절차**
1. `build_record` 의 **matching 제어흐름만** 안전한 oracle harness 로 실행한다.
   synthetic dependency injection 을 쓰고, 등록 ECG·`detect_r()`·M0~M4 는
   열지도 실행하지도 않는다.
2. 각 반례에서 adapter 와 source 의 **선택 결과** 를 비교한다. 최소 비교 항목:
   - peak → annotation 매핑
   - kept row 집합과 순서
   - `annotation_without_peak` / `peak_without_annotation` 집합
3. 불일치가 나오면 **count 를 보지 않고** source 제어흐름에 맞춰 adapter 를
   정정한다.
4. adapter 를 고쳤으면 fingerprint 를 다시 계산하고 전체 differential 을
   처음부터 재실행한다.

**출력** — `SOURCE_MATCH_ORACLE_RECORD` 에 넣을 구조화 레코드:

```
verdict                 = SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE
registered_file_sha256  = <data.py SHA-256>
adapter_fingerprint     = <정정 후 최종 fingerprint>
prep_bundle_sha256      = <PREP 산출물 번들 identity>
fixtures                = [<반례 이름 …>]
fixtures_passed         = <통과 수, fixtures 길이와 같아야 함>
```

**중단 규칙**
- `data.py` digest 불일치 → 중단
- 반례 하나라도 불일치한 채로 PASS 기록 금지
- 부분 통과는 PASS 가 아니다(`fixtures_passed != len(fixtures)` 는 거부됨)
- adapter 를 고친 뒤 fingerprint 재계산 없이 기존 결과 재사용 금지

**승인 경계** — read-only. 등록 ECG 미개봉, `detect_r()` 미실행, M0~M4 미집계,
DS2 label · V10 probability · association · S PR-AUC 미접근, 학습 없음.

---

## 실행 순서 제안

P1 과 P2 는 서로 독립이라 한 번의 승인으로 함께 처리해도 된다.
P3 는 분량과 위험이 달라 **별도 승인·별도 PR** 을 권한다.

셋이 끝나고 Codex 5차 인수검사가 `IMPLEMENTATION_ACCEPTED` 를 주면, 그때
비로소 사용자 실행 승인을 요청한다. 실행 승인 PR 이 건드릴 범위는 terminal
execution guard 제거와 노트북 스위치 2개 변경뿐이어야 한다.

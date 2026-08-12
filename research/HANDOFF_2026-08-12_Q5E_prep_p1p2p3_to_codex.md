# Q5-E 실행 전 필수 PREP 3건 — 설계 초안 (P1 · P2 · P3)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex / 사용자
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: approved_for_implementation` 유지)
근거: Codex 4·5차 인수검사. PR #115 에서 셋 다 **terminal gate** 로 구현했고,
값은 하나도 만들지 않았다. 5차 판정의 P1 `147/147` 의미 정정, P2 folder-id
bridge 요구, P3 oracle 정의 보강을 반영했다.

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
- 등록된 MIT-BIH publisher tree (`mitdb-1.0.0`), Drive
- `BJ.mitdb_expected_files()` — **이미 `SHA256SUMS.txt` 를 포함한 147파일이다.**
  같은 파일을 따로 append 하지 마라.
- `research/ASSETS.md :: data-mitdb-raw-100` 에 등록된
  `SHA256SUMS.txt` sha256
  `b61158a96d5f2ca80edfb354a9a66a6324836c390a84e1966dcee2b907d6be43`

**선행 integrity — 147/147 의 정확한 의미**

`SHA256SUMS.txt` 는 자기 자신을 검증할 수 없고, frozen
`BJ.verify_against_publisher_checksums()` 도 checksum 파일을 명시적으로 건너뛴다.
따라서 "publisher list 가 자기 자신까지 147개를 검증했다" 고 쓰면 **틀린다.**
두 부분을 합쳐야 147/147 이다.

1. publisher list 로 검증 가능한 **나머지 146파일**
   - `checked = 146`
   - `matched = 146`
   - `mismatch = 0`
   - `unlisted = 0`
2. `SHA256SUMS.txt` **자체**
   - 파일의 SHA-256 이 위 ASSETS 등록값 `b61158a9…` 과 일치

둘을 합쳐 **published tree integrity 147/147** 로 표현한다.

**절차**
1. 위 두 조건을 먼저 확인한다. 하나라도 실패하면 aggregate 를 계산하지 않는다.
2. `BJ.hash_file_set(directory, BJ.mitdb_expected_files(), …)` 의 기존
   convention 을 그대로 쓴다. 새 convention 을 만들지 않는다.
3. `missing = 0`, `unexpected = 0` 을 선행 확인한다.
4. 관측 full aggregate 가 기존 절단형 `0b46a411…` 과 **prefix 불일치** 하면
   `MITDB_IDENTITY_DIVERGED` 로 중단한다.

**출력** — 아래를 모두 기록한다.
- 147개 per-file digest
- full aggregate (64-hex)
- `SHA256SUMS.txt` 자체 digest
- publisher `checked` / `matched` 수 (146 / 146)
- 명세와 `MITDB_TREE_AGGREGATE` 에 **동시** 등록

**중단 규칙** — 146/146 미달, checksum 파일 digest 불일치, missing/unexpected≠0,
절단형 prefix 불일치. 값을 절단형에서 복원·추측하지 않는다.

**승인 경계** — read-only. `detect_r()` 실행, M0~M4 집계, 신호 해석 금지.

---

## P2 — canonical Q5-D bundle digest 동결

**대상**
- run `20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE`
- folder id `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd`

**folder id ↔ mount path bridge (필수)**

일반 Colab mount path 만으로는 Drive folder id 를 증명할 수 없다. 같은 이름의
폴더를 찾은 것은 증거가 아니다. 다음을 반드시 만든다.

1. Drive connector/API 로 위 **folder id 를 직접 조회** 해 read-only inventory 를
   만든다: folder id · child file id · name · bytes · modified time ·
   가능하면 provider checksum.
2. 이 inventory 를 prep input manifest 로 저장하고 **manifest 자체의 SHA-256** 을
   기록한다.
3. mount 바이트와 inventory 를 연결한다.
   - exact name / size / file count 대조
   - 가능하면 file id 기반 직접 다운로드 또는 Drive API stream 사용
4. 연결을 만들 수 없으면 **`P2_FOLDER_ID_BRIDGE_UNRESOLVED`** 로 중단한다.
   폴더 이름 일치로 대체하지 않는다.

**두 계약을 분리해서 동결한다**

- **directory completeness** — frozen `BJ.BUNDLE_FILES` **12파일** 전체.
  missing / unexpected 0, `SUPERSEDED.json` 부재, `manifest.json` 의
  `code_sha256` = `6b098c67…`, `rule_fingerprint` = `31c4be9f…`.
- **Q5-E scientific input identity** — Q5-E 가 읽는 **5파일** 의 개별 SHA-256 과
  subset fold. 나머지 7개 등록 파일을 unexpected 로 취급하지 않는다.
  (구현은 `Q5E.subset_file_fold()` 가 이미 이 분리를 한다.)

**출력**
- folder id inventory 와 그 SHA-256
- 12파일 completeness report
- Q5-E input 5파일 각각의 name / bytes / SHA-256
- 5파일 subset fold
- producing code SHA · rule fingerprint
- `SUPERSEDED` marker 부재
- training / model / probability 관련 내용을 열지 않았다는 seal

**중단 규칙** — folder id bridge 실패, `SUPERSEDED.json` 존재, 12파일
completeness 실패, code SHA 또는 rule fingerprint 불일치.
**QA count 일치를 신원 근거로 쓰지 않는다.**

**승인 경계** — read-only. parquet 은 **내용 집계 없이 바이트만** hash 한다.

---

## P3 — candidate adapter ↔ registered `data.py` differential

가장 무겁고 가장 중요하다. **22/22 count 재현은 증명이 아니며 구현 선택
기준도 아니다.**

**선행조건**
- 등록 `data.py` 를 ASSETS 의 **exact file id** 와 SHA-256
  `20cde66b01d1172926aa1b84cbb70b70ea28bb20c2e958a2c26bd01d03497ada`
  **둘 다** 로 확인한다. 하나만으로는 부족하다.

**oracle 의 정의 — 두 번째 재구현은 oracle 이 아니다**

matching 규칙을 다시 옮겨 적은 구현을 oracle 로 쓰면, 같은 오독을 두 번 해서
"일치" 를 얻을 수 있다. 그러므로 **digest 검증된 원본 `data.py` 의
`build_record` 를 실제로 실행** 한다. synthetic dependency injection 으로:
- wfdb / signal / annotation reader stub
- `detect_r` stub
- rr / feature producer stub
- 등록 ECG 미사용, real detector 미실행

**비교 대상**
- source 가 선택한 peak ↔ annotation mapping
- kept row 집합과 순서
- consumed annotation 집합
- unmatched annotation / peak 집합

원본이 직접 반환하지 않는 값은 **원본 실행 trace 에서 기계적으로 캡처** 한다.
사람이 해석한 규칙으로 재구성하지 않는다.

**절차**
1. `SOURCE_MATCH_REQUIRED_FIXTURES` 전부 + 사전등록한 추가 fixture 를 한 번에
   실행한다.
2. 불일치가 있으면:
   - real-record count 를 **보지 않는다**
   - source control flow 에 맞춰 candidate adapter 를 정정
   - adapter fingerprint 재계산
   - 모든 fixture 를 처음부터 재실행
   - 수정 전/후 기록을 PREP bundle 에 모두 보존

**출력** — `SOURCE_MATCH_ORACLE_RECORD` 에 넣을 구조화 레코드. 코드의
`verify_source_match_equivalence()` 가 아래를 전부 강제한다.

```
verdict                 = SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE
registered_file_sha256  = <data.py SHA-256, lowercase 64-hex>
adapter_fingerprint     = <정정 후 최종 fingerprint, 64-hex>
prep_bundle_sha256      = <PREP bundle identity, 64-hex>
oracle_harness_sha256   = <harness 구현 identity, 64-hex>
fixtures                = [ { "name": …,
                              "source_result_sha256":  <64-hex>,
                              "adapter_result_sha256": <64-hex>,
                              "equal": true }, … ]
fixtures_passed         = <equal=true 개수, 전체 fixture 수와 같아야 함>
```

검증 조건(코드가 거부하는 것): required fixture 누락 · 이름 중복 ·
`equal=false` · source/adapter result digest 불일치 · `fixtures_passed`
불일치 · 축소된 fixture 목록 · 64-hex 아닌 digest · stale adapter
fingerprint · 다른 `data.py` digest.

**PREP bundle 최소 구성**
`config.json` · `manifest.json` · `source_inventory.json` ·
`oracle_harness_identity.json` · `fixture_results.json`(또는 CSV) ·
`decision.json` · `log.txt` · `summary.md`.
모든 파일의 digest 와 전체 bundle identity 를 남긴다.

**승인 경계** — read-only. 등록 ECG 미개봉, `detect_r()` 미실행, M0~M4 미집계,
DS2 label · V10 probability · association · S PR-AUC 미접근, 학습 없음.

---

## 모든 PREP 공통 — bundle digest 자기참조 금지

`prep_bundle_sha256` 와 "manifest 자체 SHA-256" 을 같은 것으로 두면 순환 계약이
된다. manifest 안에 자기 digest 를 적는 순간 파일이 바뀌어 그 digest 가 무효가
되기 때문이다. 세 PREP 모두 아래 규칙을 따른다.

**payload fold — `prep_payload_sha256`**

- 대상(정확히 이 이름들만):
  `config.json` · `source_inventory.json` · `oracle_harness_identity.json` ·
  `fixture_results.json` · `decision.json` · `log.txt` · `summary.md`
- **제외:** `manifest.json` — 자기가 기록하는 fold 에 자신은 들어가지 않는다.
- 계산: 위 파일들의 `(name, bytes, sha256)` 을 이름순 정렬해 기존 canonical-JSON
  convention 으로 fold. 새 convention 을 만들지 않는다.
- 구현·회귀 테스트는 `Q5E.prep_payload_fold()` 와
  `test_a4_prep_payload_fold_cannot_reference_itself` 가 고정한다. 같은 입력은
  항상 같은 digest 를 내고, manifest 를 넣어도 fold 가 변하지 않으며,
  manifest 를 payload 에 포함하려는 시도는 거부된다.

**manifest 와 그 바깥**

- `manifest.json` 에는 `prep_payload_sha256` 을 **기록만** 한다.
- `manifest.json` **자체의 SHA-256** 은 bundle 밖 — 명세 Decision log 와 등록
  기록 — 에서 별도로 동결한다. bundle 안의 어떤 파일도 이 값을 바꿀 수 없다.
- P3 의 `prep_bundle_sha256` 필드에는 **payload fold** 를 넣는다. manifest 자체
  digest 를 넣지 않는다.
- P1 · P2 의 산출물 identity 도 같은 규칙을 따른다. P2 의 folder-id inventory
  manifest 역시 자기 digest 를 자기 안에 적지 않는다.

---

## 실행 순서 (Codex 5차 판정)

1. PR #115 blocker 수정  ← **지금 여기**
2. Codex 재검토
3. 사용자 병합 판단
4. 별도 PREP 구현 승인
5. 별도 branch/PR 에서 PREP 구현
6. 사용자 read-only 실행 승인
7. P1 · P2 · P3 실행 및 bundle 보존
8. Codex 결과 인수
9. 그 뒤에만 Q5-E execution 승인 여부 판단

P1 과 P2 는 서로 독립이라 한 번의 승인으로 함께 처리해도 된다. P3 는 분량과
위험이 달라 **별도 승인·별도 PR** 을 권한다.

Q5-E 실행 승인 PR 이 건드릴 범위는 terminal execution guard 제거와 노트북
스위치 2개 변경뿐이어야 한다.

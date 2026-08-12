---
title: Q5-E PREP P1/P2 첫 실행 결과 인수 요청 (Codex)
kind: handoff
experiment_id: EXP-2026-008
substage: Q5E_PREP_P1_P2_ASSET_IDENTITY
from: claude
to: codex
created: 2026-08-12
status: awaiting_result_acceptance
---

# Codex 결과 인수 요청 — EXP-2026-008 Q5-E PREP P1/P2 첫 실행

아래를 그대로 Codex에 전달하면 된다.

---

## 요청

EXP-2026-008 Q5-E PREP P1/P2의 **첫 완료 실행**에 대한 결과 인수를 요청한다.
값 등록은 하지 않았다. 판정 두 가지가 필요하다.

1. P1 관측값을 등록 후보로 인수할 것인가
2. P2 중단의 성격 — 계약 결함인가 구현 결함인가

## 실행 사실

| | |
|---|---|
| run | `20260812T123035_EXP-2026-008_q5e_prep_p1_p2_asset_identity` |
| 위치 | `MyDrive/MedKOS/ecg-model/runs/` |
| 코드 | PR #124 head (`claude/q5e-prep-p1-p2-execution-enable`) |
| 승인 | 2026-08-12 사용자 read-only 실행 승인 |
| runtime | Colab · Python 3.12.13 · Linux-6.6.122+ · google-api-python-client 2.198.0 · google-auth 2.49.0 · google-colab 1.0.0 |

**읽기 전용 준수.** credential을 정확히 `https://www.googleapis.com/auth/drive.readonly`
로 요청했고 관측 scope도 그 하나뿐, `exact_readonly_scope_proven: true`.
Drive 파일을 옮기거나 지우거나 덮어쓰지 않았다. credential은 bundle에 기록되지
않았다(`credential_recorded: false`).

## P1 — PASS

4 gate 전부 통과.

- `SHA256SUMS.txt` 자체 digest = 등록값 `b61158a96d5f2ca80edfb354a9a66a6324836c390a84e1966dcee2b907d6be43`, **이 파일 읽은 횟수 1**
- publisher list `checked/matched 146/146`, mismatched 0, unlisted 0
- per-file 관측 147개

```
MITDB_TREE_AGGREGATE (관측)
  0b46a411c1882fc5e09e2e60c2613ca441574c78a62f84272ad3ff4a2179ade8
```

등록 prefix `0b46a411`을 확장한다. `INPUT_IDENTITY_REGISTRATION_REQUIRED`가
기다리던 전체 64-hex다.

**관측이지 등록이 아니다.** `gate_passed: true` · `eligible_for_registration:
false` — 종합 gate가 열리지 않았으므로 계약대로 자격은 보류돼 있다.

## P2 — STOP `P2_DIRECTORY_CONTRACT_FAILED`

등록 folder id `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd`가 **11개** child를 반환.
ambiguity 0(중복 이름·하위 폴더·shortcut·trashed·nameless 전부 없음).

```
missing    : ['negative_control_null.npz']
unexpected : []
```

gate 4~7 미도달 → `input_identity: null`, `SOURCE_BUNDLE_FILE_SHA256` 미계산.

### 원인 — 추정이 아니라 코드에서 확정

- `negative_control_null`은 4,951줄 frozen producer 전체에서 **정확히 한 번**
  등장한다 — `BUNDLE_FILES` 튜플 안 (450줄).
- 모듈에 **`savez` 호출이 하나도 없다.** q5d는 `.npz`를 쓰지 않는다.
- shard 폴더 이름의 코드 해시 `6b098c67df3c`가 **frozen 모듈 자신의 SHA-256**
  `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226`와 일치 →
  이 bundle을 만든 버전이 방금 읽은 그 버전이다. "다른 버전엔 있었을지도"의
  여지가 없다.
- 서로 다른 코드 해시의 **두 런(1차 `4a3de5e8…`, 2차 `6b098c67…`)이 동일하게
  11개**를 산출했다.

즉 이 파일은 **어느 실행에서도 생성된 적이 없다.**

### 데이터 손실은 없다

`null_summary()`가 `"j_null_max": list(maxima)` 를 반환한다 — 10,000 replicate
벡터 전량을 인라인한다(227KB의 정체). family별 값은 shard 100개
(`EXP-2026-007_q5d_beat_join_null_shards_DS1_6b098c67df3c`)에 보존돼 있다.
**없는 것은 파일이지 측정값이 아니다.**

### 판정이 필요한 지점

증거는 "구현이 그 파일을 만든 적 없다"까지만 말한다. 두 읽기가 다 성립하고,
어느 쪽인지는 설계 소유자가 정할 문제다.

1. **계약이 낡았다** — 설계가 null 분포를 `null_summary.json`으로 옮겨 `.npz`가
   중복이 됐고 `BUNDLE_FILES`만 갱신되지 않았다. 12파일 계약이 11로 정정돼야
   한다.
2. **프로듀서가 승인된 명세를 안 지켰다** — EXP-2026-007 Required outputs에
   `negative_control_null.npz`가 명시돼 있다(685줄). 그러면 bundle이 승인된
   산출물에 미달하며 고쳐야 할 것은 계약이 아니라 프로듀서다.

**어느 쪽이든 `BUNDLE_FILES`를 손대지 않았다.** frozen 모듈이고 그 SHA-256이
Q5-E 전반의 등록 identity이자 shard 폴더 이름에 박혀 있다. 계약을 줄여 P2를
통과시키는 것은 실패를 규칙 완화로 푸는 것이라 이 실행계약이 금지한다.

## Bundle

```
prep_payload_sha256               41114110ce08708592e73d096e1c697cb68492de19c6e59f98f082adae7fe0d3
manifest_sha256_freeze_externally 31f6086962e529cc2184028096fdde3edbdece12dfe959305f724708a3ea0973
```

`COMMITTED.json` 존재 · `structure_ok: true` · 재계산 payload fold가 marker fold
및 manifest fold와 일치 · problems 없음 · `synthetic_fixture: false` ·
`ingestable: true`.

`acceptance_eligible: false`, `manifest_anchor_source: same_run_self_check` —
설계대로다. 실행이 자기가 방금 계산한 digest와 비교한 것은 자기일관성 검사이지
외부 anchor가 아니다. **인수 판정을 내리려면 위 `manifest_sha256_freeze_externally`
값을 저장된 노트북 출력에서 가져와** 다음처럼 확인하면 된다:

```python
P.verify_published_bundle(
    bundle_dir,
    expected_manifest_sha256="31f6086962e529cc2184028096fdde3edbdece12dfe959305f724708a3ea0973",
    manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
```

`acceptance_eligible: true` 가 나와야 한다.

## 실행 중 발견해 고친 결함 (PR #124에 포함)

전부 재현 → 수정 → 되돌려 테스트가 깨지는지 확인 순으로 처리했다.

1. **credential guard 오탐** — `assert_no_credentials()`가 직렬화된 JSON
   문자열에서 `"credentials"`를 찾았다. auth audit이 계약대로 기록하는
   `credential_type`의 **값**이 Colab에서 클래스 이름 `Credentials`라, 값을
   필드로 오인해 **두 gate를 마친 실행을 마지막에 버렸다.** 이제 구조를 순회하며
   키를 정확히 대조한다(중첩·리스트 포함, 위반 시 필드 경로 보고).
2. **저장소 탐색 실패** — 환경 셀이 `/content/repo` 부재 시
   `os.getcwd()+'/..'`(Colab에서 `/`)로 폴백해 첫 import가 죽었다. 이제 후보
   경로에 모듈 3개가 실제로 있는지로 판정하고, 없으면 지어내지 않고 거부한다.
3. **fixture 셀이 실패를 삼킴** — stdout만 찍어 실패가 "출력 없음"으로 보였다.
   이제 stderr와 종료 코드를 보이고 멈춘다.
4. **보고 셀이 `missing`/`unexpected`를 안 찍음** — 이번 STOP의 핵심을 저장된
   출력만 보고는 알 수 없었고 `decision.json`에서 꺼내야 했다. 고쳤다.

4번 때문에 **이번 실행의 저장된 노트북 출력에는 missing 목록이 없다.** 값 자체는
bundle의 `decision.json`에 있고 위에 인용했다.

## 확인해 달라는 것

1. P1 관측값 `0b46a411c188…7fe0d3`을 **등록 후보로 인수**할 수 있는가 — 아니면
   P2 통과 전까지 보류인가
2. P2 중단을 **(1) 계약 정정** / **(2) 프로듀서 결함** 중 어느 쪽으로 판정하는가
3. (2)라면 EXP-2026-007을 재실행해야 하는가, 아니면 shard에서 npz를 재구성해
   새 run 폴더에 두는 것으로 충분한가 — 기존 등록 bundle은 어느 쪽이든 건드리지
   않는다
4. bundle이 위 acceptance 절차를 통과하는가

## 하지 않은 것

P3 구현·실행 · `detect_r()` · beat join 재실행 · M0~M4 집계 · DS2 per-beat
label · V10 probability · association·S PR-AUC · 학습 · Drive 파일 이동·삭제·
덮어쓰기 · 관측값 자동 등록 · frozen 모듈 수정 · 12파일 계약 완화.

`status`는 `approved_for_implementation` 유지. `MEASURED`/`PASS`/`COMPLETE`로
올리지 않았다 — 종합 판정이 stop이고 인수는 Codex 몫이다.

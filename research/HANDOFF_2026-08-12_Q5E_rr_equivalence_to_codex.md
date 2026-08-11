# Codex 과제 — PREP_M4_RR_EQUIVALENCE 인수검사 + D1~D4 결정 (설계만, 실행 금지)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: draft` · `design_owner: codex` · `implementation_owner: claude`)
근거: 위 명세 Decision log 의 2026-08-12 `RR_VALUE_IDENTICAL_44_OF_44` 항목
(PR #106, main `dbee048` 에 병합됨)

승인 체인상 위치: **step 4 — "Codex accepts that result; the user approves the
completed design and `status` becomes `approved_for_implementation`."**

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md
   - Frozen M4 identity constants
   - PREP_M4_RR_EQUIVALENCE
   - M4.0 조건 1~3
   - Dual-attestation identity standard
   - Approval boundary / Implementation checklist
   - Decision log 의 2026-08-11 PREP_M4_ASSET_FREEZE_PASS 와
     2026-08-12 RR_VALUE_IDENTICAL_44_OF_44 두 항목
3. research/ASSETS.md 의 cache-v9-mitdb · cache-v10-mitdb (2026-08-12 갱신됨)
4. research/HANDOFF_2026-08-12_Q5E_rr_equivalence_to_codex.md  ← 이번 지시서
5. mit-bih/q5d_order_preserving_beat_join.py 의 hash_file_set() ·
   cache_expected_files() · load_cache_sequences() — 읽기 전용, 수정 금지

[상황]
사용자 승인 아래 읽기 전용 PREP_M4_RR_EQUIVALENCE 를 수행했고 PR #106 이 main 에
병합됐다(dbee048). 판정은 RR_VALUE_IDENTICAL_44_OF_44 이고 status 는 draft 그대로다.
detect_r 미실행 · beat join 미재실행 · M0~M4 집계 0 · 구현 0 · Drive 쓰기 0 ·
y/DS2 label/V10 확률 미열람이다.

Gate 1 (배열 읽기 전 재검증):
  V9  45/45 · missing 0 · extra 0 · 167,064,378 B · 25cd7952… = 등록 상수
  V10 45/45 · missing 0 · extra 0 · 167,868,618 B · 82b9a593… = 등록 상수
Gate 2 (rr 값 비교, 44 record):
  record 집합 동일 · 전부 (n,7) float32 · n == meta_n == ledger cache_n ·
  값 동일 44/44 · first_mismatch null ·
  DS1 50,551 / DS2 49,289 / total 99,840 재현.
등록 기준보다 강한 관측 2건(판정 근거로는 사용하지 않음):
  (i) 44 record 전부 rr 배열이 바이트 수준까지 동일
  (ii) 양 계보 rr 에 NaN 0 → paired-NaN 절 미발화, endpoint 표식이 literal 0.0

[과제]
이 preflight 를 인수검사하고 아래 D1~D4 를 결정하라. 설계 판단만 한다.
구현·실행·집계는 하지 않는다.

──────────────────────────────────────────────────────────────────────
D1 — PREP_M4_RR_EQUIVALENCE 결과를 수용하는가
──────────────────────────────────────────────────────────────────────
확인할 것:
1) dual-attestation 표준 준수 여부. 커넥터 재열거는 2026-08-12 에 새로 수행했고
   2026-08-11 목록을 승계하지 않았다. 45/45 byte crosswalk(양 캐시 90/90),
   aggregate 2건 독립 재계산 일치. 이 절차가 표준이 요구한 항목을 전부
   충족하는지 판정하라.
2) aggregate 일치를 per-file digest 무변경의 증명으로 삼은 논증의 타당성.
   aggregate 는 모든 (name, bytes, sha256) 삼중항의 canonical fold 이므로
   등록 상수와 같으면 90개 per-file digest 가 freeze manifest 이후 무변경이다 —
   이 추론을 수용하는지, 아니면 per-file 재나열을 요구하는지 밝혀라.
3) 비교 규칙 준수. (a==b) | (isnan(a)&isnan(b)) 정확 일치만 사용했고
   tolerance·반올림·평균·보정·계보 선택은 없었다.

──────────────────────────────────────────────────────────────────────
D2 — 값 수준 증거를 명세 본문으로 승격할 것인가
──────────────────────────────────────────────────────────────────────
현재 이 결과는 Decision log 와 ASSETS.md 에만 있다. 그런데 M4.0 조건 1 의 전제
("두 계보가 같은 행 집합")와 §"What the canonical bundle does and does not
contain" 의 add-on 서술은 지금까지 개수·구조 근거만 인용한다.
→ 값 수준 등가(99,840행 비트 동일)를 본문 어디에, 어떤 문장으로 올릴지 지정하라.
→ 그리고 이 사실이 V9 cache 의 역할 규정("corroborating rebuild")을 바꾸는지도
   정하라. 여전히 보강 증거인가, 아니면 더 강한 지위를 갖는가.

──────────────────────────────────────────────────────────────────────
D3 — M4.0 조건 2를 어떻게 할 것인가  [유일하게 남은 관문]
──────────────────────────────────────────────────────────────────────
두 preflight 가 모두 통과해 조건 1(소스 식별·고정)과 조건 3(identity 일치)은
닫혔다. 조건 2(detector peak 위치를 결정론적으로 획득)만 남았고, 이것이 지금
approved_for_implementation 을 막는 유일한 항목이다.

새로 고려할 사실 하나가 생겼다. 아래 §3 에 근거를 적었다.

  V9 캐시와 V10 캐시는 서로 다른 시각의 독립 재빌드다
  (V9 2026-07-18T08:11–08:12Z, V10 11:52–11:55Z, 사이에 rmtree + prepare 재실행).
  그런데 44 record 99,840행의 rr 이 비트 단위로 같다.
  rr 은 rr_features(peaks) 를 전체 matched-peak 배열에 적용한 뒤 idx 로 고른
  값이므로, 이 동일성은 두 실행의 peak 배열이 같은 연속 차분을 낳았음을 뜻한다.
  즉 같은 등록 환경 안에서 detect_r() 가 재현됐다는 실측 증거다.

  다만 한계가 있다. rr 은 peak 위치의 차분에서 나오므로, 전 record 가 상수만큼
  평행이동한 peak 배열도 같은 rr 을 낸다. 보존된 record별 개수와 ±150 경계컷
  결과가 그런 평행이동을 사실상 배제하지만, 절대 위치 동일성이 형식적으로
  증명된 것은 아니다. 과대해석하지 마라.

선택지:
  (a) 조건 2 를 그대로 둔다. 구현 승인은 내주고, 조건 2 는 실행 단계에서
      등록 runtime 을 핀해 DS1 22 record 개수를 재현하는 것으로 평가한다.
      실패하면 M4 = DIAGNOSTIC_INPUT_ABSENT.
  (b) 구현 승인 전에 runtime-pin 실현가능성 probe 를 하나 더 요구한다
      (numpy 2.5.1 / scipy 1.18.0 / wfdb 4.3.1 이 Colab 에 실제로 서는지만
      확인하고 detect_r 은 돌리지 않는, 또는 1 record 만 돌리는 최소 probe).
  (c) 위 재현 증거를 근거로 조건 2 의 표현을 조정한다. 단 "두 과거 실행이
      서로 재현됐다"와 "지금 그 환경을 다시 세울 수 있다"는 서로 다른 주장이고,
      조건 2 는 후자를 묻는다는 점을 반드시 유지하라.
  (d) 다른 안.

(b) 를 고를 경우 그것이 네 번째 preflight 가 되어 승인 체인이 한 단계 늘어난다.
그 비용을 감수할 가치가 있는지도 함께 판단하라.

──────────────────────────────────────────────────────────────────────
D4 — approved_for_implementation 앞에 남은 항목 감사
──────────────────────────────────────────────────────────────────────
Implementation checklist 를 처음부터 훑어, 구현 승인 전에 닫혀야 하는데 아직
열려 있는 항목이 D3 말고 더 있는지 확인하라. 특히:
- Q1~Q5 결정이 본문 전체에 반영됐는지(특히 mamba_record_row primary 가
  M0.4 · M2 · M4.1 · 판정 flag · result schema 까지 일관되게 반영됐는지)
- frozen constants 와 Decision log 사이에 어긋난 수치가 없는지
- decision tree 가 여전히 mutually exhaustive 한지
없으면 "없음"이라고 명시하라. 있으면 그것까지 이번 PR 에서 닫아라.

[바꾸지 말 것]
- 고정 질문, 언어 경계(연관 기전까지 — "원인" 금지)
- H1~H4 대등 등록, NO_EDGE 와 NOT_OPTIMAL 분리
- 이미 확정된 Q1~Q5 결정과 A~E 결정
- 이미 측정된 동결값과 이번 판정
  (4개 aggregate · 104개 per-file SHA-256 · 44/44 shape/meta · 44/44 rr 값 동일)
- W = 15, d_inf 정의, 보고 구간, censoring 규칙
- 10,000 replicate, permutation p 공식, Holm 4-family, effect-size gate 병행
- mutually exhaustive decision tree 와 NO_REGISTERED_MECHANISM_ASSOCIATED 분기
- QA 재현 목표와 중단 규칙
필요한 변경은 Decision log 에 사유와 함께 남겨라.

[절대 하지 말 것]
- M0 를 포함한 어떤 집계도 실행하는 것
- detect_r() 실행, beat join 재실행
- tolerance 확대·새 tolerance 선택, join 규칙 변경
- DS2 per-beat label · V10 probability · association · S PR-AUC · 학습
- 기존 Drive 산출물·run bundle·null shard 수정
- mit-bih/q5d_order_preserving_beat_join.py 수정
- status 를 스스로 approved_for_implementation 으로 올리는 것
  (그 승격은 사용자 승인 사항이다 — 네가 하는 것은 수용 판정과 명세 정리다)

[산출 형식]
- 최신 main(dbee048)에서 시작해 브랜치 codex/<task> 로 작업한다.
  claude/ namespace 를 쓰지 않는다.
- 인수검사 결과와 D1~D4 결정을 명세 Decision log 에 남긴다.
- 결정에 따라 명세 본문(M4.0 조건 2, frozen constants 주변, add-on 서술,
  checklist)을 개정한다. 필요하면 research/ASSETS.md 도 함께.
- status 는 draft 로 둔 채 PR 을 올리고 사용자 승인을 기다린다.
- 커밋 전 CLAUDE.md 의 필수 순서를 따른다
  (git fetch origin main && git merge origin/main → indexer --check → indexer).

[승인 경계]
[1] 네가 RR 결과 인수검사 + D1~D4 결정 + 명세 정리   ← 지금
[2] 사용자 승인 → status: approved_for_implementation
[3] Claude Code 구현 (실행하지 않음)
[4] M0~M4 실행에 대한 별도 사용자 승인
[5] 실행 → 새 timestamped Drive bundle → 노트북 커밋 → ingest
PREP 통과는 [2] 도 [4] 도 아니다. V10 확률과 association 은 계속 봉인이다.
```

---

## 0. 한 줄 요약

`PREP_M4_RR_EQUIVALENCE` 가 **PASS**(`RR_VALUE_IDENTICAL_44_OF_44`)로 끝났고,
두 preflight 가 모두 닫히면서 **M4.0 조건 2 하나만 남았다.** 그리고 이번 결과가
그 조건 2 에 대해 **새로운 (부분) 증거**를 제공한다 — §3 이 그 논증과 한계다.

---

## 1. 측정 결과

### 1.1 Gate 1 — 배열을 읽기 전 캐시 identity 재검증

| cache | Drive ID | files | missing / extra | bytes | aggregate |
|---|---|---|---|---|---|
| V9 | `1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY` | 45/45 | 0 / 0 | 167,064,378 | `25cd7952…` = 등록 상수 |
| V10 | `1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF` | 45/45 | 0 / 0 | 167,868,618 | `82b9a593…` = 등록 상수 |

aggregate 는 **모든** `(name, bytes, sha256)` 삼중항의 canonical fold 이므로,
등록 상수와의 일치가 곧 **90개 per-file digest 가 2026-08-11 freeze manifest
이후 무변경**임을 증명한다.

### 1.2 Gate 2 — `rr` 값 비교

| 검사 | 결과 |
|---|---|
| record 집합 동일 | ✅ |
| shape `(n, 7)` 양쪽 동일 | 44/44 |
| dtype `float32` 양쪽 | 44/44 |
| `n == meta_n == ledger cache_n` | 44/44 |
| **값 동일** | **44/44** |
| `first_mismatch` | `null` |
| split 재현 | DS1 50,551 · DS2 49,289 · total 99,840 |

`allow_pickle=False` 로 열고 `rr` 멤버만 materialise 했으며 `y` 는 인덱싱하지
않았다. 비교는 `(a == b) | (isnan(a) & isnan(b))` 정확 일치뿐이고
tolerance·반올림·평균·보정·계보 선택은 없었다.

### 1.3 등록 기준보다 강한 관측 2건 (판정 근거로는 미사용)

1. **44 record 전부 `rr` 배열이 바이트 수준까지 동일**하다. 등록 판정은 값
   동일에 근거하고, 바이트 동일은 더 강한 관측으로 따로 기록했다.
2. **양 계보 `rr` 에 NaN 이 하나도 없다**(0/0, 44/44). paired-NaN 절이
   발화하지 않았고, endpoint "이웃 없음" 표식이 저장된 literal `0.0` 이라는
   기존 판독(§What the bundle contains 7, Q5)과 일치한다.

---

## 2. 측정 출처 — dual-attestation 준수

| 항목 | 출처 |
|---|---|
| folder ID · expected-set 멤버십 · per-file byte | Claude, 커넥터, **2026-08-12 신규 재열거** |
| per-file SHA-256 · aggregate · `rr` 배열 | 사용자, Colab 마운트 |

표준이 요구한 "매 검증마다 등록 folder ID 를 새로 열거하고 name/size crosswalk 를
반복한다. 과거 목록·mtime·경로를 증거로 물려받지 않는다"를 지켰다 — 2026-08-11
목록을 쓰지 않고 새로 열거했다.

결합 근거: **45/45 byte crosswalk(양 캐시 90/90)** + **aggregate 2건 독립 재계산
일치**.

측정 환경은 Colab `python 3.12.13 / numpy 2.0.2` 로 **등록 runtime 이 아니다**.
SHA-256 과 저장 배열 판독에는 무관하며 runtime 계약이 이미 그렇게 규정한다.

---

## 3. D3 의 새 근거 — 그리고 그 한계

### 3.1 논증

- V9 캐시와 V10 캐시는 **서로 다른 시각의 독립 재빌드**다. V9 mtime
  `2026-07-18T08:11–08:12Z`, V10 `11:52–11:55Z`, 그 사이에 `v10_ECG.ipynb` 셀 20
  `shutil.rmtree('cache')` → 셀 21 `prepare()` 재생성이 있었다
  (`ASSETS.md :: cache-v10-mitdb`).
- 캐시의 `rr` 은 `Fr = rr_features(peaks)` 를 **전체 matched-peak 배열**에 적용한
  뒤 `Fr[idx]` 로 고른 값이다(`EXP-2026-007` Decision log).
- 그 `rr` 이 44 record 99,840행에서 **비트 단위로 같다.**

→ 두 실행의 peak 배열이 **같은 연속 차분**을 낳았다는 뜻이다. 같은 등록 환경
안에서 `detect_r()` 가 **재현됐다는 실측 증거**다. 이는 조건 2 가 전제하는
"detector 가 결정론적일 수 있는가"에 직접 닿는다.

### 3.2 한계 — 과대해석 금지

- `rr` 은 peak 위치의 **차분**에서 나온다. 전 record 가 상수만큼 평행이동한 peak
  배열도 같은 `rr` 을 낸다. 보존된 record별 개수와 `±150` 경계컷 결과가 그런
  평행이동을 사실상 배제하지만, **절대 위치 동일성이 형식적으로 증명된 것은
  아니다.**
- 더 중요한 구분: 이것은 **"두 과거 실행이 서로 재현됐다"**는 증거이지
  **"지금 그 환경을 다시 세울 수 있다"**는 증거가 아니다. **조건 2 는 후자를
  묻는다.** 이 구분을 흐리면 조건 2 를 증거 없이 닫는 것이 된다.

### 3.3 그래서 무엇이 남나

조건 2 의 위험이 "detector 가 애초에 비결정론적이라 재현 자체가 불가능"에서
**"등록 runtime 을 다시 세울 수 있는가"** 로 좁혀졌다. 후자는 순수하게 환경
문제이고, 값싼 probe 로 사전에 확인 가능하다(D3 의 (b) 안).

---

## 4. 승인 체인상 위치

```
[1] PREP_M4_ASSET_FREEZE            ✅ PASS (2026-08-11, PR #102)
[2] Codex A~E 결정                   ✅ 완료 (PR #101 · #105)
[3] PREP_M4_RR_EQUIVALENCE          ✅ PASS (2026-08-12, PR #106)
[4] Codex 인수검사 + D1~D4           ← 지금
[5] 사용자 승인 → approved_for_implementation
[6] Claude 구현 (실행 안 함)
[7] 사용자 실행 승인
[8] M0~M4 실행 → Drive bundle → 노트북 커밋 → ingest
```

M4.0 조건 1·3 은 닫혔고 **조건 2 만 남았다.**

---

## 5. 근거 문서 위치

| 내용 | 파일 |
|---|---|
| 진단 명세 · frozen constants · 두 preflight 결과 | `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md` |
| 캐시 자산 등록·검증 상태 | `research/ASSETS.md` (`cache-v9-mitdb` · `cache-v10-mitdb`) |
| `rr` 이 `rr_features(peaks)[idx]` 라는 계약 | `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` Decision log |
| V10 캐시가 독립 재빌드라는 근거 | `research/ASSETS.md :: cache-v10-mitdb` |
| 선행 인계(PREP 자산 동결 A~E) | `research/HANDOFF_2026-08-11_Q5E_prep_m4_freeze_to_codex.md` |
| digest 규약 `hash_file_set` · `cache_expected_files` | `mit-bih/q5d_order_preserving_beat_join.py` (읽기 전용) |

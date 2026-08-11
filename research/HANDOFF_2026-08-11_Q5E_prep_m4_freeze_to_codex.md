# Codex 과제 — PREP_M4_ASSET_FREEZE 인수검사 + A~E 결정 (설계만, 실행 금지)

작성: 2026-08-11 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: draft` · `design_owner: codex` · `implementation_owner: claude`)
근거: 위 명세 Decision log 의 2026-08-11 `PREP_M4_ASSET_FREEZE_PASS` 항목
(PR #102, main `64c27cd` 에 병합됨)

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md
   특히 §"M4 — detector / source discordance anchors" 의 PREP_M4_ASSET_FREEZE 절과
   M4.0 조건 1~3, 그리고 Decision log 마지막 항목(2026-08-11 PREP_M4_ASSET_FREEZE_PASS)
3. research/ASSETS.md 의 baseline-v9-source · baseline-v10-source ·
   cache-v9-mitdb · cache-v10-mitdb · env-v9v10-runtime (전부 2026-08-11 갱신됨)
4. research/PROVENANCE_2026-08-10_mamba_data_lineage.md (§2 drop 규칙 · §8 R sample 미저장)
5. experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md
   Decision log 의 preflight 절(캐시 aggregate 82b9a593… 이 등록된 곳)
6. mit-bih/q5d_order_preserving_beat_join.py 의 hash_file_set · cache_expected_files
   (읽기 전용. 수정 금지)

[상황]
사용자 승인 아래 읽기 전용 PREP_M4_ASSET_FREEZE 를 수행했고 PR #102 가 main 에
병합됐다(64c27cd). 판정은 PREP_M4_ASSET_FREEZE_PASS 이고 status 는 draft 그대로다.
구현 0 · M0~M4 집계 0 · detector replay 0 · Drive 쓰기 0 · y/DS2 label/V10 확률
미열람이다.

동결된 identity:
  V9  source kinkmap 7 .py  aggregate ffb5679c…  79,329 B
  V10 source kinkmap 7 .py  aggregate 1a0c66c8…  39,761 B
  V9  cache 45파일 tree     25cd7952…  167,064,378 B
  V10 cache 45파일 tree     82b9a593…  167,868,618 B
구조: 두 버전 모두 45/45 · missing 0 · extra 0 · 44/44 에서 rr.shape[0]==meta n ·
rr (n,7) float32 · ledger cache_n/split 44/44 · DS1 50,551 / DS2 49,289 /
total 99,840 · V9-V10 record n 44/44 동일.
파일별 SHA-256 104건 전문은 명세 Decision log 의 freeze manifest 에 있다.

[과제]
이 preflight 를 인수검사하고, 아래 A~E 를 결정하라. 설계 판단만 한다.
구현·실행·집계는 하지 않는다.

──────────────────────────────────────────────────────────────────────
A — 측정 출처가 둘로 나뉜 것을 수용할 것인가  [방법론 쟁점]
──────────────────────────────────────────────────────────────────────
이 컨테이너의 Drive 커넥터는 파일 내용을 모델 컨텍스트로 반환한다. 캐시 두 세트가
334,932,996 B (최소 npz 2,543,011 B) 라 스트리밍이 원리적으로 불가능했고, 1차 시도는
PREP_ENVIRONMENT_BLOCKED 로 저장소 무변경 중단했다. 그래서 측정이 갈렸다:

- Drive file/folder ID · 파일 수 · per-file byte · mtime → Claude 가 커넥터로
- SHA-256 · tree digest · rr shape        → 사용자가 Colab 마운트에서

두 출처를 묶은 근거는 두 가지다.
(1) 캐시 90개 파일의 byte 가 커넥터 목록과 마운트에서 전부 일치(90/90)
    → 등록 Drive ID 가 가리키는 파일과 해시 대상이 같다.
(2) 보고된 aggregate 4건을 hash_file_set 의 canonical-JSON fold 로 재계산해 4/4 일치
    → 붙여넣은 값이 per-file 삼중항과 내적 정합.

판단할 것:
1) 이 결합을 identity 증거로 수용하는가. 수용하지 않는다면 무엇이 추가로 필요한가
   (예: 등록 folder ID 기준 재열거 후 byte 재대조를 매 검증마다 요구).
2) 이 절차를 이후 preflight 의 표준으로 등록할 것인가. 등록한다면 명세의
   §"Runtime and execution-environment contract" 에 어떤 문장으로 넣을지 지정하라.

──────────────────────────────────────────────────────────────────────
B — 잔여 3건을 어떻게 처리할 것인가
──────────────────────────────────────────────────────────────────────
B1. source expected-set 이 glob 이었다.
    Colab 단계가 `*.py` glob 을 hash_file_set 의 expected 로 넘겨, source aggregate 는
    계약이 아니라 스냅샷이었다. glob 은 없는 파일을 못 본다 — 이 명세가 V10 result
    grid 에 대해 이미 거부한 실패 양식이다. 지금은 이름 목록을 사후 등록해 닫았다:
      V9  = {__init__, data, evaluate, frontend, model, train, v15b_local}.py
      V10 = {__init__, data, evaluate, frontend, model, pwave, train}.py
    V9 폴더의 cache_v15b.zip · v11.zip · v12.zip · v13.zip · v13pkg.zip 5개는
    존재만 기록하고 계약 밖에 뒀다.
    → "측정 후 등록"이 유효한 동결인지 판정하라. mitdb_expected_files 를 실측 후
      publisher tree 로 교정한 선례와 같은 성격인지, 아니면 다른지 밝혀라
      (그 선례는 publisher 의 RECORDS 라는 외부 권위가 집합을 정했고, 이번엔
      폴더에 있던 것이 집합을 정했다 — 이 차이가 문제인지 네가 판단하라).
    → zip 5개를 계약에 넣을지도 결정하라.

B2. 규칙→파일 매핑이 승계다.
    detect_r() · tol=int(0.15*fs) · greedy used-set · ±150 경계컷 · AAMI 필터 ·
    rr_features · nan→0.0 endpoint 가 어느 파일에 있는지는 EXP-2026-007 Decision log
    와 ASSETS.md 의 이전 판독에서 가져왔고, 그 판독은 당시 hash 로 고정돼 있지 않았다.
    지금은 바이트가 고정됐다.
    → 이 상태로 M4.0 조건 1 을 "소스 식별 완료"로 볼 것인가, 아니면 동결 hash 대비
      키워드/diff 확인을 별도 선행 단계로 요구할 것인가.

B3. 측정 환경이 등록 runtime 이 아니다.
    동결은 Colab python 3.12.13 / numpy 2.0.2 에서 돌았다. 등록본은
    CPython 3.12.3 / numpy 2.5.1 / scipy 1.18.0 / wfdb 4.3.1 / tensorflow 2.21.0 /
    keras 3.15.0 이다. SHA-256 과 저장된 rr shape 판독에는 무관하고, 등록 runtime 은
    §E 요구대로 identity 에 연결해 기록했다. 그러나 등록 runtime 이 재현 가능하다는
    증거는 아니다.
    → 이 기록으로 PASS gate 의 "runtime identity 가 source/cache 세대와 연결됨"이
      충족됐다고 볼 것인가.

──────────────────────────────────────────────────────────────────────
C — M4 를 유지할 것인가  [가장 중요한 결정]
──────────────────────────────────────────────────────────────────────
M4.0 세 조건의 현재 상태:
  조건 1 (원 detect_r + annotation matching 재생 소스 존재) — 소스 식별·고정됨.
         단 B2 의 매핑 승계 문제가 남아 있다.
  조건 2 (detector peak 위치를 결정론적으로 획득)            — 미충족.
         두 계보 어디에도 peak 위치가 저장돼 있지 않다(load_cache_sequences 는 rr
         블록만 읽고 mamba 는 rpks 미저장). 등록 runtime 에서 detect_r() 를 재실행해
         DS1 22 record 의 등록 개수를 재현해 보여야 하는데, 이번 preflight 는 하지
         않았고 사용 가능한 Colab 런타임은 등록 버전이 아니다.
  조건 3 (source·cache·hash 가 동결 identity 와 일치)        — 이제 충족 가능.

선택지:
  (a) M4 유지 + detector replay 검증을 구현 단계의 선행 관문으로 등록한다.
      numpy 2.5.1 / scipy 1.18.0 / wfdb 4.3.1 핀이 Colab 에서 실제로 서는지가
      관문이고, 서지 않으면 M4 = DIAGNOSTIC_INPUT_ABSENT 로 종결한다.
  (b) M4 를 지금 포기한다. H2·H3 를 "현재 artifact 로 평가 불가"로 확정하고
      진단을 H1·H4 로 닫는다. 이 경우 decision tree 의
      MECHANISM_UNRESOLVED_INPUT_ABSENT 분기를 기본 경로로 재작성해야 한다.
  (c) 다른 안.

(b) 를 고를 경우 Control C 와 H2/H3 관련 절 전체가 정리 대상이라는 점을 유의하라.

──────────────────────────────────────────────────────────────────────
D — 동결 상수를 명세 본문으로 승격할 것인가
──────────────────────────────────────────────────────────────────────
현재 네 digest 는 Decision log 와 ASSETS.md 에만 있다. M4.0 조건 3 이 "동결
identity 와 같을 것"을 요구하므로, 그 identity 가 명세 본문의 frozen constants
로 올라가야 구현이 상수로 참조할 수 있다.
→ 승격 여부와 위치를 지정하라. 승격한다면 어느 digest 가 M4 입력 계약이고 어느
  것이 보강 증거인지도 구분하라. 참고로 Leg 2 는 V10 positional row 만 소비하므로
  V9 cache 는 입력이 아니라 독립 재빌드 증거일 가능성이 높다. V9 source 도
  v15b_local.py 를 포함하는데 그건 mamba(Leg 1) 생산자이지 V9/V10 캐시 생산자가
  아니다. frontend.py 는 V9/V10 바이트 동일이라 어느 쪽을 참조해도 같다.

──────────────────────────────────────────────────────────────────────
E — 추가 측정 제안 하나 (승인 필요, 아직 하지 않았다)
──────────────────────────────────────────────────────────────────────
"V10 은 V9 에 pw 를 더한 순수 add-on 이고 행을 더하거나 빼지 않는다"는 계보 주장의
현재 근거는 (i) meta.json 이 두 버전에서 바이트 동일, (ii) 44/44 record 의 rr.shape
일치, (iii) npz member 가 pw 하나만 차이, (iv) frontend.py 바이트 동일이다.
전부 개수·구조 수준이고 값 수준이 아니다.

제안: 44 record 전부에서 V9 의 rr 배열과 V10 의 rr 배열이 값까지 동일한지 비교한다.
동일하면 행 선택이 개수가 아니라 값 수준에서 같음이 확정되고, M4.0 조건 1 의
"두 계보가 같은 행 집합"이라는 전제가 훨씬 단단해진다. 다르면 그 자체가 중대한
발견이다.

주의: 이번 PREP 의 허용 열람은 rr 의 shape·dtype 까지였다. rr 의 **값** 비교는
허용 범위 밖이므로 하지 않았다. y · DS2 label · 확률은 어차피 봉인이고 이 비교는
그것들을 건드리지 않는다.
→ 이 비교를 승인할지, 승인한다면 별도 preflight 로 할지 M4 구현에 포함할지 정하라.

──────────────────────────────────────────────────────────────────────

[바꾸지 말 것]
- 고정 질문, 언어 경계(연관 기전까지 — "원인" 금지)
- H1~H4 대등 등록, NO_EDGE 와 NOT_OPTIMAL 분리
- mamba_record_row primary / raw_atr_ordinal non-decisional sensitivity (Q1 결정)
- W = 15, d_inf 정의, 보고 구간, censoring 규칙
- 10,000 replicate, permutation p 공식, Holm, effect-size gate 병행
- mutually exhaustive decision tree 와 NO_REGISTERED_MECHANISM_ASSOCIATED 분기
- QA 재현 목표와 중단 규칙
- 이미 측정된 동결값(4개 aggregate · 104개 per-file SHA-256 · 44/44 결과)
필요한 변경은 Decision log 에 사유와 함께 남겨라.

[절대 하지 말 것]
- M0 를 포함한 어떤 집계도 실행하는 것
- detect_r() 실행, beat join 재실행
- tolerance 확대·새 tolerance 선택, join 규칙 변경
- DS2 per-beat label · V10 probability · association · S PR-AUC · 학습
- 기존 Drive 산출물 수정·이동·삭제, null shard 수정
- mit-bih/q5d_order_preserving_beat_join.py 수정
- status 를 스스로 approved_for_implementation 으로 올리는 것

[산출 형식]
- 최신 main(64c27cd)에서 시작해 브랜치 codex/<task> 에서 작업한다.
  claude/ namespace 를 쓰지 않는다.
- 인수검사 결과를 명세 Decision log 에 남긴다: PREP 를 수용하는지, A~E 각각의
  결정과 사유, 그리고 다음 단계.
- 결정에 따라 명세 본문(M4.0 조건, decision tree, frozen constants, runtime 계약)을
  개정한다. 필요하면 research/ASSETS.md 도 함께.
- status 는 draft 로 둔 채 PR 을 올리고 사용자 승인을 기다린다.
- 커밋 전 CLAUDE.md 의 필수 순서를 따른다
  (git fetch origin main && git merge origin/main → indexer --check → indexer).

[승인 경계]
[1] 네가 PREP 인수검사 + A~E 결정 + 명세 개정   ← 지금
[2] 사용자 승인 → status: approved_for_implementation
[3] Claude Code 구현 (실행하지 않음)
[4] M0~M4 실행에 대한 별도 사용자 승인
[5] 실행 → 새 timestamped Drive bundle → 노트북 커밋 → ingest
PREP 통과는 [2] 도 [4] 도 아니다. V10 확률과 association 은 계속 봉인이다.
```

---

## 0. 한 줄 요약

`PREP_M4_ASSET_FREEZE` 는 **PASS** 로 끝났고 자산에는 문제가 없었다. 그러나 **M4 를
가로막는 조건은 자산이 아니라 detector peak 부재와 runtime 이었다** — 그 조건은
여전히 미충족이다. Codex 가 A~E 를 결정해야 하고, 그중 **C(M4 유지 여부)만이
진단의 범위를 바꾼다.**

---

## 1. 이번 preflight 가 확정한 것

### 1.1 동결된 identity

| asset | Drive ID | files | bytes | aggregate / tree SHA-256 |
|---|---|---|---|---|
| V9 source `kinkmap/` | `1oYHJi38hir2JqZl9s_SyuSxq3Hxw25sK` | 7 `.py` | 79,329 | `ffb5679cdfd6b9cc5d46a1071f1fac374d0bb428c360d9a2be80edb111bfb296` |
| V10 source `kinkmap/` | `1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX` | 7 `.py` | 39,761 | `1a0c66c8116745bf83f836fd267931b83f0179cc5e62fd1ba5b055ec236452ce` |
| V9 cache | `1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY` | 45 | 167,064,378 | `25cd7952329fc6f04273046c80d5b0d7b3ee74baf10d2dba4036f9ea7f94fbe8` |
| V10 cache | `1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF` | 45 | 167,868,618 | **`82b9a593dcf23fa4ffc60b44c2fe7da02313dfe7d69dfbe64d85c38b4aa78b14`** |

파일별 SHA-256 104건은 명세 Decision log 의 freeze manifest 에 전문 기록돼 있다.
tree digest 만으로는 **무엇이** 바뀌었는지 알 수 없기 때문이다.

### 1.2 구조 검증 — 두 버전 모두

| 검사 | V9 | V10 |
|---|---|---|
| files (`cache_expected_files()` = `meta.json` + 44 npz) | 45/45 | 45/45 |
| missing / unexpected | 0 / 0 | 0 / 0 |
| `rr.shape[0] == meta.json[n]` | **44/44** | **44/44** |
| `rr` dtype / shape | `(n, 7) float32` | `(n, 7) float32` |
| ledger `cache_n`·`split` | 44/44 | 44/44 |
| DS1 / DS2 / total | 50,551 / 49,289 / 99,840 | 50,551 / 49,289 / 99,840 |
| V9 ↔ V10 record `n` | 44/44 동일 | |

### 1.3 부수 소득 세 가지

1. **V10 cache tree digest 가 `EXP-2026-007` canonical DS1_GATE 의 등록 입력
   identity `82b9a593…` 과 동일하다.** 동결한 캐시가 `JOIN_UNRESOLVED` 를 낳은 바로
   그 캐시임이 경로·파일명이 아니라 **바이트로** 확인됐다. V9 digest `25cd7952…` 는
   다른데, Leg 2 가 V10 positional row 를 소비하므로 이게 옳은 결과다.
2. **`frontend.py` 가 V9/V10 바이트 동일**(`d2635e05…`, 8,434 B). `detect_r()`·
   `rr_features()` 생산자가 두 계보에서 **같은 파일**임이 hash 수준에서 확인된다 —
   기존의 "문자열 수준에서 같다"보다 강한 근거다. `data.py` 만 상이(6,972 → 7,744),
   `pwave.py` 는 V10 전용, npz member 도 `pw` 하나만 추가.
3. **`v15b_local.py` Drive 본이 커밋본·PROVENANCE 기록과 바이트 동일**(`cd4320e5…`).
   `PROVENANCE_2026-08-10` 의 "실행본과 바이트 동일한지 확인 수단이 없다" 공백이 이
   경로에서 닫혔다. 단 이 파일은 **mamba(Leg 1) 생산자이지 V9/V10 캐시 생산자가
   아니다.**

### 1.4 봉인 준수

`y` 미열람(NPZ member 는 이름만 나열, `rr` 만 materialise) · DS2 per-beat label
미열람 · V10 probability 미열람 · association 0 · S PR-AUC 0 · 학습 0 ·
detector replay 미수행 · Drive 파일 수정·이동·삭제 0.

---

## 2. A 의 근거 — 측정이 왜 두 출처로 갈렸나

이 컨테이너의 Drive 커넥터는 파일 내용을 **모델 컨텍스트로** 반환한다(`download_
file_content` → base64). 파일시스템으로 내려받는 경로가 없고 bash 에서 Drive 에 붙을
OAuth 토큰도 없다.

산술이 결정적이다:

| 항목 | 값 |
|---|---|
| 캐시 두 세트 합계 | 334,932,996 B |
| base64 환산 | 약 446 MB |
| 가장 작은 npz | 2,543,011 B → base64 약 3.4 MB |

**단일 npz 하나도 컨텍스트에 들어가지 않는다.** 그래서 1차 시도는
`PREP_ENVIRONMENT_BLOCKED` 로 저장소 무변경 중단했고, 해시는 Colab 마운트에서
계산했다.

두 출처를 묶은 것은 주장이 아니라 측정이다:

1. **캐시 90개 파일의 byte 가 커넥터 목록과 마운트에서 전부 일치(90/90)** — 등록
   Drive ID 가 가리키는 파일과 해시 대상이 같은 파일임을 뜻한다.
2. **보고된 aggregate 4건을 `hash_file_set` 의 canonical-JSON fold 로 재계산해
   4/4 일치** — 붙여넣은 값이 per-file 삼중항과 내적으로 정합한다.

`PREP_DIGEST_CONTRACT_UNRESOLVED` 는 발화하지 않았다. 등록 규약
`hash_file_set()` + `cache_expected_files()` 를 그대로 재사용했고 새 알고리즘을
만들지 않았다.

---

## 3. B — 잔여 3건

| | 항목 | 성격 |
|---|---|---|
| **B1** | source expected-set 이 glob 이었다 → 이름 목록을 사후 등록해 닫음 | 절차 유효성 판정 필요 |
| **B2** | 규칙→파일 매핑이 기존 문서에서 승계됨(당시 hash 미고정) | M4.0 조건 1 판정에 영향 |
| **B3** | 측정 환경이 등록 runtime 이 아님(py 3.12.13 / numpy 2.0.2) | PASS gate 해석 필요 |

**B1 이 미묘하다.** `mitdb_expected_files()` 를 실측 후 publisher tree 로 교정한
선례가 있지만, 그때는 **publisher 의 `RECORDS` 라는 외부 권위**가 집합을 정했다.
이번에는 **폴더에 있던 것**이 집합을 정했다. 이 차이가 문제인지 Codex 가 판단해야
한다. V9 폴더의 zip 5개(`cache_v15b`·`v11`·`v12`·`v13`·`v13pkg`)를 계약에 넣을지도
같이 정해야 한다.

**B3 는 판정에 영향이 없어 보이지만 확인이 필요하다.** SHA-256 과 저장된 `rr`
shape 판독은 numpy 버전과 무관하므로 동결 자체는 안전하다. 다만 PASS gate 의
"runtime identity 가 source/cache 세대와 연결됨" 을 **기록으로 충족**된 것으로 볼지
Codex 가 명시해야 한다.

---

## 4. C — 실질 분기점

### M4.0 세 조건의 현재 상태

| 조건 | 상태 | 근거 |
|---|---|---|
| 1. 원 `detect_r` + annotation matching 재생 소스 존재 | **소스 식별·고정됨** | `frontend.py` `d2635e05…` (V9/V10 동일) · `data.py` V10 `20cde66b…` |
| 2. detector peak 위치를 결정론적으로 획득 | **미충족** | 두 계보 어디에도 peak 미저장 |
| 3. source·cache·hash 가 동결 identity 와 일치 | **충족 가능** | §1.1 의 네 digest |

조건 2 가 남는 이유는 자산 결함이 아니다. `load_cache_sequences()` 는 캐시의 `rr`
블록만 읽고, mamba 계보는 `rpks` 를 저장하지 않는다(`PROVENANCE_2026-08-10` §8).
**애초에 저장된 적이 없다.** 따라서 M4 는 등록 runtime 에서 `detect_r()` 를 재실행해
DS1 22 record 의 등록 개수를 재현해 보여야 하고, 이번 preflight 는 그것을 하지
않았으며 가용한 Colab 런타임은 등록 버전이 아니다.

### 선택지

- **(a) M4 유지** — detector replay 검증을 구현 단계의 선행 관문으로 등록한다.
  `numpy 2.5.1` / `scipy 1.18.0` / `wfdb 4.3.1` 핀이 Colab 에서 실제로 서는지가
  관문이고, 서지 않으면 `M4 = DIAGNOSTIC_INPUT_ABSENT` 로 종결한다.
- **(b) M4 포기** — H2·H3 를 "현재 artifact 로 평가 불가"로 확정하고 진단을 H1·H4 로
  닫는다. **Control C 와 H2/H3 관련 절 전체가 정리 대상**이고, decision tree 의
  `MECHANISM_UNRESOLVED_INPUT_ABSENT` 분기를 기본 경로로 재작성해야 한다.
- **(c) 다른 안.**

어느 쪽이든 명세 본문 수술이 따라온다. A·B·D 는 절차 정리에 가깝지만 **C 는 진단의
범위를 정한다.**

---

## 5. D — 무엇이 입력 계약이고 무엇이 보강 증거인가

동결값 네 개가 전부 같은 무게는 아니다. Codex 가 구분해 등록해야 한다.

| digest | 성격(제안 — 판단은 Codex) |
|---|---|
| V10 cache `82b9a593…` | **M4/Leg 2 의 입력 계약.** Leg 2 는 V10 positional row 만 소비한다 |
| V9 cache `25cd7952…` | **보강 증거.** 독립 재빌드가 같은 행 대장을 냈다는 증언 |
| V10 source `1a0c66c8…` | **입력 계약.** `detect_r`·`rr_features` 생산자를 포함 |
| V9 source `ffb5679c…` | **혼합.** `frontend.py` 는 V10 과 바이트 동일이라 중복이고, `v15b_local.py` 는 mamba(Leg 1) 생산자라 성격이 다르다 |

현재 이 네 값은 Decision log 와 `ASSETS.md` 에만 있다. M4.0 조건 3 이 "동결
identity 와 같을 것"을 요구하므로, **구현이 상수로 참조하려면 명세 본문의 frozen
constants 로 올라가야 한다.**

---

## 6. E — 제안했으나 하지 않은 측정

"V10 은 V9 에 `pw` 를 더한 순수 add-on 이고 행을 더하거나 빼지 않는다"는 계보 주장의
현재 근거:

1. `meta.json` 이 두 버전에서 바이트 동일(`ec5efe7b…`, 1,938 B)
2. 44/44 record 의 `rr.shape` 일치
3. npz member 가 `pw` 하나만 차이
4. `frontend.py` 바이트 동일

**전부 개수·구조 수준이고 값 수준이 아니다.**

제안: 44 record 전부에서 V9 의 `rr` 배열과 V10 의 `rr` 배열이 **값까지** 동일한지
비교한다. 동일하면 행 선택이 값 수준에서 같음이 확정되고 M4.0 조건 1 의 "두 계보가
같은 행 집합"이라는 전제가 훨씬 단단해진다. 다르면 그 자체가 중대한 발견이다.

**하지 않은 이유**: 이번 PREP 의 허용 열람은 `rr` 의 shape·dtype 까지였다. 값 비교는
범위 밖이다. `y`·DS2 label·확률은 어차피 봉인이고 이 비교는 그것들을 건드리지 않는다.

---

## 7. 우선순위 제안

1. **C 먼저.** 진단의 범위를 정하므로 나머지 결정의 맥락이 된다.
2. **D 는 C 에 종속.** M4 를 포기하면 M4 입력 계약 구분이 무의미해진다.
3. **A·B 는 병렬 처리 가능.** 절차 유효성 판정이라 C 와 독립이다.
4. **E 는 선택.** 승인하면 M4 유지(a) 쪽 근거가 강해지고, M4 포기(b) 를 택해도
   계보 주장 자체를 굳히는 값은 있다.

---

## 8. 근거 문서 위치

| 내용 | 파일 |
|---|---|
| 진단 명세 · PREP 절 · freeze manifest | `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md` |
| 동결된 자산 등록 | `research/ASSETS.md` (`baseline-v9/v10-source` · `cache-v9/v10-mitdb` · `env-v9v10-runtime`) |
| Q5-D 실측 결과 · 캐시 aggregate `82b9a593…` 등록 | `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` Decision log |
| mamba 계보 · R sample 미저장(§8) | `research/PROVENANCE_2026-08-10_mamba_data_lineage.md` |
| Q1~Q5 미결 인계(선행) | `research/HANDOFF_2026-08-11_Q5E_open_questions_to_codex.md` |
| digest 규약 `hash_file_set` · `cache_expected_files` | `mit-bih/q5d_order_preserving_beat_join.py` (읽기 전용) |

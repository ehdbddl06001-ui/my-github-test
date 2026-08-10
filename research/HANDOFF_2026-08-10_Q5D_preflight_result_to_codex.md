# Codex 과제 — EXP-2026-007 beat-join 명세 개정 2차 (설계만, 실행 금지)

작성: 2026-08-10 · 작성자: Claude Code · 수신: Codex
근거 문서: `research/PREFLIGHT_2026-08-10_drive_asset_intake.md` (특히 §13·§14)
대상 명세: `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md`
(`status: draft` · `design_owner: codex` · `implementation_owner: claude`)

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. research/PROJECT_STATE.md  (EXP-2026-007 절 · DRIVE_ASSET_PREFLIGHT 절)
3. research/HANDOFF_2026-08-10_Q5D_preflight_result_to_codex.md   ← 이번 과제 지시서
4. research/PREFLIGHT_2026-08-10_drive_asset_intake.md  (특히 §13 · §14)
5. research/PROVENANCE_2026-08-10_mamba_data_lineage.md
6. experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md  ← 개정 대상

[과제]
위 join 명세(status: draft, design_owner: codex, implementation_owner: claude)를
개정하라. 설계만 한다. 구현·실행은 하지 않는다.

[왜 개정하는가]
직전 handoff 는 provenance 가 SOURCE_REPLAY_INCOMPLETE(B) 로 끝날 것을 전제로
쓰였다. 실제 판정은 SOURCE_REPLAY_PROVEN(A) 로 나왔다. 전제가 깨졌다.

[개정 항목 5건 — 상세는 지시서 §4]
(1) JOIN_INPUT_ABSENT / B-조건부 조항을 A 기준으로 재정의하라. 삭제가 아니라
    "A 하에서는 무엇이 남아 있어야 중단인가" 로 다시 쓴다.
(2) 두 leg 을 분리해 기술하라. 증거의 성격이 다르다.
    Leg1 (.atr → mamba 행): drop 규칙 3개가 원 .atr 만으로 결정론적 재계산된다.
    Leg2 (mamba 행 ↔ V9/V10 확률 행): 검출기 의존이라 .atr 로 재계산되지 않는다.
                                      대신 캐시가 행을 보존하고 record 경계가 확정됐다.
    실패 양식이 다르므로 gate 를 따로 걸어라.
(3) Leg2 를 record 단위로 재설계하라. 전역 order-preserving 정렬은 DS2 의
    105 / 111 / 222 에서 반드시 어긋난다. 지시서 §3 의 44-record 행 대장으로
    record 경계를 산술로 자르고, 일치 36개와 불일치 8개를 사전 등록으로 분리하라.
(4) "replay" 의 의미를 명시하라. A 는 전처리 계보(행 선택·순서·입력)를 증명한
    것이지 학습 산출 확률의 재현이 아니다 — train.py 가
    keras.utils.enable_op_determinism() 을 호출하지 않아 GPU 학습은 비결정론적이다.
(5) 첫·끝 비트 eligibility 전제를 고쳐라(직전 handoff 이월). 초안의 "the first or
    last beat is ineligible when either pre-RR or post-RR is absent" 는 소스와
    어긋난다 — 첫·끝 비트의 RR 은 없는 것이 아니라 복제된다.

[판단을 너에게 맡긴 것 — 내가 확정하지 않았다]
"v9/v10 행 ⊆ mamba 행" 이 성립할 개연성이 높고, 따라서 행 수가 같은 record 에서는
집합도 같을 가능성이 크다. 그러나 개수 일치가 집합 일치를 함의하지 않는다
(drop 1 + add 1 상쇄 가능). 경계컷 기준도 다르다 — mamba 는 주석 위치 pos 로,
v9/v10 은 검출 위치 p 로 자른다. 이 가설을 채택할지, 채택한다면 어떤 반증 검사를
붙일지는 네가 결정하라.

[반드시 지킬 사실 — 틀리면 설계가 무너진다]
- V9/V10 행 순서 = detect_r() 검출 순서다. .atr ordinal 이 아니다.
- V9/V10 npz 는 prob·y·pid 만 저장한다. row key 가 없다. identity 는 위치뿐이다.
- t 를 join key 로 쓸 수 없다. t = np.cumsum(pre) - pre[0] 이라 record 마다 0에서
  재시작하고 필터링된 RR 누적이라 실제 시각에서 밀린다. 전역 고유성이 없다.
  Q5-A 실측 조인 1.9%(우연 수준)가 이것으로 설명된다.
- mamba 행과 V9/V10 행은 같은 집합이 아니다. 8 record 편차, 전체 -31
  (DS1 -25 / DS2 -6).
- 232 편중: DS2 S beat 1,837 중 record 232 가 1,382(75.2%). parent spec 의
  "no single record contributes >50% of all eligible S beats" gate 와 충돌한다.

[바꾸지 말 것]
과학적 질문 · DS1→DS2 inter-patient split · primary metric(join_min_class_recall) ·
parent primary(S_PR_AUC) · 중단 조건 · 성공 gate 구조 · 단일 사전등록 경로 원칙.
필요한 변경은 임의로 하지 말고 명세의 Decision log 에 사유와 함께 남겨라.

[절대 하지 말 것]
- beat join 실행. 설계만이다. A 조항이 실행에 별도 승인을 요구한다.
- DS2 per-beat class label 열람 · V10 probability 값 열람.
- join 성능을 보고 provenance 경로나 join 규칙을 고르는 것.
- 여러 join 규칙을 돌린 뒤 가장 좋은 것을 고르는 것.
- 모델 학습·재학습.
- Drive 파일 이동·삭제·덮어쓰기.
- status 를 스스로 approved_for_implementation 으로 올리는 것.
- 브랜치 claude/drive-asset-preflight-check-ayt9iy (PR #78) 를 건드리는 것.

[산출 형식]
- 최신 main 에서 시작해 브랜치 codex/<task> 에서 작업한다.
- experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md 를 개정하고
  변경 사유를 Decision log 에 적는다.
- status 는 draft 로 둔 채 PR 을 올리고 사용자 승인을 기다린다.
- 커밋 전 CLAUDE.md 의 필수 순서를 따른다
  (git fetch origin main && git merge origin/main → indexer --check → indexer).

[승인 경계]
[1] 네가 draft 개정  ← 지금
[2] 사용자 승인 → status: approved_for_implementation
[3] Claude Code 가 구현 (implementation_owner: claude, 브랜치 claude/<task>)
[4] beat join 실행에 대한 별도 사용자 승인   ← A 조항이 요구
[5] 실행 → Drive run bundle → 노트북 커밋 → ingest_run.py 로그

[2]와 [4]는 별개의 승인이다. [2]는 "이 설계로 코드를 짜도 된다", [4]는 "그 코드를
실제 데이터에 돌려도 된다" 이다. 명세가 이 둘을 뭉뚱그리지 않게 하라.
V10 확률과 association 분석은 join 이 자체 gate 를 통과하고 그에 대한 별도 승인을
받을 때까지 봉인 상태다.
```

---

## 0. 한 줄 요약

**`DRIVE_ASSET_PREFLIGHT` 판정이 `SOURCE_REPLAY_PROVEN`(A)로 나왔다.** 명세가 예상하던
보수적 결과(B)가 아니다. 그리고 **record별 행 대장이 확보돼** 명세의 미해결 항목 하나가
산술로 닫힌다. 이 두 가지 때문에 draft 를 다시 손봐야 한다.

**여전히 실행은 금지다.** A 조항 자체가 "이 경우에도 beat join 실행은 별도 승인을
받는다"고 규정한다. 이 handoff 는 설계 개정 요청이지 실행 승인이 아니다.

---

## 1. 직전 handoff 이후 무엇이 달라졌나

직전 문서(`HANDOFF_2026-08-10_Q5D_join_spec_revision_to_codex.md`)는 provenance 가
`SOURCE_REPLAY_INCOMPLETE` 로 끝날 것을 전제로 쓰였다. 그 전제가 깨졌다.

| 항목 | 직전 handoff 시점 | 지금 |
|---|---|---|
| V10 소스 | **부재** — `v10pkg` 폴더가 Drive에 없었다 | **확보** `v9~v13/v10pkg/kinkmap/` |
| V10 row lineage | producer-side 증거 없음 | **증명됨** (동일 코드 경로 + 독립 재빌드 캐시 44/44) |
| V9/V10 행 순서 | 검출기 의존이라 재현 불가 | **캐시로 물질화** — 재현할 필요 자체가 없다 |
| 환경 | scipy/numpy 미고정 | **전 패키지 확정** (numpy 2.5.1 · scipy 1.18.0 등) |
| 입력 | 미검증 | publisher SHA-256 검증본과 **9/9 크기 일치** |
| record별 행 수 | 미상 (DS2 −6 만 알려져 있었다) | **44 record 전량 확보** (DS1 −25 신규) |
| 판정 | B 예상 | **A 확정** |

새로 들어온 자산은 `MyDrive/mitbih/v9~v13/`(2026-08-10 08:00 업로드)이고,
`research/ASSETS.md` 에 `baseline-v10-source` · `cache-v9-mitdb` · `cache-v10-mitdb` ·
`run-v9tov13-tree` · `env-v9v10-runtime` · `data-mitdb-v9runtime` 로 등록했다.

---

## 2. 소스로 확정된 사실 — 개정의 재료

### 2.1 V9와 V10은 행 선택 로직이 동일하다

`v10pkg/kinkmap/data.py::build_record()` 의 `detect_r()` 호출, `tol = int(0.15*fs)`,
`used` 집합 greedy 최근접 매칭, 경계컷(`p−150 ≥ 0`, `p+150 ≤ len`), `valid`/`idx`
구성이 v9와 **문자열 수준에서 같다**. v10 이 더한 것은 이것뿐이다:

```python
pw_all = PW.pwave_features(sig, peaks, normal_mask=None, fs=fs)   # (n_all, 5)
...
"pw": pw_all[idx].astype("float32"),
```

**같은 `idx` 를 재사용**하므로 행을 추가·삭제·재정렬하지 않는 순수 add-on 이다.

### 2.2 캐시는 독립 재빌드인데 44/44 일치한다

`v10_ECG.ipynb` 셀 20이 `shutil.rmtree('cache')` 로 캐시를 지우고 셀 21이
`prepare()` 로 다시 만든다. 그런데도 v9 캐시 `meta.json` 과 v10 캐시 `meta.json` 의
44개 record `n`·`split` 이 전부 같다(파일 크기도 1,938 B 동일).

동일 row 집합에 대한 **독립 증언 4개**: v9 캐시 meta · v9 노트북 stdout(셀 18) ·
v10 캐시 meta · v10 노트북 stdout(셀 21 + 셀 23 `DS1: S 944/50551`).

### 2.3 환경 pin (재현용)

```text
python==3.12.3          # CPython, x86_64-linux
tensorflow==2.21.0
keras==3.15.0
numpy==2.5.1
scipy==1.18.0
scikit-learn==1.9.0
wfdb==4.3.1
# GPU: NVIDIA GeForce GTX 1650 Ti with Max-Q Design (CC 7.5) · cuDNN 92400
```

전 패키지 `.dist-info` mtime 이 2026-07-18 10:59–11:00 **단일 트랜잭션**이고 v9 캐시
빌드(08:11Z)보다 앞선다 → numpy/scipy 가 V9·V10 양쪽에 동일 적용됐음이 파일 시각으로
뒷받침된다.

**단, `train.py` 는 `keras.utils.enable_op_determinism()` 을 호출하지 않는다.**
이 환경을 그대로 맞춰도 **GPU 학습 확률은 비트 재현되지 않는다.** A가 보장하는 것은
**전처리 계보(행 선택·순서·입력)** 이지 확률값 재산출이 아니다. 명세가 "replay" 라는
말을 쓸 때 이 구분을 명시해야 한다.

---

## 3. record별 행 대장 — 명세의 `processed row index` 항목이 닫힌다

`v9/v10` 열은 V9·V10 캐시 `meta.json` 의 공통값이고, `mamba` 열은 커밋본
`mit-bih/lineage/cache_v15b_meta.json` 이다. "누적 시작행"은 각 split 안에서
`data.py` 의 DS1/DS2 상수 리스트 순서로 누적한 값 = **V9/V10 확률 배열의 record 시작
인덱스**다.

**DS1** — `v9/v10` 열이 V9·V10 캐시 `meta.json` 공통값(44/44 동일)

| record | v9/v10 `n` | mamba `n` | 차이 | 누적 시작행 (v9/v10) |
|---|---|---|---|---|
| `101` | 1,862 | 1,862 | 0 | 0 |
| `106` | 2,027 | 2,027 | 0 | 1,862 |
| `108` | 1,759 | 1,760 | **-1** | 3,889 |
| `109` | 2,528 | 2,528 | 0 | 5,648 |
| `112` | 2,537 | 2,537 | 0 | 8,176 |
| `114` | 1,875 | 1,875 | 0 | 10,713 |
| `115` | 1,952 | 1,952 | 0 | 12,588 |
| `116` | 2,397 | 2,411 | **-14** | 14,540 |
| `118` | 2,277 | 2,277 | 0 | 16,937 |
| `119` | 1,987 | 1,987 | 0 | 19,214 |
| `122` | 2,474 | 2,474 | 0 | 21,201 |
| `124` | 1,613 | 1,613 | 0 | 23,675 |
| `201` | 1,961 | 1,961 | 0 | 25,288 |
| `203` | 2,972 | 2,974 | **-2** | 27,249 |
| `205` | 2,644 | 2,644 | 0 | 30,221 |
| `207` | 1,859 | 1,859 | 0 | 32,865 |
| `208` | 2,572 | 2,579 | **-7** | 34,724 |
| `209` | 3,004 | 3,004 | 0 | 37,296 |
| `215` | 3,360 | 3,360 | 0 | 40,300 |
| `220` | 2,046 | 2,046 | 0 | 43,660 |
| `223` | 2,590 | 2,591 | **-1** | 45,706 |
| `230` | 2,255 | 2,255 | 0 | 48,296 |
| **합계** | **50,551** | **50,576** | **-25** | |

**DS2** — `v9/v10` 열이 V9·V10 캐시 `meta.json` 공통값(44/44 동일)

| record | v9/v10 `n` | mamba `n` | 차이 | 누적 시작행 (v9/v10) |
|---|---|---|---|---|
| `100` | 2,271 | 2,271 | 0 | 0 |
| `103` | 2,083 | 2,083 | 0 | 2,271 |
| `105` | 2,566 | 2,567 | **-1** | 4,354 |
| `111` | 2,123 | 2,124 | **-1** | 6,920 |
| `113` | 1,794 | 1,794 | 0 | 9,043 |
| `117` | 1,534 | 1,534 | 0 | 10,837 |
| `121` | 1,862 | 1,862 | 0 | 12,371 |
| `123` | 1,517 | 1,517 | 0 | 14,233 |
| `200` | 2,598 | 2,598 | 0 | 15,750 |
| `202` | 2,134 | 2,134 | 0 | 18,348 |
| `210` | 2,638 | 2,638 | 0 | 20,482 |
| `212` | 2,747 | 2,747 | 0 | 23,120 |
| `213` | 2,887 | 2,887 | 0 | 25,867 |
| `214` | 2,257 | 2,257 | 0 | 28,754 |
| `219` | 2,153 | 2,153 | 0 | 31,011 |
| `221` | 2,427 | 2,427 | 0 | 33,164 |
| `222` | 2,477 | 2,481 | **-4** | 35,591 |
| `228` | 2,053 | 2,053 | 0 | 38,068 |
| `231` | 1,570 | 1,570 | 0 | 40,121 |
| `232` | 1,780 | 1,780 | 0 | 41,691 |
| `233` | 3,066 | 3,066 | 0 | 43,471 |
| `234` | 2,752 | 2,752 | 0 | 46,537 |
| **합계** | **49,289** | **49,295** | **-6** | |

**요약**: 36/44 일치 · 불일치 8 (DS1 5개 −25 · DS2 3개 −6) · 전체 99,840 vs 99,871 (−31).
DS2 쪽 `105 −1 · 111 −1 · 222 −4` 는 `ASSETS.md` 기존 기록과 정확히 일치한다.
**DS1 쪽 `108 −1 · 116 −14 · 203 −2 · 208 −7 · 223 −1` 은 이번에 처음 문서화된 값이다.**

기전: mamba 계보(`v15b_local.py`)는 `rpks` 를 `ann.sample` 에서 직접 취하고, v9pkg
계보(`data.py`)는 `detect_r()` 검출 결과를 ±54 sample 안에서 주석에 붙인다. 차이는
**검출기가 매칭하지 못한(또는 경계에서 잘린) 비트**다.

---

## 4. 개정해야 할 것 — 다섯 가지

### (1) `JOIN_INPUT_ABSENT` / B-조건부 조항을 A 기준으로 다시 써라 [반드시]

명세는 provenance-only audit 이 실패하면 `JOIN_INPUT_ABSENT` 로 종결하도록 등록돼
있다. 그 audit 이 요구한 세 항목(동결 소스 · manifest · 저장된 row map)은 이제
**전부 충족된다**. 종결 조항이 발화되지 않는 상태이므로, 조항을 삭제하지 말고
**"A 하에서는 어떤 조건이 남아 있어야 중단인가"** 로 다시 정의하라.

### (2) 두 leg 을 분리해서 기술하라 [구조 변경]

지금 명세는 "raw `.atr` → 등록 processed row" 를 한 덩어리로 다룬다. 실제로는 두
단계이고 **증거의 성격이 서로 다르다**:

- **Leg 1 — `.atr` → mamba 행**: `PROVENANCE_2026-08-10` §2 대로 drop 규칙 3개가
  원 `.atr` 만으로 **결정론적으로 재계산된다**. 검출기가 개입하지 않는다.
- **Leg 2 — mamba 행 ↔ V9/V10 확률 행**: 검출기 의존이라 `.atr` 로 재계산되지
  **않는다**. 대신 **캐시가 행을 보존**하고 있고 record별 경계가 §3 표로 확정된다.

두 leg 의 실패 양식이 다르므로 gate 도 따로 걸어야 한다.

### (3) Leg 2 를 record 단위로 재설계하라 [핵심]

전역 order-preserving 정렬은 record `105`·`111`·`222` 에서 **반드시 어긋난다**(DS2
기준). §3 표가 있으므로 이제 다음이 가능하다:

- record 경계를 **산술로** 잘라낸다(가정이 아니라 `meta.json` 값).
- **36개 일치 record 와 8개 불일치 record 를 사전에 분리**한다. 발견하는 게 아니라
  사전 등록한다.
- 불일치 record 는 `AMBIGUOUS` 로 격리하거나 별도 규칙을 적용한다.

**검토가 필요한 가설(내가 확정하지 않았다)**: v9/v10 필터는 mamba 필터에 검출기
매칭 조건을 하나 더 얹은 것이므로 `v9/v10 행 ⊆ mamba 행` 이 성립할 개연성이 높고,
따라서 **행 수가 같은 record 에서는 집합도 동일**할 가능성이 크다. 다만
**개수 일치가 집합 일치를 함의하지 않는다**(drop 1 + add 1 이 상쇄될 수 있다).
경계 조건도 다르다 — mamba 는 주석 위치 `pos` 로, v9/v10 은 검출 위치 `p` 로 경계컷을
한다. 이 가설을 채택할지, 채택한다면 어떤 반증 검사를 붙일지는 **Codex 가 판단하라.**
나는 근거와 반례 가능성만 제시한다.

### (4) "replay" 의 의미를 명시하라 [용어]

A 판정은 **전처리 계보**를 증명한 것이지 학습 산출 확률의 재현이 아니다(§2.3).
명세가 replay 를 근거로 무언가를 주장할 때 어느 쪽인지 못 박아라.

### (5) 첫·끝 비트 eligibility 전제 [직전 handoff 이월 — 여전히 유효]

직전 handoff 의 (1)번 지적이 그대로 남아 있다. 초안의 *"the first or last beat is
ineligible when either pre-RR or post-RR is absent"* 는 소스와 어긋난다 — 첫·끝
비트의 RR 은 **없는 것이 아니라 복제**된다(`PROVENANCE` §3).

---

## 5. 그대로 유지하라 — 바꾸지 말 것

- 과학적 질문, DS1→DS2 inter-patient split, primary metric(`join_min_class_recall`),
  parent primary(`S_PR_AUC`), 중단 조건, 성공 gate 구조.
- 단일 사전등록 경로 원칙 — **여러 join 규칙을 돌려 best 를 고르지 않는다.**
- `t` 를 join key 로 쓰지 않는다. `t = np.cumsum(pre) - pre[0]` 이라 record 마다
  0에서 재시작하고 필터링된 RR 누적이라 실제 시각에서 밀린다. 전역 고유성이 없다.
  Q5-A 실측 조인 1.9%(우연 수준)가 이것으로 설명된다.
- `232` 편중: DS2 S beat 1,837 중 record `232` 가 **1,382(75.2%)**. parent spec 의
  *"no single record contributes >50% of all eligible S beats"* gate 와 충돌한다.
  eligible 필터 이전 원 분포부터 이 수준이라는 사실은 변하지 않았다.

---

## 6. 절대 하지 말 것

- **beat join 실행.** 설계만이다. A 조항이 별도 승인을 요구한다.
- DS2 per-beat class label 열람 · V10 probability 값 열람.
- join 성능을 보고 provenance 경로나 join 규칙을 선택하는 것.
- 모델 학습·재학습.
- Drive 파일 이동·삭제·덮어쓰기.
- parent spec(`EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md`)의 과학적
  질문·split·지표·중단 조건 변경. 필요한 변경은 **Decision log** 에 남긴다.

---

## 7. 산출 형식

- 브랜치 `codex/<task>` 에서 작업한다. `claude/drive-asset-preflight-check-ayt9iy`
  (PR #78)를 건드리지 않는다.
- `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` 를 개정하고
  변경 사유를 **Decision log** 에 적는다.
- `status` 는 **Codex 가 스스로 올리지 않는다.** 개정 후 `draft` 로 두고 사용자 승인을
  기다린다.

---

## 8. 승인 경계 — 실행까지 남은 관문

```
[지금] preflight A 확정 (PR #78)
   ↓
[1] Codex 가 draft 개정  ← 이 handoff
   ↓
[2] 사용자 검토 → status: approved_for_implementation 승인
   ↓
[3] Claude Code 가 구현 (implementation_owner: claude, 브랜치 claude/<task>)
   ↓
[4] beat join 실행에 대한 별도 사용자 승인  ← A 조항이 요구
   ↓
[5] 실행 → Drive run bundle → 노트북 커밋 → ingest_run.py 로그
```

**[2]와 [4]는 별개의 승인이다.** [2]는 "이 설계로 코드를 짜도 된다"이고, [4]는
"그 코드를 실제 데이터에 돌려도 된다"이다. 명세가 이 둘을 뭉뚱그리지 않게 하라.

V10 확률과 association 분석은 **join 이 자체 gate 를 통과하고 그에 대한 별도 승인을
받을 때까지 봉인 상태**다.

---

## 9. 참고 — 근거 문서 위치

| 내용 | 위치 |
|---|---|
| preflight 전문 (자산 표·판정 근거) | `research/PREFLIGHT_2026-08-10_drive_asset_intake.md` |
| 2차 인수 (V10 소스·캐시·행 대장) | 위 문서 §13 |
| 3차 인수 (환경·입력·A 판정 조건 대조) | 위 문서 §14 |
| mamba 전처리 계보 (Leg 1 근거) | `research/PROVENANCE_2026-08-10_mamba_data_lineage.md` |
| 자산 등록 (Drive ID·크기·producer) | `research/ASSETS.md` |
| 프로젝트 상태 | `research/PROJECT_STATE.md` |
| 직전 handoff (이월 항목 (5)) | `research/HANDOFF_2026-08-10_Q5D_join_spec_revision_to_codex.md` |

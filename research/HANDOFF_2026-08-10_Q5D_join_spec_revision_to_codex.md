# Codex 과제 — EXP-2026-007 beat-join 명세 개정 (설계만, 실행 금지)

이 문서 전체가 Codex에게 주는 프롬프트다. 「프롬프트 본문」만 잘라 써도 된다.

- 요청 주체: 사용자 · 작성: Claude Code · 날짜 2026-08-10
- 대상 문서: `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md`
  (`status: draft` · `design_owner: codex` · `implementation_owner: claude`)
- 선행 문서: `research/PROVENANCE_2026-08-10_mamba_data_lineage.md` (이번에 신규)
- 산출물은 **개정된 설계 문서 하나**다. 코드도, 실행도, 데이터 열람도 하지 않는다.

---

## 프롬프트 본문

### 무엇이 달라졌나

네가 설계한 beat-join 명세는 그대로 등록됐다(`main`, PR #75). 그 명세의 첫 구현
gate는 **provenance-only audit**이고, 통과하지 못하면 `JOIN_INPUT_ABSENT`로
종결하도록 돼 있었다. 네가 「Missing or unverified at design time」에 적어 둔 네
항목이 그 대상이었다:

- processed-row `beat_uid`
- record 내부 시간순 보존 계약
- per-beat keep/drop 대장
- 저장된 row-permutation map

**그 audit을 문서로 수행했고, 전처리 원본 3계층을 전부 확보했다.** 결과는
`research/PROVENANCE_2026-08-10_mamba_data_lineage.md`에 소스 인용과 함께 있고,
소스 자체도 repo에 고정했다:

- `mit-bih/lineage/v15b_local.py` — ① 비트 추출(`build_cache`)
- `mit-bih/lineage/build_penult.py` — ② 특징 조립
- `mit-bih/lineage/make_colab_data.py` — ③ 단일 파일화
- `mit-bih/lineage/cache_v15b_meta.json` — 캐시 메타(record별 `n`/`nS`/`nV`)

**이 문서들을 먼저 읽어라.** 아래는 요약이고, 판단 근거는 그 문서의 소스 인용이다.

### 소스로 확정된 다섯 가지

1. **record 내부 행 순서 = `.atr` ordinal 순서**, 시간순·엄격 단조
   (`v15b_local.py:101-102`). 재정렬·permutation 없음.
2. **keep/drop 규칙은 세 조건이 전부**이고 원 `.atr`만으로 재계산된다
   (`:102`, `:104`): AAMI 심볼 필터(**F·Q 탈락** — 결손 818박의 정체) ·
   record 양 끝 **150 sample** · 유효비트 5개 미만 record 제외.
3. **저장 RR은 beat filtering 이후에 계산된 초 단위 값**이고,
   **첫 비트 pre-RR·마지막 비트 post-RR은 없는 것이 아니라 복제**된다
   (`:107-109`). `rr[:,0]=pre`, `rr[:,1]=post`.
4. **penult 행과 cache 행은 구성상 정렬돼 있다.** `build_penult.py`와
   `make_colab_data.py`가 **같은 `sorted(glob("*.npz"))`** 열거를 쓴다.
   전역 행 순서 = `sorted(record id 문자열)` × record 내부 시간순.
5. **`t`는 주석 sample index가 아니다.** `t = np.cumsum(pre_rr) - pre[0]`,
   즉 record 첫 비트부터의 누적 경과 시간(초)을 **복원한 값**이다.
   → Q5-A의 조인 1.9%(우연 수준)가 이것으로 완전히 설명된다.

또한 **R sample(`rpks`)은 npz에 저장되지 않는다** → 저장된 `beat_uid`는 없다.
다만 2번에 따라 **재계산은 가능**하다.

### 개정해야 할 것 — 네 가지

#### (1) 첫·끝 비트 eligibility 전제가 소스와 어긋난다 [반드시 수정]

현재 명세:

> the first or last beat is ineligible when either pre-RR or post-RR is absent

**실제로는 없지 않고 복제된 값이다.** 따라서 이 조항은 발화하지 않으며, 첫·끝
비트에서 processed RR은 raw에서 같은 방식으로 재현하지 않으면 어긋난다.
`±1 sample` 후보 간선 규칙이 이 두 비트에서 어떻게 동작해야 하는지 다시 써라.
"raw 쪽에서도 동일하게 복제한다"인지, "첫·끝 비트를 후보에서 제외한다"인지
**하나로 고정**하고, 그 선택이 coverage gate(전체 0.95 등)에 미치는 영향을 적어라.

#### (2) replay 경로를 검토하라 [분기 판단 필요]

drop 규칙이 결정론적이므로, 이 조인은 근사 매칭이 아니라 **전처리 재생**으로
성립할 여지가 있다: 원 `.atr`에 세 조건을 그대로 적용해 `rpks`를 재구성하고,
`sorted(glob)` 순서로 이어붙이면 processed 행과 **일대일 대응이 구성적으로**
나온다. 이 경로에서는 `±1 sample` 후보 간선·최대 카디널리티 단조 매칭·
`AMBIGUOUS` 개념이 필요 없어진다.

**다만 이건 내 제안이지 판정이 아니다.** 네가 판단할 것:

- replay를 **primary**로 올릴지, RR 매칭을 primary로 두고 replay를 검증
  수단으로 쓸지, 아니면 replay를 거부할지.
- replay를 채택한다면 **무엇이 이 규칙을 반증하는가**. 현 명세의 음성대조군
  3종(wrong-record · order shuffle · circular shift)은 RR 매칭을 겨냥해 설계됐다.
  replay에는 그대로 맞지 않을 수 있다 — 재생된 `rpks` 개수가 `meta.json`의
  record별 `n`과 불일치하는지, y 벡터가 재생 라벨과 불일치하는지 같은
  **결정론적 falsifier**로 갈아야 할 수 있다. 통과만 가능한 gate는 gate가 아니라는
  원칙은 그대로다.
- replay가 실패하면 어떤 판정 코드로 가는지(`JOIN_RULE_FALSIFIED`인지 새 코드인지).

#### (3) `JOIN_INPUT_ABSENT` 조항을 현실에 맞게 다시 써라

네 명세는 네 아티팩트가 없으면 `JOIN_INPUT_ABSENT`로 종결하라고 했다. 지금 상태는:

| 항목 | 상태 |
|---|---|
| 시간순 보존 계약 | **소스로 증명됨** |
| per-beat keep/drop 대장 | 저장본 없음, **결정론적 재계산 가능** |
| row-permutation map | 불필요(§4의 열거 동일성으로 대체) |
| `beat_uid` | **저장본 없음** (R sample 미저장) |

즉 "없으니 중단"이 아니라 "저장돼 있지 않지만 유도된다"가 정확하다. 조항을
그대로 두면 규칙상 즉시 중단해야 하는데, 그건 사실과 맞지 않는다. **어떤 조건에서
여전히 `JOIN_INPUT_ABSENT`인지** 다시 정의하라. 또한 명세의 「If the join is
impossible in principle」의 ledger 요구(`beat_uid = SHA256(...)`)는 **미래 실험을
위한 권고로는 유지하되**, 현 조인의 차단 조건에서는 분리하는 편이 맞아 보인다.

#### (4) `meta.json`으로 새로 가능해진 것을 반영하라

record별 `n`과 `sorted(glob)` 순서로 **`mamba_data.npz`의 record별 행 구간이
파일을 열지 않고 산술로 결정된다.** 명세의 ledger 항목 중 `processed row index`가
유도 가능해진다. 이걸 provenance gate의 **사전 검산**으로 넣을지 판단하라
(예: 재생된 record별 비트 수 == `meta.json`의 `n`, 전체 합 == 99,871).

### 참고 숫자 (검증 완료)

- 44 records · 총 99,871 beats · `y` 분포 `{0: 90082, 1: 2781, 2: 7008}`
- DS1 22 records 50,576 beats (S 944) · DS2 22 records 49,295 beats (S 1,837)
- DS2 총 beat가 V9/V10 패키지의 49,289와 6 차이 나는데, `ASSETS.md`에 기록된
  `105·111·222 N beat −1/−1/−4`와 정확히 맞는다.
- **record `232` 혼자 DS2 S beat의 75.2%(1,382/1,837)** 다. parent spec의 성공
  gate에 *"no single record contributes >50% of all eligible S beats"* 가 있는데
  **eligible 필터 이전 원 분포부터 이 수준**이다. 조인 명세에서 결정할 사항은
  아니지만, 개정 시 이 사실을 어디에 기록할지 정해라.

### 바뀌지 않은 것 — 그대로 유지하라

- `status: draft`. 사용자 승인 전까지 `approved_for_implementation` 금지.
- `design_owner: codex` · `implementation_owner: claude`.
- **EXP-2026-007의 과학적 판정은 여전히 `NOT RUN`.** measurement qualification
  통과(`MEASUREMENT_QUALIFIED`, canonical run `20260810T005802`, 5/5, per-record
  floor 정확히 5/6)는 **조인이나 association의 승인이 아니다.**
- record `222` 주석밀도 미결 조항과 record `231` 측정품질 교란 조항
  (`P_VALID` · `QUALITY_SHAM` · `MEASUREMENT_QUALITY_CONFOUNDED`),
  leave-one-record-out을 두 record 중 유리한 쪽 고르기로 쓰지 않는다는 경계.
- 선택 편향 gate(클래스·record 커버리지, 균형, `S_share_inflation ≤ 1.25`)와
  `JOIN_UNRESOLVED`가 정식 결과라는 원칙.
- 완화 규칙은 자기 영가설을 다시 돌리고 `maxT`로 비교한다는 원칙.
- `PR_discordance` 임계값 `2.000`의 경계 처리는 parent spec에서 따로 고정하며
  이 조인 명세에서 결정하지 않는다.

### 절대 하지 말 것

- 코드 작성·실행, 데이터 다운로드, Colab 실행
- DS1·DS2 데이터 열람, DS2 class label 열람, **V10 확률 열람**
- S PR-AUC·association 계산, qualification 재실행
- Google Drive 변경, 기존 자산 이동·덮어쓰기
- parent spec을 `MEASURED`로 변경, 새 실험 결과 주장
- `mit-bih/q5d_qualify_*` · `notebooks/quest53_*` · `research/PLAN_2026-08-10_*` 수정
- `research/PROVENANCE_2026-08-10_mamba_data_lineage.md`와
  `mit-bih/lineage/*` 수정 — 이건 인수 기록이다

### 산출 형식

`experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` **한 파일만**
개정한다. 브랜치는 `codex/<task>`.

Decision log에 이번 개정을 날짜와 함께 남기되, **어떤 과학적 질문·split·지표·중단
조건을 왜 바꿨는지** 명시하라. 소스 확보로 사실이 바뀐 항목((1)(3))과 네가 설계
판단으로 바꾼 항목((2)(4))을 구분해서 적어라.

### 승인 경계

이 개정이 나와도 **조인 실행은 자동으로 시작되지 않는다.** 설계 검토 + 사용자
별도 승인이 있어야 하고, 그때 비로소 `implementation_owner: claude`가 구현에
착수한다.

# Codex 과제 — EXP-2026-008 미결 설계 5건 결정 (설계만, 실행 금지)

작성: 2026-08-11 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: draft` · `design_owner: codex` · `implementation_owner: claude`)
근거: 위 명세 §「Open design questions for Codex」와 Decision log 2건 (PR #99, 병합됨)

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md  ← 이번 대상
   특히 §"Open design questions for Codex" 와 Decision log 2건
3. experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md
   Decision log 마지막 절(2026-08-11 corrected DS1_GATE 실측)
4. research/HANDOFF_2026-08-11_Q5D_v_class_join_failure_to_codex.md
5. research/PROVENANCE_2026-08-10_mamba_data_lineage.md  (§2 drop 규칙, §8 R sample 미저장)
6. research/ASSETS.md  (baseline-v9-source · baseline-v10-source · cache-v9/v10-mitdb)
7. mit-bih/q5d_order_preserving_beat_join.py  (읽기만. 이 파일은 수정 대상이 아니다)

[상황]
네가 확정한 Q5-E 진단 설계를 Claude Code 가 EXP-2026-008 로 전사해 main 에 병합했다.
status 는 draft 다. 전사 과정에서 과학 규칙(질문·가설·창 크기·분모·통계·게이트·중단
규칙)은 하나도 바뀌지 않았다.

전사 후 Claude 가 Q5-D 구현을 읽고 대조하는 과정에서, 등록된 정의가 산출물의 실제
성질과 만나 "측정의 의미"가 달라지는 지점 5건이 나왔다. Claude 는 이것을 판단하지 않고
명세 §"Open design questions for Codex" 에 미결로 올렸다. 네가 결정해야 한다.

[과제]
Q1~Q5 를 각각 채택·수정·기각하고, 그 결정을 EXP-2026-008 명세에 반영하라.
설계만 한다. 구현·실행은 하지 않는다.

──────────────────────────────────────────────────────────────────────
Q1 — raw_atr_ordinal 인접이 run 을 record 의존적으로 쪼갠다  [실질 쟁점]
──────────────────────────────────────────────────────────────────────
사실(코드로 확인됨):
- q5d_order_preserving_beat_join.py :: replay_leg1_record() 는
  `for ordinal, (pos, symbol) in enumerate(annotations)` 로 **전체 .atr 주석**에
  번호를 매긴다. AAMI 미포함(F·Q)과 경계 드롭 비트도 ordinal 을 소비하고 빠진다.
- 따라서 "처리 시퀀스에서 이웃한 두 비트"가 연속한 raw_atr_ordinal 을 갖는 것은
  그 사이에 드롭된 주석이 없을 때뿐이다.
- 드롭 대장은 818박 = N 1 · S 0 · V 0 · F 802 · Q 15 이고, 그 92% 가
  record 208 과 213 에 몰려 있다(213 은 DS2, 208 은 DS1).

결과:
- M0.4 · M2 의 run 정의는 "정확히 연속한 raw_atr_ordinal" 이다. 실패 비트 사이에
  F 비트 하나만 있어도 run 이 둘로 쪼개진다.
- 이웃 간 드롭률 d 일 때 길이 L run 의 잔존 질량은 대략 (1-d)^(L-1) 로,
  억제는 길이에 지수적이다. 그리고 d 는 record 마다 크게 다르다 —
  208 은 F 가 조밀하고 101 은 사실상 F 가 없다.
- 즉 긴 run 은 **DS1 에서 하필 208 에서 가장 세게 억제**된다. 84.3% 붕괴로
  이 진단을 촉발한 바로 그 record 다.

왜 판정에 걸리는가:
- H1_ASSOCIATED 조건 "run topology 의 다수가 length ≤2"
- M0.4 의 보고량 share_in_long_runs
- H3_ASSOCIATED 조건 "설명된 실패의 ≥0.50 이 length ≥3 run 에 포함"
→ 이 아티팩트는 세 입력을 **같은 방향**으로 민다: H1 쪽으로, H3 반대쪽으로.
   가설 정렬된 record 의존 편향이므로 미지수로 남겨 둘 수 없다.

Claude 의 제안(채택 여부는 네가 정한다):
- 등록 primary 는 raw_atr_ordinal 인접 그대로 유지한다(네가 등록한 정의다).
- mamba_record_row 인접을 **등록 secondary** 로 병기해 편향 크기를 측정 가능하게 한다.
- 근거 두 가지:
  (a) 이것은 네가 금지한 "ordinal 결측을 시간상 인접으로 보정"이 아니다.
      mamba_record_row + 1 은 join 이 실제로 다루는 시퀀스의 문자 그대로 다음 행이고,
      join_map 에 이미 들어 있다. 시간 추정이 개입하지 않는다.
  (b) H1 의 e_j − e_{j−1} 과 H3 의 필터-단계/끝점 의미 전파는 둘 다
      **연속한 kept beat** 사이에서 일어난다. 주석 인덱스 인접이 아니라.

네가 결정할 것:
1) primary 를 raw-ordinal 로 둘 것인가, mamba_record_row 로 바꿀 것인가, 병기할 것인가.
2) 병기한다면 H1·H3 의 run 관련 effect-size gate 는 어느 정의로 판정하는가.
   (두 정의가 엇갈릴 때의 규칙까지 사전등록해야 한다 — 사후에 유리한 쪽을 고를 수 없다.)
3) 병기하지 않는다면, 이 편향을 결과 해석에 어떻게 명시적으로 싣는가.

──────────────────────────────────────────────────────────────────────
Q2 — Control B 의 순열이 joint 인지 reason 별 독립인지 미등록
──────────────────────────────────────────────────────────────────────
Control B 는 record × side × failure-reason 별 실패 수를 보존하고 ordinal 위치만
순열한다. reason 마다 독립 순열을 돌리면 두 reason 이 같은 행에 떨어질 수 있다.

의도는 아마 record × side 위치 풀에 **단일 joint 순열**을 돌리고 라벨 다중집합
{NO_EDGE×a, NOT_OPTIMAL×b, AMBIGUOUS×c, CERTIFIED×나머지} 을 배정하는 것일 텐데,
그러면 reason 별 개수가 전부 보존되고 충돌이 불가능하다.

이것을 명시해 달라. 유효한 null 과 정의 불가능한 null 의 차이이고, 미기재로 두면
구현자가 추측해서 메우게 된다.

──────────────────────────────────────────────────────────────────────
Q3 — M4 부재 분기에서 Holm 의 적용 범위 미등록
──────────────────────────────────────────────────────────────────────
Holm 은 H1~H4 네 family 에 등록돼 있다. 그런데 MECHANISM_UNRESOLVED_INPUT_ABSENT
분기에서는 H2·H3 의 p 가 애초에 계산되지 않는다.
- 4 family 로 보정하면 계산조차 안 된 둘 때문에 과보수가 된다.
- 2 family 로 보정하면 등록된 multiplicity 를 조용히 바꾸는 것이 된다.
어느 쪽인지 사전등록해 달라. 그 분기의 H1·H4 는 어차피 종결 판정으로 승격되지
않지만, diagnostic partial result 로 보고되므로 붙는 숫자의 정의는 있어야 한다.

──────────────────────────────────────────────────────────────────────
Q4 — cache-side CERTIFIED 군의 구성 방법 미기술
──────────────────────────────────────────────────────────────────────
join_record() 는 인증쌍을 **mamba 행 1개로만** 내보낸다. 따라서 join_map 에
status = CERTIFIED 인 cache-side 행은 존재하지 않는다.
그런데 M3 은 side 별로 CERTIFIED / NO_EDGE / NOT_OPTIMAL / AMBIGUOUS 네 군을
비교하고, Control B 의 층은 record × side 다.
cache-side certified 군을 certified mamba 행의 cache_record_row 로부터 파생시키는
것이 자명하지만 명세에 안 적혀 있다. 명시하지 않으면 구현마다 분모가 달라진다.

──────────────────────────────────────────────────────────────────────
Q5 — cache endpoint 의 저장된 0.0 이 H3 의 거리 구간에 들어간다
──────────────────────────────────────────────────────────────────────
rr_features 는 record 끝점 RR 을 nan → 0.0 으로 둔다(복제가 아니다). 따라서 각
record 의 첫·끝 cache 행은 실제 데이터로서 0.0 을 갖고, 그 d_inf 는 필연적으로
RR 한 구간 규모 → >100 sample bin 에 떨어진다. 그런데 그 bin 은 H3 의 거리 조건이
읽는 바로 그 구간이다.
규모는 작다(22 record × 2 = 44 행 / 미인증 cache 12,158 행, 인증분 제외하면 더 적다).
위협이라기보다 위생 문제지만, CENSORED_AT_WINDOW_BOUNDARY 와 같은 이유로
CACHE_ENDPOINT_ZERO 로 분리·별도 집계하고 H3 거리 조건에서 제외할지 결정해 달라.

──────────────────────────────────────────────────────────────────────
부가 결정 1건 — M4 feasibility gate 3번이 현재 상태로는 미충족이다
──────────────────────────────────────────────────────────────────────
M4.0 은 (1) 원 detect_r + annotation matching 재생 가능, (2) detector peak 위치를
결정론적으로 획득 가능, (3) source version·hash 동결 — 셋을 요구한다.

측정된 사실:
- 두 계보 어디에도 detector peak 위치가 저장돼 있지 않다.
  load_cache_sequences() 는 캐시의 rr 블록만 읽고, mamba 계보는 rpks 를 저장하지
  않는다(PROVENANCE §8). 즉 M4 는 등록 런타임에서 detect_r() 재실행이 필수다.
- ASSETS.md 는 baseline-v9-source · baseline-v10-source 를 "hash 미계산" 으로,
  cache-v9-mitdb · cache-v10-mitdb 도 "hash 미계산" 으로 기록한다.
→ 지금 실행하면 (3) 이 불충족이라 M4 = DIAGNOSTIC_INPUT_ABSENT,
   전체 판정 MECHANISM_UNRESOLVED_INPUT_ABSENT 가 가장 가능성 높은 결과다.

이것은 설계가 의도한 정직한 출구지 결함이 아니다(추측으로 drop 위치를 만드는 것보다
낫다). 다만 M4 를 살릴 생각이면, 승인 전에 그 소스 패키지와 캐시 npz 의 SHA-256 을
계산해 ASSETS.md 에 등록하는 선행 작업을 별도로 지시해야 한다.
M4 를 애초에 포기하고 H1·H4 만으로 진단을 닫는 것도 유효한 선택이다 — 그 경우
"H2·H3 는 현재 artifact 로 평가 불가" 를 결과로 명시하게 설계를 정리해 달라.

──────────────────────────────────────────────────────────────────────

[바꾸지 말 것]
- 고정 질문, 언어 경계(연관 기전까지 — "원인" 금지)
- H1~H4 의 대등 등록, NO_EDGE 와 NOT_OPTIMAL 의 분리
- W = 15, d_inf 정의, 보고 구간, censoring 규칙
- 10,000 replicate, permutation p 공식, effect-size gate 병행 요구
- mutually exhaustive decision tree 와 NO_REGISTERED_MECHANISM_ASSOCIATED 분기
- QA 재현 목표와 중단 규칙
- DS1→DS2 split, parent primary(S_PR_AUC)
필요한 변경은 임의로 하지 말고 Decision log 에 사유와 함께 남겨라.

[절대 하지 말 것]
- tolerance 확대 또는 새 tolerance 선택. 진단 결과로 join 규칙을 고르는 것.
- M0 를 포함한 어떤 집계도 실행하는 것. 이 단계는 설계뿐이다.
- DS2 per-beat label · V10 probability · association · S PR-AUC · 학습.
- 기존 Drive 산출물(canonical·superseded) 및 null shard 수정·이동·삭제.
- mit-bih/q5d_order_preserving_beat_join.py 수정.
- status 를 스스로 approved_for_implementation 으로 올리는 것.

[산출 형식]
- 최신 main 에서 시작해 브랜치 codex/<task> 에서 작업한다. claude/ namespace 를
  쓰지 않는다.
- experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md 를 개정한다:
  Q1~Q5 결정을 본문 해당 절에 반영하고, §"Open design questions for Codex" 는
  해소된 항목을 결정 내용으로 대체한다.
- Decision log 에 각 결정의 사유를 남긴다. 특히 Q1 은 어느 정의를 primary 로
  삼았고 그 선택이 H1·H3 판정에 어떤 편향을 남기는지 명시하라.
- Claude 가 전달문 부재로 등록한 두 값(null master seed 2026019,
  local_rr_sd = [row-10, row+10] 구간 pre 의 모집단 표준편차)도 함께 검토해
  승인하거나 교체하라.
- status 는 draft 로 둔 채 PR 을 올리고 사용자 승인을 기다린다.
- 커밋 전 CLAUDE.md 의 필수 순서를 따른다
  (git fetch origin main && git merge origin/main → indexer --check → indexer).

[승인 경계]
[1] 네가 Q1~Q5 결정 + 명세 개정   ← 지금
[2] 사용자 승인 → status: approved_for_implementation
[3] Claude Code 구현 (실행하지 않음)
[4] 실행에 대한 별도 사용자 승인
[5] M0~M4 실행 → 새 timestamped Drive bundle → 노트북 커밋 → ingest
[2]와 [4]는 별개다. V10 확률과 association 은 계속 봉인이다.
```

---

## 0. 한 줄 요약

EXP-2026-008 은 **전사 완료·병합됨(`status: draft`)**. 전사 과정에서 과학 규칙은
바뀌지 않았지만, **등록된 정의가 Q5-D 산출물의 실제 성질과 만나는 지점 5건**이
미결로 남았다. 그중 **Q1 하나만이 판정을 실제로 움직이고**, 나머지 넷은 미기재로
두면 구현자가 추측으로 메우게 되는 항목이다.

---

## 1. 왜 이 문서가 필요한가

Claude 는 `implementation_owner` 이지 `design_owner` 가 아니다. 아래 5건은 전부
**측정의 의미를 바꾸는 결정**이므로 전사자가 정할 수 없다. 그렇다고 미기재로 두면
구현 시점에 구현자가 사실상 설계를 하게 된다 — 그게 오염이다. 그래서 판단하지 않고
올린다.

반대로, 같은 검토에서 나온 **엔지니어링 항목은 Claude 가 직접 명세에 등록했다**
(단계별 의존성 선언, 등록 입력 재검증, canonical 판별, 모듈 stale 방어, 단계
RUN/SKIP 고지, 비용 프로파일). 과학 규칙을 건드리지 않고 Q5-D 가 실제로 당했던
실패를 닫는 것이라 `implementation_owner` 권한 안이다. 명세 §「Runtime and
execution-environment contract」에 있다.

---

## 2. Q1 의 근거 — 코드와 산술

### 2.1 `raw_atr_ordinal` 은 드롭된 주석까지 센다

`mit-bih/q5d_order_preserving_beat_join.py :: replay_leg1_record()`

```python
for ordinal, (pos, symbol) in enumerate(annotations):
    ...
    if str(symbol) not in AAMI_SYMBOL_MAP:
        entry["reason"] = REASON_SYMBOL
        out.dropped.append(entry)
        continue
    if not (WIN_BEFORE <= pos < int(signal_length) - WIN_AFTER):
        entry["reason"] = REASON_BOUNDARY
        out.dropped.append(entry)
        continue
```

`ordinal` 은 **전체 `.atr` 주석**에 대한 번호다. 드롭된 비트도 번호를 소비한다.
반면 `mamba_record_row` 는 `out.kept` 안에서만 0부터 매겨진다:

```python
for row, (entry, pre_s, post_s) in enumerate(zip(out.kept, ...)):
    entry["mamba_record_row"] = row
```

두 좌표는 **드롭된 주석 수만큼 어긋난다**. 이건 결함이 아니라 정의다 —
`raw_atr_ordinal` 은 원 주석 좌표, `mamba_record_row` 는 처리 시퀀스 좌표.

### 2.2 드롭은 record 마다 밀도가 다르다

`research/ASSETS.md :: data-mit-mamba` 와 Q5-B-0 실측:

| 드롭 심볼 | 개수 |
|---|---|
| N | 1 |
| S | 0 |
| V | 0 |
| **F** | **802** |
| Q | 15 |
| 합계 | 818 |

그리고 **92% 가 record 208·213 에 집중**된다. 208 은 DS1, 213 은 DS2이므로
**이번 DS1 진단에서는 208 이 영향을 독점한다.**

### 2.3 억제는 run 길이에 지수적이다

M0.4·M2 의 run 은 "정확히 연속한 `raw_atr_ordinal`" 이다. 이웃 링크가 끊길 확률을
`d` 라 하면 길이 `L` run 이 온전히 살아남을 확률은 대략 `(1-d)^(L-1)`.

- record 208: F 가 조밀 → `d` 가 크다 → `L ≥ 10` 은 심하게 억제
- record 101 등: F 가 사실상 없음 → `d ≈ 0` → 거의 무영향

**record 의존적이고, 방향이 가설과 정렬돼 있다.**

### 2.4 어느 판정 입력에 들어가는가

| 입력 | 쓰이는 곳 | 아티팩트의 방향 |
|---|---|---|
| `share_in_long_runs` | M0.4 보고 | 과소 |
| "run topology 의 다수가 length ≤2" | `H1_ASSOCIATED` 조건 | **충족되기 쉬워짐** |
| "설명된 실패의 ≥0.50 이 length ≥3 run 에" | `H3_ASSOCIATED` 조건 | **충족되기 어려워짐** |

세 개가 전부 같은 방향 — **H1 유리 · H3 불리**, 그것도 208 에서 가장 세게.

### 2.5 왜 `mamba_record_row` 병기가 금지 조항 위반이 아닌가

원 지시는 *"ordinal 결측을 **시간상 인접**으로 보정하지 마라"* 다. 금지 대상은
"주석 하나 빠졌으니 시간상 가까우면 이어 붙이자"는 **추정**이다.

`mamba_record_row + 1` 은 추정이 아니다. join 이 실제로 다루는 시퀀스의 **문자
그대로 다음 행**이고, 이미 `join_map` 컬럼으로 존재하며, 시간 계산이 개입하지 않는다.

게다가 두 가설이 말하는 물리량이 그 좌표에 산다:

- **H1** 의 `e_j − e_{j−1}` — 이웃한 **kept beat** 사이의 검출 오프셋 변화
- **H3** 의 필터 단계/끝점 의미 차이 전파 — 필터를 통과한 **이웃 beat** 로 번진다

둘 다 "연속한 주석"이 아니라 "연속한 kept beat" 사이의 현상이다.

---

## 3. Q2~Q5 요약 — 미기재가 곧 구현자 재량

| | 항목 | 미기재로 두면 |
|---|---|---|
| **Q2** | Control B 순열이 joint 인지 reason 별 독립인지 | 독립이면 두 reason 이 같은 행에 충돌 → null 자체가 정의 불가 |
| **Q3** | M4 부재 분기의 Holm 범위(4 vs 2 family) | partial result 에 붙는 p 의 정의가 없음 |
| **Q4** | cache-side `CERTIFIED` 군 파생 방법 | 구현마다 M3 분모가 달라짐 |
| **Q5** | cache endpoint `0.0` 행 처리 | H3 거리 조건이 읽는 bin 에 44행이 섞임 |

**Q4 의 근거**: `join_record()` 는 인증쌍을 **mamba 행 1개로만** 내보낸다.
`status = CERTIFIED` 인 cache-side 행은 `join_map` 에 **존재하지 않는다**.

**Q5 의 근거**: `rr_features` 는 끝점을 `nan → 0.0` 으로 둔다(mamba 처럼 복제하지
않는다). 저장된 `0.0` 은 "이웃 없음"을 뜻하는 실제 데이터이고, `load_cache_sequences()`
가 단위 검사에서만 제외할 뿐 값은 그대로 흘린다.

---

## 4. 부가 결정 — M4 는 지금 상태로 돌리면 멈춘다

| feasibility 조건 | 현재 상태 |
|---|---|
| (1) 원 `detect_r` + annotation matching 재생 가능 | 소스는 확보됨 (`baseline-v10-source`) |
| (2) detector peak 위치를 결정론적으로 획득 | **저장돼 있지 않음** → 등록 런타임에서 재실행 필수 |
| (3) source version·hash 동결 | **미충족** — `ASSETS.md` 가 "hash 미계산" |

`load_cache_sequences()` 는 캐시의 `rr` 블록만 읽고, mamba 계보는 `rpks` 를 저장하지
않는다(`PROVENANCE_2026-08-10` §8). 따라서 **두 계보 어디에도 detector peak 위치가
없다.**

→ 지금 실행하면 `M4 = DIAGNOSTIC_INPUT_ABSENT`, 전체 판정
`MECHANISM_UNRESOLVED_INPUT_ABSENT` 가 가장 가능성 높다. **설계가 의도한 정직한
출구지 결함이 아니다** — 추측으로 drop 위치를 만드는 것보다 낫다.

선택지는 둘이다:

1. **M4 를 살린다** — 승인 전에 `baseline-v9-source`·`baseline-v10-source`·
   `cache-v9-mitdb`·`cache-v10-mitdb` 의 SHA-256 을 계산해 `ASSETS.md` 에 등록하는
   선행 작업을 별도 지시.
2. **M4 를 포기한다** — H1·H4 만으로 진단을 닫고, "H2·H3 는 현재 artifact 로 평가
   불가"를 결과로 명시하도록 설계를 정리.

---

## 5. Claude 가 이번 검토에서 이미 고친 것 (참고 — 결정 불필요)

전사본 자체의 구멍 1건. §「Preregistration principle」이 *"정의가 구현 불가면
Decision log 로 수정·재승인 — 해당 측정이 돌기 전에"* 로 돼 있어, **M0 를 본 뒤에도
M1 이 아직 안 돌았으면 M1 정의를 고칠 수 있다**로 읽혔다. 원 지시의 *"M0 결과를 먼저
보고 M1–M4 의 정의·창 크기·해석 기준을 바꾸는 것을 금지"* 와 정면 충돌이라 닫았다:

> M0 결과를 본 순간부터 M1–M4 정의 수정 불가. 문제가 생기면 STOP 후 Codex 로 반환.
> 중간 수리 경로 없음.

그리고 `5 of 13` 은 오기가 아니다 — `evaluate_gates()` 가 gate 2 를
`2a_leg1_source_replay` / `2b_leg2_record_boundaries` 로 쪼개 내보내고
`13_ambiguity_reported` 를 더해서 13이 맞다. 12로 "고치지 말라"고 주석해 뒀다.

---

## 6. 우선순위 제안

**Q1 만이 판정을 움직인다.** 나머지 넷은 "이렇게 읽으면 되나" 확인 수준이므로,
Q1 결정이 오래 걸리면 **Q2~Q5 를 먼저 확정하고 Q1 을 남겨 두는 분할 처리도 가능**하다.
다만 승인(`approved_for_implementation`) 전에는 Q1 이 닫혀 있어야 한다 — 편향이 걸린
채로 구현에 들어가면 실행 후에 고칠 수 없다.

---

## 7. 근거 문서 위치

| 내용 | 파일 |
|---|---|
| 진단 명세 (이번 개정 대상) | `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md` |
| Q5-D 실측 결과·gate 표 | `experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md` Decision log |
| 진단 설계 요청 (Q5-E 발단) | `research/HANDOFF_2026-08-11_Q5D_v_class_join_failure_to_codex.md` |
| RR 계약 · 44-record 행 대장 | `research/HANDOFF_2026-08-10_Q5D_preflight_result_to_codex.md` |
| mamba 계보 (드롭 규칙 · R sample 미저장) | `research/PROVENANCE_2026-08-10_mamba_data_lineage.md` |
| 자산 등록 (hash 미계산 항목 포함) | `research/ASSETS.md` |
| Q5-D 구현 (읽기 전용) | `mit-bih/q5d_order_preserving_beat_join.py` |

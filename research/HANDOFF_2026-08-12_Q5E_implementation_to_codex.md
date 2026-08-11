# Codex 과제 — Q5-E 구현 인수검사 + I1~I4 결정 (검토만, 실행 금지)

작성: 2026-08-12 · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md`
(`status: approved_for_implementation` · `design_owner: codex` ·
`implementation_owner: claude`)
근거: PR #110(구현) + `45d7c4f`(H4 확정), main `affc152` 에 병합됨

승인 체인상 위치: **구현 PR 병합 완료 → Codex 구현 인수검사 → 사용자 실행 승인.**
지금은 그 가운데 단계다.

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/my-github-test (MedKOS / ECG).

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md 전체
   특히 M0~M5 · M4.0/M4.1 · Runtime 계약 · Q1~Q5 · Multiplicity ·
   Preregistered association flags · Decision tree · QA · Decision log 의
   2026-08-12 구현 항목
3. mit-bih/q5e_leg2_failure_mechanism_audit.py
4. mit-bih/test_q5e_leg2_failure_mechanism_audit.py
5. notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb
6. research/HANDOFF_2026-08-12_Q5E_implementation_to_codex.md  ← 이번 지시서
7. mit-bih/q5d_order_preserving_beat_join.py (읽기 전용, 수정 금지)

[상황]
동결 설계 구현이 main(affc152)에 병합됐다. status 는 approved_for_implementation
그대로다. 한 번도 실행되지 않았다 — 등록 자산 미열람 · M0~M4 집계 0 ·
detect_r() 미호출 · beat join 미재실행 · DS2 label/V10 확률 미열람 · 학습 0 ·
Drive 쓰기 0. 노트북은 미실행(code cell 9, outputs 0, execution_count 0).

테스트 44 함수 · 268 assertion 통과, 전부 synthetic.
동결 Q5-D 무변경: git diff 없음 · 자체 881 assertion 통과 ·
rule_fingerprint 31c4be9f… · 파일 해시 6b098c67….

네가 2026-08-12 에 확정한 H4_DECISIONAL_SIDE = cache 도 반영을 마쳤고,
부정확했던 근거 문구("every other decisional population here is cache-side")는
철회하고 네가 지정한 근거로 교체했다.

[과제]
구현을 인수검사하고 아래 I1~I4 를 결정하라. 검토와 설계 판단만 한다.
구현 수정이 필요하면 지시하되, 등록 데이터 실행은 하지 않는다.

──────────────────────────────────────────────────────────────────────
I1 — 구현이 동결 설계와 일치하는가
──────────────────────────────────────────────────────────────────────
확인 대상(전부 코드로 확인 가능):
- M0.1~M0.6 의 분자·분모, M0.4/M0.5 의 primary=mamba_record_row 와
  secondary=raw_atr_ordinal 의 decisional 태그
- M1 의 W=15, rank-proportional centre, d_inf, 보고 구간,
  CENSORED_AT_WINDOW_BOUNDARY 와 CACHE_ENDPOINT_ZERO 의 배제
- M2 의 ±1 / ±10 이웃, cache-side 행 배제
- M3 의 다섯 행별 지표, 네 group, cache-side CERTIFIED 1:1 파생과
  disjoint/exhaustive partition assertion
- M4.0 세 조건과 조건 2 의 하위 gate 순서, M4.1 의 anchor 배치 규칙
- control A/B/C, permutation p 공식, q99, Holm 4-family, effect gate,
  decision tree 전 분기

특히 볼 것 두 가지:
(a) rank-proportional centre 가 동결 모듈의 to_samples() 를 재사용해
    round-half-to-even 을 단일 출처화했다. 재구현이 아니라 재사용이 맞는지.
(b) CENSORED 와 CACHE_ENDPOINT_ZERO 배제가 distance_gate_rows() 한 함수로만
    이뤄져, 관측 통계와 모든 replicate 가 "두 코드 경로의 우연한 일치"가 아니라
    구성상 같은 모집단을 쓴다. 이 구조를 수용하는지.

──────────────────────────────────────────────────────────────────────
I2 — 안전장치가 실제로 막는가
──────────────────────────────────────────────────────────────────────
- OPEN_REGISTERED_DATA 기본 False, run_audit() 이 그것부터 거부
- require_execution_approval() 이 open() 보다 먼저 → 미승인 호출은 파일 존재
  여부조차 알 수 없다. 권한이 능력보다 먼저 검사된다
- run_audit() 말미의 종단 가드(실행 승인 부재를 명시하고 raise)
- CLI 기본 DESIGN, --mode AUDIT 은 exit 2
- stage_should_run() 이 RUN/SKIP 을 항상 고지
- assert_implementation_only() 의 봉인 토큰 검사
- 비어 있지 않은 번들 디렉터리에 쓰지 않음

판단할 것: 이 조합이 "실행 승인 없이는 어떤 등록 자산도 열리지 않는다"를
충분히 보장하는가. 부족하면 무엇을 더 요구하는가.

──────────────────────────────────────────────────────────────────────
I3 — H4 cache-side 확정이 7항목 전부에 단일 출처로 반영됐는가
──────────────────────────────────────────────────────────────────────
네 계약은 observed contrast · Control B null · raw p · q99 · Holm 에 들어가는
H4 p · candidate_degree>=2 share · rr_pair_multiplicity/local_rr_sd 방향
조건 일곱 가지였다.

구현:
- stat_h4() 에서 side 인자를 제거했다 → production 호출자가 판정 side 를
  바꿀 수 없다. 반대편은 private _degree_median_contrast() 로만 도달한다.
- h4_evaluate() 가 일곱 항목을 한 곳에서 낸다.
- h4_null_statistic() 은 record x cache-side 에서만 permutation 한다.
- mamba-side 행은 decisional:false 로 직렬화되고 m3_graph.csv 에 decisional
  열이 추가됐다. result/config 에 h4_decisional_side == "cache".
- pooled/max/best-side/side-pvalue 경로 부재를 테스트가 이름으로 검사한다.

판단할 것: 이 반영이 계약을 충족하는가. 그리고 §5.2 의 CSV 열 추가를
승인하는가(등록 스키마 변경이라 네 확인이 필요하다).

──────────────────────────────────────────────────────────────────────
I4 — 실행 승인 전에 무엇이 더 필요한가  [실질 쟁점]
──────────────────────────────────────────────────────────────────────
M4.0 조건 1·3 은 닫혔고 조건 2 만 남았다. 그리고 조건 2 는 코드 문제가 아니라
환경 문제로 좁혀져 있다 — 등록 runtime(CPython 3.12.3 / numpy 2.5.1 /
scipy 1.18.0 / wfdb 4.3.1)을 fallback 없이 지금 세울 수 있는가.

사실관계: 지금까지의 두 preflight 는 전부 Colab python 3.12.13 / numpy 2.0.2
에서 돌았다. 등록 runtime 이 실제로 서는지는 **한 번도 시험되지 않았다.**

선택지:
  (a) 그대로 실행 승인. 조건 2 는 실행 중에 평가되고, 서지 않으면 설계대로
      M4 = DIAGNOSTIC_INPUT_ABSENT → MECHANISM_UNRESOLVED_INPUT_ABSENT 로
      끝난다. 정직한 출구지만 실행 승인 한 번을 소모한다.
  (b) 실행 승인 전에 **최소 runtime probe** 를 하나 요구한다. 버전 핀이 서는지만
      확인하고 detect_r() 는 부르지 않으며 등록 자산도 열지 않는다. 봉인에
      걸리지 않고 비용이 거의 없다. 대신 승인 체인이 한 단계 늘어난다.
  (c) 다른 안.

(b) 를 고른다면 그 probe 가 무엇을 통과 기준으로 삼는지(예: import 성공 +
버전 문자열 정확 일치, 또는 1 record 에 대한 detect_r 재현까지)를 명시하라.
후자는 이미 조건 2 의 일부이므로 별도 probe 가 아니라 M4 실행이라는 점에
주의하라.

──────────────────────────────────────────────────────────────────────

[바꾸지 말 것]
- 고정 질문, 언어 경계(연관 기전까지 — "원인" 금지)
- H1~H4 대등 등록, NO_EDGE 와 NOT_OPTIMAL 분리
- 확정된 Q1~Q5 · A~E · D1~D4 결정과 H4 cache-side 확정
- W=15, d_inf 정의, 보고 구간, censoring 규칙
- 10,000 replicate, seed 2026019, permutation p 공식, Holm 4-family,
  effect-size gate 병행
- mutually exhaustive decision tree 와 NO_REGISTERED_MECHANISM_ASSOCIATED 분기
- QA 재현 목표와 중단 규칙
- 동결 M4 identity 상수와 두 preflight 판정

[절대 하지 말 것]
- M0 를 포함한 어떤 집계도 실행하는 것
- detect_r() 실행, beat join 재실행
- DS2 per-beat label · V10 probability · association · S PR-AUC · 학습
- 기존 Drive 산출물·run bundle·null shard 수정
- mit-bih/q5d_order_preserving_beat_join.py 수정
- status 를 approved_for_execution / RUNNING / MEASURED / COMPLETE 로 올리는 것
  (실행 승인은 사용자 사항이다)
- 결과 수치나 과학적 판정을 명세에 쓰는 것

[산출 형식]
- 최신 main(affc152)에서 시작해 브랜치 codex/<task> 로 작업한다.
  claude/ namespace 를 쓰지 않는다.
- 인수검사 결과와 I1~I4 결정을 명세 Decision log 에 남긴다.
- 구현 수정이 필요하면 무엇을 어떻게 고칠지 지시하라. 직접 고칠 경우에도
  허용 파일은 네 개(명세 · 모듈 · 테스트 · 노트북)뿐이다.
- status 는 approved_for_implementation 으로 두고 PR 을 올린 뒤 사용자
  승인을 기다린다.
- 커밋 전 CLAUDE.md 의 필수 순서를 따른다
  (git fetch origin main && git merge origin/main → indexer --check → indexer).

[승인 경계]
[1] 네가 구현 인수검사 + I1~I4 결정   ← 지금
[2] 사용자 실행 승인
[3] M0~M4 실행 (M4.0 조건 2 를 anchor 전에 평가)
[4] 새 timestamped Drive bundle → 실행된 노트북 커밋 → ingest
[5] 네가 결과 인수검사
[1] 은 [2] 가 아니다. V10 확률과 association 은 계속 봉인이다.
```

---

## 0. 한 줄 요약

동결 설계 구현이 병합됐고 **한 번도 실행되지 않았다.** 남은 실질 쟁점은 하나 —
**M4.0 조건 2 의 등록 runtime 이 지금 세워지는지가 한 번도 시험되지 않았다**는
것이고, 그것을 실행 승인 전에 확인할지가 I4 다.

---

## 1. 무엇이 구현됐나

| 파일 | 내용 |
|---|---|
| `mit-bih/q5e_leg2_failure_mechanism_audit.py` | M0~M5 · M4.0/M4.1 · control A/B/C · Holm · flag · decision tree · 결과/번들 스키마 · 그림 계약 · production entry point |
| `mit-bih/test_q5e_leg2_failure_mechanism_audit.py` | 44 함수 · 268 assertion, 전부 synthetic |
| `notebooks/quest55_…ipynb` | 미실행(code cell 9, outputs 0, execution_count 0) |
| 명세 | 체크 1개 + 구현 Decision log + H4 확정 반영 |

측정 정의는 명세 그대로다. 특히:

- `mamba_record_row` 가 primary, `raw_atr_ordinal` 은 모든 표에서
  `decisional: false` 로만 동행한다.
- `W = 15` 는 상수이고, rank-proportional centre 는 **동결 모듈의
  `to_samples()` 를 재사용**해 round-half-to-even 을 단일 출처화했다(재구현하지
  않았다).
- `CENSORED_AT_WINDOW_BOUNDARY` 와 `CACHE_ENDPOINT_ZERO` 배제는
  **`distance_gate_rows()` 한 함수**로만 이뤄진다 → 관측 통계와 모든 replicate 가
  "두 코드 경로의 우연한 일치"가 아니라 **구성상** 같은 모집단을 쓴다.
- Control B 는 `record x side` **단일 joint categorical permutation** 이라
  per-reason 개수가 보존되고 충돌이 불가능하다.
- `UNEVALUABLE` family 는 p=1 을 **Holm 계산 안에서만** 쓰고, 테스트가
  "unevaluable family 에는 significance 판정이 아예 붙지 않음"을 확인한다.

---

## 2. 안전장치

| 장치 | 효과 |
|---|---|
| `OPEN_REGISTERED_DATA = False` | 기본값. `run_audit()` 이 **그것부터** 거부 |
| `require_execution_approval()` | `open()` **보다 먼저** → 미승인 호출은 파일 존재 여부조차 못 얻는다 |
| 권한 → 능력 순서 | 환경에 무엇이 깔려 있든 미승인은 미승인으로 거부 |
| `run_audit()` 종단 가드 | 실행 승인 부재를 명시하고 raise |
| CLI | 기본 `DESIGN`, `--mode AUDIT` 은 **exit 2** |
| `stage_should_run()` | 모든 단계가 `RUN`/`SKIP` 을 사유와 함께 고지 |
| `assert_implementation_only()` | 봉인 토큰 부재를 텍스트로 증명 |
| 번들 쓰기 | 비어 있지 않은 디렉터리에는 쓰지 않는다 |

---

## 3. H4 확정 반영

| 계약 항목 | 반영 |
|---|---|
| observed contrast | `stat_h4()` — **`side` 인자 없음** |
| Control B null | `h4_null_statistic()` — `record x cache-side` 만 permutation |
| raw p · q99 · Holm 입력 p | `h4_evaluate()` 한 곳에서 산출 |
| `degree >= 2` share | `h4_effect_gates()` — cache-side만 |
| multiplicity / variability 방향 | 동상 |
| mamba-side | `decisional: false` 직렬화, `m3_graph.csv` 에 `decisional` 열 |
| 사후 선택 차단 | `pooled`/`max`/`best_side`/`side_pvalue` 경로 부재를 테스트가 이름으로 검사 |

부정확했던 근거 문구는 철회하고 Codex 가 지정한 근거로 교체했다.

---

## 4. I4 의 근거 — 조건 2 는 환경 문제로 좁혀져 있다

| M4.0 조건 | 상태 |
|---|---|
| 1. 원 `detect_r`/`rr_features` 생산자 식별 | **닫힘** — `frontend.py` `d2635e05…` · `data.py` `20cde66b…` 동결, 정적 source-map 검증 구현 |
| 3. V10 source/cache identity + RR 등가 | **닫힘** — `1a0c66c8…` · `82b9a593…` · `RR_VALUE_IDENTICAL_44_OF_44` |
| 2. detector peak 를 결정론적으로 획득 | **미충족** |

조건 2 가 남는 이유는 자산 결함이 아니다. peak 위치가 어느 계보에도 저장돼
있지 않아 등록 runtime 에서 재실행해야 하는데, **그 runtime 이 지금 서는지가 한
번도 시험되지 않았다.** 두 preflight 는 전부 Colab `python 3.12.13 /
numpy 2.0.2` 에서 돌았다.

RR 등가 결과가 말해 주는 것은 "두 과거 실행이 서로 재현됐다"까지이고,
"지금 그 환경을 다시 세울 수 있다"는 아니다 — 명세 M4.0 조건 2 가 그 구분을
이미 못 박아 뒀다.

**그래서 실행 승인 한 번을 쓰기 전에 값싼 probe 로 확인할지가 I4 다.**

---

## 5. 구현 중 나온 확인 요망 3건

### 5.1 Control A 가 순환이동하는 class 벡터

`control_a_class_shift()` 는 record별 class 시퀀스를 받는 **범용** 함수로
구현했다. H1 의 모집단이 cache-side 이고 통계량이 processed class 로 V/비V 를
가르므로, 배선 시점에 넘길 벡터는 **canonical DS1 processed-class map 의
cache-side 시퀀스**여야 한다(`mamba_aami` 가 아니다).

명세가 "the per-record class sequence" 라고만 적어 배선이 코드 밖에 남아 있다.
M4 가 부재하면 **H1 이 완전히 평가되는 유일한 family** 이므로, 그 null 이 어느
class 벡터 위에서 도는지는 확인해 둘 가치가 있다.

### 5.2 `m3_graph.csv` 에 `decisional` 열 추가

"mamba-side 는 명시적으로 `decisional:false` 로만 직렬화하라"는 지시를 따르려면
행 단위 태그가 필요해서 열을 하나 추가하고 명세의 CSV 스키마도 같이 고쳤다.
**등록 스키마 변경**이므로 Codex 승인이 필요하다. 원하지 않으면 대안은 result
JSON 에만 기록하고 CSV 는 원안대로 두는 것이다.

### 5.3 `run_audit()` 종단 가드의 제거 시점

`run_audit()` 은 canonical 검증까지 마친 뒤 "실행 승인이 아직 없다"를 명시하며
raise 한다. 이 가드는 **실행 승인 변경이 제거하는 것**이지 구현자가 미리 지우는
것이 아니다. 제거가 실행 승인 PR 의 일부임을 Decision log 에 못 박아 두면
조용히 사라지는 일을 막을 수 있다.

---

## 6. 실행 승인이 나면 — Colab 순서

노트북 셀 4 의 스위치 **셋을 모두** 열어야 한다(하나만으로는 거부된다):

```python
MODE = Q5E.MODE_AUDIT
APPROVAL = Q5E.EXECUTION_APPROVAL_TOKEN
OPEN_REGISTERED_DATA = True
```

그 뒤 `run_audit()` 이 이 순서로 간다:

1. 의존성 확인(`numpy`·`pyarrow`·`wfdb`·`matplotlib`)을 **작업 전에**
2. canonicity — `SUPERSEDED.json` 부재 + `manifest.json` code hash `6b098c67…`
3. QA 재현 — 24,341 / 12,183 / 12,158 / 13,716 / 9,887 / 738 / DS1 22 /
   fingerprint. 하나라도 어긋나면 `DIAGNOSTIC_INPUT_MISMATCH` 로 즉시 STOP
4. M0 → M1 → M2 → M3 (M3 는 재생 분할이 번들과 정확히 일치하는지 먼저 확인)
5. **M4.0 gate** — `runtime → source_map → identity → detector replay →
   22/22 counts → RR exact`
6. control A/B/C × 10,000(seed 2026019) → Holm 4-family → flag → decision tree
7. 새 timestamped Drive bundle → 실행된 노트북 커밋 → `ingest_run.py`

M4 가 부재로 끝나도 **Control A 와 B 는 그대로 돈다** — H1/H4 를 diagnostic
partial result 로 보고해야 하고, Control C 만 "unevaluable, not
non-significant" 로 처리된다.

비용은 분 단위다. control 이 matcher 를 다시 돌리지 않으므로 Q5-D 의 14시간과
다르고 샤딩·resume 이 필요 없다.

---

## 7. 근거 문서 위치

| 내용 | 파일 |
|---|---|
| 동결 설계 · 두 preflight 결과 · 구현 Decision log | `experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md` |
| 구현 | `mit-bih/q5e_leg2_failure_mechanism_audit.py` |
| 회귀 테스트 | `mit-bih/test_q5e_leg2_failure_mechanism_audit.py` |
| 미실행 노트북 | `notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb` |
| 동결 자산 identity | `research/ASSETS.md` (`cache-v9/v10-mitdb`, `baseline-v9/v10-source`, `env-v9v10-runtime`) |
| 선행 인계(Q1~Q5 / A~E / D1~D4) | `research/HANDOFF_2026-08-11_Q5E_open_questions_to_codex.md` · `..._prep_m4_freeze_to_codex.md` · `HANDOFF_2026-08-12_Q5E_rr_equivalence_to_codex.md` |
| 동결 Q5-D 규약 | `mit-bih/q5d_order_preserving_beat_join.py` (읽기 전용) |

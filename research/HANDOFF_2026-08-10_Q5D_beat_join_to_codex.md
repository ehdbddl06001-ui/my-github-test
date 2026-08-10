# Codex 과제 — EXP-2026-007 beat-join 설계 (설계만, 실행 금지)

이 문서 전체가 Codex에게 주는 프롬프트다. 그대로 붙여 써도 되고, 아래
「프롬프트 본문」만 잘라 써도 된다.

- 요청 주체: 사용자 · 작성: Claude Code · 날짜 2026-08-10
- `design_owner: codex` · `implementation_owner: claude`
- Claude는 병렬로 measurement qualification을 실행 중이다. **두 작업은 파일도
  브랜치도 겹치지 않는다.** Codex 브랜치는 `codex/<task>`.
- 산출물은 **설계 문서 하나**다. 코드도, 실행도, 데이터 열람도 하지 않는다.

---

## 프롬프트 본문

### 배경 — 지금까지 확정된 사실만

`EXP-2026-007 / Q5-D`는 "전문가 검증된 P파 타이밍이 V10 모델의 S beat 실패와
연관되는가"를 묻는 사전등록 실험이다. 명세는
`experiments/specs/EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md`.

진행 상태:

1. **PREP_DATA-A `ACQUIRE_ONLY` 통과** (canonical run `20260809T153151`,
   12/12 gate). `mitdb 1.0.0` 48/48 records와 `pwave 1.0.0` 12/12 records를
   publisher checksum까지 검증해 Drive에 불변 자산으로 확보했다.
   등록: `research/ASSETS.md`의 `data-mitdb-raw-100` ·
   `data-pwave-raw-100` · `run-20260809-q5d-prep-data`.
2. **measurement qualification 통과** (canonical run `20260810T005802`,
   `MEASUREMENT_QUALIFIED`, gate 5/5). raw 파형 + `.atr` R 위치 + 전문가 P
   주석만 썼고, DS2 class label·V10 확률은 열지 않았다. DS2 record-macro
   sensitivity 0.9476 · PPV 0.8860 · cross-beat 0 · 우연 대비 8.283×
   [7.460, 9.548]. 등록: `research/ASSETS.md`의 `run-20260810-q5d-qualify`.
   **즉 측정도구는 확보됐고, 이제 막힌 것은 조인 하나다.**
3. **실험의 과학적 판정은 여전히 `NOT RUN`이다.** spec status는
   `approved_for_implementation` 그대로다.

### 풀어야 할 문제

명세의 PREP_DATA gate item 3은 이렇게 요구한다:

> Join raw `atr` R samples to the registered processed beat identity using
> `(record, sample)` and the already-audited beat filtering semantics. No
> nearest-neighbor many-to-one join is allowed.

**이 조인은 이미 실패한 것으로 실측됐다.** 그리고 이건 추측이 아니라 측정값이다:

- **Q5-A (EXP-2026-004, MEASURED)**: 동결 source의 `t` ↔ `.atr` sample 조인
  성공률 **1.9% = 우연 수준**(최근접 주석까지 중앙 거리 `0.222 × RR`).
  결론: **`t`는 annotation sample index가 아니다.** 이 경로로는 조인 불가.
- **Q5-B-0 (EXP-2026-005, MEASURED, `NO_GO_SUBTYPE_CLOSED`)**: RR 키
  `(pre_rr, post_rr)`로 우회 시도 → 조인 25.9%. v5의 동점 규칙으로 90.5%까지
  올렸으나 `subtype_coverage_balance` 0.368(<0.80)로 gate 탈락. 빠진 10%가
  드문 subtype에 몰려 분포가 왜곡됐다.
- 진단으로 밝혀진 것: 못 붙인 beat의 최근접 후보 거리는 p50 **0.10 ms**이고
  허용치 2배 안에 **93.8%**가 들어온다. **멀어서 탈락한 게 아니라 margin
  규칙(5 ms) 때문에 탈락했다** — 360 Hz에서 1 sample = 2.78 ms인데 5 ms
  margin은 차점이 ~3.6 sample 떨어질 것을 요구한다. record 안에서 coupling
  interval이 반복되면 만족 불가다.

즉 **PR_discordance를 raw 쪽에서 재더라도, 그 값을 V10이 채점한 beat에 붙일
키가 없다.** association 단계는 여기서 막혀 있다.

### 이번에 설계할 것

`.atr` beat ↔ 처리된 beat identity를 잇는 **조인 규칙 하나**와, 그 규칙이
맞는지 스스로 반증할 수 있는 검증 장치. 다음 다섯 가지를 명세로 낸다.

1. **조인 규칙 하나.** `t`를 sample index로 가정하지 않는 경로여야 한다.
   유력 후보(강제 아님): record 내 **순서 기반 정렬** + Q5-B-0의 drop map
   보정. 처리 배열이 record 안에서 beat 순서를 보존한다면, 버려진 beat를
   되돌린 뒤 rank로 대응시킬 수 있다. 다른 경로를 제안해도 된다 — 근거만 대라.
2. **음성대조군.** 최소 wrong-record · 순서 셔플 · circular shift.
   Q5-A/Q5-B-0가 쓴 것과 같은 계열로, 규칙이 우연으로도 성립하는지 본다.
3. **영가설과 신호/영가설 비.** 어떻게 계산하고 무엇과 비교하는지.
4. **중단 기준.** 어느 커버리지·정확도 아래면 `JOIN_UNRESOLVED`로 종결하는지
   숫자로. **Q5-B-0의 원칙을 유지한다: 부분 조인으로 선택 편향된 부분집합을
   쓰지 않는다.** 90%가 붙어도 빠진 10%가 특정 클래스에 몰리면 탈락이다.
   커버리지뿐 아니라 **클래스별 균형**도 기준에 넣어라.
5. **조인이 원리적으로 불가하다는 결론도 유효한 산출물이다.** 그 경우
   "무엇이 있었다면 가능했는가"(어떤 아티팩트를 어느 단계에서 저장했어야
   하는가)를 적어라. 다음 실험 설계에 그게 필요하다.

### 쓸 수 있는 것

- **synthetic fixture** — 정답을 아는 합성 beat 열. 규칙 검증의 주력.
- **DS1** — label 포함. DS1은 봉인 대상이 아니다.
- **Q5-B-0의 drop map**: 버려진 818박 = N 1 · **S 0** · V 0 · **F 802** ·
  Q 15. 92%가 record 208·213에 몰려 있다. `mamba_data.npz`에는 F가 없다
  (사실상 4-class 데이터). record별·클래스별 표는 Q5-B-0 run의
  `record_mapping.csv`.
- **record 동일성**: 5-class 지문 배정으로 44개 record가 확립됐고 leftover
  4개는 paced다. **per-record S 개수 불일치 0.**
- `ecg_multi.npz`의 RR 단위는 **samples**(median 268), `mamba_data`와 단위가
  다르다. 이 단위 혼동이 과거 조인 실패에 기여했다.
- `research/ASSETS.md` · `research/PROJECT_STATE.md` · 기존 spec 전부.

### 절대 열지 말 것

- **DS2 outcome** — DS2 beat class label, V10 확률(`v10pkg_results/`),
  DS2 기반 어떤 metric도 열지 않는다.
- 조인 규칙이나 임계값을 **DS2를 보고** 정하지 않는다. 모든 상수는 synthetic
  fixture와 DS1에서만 나온다.
- 코드를 작성하거나 실행하지 않는다. 데이터를 내려받지 않는다.
- 기존 Drive 자산을 옮기거나 덮어쓰지 않는다.

### 지켜야 할 설계 규율

- 사전등록 정신을 유지한다: **규칙·임계값·중단 기준을 데이터 보기 전에 고정**하고,
  나중에 완화하지 않는다.
- 규칙을 완화하는 민감도 분석을 보이려면 **완화된 규칙 자체로 영가설을 다시
  돌리고 `maxT`로 비교**한다(spec의 「Chance baseline and rule-relaxation rule」).
  더 엄격한 규칙의 낮은 cutoff를 재사용하지 않는다.
- 값을 못 재면 **추정으로 채우지 않는다.** Q5-A가 `B_SUBTYPE`을 "측정 불가"로
  남긴 전례를 따른다.
- 실패 판정을 만들기 쉽게 설계한다. 통과만 가능한 gate는 gate가 아니다.

### 산출 형식

`experiments/specs/` 아래 새 명세 파일 하나. `TEMPLATE.md`를 따르고
frontmatter에 `design_owner: codex` · `implementation_owner: claude` ·
`status: draft`(사용자 승인 전까지 `approved_for_implementation` 금지).

포함할 절: Fixed question · Inputs(있는 것/없는 것) · 조인 규칙 · 음성대조군 ·
영가설과 비교 방식 · 중단 기준과 판정 코드 · 「원리적 불가」 분기 ·
Files allowed to change · Decision log.

브랜치는 `codex/<task>`. Claude가 건드리는
`mit-bih/q5d_qualify_*` · `notebooks/quest53_*` · `research/PLAN_2026-08-10_*`
는 수정하지 않는다.

### 승인 경계 (중요)

이 설계가 나와도 **조인 실행은 자동으로 시작되지 않는다.** 설계 검토 + 사용자
별도 승인이 있어야 한다. 그리고 앞단의 measurement qualification이
`MEASUREMENT_UNQUALIFIED`로 끝나면 **과학 실험은 거기서 종료되고 이 조인은
실행되지 않는다** — 그 경우에도 이 설계 문서는 "무엇이 있었다면 가능했는가"의
기록으로 남는다.

---

## 참고 — Claude 쪽 진행 상황 (Codex가 알아야 할 만큼만)

- 자격검증 규칙은 고정됐다: neurokit2 `ecg_delineate(method="dwt")` ·
  channel 0 · R은 `.atr` 참조값 · P 탐색 40–300 ms · 매칭 ±50 ms 1:1.
- DS1 22 records에서 상수를 뽑아 freeze했다(run `20260810T003840` 환경 pin,
  freeze `2a0a48cf243655e4…`): RR normal band `[0.9827, 1.0304]`
  (DS1 N beats 45,845개) · discordance threshold `2.000`
  (valid 50,690 beats의 p75).
- **DS2 gate 실측 (canonical `20260810T005802`)**: macro sensitivity 0.9476 ·
  macro PPV 0.8860 · many-to-one 0 · cross-beat 0 · 우연 대비 8.283×
  [7.460, 9.548]. per-record: `100` 0.997/0.990 · `103` 0.993/0.995 ·
  `117` 0.998/0.999 · `214` 0.952/0.847 · `222` 0.960/**0.487** ·
  `231` **0.786**/0.997 (sens/PPV).
- **자격검증이 통과하며 남긴 세 가지 — 조인·association 설계에 직접 걸린다:**
  1. per-record floor 가 **정확히 최소 통과선 5/6**(여유 0). `222` 가 PPV
     0.4873 으로 0.70 미달.
  2. `222` 의 PPV 상한이 **0.5075**(주석 1,257 대 검출 2,477)이고 도달률
     0.9602. **미주석 절반이 "라벨 안 된 P"인지 "P 가 없는 구간"인지 판별되지
     않았다.** 조인 설계가 `222` 를 포함한다면 이 미결을 어떻게 다룰지 적어라.
  3. **`231` 은 sensitivity 최저(0.7859)인데 Q5-A 에서 네 모델 모두의 worst
     quartile 에 들고 S PR-AUC 0.001–0.002 로 붕괴하는 record 다.** 측정 품질과
     모델 실패가 같은 record 에서 함께 나빠진다 → **association 이 찾는 연관의
     일부가 측정 품질의 공변일 수 있다. 교란으로 사전 등록해야 한다.**
- **DS1 dry report에서 나온 주의사항 둘** — Codex 설계에 영향을 줄 수 있다:
  1. **PPV에 구조적 상한이 있다.** `ppv/sens = n_expert/n_detected`이고,
     publisher가 모든 P를 라벨하지 않아 record 106은 상한 0.745에 0.742를
     찍었다(라벨된 P는 99.6% 찾음). DS1 macro PPV 0.754. 라벨 밀도가 곧
     PPV 천장이다.
  2. **discordance가 sample 해상도로 양자화돼 있다.** p75가 정확히 `2.000`인
     것은 record MAD가 대략 1 sample(2.78 ms)이라 discordance가 정수값을
     갖는다는 뜻이다. 임계값 근처에 질량이 몰리므로, **이 threshold로
     concordant/discordant를 가르는 후속 분석은 경계 처리 규칙을 명시해야
     한다**(≥ 인지 > 인지, 동률을 어디로 보낼지). 조인 설계에서 직접 쓰지는
     않지만 association 단계에서 바로 걸린다.

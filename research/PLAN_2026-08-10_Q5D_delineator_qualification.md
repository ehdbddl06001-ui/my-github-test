# EXP-2026-007 / Q5-D — delineator qualification 실행 초안

Status: **DRAFT — 실행 승인 전.** 이 문서는 새 과학 설계가 아니라, 이미 사전등록된
spec의 「Measurement qualification gate」를 **어떤 순서로 무엇을 돌릴지**로 옮긴
실행 계획이다. 과학적 질문·split·지표·중단 조건은 spec 그대로이며 바꾸지 않았다.

- 선행 조건: PREP_DATA-A `ACQUIRE_ONLY` accepted (canonical run `20260809T153151`, PR #72).
- 현재 실험 status: `approved_for_implementation`. **`MEASURED` 아님.**
- 이 단계 판정 코드: `MEASUREMENT_QUALIFIED` | `MEASUREMENT_UNQUALIFIED` | `QUALIFY_RESULT_NOT_RUN`

---

## 1. 실행 경계 — 무엇을 열고 무엇을 봉인하는가

qualification 은 **raw 자산과 전문가 주석만으로** 끝난다. 이 경계가 이 단계의 전부다.

| | 대상 | 이 단계에서 |
|---|---|---|
| 연다 | MIT-BIH raw 파형 `.dat`/`.hea` (48 records 취득본) | **열람** |
| 연다 | `.atr` — R 위치와 beat symbol | **열람** (R 위치는 재검출하지 않고 그대로 쓴다) |
| 연다 | `pwave 1.0.0` 전문가 P 주석 `.pwave` — DS1 6 + DS2 6 | **열람** |
| **봉인** | DS2 beat class label | **열지 않는다** |
| **봉인** | V10 확률·metric (`v10pkg_results/`) | **열지 않는다** |
| **봉인** | 처리 배열 `mamba_data.npz`·`ecg_multi.npz` | **열지 않는다** |

**중요한 구분**: gate item 3 은 "DS2 6 record 의 **전문가 P 주석**" 을 요구한다. 이것은
DS2 **outcome**(class label·모델 확률)이 아니다. P 주석 열람은 사전등록이 명시적으로
요구한 것이고, outcome 봉인은 그대로 유지된다. 코드에서 두 경로를 분리해 강제한다
(q5d ACQUIRE 모듈과 같은 `FORBIDDEN_TOKENS` 방식).

**이 단계에서 하지 않는 것**: beat join · P-to-R association · S PR-AUC · SHAM
permutation · 학습 · 파라미터 튜닝 · lead 교체 · 다른 delineator 시도.

---

## 2. record 배정 (검증됨)

pwave 1.0.0 의 12 record 를 repo 의 de Chazal split(`colab_crossdb.py:24-25`)에 대면
**정확히 6 / 6** 으로 갈린다. spec 이 "six DS1 / six DS2" 라고 쓴 근거가 이것이다.

| | records | 쓰임 |
|---|---|---|
| DS1 전문가 주석 | `101 106 119 122 207 223` | dry qualification report (튜닝 금지) |
| DS2 전문가 주석 | `100 103 117 214 222 231` | **단 한 번** 돌리는 gate 판정 |
| DS1 전체 | 22 records | frozen 상수 산출 (아래 §4) |

---

## 3. 단계 — 3-run 구조

freeze 를 실행 경계로 삼아 세 run 으로 쪼갠다. **QUALIFY-B 는 QUALIFY-A 가 상수를
저장한 뒤에만 돌 수 있고, 한 번만 돈다.**

### QUALIFY-0 — environment pin (파형 읽기 전) — **실행 완료**

spec: *"Pin and record the exact package version and source hash **before reading any
DS1 waveform**."* 그래서 별도 run 으로 앞에 뺀다.

- 기록: Python·OS·`neurokit2` 버전과 **소스 트리 SHA-256**·`wfdb`·`numpy`·`scipy`·`pandas`.
- 산출: `qualify/runs/<ts>/env_pin.json`
- 이 파일이 없으면 QUALIFY-A 가 시작을 거부한다(`env_pin_is_complete`).

**실측 (run `20260810T000629`, Colab, 파형 읽기 전)**

| package | version | .py files |
|---|---|---|
| `neurokit2` | 0.2.13 | 313 |
| `wfdb` | 4.3.1 | 28 |
| `numpy` | 2.0.2 | 400 |
| `scipy` | 1.16.3 | 961 |

**이 run 의 source SHA-256 값은 폐기했다 (2026-08-10 정정).** 그 값들은 임시
인라인 셀이 `os.walk` **순회 순서**로 해시한 것이고, 모듈의 `hash_source_tree` 는
**상대경로 정렬 순서**로 해시한다. 같은 파일·같은 내용이라도 두 순서는 다른 digest 를
내므로(로컬 재현: `numpy` walk `74ccf630…` vs sorted `ad55d46e…`) 두 값은 애초에
비교 대상이 아니었다. 그 값을 baseline 으로 박아둔 탓에 두 번째 실행이
`wfdb`·`numpy`·`scipy` 에서 DRIFT 를 보고했는데, **환경은 전혀 바뀌지 않았다** —
하위 디렉터리가 없는 패키지만 두 순서가 우연히 일치하고(`neurokit2` 가 그래서 통과),
나머지는 전부 어긋난 것이다.

고친 방식: **repo 에 hash 를 박지 않는다.** hash 를 박으면 그 hash 를 만든 알고리즘까지
박는 셈이다. 대신 첫 실행이 Drive 에 `qualify/env_pin_baseline.json` 을 쓰고, 이후
실행이 그 파일과 대조한다. pin 은 `hash_algo_version` 을 함께 들고 다니며, 버전이
다르면 "드리프트" 라고 말하지 않고 **비교 불가로 거부**한다.

**정정 — `pandas` 가 pin 목록에서 빠져 있었다.** 그 실행에서 `neurokit2` 설치가
`pandas` 를 2.2.2 → 2.3.3 으로 올렸고(`google-colab 1.0.0 requires pandas==2.2.2`
경고), `ecg_delineate` 는 pandas 를 거쳐 결과를 돌려주므로 버전이 결과에 닿을 수
있다. 모듈의 `PINNED_PACKAGES` 에 `pandas` 를 넣었으니, **셀 5를 한 번 더 돌려
pandas 까지 포함된 pin 을 만든 뒤 QUALIFY-A 로 넘어간다.** 위 네 값은 그때 다시
찍히며 동일해야 한다(다르면 환경이 바뀐 것이므로 멈추고 보고).

### QUALIFY-A — DS1 dry report + 상수 freeze

- delineator: NeuroKit2 `ecg_delineate(method="dwt")`, **channel 0 only**,
  R 위치는 `.atr` 참조값 사용(재검출 금지), 기본 파라미터 고정, sweep 금지.
- (a) DS1 전문가 6 record 에 돌려 **dry qualification report** 산출 — 민감도·PPV 를
  보되 **여기서 튜닝하지 않는다**. 이 수치는 gate 판정이 아니다.
- (b) DS1 22 record 전체에 돌려 frozen 상수 산출(§4).
- 산출: `ds1_dry_report.csv` · `frozen_constants.json` · `ds1_pr_distribution.csv`
- **`frozen_constants.json` 이 저장되는 순간이 freeze 다.** 이후 어떤 상수도 못 바꾼다.

### QUALIFY-B — DS2 gate (단 한 번)

- 입력: `frozen_constants.json`(해시 검증) + DS2 6 record raw + 전문가 P 주석.
- DS2 6 record 에 **한 번** 돌리고 ±50 ms 안에서 **1:1** 매칭.
- 산출: `pwave_qualification.csv` · `decision.json` · gate 카드.
- 판정: 아래 §5 전부 참이면 `MEASUREMENT_QUALIFIED`, 아니면 `MEASUREMENT_UNQUALIFIED` 후 **중단**.

### QUALIFY-REPORT — 저장 bundle 재표시 (재계산 없음)

---

## 4. Frozen 상수

| 상수 | 값 / 산출 방식 | 출처 |
|---|---|---|
| delineator | NeuroKit2 `ecg_delineate(method="dwt")`, channel 0 | spec |
| R 위치 | `.atr` 참조값 (재검출 금지) | spec |
| P 매칭 허용치 | **±50 ms** | spec gate item 2 |
| P 탐색 구간 | R 이전 **40–300 ms** | spec gate item 2 |
| `PR_ms` | `R_sample - P_peak_sample` | spec |
| `PR_discordance` | `abs(PR_ms - record_median_PR) / record_MAD_PR` (label-free, record 내 전 valid beat) | spec |
| RR normal band | DS1 **N beats** 의 `coupling_ratio` 중앙 사분위 구간 (두 끝점) | spec |
| discordance threshold | DS1 valid `PR_discordance` 의 **75th percentile** | spec |
| N 클래스 정의 | AAMI N = `{N, L, R, e, j}` | repo `svdb_labels.py:62` |
| `coupling_ratio` | `pre_rr / local_median_rr` | repo `q5a_patient_failure_atlas.py:2078-2085` |
| 상수 산출 범위 | **DS1 22 records 전체** | 사용자 결정 2026-08-10 (§7) |
| seeds | permutation master `2026007` · bootstrap master `2026008` | spec |

`coupling_ratio` 와 RR band 는 `.atr` 의 R 위치·symbol 만으로 계산된다 — 처리 배열이나
DS2 를 건드리지 않는다. discordance threshold 만 delineator 출력을 필요로 한다.

---

## 5. Gate 판정 기준 (spec 원문 그대로, 완화 금지)

`MEASUREMENT_QUALIFIED` 는 **다섯 개가 전부 참일 때만** 나온다.

1. DS2 record-macro P-peak **sensitivity ≥ 0.80**
2. DS2 record-macro **PPV ≥ 0.80**
3. DS2 6 record 중 **최소 5개**가 sensitivity·PPV **≥ 0.70**
4. many-to-one 또는 cross-beat 조인이 **한 record 도 없음**
5. true P-match rate 가 **record 내 circular-shift 우연 수준의 4배 이상**이고,
   그 **record-bootstrap 95% CI 하한이 1배 초과**

- 하나라도 실패 → `MEASUREMENT_UNQUALIFIED` **즉시 중단**. 창 넓히기·다른
  delineator·더 좋아 보이는 lead·수동 제외는 이 실험 안에서 **금지**.
- 공개 자원 경고("모든 P 파가 라벨된다고 보장하지 않는다")를 **한계로 보고**한다.
  DS2 를 본 뒤 임계값을 낮추지 않는다.

---

## 6. 산출물

`MyDrive/MedKOS/ecg-model/assets/EXP-2026-007_prep_data/qualify/` 아래에 두고,
ACQUIRE 와 같은 방식으로 `runs/<timestamp>/` 에 불변 사본을 남긴다.

`env_pin.json` · `config.json` · `manifest.json` · `frozen_constants.json` ·
`ds1_dry_report.csv` · `ds1_pr_distribution.csv` · `pwave_qualification.csv` ·
`chance_null.csv` · `decision.json` · `log.txt` · `summary.md`

**canonical evidence 는 notebook 출력이 아니라 이 bundle 이다** (PREP_DATA-A 와 동일 원칙).

---

## 7. Decision log (이 초안에서 확정한 것)

- **2026-08-10 — frozen 상수 산출 범위 = DS1 22 records 전체.** spec 은 "DS1 75th
  percentile" 이라고만 쓰고 record 범위를 못박지 않았다. 전문가 주석 6 record 로
  제한하면 싸지만 DS1 을 대표하지 못한다. 사용자가 전체 22 record 를 택했다.
  RR band 도 같은 범위로 통일한다. Colab 시간이 늘어나는 것이 비용이다.
- **2026-08-10 — 실행 경계 분리(병렬 진행).** Claude 는 raw MIT-BIH + 전문가 P 주석
  만으로 qualification 을 구현·실행한다. Codex 는 **동시에** beat-join 을 설계만
  한다(§8). qualification 실패 시 과학 실험은 `MEASUREMENT_UNQUALIFIED` 로 종료하고
  join·association 은 **실행하지 않는다**. 통과해도 join 실행은 설계 검토 + **별도
  승인** 후에만 진행한다.

---

## 8. Codex 병렬 과제 — beat-join 설계 (설계만, 실행 금지)

### 문제

spec 의 PREP_DATA gate item 3 은 `.atr` R sample 을 등록된 처리 beat identity 에
`(record, sample)` 로 조인하라고 요구한다. **이 조인은 이미 실패한 것으로 실측됐다.**

- Q5-A 실측: `t` ↔ `.atr` sample 조인 성공률 **1.9% = 우연 수준**
  (최근접 주석까지 중앙 거리 0.222×RR) → 동결 source 의 `t` 는 annotation sample index 가 아니다.
- Q5-B-0: RR 키 조인 25.9% → v5 동점 규칙으로 90.5% 까지 올렸으나
  `subtype_coverage_balance` 0.368 로 gate 탈락.

즉 qualification 을 통과해도 **PR_discordance 를 V10 이 채점한 beat 에 붙일 키가 없다.**
association 단계는 여기서 막혀 있다.

### 쓸 수 있는 것 / 열지 말 것

- 쓸 수 있다: synthetic fixture · DS1 · Q5-B-0 의 drop map
  (버려진 818박 = N 1 · **S 0** · V 0 · **F 802** · Q 15, 92%가 208·213)
  · record 동일성 44개 확립 사실 · **per-record S 불일치 0**.
- **열지 말 것: DS2 outcome (class label · V10 확률).**

### 요구 산출물 (실행 아님)

1. 조인 규칙 하나 — 예컨대 record 내 순서 정렬 + drop map 보정처럼, `t` 를
   sample index 로 가정하지 않는 경로.
2. **음성대조군** — wrong-record·순서 셔플·circular shift.
3. **영가설과 신호/영가설 비** 산출 방식.
4. **중단 기준** — 어느 커버리지·정확도 아래면 `JOIN_UNRESOLVED` 로 종결하는지.
   Q5-B-0 처럼 "부분 조인으로 선택 편향된 부분집합을 쓰지 않는다" 원칙 유지.
5. 조인이 원리적으로 불가하면 그 결론 자체가 유효한 산출물이다.

---

## 9. Colab 실행 순서 (사용자용)

| # | run | 무엇을 | 대략 시간 | 선행 |
|---|---|---|---|---|
| 0 | QUALIFY-0 | environment pin 저장 | < 1 분 | 없음 — **지금 바로 가능** |
| 1 | QUALIFY-A | DS1 6 dry report + DS1 22 상수 freeze | 30–60 분 | QUALIFY-0, 모듈 구현 |
| 2 | QUALIFY-B | DS2 6 gate 판정 (단 한 번) | 10–15 분 | `frozen_constants.json` |
| 3 | QUALIFY-REPORT | 저장 bundle 재표시 | < 1 분 | QUALIFY-B |

시간은 360 Hz · 30분 record 기준 어림이고 hard gate 가 아니다.

**지금 돌릴 수 있는 것은 0번뿐이다.** 1–3 번은 qualification 모듈이 아직 없어서 못 돈다
(현재 q5d 모듈은 ACQUIRE 전용이고, `FORBIDDEN_TOKENS` 로 delineation 경로 자체가 막혀 있다).
0번을 먼저 돌려두면 "파형 읽기 전에 환경을 고정했다" 는 순서 요구가 충족된 채로 시작할 수 있다.

---

## 10. 구현 전 걸리는 것 — spec 의 허용 파일 목록

spec 「Files allowed to change during implementation」은 네 파일만 허용한다:

- `experiments/specs/EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md`
- `mit-bih/q5d_expert_validated_pwave_timing.py`
- `mit-bih/test_q5d_expert_validated_pwave_timing.py`
- `notebooks/quest47_q5d_expert_validated_pwave_timing.ipynb`

qualification 을 구현하려면 둘 중 하나가 필요하고, **어느 쪽이든 spec 개정 사항**이다.

- **A. 기존 q5d 모듈을 확장** — 그런데 그 모듈은 `assert_acquire_only` 와
  `FORBIDDEN_TOKENS`(`delineate` 등)로 **delineation 경로가 존재하지 못하게** 스스로를
  막고 있다. 확장하려면 그 안전장치를 풀어야 하는데, ACQUIRE 단계의 보증이 약해진다.
  **권장하지 않는다.**
- **B. 새 모듈 파일을 추가**(예: `mit-bih/q5d_qualify_pwave_delineator.py` +
  테스트 + `notebooks/quest53_q5d_qualify_pwave_delineator.ipynb`) 하고 spec 의 허용
  목록에 세 파일을 더한다. ACQUIRE 모듈은 잠긴 채로 남는다. **권장.**

**2026-08-10 확정: B 를 택했다.** 사용자 승인으로 세 파일을 추가하고 spec 의 허용
목록에 등재했다. ACQUIRE 모듈은 손대지 않았다 — `assert_acquire_only` 와
`FORBIDDEN_TOKENS` 가 그대로 남아 있고, 그 모듈의 220 checks 도 그대로 통과한다.

새 모듈도 같은 방식으로 자신을 잠근다: `assert_qualify_only` 가 소스에서
`v10pkg`·`mamba_data`·`ecg_multi`·`core_membership`·PR-AUC 계열·학습 호출을 텍스트로
금지한다. 즉 **자격검증 모듈은 outcome 에 닿는 코드를 가질 수 없다.**

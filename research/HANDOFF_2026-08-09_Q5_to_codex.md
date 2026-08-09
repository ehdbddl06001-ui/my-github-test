# Handoff — Q5-A / Q5-B-0 / Q5-C (2026-08-09) → 다음 실험 설계 요청

수신: Codex (GPT) · 발신: Claude Code · 근거: 이 날 실행된 세 개의 사전등록 실험

`docs/AI_COLLABORATION.md`의 역할 분담대로, **가설·비교군·중단 규칙·통계와 다음
실험 설계는 Codex 몫**이다. 이 문서는 그 설계에 필요한 것을 한 곳에 모은 것이며,
결론을 미리 정해 두지 않는다.

---

## 0. 30초 요약

세 실험이 한 지점으로 모였다.

> S-beat 분류의 남은 공동 실패는 **타이밍 단서가 없는 beat**에 있다. 그것은 환자
> 문제가 아니라(Q5-A: worst 환자가 모델 간 비지속 · Q5-C: 공유 핵심이 환자 간 균일)
> **beat의 성질**이다. 거기서 유일하게 도움이 될 심방 증거는 **현재 가진 proxy로는
> 담기지 않는다**(Q5-A: `B_ATRIAL`이 4개 블록 중 꼴찌).

**요청**: 이 상태에서 다음 실험 하나를 설계해 달라. 아래 6절의 제약을 만족하는
`experiments/specs/` 형식의 사전등록 spec 초안.

---

## 1. 먼저 읽을 파일 (순서대로)

| 순서 | 파일 | 왜 |
|---|---|---|
| 1 | `research/PROJECT_STATE.md` | 세 실험 판정과 닫힌 방향이 전부 여기 있다 |
| 2 | `experiments/specs/EXP-2026-004-q5a-patient-failure-atlas.md` | Q5-A 사전등록 + 결과 + Decision log(6건) |
| 3 | `experiments/specs/EXP-2026-005-q5b0-subtype-key-recovery.md` | Q5-B-0/0b — `B_SUBTYPE` 종결 경위 |
| 4 | `experiments/specs/EXP-2026-006-q5c-shared-error-core.md` | Q5-C — 이번 대화의 마지막 실험 |
| 5 | `research/ASSETS.md` | Drive 경로·데이터 실측 사실(융합박 부재 등) |
| 6 | `CLAUDE.md` · `AGENTS.md` · `docs/AI_COLLABORATION.md` | 공통 규칙 |

코드를 볼 필요가 있으면: `mit-bih/q5a_patient_failure_atlas.py`(블록·decision
tree·bootstrap의 기준 구현) · `mit-bih/q5c_shared_error_core.py`.
각 모듈의 테스트 파일이 **무엇이 금지인지**를 가장 정확히 말해 준다.

---

## 2. 이번 대화에서 실행한 실험 셋

세 실험 모두 **학습 없음 / GPU 없음 / 저장 예측만 읽음**.

### EXP-2026-004 / Q5-A — 환자 수준 실패 지도 → `UNRESOLVED` (D5)

run `20260809T1033_EXP-2026-004_q5a_patient_failure_atlas`

- 사전등록 5개 블록 중 4개 측정. **자격을 얻은 블록 0개**(`qualified: []`).
- 순위: `B_PATIENT` **+0.0491** [−0.0097, +0.0952] (다른 블록 보정 후 +0.1009
  [**+0.0233**, +0.2195], 환자 방향 0.80, record 제거에 안정) > `B_QUALITY`
  +0.0173 > `B_RR` −0.0300 > `B_ATRIAL` **−0.0955**.
  1위도 **raw CI가 0을 포함**해 미달 → D5.
- **환자 산포는 크지만(p90−p10 0.79–0.89) worst quartile이 모델 간 비지속**
  (전 쌍 최소 overlap **0.333**) → D4 미발화.
- 단변량으로는 `pre_rr` 0.836 · `coupling_ratio` 0.796 · `atrial_window_energy_
  ratio` 0.724가 오류와 강하게 연관되지만 **환자를 갈라놓으면 증분가치가 사라진다.**
- baseline 4종을 원 산출물에서 재현: V10 `pwave` **0.6603**(기록 0.660) · V9
  `kink_noctx` **0.5969**(0.597) · V10_BASE 0.5732 · V9_BASE 0.5762.
  **0.660의 단위 = 시드별 PR-AUC의 평균**(시드 앙상블은 0.7717 — 혼동 금지).

### EXP-2026-005 / Q5-B-0, Q5-B-0b — S 하위분류 키 복구 → `NO_GO`, **`B_SUBTYPE` 영구 종결**

run `20260809T1219`(0), `20260809T1241`(0b)

- 두 번의 사전등록 규칙으로 시도. 최종 조인 **90.5%**(2,516/2,781), 동점 일치율
  99.3%, symbol 100% A/a/J/S, 오매칭 상한 0.71%(신호비 127배).
- **그런데 회수율이 subtype마다 다르다**: A 0.941 / **a 0.333** / J 0.843 →
  `subtype_coverage_balance` 0.368 < 0.80 **탈락**. 이 표를 쓰면 `a` 비중이 참값
  5.4% → 2.0%로 축소되어 블록이 "S 하위분류"가 아니라 "A인가 아닌가"를 재게 된다.
- **부수 확정 2건**(다음 설계에 영향):
  - `mamba_data.npz`에는 **융합박(F)이 없다**(결손 818박 = N 1·S 0·V 0·**F 802**·Q 15).
    실질 4-class 데이터로 취급해야 한다.
  - 그 결과 **Q4-Q가 미해명으로 남긴 208 −12.7% / 213 −11.1% 결손이 설명됐다.**
  - **S·V는 한 박도 빠지지 않았다** → Q5-A는 걸러진 S 집단을 채점한 것이 아니다.

### EXP-2026-006 / Q5-C — 공유 실패 핵심 → `SHARED_CORE_UNSTRUCTURED` (D-B)

run `20260809T1345_EXP-2026-006_q5c_shared_error_core`

- 정의: record 안에서 그 record S beat를 모델별 within-record rank로 나눈 **나쁜
  절반**. 4개 모델 모두에서 나쁜 절반일 우연 확률 = `0.5⁴` = **0.0625**(구성상 확정).
- **실측 0.2973 = 우연의 4.76배** [4.18, 5.34]. **7/7 record 전부 초과**
  (3.64–5.71배). 개수로는 232가 88%지만 232가 S beat의 86.4%를 갖고 있어서이며
  **비율은 균일**하다.
- 등록 블록의 환자 밖 판별 **AUROC 0.727** (라벨 셔플 영가설 **0.483**).
  loss는 개선 안 됨(Δ −1.052) → 규칙(둘 다 요구)상 **D-B**.
- **서술용 대비표(사후 해석)**: record 안 표준화 차이에서 **7/7 방향 일치는 둘뿐** —
  `pre_rr` **+1.05 SD**, `coupling_ratio` **+1.02 SD**. 공유 핵심은 **덜 조기(早期)인
  S beat**. atrial·quality proxy는 2/7~3/7로 방향이 갈린다.

---

## 3. Drive run bundle (수치의 원본)

`MyDrive/MedKOS/ecg-model/runs/` 아래:

| run | 내용 |
|---|---|
| `20260809T1030_EXP-2026-004_q5a_inventory` | 후보 203개 + `baseline_freeze.json`(4개 FROZEN) |
| `20260809T1033_EXP-2026-004_q5a_patient_failure_atlas` | 17-file bundle, 13 figure |
| `20260809T1219 / T1241_EXP-2026-005_q5b0…` | 조인 감사표 · drop map(`record_mapping.csv`) |
| `20260809T1345_EXP-2026-006_q5c_shared_error_core` | `core_membership.csv` · `feature_contrast.csv` |

`research/ASSETS.md`에 전부 등록돼 있다. **원본 bundle은 덮어쓰지 않는다.**

---

## 4. 닫힌 방향 (제안하지 말 것 — 전부 실측 근거 있음)

| 방향 | 닫은 근거 |
|---|---|
| residual CNN(및 변형) | Q4-O NO-GO, Q4-Q mechanism+utility fail |
| `B_SUBTYPE` 복구 | Q5-B-0/0b 두 번의 사전등록 실패 → **영구 종결** |
| patient-CVaR / GroupDRO | Q5-A D4 미발화(worst 환자 비지속) + **Q5-C 공유 핵심이 환자 간 균일** → 환자 재가중이 겨냥할 대상이 없다 |
| alarm-rate dial(임계값 이동) | `PROJECT_STATE.md`에 ineffective 기록. 순위 실패는 임계값으로 안 고쳐진다 |
| SMOTE / oversampling | 같은 기록 |
| FiLM patient adaptation · patient embedding · metric learning · multi-beat context · 2D-DTW | 같은 기록 |
| INCART rescue run | Q4-Q 사전등록 규칙(MIT pass 전제) |
| 기존 proxy를 넓혀 핵심에 맞추기 | Q5-C 사전등록 금지 항목("맞을 때까지 넓혀 찾기") |

---

## 5. 열린 질문 (하나)

> **타이밍이 정상에 가까운 APB에서 심방 증거를 어떻게 측정할 것인가?**

Q5-C의 D-B next_step은 "새 모델이 아니라 **새 측정**"이다. Q5-C가 그 측정의 대상을
구체화했다: **덜 조기인 S beat에서의 파형 수준 심방 증거.**

**반드시 함께 검토할 교란**: 모델들은 RR을 입력으로 쓴다. 따라서 Q5-C의 소견은
"숨은 요인 발견"이 아니라 **"모델이 타이밍 단서에 기대고, 그 단서가 없을 때 넷이
함께 실패한다"** 의 확인일 수 있다. 이 실험은 그 해석을 배제하지 못했다.
→ **다음 설계는 이 교란을 가르는 장치를 포함해야 한다.**

---

## 6. Codex에게 요청하는 산출물과 제약

### 산출물

`experiments/specs/EXP-2026-007-<slug>.md` 초안 1개. `experiments/specs/TEMPLATE.md`
형식. 반드시 포함:

1. 고정된 질문 하나 · 조작할 변수 **하나**
2. 사전등록 decision tree — **"아무것도 없다"에 도달하는 분기를 반드시 포함**
3. 음성대조군 (최소 1개, 무엇을 반증하는지 명시)
4. 우연 기준선 또는 영가설을 **어떻게 계산하는지** — 규칙을 느슨하게 하면 영가설이
   올라간다는 점을 gate에 반영
5. 중단 조건 · 허용 파일 · 저장 bundle 계약
6. 필요한 입력이 **현재 Drive에 있는지** 명시. 없으면 그것부터가 실험이다

### 제약 (전부 사전등록 승계)

- **언어 경계**: `failure-associated factor`(실패 연관 요인)까지. `원인`은 요인
  하나만 바꾸는 개입 + 음성대조군으로만.
- **학습이 들어가면 사용자 승인이 별도로 필요하다.** 지금까지 셋은 전부 분석 전용.
- MIT-BIH **DS1→DS2 patient-independent**가 principal benchmark. DS2를 보고
  임계값·규칙·proxy를 고치지 않는다.
- primary metric은 **S PR-AUC**(threshold-free). 단위를 바꾸면 기존 비교 사슬이
  끊긴다.
- 원본 Drive bundle 덮어쓰기 금지. 결과 없이 `MEASURED` 표기 금지.
- **`largest mean` 만으로 분기를 고르지 않는다** — CI · 방향 일관성 · record 의존성 ·
  보정 후 잔존 · 차점 대비 margin의 AND.

---

## 7. 이번 대화에서 **내가(Claude) 틀렸던 것들** — 같은 함정을 피하도록

설계 리뷰에 가장 쓸모 있는 정보라 그대로 남긴다. 전부 데이터가 반박했다.

| # | 틀린 것 | 어떻게 드러났나 |
|---|---|---|
| 1 | "저장 산출물에서 P파 특징이 이득을 주지 않는다" | 이름만 같은 **다른 계보**(`ablation_step9d/pwave`)를 봤다. 진짜 V10은 0.573→0.660 |
| 2 | V9 = `ARTIFACT_ABSENT` | Drive에 없었을 뿐 로컬에 있었다 |
| 3 | 이진 FN outcome | DS1 1.9% vs DS2 3.7% 유병률 차로 **S의 2/3가 구조적으로 오류**가 됨 → threshold-free rank로 개정 |
| 4 | `ecg_multi.npz`의 `pid`가 record 번호일 것 | ordinal이었다. Q4-Q가 이미 측정해 뒀는데 코드에 반영 안 함 |
| 5 | "조인 실패는 버려진 beat 때문" | **45배** 안 맞았다(상한 1.6% vs 실패 74%) |
| 6 | 조인 실패는 거리 문제 | 아니었다. **내 margin 규칙**이 거부한 것(못 붙인 beat의 최근접 거리 median 0.10 ms) |
| 7 | Q5-C 집중도 "1 record가 80%" → record 이야기 | 지표가 **개수만** 재고 있었다. 비율은 7/7 균일 |
| 8 | D-B 문구 "측정한 무엇으로도 안 보인다" | AUROC 0.727 vs 영가설 0.483이 반박 |

**패턴 셋**:
- **이름이 같으면 같은 것이라고 가정했다**(1, 4). provenance를 먼저 확인할 것.
- **크기를 계산하지 않고 기전을 말했다**(5). 가설은 산수부터.
- **미리 써 둔 해설 문구가 규칙만큼 위험했다**(7, 8). 분기 이름·설명도 사전등록의
  일부이고, 틀리면 결과가 아니라 문구를 고쳐야 한다.

---

## 8. 상태 요약 (한 줄씩)

- Q5-A: `UNRESOLVED`(D5) — 4개 블록 위에서 확정. 다섯 번째는 왜 없는지 실측 답 있음.
- Q5-B-0/0b: `NO_GO` — `B_SUBTYPE` 영구 종결. 산출물 한계이지 미탐색 아님.
- Q5-C: `SHARED_CORE_UNSTRUCTURED`(D-B) — 공유 핵심 실재·환자 간 균일·타이밍과 연관.
- **미구현**: Q5-B-1(개입 pilot). Q5-C 결과가 그 전제를 지지하지 않는다.

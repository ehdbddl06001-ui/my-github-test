# ECG research project state

Updated: 2026-08-09

## EXP-2026-004 / Q5-A — MEASURED (2026-08-09), 판정 `UNRESOLVED` (D5)

run `20260809T1033_EXP-2026-004_q5a_patient_failure_atlas` · 모듈 q5a v8 ·
`training_performed: false`. 사전등록 decision tree에서 **자격을 얻은 block이
하나도 없다**(`qualified: []`).

- block 순위(primary = `within_record_rank`, 환자-grouped holdout, S beat 1,628 ·
  환자 15): `B_PATIENT` **+0.0491** [−0.0097, +0.0952] (다른 block 보정 후
  +0.1009 [**+0.0233**, +0.2195], 환자 방향 0.80, record 제거에 안정) ·
  `B_QUALITY` +0.0173 · `B_RR` −0.0300 · `B_ATRIAL` −0.0955.
  1위인 `B_PATIENT`도 **raw CI가 0을 포함**해 분기 자격 미달 → D5.
- 환자 산포는 크지만(`p90−p10` 0.79–0.89) **worst quartile이 모델 간에 지속되지
  않는다**(전 쌍 최소 overlap 0.333) → D4 미발화. 네 모델 모두의 worst quartile에
  드는 record는 `219`·`231` 둘뿐이며 231은 어디서나 붕괴한다(S PR-AUC 0.001–0.002).
  V10 대 V9_BASE는 S beat 1,628개 중 **710개(43.6%)를 둘 다 틀린다**.
- `B_SUBTYPE`은 **측정 불가**: `.atr` 조인 성공률 1.9% = 우연 수준(최근접 주석까지
  중앙 거리 0.222×RR). 동결 source의 `t`는 annotation sample index가 아니다.
  없는 것을 추정으로 채우지 않았다.
- 단변량으로는 `pre_rr`(0.836)·`coupling_ratio`(0.796)·
  `atrial_window_energy_ratio`(0.724)가 오류와 강하게 연관되지만, **환자를 갈라
  놓으면 증분가치가 남지 않는다** — 연관의 상당 부분이 환자 간 차이로 흡수된다.
- 이것은 `원인`이 아니라 **실패 연관 요인**이다. 인과는 Q5-B에서 요인 하나만 바꾸는
  개입 + 음성대조군으로만 검증한다.
- **다음 단계(사전등록 D5 next_step: "가장 저비용의 추가 측정 또는 artifact 보강")**:
  ① `B_SUBTYPE` 복구 측정, ② 그 뒤에도 자격 block이 없고 `B_PATIENT`가 1위면
  objective 하나만 바꾸는 DS1-only patient-CVaR pilot. 자세한 내용은 spec의
  「Q5-B design brief」.

## EXP-2026-005 / Q5-B-0 — MEASURED (2026-08-09), 판정 `NO_GO_SUBTYPE_CLOSED`

run `20260809T1219_EXP-2026-005_q5b0_subtype_key_recovery`(진단 포함 최종;
앞선 `…T1156`은 모듈 v2 이력) · 학습 없음.
**`B_SUBTYPE`은 이 사전등록 아래에서 종결**이고, Q5-A의 `UNRESOLVED`(D5)는 4개
블록 위에서 그대로 유지된다. symbols를 붙이지 않았고 재분석도 돌리지 않았다.

- 실패한 검사: `s_match_fraction` **0.2593**(≥0.95) · `content_anchor_fraction`
  **0.1981**(≥0.50) · record floor 18/32.
- 통과한 검사가 더 많은 것을 말해준다: 매칭된 **721박의 symbol이 100% A/a/J/S**
  (matcher가 볼 수 없는 값) · wrong-record 영가설 **0.48%** · 신호/영가설 **54배**
  · 매칭 잔차 median **1.4 ms** · 순서 뒤섞기 불변 · record 동일성 44개 확립
  (leftover 4개 = paced) · **per-record S 개수 불일치 0**.
- 복구된 분포도 임상적으로 타당: **A 627 · a 32 · J 61 · S 1**.
- 즉 **같은 S beat 집합인데 80%에서 RR이 5 ms 안에 안 들어온다.** 26%만 붙은 채
  부분 사용하는 것은 하지 않는다 — 그 26%는 RR 일치를 조건으로 뽑힌 부분집합이라
  선택 편향이다.
- **"버려진 beat 때문"이라는 첫 설명은 철회했다** — 크기가 45배 안 맞는다.
  cohort에 없는 beat는 818박(**0.81%**, 90%가 208·213)뿐이고, 이웃 소실로 RR이
  오염될 수 있는 생존 beat는 상한이 **1.64%** 인데 실제 실패는 **74.1%** 다.
- 대신 이 계산에서 확정된 것: **버려진 beat 중 S는 0박**(per-record S 불일치 0).
  즉 **Q5-A는 걸러진 S 집단을 채점한 것이 아니다.** v4가 이 drop map을
  record별·클래스별로 `record_mapping.csv`에 남긴다.
- **진단 실측(run `20260809T1219`)으로 원인이 밝혀졌고, 내가 적어둔 후보 셋은
  전부 틀렸다.** 못 붙인 2,230박의 최근접 후보 거리는 p50 **0.10 ms** · p90
  6.90 ms · 허용치 2배 안 **93.8%** — **멀어서 탈락한 게 아니라 margin 규칙 때문에
  탈락했다.** 360 Hz에서 1 sample = 2.78 ms인데 5 ms margin은 차점이 ~3.6 sample
  떨어질 것을 요구한다. 한 record 안에서 coupling interval이 반복되면 만족 불가다.
  즉 이번 NO-GO는 "산출물이 부족하다"가 아니라 **"내 규칙이 조인을 거부했다"** 이고,
  종결의 성격은 **영구가 아니라 규칙 재설계 대상**이다.
- **같은 run의 별개 확정**: 버려진 818박은 N 1 · **S 0** · V 0 · **F 802** · Q 15
  — 사실상 **융합박(F) 전량**이다. `mamba_data.npz`에는 F가 없다. F 누락의 92%가
  208·213에 몰려 있어, Q4-Q가 "stricter preprocessing"으로 미해명 처리했던
  208 −12.7% / 213 −11.1% 결손이 **이것으로 설명된다**. Q5-A 영향: S PR-AUC의
  음성 pool에서 약 0.8%가 빠져 있다(인용 시 명시).

### Q5-B-0b (run `20260809T1241`) — **`B_SUBTYPE` 영구 종결**

동점 집합이 한 symbol로 일치하면 부여하는 규칙으로 다시 물었다. 규칙은 의도대로
작동했고, 바로 그 덕분에 이 산출물로는 안 된다는 것이 확정됐다.

- 좋아진 것: 조인 **25.9% → 90.5%**(2,516/2,781) · 동점 일치율 **99.3%** ·
  symbol이 AAMI S 집합 **100%** · 영가설 0.48% → **0.71%**(기준 5% 안) ·
  신호/영가설 54배 → **127배**. **규칙 완화의 대가는 오매칭이 아니었다.**
- 결정적으로 실패한 것 — subtype별 회수율: A **0.941** · **a 0.333** ·
  J 0.843 (`subtype_coverage_balance` 0.368 < 0.80). **빠진 10%가 드문 subtype에
  몰려 있다.** 이 표를 쓰면 `a` 비중이 참값 5.4% → 2.0%(**0.37배**)로 축소되어,
  블록이 "S 하위분류"가 아니라 **"A인가 아닌가"** 를 재게 된다.
- 기전은 사전 등록 때 예측한 그대로: `a`가 든 동점 집합은 대개 다른 구성원이 A라
  혼합이고, 규칙이 (올바르게) 부여를 거부한다. **더 똑똑한 규칙으로 풀 문제가
  아니다** — 동일성을 주장해야만 풀리는데 그것이 이 산출물이 못 지탱하는 것이다.
- 90.5%까지 올라와도 **실제로 식별된 beat는 19.8%(551박)** 뿐이다. 나머지는
  "누구인지는 모르나 symbol은 정해진다"이며 그 구분은 기록에 남는다.
- **세 번째 규칙은 만들지 않는다**(사전 등록 약속). 숫자가 좋아진 것은 약속을 깰
  이유가 못 된다. 이번 gate는 **"많이 붙었다"와 "쓸 수 있다"가 다르다**는 것을
  실측으로 구분해 준 사례로 남긴다.
- Q5-A의 `UNRESOLVED`(D5)는 4개 블록 위에서 **확정 유지**되고, 이제 그 4개에는
  "다섯 번째는 왜 없는가"에 대한 실측 답이 붙어 있다. 남은 다음 후보는
  **Q5-B-1(개입 pilot)** 이며 별도 승인 대상이다.

### 사전 등록 원문 (2026-08-09 승인, 변경 없음)

사용자가 Q5-B 진행을 승인해 **①(측정)** 을 사전 등록했다:
`experiments/specs/EXP-2026-005-q5b0-subtype-key-recovery.md`.

- 하는 일: 동결 cohort(`mamba_data.npz`)의 **S beat**에 `ecg_multi.npz`의 원
  annotation symbol을 되붙인다. 키는 `(pre_rr, post_rr)` 초 단위 — **beat 자신의
  성질만** 쓴다(이웃 RR을 넣으면 행 순서에 의존해 "pool을 섞어도 같은 결과"를
  증명할 수 없다). symbol은 매칭에 쓰지 않으므로 "매칭된 beat의 symbol이 A/a/J/S에
  드는가"가 **독립 검증**이 된다.
- 음성대조군 4종을 사전 등록: permutation(anchor 불변) · shift(대응이 한 칸
  밀리면 tolerance 밖) · wrong-record(오매칭률 **상한**) · shuffle(복구 symbol을
  record 안에서 섞으면 `B_SUBTYPE` 효과가 무너져야 한다).
- gate 실패 = `NO_GO_SUBTYPE_CLOSED` → `B_SUBTYPE` **영구 종결**, Q5-A의
  `UNRESOLVED`(D5)는 4개 블록 위에서 유지. 추정으로 채우지 않고 재학습하지 않는다.
- GO면 Q5-A의 `run_atlas`를 **수정 없이** 다시 호출해 5개 블록으로 decision tree를
  재평가한다. `B_SUBTYPE`은 Q5-A에서 이미 **개입 분기가 없는 서술 블록**이므로,
  이겨도 자동으로 모델 실험이 되지 않는다(D5로 간다).
- 학습·GPU 없음. 테스트 155개 통과(CPU). **Q5-B-1(개입 pilot)은 여전히 승인 전까지
  만들지 않는다.**

## EXP-2026-006 / Q5-C — MEASURED (2026-08-09), 판정 `SHARED_CORE_UNSTRUCTURED` (D-B)

run `20260809T1345_EXP-2026-006_q5c_shared_error_core` · 학습 없음 · S beat 1,600 ·
record 7.

- **공유 핵심은 실재하고 환자 간 균일하다**: record 평균 0.2973 = 우연(`0.5⁴`=0.0625)의
  **4.76배** [4.18, 5.34]. record별로 **7/7 전부 초과**(3.64–5.71배). 개수로는 232가
  핵심의 88%지만 232가 cohort S beat의 86.4%를 갖고 있어서다 — **비율은 균일**하다.
- **판정은 D-B지만 "안 보인다"가 아니다**: joint held-out **AUROC 0.727**(라벨 셔플
  영가설 **0.483**)로 등록 특징이 핵심을 환자 밖에서 실제로 순위 매긴다. 실패한 것은
  loss 기준(Δ −1.052 [−1.635, −0.546])이고, **환자 group 7개 중 하나가 86%를 차지하는
  설계에서 19-특징 적합이 환자 밖 확률 보정에 성공할 근거가 없다.** 내가 D-B에 미리 써
  둔 "측정한 무엇으로도 보이지 않는다"는 문구는 실측에 반박당해 수정했다(규칙 불변).
- **서술용 대비표(사후 해석)**: record 안에서 **7/7 방향이 일치하는 특징은 둘뿐**이고
  크기도 가장 크다 — `pre_rr` **+1.05 SD**, `coupling_ratio` **+1.02 SD**. 즉 공유
  핵심의 S beat는 **덜 조기(早期)** 다(직전 RR이 길고 결합 간격이 정상박에 가깝다).
  atrial·quality proxy는 방향이 record마다 갈린다(2/7~3/7).
- **교란(반드시 함께 읽을 것)**: 모델들은 RR을 입력으로 쓴다. 따라서 위 소견은
  "숨은 요인 발견"이 아니라 **"모델들이 타이밍 단서에 기대고, 그 단서가 없는 S beat
  에서 넷이 함께 실패한다"** 의 확인일 수 있다. 이 실험은 그 해석을 배제하지 못한다.
- **그래도 남는 문장**: 남은 공유 실패는 **타이밍 단서가 없는 S beat**에 몰려 있고,
  거기서 도움이 될 유일한 증거는 심방 증거인데 **Q5-A가 현재 atrial proxy로는 그
  증거가 담기지 않는다고 이미 측정했다**(`B_ATRIAL` 꼴찌, Δ −0.0955). 이 두 사실을
  나란히 놓은 것이 지금까지 도달한 가장 날카로운 지점이다.
- **함의**: D-B의 next_step("새 모델이 아니라 새 측정")의 대상이 구체화된다 —
  **타이밍이 정상에 가까운 S beat에서의 파형 수준 심방 증거**(proxy를 넓히는 것이
  아니라 새 측정). **Q5-B-1(patient-CVaR)은 이 결과로 지지되지 않는다** — 핵심이
  환자 간 균일하므로 환자 재가중이 겨냥할 대상이 아니다.
- 한계: 환자 group 7개(하나가 86%) · 서술 표는 사후 해석 · S가 8박 미만인 record 12개
  제외(cohort 19 중 7 사용).

### 사전 등록 원문 (2026-08-09, 변경 없음)

Q5-B-0/0b가 `B_SUBTYPE`을 종결한 뒤 남은 선택지는 ① 트리가 고르지 않은
patient-CVaR pilot 강행 ② Q5-A가 남긴 **미해석 사실** 측정 ③ 종료 였고, ②를
선택했다: `experiments/specs/EXP-2026-006-q5c-shared-error-core.md`.

- 묻는 것: V10과 V9_BASE(서로 다른 계보)가 S beat의 절반 가까이를 **동시에**
  틀리는데, 두 모델의 worst **환자**는 거의 안 겹친다(최소 overlap 0.333).
  환자 단위로는 비지속인데 beat 단위로는 지속되는 이 물건은 무엇인가.
- **43.6%는 설명 대상이 아니다.** 임계값 기반(Q5-A가 강등한 정의)이고, 두 모델이
  각자 나빠서 우연히 겹치는 몫이 **29.1%(474박)** 다 → 이름 붙일 가치가 있는 것은
  **초과분 1.50배**뿐이다.
- 난이도를 **record 안에서만** 정의한다(그 record S beat의 나쁜 절반). 그래서
  우연 기준선이 `0.5**4 = 0.0625`로 **계산 없이** 확정되고, Q5-A가 1위로 측정한
  환자 효과가 구성상 제거된다.
- 설명은 **Q5-A가 이미 등록한 블록**(`B_ATRIAL`·`B_RR`·`B_QUALITY`)으로만 시도.
  새 특징을 만들지 않는다. `B_SUBTYPE` 종결·`B_PATIENT`는 순환이라 제외.
- 분기: `NO_SHARED_CORE`(D-C, 내 표현이 틀렸다는 판정) · `SHARED_CORE_
  UNSTRUCTURED`(D-B, 실재하나 측정한 무엇으로도 안 보임 → 새 모델이 아니라 새
  측정) · `SHARED_CORE_STRUCTURED`(D-A, 후보 요인 **지목**이지 개입 승인 아님).
- 학습·GPU 없음. 테스트 90개 통과(CPU).
- **Q5-B-1은 만들지 않는다**: Q5-A의 트리가 patient-robust 분기를 **선택하지
  않았고**(D4 미발화), 지금 돌리면 트리가 안 고른 분기를 사람이 고르는 것이 된다.
  Q5-C 결과에 따라 그 전제가 살아나거나 죽는다.

## EXP-2026-007 / Q5-D — PREP_DATA-A `ACQUIRE_ONLY` accepted (2026-08-09)

- **PREP_DATA-A ACQUIRE_ONLY 인수 완료.** 판정 `PREP_DATA_ACQUIRED_VERIFIED`,
  gate 12/12 PASS, `first_stopping_reason: null`. canonical run
  `20260809T153151`; 최종 판정의 근거는 notebook 출력이 아니라 Drive audit bundle
  `…/assets/EXP-2026-007_prep_data/audit/runs/20260809T153151/` 이다.
  자산은 `research/ASSETS.md` 의 `data-mitdb-raw-100` · `data-pwave-raw-100` ·
  `run-20260809-q5d-prep-data` 세 행에 등록했다.
- **이것은 데이터 준비 성공일 뿐이고 EXP-2026-007 의 과학적 질문은 답해지지
  않았다.** spec status 는 `approved_for_implementation` 그대로이며 `MEASURED`
  가 아니다. 학습 · delineation · beat join · DS2 outcome 분석 · S PR-AUC ·
  SHAM permutation 은 하나도 수행하지 않았다.
- **다음에 올 수 있는 단계는 delineator qualification 하나뿐이다** (frozen
  delineator 를 DS1 전문가 주석 record 에서 자격검증).
- **아직 승인되지 않은 것**: 그 qualification 실행, DS2 label·V10 outcome 열람,
  association analysis, 그리고 모든 학습. 승인은 별도 결정으로만 이루어지며 이
  인수 기록은 승인이 아니다.

### QUALIFY (2026-08-10) — `MEASUREMENT_QUALIFIED`, gate 5/5

canonical run `20260810T005802` (freeze `20260810T003933`). 측정도구 자격검증만
통과했다. **EXP-2026-007의 과학적 질문은 여전히 답해지지 않았고** spec status는
`approved_for_implementation` 그대로다. 학습·beat join·association·S PR-AUC·SHAM은
하나도 수행하지 않았다(`training_performed`·`model_scored`·`ds2_outcome_opened`·
`association_performed` 전부 false).

- 고정 규칙: neurokit2 0.2.13 `ecg_delineate(method="dwt")` · channel 0 ·
  R은 `.atr` 참조값(재검출 없음) · P 탐색 40–300 ms · 매칭 ±50 ms 1:1.
  frozen `2a0a48cf243655e4…`. DS1 22 records에서 뽑은 상수: RR normal band
  `[0.98268, 1.03043]`(N beats 45,845) · discordance threshold `2.000`
  (valid 50,690 beats의 p75).
- DS2 6 records(`100 103 117 214 222 231`) 실측: macro sensitivity **0.9476** ·
  macro PPV **0.8860** · cross-beat 0 · many-to-one 0 ·
  우연 대비 **8.283×** [7.460, 9.548]. 전 record cross-beat 0.
- **통과했지만 여유가 없다 — per-record floor가 정확히 5/6**(필요 5). `222`가
  PPV 0.4873으로 0.70 미달이다. record 하나만 더 흔들렸으면 떨어졌다.
- **`222`의 낮은 PPV는 대부분 구조적이다**: 주석 1,257개 대 검출 2,477개라
  PPV 상한이 **0.5075**이고 도달률은 0.9602다. 다만 **미주석 절반이 "라벨 안 된
  P"인지 "P파가 없는 구간"인지 이 run으로는 판별되지 않는다.** 두 해석의 함의가
  정반대다 — 전자면 delineator는 멀쩡하고, 후자면 P가 없는 자리에 P를 찍고 있다.
  `222`의 `PR_discordance`를 association에서 쓰려면 **먼저 이걸 가려야 한다.**
- **`231`은 sensitivity 최저(0.7859)인데, Q5-A에서 네 모델 모두의 worst quartile에
  들고 S PR-AUC 0.001–0.002로 붕괴하는 바로 그 record다.** 측정 품질과 모델
  실패가 같은 record에서 함께 나빠진다 → association이 "P 타이밍이 실패와
  연관"을 찾더라도 일부는 측정 품질의 공변일 수 있다. **교란으로 사전 등록해야
  한다.**
- 전체 macro `ppv_vs_ceiling` 0.9834 — 라벨된 P에 한해서는 거의 다 찾았다.
- 부수 관찰: discordance threshold p75가 정확히 `2.000`이다. record MAD가 대략
  1 sample(2.78 ms)이라 discordance가 정수로 양자화됐다는 뜻이고, 임계값 근처에
  질량이 몰린다. association에서 concordant/discordant를 가를 때 **경계 처리
  규칙(≥ 인지 > 인지, 동률 처리)을 명시해야 한다.**
- **다음 단계는 여전히 자동 실행되지 않는다.** beat join과 association은 설계
  검토 + 별도 승인이 필요하고, beat join 자체가 Q5-A 실측(조인 1.9% = 우연
  수준)으로 막혀 있다. Codex가 병렬로 설계 중이다
  (`research/HANDOFF_2026-08-10_Q5D_beat_join_to_codex.md`).

## 설계 원칙 (Q5-A 사전등록 — 변경 없음)

residual CNN 경로가 닫힌 뒤의 다음 단계는 **새 모델이 아니라 실패 지도**다.
`EXP-2026-004 / Q5-A`(`experiments/specs/EXP-2026-004-q5a-patient-failure-atlas.md`)
는 **재학습 없이** 저장된 예측만 읽어 어떤 환자·beat·상황에서 S-beat 분류가
실패하는지 지도로 만들고, 다음 실험에서 검증할 **단 하나의** 개입 가설을
사전등록 decision tree로 고른다.

- kind `preregistered_analysis_only` · 학습 금지 · 원본 run bundle 변경 금지 ·
  DS2 정보로 threshold/bin/proxy/branch rule 변경 금지.
- 언어 경계: Q5-A가 말하는 것은 **failure-associated factor(실패 연관 요인)**
  까지다. `원인`은 Q5-B에서 그 요인 하나만 바꾸는 개입 + 음성대조군으로 검증한다.
- 판정 후보: `Q5B_QUALITY_GATE_OR_PREPROCESSING` · `Q5B_ATRIAL_EVIDENCE_BOTTLENECK`
  · `Q5B_HIERARCHICAL_RR_ATRIAL_MODEL` · `Q5B_PATIENT_ROBUST_OBJECTIVE_PILOT` ·
  `UNRESOLVED` · `INSUFFICIENT_ARTIFACTS` / `DATA_INTEGRITY_BLOCKED`.
  근거가 부족하면 억지로 다음 모델을 고르지 않는다.
- 첫 임무였던 "V9 0.597 / V10 0.660을 실제 저장 산출물과 대조해 확정"은 **완료**
  됐다 — 네 arm 모두 artifact 자신의 cohort에서 `consistent`(아래 Current
  benchmark 참조).
- 분기 선택 규칙은 `largest mean` 단독이 아니라 raw CI · adjusted CI · 환자 방향
  일관성(≥0.60) · 상위 2 record 제거 후 생존 · 차점 대비 1.25배 margin의 **AND**
  다. 이번 실측에서 이 AND를 통과한 block은 없었고, 규칙을 결과에 맞춰 완화하지
  않았다.

## Measured results (Q4-O / Q4-P) and the next step (Q4-Q)

- **EXP-2026-001 / Q4-O (MEASURED, NO-GO)** — SVDB leakage-free residual CNN.
  run `20260806T0923`, commit `624e987b`. Arm C가 25/25 (seed×fold)에서
  `best_epoch = 0`(첫 학습 epoch 완료 후) 체크포인트를 선택했고 utility 이득
  없음. epoch −1(학습 전)은 dev 후보로 평가되지 않았으므로 원인은 Q4-O만으로
  판정 불가였다.
- **EXP-2026-002 / Q4-P (MEASURED, verdict `B3_lr_or_alpha_overshoot`)** —
  run `20260808T1310`, code SHA `a4e24f4d…`, data SHA `892f6ae9…`. 사전 등록
  decision tree에서 **B3 단독 발화**: alpha LR만 1e-4로 낮춘 S2에서 best
  epoch가 뒤로 이동(1.88 vs 1.84), dev 개선(+0.00268), test C−D가 S0 대비 개선
  (+0.004823 vs +0.001389). epoch −1이 dev 최적인 비율 ~60–72%; 첫 epoch이
  dev를 개선한 비율 20%(train loss는 100% 감소). **경계**: S2 C−D CI
  [−0.001940, +0.012379]가 0을 포함 — waveform residual의 확증 아님(B6는 공식
  기준상 S0 C−D 검사로 미발화). seed 5/5 양수는 차기 실험 근거일 뿐이다.
- **EXP-2026-003 / Q4-Q (MEASURED, 판정: mechanism fail + utility fail →
  residual CNN 경로 중단)** — run `20260808T1842`, code SHA `579fed7`, data
  `mamba_data.npz` SHA `b1c16106…`, MIT-BIH DS1→DS2 (endpoint 16 records),
  L4 237.7s. 기전 DiD `(C−D)_S2−(C−D)_S0` = −0.000441 [−0.001360, +0.000115],
  seed 1/5 양수 — **SVDB의 Q4-P B3 기전이 MIT로 transport되지 않았다**(부호
  반전, 효과 ~1e-4로 사실상 0). utility `C−A`(S2) −0.000533 → gate fail.
  정성 패턴만 재현(S2에서 best epoch 후행 이동). PREP_DATA gate 통과(mamba↔
  ecg_multi 5-클래스 지문 corroboration, S 불일치 0 beat; INCART 75→32 map
  검증). Q4-P 사후 파생 DiD(SVDB) +0.003434 [−0.000815, +0.008587]는 B3 판정
  불변의 사후 지지 증거일 뿐. **INCART stage는 진행하지 않는다**(사전 등록
  규칙상 MIT pass 전제). 상세: `experiments/specs/EXP-2026-003-…md` §11.

## Current benchmark
- Dataset/task: MIT-BIH AAMI 5-class, de Chazal DS1→DS2 patient-independent evaluation.
- Primary metric: S-beat PR-AUC.
- Required supporting views: patient-level lower tail, patient macro metrics, seed variability, patient bootstrap.
- Historical path: V8 base CNN → V9 comparison/prototype → V10 explicit P-wave morphology.
- Recorded reference: V9 `kink_noctx` S PR-AUC about 0.597; V10 `pwave` about 0.660.
  **2026-08-09 검증 완료** — 원 실행 패키지(`v9_results` / `v10_results`)의 arm×seed
  확률 원값에서 재학습 없이 재현했다:
  - **V10 `pwave` 0.6603** (기록 0.660), 짝 대조군 `base` 0.5732 (0.573) → 같은
    실행 안에서 Δ+0.087, 5/5 시드
  - **V9 `kink_noctx` 0.5969 ± 0.0411** (기록 0.597 ± 0.041), 짝 대조군 `v8base`
    0.5762 (0.576)
  - **0.660의 단위는 "시드별 PR-AUC의 평균"** 이다. 같은 확률을 시드 앙상블하면
    0.7717이 나오므로 인용 시 단위를 반드시 붙인다.
  - 앞서 `ARTIFACT_ABSENT`로 기록했던 V9는 **철회** — Drive에 없었을 뿐 로컬
    보관본이 존재했다. `ablation_step9d/pwave`는 이름만 같은 **별개 계보**였고
    baseline에서 제외한다.
  - V9·V10의 DS2는 동일(49,289박)하고 atlas cohort와 19/22 record가 정확히
    일치한다 → V9↔V10 beat 수준 비교가 가능하며 seed variability도 복원된다.
  - Q5-A run `20260809T1033`이 네 arm을 **artifact 자신의 cohort**에서 다시 확인
    (`consistent`). 같은 run의 환자 하위 꼬리(19 record cohort, record-macro / p10):
    V10 0.4209 / 0.0569 · V9 0.4112 / 0.0369 · V10_BASE 0.4081 / 0.0697 ·
    V9_BASE 0.4208 / 0.0559 — **평균에서 앞선 V10이 p10에서는 앞서지 않는다.**

## Current scientific focus
The next decision is driven by failure patients and lower-tail robustness, not a small mean-only gain.
P-wave/QRST work showed that QRST removal can improve P-wave ranking, but the tested detector did not establish independent P-wave presence evidence.

## Closed or non-beneficial directions
Previously recorded as ineffective, unstable, or harmful in the tested setting: SMOTE/oversampling, FiLM patient adaptation, patient embedding, metric learning, multi-beat context, 2D-DTW, and alarm-rate dial approaches.
2026-08-08 추가: **raw-waveform residual CNN 경로** — Q4-O NO-GO, Q4-P B3(탐색적), Q4-Q transportability replication에서 mechanism·utility 동시 fail로 사전 등록 규칙에 따라 중단(EXP-2026-003 §11).
A new spec must state why conditions differ before reopening one.

## Reproducibility requirements
- fixed patient split and recorded patient IDs;
- deterministic settings and environment manifest;
- multiple seeds or a predeclared seed plan;
- patient-level bootstrap;
- saved probabilities when practical, allowing re-evaluation without retraining;
- no final-test feedback into training.

## Latest known run reference
- Drive: `/content/drive/MyDrive/MedKOS/ecg-model/runs/20260808T1842_EXP-2026-003_q4q_transportability_replication`
- Notebook target: `notebooks/quest49_q4q_transportability_replication.ipynb` (실행본, MEASURED)
- Next: residual CNN 경로 중단이 확정되었으므로 차기 방향은 새 spec으로 —
  기존 closed 목록을 재개하려면 조건 차이를 명시해야 한다.
- 차기 spec은 `EXP-2026-004 / Q5-A`(분석 전용 실패 지도, DESIGN / RESULT NOT RUN).
  Q5-A 결과 bundle 예정 경로:
  `MyDrive/MedKOS/ecg-model/runs/<ts>_EXP-2026-004_q5a_patient_failure_atlas`
  (아직 없음). notebook: `notebooks/quest50_q5a_patient_failure_atlas.ipynb`.

## Immediate intake work
1. Inventory Drive assets without moving them.
2. Match each important run to its notebook, result, config, and probabilities.
3. Ingest missing executed notebooks/results.
4. Reconcile this summary with the newest ingested run.
5. Create the next experiment only after the inventory identifies the true latest baseline.

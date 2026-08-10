# DRIVE_ASSET_PREFLIGHT — 신규 Drive 자산 인수검사 (2026-08-10)

**판정: `SOURCE_REPLAY_INCOMPLETE` (B)** — 2차 인수 후에도 유지. **단 근거가 크게 바뀌었다.**

> **2026-08-10 2차 인수 (§13)**: 1차 스캔(04:00–07:00) 이후 **08:00에 `MyDrive/mitbih/v9~v13/`
> 가 업로드**됐다. 여기에 1차에서 "부재"로 기록한 **V10 소스(`v10pkg/kinkmap/`)** 와
> **v9·v10 캐시 실물**이 들어 있다. 그 결과 B의 두 결격 사유 중 **V10 row lineage는
> 닫혔고**, 남은 것은 **numpy/scipy 버전 미상 하나뿐**이다. §2–§12는 1차 인수 시점의
> 기록으로 보존하고, 변경된 사실은 §13에 모아 정정한다.

이 문서는 **읽기 전용 인벤토리·provenance 판정**이다. EXP-2026-007의 과학적 분석이
아니고, 어떤 실험의 판정도 바꾸지 않는다. beat join·association·학습은 실행하지
않았고, Drive 파일은 하나도 이동·삭제·덮어쓰기하지 않았다.

금지 항목 준수: DS2 class label·V10 probability 값을 열지 않았다(확률 배열이 든
NPZ는 단 하나도 다운로드하지 않았다). join 규칙을 여러 개 돌려보고 고르지 않았고,
성능을 보고 provenance 경로를 택하지 않았다 — 아래 판정은 전부 **소스 코드와 파일
메타데이터만으로** 내렸다.

---

## 1. 판정 요약

| 필수 질문 | 답 | 근거 |
|---|---|---|
| V9 확률 row의 record 내 순서·filtering을 결과를 보지 않고 완전히 재현 가능한가 | **재현은 여전히 불가 · 그러나 재현할 필요가 없어졌다** | 행 순서가 `.atr` ordinal이 아니라 **런타임 R 검출기** 출력 순서다(§3). 다만 그 행이 **캐시로 보존**돼 있어 재계산 없이 확정된다(§13.2) |
| V9 소스의 정확한 버전·입력 hash·환경·cache lineage가 증명되는가 | **부분** | 소스·producer 확증(§2). cache lineage는 **실물 확보**(§13.2). 환경은 Python 3.12.3·tf 2.21.0·keras 3.15.0·cuDNN 92400·GPU까지 확정됐으나 **numpy/scipy 버전만 끝내 미상**(§13.3) |
| V10이 V9와 동일한 처리 row를 썼다는 **producer-side** 증거가 있는가 | **예 (2026-08-10 2차 인수)** | `v10pkg/kinkmap/data.py` 의 row 선택 로직이 v9와 동일하고 `pw` 는 순수 add-on이며, **독립 재빌드된 v10 캐시가 v9 캐시와 44/44 일치**(§13.1–13.2) |
| `mamba_data/t.npy`의 의미·생성 규칙이 소스/manifest로 확인되는가 | **예** | `build_penult.py`의 `t = np.cumsum(pre) - pre[0]` — 소스로 확정(§6) |
| 압축 해제된 mamba 배열이 등록 `mamba_data.npz`(hash `b1c16106…`)의 정확한 구성원인가 | **미확인(정합하나 미증명)** | 6개 배열 전부 정확히 99,871행으로 구조 정합. 그러나 hash 미계산 + 동일 크기 사본 3개 존재(§7) |
| 중복·부분 실행 폴더와 canonical 최종 번들을 구분했는가 | **예** | §8 |

**B를 발화하는 이유**: V9 source는 있고(A의 일부 충족), exact environment와 V10 row
lineage가 없다 — 이것이 B의 정의 그대로다. 따라서 기존 order-preserving RR join
명세를 **유지**한다. C(`JOIN_INPUT_ABSENT`)로 내려가지 않는 이유는, row 순서의
*의미*와 `t`의 *단위*가 소스로 확정됐기 때문이다(§3·§6). 부족한 것은 순서의 의미가
아니라 **replay 환경과 V10 계보**다.

---

## 2. V9 source는 특정됐고 producer가 확증된다

`MyDrive/mitbih/v9pkg/` 에서 실제 소스를 확보했다. `v9pkg_results`의 producer라는
것은 **추정이 아니라 대조로 확증**된다:

- `train.py :: run()` 이 `{arm}_s{seed}.npz`(키 `prob`,`y`,`pid`)와
  `{arm}_metrics.json` 을 쓴다 → `v9pkg_results`의 파일명 규약과 정확히 일치.
- `metrics.json` 의 필드 집합이 `evaluate.py :: metrics()` 출력 + `train_one()` 의
  `info` dict와 정확히 일치(`params`,`n_ep`,`best_ep`,`train_S`,`val_S`,`w_S`).
- **arm별 param 수가 5/5 정확히 일치**한다 — 이것이 가장 강한 producer 증거다:

| arm | `model.py` 정의 | README 기재 | `metrics.json` 실측 |
|---|---|---|---|
| `v8base` | comparison+RR+SIM | 1.13M | **1,126,891** |
| `v8_noc` | comparison 제거 | 1.03M | **1,028,587** |
| `kink_noproto` | +ctx | 1.14M | **1,135,403** |
| `kink_noctx` | +proto | 1.14M | **1,141,291** |
| `kink` | +ctx+proto | 1.15M | **1,149,803** |

→ `v9pkg/kinkmap/` 가 `v9pkg_results` 를 낳았다는 것은 **producer-side로 성립**한다.

---

## 3. 행 순서·filtering 규칙 — 소스로 읽히지만 `.atr` 만으로는 재현 불가

`kinkmap/data.py :: build_record()` (`use_detected=True`, README `PEAK_SOURCE='detected'`):

```python
peaks = detect_r(sig)                      # 런타임 R 검출기
tol = int(0.15 * fs); used = set(); kp = []; li = []
for p in peaks:                            # 검출 순서(sample 오름차순)
    j = int(np.argmin(np.abs(tpk - p)))
    if abs(tpk[j] - p) <= tol and j not in used:
        used.add(j); kp.append(p); li.append(j)
```

확정 사실:

1. **record 내 행 순서** = `detect_r()` 출력 순서 = sample 오름차순. 재정렬 없음.
2. **filtering 3단계**: ① `AAMI.get(s) in C2I` 로 N/S/V만 통과(F·Q 탈락) →
   ② 검출 peak ↔ 주석 **greedy 최근접 매칭**, 허용 `0.15×360 = 54 sample`,
   `used` 집합으로 1:1 강제 → ③ 경계 컷(`p−150 ≥ 0`, `p+150 ≤ len(sig)`).
3. **record 간 순서**는 `prepare()` 의 `DS1 + DS2` 상수 리스트 순서.

**핵심 한계**: ②의 greedy 매칭은 **검출기 출력**에 의존한다. `detect_r()` 는
`scipy.signal.butter/filtfilt` (5–15 Hz) → 미분 → 제곱 → 0.12 s 이동적분 →
`0.3 × median(integ[integ>0])` 임계 → `find_peaks(distance=0.25·fs)` 다. 즉 어떤
비트가 남고 빠지는지가 **부동소수 필터 출력에 걸려 있다**. `.atr` ordinal만으로
결정론적으로 복원되는 mamba 계보(§6·`PROVENANCE_2026-08-10`)와 **근본적으로 다르다**.

또한 `train.py` 는 `prob`,`y`,`pid` 만 저장한다 — **row key(`t`·sample·beat_uid)가
저장되지 않는다**. 따라서 V9/V10 행의 identity는 오직 **위치**로만 존재한다.

---

## 4. 환경·입력 hash·cache lineage — 증명되지 않는다

`v9pkg/requirements.txt` 전문:

```text
tensorflow==2.21.0
keras==3.15.0
numpy>=2.0
scipy>=1.13
scikit-learn>=1.5
wfdb>=4.1
```

- **정확히 행 순서를 결정하는 부분(`scipy`, `numpy`)이 미고정(`>=`)이다.** TF/Keras만
  고정돼 있는데, 이것은 학습에는 관계있어도 row 선택에는 관계없다.
- `v9pkg`·`v9pkg_results` 어디에도 lockfile·`env.json`·입력 hash·cache manifest가
  **없다**. `v9pkg_results` 는 25 NPZ + 5 metrics.json = 30개가 전부다(config·
  manifest 파일 0개). `v10pkg_results` 도 동일하게 30개, manifest 0개.
- `train.py` 는 `keras.utils.set_random_seed(seed)` 만 호출하고
  `enable_op_determinism()` 을 **호출하지 않는다** → GPU 학습은 시드를 고정해도
  비결정론적이다. 이 사실은 §5의 해석에 결정적이다.

→ A(`SOURCE_REPLAY_PROVEN`)의 "exact environment, input hash, cache lineage" 조건은
**충족되지 않는다**.

---

## 5. V10 row lineage — producer-side 증거 부재

**(a) 소스 패키지가 없다.** Drive 전체에 `v10pkg` 소스 폴더가 **존재하지 않는다**.
`v10_ECG.ipynb` 는 `v9pkg/kinkmap/` 아래 **v11pkg·v12pkg·v13pkg 안에 중첩된 사본
3개**로만 있고, 전부 53,249 B이지만 **mtime이 두 가지**다(v12pkg `2026-07-19T04:47:35Z`,
v13pkg `2026-07-19T18:24:07Z`). `ASSETS.md` 가 인용하는 경로 `v10pkg/v10_ECG.ipynb`
는 **실재하지 않는 경로**다. 어느 사본이 `v10pkg_results` 를 낳았는지 확정 불가.

**(b) 유일한 대조 신호는 판별력이 없다.** V9와 V10 **양쪽에 `v8base` 라는 같은 이름의
arm이 있다.** 실측:

| | V9 `v8base` | V10 `v8base` |
|---|---|---|
| params | 1,126,891 | **1,126,891** (동일) |
| seed별 `train_S`/`val_S` | 559/385 · 357/587 · 910/34 · 804/140 · 935/9 | **완전 동일** |
| seed별 `S_prauc` | 0.4187 · 0.7415 · 0.5760 · 0.4922 · 0.6525 | 0.4490 · 0.6499 · 0.6659 · 0.4998 · 0.7272 |
| 평균 | **0.5762** | **0.5984** |

해석 — **이것은 identity 증거가 아니다**:

- `train_S`/`val_S` 완전 일치는 `val_patients()` 가 같은 seed·같은 `pid`/`y` 위에서
  같은 분할을 냈다는 뜻이다. 그러나 이는 **label 개수 일치**일 뿐이고, 과제가 명시적으로
  identity 증거로 인정하지 않는 부류다(row 수·`pid`·label 일치).
- **같은 params·같은 seed·같은 분할인데 5개 시드 전부 `S_prauc`가 다르다.** §4에서
  본 대로 op determinism이 꺼져 있으므로, 이 차이는 (ⅰ) 동일 row 위 GPU 비결정론과
  (ⅱ) 실제로 다른 row, **어느 쪽으로도 설명된다**. 판별이 불가능하므로 증거가 아니다.

**(c) 결정적: mamba 계보와 V9/V10은 애초에 다른 row 집합이다.**

| 계보 | 비트 추출 | DS2 총 beat |
|---|---|---|
| mamba (`v15b_local.py`) | `rpks` ← `ann.sample` (주석 ordinal) | **49,295** |
| v9pkg (`data.py`) | `peaks` ← `detect_r()` (검출기) | **49,289** |

차이 **−6**, 기록된 record별 편차(105 −1 · 111 −1 · 222 −4, 전부 N beat)와 정확히
일치한다. 지금까지 "stricter preprocessing" 으로 남아 있던 이 −6이 **기전적으로
설명된다**: 검출기가 ±54 sample 안에서 매칭하지 못한(또는 경계에서 잘린) 비트다.

→ `mamba_data.npz` 의 행과 V9/V10 확률 행은 **같은 행 집합이 아니다.** 22개 record 중
3개에서 길이가 어긋나고, 양쪽 어디에도 저장된 row key가 없어 오프셋을 복구할 수단이
없다. 이것이 beat join 설계가 반드시 안고 가야 할 제약이다.

---

## 6. `t.npy` 의 의미 — 소스로 확정

`build_penult.py`:

```python
# t: pre-RR 누적. 단위 자동보정(중앙값>5면 sample→초)
t = np.cumsum(pre) - pre[0]
```

- **float32, 단위 초.** record 첫 비트부터의 **누적 경과 시간**.
- `- pre[0]` 때문에 **record마다 정확히 0에서 재시작**한다(관측과 일치).
- 캐시에 시각이 없어 **pre-RR을 누적해 복원한 값**이며, 필터링된 RR을 누적하므로
  버려진 비트만큼 실제 시각에서 **누적 오차로 밀린다**.
- **`.atr` sample index가 아니고 beat_uid도 아니다.** 독립적인 identity 정보를
  담고 있지 않다.

→ Q5-A가 실측한 `t` ↔ `.atr` sample 조인 **1.9%(우연 수준, 최근접 중앙거리
0.222×RR)** 가 이것으로 완전히 설명된다. `t` 는 애초에 sample index였던 적이 없다.

---

## 7. 압축 해제 mamba 배열 — 구조 정합, identity 미증명

6개 `.npy` 전부 **정확히 99,871행**으로 떨어진다(npy 헤더 128 B 가정):

| 파일 | 크기 (B) | (크기−128)/99,871 | 해석 |
|---|---|---|---|
| `beat.npy` | 239,690,528 | **2,400.0** | float32 300×2 (WIN 150+150, 2채널) |
| `ref.npy` | 239,690,528 | **2,400.0** | 동일 |
| `feats.npy` | 10,386,712 | **104.0** | 26×float32 (또는 13×float64) |
| `y.npy` | 799,096 | **8.0** | int64 |
| `pid.npy` | 799,096 | **8.0** | int64 |
| `t.npy` | 399,612 | **4.0** | **float32** (§6과 일치) |

등록 정보(99,871 beats · 44 records)와 행 수가 정확히 맞고, `beat` 폭 300×2는
`WIN_BEFORE=WIN_AFTER=150`·2채널과 일치하며, `t` 4 B/행은 float32 판정을 뒷받침한다.
비압축 합계 491,765,572 B vs 등록 `mamba_data.npz` 204,504,913 B — `savez_compressed`
비율로 타당하다.

**그러나 identity는 증명되지 않았다:**

- 읽기 전용 제약 하에서 **hash를 계산하지 않았다**(200 MB급 배열이고, Drive 도구가
  checksum 필드를 노출하지 않는다). 따라서 `b1c16106…` 과의 대조는 **미실시**다.
- 추출 주체가 서드파티 `zipextractor.app` 이고, mtime이 전부 DOS-zip epoch
  (`1979-12-31T15:00:00Z`)이라 원본 시각 정보가 소실됐다.
- **크기가 동일한 `mamba_data.npz` 사본이 Drive에 3개** 있다(§8). 그중 등록 hash를
  가진 것은 하나뿐이고, 어느 것을 풀었는지 구분할 메타데이터가 없다.
- 압축 해제 폴더에 manifest가 **없다**.

→ **정합하나 미증명(CONSISTENT, NOT PROVEN).** 과학적 사용 전에 hash 대조가 필요하다.

---

## 8. 중복·부분 실행 vs canonical

**canonical 최종 번들 (인용은 이것으로 통일):**

| 실행 | canonical | Drive folder id |
|---|---|---|
| Q5-A atlas | `20260809T1033` | `1ZSXZnLbqpvxM0TStK_n8jYf0mAZRUwzB` |
| Q5-B-0b tie | `20260809T1241` | `1Sojo5hNdPO1dJEFe-Hp_QwyXTHqNQ7dP` |
| Q5-C core | `20260809T1345` | `1gbLlo5G8lLS5q2bHDsAFUHHYjhV0V98d` |
| PREP_DATA-A | `20260809T153151` | `1gYjRfQLCgt5A1XlmYCQ7Jx6XPdtvLIwA` |
| P-wave QUALIFY | `20260810T005802` | `1sVW5LkPSm6lBRDfruZHqgpIt7y1YjZN2` |

**선행/중복 실행 (결과 인용 금지):**

- Q5-A atlas: `20260809T1000`, `20260809T1009` — 모듈 v2~v7 이력.
- Q5-A inventory: `20260809T1009`, `20260809T1030`(canonical inventory).
- Q5-C: `20260809T1320`, `20260809T1321`, `20260809T1330` — canonical 1345 이전.
- QUALIFY: `20260810T000629`, `20260810T003840`, `20260810T003933`(DS1 상수 freeze run
  — 이것은 실패 이력이 아니라 canonical이 참조하는 상수 산출 run이다).
- PREP_DATA: `20260809T151626` — 동일하게 `PREP_DATA_ACQUIRED_VERIFIED` 12/12인
  선행 실행. 어긋나지 않지만 인용은 153151로 통일.

**파일 수준 중복 (신규 발견):**

| 자산 | 사본 | 비고 |
|---|---|---|
| `v9pkg_results` | `baseline_pkgs/v9pkg_results` (`1XqE…`, 등록본) · `v9pkg_results (Unzipped Files)` (`1K78…`, 2026-08-10 생성) | 파일명·크기 일치. 압축해제본이 원 mtime(2026-07-18) 보존 |
| `mamba_data.npz` | `1p3HvC_…`(등록·hash 보유) · `1_Wg_7wH_…`(v13pkg) · `1hLhMp1z…`(v13pkg) | 전부 204,504,913 B · mtime `2026-07-22T12:34:56Z` |
| `v10_ECG.ipynb` | `1umSvsic…`(v12pkg) · `1JJ57hjI…`·`1aF6FXvo…`(v13pkg) | 전부 53,249 B, **mtime 2종** |
| `v13pkg` 폴더 | `1fjnSchM…` · `1zKIEFKa…` | 같은 부모(`kinkmap`) 아래 동명 폴더 2개 |

---

## 9. 자산 표

hash 열: **읽기 전용 preflight에서 새로 계산한 hash는 없다.** 기재된 값은 기존 등록
hash의 인용이며, `—`는 미계산을 뜻한다(대용량 + 도구가 checksum 미노출).

| 자산 | Drive 경로 / ID | 크기 | hash | producer | consumer | row-key | 순서 의미 | 중복 | 과학적 사용 |
|---|---|---|---|---|---|---|---|---|---|
| `v9pkg` 소스 | `MyDrive/mitbih/v9pkg/` `1oYHJi38hir2JqZl9s_SyuSxq3Hxw25sK` | 폴더 | — | 사용자 로컬 | `v9pkg_results` | — | — | 아니오 | **가능** — producer 확증(§2) |
| `v9_ECG.ipynb` | `10WM6FuH20KXQ-Ik6-m9xGaCi_GT9J8Fe` | 81,324 B | — | 사용자 | V9 실행 진입점 | — | — | 아니오 | 가능 |
| `v9pkg/README.md` | `1Zsk38rlEoQDodUYGQNMr0J2B4t6OLuaL` | 1,752 B | — | 사용자 | 설계 근거 | — | — | 아니오 | 가능 — `PEAK_SOURCE='detected'` 명시 |
| `v9pkg/requirements.txt` | `176a1pt4ocKB2ujtFtxBvy1MMsGdJoh5I` | 84 B | — | 사용자 | 환경 근거 | — | — | 아니오 | **제한적** — scipy/numpy 미고정(§4) |
| `kinkmap/data.py` | `11bMKFhXafVbux02S9xKofeO-a0CBjjt0` | 6,972 B | — | 사용자 | row 순서·filtering 정의 | — | 검출기 순서 | 아니오 | **가능** — §3의 근거 |
| `kinkmap/frontend.py` | `15YJqlvVn_x-akjzV_mNyKWA4G6am-BKJ` | 8,434 B | — | 사용자 | 특징 정의 | — | — | 아니오 | 가능 |
| `kinkmap/model.py` | `1OU-3OvaYdk4xdeDZEoa69QPtWuuF13up` | 5,133 B | — | 사용자 | arm 정의 | — | — | 아니오 | 가능 — param 대조 근거 |
| `kinkmap/train.py` | `1CQ4I-vh10HC6L8NWMGoP-DNnkTR8bEct` | 4,697 B | — | 사용자 | NPZ 저장 규약 | **없음**(`prob`,`y`,`pid`만) | — | 아니오 | 가능 |
| `kinkmap/evaluate.py` | `16b1pgJLs2OWCq1Jp-gNFhc-ha0UwxCvT` | 6,898 B | — | 사용자 | metrics 스키마 | — | — | 아니오 | 가능 |
| `kinkmap/v15b_local.py` | `1jfY8wySc7O2N1Z-z9vqY5cXr6pwVtdRf` | 47,195 B | `cd4320e5…`(커밋본) | 사용자 | mamba 계보 ① | — | `.atr` ordinal | 아니오 | 가능 — 이미 등록 |
| v11/v12/v13pkg | `1ONQIWhe…` / `1sSlVQF-…` / `1fjnSchM…`·`1zKIEFKa…` | 폴더 | — | 사용자 | 후속 계보 | — | — | **v13pkg ×2** | 참고만 |
| `v10_ECG.ipynb` | `1umSvsic…`·`1JJ57hjI…`·`1aF6FXvo…` | 53,249 B | — | 사용자 | V10 실행 진입점(추정) | — | — | **×3, mtime 2종** | **불가** — 어느 사본인지 미확정(§5a) |
| `v9pkg_results` (등록) | `baseline_pkgs/v9pkg_results` `1XqE_tPtwU5V4161Fcsc-cfnXi9RsqTFF` | 25 NPZ + 5 JSON | — | `v9pkg/kinkmap` (확증) | Q5-A primary V9 | **없음** | 위치 전용 | **×2** | **가능**(확률 원값 보존) |
| `v9pkg_results` (해제본) | `1K78edqxT1fhKRkw7VEGR4eVUNtXr-53e` | 동일 30개 | — | 위 zip 해제 | — | 없음 | 위치 전용 | **중복** | 등록본 사용 권장 |
| `v10pkg_results` | `1DEmhM915usxXVrka3Z4aDliUbwKuRWXO` | 25 NPZ + 5 JSON | — | **미확정** | Q5-A primary V10 | **없음** | 위치 전용 | 아니오 | **제한적** — producer 미확증(§5) |
| `mamba_data.npz` (등록) | `MyDrive/mitbih/mamba_data.npz` `1p3HvC_bnbiQlEanFOVIvVdejy60W0tho` | 204,504,913 B | `b1c16106…f6c05` | `make_colab_data.py` | Q4-Q · Q5-A key source | `t`(비고유) | `sorted(rec)` × 시간순 | **×3** | **가능** |
| `mamba_data.npz` 사본 | `1_Wg_7wH_LrD-oHyQiEeeZjurMGtGAQUX` · `1hLhMp1zfcJugl_DZwfOEaEfhA-ydzSZC` | 동일 | — | — | — | — | — | **중복** | 등록본 사용 |
| `mamba (Unzipped)/beat.npy` | `1btEdnIovt08N_gz2MikoqZoS2XOTdHlf` | 239,690,528 B | — | zipextractor | (미정) | — | 99,871행 | 파생 | **미증명**(§7) |
| `mamba (Unzipped)/ref.npy` | `11XzbAczJ20gyGQYBlmaZ3JyupdLxKx9L` | 239,690,528 B | — | zipextractor | (미정) | — | 99,871행 | 파생 | 미증명 |
| `mamba (Unzipped)/feats.npy` | `1D2zpbCxOLtJVS_4p_SGWf4_CeMypBVFy` | 10,386,712 B | — | zipextractor | (미정) | — | 99,871×26 f32 | 파생 | 미증명 |
| `mamba (Unzipped)/y.npy` | `1MpEiZ8jLSXRujlne9BEql1uiQRv58GJc` | 799,096 B | — | zipextractor | (미정) | — | 99,871 int64 | 파생 | 미증명 · **DS2 label 열람 금지 대상** |
| `mamba (Unzipped)/pid.npy` | `1gOdCekSadXcVh1iJfg8rqnkzTU3pnNXP` | 799,096 B | — | zipextractor | (미정) | — | 99,871 int64 | 파생 | 미증명 |
| `mamba (Unzipped)/t.npy` | `1YbZZv86lRQ2AB6baDiM45kF9cZWt94Hh` | 399,612 B | — | zipextractor | join 후보 키 | **비고유** | float32 초, record별 0 재시작 | 파생 | **미증명** · identity 정보 없음(§6) |

---

## 10. 조인 설계에 걸리는 사항 (판정 아님 — Codex 검토 대상)

1. **mamba row ≠ V9/V10 row 가 확정됐다**(§5c). DS2 49,295 vs 49,289, 105/111/222에서
   −1/−1/−4. 양쪽 어디에도 저장 row key가 없다. order-preserving join은 이 3개
   record에서 반드시 정렬이 깨지므로, 명세는 **record 단위로 길이 일치를 먼저 검사**하고
   불일치 record를 `AMBIGUOUS`로 격리하는 경로가 필요하다.
2. **`t` 를 join key로 쓸 수 없다**(§6). 필터링된 RR의 누적이라 실제 시각에서 밀리고,
   record별로 0에서 재시작하며, 전역 고유성이 없다.
3. **replay 경로는 mamba 쪽에서만 열려 있다.** mamba 계보의 drop 규칙은 `.atr` 만으로
   결정론적 복원이 되지만(`PROVENANCE_2026-08-10` §2), **V9/V10 쪽은 검출기 의존이라
   같은 방법이 통하지 않는다**(§3). 따라서 "전처리 재생으로 join을 대체한다"는 안은
   V9/V10 측에 적용 불가다.
4. **V10 producer를 먼저 닫아야 한다.** `v10pkg` 소스가 없는 한, V10 확률 행이 어떤
   전처리에서 나왔는지는 영원히 추정이다. 사용자가 `v10pkg` 원본(또는 실행 노트북의
   확정 사본)을 올려 주면 §5가 재평가 가능하다.

위 1–4는 **제안이며 결정이 아니다.** join spec의 `design_owner` 는 Codex이고
`status` 는 `draft` 이며, 구현은 사용자 승인 전까지 시작하지 않는다.

---

## 11. 이 preflight에서 하지 않은 것

- beat join·association 실행, join 코드·테스트 작성
- DS2 class label 열람, V10 probability 값 열람 (확률 NPZ 다운로드 0건)
- 모델 학습·재학습, S PR-AUC·qualification 재실행
- Google Drive 변경 (읽기만 했다) — 이동·삭제·덮어쓰기 0건
- parent spec 또는 join spec 수정
- 여러 join 규칙 시행 후 선택 (단 하나도 실행하지 않았다)

## 12. 남은 공백 (→ §13에서 대부분 해소)

- 압축 해제 mamba 배열의 **hash 대조 미실시**(§7). **[여전히 유효]**
- ~~`v10pkg` 소스 부재(§5a)~~ → **§13.1에서 해소**
- ~~V9를 낳은 실행의 scipy/numpy 실제 버전 미상(§4)~~ → **§13.3에서 부분 해소**
  (Python·TF·Keras·cuDNN·GPU 확정, **numpy/scipy만 미상**)

---

# 13. 2차 인수 (2026-08-10 08:00 업로드분)

1차 스캔 종료 후 `MyDrive/mitbih/v9~v13/` (folder id `18EC4UoOTV3pTW2ehyx5nI6nToBoMOK66`,
생성 2026-08-10T08:00:31Z · `v9~v13.zip` `18MbILCkW2W48SeDaXy_JiEdZJzdKwilg` 1,343,598,610 B)
가 업로드됐다. 구조: `v10pkg/`(소스) + `v9`·`v10`·`v11`·`v12`·`v13`(각 실행 산출물
`cache/`·`results/`·`data/` + `v*_results.zip`).

## 13.1 V10 소스 확보 — §5a 정정

`v9~v13/v10pkg/kinkmap/` (folder id `1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX`):
`data.py`(7,744 B) · `frontend.py`(8,434 B) · `model.py`(5,861 B) · **`pwave.py`(6,127 B)** ·
`train.py`(4,697 B) · `evaluate.py`(6,898 B) · `__init__.py`(0 B). 상위에
`v10_ECG.ipynb`(**118,721 B — 출력 보존본**) · `v9_ECG.ipynb`(46,182 B) ·
`README.md`(1,453 B) · `requirements.txt`(84 B) · `data/`.

**행 선택 로직이 v9와 동일하다.** `data.py::build_record()` 의 `detect_r()` 호출,
`tol = int(0.15*fs)`, `used` 집합 greedy 최근접 매칭, 경계컷(`p−150 ≥ 0`, `p+150 ≤ len`),
`valid`/`idx` 구성이 v9와 문자열 수준에서 같다. v10이 더한 것은 이것뿐이다:

```python
pw_all = PW.pwave_features(sig, peaks, normal_mask=None, fs=fs)   # (n_all, 5)
...
"pw": pw_all[idx].astype("float32"),
```

**같은 `idx` 를 재사용하므로 행을 추가·삭제·재정렬하지 않는 순수 add-on**이다.
`model.py::ARMS` 도 확인됐다 — `base`=(compare,¬ctx,proto,¬pw) 는 v9 `kink_noctx`
와 같은 조합이고(그래서 params 1,141,291 이 v9 `kink_noctx` 와 일치), `v8base`
=(compare,¬ctx,¬proto,¬pw) 는 v9 `v8base` 와 같다(1,126,891 일치).

## 13.2 캐시 실물 확보 + 44/44 독립 일치 — 결정적

| 캐시 | folder id | 내용 | mtime |
|---|---|---|---|
| v9 | `1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY` | record npz 44 + `meta.json`(1,938 B, `1zWBzId_x71DK_VGdfHKg3z0DXF_F0km_`) | 2026-07-18T08:11–08:12 |
| v10 | `1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF` | record npz 44 + `meta.json`(1,938 B, `107_BY6HWEKjR5sSjPmUlhkopVmdvUwg_`) | 2026-07-18T11:55 |

두 `meta.json` 의 **44개 record `n`·`split` 이 전부 동일**하다(파일 크기도 1,938 B로 같다).
mtime은 각 실행 직전이다(v9 결과 08:22–10:19, v10 결과 12:04–15:15).

**이것이 복사본이 아니라 독립 재현이라는 증거**: `v10_ECG.ipynb` 셀 20이
`shutil.rmtree('cache', ignore_errors=True)` 로 캐시를 **지우고**, 셀 21이
`prepare(CFG.DATA_DIR, CFG.CACHE_DIR, ...)` 로 **처음부터 다시 빌드**한다. 원본 입력은
셀 19의 `wfdb.dl_database('mitdb', dl_dir=CFG.DATA_DIR, records=sorted(set(DS1+DS2)),
annotators=['atr'])` 로 PhysioNet에서 받은 mitdb다.

셀 21 stdout이 record별 beat 수를 그대로 출력하고 `meta.json` 과 일치하며, 셀 23이
`실데이터 DS1: S 944/50551` 을 찍는다 — **DS1 50,551 이 독립 확인된다.**
→ 동일 row 집합에 대한 **독립 증언 3개**(v9 캐시 meta · v10 캐시 meta · v10 노트북 stdout).

### record별 행 대장 — v9/v10 캐시 vs mamba 계보

`cache_v15b_meta.json`(커밋본) 전량 대조. **36/44 일치, 8개 불일치:**

| record | split | v9/v10 | mamba | 차이 |
|---|---|---|---|---|
| 108 | DS1 | 1,759 | 1,760 | −1 |
| 116 | DS1 | 2,397 | 2,411 | **−14** |
| 203 | DS1 | 2,972 | 2,974 | −2 |
| 208 | DS1 | 2,572 | 2,579 | −7 |
| 223 | DS1 | 2,590 | 2,591 | −1 |
| **105** | DS2 | 2,566 | 2,567 | **−1** |
| **111** | DS2 | 2,123 | 2,124 | **−1** |
| **222** | DS2 | 2,477 | 2,481 | **−4** |

DS1 50,551 vs 50,576 (**−25**) · DS2 **49,289 vs 49,295 (−6)** · 전체 99,840 vs 99,871 (−31).

DS2 쪽 −1/−1/−4 가 `ASSETS.md` 기록과 정확히 일치한다. **DS1 쪽 −25 는 지금까지
문서화된 적이 없던 값이다.** §5c의 기전(검출기 vs 주석 ordinal)이 양쪽 split에서
일관되게 확인된다.

→ **`mamba_data.npz` 행과 V9/V10 확률 행의 record별 구간이 이제 산술로 결정된다**
(DS2 리스트 순서 × 위 `n`). join 명세가 요구하던 `processed row index` ledger 항목이
채워진다.

## 13.3 환경 — 부분 해소, numpy/scipy만 미상

`v10_ECG.ipynb` 출력에서 실측:

| 항목 | 값 | 출처 |
|---|---|---|
| 실행 위치 | **로컬** `/home/user/work/v10` (Colab 아님) | 셀 2 stdout `환경: local` |
| Python | **3.12.3** · venv `~/ecg` | notebook `language_info` · traceback 경로 `~/ecg/lib/python3.12/site-packages` |
| TensorFlow | **2.21.0** | 셀 2 stdout — `requirements.txt` 핀과 일치 |
| Keras | **3.15.0** | 동일 |
| GPU | **NVIDIA GeForce GTX 1650 Ti with Max-Q**, CC 7.5, 2,242 MB | 셀 26 stdout |
| cuDNN | **92400** | 셀 26 stdout |
| **numpy / scipy** | **미상** | `pip freeze`·`__version__` 출력 셀이 **없다** |

`kernelspec` 은 `Python (ecg)` 로, 재현 가능한 named venv다. **`~/ecg` 는 사용자 로컬
머신에 아직 존재할 가능성이 높다** → `~/ecg/bin/pip freeze` 한 번이면 마지막 공백이 닫힌다.
경로가 POSIX(`~/ecg/lib/python3.12/site-packages`)이므로 Windows 사용자 기준으로는
**WSL 쪽**이다(Windows 네이티브 venv 라면 `ecg\Lib\site-packages` 여야 한다).

### 노트북 경로는 소진됐다 — v9·v11·v12·v13 전수 확인

`numpy`/`scipy` 를 찾기 위해 계열 노트북 5개를 전부 받아 스캔했다:

| 노트북 | Drive id | 크기 | `pip`·`__version__` 셀 | numpy/scipy |
|---|---|---|---|---|
| `v9_ECG.ipynb` (실행본) | `10WM6FuH20KXQ-Ik6-m9xGaCi_GT9J8Fe` | 81,324 B · 38 cells | **없음** | **없음** |
| `v10_ECG.ipynb` (실행본) | `1W1OEXp_AjvKcjJlXSmimIG18jQ4dOo8h` | 118,721 B · 43 cells | **없음** | **없음** |
| `v11_ECG.ipynb` (실행본) | `1SVL13QAmQzqZiPvEe2rVz9x-I13NrhCn` | 97,349 B · 39 cells | **없음** | **없음** |
| `v12_ECG.ipynb` (실행본) | `1puD70YxTwABFI-hfiLBAptdve3yA4roO` | 95,375 B · 37 cells | **없음** | **없음** |
| `v13_ECG.ipynb` | `1CGpQcL99QD1KbhCUBZ7gnPmjwJu_C-ln` | 71,977 B · 42 cells | **없음** | **없음** |

버전을 흘릴 만한 다른 경로(shell `!`/`%` 셀, `pip list/freeze`, Deprecation·Future·
User·RuntimeWarning, site-packages 경로가 찍힌 traceback)도 함께 훑었으나 **numpy/scipy
버전은 어디에도 없다.** → **노트북으로는 더 얻을 것이 없다. `~/ecg` venv 가 유일한 남은 출처다.**

### 부수 확인 ① — v9~v13 환경 균질성

다섯 노트북 전부 동일하다: `환경: local` · 작업폴더 `/home/user/work/v{9,10,11,12,13}` ·
Python **3.12.3** · kernel `ecg` · **tf 2.21.0 / keras 3.15.0** · GPU **GTX 1650 Ti Max-Q**
(CC 7.5) · **cuDNN 92400**(v9·v10·v11 에서 확인). **v9 와 V10 이 같은 기계·같은 venv 에서
돌았다는 것이 직접 확인된다** — 지금까지는 v10 만 확인돼 있었고 v9 는 추정이었다.

### 부수 확인 ② — v9 노트북 stdout 이 캐시와 44/44 일치 (4번째 증언)

`v9_ECG.ipynb` 셀 18의 캐시 빌드 stdout(`[nn/44] <rec> (DSx) beats=…`)을 파싱해
v9 캐시 `meta.json` 과 대조: **44/44 전부 일치, 불일치 0**, 합계 **99,840**,
DS2 **49,289**. §13.2의 증언 3개에 이것이 더해져 **동일 row 집합에 대한 독립 증언이 4개**가 된다:

1. v9 캐시 `meta.json` · 2. **v9 노트북 stdout(셀 18)** · 3. v10 캐시 `meta.json`(독립 재빌드) ·
4. v10 노트북 stdout(셀 21) + 셀 23 `DS1: S 944/50551`

참고: 셀 26의 `KeyboardInterrupt` 는 GPU OOM(2.05 GiB 할당 실패)이 난 smoke 실행
(`arms=['base'], seeds=[1000]`)을 수동 중단한 것이고, 본 실행은 셀 28
(`arms=['base','pwave','v8base','pwave_noc','full']`, seeds 1000–1004)이다. 셀 28
stdout의 시드별 수치가 `results/*_metrics.json` 과 일치한다 — **실패 이력이 아니다.**

## 13.4 판정을 A로 올리지 않는 이유

A(`SOURCE_REPLAY_PROVEN`)는 "exact source, environment, input, filtering, row-order 및
V10 lineage가 **모두** 증명된 경우에만 발화한다"고 등록돼 있다. 현재 상태:

| 조건 | 상태 |
|---|---|
| exact source | ✅ V9·V10 둘 다 확보, param 5/5 대조로 producer 확증 |
| input | ✅ PhysioNet `mitdb` (`wfdb.dl_database`) — publisher SHA-256 검증본이 `data-mitdb-raw-100` 으로 등록돼 있음 |
| filtering | ✅ 소스로 확정(§3) |
| row-order | ✅ 캐시 2개 + 노트북 stdout 으로 **물질화** |
| V10 lineage | ✅ 동일 코드 경로 + 독립 재빌드 44/44 일치 |
| **environment** | ⚠️ **numpy/scipy 미상** |

**환경 조건 하나가 미충족이므로 B를 유지한다.** 캐시가 행을 보존하고 있어 실무적으로는
replay가 불필요해졌지만, **gate 문구를 사후에 재해석해 더 유리한 판정으로 옮기지
않는다** — 그것이 이 preflight가 금지하는 행동(provenance 경로를 결과 편의로 고르는 것)과
같은 종류이기 때문이다. 재해석 여부는 join spec의 `design_owner`(Codex)와 사용자의
결정 사항이지 이 인수검사의 권한이 아니다.

**A로 가는 데 남은 것은 정확히 하나**: V9/V10을 실행한 `~/ecg` venv의 numpy·scipy 버전.

## 13.5 v9 → v13 실험 계보 (README 실측)

| 버전 | 핵심 전환 | arm | 결과 |
|---|---|---|---|
| v8 | 검증된 base — comparison branch(본인 median 템플릿과의 latent 차이)가 S를 0.055 → 0.46 | — | 기준선 |
| v1 (kinkmap) | v8 base를 통째로 제거 | — | **붕괴** S 0.13. "val 무가중 버그"도 이 부재의 증상 |
| **v9** | v8 base 값까지 복원 + kink 좌표(d1=1차미분, κ=곡률) add-on | `v8base` `v8_noc` `kink` `kink_noctx` `kink_noproto` | `kink_noctx` **0.5969** 최고 · **ctx(개인 내 layer)는 해로움** |
| **v10** | v9 `kink_noctx` 조합을 `base` 로 놓고 **P파 직접 포착 5특징**(`pwave.py`) 추가. 미분을 날것이 아니라 **정상 템플릿과의 residual**에만 사용 | `base` `pwave` `v8base` `pwave_noc` `full` | `pwave` **0.6603** 최고 (`pw` 5개 단독 DS2 S PR-AUC 0.110) |
| **v11** | V10 실패를 환자별로 해부 → **222**(기준선 오염형: P진폭 1.22인데 RR변이 0.337로 median 템플릿 오염)와 **200**(P파 소실형: P진폭 0.394)을 **정반대 이유로** 겨냥. `rhythm.py`(PP-RR 불일치·short-long, 템플릿 없이 222 우회) + P부재 게이트 | `base` `pwave` `rhythm` `pw_rhythm` | 판정축 = 최악환자 **하방** |
| **v12** | v11까지도 222가 0.11–0.14를 못 벗어남 → "특징이 아니라 **구조** 문제". 재검(recheck) 구조 + **이중게이트**(B가 경계선 N<0.85 AND D가 S 0.9+; 단일게이트는 precision 붕괴) | `b_only` `recheck_sl/pr/ib/pw` `recheck_all` | `prob_B`/`prob_D`/`prob_final` 3종 저장 |
| **v13** | 미분 계열 전패(slope −0.038, idea B, ctx −0.117) → **적분**으로 전환 + **RR^(2/3) 정규화**(v8–v12에서 한 번도 안 한 것). 222 대비 detrend 필수 | `base` `integ` `integ_nonorm` `integ_full` `intg_only` | — |
| v14 / v15b | mamba 계보(`v15b_local.py`). `psa`(P극성)·`psa_rel`(자기대비 상대화), v14 게이트 폐기 | — | `mamba_data.npz` 로 이어짐 |

줄기: **미분 → (residual로서의) P파 → 환자별 표적 → 재검 구조 → 적분+RR 정규화.**
**222·200이 v10부터 v13까지 계속 표적이었다는 점**이, Q5-A에서 `231`·`222` 가 붕괴
record로 나온 것과 이어진다(`run-20260810-q5d-qualify` 주의 ③과 같은 record다).

## 13.6 2차 인수에서도 하지 않은 것

- 캐시 npz·확률 npz를 **열지 않았다**(`meta.json` 의 record별 행 수와 노트북 stdout만 읽었다)
- DS2 per-beat class label 열람 없음 · V10 probability 값 열람 없음
- beat join·association·학습 실행 없음 · Drive 변경 0건

# `mamba_data.npz` 전처리 계보 — provenance 인수 (2026-08-10)

이 문서는 **출처 확보 기록**이다. 실험 결과가 아니고, 어떤 실험의 판정도 바꾸지
않는다. `EXP-2026-007`의 과학적 판정은 여전히 **NOT RUN**이고, beat join은
설계 `draft` 상태이며 구현·실행되지 않았다.

작성 경위: `EXP-2026-007-q5d-order-preserving-beat-join-gate.md`(draft)의 첫
구현 gate가 **provenance-only audit**이고, 실패 시 `JOIN_INPUT_ABSENT`로 종결
하도록 등록돼 있다. 그 audit이 요구하는 세 항목을 문서로 닫기 위해 전처리 원본을
찾아 repo에 고정한다. 명세는 "동결 소스·manifest·저장된 row map에서 증명하고,
DS1 매칭이 잘 된다는 이유로 추정하지 말라"고 요구한다 — 아래는 전부 소스 인용이다.

## 확보한 3계층

| 계층 | 파일 | 원 위치 (Google Drive) | Drive file id | 커밋본 크기 | Drive mtime |
|---|---|---|---|---|---|
| ① 비트 추출 | `mit-bih/lineage/v15b_local.py` | `MyDrive/mitbih/v9pkg/kinkmap/` | `1jfY8wySc7O2N1Z-z9vqY5cXr6pwVtdRf` | 47,195 B | 2026-07-20T10:49:08Z |
| ② 특징 조립 | `mit-bih/lineage/build_penult.py` | `MyDrive/mitbih/v9pkg/kinkmap/v13pkg/` | `1FZMUh2FH49iwNfiZxy7AEeMI3Plv8_4c` | 2,879 B | 2026-07-21T13:24:17Z |
| ③ 단일 파일화 | `mit-bih/lineage/make_colab_data.py` | `MyDrive/mitbih/v9pkg/kinkmap/v13pkg/` | `1M6clNbiJoRSVqybkFK_Q127IjTk5FnFG` | 2,173 B | 2026-07-22T12:34:45Z |
| 캐시 메타 | `mit-bih/lineage/cache_v15b_meta.json` | 사용자가 직접 업로드(Drive 사본 미확인) | — | 2,969 B | — |

크기 대조에서 **불일치 1건**: Drive 메타데이터가 보고한 `build_penult.py` 크기는
**2,882 B**인데 내려받아 디코드한 내용은 **2,879 B**다(3 B 차이). BOM은 아니다
(파일이 `#!/usr/bin/e…`로 시작). `v15b_local.py`(47,195)와 `make_colab_data.py`
(2,173)는 Drive 보고 크기와 정확히 일치한다. 원인 미상이므로 이 커밋본을
**바이트 단위 원본이라고 주장하지 않는다** — 로직 인용(§1-§5)에는 영향이 없다.

커밋본 SHA-256:

```text
cd4320e50068a93f460238ff28a2c22f80da42b0002b1a192d79ea2e17721421  v15b_local.py
df4fe5571f279cc101ddbc6f15a272a0f6c21145243001dd539f74dea345b7dd  build_penult.py
b3da22dfe97599f8080ed336601910c7400e166657aaddffadcb8e0a69a2a82e  make_colab_data.py
d267359120ead3526b2f55e081b77eaa1593ef581a5469d7869a4e4de2ec4fef  cache_v15b_meta.json
```

파이프라인: `.atr`/`.dat` → ① record별 `cache_v15b/mitdb/{rec}.npz` + `meta.json`
→ ② `penult_v23.npz`(`Z` 26D · `y` · `pid` · `t`) → ③ `mamba_data.npz`
(Drive `1p3HvC_bnbiQlEanFOVIvVdejy60W0tho`, `ASSETS.md`의 `data-mit-mamba`).

## 소스로 확정된 사실

### 1. record 내부 행 순서 = `.atr` ordinal 순서 (시간순·엄격 단조)

`v15b_local.py:101-102`

```python
for pos, sym in zip(ann.sample, ann.symbol):
    if sym in AAMI and WIN_BEFORE <= pos < len(s0)-WIN_AFTER:
        rpks.append(int(pos)); labs.append(C2I[AAMI[sym]])
```

`wfdb.rdann` 반환 순서 그대로 append하고, 이후 모든 특징이 이 `rpks` 인덱스
순서로 쌓인다. 재정렬·permutation·shuffle 없음.

### 2. keep/drop 규칙 — 결정론적이고 원 `.atr`만으로 재계산 가능

세 조건이 전부다(`v15b_local.py:102`, `:104`):

- `sym in AAMI` — `N L R e j` → N, `A a J S` → S, `V E` → V.
  **`F`·`Q` 는 통과하지 못한다** → Q5-B-0가 실측한 결손 818박(N 1 · S 0 · V 0 ·
  **F 802** · Q 15)의 정체가 이 한 줄이다.
- `WIN_BEFORE <= pos < len(s0)-WIN_AFTER` — record 양 끝 **150 sample**
  이내 비트 탈락(`WIN_BEFORE = WIN_AFTER = 150`, `FS = 360`).
- `len(rpks) < 5` — 유효 비트 5개 미만 record는 통째로 제외.

저장된 per-beat keep/drop 대장은 **없지만**, 원 `.atr`와 위 세 조건만으로
어느 비트가 왜 빠졌는지 **결정론적으로 복원된다**.

### 3. RR semantic — 필터링 **이후**, 단위 **초**, 첫·끝은 **복제**

`v15b_local.py:107-109`

```python
rr_all = np.diff(rpks) / FS                          # 초
rr_all = np.concatenate([[rr_all[0]], rr_all])       # pre-RR (첫 비트 보정)
post   = np.concatenate([rr_all[1:], [rr_all[-1]]])  # post-RR
```

- `rpks`는 **이미 필터링된** 비트 배열이다 → 저장 RR은 **beat filtering 이후**
  값이다. raw `.atr` 전체에서 계산한 RR과 다르다(버려진 비트의 이웃에서 어긋난다).
- `/FS` → **초**. `ecg_multi.npz`의 RR이 samples(median 268)인 것과 단위가 다르다.
- **첫 비트의 pre-RR과 마지막 비트의 post-RR은 없는 것이 아니라 복제된 값이다.**
- `rr` 블록은 7차원이고 `rr[:,0]=pre(초)`, `rr[:,1]=post(초)`
  (`build_penult.py`의 `RR_PRE_COL = 0`이 이를 재확인한다).

### 4. record 간 행 순서 — 두 스크립트가 동일한 열거를 쓴다

```python
files = sorted(glob.glob(os.path.join(CACHE_DIR, "*.npz")))   # build_penult.py
files = sorted(glob.glob(os.path.join(CACHE,     "*.npz")))   # make_colab_data.py
```

같은 디렉터리를 같은 정렬로 열어 record별 행을 그대로 쌓는다. 따라서
**`penult_v23.npz`의 행과 record npz의 행은 가정이 아니라 구성상 정렬돼 있다.**
`make_colab_data.py`의 `assert`는 행 **개수**만 보지만, 순서 일치는 이 열거
동일성으로 별도로 성립한다. `pid`도 파일명에서 나온다(`np.full(n, rec)`).

`mamba_data.npz`의 전역 행 순서 = `sorted(record id 문자열)` × record 내부 시간순.

### 5. `t` 의 정체 — 주석 sample index가 아니다

`build_penult.py`

```python
# t: pre-RR 누적. 단위 자동보정(중앙값>5면 sample→초)
t = np.cumsum(pre) - pre[0]
```

`t`는 **record 첫 비트부터의 누적 경과 시간(초)** 이며, 캐시에 시각이 없어서
pre-RR을 누적해 **복원한 값**이다(파일 주석에 그대로 적혀 있다). 게다가
필터링된 RR을 누적하므로 버려진 비트만큼 실제 시각에서 밀린다.

→ **Q5-A가 실측한 `t` ↔ `.atr` sample 조인 1.9%(우연 수준, 최근접 중앙거리
`0.222 × RR`)가 이것으로 완전히 설명된다.** `t`는 애초에 sample index였던 적이
없고, 독립적인 identity 정보를 담고 있지 않다.

### 6. 19키의 출처 — 행 순서를 건드리지 않는 in-place 추가

`build_cache`가 저장하는 키는 11개다: `beat ref rr sim pw pw_norm rhy intg
intg_nonorm ctx y`. 나머지 8개(`psa psa_rel ptf ptf_rel ptf2 ptf2_rel rr_z
ptf2_z`)는 마이그레이션 함수가 기존 npz를 열어 **키만 덧붙여 다시 저장**한다:

- `v15b_local.py :: migrate_add_psa` (L543) · `migrate_add_psa_rel` (L652)
- `Untitled13.ipynb :: migrate_add_z` (Drive `1pc-KwovE8lUSglngIWABy6Z4NpgT5wJz`)

세 함수 모두 `d = dict(np.load(p))` → 키 추가 → `np.savez_compressed(p, **d)`
형태로, `y`와 행 순서를 재배열하지 않는다.

### 7. v15b `build_cache` 는 v14 계보와 동일

`v14_two_view.ipynb`(Drive `1JByQICladUzu-QE8oOICqLElfNNJkowR`, 2026-07-20)
cell 8의 `build_cache`와 `v15b_local.py:74-206`의 `build_cache`를 대조한 결과,
**비트 선택 ~ RR 계산 블록(위 §1-§3에 해당)이 문자열 수준에서 완전히 일치**한다.
저장 키 11개도 같다. v15b는 이 빌더에 특징 마이그레이션을 얹은 것이다.

### 8. R sample 은 저장되지 않는다

`rpks`(원 `.atr` R sample)는 특징 계산에만 쓰이고 npz에 저장되지 않는다.
따라서 저장된 `beat_uid`나 raw ordinal은 **없다**. 다만 §2에 따라
**재계산은 가능**하다.

## 수치 검증 — `cache_v15b_meta.json`

| 검사 | 값 | 대조 대상 | 판정 |
|---|---|---|---|
| record 수 | 44 | `ASSETS.md` `data-mit-mamba` | 일치 |
| 총 beat | 99,871 | 동일 | 일치 |
| y 분포 | `{0: 90082, 1: 2781, 2: 7008}` | `make_colab_data.py` 기대 출력 | 일치 |
| DS1 / DS2 | 22 / 22 · 50,576 / 49,295 | `v15b_local.py`의 `DS1`·`DS2` 상수 | record 목록까지 완전 일치 |
| DS2 S | 1,837 | V9/V10 DS2 구성 (N/S/V 44,232 / **1,837** / 3,220) | 일치 |
| DS2 총 beat | 49,295 vs V9/V10 49,289 | `ASSETS.md`: 105·111·222 N beat −1/−1/−4 | 차이 −6, 기록과 일치 |

→ 이 `meta.json`은 `mamba_data.npz`를 낳은 캐시 세대의 것이다.

## 조인 설계에 걸리는 사항 (판정 아님 — Codex 검토 대상)

1. **초안의 전제 하나가 소스와 어긋난다.** 초안은 *"the first or last beat is
   ineligible when either pre-RR or post-RR is absent"* 라고 썼지만, §3에서
   보듯 첫·끝 비트의 RR은 **없는 것이 아니라 복제**된다. 후보 간선 규칙이 첫·끝
   비트에서 raw 쪽과 다르게 동작한다.
2. **replay 경로 검토 여지.** §2의 drop 규칙이 원 `.atr`에서 결정론적으로
   재계산되므로, 조인이 ±1 sample 후보 간선·최대 카디널리티 매칭·`AMBIGUOUS`
   없이 **전처리 재생**으로 성립할 여지가 있다.
3. **`processed row index` 유도 가능.** `meta.json`의 record별 `n`과 §4의
   `sorted(glob)` 순서로, `mamba_data.npz`의 record별 행 구간이 파일을 열지 않고
   산술로 결정된다. 명세의 ledger 항목 하나가 유도 가능해진다.
4. **232 편중(참고).** DS2 S beat 1,837 중 record `232`가 **1,382(75.2%)** 다.
   parent spec의 성공 gate에 *"no single record contributes >50% of all eligible
   S beats"* 가 있는데, eligible 필터 이전 원 분포부터 이 수준이다.

위 1-4는 **제안이며 결정이 아니다.** 조인 명세의 `design_owner`는 Codex이고,
`status`는 `draft`이며, 구현은 사용자 승인 전까지 시작하지 않는다.

## 이 인수에서 하지 않은 것

- 조인 코드·테스트·notebook 작성, 조인 실행
- DS1·DS2 데이터 열람, DS2 class label 열람, V10 확률 열람
- S PR-AUC·association·SHAM permutation·qualification 재실행
- Google Drive 변경(읽기만 했다), 기존 자산 이동·덮어쓰기
- parent spec 또는 join spec 수정

## 남은 공백

- `cache_v15b/mitdb/meta.json`의 **Drive 사본은 확인하지 못했다**. 위 파일은
  사용자가 직접 업로드한 것이고, §「수치 검증」의 여섯 항목으로 세대 일치를
  확인했다.
- `penult_v23.npz` 실물은 확보하지 않았다(§4로 순서는 소스에서 증명되므로
  provenance에는 필요하지 않다).
- `v15b_local.py`가 `cache_v15b`를 실제로 생성한 그 실행본과 **바이트 단위로**
  동일한지는 확인 수단이 없다. mtime 순서(① 07-20 → ② 07-21 → ③ 07-22)와
  §7의 코드 일치, §「수치 검증」의 수치 일치가 정황 근거다.

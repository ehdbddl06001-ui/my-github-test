# 런타임 복구 가이드 — Colab 이 끊겼을 때

> Colab 무료/기본 런타임은 유휴 몇십 분이면 끊긴다. 긴 여정에서 반복될 일이므로
> "무엇이 사라지고 무엇이 남는가 → 무엇을 다시 하면 되는가"를 고정해 둔다.

---

## 1. 끊기면 무엇이 사라지나

| | 상태 | 복구 |
|---|---|---|
| **메모리(RAM)** | 함수 정의(→ `NameError`), 특징 캐시, **`OUT` 결과 변수** | 재로드/재실행 |
| `/content/…` (로컬 디스크) | `svdb_raw/` 등 임시 다운로드 | 자동 재다운로드 |
| **Google Drive** | `svdb_data.npz`, `svdb_feats/`, `.py` 파일, **저장한 결과** | **남아 있음** ✅ |

> 핵심: **코드와 데이터는 Drive 에 있으니 안전**하다. 사라지는 건 "메모리에 로드된
> 상태"뿐이다. 그래서 복구 = 첫 셀(부트스트랩)을 **다시 실행**하는 것이다.

---

## 2. 복구 절차

### 2-1. 무조건 첫 셀부터 (30초, GPU 불필요)
```python
import urllib.request as u, json
R="ehdbddl06001-ui/my-github-test"; B="claude/svdb-rhythm-sequence-model-h5t30u"
S=json.load(u.urlopen(f"https://api.github.com/repos/{R}/commits/{B.replace('/','%2F')}"))["sha"]
exec(u.urlopen(f"https://raw.githubusercontent.com/{R}/{S}/mit-bih/colab_setup.py").read().decode())

from google.colab import drive; drive.mount('/content/drive')   # 끊기면 마운트도 풀린다
sync()          # 함수 전부 재로드. "✔ 준비 완료" 나오면 끝.
```
`which()` 로 무엇이 로드됐는지 확인할 수 있다(`NameError` 원인 추적).

### 2-2. 하려던 작업별

**(A) `label_audit()` 만 돌리려던 경우** — GPU·체인·특징캐시 전부 불필요:
```python
# 위 첫 셀 실행 후 바로
label_audit()      # wfdb 로 .atr 만 받아 읽음(수 분). svdb_data.npz 도 필요 없음.
```

**(B) 벤치를 다시 돌려야 하는 경우** — 특징캐시가 Drive 에 있으면 학습만:
```python
attach_arms()
OUT = bench_models(n_rep=1)     # GPU, 수십 분
save_out(OUT)                   # ★끝나면 바로 저장 (아래 3장)
report(OUT)
```

**(C) 이미 돌린 결과를 다시 보려는 경우** — 학습 없이 즉시:
```python
OUT = load_out()                # Drive 에서 복원(2-1 다음, 학습 0초)
report(OUT)
patient_breakdown(OUT, "R1.RSN(리듬+형태)")
```

---

## 3. 결과를 잃지 않으려면 — `save_out()` 을 습관으로

`bench_models()` 는 수십 분 GPU 학습이다. 그 결과 `OUT` 은 **메모리에만** 있어서
런타임이 끊기면 통째로 날아간다. 끝나면 **즉시** Drive 에 저장한다:

```python
OUT = bench_models(n_rep=1)
save_out(OUT)                   # → /content/drive/MyDrive/mitbih/rsn_last.pkl
```

저장 시 그 결과를 낸 **코드 버전(SHA)** 도 함께 박히므로, 나중에 "이 수치가 어느
코드에서 나왔나"를 추적할 수 있다. 여러 실험을 구분하려면 이름을 준다:

```python
save_out(OUT, name="rsn_baseline_5fold")
...
OUT = load_out(name="rsn_baseline_5fold")
```

> 이번에 나온 R1=0.622 같은 값은 반드시 `save_out()` 해두자. 재현 확인(`n_rep=3`)을
> 다음 세션에 이어서 하려면 이전 결과가 있어야 대응 비교가 가능하다.

---

## 4. 자주 겪는 증상 → 원인

| 증상 | 원인 | 조치 |
|---|---|---|
| `NameError: attach_arms` / `label_audit` | 함수가 메모리에서 사라짐(끊김) | 첫 셀(`sync()`) 재실행 |
| `RuntimeError: register_arm 없음` | Drive 의 `svdb_bench.py` 가 옛 버전 | `sync()` (SHA 로 최신 강제) |
| 방금 고친 게 반영 안 됨 | raw CDN 캐시 | 첫 셀이 SHA 를 먼저 풀므로 자동 해결. 안 되면 몇 분 뒤 |
| `svdb_data.npz 없음` | Drive 마운트 안 됨 | `drive.mount(...)` 먼저 |
| 특징캐시 없음(B1~B4 실패) | `svdb_feats/` 없음 | `svdb_prep_feats()` 재계산(수십 분) — RSN(R0~R2)은 불필요 |

> RSN(R0/R1/R2)은 `svdb_data.npz` 하나만 있으면 돈다(특징캐시 불필요). 그래서
> 최소 복구로도 RSN 실험은 항상 재개할 수 있다.

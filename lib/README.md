# `lib/` — Colab 노트북이 Drive에서 import 하는 공용 코드의 **원본**

## 왜 여기 있나

`notebooks/exp*.ipynb` 는 Colab에서 이렇게 시작한다:

```python
sys.path.insert(0, os.path.join(PROJECT, "lib"))
from medkos_run import MedKOSRun
```

즉 실행 시점에는 **Google Drive의 `MedKOS/ecg-model/lib/`** 를 읽는다.
그동안 이 파일이 **Drive에만 있고 repo에 없었다** — 전 실험이 의존하는데
버전 관리도, 테스트도 없는 상태였다. Drive 쪽이 지워지거나 조용히 수정되면
실험 전체가 재현 불가가 된다.

2026-08-01에 Drive 원본을 그대로 가져와 여기에 박았다.

## 동기화 규칙

- **원본은 이 repo다.** Drive는 실행용 사본으로 취급한다.
- 한쪽을 고치면 **반드시 다른 쪽도 맞춘다.** 특히 Colab에서 급하게 고치고
  repo에 반영 안 하는 것을 조심한다 — 그게 정확히 이 파일이 repo 밖에 있던 이유다.
- 고칠 때마다 `python pipelines/test_medkos_run.py` 를 돌린다.

## 파일

| 파일 | 내용 | 테스트 |
|---|---|---|
| `medkos_run.py` | `MedKOSRun` — 실행 폴더·로그·arm 체크포인트·`registry.jsonl` 기록 | `pipelines/test_medkos_run.py` |

`medkos_run.py` 는 Drive에서 받은 시점에 **4,654 바이트 / sha256 `f6b6be6bf4507d5d…`** 였다.

## 관련

- `pipelines/ecg_preflight.py` — 실험 공통 사전점검(라벨 어휘 검증·관문 3분 판정·붕괴 감시·
  경로 표본 확인·메모리 안전 부트스트랩). 노트북에 인라인해서 쓴다.
  self-test: `python pipelines/ecg_preflight.py --selftest`

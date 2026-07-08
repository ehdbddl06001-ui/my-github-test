# notebooks/ — Colab 실습장 (Google Drive 연동)

MedKOS **AI랩**의 실습 노트북. 원본 규칙·데이터 목록·학습 카드는 repo에 있고,
여기 노트북은 무료 GPU에서 직접 돌려보는 '실습장'이다.

## 3각 구조
```
GitHub(이 repo)  ── 코드·datasets.py·학습 카드(원본)
      │  Colab이 GitHub에서 노트북을 바로 연다
      ▼
Google Colab     ── 무료 GPU로 학습
      ▲  drive.mount 로 마운트
      │
Google Drive     ── 데이터·체크포인트(용량 큰 산출물) 영구 보관
```

- **코드/카드는 GitHub이 원본.** Drive에 코드를 두지 않는다.
- **데이터·체크포인트는 Drive.** 매번 새로 받지 않게 `MyDrive/MedKOS/data|ckpt/`에 재사용.
- **결과·회고는 다시 repo로.** 카드(`content/ailab/*.md`)의 `## My notes`에 옮겨 버전관리.

## 바로 열기 (Colab)
GitHub 경로를 Colab이 직접 연다:

- 템플릿: https://colab.research.google.com/github/ehdbddl06001-ui/my-github-test/blob/main/notebooks/ailab_template.ipynb
- 뇌종양 3D 분할: https://colab.research.google.com/github/ehdbddl06001-ui/my-github-test/blob/main/notebooks/ailab_brain_tumor_segmentation.ipynb

## 노트북
| 파일 | 용도 |
|------|------|
| `ailab_template.ipynb` | 매주 아무 주제나 시작하는 범용 템플릿(준비 셀 4개 + 빈 실습 셀) |
| `ailab_brain_tumor_segmentation.ipynb` | Keras 3D U-Net 뇌종양 분할 실습(카드 `ailab-2026-0002`와 짝) |

## 준비 셀이 하는 일
1. `drive.mount` — Drive를 붙여 `MyDrive/MedKOS/{data,ckpt}` 준비
2. `git clone` — 최신 repo를 가져와 `pipelines/datasets.py` 등을 import 가능하게
3. `weekly_topic()` — 이번 주 실습 주제를 **코드에게** 물어봄(ISO 주차 기준 결정론)
4. GPU 확인

자세한 셋업·모델 코드 읽는 법은 카드 `content/ailab/ailab-2026-0003.md` 참고.

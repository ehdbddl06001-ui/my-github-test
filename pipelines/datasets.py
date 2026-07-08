"""
datasets.py — 의료 AI 실습용 '오픈 데이터셋 레지스트리' + 결정론적 주간 주제 선정.

MedKOS 원칙대로, **주차 선정·데이터셋 목록 같은 결정론적 판단은 LLM이 아니라 코드**가 한다.
카드(content/ailab/*.md)는 해석·학습 노트를 담고, 여기(datasets.py)는 기계가 읽는 사실
목록이다(scrape_papers.py의 TOPICS 딕셔너리와 같은 성격의 '설정 겸 코드').

- DATASETS   : 재배포/접근 조건이 명확한 공개 의료 데이터셋. modality(양식)로 묶어 쓴다.
- CURRICULUM : 12주 실습 커리큘럼(주차 → 데이터셋·목표·모델구조). 순서가 곧 학습 경로.
- 실습 주차: **1→12 순서대로** 진행한다(달력이 아니라 내 진도 기준). 현재 주차는
  state/ailab_progress.json 에 저장되고, 한 주를 끝내면 `--advance` 로 다음으로 넘어간다.

접근(access) 값의 뜻:
  open          가입 없이 바로 내려받음(가장 Colab 친화적)
  registration  무료지만 계정/동의 필요(Kaggle·ISIC·Stanford 등)
  credentialed  자격심사 필요(PhysioNet CITI 등 — 환자정보 민감)

사용:
  python pipelines/datasets.py                 # 현재 주차 실습 주제 + 카탈로그 요약
  python pipelines/datasets.py --list          # 12주 커리큘럼 전체(완료 표시)
  python pipelines/datasets.py --week 1         # 현재 주차를 1로 지정(건너뛰기/되돌리기)
  python pipelines/datasets.py --advance        # 이번 주 완료 → 다음 주차로
  python pipelines/datasets.py --modality ecg   # 특정 양식 데이터셋만
  python -c "from pipelines.datasets import current_topic; print(current_topic())"
"""
from __future__ import annotations

import argparse
from datetime import date

# 실습 진도(순차 1→12)는 state.py가 관리. 실행 진입점에 따라 import 경로가 달라 둘 다 시도.
try:  # `python pipelines/datasets.py` 또는 Colab의 sys.path append
    from state import ailab_week, set_ailab_week, advance_ailab_week, ailab_progress
except ImportError:  # `from pipelines.datasets import ...`
    from pipelines.state import (
        ailab_week, set_ailab_week, advance_ailab_week, ailab_progress,
    )

# ── 오픈 의료 데이터셋 카탈로그 ────────────────────────────────────────────────
# 각 항목은 사실(fact)이다. 링크·라이선스·접근조건이 바뀌면 여기만 고치면
# 카드/홈페이지/노트북이 함께 정합성을 유지한다(파생물이므로).
DATASETS: list[dict] = [
    # ── 심전도 · 생체신호(EKG/ECG) ──
    {
        "key": "ptb-xl",
        "name": "PTB-XL 12-lead ECG",
        "modality": "ecg",
        "task": "심전도 진단 분류(다중 라벨)",
        "records": "21,837건 · 12유도 · 10초",
        "format": "WFDB(.dat/.hea), 500/100Hz",
        "license": "CC BY 4.0",
        "access": "open",
        "url": "https://physionet.org/content/ptb-xl/",
        "colab_ready": True,
        "note": "MedKOS가 이미 12유도 렌더(assets/ecg)에 쓰는 데이터셋. 딥러닝 입문에 가장 무난.",
    },
    {
        "key": "mitdb",
        "name": "MIT-BIH Arrhythmia",
        "modality": "ecg",
        "task": "부정맥 비트 분류",
        "records": "48건 · 2유도 · 30분",
        "format": "WFDB, 360Hz",
        "license": "ODC-BY 1.0",
        "access": "open",
        "url": "https://physionet.org/content/mitdb/",
        "colab_ready": True,
        "note": "부정맥 연구의 고전. assets/ecg/mitdb-100.json 로 이미 샘플 보유.",
    },
    {
        "key": "chapman-shaoxing",
        "name": "Chapman-Shaoxing 12-lead ECG",
        "modality": "ecg",
        "task": "리듬 분류",
        "records": "10,646건 · 12유도",
        "format": "CSV/WFDB",
        "license": "CC BY 4.0",
        "access": "open",
        "url": "https://physionet.org/content/ecg-arrhythmia/",
        "colab_ready": True,
        "note": "PTB-XL 다음 단계로 규모를 키우고 싶을 때.",
    },
    # ── 3D 뇌 MRI ──
    {
        "key": "brats",
        "name": "BraTS (Brain Tumor Segmentation)",
        "modality": "brain-mri",
        "task": "3D 뇌종양 분할(멀티모달 MRI)",
        "records": "~1,250 케이스 · 4모달(T1/T1ce/T2/FLAIR)",
        "format": "NIfTI(.nii.gz)",
        "license": "연구용(대회 동의)",
        "access": "registration",
        "url": "https://www.synapse.org/brats",
        "colab_ready": True,
        "note": "Keras 공식 뇌종양 분할 예제의 데이터. Medical Segmentation Decathlon Task01로도 열림.",
    },
    {
        "key": "msd-brain",
        "name": "Medical Segmentation Decathlon — Task01 Brain",
        "modality": "brain-mri",
        "task": "3D 뇌종양 분할",
        "records": "484 학습 케이스",
        "format": "NIfTI",
        "license": "CC BY-SA 4.0",
        "access": "open",
        "url": "http://medicaldecathlon.com/",
        "colab_ready": True,
        "note": "BraTS의 재배포 가능 미러. 가입 없이 바로 받아 Colab 실습하기 좋음.",
    },
    {
        "key": "ixi",
        "name": "IXI Brain MRI",
        "modality": "brain-mri",
        "task": "정상 뇌 MRI(등록·분할·생성 실습)",
        "records": "~600명 · T1/T2/PD/MRA/DTI",
        "format": "NIfTI",
        "license": "CC BY-SA 3.0",
        "access": "open",
        "url": "https://brain-development.org/ixi-dataset/",
        "colab_ready": True,
        "note": "라벨 없는 정상 뇌. 전처리·정합·자기지도학습 연습에 적합.",
    },
    {
        "key": "oasis",
        "name": "OASIS Brains",
        "modality": "brain-mri",
        "task": "노화·치매 뇌 MRI",
        "records": "OASIS-1/2/3",
        "format": "NIfTI/DICOM",
        "license": "데이터 사용 동의",
        "access": "registration",
        "url": "https://www.oasis-brains.org/",
        "colab_ready": False,
        "note": "치매·위축 정량 연구용. 용량이 커 Colab 무료 티어엔 버거움.",
    },
    # ── 흉부 X선 ──
    {
        "key": "nih-cxr14",
        "name": "NIH ChestX-ray14",
        "modality": "chest-xray",
        "task": "흉부질환 14종 다중라벨 분류",
        "records": "112,120장 · 30,805명",
        "format": "PNG(1024²)",
        "license": "공개(임상 재사용 주의)",
        "access": "open",
        "url": "https://nihcc.app.box.com/v/ChestXray-NIHCC",
        "colab_ready": True,
        "note": "흉부 X선 분류 입문 표준. 라벨이 NLP 추출이라 잡음 있음(공부 포인트).",
    },
    {
        "key": "chexpert",
        "name": "CheXpert (Stanford)",
        "modality": "chest-xray",
        "task": "흉부질환 분류(불확실 라벨 포함)",
        "records": "224,316장 · 65,240명",
        "format": "JPG",
        "license": "Stanford 연구용 동의",
        "access": "registration",
        "url": "https://stanfordmlgroup.github.io/competitions/chexpert/",
        "colab_ready": True,
        "note": "불확실(uncertain) 라벨 처리 전략을 배우는 데 좋음.",
    },
    # ── CT ──
    {
        "key": "lidc-idri",
        "name": "LIDC-IDRI (Lung CT)",
        "modality": "ct",
        "task": "폐결절 검출·분할",
        "records": "1,018 흉부 CT",
        "format": "DICOM + XML 주석",
        "license": "TCIA(CC BY 3.0)",
        "access": "open",
        "url": "https://www.cancerimagingarchive.net/collection/lidc-idri/",
        "colab_ready": False,
        "note": "방사선과 4명의 주석이 있어 관찰자 변이 공부에 좋음. 용량 큼.",
    },
    {
        "key": "msd-lung",
        "name": "Medical Segmentation Decathlon — Lung/Liver/etc",
        "modality": "ct",
        "task": "장기·종양 3D 분할(10개 과제)",
        "records": "과제별 수백 케이스",
        "format": "NIfTI",
        "license": "CC BY-SA 4.0",
        "access": "open",
        "url": "http://medicaldecathlon.com/",
        "colab_ready": True,
        "note": "nnU-Net·MONAI 실습의 사실상 표준 벤치마크.",
    },
    # ── 병리 ──
    {
        "key": "pcam",
        "name": "PatchCamelyon (PCam)",
        "modality": "path",
        "task": "림프절 전이 유무 이진분류",
        "records": "327,680 패치(96²)",
        "format": "HDF5",
        "license": "CC0",
        "access": "open",
        "url": "https://github.com/basveeling/pcam",
        "colab_ready": True,
        "note": "병리 입문 최적. 작은 패치라 Colab 무료로 끝까지 학습 가능.",
    },
    {
        "key": "camelyon16",
        "name": "CAMELYON16 (WSI)",
        "modality": "path",
        "task": "전체 슬라이드 전이 검출",
        "records": "400 WSI",
        "format": "TIFF(기가픽셀)",
        "license": "CC0",
        "access": "open",
        "url": "https://camelyon16.grand-challenge.org/",
        "colab_ready": False,
        "note": "기가픽셀 WSI 타일링 파이프라인을 배우는 상급 과제.",
    },
    # ── 피부 · 안저 ──
    {
        "key": "ham10000",
        "name": "HAM10000 (Skin Lesion)",
        "modality": "derm",
        "task": "피부병변 7종 분류",
        "records": "10,015장",
        "format": "JPG + CSV 메타",
        "license": "CC BY-NC 4.0",
        "access": "registration",
        "url": "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T",
        "colab_ready": True,
        "note": "클래스 불균형·메타데이터 결합을 배우기 좋은 규모.",
    },
    {
        "key": "aptos2019",
        "name": "APTOS 2019 Diabetic Retinopathy",
        "modality": "fundus",
        "task": "당뇨망막병증 중증도 5등급",
        "records": "~3,600 학습 안저",
        "format": "PNG",
        "license": "Kaggle 대회 규정",
        "access": "registration",
        "url": "https://www.kaggle.com/competitions/aptos2019-blindness-detection",
        "colab_ready": True,
        "note": "순서형(ordinal) 등급 회귀·QWK 지표를 배우는 데 적합.",
    },
    # ── 표형/임상 · 텍스트 ──
    {
        "key": "mimic-iv",
        "name": "MIMIC-IV (ICU EHR)",
        "modality": "tabular",
        "task": "임상 예측(사망·재입원 등)",
        "records": "중환자 40만+ 입원",
        "format": "CSV/관계형",
        "license": "PhysioNet Credentialed",
        "access": "credentialed",
        "url": "https://physionet.org/content/mimiciv/",
        "colab_ready": True,
        "note": "CITI 교육 이수 후 접근. 표형 임상예측·시계열 공부의 정석.",
    },
]

# 양식(modality) 사람이 읽는 이름
MODALITY_LABELS = {
    "ecg": "심전도·생체신호",
    "brain-mri": "3D 뇌 MRI",
    "chest-xray": "흉부 X선",
    "ct": "CT",
    "path": "병리(슬라이드)",
    "derm": "피부",
    "fundus": "안저(망막)",
    "tabular": "표형·임상 EHR",
    "text": "임상 텍스트",
}

# ── 12주 실습 커리큘럼 ───────────────────────────────────────────────────────
# 순서 = 학습 경로(신호 → 2D 영상 → 3D → 병리/멀티모달). 주차 선정은 코드가 한다.
CURRICULUM: list[dict] = [
    {"goal": "심전도 1D-CNN 부정맥 분류", "dataset": "mitdb", "arch": "1D-CNN",
     "why": "가장 가벼운 의료 딥러닝. 신호 → 라벨의 전 과정을 하루에 끝낸다."},
    {"goal": "12유도 ECG 다중라벨 진단", "dataset": "ptb-xl", "arch": "1D-ResNet",
     "why": "다중라벨·클래스불균형·AUROC를 실제 규모에서 경험."},
    {"goal": "흉부 X선 폐렴 이진분류(전이학습)", "dataset": "nih-cxr14", "arch": "ResNet50(전이학습)",
     "why": "ImageNet 사전학습 → 의료영상 미세조정의 표준 레시피."},
    {"goal": "흉부 X선 14종 다중라벨 + Grad-CAM", "dataset": "chexpert", "arch": "DenseNet121",
     "why": "불확실 라벨 처리 + 설명가능성(Grad-CAM) 시각화."},
    {"goal": "피부병변 7종 분류(불균형 처리)", "dataset": "ham10000", "arch": "EfficientNet",
     "why": "클래스 가중치·증강으로 불균형을 다루는 법."},
    {"goal": "당뇨망막병증 순서형 등급", "dataset": "aptos2019", "arch": "EfficientNet + 회귀",
     "why": "순서형 출력·QWK 지표라는 다른 문제틀을 경험."},
    {"goal": "병리 패치 전이 이진분류", "dataset": "pcam", "arch": "CNN",
     "why": "병리 입문. 작은 패치라 무료 Colab로 끝까지 학습 가능."},
    {"goal": "폐 CT 결절 분할(2D 슬라이스)", "dataset": "msd-lung", "arch": "2D U-Net",
     "why": "분할(segmentation) 문제와 Dice 손실 첫 경험."},
    {"goal": "3D 뇌종양 분할 — 입문", "dataset": "msd-brain", "arch": "3D U-Net",
     "why": "Keras 공식 예제 재현. 볼륨 데이터·패치 학습·메모리 관리."},
    {"goal": "3D 뇌종양 분할 — 심화(MONAI)", "dataset": "brats", "arch": "SegResNet/SwinUNETR",
     "why": "MONAI 파이프라인·데이터 증강·후처리로 성능을 끌어올린다."},
    {"goal": "정상 뇌 MRI 자기지도 사전학습", "dataset": "ixi", "arch": "Autoencoder/SSL",
     "why": "라벨 없이 표현학습. 이후 소량 라벨 미세조정으로 연결."},
    {"goal": "ICU 임상 예측(표형)", "dataset": "mimic-iv", "arch": "GBM/시계열",
     "why": "영상이 아닌 표형·시계열 임상예측으로 시야를 넓힌다."},
]


def by_modality(modality: str | None = None) -> list[dict]:
    if not modality:
        return list(DATASETS)
    return [d for d in DATASETS if d["modality"] == modality]


def get_dataset(key: str) -> dict | None:
    return next((d for d in DATASETS if d["key"] == key), None)


TOTAL_WEEKS = len(CURRICULUM)


def topic_for_week(n: int) -> dict:
    """커리큘럼 n주차(1-based)의 실습 주제. 범위를 벗어나면 1~12로 클램프."""
    n = max(1, min(int(n), TOTAL_WEEKS))
    item = CURRICULUM[n - 1]
    ds = get_dataset(item["dataset"]) or {}
    prog = ailab_progress()
    return {
        "week": n,
        "total": TOTAL_WEEKS,
        "goal": item["goal"],
        "arch": item["arch"],
        "why": item["why"],
        "dataset_key": item["dataset"],
        "dataset_name": ds.get("name", item["dataset"]),
        "dataset_url": ds.get("url", ""),
        "modality": ds.get("modality", ""),
        "access": ds.get("access", ""),
        "colab_ready": ds.get("colab_ready", False),
        "done": str(n) in prog["done"],
    }


def current_topic() -> dict:
    """지금 진행 중인 주차의 실습 주제(state의 진도 기준, 1주차부터 순서대로)."""
    return topic_for_week(ailab_week())


def weekly_topic(*_args, **_kwargs) -> dict:
    """하위호환 별칭: 이제 '현재 주차'를 돌려준다(과거엔 ISO 주차 기반이었다).
    web export·노트북이 인자 없이 호출하므로 남는 인자는 무시한다."""
    return current_topic()


def _print_catalog(modality: str | None) -> None:
    rows = by_modality(modality)
    groups: dict[str, list[dict]] = {}
    for d in rows:
        groups.setdefault(d["modality"], []).append(d)
    for mod, items in groups.items():
        print(f"\n[{MODALITY_LABELS.get(mod, mod)}]  ({mod})")
        for d in items:
            flag = "🟢" if d["access"] == "open" else ("🟡" if d["access"] == "registration" else "🔴")
            colab = "· Colab OK" if d.get("colab_ready") else ""
            print(f"  {flag} {d['name']:<38} {d['task']}  {colab}")
            print(f"     {d['url']}")


def _print_week(wt: dict) -> None:
    mark = " ✅완료" if wt.get("done") else ""
    print(f"── {wt['week']}주차 / 총 {wt['total']}주 실습 주제{mark} ──────────────────")
    print(f"  🎯 {wt['goal']}")
    print(f"  🧠 모델: {wt['arch']}")
    print(f"  📦 데이터: {wt['dataset_name']}  ({wt['access']})")
    print(f"  🔗 {wt['dataset_url']}")
    print(f"  💡 {wt['why']}")


def _print_curriculum() -> None:
    prog = ailab_progress()
    cur = prog["week"]
    print(f"── 12주 커리큘럼 (현재 {cur}주차, 완료 {len(prog['done'])}개) ──")
    for i in range(1, TOTAL_WEEKS + 1):
        t = topic_for_week(i)
        here = "👉" if i == cur else "  "
        done = "✅" if t["done"] else "· "
        print(f" {here}{done}{i:>2}주  {t['goal']:<28} [{t['dataset_name']}]")


def main() -> int:
    ap = argparse.ArgumentParser(description="MedKOS 오픈 의료 데이터셋 레지스트리 + 실습 진도")
    ap.add_argument("--modality", help="양식 필터(ecg/brain-mri/chest-xray/ct/path/derm/fundus/tabular)")
    ap.add_argument("--list", action="store_true", help="12주 커리큘럼 전체를 진도와 함께 표시")
    ap.add_argument("--week", type=int, help="현재 주차를 지정(건너뛰기/되돌리기)")
    ap.add_argument("--advance", action="store_true", help="이번 주 완료 처리 후 다음 주차로")
    args = ap.parse_args()

    if args.week is not None:
        set_ailab_week(args.week)
        print(f"현재 주차를 {max(1, min(args.week, TOTAL_WEEKS))}주차로 설정했습니다.")
    if args.advance:
        nxt = advance_ailab_week(TOTAL_WEEKS)
        print(f"이번 주를 완료로 기록하고 {nxt}주차로 이동했습니다.")

    if args.list:
        _print_curriculum()
        return 0

    _print_week(current_topic())
    print("\n── 오픈 데이터 카탈로그 (🟢open 🟡registration 🔴credentialed) ──")
    _print_catalog(args.modality)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        # `... | head` 처럼 출력이 중간에 닫히는 정상 상황 — 조용히 종료
        pass

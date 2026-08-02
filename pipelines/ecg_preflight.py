#!/usr/bin/env python3
"""ECG 실험 공통 사전점검 — 노트북마다 다시 짜지 말고 여기서 가져다 쓴다.

왜 생겼나 (2026-08-01):
  실험 13·13b·15 가 PTB-XL 의 `diagnostic_subclass` 와 **scp 원본 코드**를 혼동했다.
  `ASMI`·`ALMI`·`ILMI`·`IPMI`·`IPLMI` 는 subclass 가 아니라 코드라서 매칭이 0이었는데,
  **0을 "그 소견이 데이터에 없다"로 읽어** 세 노트북을 연달아 지나갔다.
  같은 정의를 노트북마다 다시 타이핑한 것이 근본 원인이므로, 검증된 정의와 관문을
  한 곳에 모은다.

여기 있는 것:
  assert_label_vocab  — 요청한 라벨 이름이 실제 어휘에 있는지. 없으면 **즉시 실패**
  decide              — 사전등록 관문의 유일한 계약. 지지/기각/**미결** 3분
  collapse_report     — 붕괴 감시. 전체가 아니라 **단위별**로 판정
  assert_arm_shape    — 저장된 arm 은 **겹 크기**다. 전역 인덱스로 자르면 안 된다
  assert_path_sample  — 긴 루프 전에 경로 몇 개를 실제로 확인
  boot_indices        — 메모리 안전 + 군 간 공유 축 부트스트랩 인덱스

self-test:  python pipelines/ecg_preflight.py --selftest
"""
from __future__ import annotations

import sys

# PTB-XL diagnostic_subclass 23개 (참고용 상수 — **신뢰하지 말고** 실제 csv 로 검증할 것).
# assert_label_vocab 에 scp_statements.csv 에서 뽑은 집합을 넘기는 것이 정석이다.
PTBXL_SUBCLASSES = {
    "NORM",
    "LAFB/LPFB", "IRBBB", "_AVB", "IVCD", "CRBBB", "CLBBB", "ILBBB", "WPW",
    "LVH", "LAO/LAE", "RVH", "RAO/RAE", "SEHYP",
    "IMI", "AMI", "LMI", "PMI",
    "ISCA", "ISCI", "ISC_", "STTC", "NST_",
}


class LabelVocabError(ValueError):
    """요청한 라벨 이름이 데이터의 어휘에 없다."""


def assert_label_vocab(requested, available, kind="label", counts=None, min_count=1):
    """요청한 이름이 실제 어휘에 **전부** 있는지 확인한다. 하나라도 없으면 예외.

    0건은 "데이터에 그 소견이 없다"가 아니라 **대개 이름을 잘못 골랐다**는 뜻이다.
    그 둘을 구별하려고 어휘 자체를 대조한다.

    requested : 쓰려는 이름들
    available : 데이터에서 실제로 관측된 이름 집합
    counts    : {이름: 건수} (있으면 min_count 미만도 함께 보고)
    """
    requested, available = list(requested), set(available)
    unknown = [r for r in requested if r not in available]
    if unknown:
        raise LabelVocabError(
            f"{kind} 어휘에 없는 이름 {unknown}.\n"
            f"  → 0건이 나온 이유는 '데이터에 없어서'가 아니라 **이름이 틀려서**다.\n"
            f"  실제 어휘({len(available)}개): {sorted(available)}"
        )
    thin = []
    if counts:
        thin = [(r, counts.get(r, 0)) for r in requested if counts.get(r, 0) < min_count]
    return {"ok": True, "n_requested": len(requested), "thin": thin}


def decide(lo, hi, thr, direction):
    """사전등록 관문의 **유일한** 계약: 지지(True) / 기각(False) / 미결(None).

    CI 가 임계값을 걸치면 **기각이 아니라 미결**이다. 검정력 부족을 반증으로
    위장하지 않기 위해서다. 점추정 2분 채점은 금지한다(실험13b·14 에서 그 실수를 했다).
    """
    if direction not in (">", "<"):
        raise ValueError("direction 은 '>' 또는 '<'")
    if direction == ">":
        if lo > thr:
            return True
        if hi < thr:
            return False
    else:
        if hi < thr:
            return True
        if lo > thr:
            return False
    return None


MARK = {True: "✅ 지지", False: "❌ 기각", None: "⚠️ 미결"}


def collapse_report(scores, floors, names, lift=1.2):
    """붕괴 감시 — 단위(클래스·부위)별로 판정한다.

    scores : {이름: 성능}   floors : {이름: 무작위 수준(유병률 등)}
    성능이 floor 의 `lift` 배도 안 되면 그 단위는 죽은 것으로 본다.

    ★ 하나 죽었다고 실험 전체를 무효화하지 않는다. 무효 판단은 호출자가
      '과반이 죽었는가 / 대조군 한쪽이 통째로 죽었는가'로 따로 한다.
    """
    dead = [n for n in names if scores.get(n, 0.0) < floors.get(n, 0.0) * lift]
    alive = [n for n in names if n not in dead]
    return {"dead": dead, "alive": alive,
            "fatal_majority": len(dead) >= len(names) / 2 if names else True}


def assert_arm_shape(arm, expected_rows, name="arm"):
    """저장된 arm 의 행 수가 **겹 크기**인지 확인한다.

    MedKOSRun.save_arm 은 그 겹의 예측만 저장한다(전체 길이가 아니다).
    겹 순서는 `np.where(CV == k)[0]` 의 오름차순이므로,
      OOF[np.where(CV == k)[0]] = load_arm(...)      ← 이렇게 **넣는다**
      load_arm(...)[전역인덱스]                       ← 이렇게 자르면 IndexError
    실험15d G0 에서 이 혼동으로 터졌다.
    """
    n = arm.shape[0]
    if n != expected_rows:
        raise ValueError(
            f"{name} 행 수 {n} != 기대 {expected_rows}.\n"
            "  → arm 은 **겹 크기**로 저장된다. 전역 인덱스로 자르지 말고 "
            "OOF[np.where(CV==k)[0]] = arm 형태로 넣을 것."
        )
    return {"ok": True, "rows": n}


def assert_path_sample(paths, k=5, exists=None):
    """긴 루프 **전에** 경로 몇 개가 실제로 존재하는지 본다.

    실험15 에서 wget --cut-dirs 를 잘못 줘 21,799 건 전부 읽기 실패한 적이 있다.
    한 개만 미리 확인했으면 즉시 알았다.
    """
    import os
    exists = exists or os.path.exists
    paths = list(paths)[:k]
    missing = [p for p in paths if not (exists(p) or exists(p + ".dat") or exists(p + ".hea"))]
    if missing:
        raise FileNotFoundError(
            f"표본 경로 {len(missing)}/{len(paths)} 개가 없다: {missing[:3]}\n"
            "  → 루프를 돌리기 전에 멈춘다. 다운로드 위치(디렉터리 계층)를 먼저 확인할 것."
        )
    return {"ok": True, "checked": len(paths)}


def boot_indices(n, B, seed):
    """부트스트랩 인덱스를 **생성기로** 돌려준다.

    미리 리스트로 만들면 B=4000, n=16k 에서 520MB 다. 같은 시드로 매번 다시 돌리면
    메모리 0 이면서 **여러 군이 같은 재표본 축을 공유**한다(짝지은 비교의 전제).
    """
    import numpy as np
    rs = np.random.RandomState(seed)
    for _ in range(B):
        yield rs.randint(0, n, n)


# ─────────────────────────────────────────────────────────────── self-test
def _selftest():
    import numpy as np
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("  ✅ " if cond else "  ❌ ") + name)
        ok = ok and bool(cond)

    print("assert_label_vocab")
    vocab = {"IMI", "AMI", "LMI", "PMI"}
    try:
        assert_label_vocab(["ASMI", "AMI"], vocab, kind="subclass")
        check("잘못된 이름을 잡는다", False)
    except LabelVocabError as e:
        check("잘못된 이름을 잡는다", "ASMI" in str(e) and "실제 어휘" in str(e))
    check("올바른 이름은 통과", assert_label_vocab(["IMI"], vocab)["ok"])
    r = assert_label_vocab(["IMI", "PMI"], vocab, counts={"IMI": 2676, "PMI": 17}, min_count=50)
    check("표본 부족을 함께 보고", r["thin"] == [("PMI", 17)])

    print("decide (3분)")
    for lo, hi, thr, d, exp in [(0.1, 0.3, 0.0, ">", True), (-0.3, -0.1, 0.0, ">", False),
                                (-0.1, 0.3, 0.0, ">", None), (0.05, 0.34, 0.33, "<", None),
                                (0.05, 0.20, 0.33, "<", True), (0.40, 0.90, 0.33, "<", False)]:
        check(f"[{lo:+.2f},{hi:+.2f}] {d}{thr} → {exp}", decide(lo, hi, thr, d) is exp)
    check("−0.104 vs −0.10 은 CI 없이는 판정 못 한다(미결)",
          decide(-0.145, -0.063, -0.10, ">") is None)

    print("collapse_report (단위별)")
    names = ["IMI", "ASMI", "LMI", "IPLMI"]
    floors = {"IMI": .12, "ASMI": .11, "LMI": .009, "IPLMI": .0023}
    r = collapse_report({"IMI": .55, "ASMI": .48, "LMI": .10, "IPLMI": .0024}, floors, names)
    check("희소 단위만 죽은 것으로", r["dead"] == ["IPLMI"] and len(r["alive"]) == 3)
    check("하나 죽었다고 전멸 아님", r["fatal_majority"] is False)
    r2 = collapse_report({n: floors[n] for n in names}, floors, names)
    check("전부 무작위면 과반 플래그", r2["fatal_majority"] is True)

    print("assert_arm_shape")
    check("겹 크기면 통과", assert_arm_shape(np.zeros((4348, 7)), 4348)["ok"])
    try:
        assert_arm_shape(np.zeros((4348, 7)), 21799, name="12_f0")
        check("전체 길이로 착각하면 잡는다", False)
    except ValueError as e:
        check("전체 길이로 착각하면 잡는다", "겹 크기" in str(e) and "12_f0" in str(e))

    print("assert_path_sample")
    fake = {"/a/rec1.dat", "/a/rec1.hea"}
    check("있는 경로는 통과",
          assert_path_sample(["/a/rec1"], exists=lambda p: p in fake)["ok"])
    try:
        assert_path_sample(["/b/rec1"], exists=lambda p: p in fake)
        check("없는 경로를 잡는다", False)
    except FileNotFoundError as e:
        check("없는 경로를 잡는다", "루프를 돌리기 전에 멈춘다" in str(e))

    print("boot_indices")
    a = [x[:4].tolist() for x in boot_indices(1000, 3, 7)]
    b = [x[:4].tolist() for x in boot_indices(1000, 3, 7)]
    check("같은 시드 = 같은 축(군 간 짝지음)", a == b)
    c = [x[:4].tolist() for x in boot_indices(2000, 3, 7)]
    check("n 이 다르면 축도 다르다(당연)", a != c)
    check("생성기라 메모리 상수", not isinstance(boot_indices(10, 2, 1), list))

    print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(_selftest() if "--selftest" in sys.argv else
             (print(__doc__) or 0))

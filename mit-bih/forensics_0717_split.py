# -*- coding: utf-8 -*-
# =============================================================================
#  forensics_0717_split.py — 2026-07-17 실행의 **분할 정체**를 확정한다
#
#  왜: 실험22-A 가 07-17 pkl 을 회수하려는데 테스트셋이 47,801 로 현재 DS2(49,295)
#      와 안 맞았다. "DS1/DS2 표준 분할 + 균일 손실" 인가, "44레코드 자체 3등분" 인가?
#
#  ★ 앞선 진단이 "레코드 ID 배열 없음" 이라고 한 것은 **오판**이다.
#    data_mit.npz 의 gp·gv·gt 가 바로 그것인데 dtype 이 '<U9'(문자열)이라
#    `np.issubdtype(dtype, np.integer)` 필터에 걸려 걸러졌다.
#    → 문자열에서 숫자를 뽑으면 그대로 쓸 수 있다. 재추출이 필요 없다.
#
#  Colab 사용법(학습 0회 · 30초):
#      exec(open('/content/drive/MyDrive/mitbih/forensics_0717_split.py').read())
#  또는 이 파일 내용을 셀에 그대로 붙여넣고 실행.
# =============================================================================
import os, re, numpy as np

OLD = os.environ.get("OLD_NPZ", "/content/drive/MyDrive/ecg_out/data_mit.npz")
CUR = os.environ.get("CUR_NPZ", "/content/drive/MyDrive/mitbih/mamba_data.npz")

DS1 = [101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122,
       124, 201, 203, 205, 207, 208, 209, 215, 220, 223, 230]
DS2 = [100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210,
       212, 213, 214, 219, 221, 222, 228, 231, 232, 233, 234]
CLS = ["N", "S", "V", "F"]


def to_rec(g):
    """그룹 배열 → 레코드 번호(int). 문자열('100'·'mitdb_100' 등)도 받는다.

    고유값에만 정규식을 돌리고 매핑한다(47,801개를 하나씩 훑지 않는다).
    """
    a = np.asarray(g)
    if np.issubdtype(a.dtype, np.integer):
        return a.astype(int)
    s = a.astype(str)
    u = np.unique(s)
    m = {}
    for x in u:
        dg = re.findall(r"\d+", x)
        m[x] = int(dg[-1]) if dg else -1
    return np.array([m[x] for x in s], dtype=int)


def main():
    for p in (OLD, CUR):
        if not os.path.exists(p):
            raise SystemExit(f"파일 없음: {p}\n  → 경로를 OLD_NPZ/CUR_NPZ 로 바꿔 지정할 것")

    d = np.load(OLD, allow_pickle=True)
    print("=" * 78)
    print("0. 07-17 캐시 — 그룹 배열의 **실제 dtype**")
    print("=" * 78)
    SPL = []
    for sfx, name in (("p", "train"), ("v", "val"), ("t", "test")):
        yk, gk = f"y{sfx}", f"g{sfx}"
        if yk not in d.files or gk not in d.files:
            print(f"  ⚠️ {yk}/{gk} 없음 — 건너뜀")
            continue
        raw = d[gk]
        y = np.asarray(d[yk]).astype(int)
        print(f"  {gk}: dtype={raw.dtype} · 예시 {np.asarray(raw).astype(str)[:3].tolist()}")
        SPL.append((name, y, to_rec(raw)))
    if not SPL:
        raise SystemExit("그룹 배열을 못 찾았다. 추측하지 않는다.")

    print("\n" + "=" * 78)
    print("1. 【결정적】 각 분할의 레코드 집합이 DS1 인가 DS2 인가")
    print("=" * 78)
    sets = {}
    for name, y, r in SPL:
        s = set(int(x) for x in np.unique(r))
        sets[name] = s
        i1, i2 = sorted(s & set(DS1)), sorted(s & set(DS2))
        other = sorted(s - set(DS1) - set(DS2))
        h = np.bincount(y, minlength=4)[:4]
        print(f"\n  [{name}] n={len(y):,} · 레코드 {len(s)}개 · "
              + " ".join(f"{CLS[i]} {int(h[i]):,}" for i in range(4)))
        print(f"    DS1 소속 {len(i1)}개 · DS2 소속 {len(i2)}개 · 그 외 {other}")
        if s and s <= set(DS1):
            print("    → **DS1 부분집합** ✅")
        elif s and s <= set(DS2):
            print("    → **DS2 부분집합** ✅")
        elif i1 and i2:
            print("    → ❗ DS1·DS2 **혼재** = 표준 분할이 아니다")
        print(f"    레코드: {sorted(s)}")

    tv = sets.get("train", set()) | sets.get("val", set())
    te = sets.get("test", set())
    print("\n  " + "-" * 74)
    print(f"  train ∪ val = {len(tv)}개 · DS1 과 같은가? "
          f"{'✅ 정확히 일치' if tv == set(DS1) else '❌ 다르다'}")
    if tv != set(DS1):
        print(f"    DS1 에만 있음 {sorted(set(DS1) - tv)} · train∪val 에만 있음 {sorted(tv - set(DS1))}")
    print(f"  test        = {len(te)}개 · DS2 와 같은가? "
          f"{'✅ 정확히 일치' if te == set(DS2) else '❌ 다르다'}")
    if te != set(DS2):
        print(f"    DS2 에만 있음 {sorted(set(DS2) - te)} · test 에만 있음 {sorted(te - set(DS2))}")
    if tv & te:
        print(f"  ❗❗ train∪val 과 test 가 겹친다 {sorted(tv & te)} — 환자 누수")
    else:
        print("  train∪val ∩ test = 공집합 ✅ (환자 누수 없음)")

    # ── S 가 어디로 갔나: train S 422 의 기전
    print("\n" + "=" * 78)
    print("2. S 가 어느 분할로 갔나 (train S 가 왜 422 인가)")
    print("=" * 78)
    for name, y, r in SPL:
        top = sorted(((int(((y == 1) & (r == q)).sum()), q)
                      for q in np.unique(r)), reverse=True)[:4]
        tot = int((y == 1).sum())
        print(f"  [{name}] S {tot:,} · 상위 레코드 "
              + " ".join(f"#{q}:{c:,}" for c, q in top if c))

    # ── 현재 파이프라인과 레코드별 대조
    print("\n" + "=" * 78)
    print("3. 현재 파이프라인과 **레코드별** 대조 (손실이 균일한가)")
    print("=" * 78)
    c = np.load(CUR, allow_pickle=True)
    if not {"y", "pid"} <= set(c.files):
        print(f"  ⚠️ {CUR} 에 y·pid 가 없다 (키 {list(c.files)}) — 대조 생략")
        return
    cy, cp = np.asarray(c["y"]).astype(int), np.asarray(c["pid"]).astype(int)
    oy = np.concatenate([y for _, y, _ in SPL])
    orr = np.concatenate([r for _, _, r in SPL])

    print(f"  {'rec':>5} {'분할':<6} {'07-17 N/S/V':>18} {'현재 N/S/V':>16} "
          f"{'차이(현재−07)':>16} {'손실률':>8}   F")
    tot_d = np.zeros(3, int)
    rows = 0
    for q in sorted(set(int(x) for x in np.unique(cp))):
        om = orr == q
        cm = cp == q
        o3 = [int(((oy == k) & om).sum()) for k in range(3)]
        oF = int(((oy == 3) & om).sum())
        c3 = [int(((cy == k) & cm).sum()) for k in range(3)]
        dd = [c3[k] - o3[k] for k in range(3)]
        tot_d += np.array(dd)
        where = next((n for n, _, r in SPL if q in set(int(x) for x in np.unique(r))), "없음")
        rate = sum(dd) / max(sum(c3), 1)
        rows += 1
        print(f"  {q:>5} {where:<6} {str(o3):>18} {str(c3):>16} {str(dd):>16} "
              f"{rate:>7.2%}   {oF}")
    ct = [int((cy == k).sum()) for k in range(3)]
    ot = [int((oy == k).sum()) for k in range(3)]
    print(f"\n  합계  07-17 N/S/V {ot} (+F {int((oy==3).sum()):,}) · 현재 {ct}")
    print(f"        부족 {tot_d.tolist()} · 소계 {int(tot_d.sum()):,}"
          f" ({tot_d.sum()/max(sum(ct),1):.2%})")
    print(f"        클래스별 손실률 "
          + " · ".join(f"{CLS[k]} {tot_d[k]/max(ct[k],1):.2%}" for k in range(3)))
    print(f"\n  레코드 {rows}개 중 손실 0 인 레코드 수는 위 표에서 차이가 [0, 0, 0] 인 행")
    print("  → 전 레코드에 고르게 퍼져 있으면 **검출기 정합 실패**(분산 손실),")
    print("    한두 레코드에 몰려 있으면 **레코드 단위 사고**다.")


main()

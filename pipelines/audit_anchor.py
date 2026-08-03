#!/usr/bin/env python3
"""Q7-E 앵커 감사 — **유병률 대비 S 농축비**로 다시 센다.

왜 필요한가
-----------
Q7-E 노트북 【E-D】는 「앵커가 **S 우세 군**(S비율 > 0.5)을 기저로 골랐나」를 물었고
전수 70개체에서 **0개**가 나왔다. 그런데 같은 실행에서 앵커는 정상 개체를 깎았다
(E3 −0.0128 [−0.0263, −0.0023]). 손해 본 개체를 손으로 계산해 보면 이유가 나온다:

    #865  유병률 0.576 · 앵커군 S비율 0.043  →  농축비 0.07  (희석)  Δ +0.7563
    #888  유병률 0.029 · 앵커군 S비율 0.139  →  농축비 4.79  (농축)  Δ −0.2237
    #862  유병률 0.012 · 앵커군 S비율 0.031  →  농축비 2.58  (농축)  Δ −0.1383
    #876  유병률 0.063 · 앵커군 S비율 0.082  →  농축비 1.30  (농축)  Δ −0.0968
    #828  유병률 0.078 · 앵커군 S비율 0.075  →  농축비 0.96  (무변)  Δ −0.2833

앵커가 하는 일은 「기저에서 S 를 빼내는 것」이다. **실제로 뺀 개체에서만 이득이 났고,
오히려 넣은 개체에서 손해가 났다.** 절대 문턱(0.5)은 이걸 **한 건도 못 잡는다** —
유병률이 0.03 인 개체에서 앵커군 S비율 0.139 는 4.8배 농축인데도 0.5 밑이다.

→ 감사 지표는 **절대 비율이 아니라 유병률 대비 농축비**여야 한다.
   이 스크립트가 그걸 전수로 계산한다. **노트북은 이미 관문이 발화해 동결**이므로
   (Q7-B 선례), 고친 감사는 여기와 후속 노트북에 둔다.

사용
----
    python pipelines/audit_anchor.py --config <run>/config.json
    python pipelines/audit_anchor.py --selftest

Colab 에서 바로:
    !python pipelines/audit_anchor.py --config \
        /content/drive/MyDrive/MedKOS/ecg-model/runs/<run_id>/config.json
"""
import argparse
import json
import math
import sys

EPS = 1e-9


def enrichment(row):
    """앵커군 S비율 / 유병률. 유병률 0 이면 정의 불가(None)."""
    prev = float(row.get("prev", float("nan")))
    sf = float(row.get("s_frac_anchor", float("nan")))
    if not (prev > EPS) or math.isnan(sf):
        return None
    return sf / prev


def spearman(x, y):
    """순위 상관 — scipy 없이도 돌게 직접 짠다(동점은 평균 순위)."""
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    n = len(x)
    if n < 3:
        return float("nan")
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")


def audit(per_record):
    rows = []
    undef = []
    for k, v in per_record.items():
        e = enrichment(v)
        if e is None:
            undef.append(int(k)); continue
        rows.append(dict(rec=int(k), prev=float(v["prev"]), sf=float(v["s_frac_anchor"]),
                         enr=e, maj=float(v["maj"]), anchor=float(v["anchor"]),
                         delta=float(v["anchor"]) - float(v["maj"]),
                         rr_sep=float(v.get("rr_sep", float("nan")))))
    rows.sort(key=lambda r: r["rec"])
    return rows, sorted(undef)


def report(rows, undef, out=print):
    out("=" * 92)
    out("앵커 감사 — 유병률 대비 S 농축비 (절대 0.5 문턱이 못 보는 것)")
    out("=" * 92)
    if undef:
        out(f"  농축비 정의 불가(유병률 0) {len(undef)}개: {undef}")
    if not rows:
        out("  채점 가능한 개체가 없다"); return {}

    enr = [r["enr"] for r in rows]
    dlt = [r["delta"] for r in rows]
    dil = [r for r in rows if r["enr"] < 1.0]
    ric = [r for r in rows if r["enr"] > 1.0]
    out(f"  개체 {len(rows)}개 — **희석(<1) {len(dil)}개 · 농축(>1) {len(ric)}개**")
    out(f"  절대 문턱(S비율 > 0.5)으로 잡히는 개체: "
        f"{[r['rec'] for r in rows if r['sf'] > 0.5] or '없음'}"
        "   ← 이게 0 이어도 농축은 얼마든지 있을 수 있다")

    def mean(v):
        return sum(v) / len(v) if v else float("nan")
    out(f"\n  농축비 vs Δ(앵커−다수결) 스피어만 rho = {spearman(enr, dlt):+.3f}")
    out(f"    희석 개체 Δ 평균 {mean([r['delta'] for r in dil]):+.4f}"
        f"  ·  농축 개체 Δ 평균 {mean([r['delta'] for r in ric]):+.4f}")

    out("\n  농축비 층별")
    for lo, hi in ((0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 3.0), (3.0, float("inf"))):
        s = [r for r in rows if lo <= r["enr"] < hi]
        if s:
            hs = "inf" if hi == float("inf") else f"{hi:.1f}"
            out(f"    [{lo:.1f},{hs}) — {len(s):>3}개체 · 다수결 {mean([r['maj'] for r in s]):.4f}"
                f" · 앵커 {mean([r['anchor'] for r in s]):.4f}"
                f" · **Δ {mean([r['delta'] for r in s]):+.4f}**")

    out("\n  가장 농축된 5 (앵커가 기저에 S 를 **넣은** 개체)")
    for r in sorted(rows, key=lambda r: -r["enr"])[:5]:
        out(f"    #{r['rec']}  유병률 {r['prev']:.3f} · 앵커군 S비율 {r['sf']:.3f}"
            f" · **농축비 {r['enr']:.2f}** · Δ {r['delta']:+.4f} · RR분리도 {r['rr_sep']:.3f}")
    out("  가장 희석된 5 (앵커가 제 일을 한 개체)")
    for r in sorted(rows, key=lambda r: r["enr"])[:5]:
        out(f"    #{r['rec']}  유병률 {r['prev']:.3f} · 앵커군 S비율 {r['sf']:.3f}"
            f" · **농축비 {r['enr']:.2f}** · Δ {r['delta']:+.4f} · RR분리도 {r['rr_sep']:.3f}")

    out("\n  ⚠️ 이건 **사후 감사**다. 여기서 나온 문턱으로 Q7-E 관문을 다시 매기지 않는다 —")
    out("     후속 실험의 사전등록 재료다. 그리고 농축비는 **라벨을 쓴다**(유병률·S비율).")
    out("     배포 규칙으로 쓸 수 있는 건 라벨이 필요 없는 **RR 분리도** 쪽이다.")
    return dict(n=len(rows), n_diluted=len(dil), n_enriched=len(ric),
                rho_enr_delta=spearman(enr, dlt),
                mean_delta_diluted=mean([r["delta"] for r in dil]),
                mean_delta_enriched=mean([r["delta"] for r in ric]),
                undefined=undef)


def selftest():
    """합성으로 확인: 절대 문턱은 못 보고 농축비는 보는 상황을 만든다."""
    per = {
        # 유병률 높고 앵커가 S 를 빼냄 → 이득 (#865 형)
        "865": dict(prev=0.576, s_frac_anchor=0.043, maj=0.2103, anchor=0.9666, rr_sep=0.40),
        # 유병률 낮은데 앵커군에 S 가 몰림 → 손해. S비율 0.139 는 **0.5 밑**이다
        "888": dict(prev=0.029, s_frac_anchor=0.139, maj=0.934, anchor=0.711, rr_sep=0.02),
        "862": dict(prev=0.012, s_frac_anchor=0.031, maj=0.896, anchor=0.758, rr_sep=0.03),
        "876": dict(prev=0.063, s_frac_anchor=0.082, maj=0.561, anchor=0.464, rr_sep=0.04),
        # 무변
        "828": dict(prev=0.078, s_frac_anchor=0.075, maj=0.689, anchor=0.406, rr_sep=0.01),
        "900": dict(prev=0.100, s_frac_anchor=0.020, maj=0.850, anchor=0.880, rr_sep=0.35),
        "901": dict(prev=0.050, s_frac_anchor=0.010, maj=0.870, anchor=0.900, rr_sep=0.33),
    }
    rows, undef = audit(per)
    summ = report(rows, undef)
    print()
    assert not [r for r in rows if r["sf"] > 0.5], \
        "자가검정 전제가 깨졌다 — 절대 문턱에 걸리는 개체가 있으면 안 된다"
    print("  ✅ ① 절대 문턱(S비율>0.5)은 **한 건도** 못 잡는다 — 그런데도 손해가 나 있다")
    enr = [r for r in rows if r["enr"] > 1.0]
    assert len(enr) == 3 and {r["rec"] for r in enr} == {888, 862, 876}, \
        f"농축 개체 판정이 틀렸다: {[r['rec'] for r in enr]}"
    print("  ✅ ② 농축비는 #888(4.79) · #862(2.58) · #876(1.30) 을 잡아낸다")
    assert summ["mean_delta_enriched"] < 0 < summ["mean_delta_diluted"], \
        f"농축=손해 · 희석=이득 방향이 안 나온다: {summ}"
    print("  ✅ ③ 농축 개체는 평균 손해 · 희석 개체는 평균 이득 — 방향이 맞다")
    assert summ["rho_enr_delta"] < -0.5, f"농축비와 Δ 의 음의 상관이 약하다: {summ}"
    print(f"  ✅ ④ 농축비 vs Δ rho = {summ['rho_enr_delta']:+.3f} (음의 상관)")
    # 유병률 0 은 정의 불가로 빠지고 **이름이 남아야** 한다
    per2 = dict(per); per2["999"] = dict(prev=0.0, s_frac_anchor=0.0, maj=0.5, anchor=0.5)
    rows2, undef2 = audit(per2)
    assert undef2 == [999] and 999 not in {r["rec"] for r in rows2}, \
        f"유병률 0 개체가 조용히 사라지거나 끼어들었다: {undef2}"
    print("  ✅ ⑤ 유병률 0 개체는 '정의 불가' 로 **이름과 함께** 빠진다")
    print("\n전부 통과 ✅ — 농축비 감사가 절대 문턱의 사각지대를 덮는다")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", help="Q7-E 실행의 config.json 경로")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); return 0
    if not a.config:
        ap.error("--config 또는 --selftest 가 필요하다")
    cfg = json.load(open(a.config))
    per = cfg.get("per_record")
    if not per:
        print("❌ config.json 에 per_record 가 없다 — Q7-E 실행 산출물이 맞는지 확인할 것")
        return 1
    rows, undef = audit(per)
    report(rows, undef)
    return 0


if __name__ == "__main__":
    sys.exit(main())

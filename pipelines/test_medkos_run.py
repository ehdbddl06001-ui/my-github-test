#!/usr/bin/env python3
"""lib/medkos_run.py 연기 테스트 — Drive 원본과 repo 사본이 실제로 동작하는지 본다.

전 실험이 이 클래스에 의존하는데 여태 테스트가 없었다(그리고 repo 밖에 있었다).
TF·GPU 없이 돌아가는 부분만 임시 디렉터리에서 확인한다.

    python pipelines/test_medkos_run.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib"))


def main() -> int:
    import numpy as np
    from medkos_run import MedKOSRun

    ok = True

    def check(name, cond):
        nonlocal ok
        print(("  ✅ " if cond else "  ❌ ") + name)
        ok = ok and bool(cond)

    with tempfile.TemporaryDirectory() as proj:
        cfg = {"exp": "smoke", "note": "한글도 깨지지 않아야 한다"}
        run = MedKOSRun("smoke_exp", cfg, project=proj, run_id="TESTRUN")

        print("초기화")
        check("run.dir 생성", os.path.isdir(run.dir))
        check("arms/figures 하위 생성",
              os.path.isdir(os.path.join(run.dir, "arms"))
              and os.path.isdir(os.path.join(run.dir, "figures")))
        check("config.json 기록", os.path.exists(os.path.join(run.dir, "config.json")))
        man = json.load(open(os.path.join(run.dir, "manifest.json")))
        check("manifest 에 환경 기록", {"python", "platform", "gpu", "packages"} <= set(man))

        print("경로")
        check("run.data() 는 실행 폴더가 아니라 공용 data/ 를 가리킨다",
              run.data("x.npz") == os.path.join(proj, "data", "x.npz"))
        check("run.path() 는 중간 폴더를 만든다",
              os.path.isdir(os.path.dirname(run.path("a", "b", "c.txt"))))

        print("기록")
        run.log("한글 로그")
        check("log.txt 에 남는다", "한글 로그" in open(os.path.join(run.dir, "log.txt")).read())
        run.save_json("obj", {"ko": "값", "n": 1})
        check("save_json 이 ensure_ascii=False",
              "값" in open(os.path.join(run.dir, "obj.json"), encoding="utf-8").read())

        print("배열 · arm")
        arr = np.arange(6, dtype="float32").reshape(3, 2)
        run.save_npy("arr", arr)
        check("save/load_npy 왕복", np.array_equal(run.load_npy("arr"), arr))
        check("없는 npy 는 None", run.load_npy("nope") is None)
        check("done() 는 저장 전 False", run.done("armA") is False)
        run.save_arm("armA", arr)
        check("done() 는 저장 후 True", run.done("armA") is True)
        check("load_arm 왕복", np.array_equal(run.load_arm("armA"), arr))
        check("없는 arm 은 None", run.load_arm("nope") is None)

        print("그림")
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.plot([0, 1], [0, 1])
            p = run.save_fig("f1", fig)
            check("save_fig 파일 생성", os.path.exists(p))
            plt.close(fig)
        except ImportError:
            print("  ⏭ matplotlib 없음 — 건너뜀")

        print("마무리")
        res = run.finish({"exp_id": "smoke_exp", "date": "2026-08-01",
                          "metric": "m", "value": 0.5, "passed": True,
                          "summary": "요약"})
        check("result.json 기록", os.path.exists(os.path.join(run.dir, "result.json")))
        check("run_id·elapsed_sec 주입", res["run_id"] == "TESTRUN" and "elapsed_sec" in res)
        reg = os.path.join(proj, "registry.jsonl")
        line = json.loads(open(reg, encoding="utf-8").read().strip())
        check("registry 한 줄 추가", line["run_id"] == "TESTRUN")
        check("registry 에 dir 이 들어간다(후속 실험이 이걸로 찾는다)",
              line["dir"] == run.dir)
        check("registry 에 exp_id·metric·value·passed·summary",
              {"exp_id", "metric", "value", "passed", "summary"} <= set(line))

        print("이어하기(같은 run_id 로 다시 열기)")
        run2 = MedKOSRun("smoke_exp", cfg, project=proj, run_id="TESTRUN")
        check("이전 arm 을 그대로 읽는다", np.array_equal(run2.load_arm("armA"), arr))

    print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

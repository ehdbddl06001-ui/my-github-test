
import os, sys, json, time, platform, subprocess

class MedKOSRun:
    """실행 하나의 모든 산출물을 Drive에 남기는 아티팩트 스토어.

    run = MedKOSRun("exp1p_icentia", config, project=PROJECT)
    run.log("...")            # 화면 + log.txt
    run.save_json("a", obj);  run.save_npy("b", arr);  run.save_fig("c", fig)
    run.save_model(m, "B3R"); run.load_npy("b")
    run.done("B3R")           # 이 arm 끝났나?  (이어하기)
    run.finish(result)        # result.json + registry.jsonl 한 줄 append
    """

    def __init__(self, exp_id, config, project, run_id=None):
        self.project = project
        self.exp_id = exp_id
        self.run_id = run_id or f"{time.strftime('%Y%m%dT%H%M')}_{exp_id}"
        self.dir = os.path.join(project, "runs", self.run_id)
        self.data_dir = os.path.join(project, "data")
        for d in (self.dir, self.data_dir,
                  os.path.join(self.dir, "figures"), os.path.join(self.dir, "arms")):
            os.makedirs(d, exist_ok=True)
        self.t0 = time.time()
        self.save_json("config", config)
        self.save_json("manifest", {
            "run_id": self.run_id, "exp_id": exp_id,
            "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "python": sys.version.split()[0], "platform": platform.platform(),
            "gpu": self._gpu(), "packages": self._pkgs(),
        })
        self.log(f"RUN {self.run_id}")
        self.log(f"  → {self.dir}")

    # ---------- 환경 ----------
    def _gpu(self):
        try:
            return subprocess.check_output(
                ["nvidia-smi", "--query-gpu=name,memory.total",
                 "--format=csv,noheader"], text=True).strip()
        except Exception:
            return "none"

    def _pkgs(self):
        out = {}
        for m in ("numpy", "tensorflow", "wfdb", "sklearn"):
            try:
                out[m] = __import__(m).__version__
            except Exception:
                out[m] = "n/a"
        return out

    # ---------- 경로 ----------
    def path(self, *parts):
        p = os.path.join(self.dir, *parts)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    def data(self, name):
        return os.path.join(self.data_dir, name)

    # ---------- 기록 ----------
    def log(self, msg=""):
        print(msg)
        with open(os.path.join(self.dir, "log.txt"), "a") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

    def save_json(self, name, obj):
        p = self.path(f"{name}.json")
        with open(p, "w") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2, default=str)
        return p

    def save_npy(self, name, arr):
        import numpy as np
        p = self.path(f"{name}.npy"); np.save(p, arr); return p

    def load_npy(self, name):
        import numpy as np
        p = os.path.join(self.dir, f"{name}.npy")
        return np.load(p) if os.path.exists(p) else None

    def save_fig(self, name, fig=None):
        import matplotlib.pyplot as plt
        p = self.path("figures", f"{name}.png")
        (fig or plt.gcf()).savefig(p, dpi=140, bbox_inches="tight")
        return p

    def save_model(self, model, arm):
        p = self.path("arms", arm, "weights.keras")
        try:
            model.save(p)
        except Exception as e:
            self.log(f"  (모델 저장 실패 {arm}: {e})")
        return p

    # ---------- 이어하기 ----------
    def done(self, arm):
        return os.path.exists(os.path.join(self.dir, "arms", arm, "probs.npy"))

    def save_arm(self, arm, probs):
        import numpy as np
        p = self.path("arms", arm, "probs.npy"); np.save(p, probs); return p

    def load_arm(self, arm):
        import numpy as np
        p = os.path.join(self.dir, "arms", arm, "probs.npy")
        return np.load(p) if os.path.exists(p) else None

    # ---------- 마무리 ----------
    def finish(self, result):
        result = dict(result)
        result["run_id"] = self.run_id
        result["elapsed_sec"] = round(time.time() - self.t0, 1)
        self.save_json("result", result)
        line = {k: result.get(k) for k in
                ("run_id", "exp_id", "date", "metric", "value", "passed")}
        line["exp_id"] = self.exp_id
        line["summary"] = result.get("summary", "")
        line["dir"] = self.dir
        with open(os.path.join(self.project, "registry.jsonl"), "a") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
        self.log(f"FINISH {self.run_id}  ({result['elapsed_sec']:.0f}s)")
        self.log(f"  registry.jsonl 에 1줄 추가됨")
        return result

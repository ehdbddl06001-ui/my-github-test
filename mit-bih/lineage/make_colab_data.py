#!/usr/bin/env python3
import os, glob, numpy as np

BASE   = os.path.expanduser("~/v9pkg/kinkmap/v13pkg/cache_v15b")
CACHE  = os.path.join(BASE, "mitdb")
PENULT = os.path.join(BASE, "penult_v23.npz")

files = sorted(glob.glob(os.path.join(CACHE, "*.npz")))
print(f"record npz {len(files)}개  (44 기대)")

# ── record npz 에서 beat/ref/y(3-class) 를 sorted 순서로 읽음 (penult 와 자동정렬) ──
beats, refs, ys = [], [], []
label_key = None
for i, f in enumerate(files):
    d = np.load(f, allow_pickle=True)
    if i == 0:
        print("record npz 키:", list(d.files))
        # y 라벨 키 자동탐색 (y/label/cls 중)
        for cand in ("y", "label", "labels", "cls", "target"):
            if cand in d.files:
                label_key = cand; break
        if label_key is None:
            raise SystemExit(f"라벨 키를 못찾읍. 키목록: {list(d.files)}")
        print("→ 라벨 키:", label_key)
    beats.append(np.asarray(d["beat"], "float32"))
    refs.append(np.asarray(d["ref"],  "float32"))
    ys.append(np.asarray(d[label_key]).ravel())

beats = np.transpose(np.concatenate(beats), (0, 2, 1)).astype("float32")  # (N,2,300)
refs  = np.transpose(np.concatenate(refs),  (0, 2, 1)).astype("float32")
y     = np.concatenate(ys).astype("int64")

# ── feats/pid/t 는 penult 에서 (같은 sorted 순서라 정렬 일치) ──
p = np.load(PENULT, allow_pickle=True)
feats = p["Z"].astype("float32")
pid   = p["pid"].astype(int)
t     = p["t"].astype("float32")

assert beats.shape[0] == feats.shape[0] == y.shape[0] == pid.shape[0], \
    f"행수 불일치: beat {beats.shape[0]} / feat {feats.shape[0]} / y {y.shape[0]} / pid {pid.shape[0]}"

u, c = np.unique(y, return_counts=True)
print("★ record y 분포:", dict(zip(u.tolist(), c.tolist())))
print("   (0=N,1=S,2=V 3개면 정상. 4~5개면 F/Q 포함 → 매핑 필요)")
print("shapes  beat", beats.shape, " feats", feats.shape)
print("pid 총", len(np.unique(pid)), "명")

np.savez_compressed("mamba_data.npz", beat=beats, ref=refs, feats=feats, y=y, pid=pid, t=t)
print(f"\n저장 완료: mamba_data.npz  ({os.path.getsize('mamba_data.npz')/1e6:.1f} MB)")

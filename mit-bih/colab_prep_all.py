# =============================================================================
#  colab_prep_all.py  —  전체 특징군 복원/준비 마스터 (GPU 교체·런타임 재시작 대비)
#
#  지금까지의 모든 특징군을 한 방에 계산해 Drive(synergy_feats/*.npy)에 영속화한다.
#  전부 CPU(numpy/kymatio) — GPU 무관. GPU는 이후 sweep의 CNN training에만 필요.
#  이미 있는 .npy는 스킵(재개가능) → 재실행 싸다. 다음 '고정백본 시너지 sweep'의 준비물.
#
#  포함 군: [기존10] WST40 MORPHO REPOL4 DTW SEGDEV VCG PWAVE XLEAD DENOISE MF
#          [신규 ] RHYTHM(10, 리듬 innovation) NOISE(7, 잔차 노이즈성격)
#  + 코어 캐시(_WST,_MORPHO,_REPOL,_DTW)를 globals에 세팅(레거시 단일스텝 호환).
#
#  전제(Drive에 함께 있어야): colab_step47_synergy.py, colab_step49_rhythm2.py,
#                          colab_step50_noise.py, colab_recover.py + 추출기 소스들
#  실행(새 런타임에서 1줄):
#    exec(open('/content/drive/MyDrive/mitbih/colab_prep_all.py').read())
#    # → "✔ 전체 복원 완료" + 군별 차원 매니페스트. 이후 sweep 바로.
#  강제 재계산: prep_all(force=True)
# =============================================================================
import os
import numpy as np
_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"

def _need(name, force): return force or not os.path.exists(f"{_FEATDIR}/{name}.npy")
def _exec(fname, g):
    p=f"{_BASE}/{fname}"
    if not os.path.exists(p): print(f"  ✗ 소스 없음: {fname} (Drive에 올려줘)"); return False
    exec(open(p).read(), g); return True

def prep_all(force=False):
    g=globals(); os.makedirs(_FEATDIR, exist_ok=True)
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]

    # ── 1) 기존 10군 + feats0/y/pid : STEP47 synergy_prep 재사용(WST40·DTW 등 계산·저장) ──
    print("[1/4] 기존 10군 (WST40·MORPHO·REPOL4·DTW·SEGDEV·VCG·PWAVE·XLEAD·DENOISE·MF)...")
    if _exec("colab_step47_synergy.py", g):
        try: g["synergy_prep"](force=force)
        except Exception as e: print(f"  ✗ synergy_prep 실패: {type(e).__name__}: {e}")

    # ── 2) RHYTHM(10) : 리듬 innovation (STEP49 extract_rhythm_v2) ──
    print("[2/4] RHYTHM(리듬 innovation 10)...")
    if _need("RHYTHM", force):
        if _exec("colab_step49_rhythm2.py", g):
            R=g["extract_rhythm_v2"](beats,feats0,pid,y,verbose=False)
            np.save(f"{_FEATDIR}/RHYTHM.npy", np.nan_to_num(R).astype("float32")); print(f"  RHYTHM 저장 dim={R.shape[1]}")
    else: print("  RHYTHM 캐시 있음")

    # ── 3) NOISE(7) : 잔차 노이즈성격 (STEP50 extract_noise_features) ──
    print("[3/4] NOISE(잔차 노이즈성격 7)...")
    if _need("NOISE", force):
        if _exec("colab_step50_noise.py", g):
            N=g["extract_noise_features"](beats,pid,y)
            np.save(f"{_FEATDIR}/NOISE.npy", np.nan_to_num(N).astype("float32")); print(f"  NOISE 저장 dim={N.shape[1]}")
    else: print("  NOISE 캐시 있음")

    # ── 4) 코어 캐시 globals 세팅(_WST 등) : colab_recover 재사용(레거시 단일스텝 호환) ──
    print("[4/4] 코어 캐시 globals(_WST,_MORPHO,_REPOL,_DTW) 세팅...")
    _exec("colab_recover.py", g)          # 로드 즉시 recover() 실행됨

    # ── 매니페스트 ──
    print("\n"+"="*60+"\n✔ 전체 복원 완료 — synergy_feats/ 매니페스트:")
    man={}
    for f in sorted(os.listdir(_FEATDIR)):
        if f.endswith(".npy"):
            try: man[f[:-4]]=np.load(f"{_FEATDIR}/{f}").shape
            except: man[f[:-4]]="?"
    for k,v in man.items(): print(f"  {k:10s}: {v}")
    print(f"\n  (N={len(beats)})  이제 고정백본 시너지 sweep 준비 완료. GPU는 sweep CNN에만 필요.")
    return man

prep_all()      # 로드 즉시 1회

# =============================================================================
#  colab_bootstrap.py  —  캐시 복구 부트스트랩 (런타임 재시작 대응)
#
#  Colab 런타임이 끊기면 메모리 캐시(_WST·_MORPHO·_REPOL·_DTW)와 함수정의가 다 날아간다.
#  그때 step39~44 를 돌리면 'NoneType has no attribute shape' 로 죽는다.
#  이 파일 하나만 돌리면 4개 특징을 전부 재계산해 전역 캐시로 복구한다(이미 있으면 스킵).
#
#  전제: 아래 4개 소스가 Drive(_BASE)에 함께 있어야 함
#        colab_step12_wst.py / colab_step15_morpho.py / colab_step18_repol.py / colab_step35_dtw.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_bootstrap.py').read())
#    # → 이후 run_prec / run_wsweep / run_autoweight / run_leadablation / run_nsdiscrim 정상
#    # 강제 재계산: bootstrap_caches(force=True)
# =============================================================================
import numpy as np
_BASE="/content/drive/MyDrive/mitbih"
_SRC=["colab_step12_wst.py","colab_step15_morpho.py","colab_step18_repol.py","colab_step35_dtw.py"]

def bootstrap_caches(force=False):
    g=globals()
    # 1) 함수정의 로드(WST·morpho·repol·DTW 추출기 + 헬퍼)를 전역에 주입
    for f in _SRC:
        path=f"{_BASE}/{f}"
        try:
            exec(open(path).read(), g)                       # g=이 모듈 전역 → __main__ 로 승격됨
        except FileNotFoundError:
            print(f"✗ 없음: {path}  → 이 step 파일도 Drive에 올려줘"); return
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]
    # 2) 환자별 전체비트 중앙값 기준비트(개인정상) — 모든 추출기 공통
    if force or ("_REF" not in g) or (g.get("_REF") is None):
        ref=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],axis=0,keepdims=True)
        g["_REF"]=ref.astype("float32")
    ref=g["_REF"]
    need=lambda k:(force or k not in g or g.get(k) is None)
    # 3) 4개 특징 캐시(있으면 스킵)
    if need("_WST"):
        print("WST 재계산 중(수분)..."); g["_WST"]=compute_wst_features(beats)
    if need("_MORPHO"):
        print("morpho 재계산 중...");     g["_MORPHO"]=extract_morpho_features(beats,ref,pid)
    if need("_REPOL"):
        print("repol 재계산 중...");      g["_REPOL"]=extract_repol_features(beats,ref,pid)
    if need("_DTW"):
        print("DTW 재계산 중(수분)...");  g["_DTW"]=extract_dtw_features(beats,ref,pid,y)
    shp={k:g[k].shape for k in ("_WST","_MORPHO","_REPOL","_DTW")}
    print("\n✔ 캐시 복구 완료:", {k:v[1] for k,v in shp.items()}, f"(N={beats.shape[0]})")
    print("  이제 run_prec / run_wsweep / run_autoweight / run_leadablation / run_nsdiscrim 정상 동작.")
    return shp

bootstrap_caches()      # 로드 즉시 1회 실행(이미 캐시 있으면 스킵)

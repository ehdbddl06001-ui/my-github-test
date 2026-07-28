# =============================================================================
#  colab_recover.py  —  런타임 끊김 스마트 복구 (Drive 저장본 우선 로드)
#
#  런타임 재시작 시 메모리 캐시(_WST 등)·pip(kymatio)·함수정의가 다 날아간다.
#  STEP47 prep이 이미 특징행렬을 Drive(synergy_feats/*.npy)에 저장해뒀으므로 그걸 '로드'해
#  즉시 복구한다(WST·DTW 재계산 회피). 저장본 없으면 그 군만 재계산(fallback).
#
#  핵심: synergy가 저장한 WST.npy는 이미 SelectKBest(40) 적용본. 다운스트림이 다시
#        SelectKBest(40)을 걸면 40중40=동일 → 그대로 _WST로 써도 결과 동일(안전).
#        단 REPOL 저장본은 [0,1,4,5] 4열이라 다운스트림 슬라이스와 안 맞음 → raw로 재계산(초 단위).
#
#  실행(재시작 후 1줄):
#    exec(open('/content/drive/MyDrive/mitbih/colab_recover.py').read())
#    # → _WST,_MORPHO,_REPOL,_DTW,(_SEGDEV,_VCG,_PWAVE,_XLEAD,_MF) 복구.
#    # 이후 diag_rhythm()/run_finale()/run_synergy()/run_nsdiscrim() 정상.
#  전체 raw WST 강제 재계산이 필요하면: recover(full_wst=True)
# =============================================================================
import os, importlib, subprocess, sys
import numpy as np
_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
# 저장본이 raw 추출기 출력과 동일한 군(그대로 로드 가능). WST는 40본을 _WST로(재선택=동일).
_DIRECT={"_MORPHO":"MORPHO","_DTW":"DTW","_SEGDEV":"SEGDEV","_VCG":"VCG",
         "_PWAVE":"PWAVE","_XLEAD":"XLEAD","_MF":"MF"}
_SRC={"_WST":"colab_step12_wst.py","_MORPHO":"colab_step15_morpho.py","_REPOL":"colab_step18_repol.py",
      "_DTW":"colab_step35_dtw.py","_SEGDEV":"colab_step28_segdev.py","_VCG":"colab_step33_vcg.py",
      "_PWAVE":"colab_step9_pwave.py","_XLEAD":"colab_step25_xlead.py","_MF":"colab_step17_mf.py"}

def _ensure(pkg):
    try: importlib.import_module(pkg)
    except ModuleNotFoundError:
        print(f"  '{pkg}' 재설치..."); subprocess.run([sys.executable,"-m","pip","install","-q",pkg],check=True); importlib.invalidate_caches()

def _load(name):
    p=f"{_FEATDIR}/{name}.npy"; return np.load(p) if os.path.exists(p) else None

def _medref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _srcexec(g, cache):
    exec(open(f"{_BASE}/{_SRC[cache]}").read(), g)          # 추출기+헬퍼를 전역에 주입

def recover(full_wst=False):
    if not os.path.isdir(_BASE):
        print(f"✗ {_BASE} 없음. Drive 마운트 먼저: from google.colab import drive; drive.mount('/content/drive')"); return
    g=globals()
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]; m1=np.isin(pid,_DS1)
    ref=_medref(beats,pid); loaded=[]; recomputed=[]

    # ── WST: 저장본(WST40) 로드 우선 / 없거나 full_wst면 raw 재계산 ──
    w=_load("WST")
    if (w is not None) and (not full_wst):
        g["_WST"]=w.astype("float32"); loaded.append(f"_WST({w.shape[1]}, synergy40=재선택시 동일)")
    else:
        _srcexec(g,"_WST"); _ensure("kymatio"); print("  _WST raw 재계산(수분)...")
        g["_WST"]=np.nan_to_num(g["compute_wst_features"](beats)).astype("float32"); recomputed.append(f"_WST({g['_WST'].shape[1]})")

    # ── 저장본 그대로 로드 가능한 군(MORPHO/DTW/SEGDEV/VCG/PWAVE/XLEAD/MF) ──
    for cache,fname in _DIRECT.items():
        mat=_load(fname)
        if mat is not None:
            g[cache]=mat.astype("float32"); loaded.append(f"{cache}({mat.shape[1]})")
        else:                                              # 저장본 없으면 재계산(fallback)
            try:
                _srcexec(g,cache)
                if cache=="_DTW":   g[cache]=g["extract_dtw_features"](beats,ref,pid,y)
                elif cache=="_MF":  T,Xn=g["build_templates"](beats,y,m1); g[cache]=g["extract_mf_features"](Xn,T)
                else:               g[cache]=g[{"_MORPHO":"extract_morpho_features","_SEGDEV":"extract_segdev_features",
                                                "_VCG":"extract_vcg_features","_PWAVE":"extract_pwave_features",
                                                "_XLEAD":"extract_xlead_features"}[cache]](beats,ref,pid)
                g[cache]=np.nan_to_num(g[cache]).astype("float32"); recomputed.append(f"{cache}({g[cache].shape[1]})")
            except Exception as e:
                print(f"  ✗ {cache} 복구 실패: {type(e).__name__}: {e}")

    # ── REPOL: 저장본은 4열 subset이라 다운스트림([:, [0,1,4,5]])과 불일치 → raw 12 재계산(초) ──
    _srcexec(g,"_REPOL"); g["_REPOL"]=np.nan_to_num(g["extract_repol_features"](beats,ref,pid)).astype("float32")
    recomputed.append(f"_REPOL({g['_REPOL'].shape[1]}, raw)")

    print(f"\n✔ Drive 로드: {loaded}")
    print(f"✔ 재계산   : {recomputed}")
    core=all(k in g and g[k] is not None for k in ("_WST","_MORPHO","_REPOL","_DTW"))
    print(f"{'✔ 코어 캐시(_WST,_MORPHO,_REPOL,_DTW) 준비 완료' if core else '✗ 코어 캐시 일부 누락'} (N={len(beats)})")
    print("  이제 diag_rhythm() / run_finale() / run_nsdiscrim() / run_synergy() 정상 동작.")
    return {"loaded":loaded,"recomputed":recomputed}

recover()      # 로드 즉시 1회 실행

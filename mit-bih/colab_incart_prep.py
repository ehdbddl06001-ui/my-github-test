# =============================================================================
#  colab_incart_prep.py  —  [교차DB ①] INCART → MIT-BIH 포맷 전처리 (incart_data.npz)
#
#  St.Petersburg INCART(12리드·257Hz·75레코드)를 우리 MIT-BIH 포맷(2채널·360Hz·300샘플·N/S/V)으로.
#  단계: wfdb 다운로드 → 리드 II·V1 선택 → 리샘플 257→360Hz(R위치 보정) → R중심 300샘플 세그먼트
#        → AAMI 라벨(N/S/V) → per-beat 정규화(스케일 매칭) → incart_data.npz(beat,y,pid,rr)
#  ※ 진폭 스케일은 MIT-BIH 전처리가 불명 → mitbih_beat_stats()로 통계 뽑아 맞춘다.
#  ※ RR(pre/post)도 R-peak 주석에서 계산해 저장(feats0 재구성·RHYTHM 타이밍용).
#
#  실행(Colab):
#    exec(open('/content/drive/MyDrive/mitbih/colab_incart_prep.py').read())
#    mitbih_beat_stats()          # 먼저 MIT-BIH 비트 스케일 확인(정규화 맞추기용)
#    build_incart(n_rec=None)     # 전체(느림, ~수십분). 테스트는 n_rec=5
# =============================================================================
import os
import numpy as np

_BASE="/content/drive/MyDrive/mitbih"; _DLDIR=f"{_BASE}/incart_raw"
_FS_SRC=257; _FS_DST=360; _L=300; _RPRE=100      # R중심: [R-100, R+200] = 300샘플 (argmax로 재정합되므로 여유만)
# AAMI 매핑: 기호 → 0=N,1=S,2=V (F/Q는 제외)
_AAMI={ 'N':0,'L':0,'R':0,'e':0,'j':0, 'A':1,'a':1,'J':1,'S':1, 'V':2,'E':2 }

def _ensure(pkg):
    import importlib,subprocess,sys
    try: importlib.import_module(pkg)
    except ModuleNotFoundError: subprocess.run([sys.executable,"-m","pip","install","-q",pkg],check=True)

def mitbih_beat_stats():
    """MIT-BIH 비트 스케일 통계(INCART 정규화 맞추기용)."""
    d=np.load(f"{_BASE}/mamba_data.npz"); b=d["beat"]
    print(f"MIT-BIH beat: shape={b.shape}  dtype={b.dtype}")
    print(f"  전체 mean={b.mean():.4f} std={b.std():.4f}  min={b.min():.3f} max={b.max():.3f}")
    print(f"  채널0(MLII): mean={b[:,0].mean():.4f} std={b[:,0].std():.4f}")
    print(f"  채널1(V1?) : mean={b[:,1].mean():.4f} std={b[:,1].std():.4f}")
    print(f"  비트당 std 중앙값: ch0={np.median(b[:,0].std(1)):.4f} ch1={np.median(b[:,1].std(1)):.4f}")
    print("  → 이 통계에 맞춰 build_incart 의 정규화(norm=) 결정")
    return b.mean(),b.std()

def build_incart(n_rec=None, norm="perbeat_z", dl=True):
    """INCART 다운로드·전처리 → incart_data.npz. norm: 'perbeat_z'(비트별 z) | 'none'."""
    _ensure("wfdb"); import wfdb
    from scipy.signal import resample_poly
    os.makedirs(_DLDIR,exist_ok=True)
    # 레코드 목록
    try: recs=wfdb.get_record_list("incartdb")
    except Exception: recs=[f"I{ i:02d}" for i in range(1,76)]
    if n_rec: recs=recs[:n_rec]
    print(f"INCART {len(recs)}레코드 처리 (norm={norm})...")
    BEAT=[]; Y=[]; PID=[]; PRE=[]; POST=[]
    for ri,rec in enumerate(recs):
        try:
            if dl:
                for ext in ("dat","hea","atr"):
                    try: wfdb.dl_files("incartdb",_DLDIR,[f"{rec}.{ext}"])
                    except Exception: pass
            r=wfdb.rdrecord(f"{_DLDIR}/{rec}"); ann=wfdb.rdann(f"{_DLDIR}/{rec}","atr")
        except Exception as e:
            print(f"  ✗ {rec}: {type(e).__name__} {e}"); continue
        names=[s.upper() for s in r.sig_name]
        if "II" not in names or "V1" not in names: print(f"  ✗ {rec}: 리드없음 {r.sig_name}"); continue
        sig=r.p_signal[:,[names.index("II"),names.index("V1")]].T          # (2, T) @257Hz
        sig=np.stack([resample_poly(sig[c],_FS_DST,_FS_SRC) for c in range(2)])   # →360Hz
        scale=_FS_DST/_FS_SRC; samp=(ann.sample*scale).astype(int); sym=ann.symbol; T=sig.shape[1]
        rr=np.diff(samp)                                                    # 샘플단위 RR
        for i in range(len(samp)):
            lab=_AAMI.get(sym[i],None)
            if lab is None: continue
            R=samp[i]; a,b2=R-_RPRE,R-_RPRE+_L
            if a<0 or b2>T: continue
            seg=sig[:,a:b2].astype("float32")
            if norm=="perbeat_z":
                seg=(seg-seg.mean(1,keepdims=True))/(seg.std(1,keepdims=True)+1e-6)
            pre=rr[i-1] if i>0 else (rr[i] if i<len(rr) else 300)
            post=rr[i] if i<len(rr) else pre
            BEAT.append(seg); Y.append(lab); PID.append(ri); PRE.append(pre); POST.append(post)
        if (ri+1)%10==0 or ri==len(recs)-1: print(f"  {ri+1}/{len(recs)}  누적비트 {len(BEAT)}")
    BEAT=np.stack(BEAT); Y=np.array(Y,np.int64); PID=np.array(PID,np.int64); PRE=np.array(PRE,"float32"); POST=np.array(POST,"float32")
    out=f"{_BASE}/incart_data.npz"; np.savez(out,beat=BEAT,y=Y,pid=PID,pre_rr=PRE,post_rr=POST)
    n=len(Y); print(f"\n✔ 저장 {out}")
    print(f"  비트 {n}  (N={int((Y==0).sum())} S={int((Y==1).sum())} V={int((Y==2).sum())})  환자 {len(np.unique(PID))}")
    print(f"  beat shape {BEAT.shape}  mean={BEAT.mean():.3f} std={BEAT.std():.3f}")
    print(f"  → mitbih_beat_stats()와 스케일 비슷한지 확인. 다르면 norm 조정.")
    return out

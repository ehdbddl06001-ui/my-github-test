# =============================================================================
#  svdb_prep.py  —  [대규모 Phase A] MIT-BIH SVDB 전처리 (검정력 확보용)
#
#  왜: MIT-BIH DS2는 S를 가진 환자가 16명뿐 → 매크로 F1 95%CI ±0.16(검출 불가).
#      SVDB(78레코드, 2리드)는 '상심실성 부정맥 보강'을 목적으로 만들어진 DB.
#      환자 수 16→수십 = 검정력 ±0.16 → ±0.07. 비로소 0.07 크기 효과를 검정 가능.
#  왜 SVDB부터: 2리드·AAMI·같은 기관 규약 → 도메인 shift 교란 최소, 파이프라인 거의 그대로.
#
#  LARGESCALE_PLAN.md 의 선결수정 반영:
#   F1 R피크 재정합 : 주석 위치 ±50ms 창에서 argmax|VM| 재탐색 (INCART 문제 예방)
#   F2 정규화 대칭  : per-beat z정규로 저장 → 특징계산도 동일 비트에서
#   F3 환자 단위    : SVDB는 레코드=환자 1:1 (INCART와 달리 병합 불필요)
#   F4 대역         : 128→360Hz 업샘플. ★주의: 원 MIT-BIH(360)와 대역이 다르므로
#                     '동일 대역 MIT-BIH 기준선'을 반드시 병기할 것(계획서 §3 F4)
#
#  실행(Colab):
#    exec(open('/content/drive/MyDrive/mitbih/svdb_prep.py').read())
#    svdb_stats()                 # 다운로드 없이 목록·규모 확인
#    build_svdb(n_rec=5)          # 소규모 시험
#    build_svdb()                 # 전체(78레코드, 수십분)
# =============================================================================
import os
import numpy as np

_BASE="/content/drive/MyDrive/mitbih"; _DLDIR="/content/svdb_raw"
_FS_SRC=128; _FS_DST=360; _L=300; _RPRE=100
_RALIGN_MS=50                                   # F1: R 재정합 탐색 반경(±50ms)
# AAMI: 0=N, 1=S(상심실), 2=V(심실).  F/Q 및 기타는 제외
_AAMI={'N':0,'L':0,'R':0,'e':0,'j':0, 'A':1,'a':1,'J':1,'S':1, 'V':2,'E':2}

def _ensure(pkg):
    import importlib,subprocess,sys
    try: importlib.import_module(pkg)
    except ModuleNotFoundError: subprocess.run([sys.executable,"-m","pip","install","-q",pkg],check=True)

def svdb_stats():
    """SVDB 레코드 목록·리드 구성 확인(다운로드 최소)."""
    _ensure("wfdb"); import wfdb
    try: recs=wfdb.get_record_list("svdb")
    except Exception: recs=[str(i) for i in range(800,895)]
    print(f"SVDB 레코드 {len(recs)}개: {recs[:8]} ...")
    print(f"  원 샘플링 {_FS_SRC}Hz → {_FS_DST}Hz 리샘플, R중심 {_L}샘플")
    print(f"  ★계획서 §3 F4: 대역이 원 MIT-BIH(360Hz 원본)와 달라 '동일대역 MIT-BIH 기준선' 병기 필수")
    return recs

def _realign_R(sig, R, fs=_FS_DST, ms=_RALIGN_MS):
    """F1: 주석 R 주변 ±ms 에서 벡터크기 최대점으로 재정합(주석 지터 흡수)."""
    w=int(fs*ms/1000.0); a=max(0,R-w); b=min(sig.shape[1],R+w+1)
    if b-a<3: return R
    vm=np.sqrt(sig[0,a:b]**2+sig[1,a:b]**2)
    return a+int(np.argmax(vm))

def build_svdb(n_rec=None, dl=True, dldir=None, realign=True, out=None):
    """SVDB 다운로드·전처리 → svdb_data.npz(beat,y,pid,pre_rr,post_rr). 재개 지원."""
    _ensure("wfdb"); import wfdb
    from scipy.signal import resample_poly
    dldir=dldir or _DLDIR; os.makedirs(dldir,exist_ok=True)
    try: recs=wfdb.get_record_list("svdb")
    except Exception: recs=[str(i) for i in range(800,895)]
    if n_rec: recs=recs[:n_rec]
    print(f"SVDB {len(recs)}레코드 처리 (realign={realign}, dldir={dldir}) — 받은 건 스킵")
    BEAT=[];Y=[];PID=[];PRE=[];POST=[]; nrealign=[]
    for ri,rec in enumerate(recs):
        try:
            if dl:
                for ext in ("hea","dat","atr"):
                    fp=f"{dldir}/{rec}.{ext}"
                    if os.path.exists(fp) and os.path.getsize(fp)>0: continue
                    for _t in range(3):
                        try: wfdb.dl_files("svdb",dldir,[f"{rec}.{ext}"]); break
                        except Exception: pass
            r=wfdb.rdrecord(f"{dldir}/{rec}"); ann=wfdb.rdann(f"{dldir}/{rec}","atr")
        except Exception as e:
            print(f"  ✗ {rec}: {type(e).__name__} {e} → 파일 삭제(재실행시 재다운)")
            for ext in ("hea","dat","atr"):
                try: os.remove(f"{dldir}/{rec}.{ext}")
                except Exception: pass
            continue
        if r.p_signal is None or r.p_signal.shape[1]<2:
            print(f"  ✗ {rec}: 2리드 아님 {r.sig_name}"); continue
        sig=r.p_signal[:,:2].T                                    # (2,T) @128Hz
        sig=np.stack([resample_poly(sig[c],_FS_DST,_FS_SRC) for c in range(2)])
        scale=_FS_DST/_FS_SRC; samp=(ann.sample*scale).astype(int); sym=ann.symbol; T=sig.shape[1]
        # F1: R 재정합 (라벨 미사용, 신호만)
        if realign:
            new=np.array([_realign_R(sig,int(s)) for s in samp])
            nrealign.append(float(np.mean(np.abs(new-samp))/_FS_DST*1000)); samp=new
        rr=np.diff(samp)
        for i in range(len(samp)):
            lab=_AAMI.get(sym[i],None)
            if lab is None: continue
            R=samp[i]; a,b2=R-_RPRE,R-_RPRE+_L
            if a<0 or b2>T: continue
            seg=sig[:,a:b2].astype("float32")
            seg=(seg-seg.mean(1,keepdims=True))/(seg.std(1,keepdims=True)+1e-6)   # F2: per-beat z
            pre=rr[i-1] if i>0 else (rr[i] if i<len(rr) else 300)
            post=rr[i] if i<len(rr) else pre
            BEAT.append(seg);Y.append(lab);PID.append(ri);PRE.append(pre);POST.append(post)
        if (ri+1)%10==0 or ri==len(recs)-1: print(f"  {ri+1}/{len(recs)}  누적비트 {len(BEAT)}")
    BEAT=np.stack(BEAT);Y=np.array(Y,np.int64);PID=np.array(PID,np.int64)
    PRE=np.array(PRE,"float32");POST=np.array(POST,"float32")
    out=out or f"{_BASE}/svdb_data.npz"
    np.savez(out,beat=BEAT,y=Y,pid=PID,pre_rr=PRE,post_rr=POST)
    n=len(Y); nS=int((Y==1).sum())
    print(f"\n✔ 저장 {out}")
    print(f"  비트 {n}  (N={int((Y==0).sum())} S={nS} V={int((Y==2).sum())})  레코드 {len(np.unique(PID))}")
    print(f"  S 유병률 {100*nS/max(n,1):.2f}%")
    if realign and nrealign: print(f"  R 재정합 평균 이동 {np.mean(nrealign):.1f} ms (주석 지터 크기)")
    # ★검정력: S를 가진 레코드 수로 계산
    withS=[int(p) for p in np.unique(PID) if (Y[PID==p]==1).sum()>0]
    N=len(withS); ci=1.96*0.32/max(np.sqrt(N),1)
    print(f"\n  ★검정력: S 보유 레코드 {N}개 → 매크로F1 95%CI ≈ ±{ci:.3f}")
    print(f"    (MIT-BIH DS2는 16명 ±0.157. {'개선됨' if N>16 else '개선 없음'})")
    return out

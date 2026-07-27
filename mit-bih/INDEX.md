# MIT-BIH SVEB(상심실 이소성) 분류 — 전체 알고리즘 설계 인덱스

**목표**: 정직한 inter-patient 세팅(de Chazal DS1 22명 학습 → DS2 22명 테스트)에서 SVEB(S) 검출.
주지표 **S_PR-AUC**(Average Precision) + F1/PREC/SEN. 벤치마크 Farag(SVEB F1≈0.82).

**철칙(무결성)**: DS2로 절대 튜닝 안 함. DS2 라벨은 최종 평가에만. 모든 하이퍼파라미터는
DS1 클래스 카운트/공식에서 유도(DS2 최적화 금지).

---

## 0. 핵심 파일 (여기부터 보면 됨)

| 파일 | 역할 |
|---|---|
| `colab_common.py` | DS1 유도 전이 하이퍼파라미터 단일 소스: `auto_weights`(effective-number), `ldam_margins`, `scaled_lr` |
| `colab_prep_all.py` | 마스터 특징 복원 — 12+개 특징군을 Drive 캐시로 계산(WST/MORPHO/REPOL/DTW/…/RHYTHM/KOOPMAN/AE/GNN) |
| `colab_step49_rhythm2.py` | **RHYTHM innovation(최대 성과)** — 환자별 인과 EWMA(=이산 선형 SDE/칼만 innovation) 예측 잔차 = 조기성 신호. 보상성 지수로 APC/PVC 분리 |
| `colab_step47_synergy.py` | 코어 특징 시너지(WST40+MORPHO16+REPOL4+DTW) 조합·저장 |
| `colab_crossdb.py` | **교차DB 외부검증** — MIT-BIH 학습 → INCART 적용. v1(형태)/v2(형태+리듬) A/B |
| `colab_incart_prep.py` | INCART(러시아·257Hz·12리드) → MIT-BIH 포맷(2채널·360Hz·N/S/V) 전처리 |
| `colab_step65_stats.py` | 통계 검증: val↔test 순위상관·순열검정·bootstrap CI |
| `FINDINGS.md` | 발견 요약(승리/실패/방법론) |

---

## 1. 데이터·베이스라인
- `colab_step1.py` `colab_step3*.py` `colab_step4.py` `colab_step5.py` : 초기 베이스라인 CNN
- `cnn_base_psa2_step1.py` : 기본 CNN 구조
- `colab_bootstrap.py` `colab_recover.py` : 캐시 부트스트랩/복구

## 2. 특징 추출기 (형태 축)
- `colab_step12_wst.py` : **WST**(Wavelet Scattering, kymatio) — 이동불변 다중스케일 형태
- `colab_step15_morpho.py` : **MORPHO**(16) — 형태 편차
- `colab_step18_repol.py` `colab_step19_repolk.py` : **REPOL**(재분극)
- `colab_step17_mf.py` `colab_step27_mfconv.py` : MF(정합필터)
- `colab_step28_segdev.py` `colab_step29_segcnn.py` : SEGDEV(세그먼트 편차)
- `colab_step33_vcg.py` : VCG(벡터심전도)
- `colab_step9_pwave.py` : PWAVE(P파)
- `colab_step25_xlead.py` : XLEAD(교차리드)
- `colab_step10_denoise.py` : DENOISE
- `colab_step35_dtw.py` `colab_step41_dtwmv.py` : DTW(템플릿 정합)

## 3. 특징 추출기 (동역학·구조 축 — 새 축)
- `colab_step48_rhythm.py` `colab_step49_rhythm2.py` : **RHYTHM**(리듬 innovation, 최대 성과)
- `colab_step50_noise.py` : NOISE(잔차 노이즈 성격)
- `colab_step52_newfeats.py` : **KOOPMAN**(DMD 선형연산자 잔차) · **AE**(오토인코더 재구성오차) · **GNN**(kNN/LOF 구조)
- `colab_step51_recency.py` : 최근성 가중

## 4. 모델 구조·앙상블
- `colab_step7_dualhead.py` `colab_step8_stack.py` `colab_step38_stack2.py` : 듀얼헤드/스태킹
- `colab_step22_gate.py` `colab_step23_moe.py` `colab_step36_moe2.py` : 게이팅/MoE
- `colab_step24_knn.py` : kNN 하이브리드
- `colab_step30_ptbranch.py` `colab_step31_specialist.py` : 전문가 분기
- `colab_step32_synergy.py` `colab_step47_synergy.py` : 특징 시너지 스윕
- `colab_step54_sweep2.py` : 2^7 특징군 조합 스윕
- `ensemble_eval.py` `grand_ensemble.py` `grand_ensemble_v2.py` : 대앙상블

## 5. 손실·불균형 대응
- `colab_step21_ds1weight.py` `colab_step40_weight.py` `colab_step42_autoweight.py` : DS1 유도 클래스 가중(effective-number)
- `colab_step39_precision.py` : 정밀도 지향(LDAM margin)
- `colab_step59_asl.py` : ASL(비대칭 손실)
- `colab_step57_smote.py` : SMOTE/오버샘플링
- `colab_step44_nsdiscrim.py` `colab_step46_nslever.py` : N/S 판별 강화
- `colab_step56_atrial.py` : 심방 P 잔차(subtle-S)

## 6. 안정화·분산·통계 (방법론적 핵심)
- `colab_step62_stable.py` : 결정성 + 시드 분산 리포트(F1 0.737±0.064)
- `colab_step63_robust.py` : 강건성
- `colab_step64_swa.py` : SWA(가중치 평균)
- `colab_step65_stats.py` : **val↔test 순위상관 비유의 증명**(선택 불가능성) + bootstrap CI
- `hardness_analysis.py` `inspect_patient_boundary.py` : 난이도/환자경계 분석

## 7. 통합·최종
- `colab_step45_finale.py` `colab_step53_topauc.py` `colab_step55_fuse.py` `colab_step58_fuse2.py` `colab_step60_total.py` : 융합/최종
- `colab_step61_context.py` : 다중비트 컨텍스트
- `colab_step66_patemb.py` : 환자 임베딩

## 8. 교차DB 외부검증 (최신)
- `colab_incart_prep.py` : INCART 전처리
- `colab_crossdb.py` : MIT-BIH→INCART 전이. **v1(형태) S_PR 0.020 → v2(+리듬) S_PR 0.088(7.9× lift)**

---

## 핵심 발견 요약
- **최대 성과 = RHYTHM innovation**: 환자별 인과 EWMA로 리듬 예측 → 잔차가 조기성. PREC 0.725→0.802.
- **방법론적 발견(논문 핵심)**: DS1-val이 DS2를 예측 못함(Spearman ρ=0.07 p=0.78; 순열 p=0.23) →
  검증기반 선택이 통계적으로 무효 → 무지도 trim 앙상블 보고. 큰 시드 분산(F1 σ~0.06)은 22명 DS1 분할에 기인.
- **교차DB**: V(형태정의)는 리듬 없이도 전이(V_PR 0.69→0.85), S(타이밍정의)는 리듬 없으면 우연(0.02),
  리듬 넣으면 7.9× lift(0.088). → "S 판별은 형태가 아니라 리듬이 나른다"를 두 DB로 입증.
- **정직한 최종(MIT-BIH inter-patient)**: 무지도 trim 앙상블 S_PR 0.784 [0.765–0.801], F1 0.775 [0.761–0.792].

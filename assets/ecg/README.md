# ECG 실데이터 에셋 (오픈 신호 DB)

`pipelines/ingest_ecg.py`로 오픈 심전도 DB의 신호를 잘라 담은 JSON들. `export`가
`figure: {type: ecg_signal, source: assets/ecg/<name>.json}`에서 이걸 읽어
`pipelines/render_signal_svg.py`로 SVG를 그린다(런타임 네트워크·wfdb 불필요).

**합성(gen_ecg_svg)과 달리 진짜 파형**이므로, 모양이 본질인 진단(향후 12유도 확장 시
브루가다·STEMI 등)도 안전하게 다룰 수 있다. 단 재배포 가능한 **오픈 라이선스만** 담고
출처를 표기한다.

## 수록 목록
| 파일 | 출처 | 라이선스 |
|------|------|----------|
| `mitdb-100.json` | MIT-BIH Arrhythmia Database (PhysioNet), MIT-LCP/wfdb-python 샘플데이터 | ODC-BY 1.0 |
| `ptbxl-00001-norm.json` | PTB-XL 1.0.3 (PhysioNet), ecg_id 1 — 정상 12유도 | CC-BY 4.0 |
| `ptbxl-00172-crbbb.json` | PTB-XL 1.0.3 (PhysioNet), ecg_id 172 — 완전우각차단+LAFB 12유도 | CC-BY 4.0 |
| `ptbxl-00270-imi.json` | PTB-XL 1.0.3 (PhysioNet), ecg_id 270 — 하벽·전중격 심근경색 12유도 | CC-BY 4.0 |

**12유도(PTB-XL)** 는 `figure: {type: ecg12, source: assets/ecg/<name>.json}` 로 표준
3×4 + 리듬 스트립으로 렌더한다(`render_signal_svg.twelve_lead_svg`). CC-BY이므로
문항 `참고문헌`·에셋 `source`에 PTB-XL 출처를 표기한다.

PhysioNet 직접 접근이 막힌 환경에선 **오픈 S3 미러**에서 받는다:
`https://physionet-open.s3.amazonaws.com/ptb-xl/1.0.3/records100/<폴더>/<id>_lr.{hea,dat}`
(진단 라벨은 `ptbxl_database.csv` 의 `scp_codes`.)

## 새 레코드 추가(데이터 접근 되는 환경에서 1회)
```
pip install wfdb
python pipelines/ingest_ecg.py --record <경로/레코드> --name <이름> \
    --start 0 --seconds 6 --leads MLII --source "<출처>" --license "<라이선스>"
```
PhysioNet 직접 접근이 정책상 막힌 환경에선 AWS/GCS 미러나 GitHub 샘플에서
`.hea`/`.dat`를 받아 로컬 경로로 넘긴다. (PTB-XL 등 12유도·병리 레코드는 CC-BY.)

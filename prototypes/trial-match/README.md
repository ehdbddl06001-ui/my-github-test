# TrialMatch — 임상시험 연결 검색 플랫폼 (프로토타입)

표준치료·희귀의약품으로도 치료가 어려운 환자가 **자기 상황을 검색창에 자유롭게 적으면**,
현재 **모집 중인 실제 임상시험**을 찾아 선정기준과 대조하고 공식 연락처로 연결한다.

앞의 `oncoreg-ai` 모듈과 **같은 방식**(Colab + Gemini + Flask + cloudflared)으로 동작하는
독립 모듈이다.

```
[검색창(자유입력)] --> [Gemini: 검색어 해석] --> [ClinicalTrials.gov API: 모집중 시험 조회(실데이터)]
                                              --> [Gemini: 선정기준 대조·적합도 채점] --> 결과·연결
```

## 설계 원칙 — "IRB/규제가 허락한 부분만"
- 임상시험 정보는 **지어내지 않는다.** ClinicalTrials.gov 공개 API(v2)로 **실제 등록·모집중**
  시험만 가져온다. (중재연구는 기관생명윤리위원회(IRB)/규제기관 승인 하에 등록·수행됨)
- Gemini 는 (1) 한글 자유입력을 검색어로 해석하고 (2) 선정기준과 환자를 대조해 **적합도(참고
  추정치)** 를 매기는 보조 역할만 한다. 판정 주체가 아니다.
- 본 도구는 **환자를 직접 모집·중개하지 않는다.** 표시 연락처는 각 시험의 공식 등록 연락처이며,
  최종 참여 결정·적격 판정은 **담당 의료진과 실시기관**이 한다. 개인 식별정보는 입력하지 않는다.

> ⚠️ `IRP`로 적어주셨는데 **IRB(기관생명윤리위원회)** 로 해석해 반영했습니다. 다른 의미(예: 특정
> 기관 프로그램)였다면 알려주세요.

## 파일
| 파일 | 역할 |
|---|---|
| `TrialMatch_Colab.ipynb` | **Colab 업로드용 노트북** (셀 실행만으로 동작) |
| `server.py` | Flask + Gemini + ClinicalTrials.gov 조회 (`/api/search`, `/api/health`) |
| `templates/index.html` | 검색엔진형 프론트엔드 (자유입력 → 결과 → 연결 초안) |
| `build_notebook.py` | 노트북 생성기 |
| `requirements.txt` | 로컬 실행 의존성 |

## 실행 — Colab (권장)
1. Gemini 키 발급: <https://aistudio.google.com/app/apikey>
2. Colab → **파일 → 노트북 업로드** → `TrialMatch_Colab.ipynb`
3. 셀 순서대로: ①설치 → ②파일 기록 → ③**키 입력**(+CT.gov 연결 자동 확인) → ④**서버 실행**
4. 출력된 **`trycloudflare.com` 주소를 새 탭에서 열기** → 검색창 등장.
5. 환자 상황을 적고 검색 → 모집중 시험이 **적합도순**으로, 클릭하면 선정기준 대조·기관·연락처·
   **담당 의사 전달용 문의 초안**이 표시된다.

## 실행 — 로컬
```bash
cd prototypes/trial-match
pip install -r requirements.txt
export GEMINI_API_KEY="키"          # Windows(PS): $env:GEMINI_API_KEY="키"
python server.py                     # http://localhost:8000
```

## 동작 확인 포인트 (시연용)
- **엔진 배지**: `Gemini · 모델명` = 연동됨.
- **검색**: 예시 칩을 눌러 자유입력 → `해석된 검색`(한글 요약 + 영어 검색어) + **데이터 출처 배지**
  (`실데이터 · ClinicalTrials.gov` / `표본 데이터`)가 뜬다.
- **결과 카드**: 상태(모집중/모집예정), 단계, 조건, **적합도 바**, 한 줄 요약.
- **상세(우측)**: 선정·제외 대조 체크리스트, 원문 eligibility, 실시기관, 공식 연락처,
  CT.gov 원문 링크, **문의 초안 복사**.
- **표본 데이터로 미리보기** 체크 시 Gemini/네트워크 없이 UI 흐름만 시연.

## 데이터 소스 메모
- ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`) — 무료·키 불필요.
  상태 필터 `RECRUITING,NOT_YET_RECRUITING` 로 '진행 중' 시험만 조회.
- 국내(한국) 시험 위주로 보려면 검색 문장에 지역(예: "국내", "한국")을 넣으면 Gemini가
  `location_en`(예: "Korea")으로 변환해 `query.locn` 에 반영한다.
- 국내 전용 등록부(질병관리청 **CRIS**)를 붙이고 싶으면 `server.py`의 `fetch_ctgov` 옆에
  동일 형태의 `fetch_cris`를 추가하고 결과를 합치면 된다(같은 결과 구조 사용).

## 흔한 문제
- **옛/다른 노트북을 열었는데 이 앱(또는 저 앱)이 뜬다**: 같은 Colab 런타임에서 두 앱을 돌리면
  파이썬이 먼저 로드한 모듈을 캐시해 파일을 다시 안 읽습니다. 이 노트북은 전용 폴더
  (`trialmatch/`)·전용 모듈명(`trialmatch_app`)·전용 포트(8001)로 분리했고 0단계에 캐시 정리
  셀을 뒀습니다. 그래도 섞이면 **런타임 → 세션 다시 시작** 후 원하는 노트북만 실행하세요.
  실행 셀의 `>>> 실행 중인 앱: TrialMatch` 출력으로 확인할 수 있습니다.
- **결과가 표본으로 뜬다**: CT.gov 미도달(사내망 차단 등) 또는 백엔드 미실행. Colab의 외부망은
  열려 있어 대개 실데이터가 나온다(③번 셀의 연결 확인 참고).
- **결과가 비어 있음**: 진단명이 너무 구체적이거나 지역 필터가 좁을 때. 더 일반적 진단명으로.
- **429**: Gemini 무료 한도 초과 — 잠시 후 재시도 또는 `GEMINI_MODEL=gemini-2.0-flash`.

## 노트북 재생성
`server.py`/`templates/index.html` 수정 후: `python build_notebook.py`

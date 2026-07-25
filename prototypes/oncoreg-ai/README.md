# OncoReg AI — Gemini 연동 프로토타입

허가초과(off-label) **근거 문서 생성 + 임상시험 적격성 검토** 데모를,
하드코딩 데이터 대신 **내 Google Gemini API** 로 실제 동작시킨다.

원래 준 HTML은 `CASES` 라는 하드코딩 데이터로만 돌았다. 여기서는 브라우저가
`검색` 버튼을 누르면 → 작은 백엔드(Flask)가 → Gemini 를 호출해 문헌·지표·임상시험을
JSON 으로 구조화해 돌려주고 → 화면이 그걸 렌더링한다. 문서 생성 단계의 서술 문단도
Gemini 로 생성한다.

```
[브라우저 HTML]  --fetch-->  [Flask 백엔드(server.py)]  --API-->  [Gemini]
   화면 렌더링     api/search / api/generate      근거 JSON 생성
```

> ⚠️ **의료 안전** — 문헌·수치·임상시험은 Gemini가 생성한 초안이라 실제 출판물과
> 다를 수 있습니다. 데모/프로토타입 용도이며, 인용·제출 전 반드시 원문 대조와
> 약사·의사의 검증이 필요합니다. (이 "검증" 단계가 제품의 핵심 컨셉입니다.)

## 파일
| 파일 | 설명 |
|---|---|
| `templates/index.html` | 백엔드 연동 프론트엔드 (원본 UI 유지 + `검색`이 실제 호출) |
| `server.py` | Flask 백엔드 + Gemini 호출 (`/`, `/api/search`, `/api/generate`, `/api/health`) |
| `OncoReg_Colab.ipynb` | **Colab 업로드용 노트북** (셀만 실행하면 끝, 아래 A안) |
| `build_notebook.py` | 위 노트북 생성기 (`server.py`+`index.html`을 노트북에 심음) |
| `requirements.txt` | 로컬 실행용 의존성 |

## Gemini API 키 발급
<https://aistudio.google.com/app/apikey> 에서 키 생성(무료 등급 가능).

---

## A안) Google Colab 에서 실행 — 권장 (설치 최소)

1. Colab(<https://colab.research.google.com>) 접속 → **파일 → 노트북 업로드** →
   `OncoReg_Colab.ipynb` 업로드.
2. 위에서부터 셀을 순서대로 실행:
   1. 패키지 설치
   2. `server.py` / `templates/index.html` 파일 기록
   3. **API 키 입력** (입력창에 붙여넣기. 또는 왼쪽 🔑 보안 비밀에 `GEMINI_API_KEY` 저장)
   4. **서버 실행** — 잠시 뒤 `https://....trycloudflare.com` 주소가 출력됨
3. 출력된 **`trycloudflare.com` 주소를 새 탭에서 열기** → HTML 화면 등장.
   `검색` 버튼을 누르면 내 Gemini 로 실제 문헌·임상시험이 생성된다.
4. 상단 우측 배지에 `Gemini · gemini-2.5-flash` 라고 뜨면 엔진 연결 성공.

> `cloudflared` 터널이 막히면, 노트북 맨 아래 **"대안: Colab 내장 프록시"** 셀을
> 대신 실행하면 된다(설치 없이 Colab 링크로 접속).

> 서버 셀은 실행 상태로 계속 둬야 한다(멈추면 서버도 꺼짐). 화면만 미리 보고 싶으면
> HTML의 **"데모 데이터로 미리보기"** 체크박스로 Gemini 호출 없이 원본 예시를 볼 수 있다.

---

## B안) 내 PC(로컬)에서 실행

```bash
cd prototypes/oncoreg-ai
pip install -r requirements.txt

# Gemini 키 설정
export GEMINI_API_KEY="여기에_키"          # Windows(파워셸): $env:GEMINI_API_KEY="키"
# (선택) 모델 변경
export GEMINI_MODEL="gemini-2.5-flash"

python server.py
```
→ 브라우저에서 <http://localhost:8000> 접속. 로컬은 터널이 필요 없다.

---

## 핵심 기능 2가지

### 1) 환자 유사도 가중치 매칭
Gemini가 각 논문의 대상 집단을 **5개 축(질환·임상지표·병기·치료차수·약제)** 으로 환자와
대조해 0~100 점을 매긴다. 백엔드가 기본 가중치를 함께 내려주고, 프론트는
`가중합 ÷ 가중치합` 으로 **유사도 점수**를 계산해 논문을 정렬한다(1등엔 "최고 유사도" 배지).
STEP 2의 슬라이더로 "무엇을 더 중요하게 볼지"를 바꾸면 **Gemini 재호출 없이 즉시 재정렬**된다
(축별 점수는 이미 받아왔으므로 클라이언트 계산만으로 순위가 바뀜).

### 2) 의약품 종류별 서식
STEP 1의 **신청 서식 유형**에 따라 신청서 섹션 구성이 달라진다.
| 서식 | 달라지는 섹션 |
|---|---|
| 효능·효과 초과(일반) | 유효성 근거 + **대체요법 검토** |
| **희귀의약품** | **대체치료 부재 근거** + **국내외 허가·공급 현황** (+추정 환자 수 입력) |
| **추가 용량 의약품** | **용량 설정 근거** + **기존 용량 대비 이익-위해 평가** (+기존/신청 용량 입력, 감량·중단 기준) |

서술 문단도 서식에 맞춰 Gemini가 다르게 생성한다(`/api/generate` 의 `form` 파라미터).
실제 심의 서식을 확보하면 이 섹션 정의만 교체하면 된다.

## 동작 확인 포인트 (시연용)
- **엔진 배지**: 상단에 `Gemini · 모델명` = 실제 연동됨 / `데모 모드` = 백엔드 미연결.
- **STEP 1 → 검색**: `Gemini로 …구조화하는 중` 스피너 후 STEP 2 로 이동.
- **STEP 2**: 문헌 체크 → 지표 카드의 수치 클릭 시 우측에 원문 인용(하이라이트) 표시,
  임상시험 클릭 시 선정/제외 기준 대조. Gemini 결과에는 상단에 "AI 생성" 경고 배너.
- **STEP 3 → 신청서 생성**: 서술 문단을 Gemini 로 생성, 인용 수치마다 출처 결합,
  미검증 항목은 붉게 표시. `인쇄/PDF 저장` 가능.

## 자주 나는 문제
- **키 확인 실패 / 401**: 키 오타·비활성. AI Studio 에서 재발급.
- **429 (rate limit)**: 무료 등급 분당 한도. 잠깐 뒤 재시도하거나 모델을
  `gemini-2.0-flash` 로 변경.
- **검색이 데모 데이터로 뜬다**: 백엔드 연결 실패 시 자동 폴백. 서버 셀이 실행 중인지,
  `trycloudflare` 주소로 접속했는지 확인. (파일을 직접 `file://` 로 열면 백엔드가 없음)
- **결과 구조가 가끔 비어 보임**: 모델이 스키마를 덜 채운 경우. 다시 `검색`을 누르거나
  `server.py` 의 `temperature` 를 낮춘다.

## 노트북을 다시 만들려면
`server.py` 나 `templates/index.html` 을 고친 뒤:
```bash
python build_notebook.py    # OncoReg_Colab.ipynb 재생성
```

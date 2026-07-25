"""
OncoReg AI — Gemini 연동 백엔드 (프로토타입)

역할
  - templates/index.html (프론트엔드)을 그대로 서빙한다.
  - /api/search   : 케이스 조건을 받아 Gemini로 '근거 문헌 + 추출 지표 + 임상시험'을
                    구조화(JSON)해서 돌려준다.  (프론트의 하드코딩 CASES를 대체)
  - /api/generate : 선택된 근거로 신청서의 서술 문단(신청 사유/대체요법)을 생성한다.

주의(의료 안전)
  - 여기서 나오는 문헌/수치/임상시험은 LLM이 생성한 것으로, 실제 출판물과 다를 수
    있다. 반드시 원문 대조·전문가 검증이 필요하다. 데모/프로토타입 용도.

로컬 실행:  GEMINI_API_KEY=... python server.py   ->  http://localhost:8000
Colab 실행: OncoReg_Colab.ipynb 참고 (cloudflared 터널)
"""
import os
import json
from typing import List, Optional

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# 새 Google GenAI SDK (google-genai). 구버전 google-generativeai 아님.
from google import genai
from google.genai import types
from pydantic import BaseModel

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
# 모델을 바꾸고 싶으면 환경변수 GEMINI_MODEL 로 지정 (예: gemini-2.0-flash).


# ----------------------------------------------------------------------------
# 응답 스키마 — 프론트엔드(index.html)가 기대하는 구조와 1:1로 맞춘다.
# ----------------------------------------------------------------------------
class Paper(BaseModel):
    id: int                 # 1,2,3... 인용 번호
    t: str                  # 논문 제목(한국어)
    j: str                  # 학술지/출처명
    y: int                  # 연도
    n: Optional[int] = None # 표본 수 (지침 등은 null)
    fit: str                # 이 케이스와의 부합 사유(짧게)


class Metric(BaseModel):
    k: str                  # 짧은 고유 키 (예: ORR, PFS, HR, AE) — 중복 금지
    label: str              # 지표 한글 이름
    val: str                # 추출된 값 (예: "52.6%")
    src: int                # 근거 논문 id (papers[].id 중 하나)
    loc: str                # 원문 위치 (예: "Results · Table 2")
    pre: str                # 인용문에서 값 앞부분 (영어 원문 스타일)
    mark: str               # 강조될 핵심 문장 (val 이 여기서 도출됨)
    post: str               # 인용문에서 값 뒷부분


class Criterion(BaseModel):
    status: str             # "y"(부합) | "n"(불충족) | "q"(확인 필요)
    text: str               # 선정/제외 기준 문장(한국어)


class Trial(BaseModel):
    id: str                 # 예: "T-01"
    t: str                  # 임상시험명(한국어)
    ph: str                 # 상(예: "2상","3상","관찰연구")
    site: str               # 실시기관(예: "국내 4개 기관")
    pct: int                # 종합 부합률 0~100
    crit: List[Criterion]   # 선정/제외 기준 대조 3~5개


class CaseResult(BaseModel):
    papers: List[Paper]
    metrics: List[Metric]
    trials: List[Trial]


class DocProse(BaseModel):
    reason: str             # 2. 신청 사유 문단
    alternatives: str       # 5. 대체요법 검토 문단


# ----------------------------------------------------------------------------
# 프롬프트
# ----------------------------------------------------------------------------
def build_search_prompt(c: dict) -> str:
    return f"""당신은 종양내과/희귀질환 임상 근거를 정리하는 의학 리서치 보조자다.
아래 '검토 케이스'에 대해, 허가초과(off-label) 사용승인 신청서 작성에 쓸 근거를
구조화해서 만들어라. 출력은 반드시 지정된 JSON 스키마를 따른다.

[검토 케이스]
- 질환 유형: {c.get('typeLabel')}
- 병기/상태: {c.get('stage')}
- 이전 치료 차수: {c.get('line')}
- 주요 임상 지표: {c.get('bio')}
- 검토 약제: {c.get('drug')}

[작성 규칙]
1) papers: 이 케이스에 부합하는 근거 문헌 3~5개.
   - t(제목)·j(출처)·fit(부합 사유)은 한국어. 그중 1개는 진료지침(j="진료지침", n=null).
   - id 는 1부터 연속. y 는 최근 연도 위주.
2) metrics: 위 papers 에서 도출되는 핵심 지표 3~5개. 반드시 안전성 지표 1개 포함(k="AE").
   - k 는 짧은 영문 대문자 키(ORR/PFS/HR/AE 등), 서로 중복되지 않게.
   - src 는 반드시 위 papers 의 id 중 하나.
   - pre/mark/post 는 해당 논문에 나올 법한 '영어 원문' 인용 문장으로, mark 안에
     val 값이 그대로 들어가야 한다(예: val="52.6%" 이면 mark에 "52.6%"가 포함).
   - loc 는 한국어 위치 표기(예: "Results · Table 2").
3) trials: 이 케이스가 참여를 검토할 만한 공개 임상시험 2~3개.
   - id 는 "T-01" 형식. crit 은 선정/제외 기준 3~5개, status 는 y/n/q.
   - pct 는 종합 부합률(40~95 사이 정수).

[중요] 이 결과는 전문가 검증 전 초안이다. 과장 없이 임상적으로 그럴듯하게 작성하되,
실제 인용 시에는 원문 대조가 필요함을 전제로 한다."""


def build_generate_prompt(c: dict, metrics: List[dict], trials: List[dict]) -> str:
    ev = "\n".join(f"- {m.get('label')}: {m.get('val')} (출처 [{m.get('src')}])" for m in metrics)
    tr = "\n".join(f"- {t.get('id')} {t.get('t')} (부합률 {t.get('pct')}%)" for t in trials) or "- 없음"
    return f"""아래 근거를 바탕으로 '허가초과 사용승인 신청서'의 두 서술 문단을 한국어로 작성하라.
과장·단정 없이 사실 근거에 기반해 담백하게 쓴다. 각 문단 3~5문장.

[약제] {c.get('drug')}
[질환] {c.get('typeLabel')} · {c.get('stage')} · {c.get('line')}
[유효성/안전성 근거]
{ev}
[검토된 임상시험]
{tr}

- reason: '신청 사유'. 표준치료 소진 상황과 위 근거에 근거해 왜 이 약제를 신청하는지.
- alternatives: '대체요법 검토'. 현행 급여 대체요법 대비 본 요법의 상대적 임상 이익을 서술."""


# ----------------------------------------------------------------------------
# Gemini 호출
# ----------------------------------------------------------------------------
def get_client() -> genai.Client:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
    return genai.Client(api_key=key)


def call_gemini(prompt: str, schema) -> dict:
    client = get_client()
    resp = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.5,
        ),
    )
    parsed = getattr(resp, "parsed", None)
    if parsed is not None:
        return parsed.model_dump()
    # 일부 버전은 parsed 미제공 -> 텍스트 파싱
    return json.loads(resp.text)


def sanitize_result(d: dict) -> dict:
    """프론트가 깨지지 않도록 최소한의 정합성 보정."""
    papers = d.get("papers") or []
    metrics = d.get("metrics") or []
    trials = d.get("trials") or []

    valid_ids = {p.get("id") for p in papers}
    # src 가 없는 지표 제거, 키 중복 제거
    seen_k = set()
    clean_metrics = []
    for m in metrics:
        if m.get("src") not in valid_ids:
            continue
        k = m.get("k") or f"M{len(clean_metrics)}"
        if k in seen_k:
            k = f"{k}_{len(clean_metrics)}"
        m["k"] = k
        seen_k.add(k)
        clean_metrics.append(m)

    for t in trials:
        pct = t.get("pct", 0)
        try:
            t["pct"] = max(0, min(100, int(pct)))
        except Exception:
            t["pct"] = 0
        for c in t.get("crit", []):
            if c.get("status") not in ("y", "n", "q"):
                c["status"] = "q"

    return {"papers": papers, "metrics": clean_metrics, "trials": trials}


# ----------------------------------------------------------------------------
# Flask 앱
# ----------------------------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    CORS(app)  # 프론트를 별도 파일로 열 때를 대비한 보험(같은 오리진이면 불필요)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({
            "ok": True,
            "model": DEFAULT_MODEL,
            "key_present": bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")),
        })

    @app.post("/api/search")
    def search():
        c = request.get_json(force=True) or {}
        try:
            raw = call_gemini(build_search_prompt(c), CaseResult)
            return jsonify(sanitize_result(raw))
        except Exception as e:
            # 프론트는 실패 시 데모 데이터로 폴백하므로 502 로 알린다.
            return jsonify({"error": str(e)}), 502

    @app.post("/api/generate")
    def generate():
        body = request.get_json(force=True) or {}
        c = body.get("case", {})
        metrics = body.get("metrics", [])
        trials = body.get("trials", [])
        try:
            prose = call_gemini(build_generate_prompt(c, metrics, trials), DocProse)
            return jsonify(prose)
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    return app


if __name__ == "__main__":
    # 로컬 실행용. Colab 에서는 노트북 마지막 셀(cloudflared)로 띄운다.
    port = int(os.environ.get("PORT", "8000"))
    print(f"[OncoReg AI] http://localhost:{port}  (model={DEFAULT_MODEL})")
    create_app().run(host="0.0.0.0", port=port, debug=False)

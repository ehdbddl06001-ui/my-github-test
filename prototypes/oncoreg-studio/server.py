"""
OncoReg Studio — 자유서술 검색 + 근거수준 가중 랭킹 + 문서 스튜디오 (OpenAI 연동)

바뀐 점(이전 oncoreg-ai 대비)
  - 드롭다운 대신 '자유 서술(챗)' 입력을 LLM이 해석해 조건을 추출한다.
  - 근거수준(피라미드)을 '필터'가 아니라 '가중치'로 써서, 유사도와 함께 블렌딩해
    가장 알맞은 논문을 맨 위로 올린다.
  - 약제/질환 기준 모드: 지정(긴급승인·희귀의약품)·대상 환자군·가이드라인·근거 논문을 모은다.
  - 문서 스튜디오: 논문의 '특정 수치·문장'을 골라 서식 각 칸에 삽입한다.

엔드포인트
  - /            : templates/index.html
  - /api/health  : 상태
  - /api/search  : {text} 자유서술 → {query, papers[근거수준·유사도·삽입가능항목], weights}
  - /api/drug    : {name, kind} 약제/질환 → 지정·대상·가이드라인·근거 논문
  - /api/fill    : (선택) 특정 서식 칸 문장 다듬기

주의: 문헌·수치·지정·가이드라인은 LLM 생성 초안으로 실제와 다를 수 있다(반드시 원문 검증).

로컬:  OPENAI_API_KEY=... python server.py   ->  http://localhost:8000
Colab: OncoReg_Studio_Colab.ipynb (cloudflared)
"""
import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# 근거수준 가중치 포함(합=1). 프론트 슬라이더로 조정.
DEFAULT_WEIGHTS = {"disease": 0.24, "biomarker": 0.20, "stage": 0.12,
                   "line": 0.12, "drug": 0.17, "evidence": 0.15}

EVIDENCE_LEVELS = [
    "체계적 문헌고찰/메타분석",   # rank 1 (최상)
    "무작위 대조연구(RCT)",       # 2
    "코호트 연구",                # 3
    "환자-대조군 연구",           # 4
    "사례군/사례보고",            # 5 (최하)
]


def get_client() -> OpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    return OpenAI(api_key=key)


def chat_json(system: str, user: str, temperature=0.4) -> dict:
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    return json.loads(r.choices[0].message.content)


# ----------------------------------------------------------------------------
# 프롬프트
# ----------------------------------------------------------------------------
SEARCH_SYS = """당신은 종양내과/희귀질환 임상 근거를 정리하는 의학 리서치 보조자다.
사용자가 '자유 서술'로 적은 환자 상황을 해석해, 허가초과(off-label) 사용승인 서류에 쓸
근거 문헌을 구조화한다. 반드시 아래 JSON 스키마 '하나의 객체'로만 답한다. 한국어로.

{
 "query": {
   "condition": "핵심 질환명",
   "drug": "검토 약제(있으면)",
   "biomarker": "바이오마커/유전체/검사 지표",
   "stage": "병기/중증도",
   "line": "이전 치료 차수/치료력",
   "excess_type": "eff|dose|age",   // 효능효과 초과 / 용법용량 초과 / 연령대상군 초과
   "rare": true/false,               // 희귀질환 여부
   "summary_ko": "사용자 입력을 1~2문장으로 요약(확인용)"
 },
 "papers": [
   {
     "id": 1,
     "title": "논문 제목(한국어)",
     "journal": "출처(학술지/진료지침)",
     "year": 2023,
     "n": 정수 또는 null,
     "evidence_level": "체계적 문헌고찰/메타분석|무작위 대조연구(RCT)|코호트 연구|환자-대조군 연구|사례군/사례보고",
     "evidence_rank": 1,             // 1(최상)~5(최하)
     "fit": "이 케이스와의 부합 사유(짧게)",
     "sim": {"disease":0-100,"biomarker":0-100,"stage":0-100,"line":0-100,"drug":0-100},
     "items": [                       // 서식에 '삽입 가능한' 근거 조각들
       {"key":"ORR","label":"객관적 반응률","value":"52.6%",
        "pre":"영어 원문 앞부분 ","mark":"the ORR was 52.6%","post":" ...",
        "loc":"Results · Table 2"}
     ]
   }
 ]
}

규칙:
- papers 4~6개. 근거수준을 '섞어서'(메타분석~사례보고) 제시한다. 희귀질환이면 사례군/사례보고도 포함.
- 각 논문마다 items 최소 1개(수치가 없으면 권고등급/핵심 결론을 value로, 예 "Category 1").
- 안전성 관련 item 최소 1개 포함(key 를 "AE"로 시작).
- mark 안에 value 문자열이 그대로 포함되게. sim 은 이 논문 집단이 환자와 얼마나 비슷한지 냉정하게.
- 이 결과는 검증 전 초안이다. 과장 없이."""


DRUG_SYS = """당신은 의약품 규제·급여 정보를 정리하는 의학 보조자다. 사용자가 준 약제 또는
질환에 대해, 허가초과/희귀의약품/긴급(신속)승인 관점의 정보를 구조화한다.
반드시 아래 JSON '하나의 객체'로만 답한다. 한국어. 확실치 않으면 confidence 를 낮추고 note 로 밝힌다.

{
 "drug": "약제명(입력이 질환이면 대표 약제 후보)",
 "disease": "관련 질환",
 "designation": {
   "orphan": "희귀의약품 지정 여부/대상(모르면 '확인 필요')",
   "emergency": "긴급(신속)승인/특례 관련 사항(모르면 '해당/확인 필요')",
   "note": "주의·한계"
 },
 "populations": ["이 약이 고려되는 대표 환자군 2~4개(간결히)"],
 "guidelines": [
   {"name":"가이드라인/진료지침명","org":"발행기관","year":2024,"recommendation":"핵심 권고 한 줄"}
 ],
 "papers": [ (search 와 동일한 paper 객체 형식, 2~4개, 근거수준 표시) ],
 "confidence": "high|medium|low"
}

규칙: 실제 규제 사실과 다를 수 있으므로 단정하지 말고 '확인 필요'를 적극 사용. papers 는 근거수준을 섞어서."""


# ----------------------------------------------------------------------------
def sanitize_papers(papers):
    out = []
    for i, p in enumerate(papers or []):
        p["id"] = p.get("id", i + 1)
        sim = p.get("sim") or {}
        p["sim"] = {a: _clamp(sim.get(a, 55)) for a in ("disease", "biomarker", "stage", "line", "drug")}
        try:
            p["evidence_rank"] = max(1, min(5, int(p.get("evidence_rank", 3))))
        except Exception:
            p["evidence_rank"] = 3
        if p.get("evidence_level") not in EVIDENCE_LEVELS:
            p["evidence_level"] = EVIDENCE_LEVELS[p["evidence_rank"] - 1]
        items = []
        for j, it in enumerate(p.get("items") or []):
            it["key"] = it.get("key") or f"IT{i}_{j}"
            items.append(it)
        p["items"] = items
        out.append(p)
    return out


def _clamp(v, lo=0, hi=100):
    try:
        return max(lo, min(hi, int(v)))
    except Exception:
        return lo


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True, "model": MODEL,
                        "key_present": bool(os.environ.get("OPENAI_API_KEY"))})

    @app.post("/api/search")
    def search():
        text = (request.get_json(force=True) or {}).get("text", "").strip()
        if not text:
            return jsonify({"error": "환자 상황을 입력하세요."}), 400
        try:
            d = chat_json(SEARCH_SYS, f"[사용자 자유 서술]\n{text}")
            d["papers"] = sanitize_papers(d.get("papers"))
            d["weights"] = DEFAULT_WEIGHTS
            return jsonify(d)
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    @app.post("/api/drug")
    def drug():
        body = request.get_json(force=True) or {}
        name = (body.get("name") or "").strip()
        kind = body.get("kind", "drug")
        if not name:
            return jsonify({"error": "약제 또는 질환명을 입력하세요."}), 400
        try:
            d = chat_json(DRUG_SYS, f"[{'약제' if kind=='drug' else '질환'}] {name}")
            d["papers"] = sanitize_papers(d.get("papers"))
            d["weights"] = DEFAULT_WEIGHTS
            return jsonify(d)
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    @app.post("/api/fill")
    def fill():
        # 선택한 근거 조각들을 서식 칸 문장으로 자연스럽게 다듬는다(선택 기능).
        body = request.get_json(force=True) or {}
        field = body.get("field", "")
        snippets = body.get("snippets", [])
        try:
            sys = ("당신은 허가초과 사용승인 신청서 작성을 돕는다. 주어진 근거 조각들을 해당 "
                   "서식 칸에 들어갈 한국어 문장으로 담백하게 다듬어라. JSON {\"text\":\"...\"} 로만 답한다.")
            usr = f"[칸] {field}\n[근거 조각]\n" + "\n".join(f"- {s}" for s in snippets)
            return jsonify(chat_json(sys, usr))
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"[OncoReg Studio] http://localhost:{port}  (model={MODEL})")
    create_app().run(host="0.0.0.0", port=port, debug=False)

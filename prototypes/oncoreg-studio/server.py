"""
OncoReg Studio — 자유서술/PICO 검색 + 상세 유사도 가중 랭킹 + 문서 스튜디오
공급자 자동감지: GEMINI_API_KEY 있으면 Gemini, 없고 OPENAI_API_KEY 있으면 OpenAI.

엔드포인트
  - /            : templates/index.html
  - /api/health  : 상태(provider/model/key)
  - /api/search  : {text} 또는 {pico:{p,i,c,o}} → {query(PICO 포함), papers, weights}
  - /api/drug    : {name, kind} → 지정(긴급승인·희귀의약품)·대상·가이드라인·근거 논문

주의: 문헌·수치·지정·가이드라인은 LLM 생성 초안으로 실제와 다를 수 있다(반드시 원문/공고 검증).
로컬:  GEMINI_API_KEY=... python server.py   ->  http://localhost:8000
"""
import os
import json
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# 유사도 가중치 축(사용자 지정) + 근거수준. 합=1.
DEFAULT_WEIGHTS = {"genetic": 0.22, "symptom": 0.15, "age": 0.10,
                   "comorbidity": 0.14, "pathology": 0.17, "priormed": 0.14, "evidence": 0.08}
SIM_AXES = ["genetic", "symptom", "age", "comorbidity", "pathology", "priormed"]

EVIDENCE_LEVELS = ["체계적 문헌고찰/메타분석", "무작위 대조연구(RCT)", "코호트 연구",
                   "환자-대조군 연구", "사례군/사례보고"]


# ---------------------------------------------------------------- LLM 공급자
def _provider() -> str:
    p = os.environ.get("LLM_PROVIDER", "").lower()
    if p in ("gemini", "openai"):
        return p
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return "gemini"


def _model() -> str:
    return (os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
            if _provider() == "gemini" else os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))


def _key_present() -> bool:
    return (bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
            if _provider() == "gemini" else bool(os.environ.get("OPENAI_API_KEY")))


def chat_json(system: str, user: str, temperature=0.6) -> dict:
    if _provider() == "gemini":
        from google import genai
        from google.genai import types
        key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        client = genai.Client(api_key=key)
        kwargs = dict(response_mime_type="application/json", temperature=temperature)
        # 속도 조절: 2.5 flash 계열은 기본 'thinking'이 켜져 느리다.
        #   GEMINI_THINKING=0(기본, 빠름) / 양수=사고 예산 늘려 품질↑(느려짐).
        try:
            if "flash" in _model().lower():
                tb = int(os.environ.get("GEMINI_THINKING", "0"))
                kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=tb)
        except Exception:
            pass
        resp = client.models.generate_content(
            model=_model(), contents=system + "\n\n" + user,
            config=types.GenerateContentConfig(**kwargs))
        try:
            txt = resp.text
        except Exception:
            txt = None
        if not txt:
            reason = ""
            try:
                reason = str(resp.candidates[0].finish_reason)
            except Exception:
                try:
                    reason = str(resp.prompt_feedback)
                except Exception:
                    pass
            raise RuntimeError(f"모델 응답이 비었습니다(안전 필터 차단 가능: {reason}). "
                               f"모델={_model()}. 다른 표현으로 재시도하거나 GEMINI_THINKING 조정.")
        return _loads(txt)
    from openai import OpenAI
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    client = OpenAI(api_key=key)
    r = client.chat.completions.create(
        model=_model(),
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        response_format={"type": "json_object"}, temperature=temperature)
    return _loads(r.choices[0].message.content)


def _loads(txt: str) -> dict:
    """모델 출력에서 JSON 객체만 뽑아 파싱(코드펜스/잡텍스트 방어)."""
    if not txt:
        raise RuntimeError("모델 응답이 비어 있습니다.")
    s, e = txt.find("{"), txt.rfind("}")
    return json.loads(txt[s:e + 1] if (s != -1 and e != -1) else txt)


# ---------------------------------------------------------------- 프롬프트
SEARCH_SYS = """당신은 근거중심의학 리서치 보조자다. 사용자의 환자 상황(자유서술 또는 PICO)을
해석해, 허가초과 사용승인 서류에 쓸 근거 문헌을 '풍부하게' 구조화한다. 반드시 아래 JSON
'하나의 객체'로만 답한다. 한국어.

{
 "query": {
   "P":"대상 환자·질환(짧게)", "I":"중재(약물/시술)", "C":"비교 대상", "O":"평가 결과지표",
   "condition":"핵심 질환명", "drug":"검토 약제", "biomarker":"유전체/바이오마커",
   "stage":"병기/중증도", "line":"이전 치료력", "excess_type":"eff|dose|age", "rare":true/false,
   "special": true/false,          // 특이/복잡 케이스면 true, 전형적이면 false
   "summary_ko":"1~2문장 요약"
 },
 "papers": [                        // 6~8편. 근거수준을 섞고, 유사도가 서로 다르게.
   {
     "id":1, "title":"제목(한국어)", "journal":"출처", "year":2023, "n":정수 또는 null,
     "doi":"있으면 DOI, 없으면 \\"\\"",
     "evidence_level":"체계적 문헌고찰/메타분석|무작위 대조연구(RCT)|코호트 연구|환자-대조군 연구|사례군/사례보고",
     "evidence_rank":1,             // 1(최상)~5(최하)
     "sim":{"genetic":0-100,"symptom":0-100,"age":0-100,"comorbidity":0-100,"pathology":0-100,"priormed":0-100},
     "sim_detail":{                 // 각 축이 '왜 그 점수인지' 한 구절씩(구체적으로)
       "genetic":"예: 동일 HER2 IHC 1+ 집단, KRAS 상태 유사",
       "symptom":"","age":"예: 중앙연령 58세로 유사","comorbidity":"","pathology":"","priormed":"예: 이전 항암 2차 경험 일치"
     },
     "relevance":0-100,             // 이 케이스의 '문서작성 유용성'을 스스로 종합 판단한 점수.
                                    //   진료지침/직접 해당하는 RCT=높게(85~100), 부수적=낮게. 정렬 기준.
     "why":"이 논문이 본 환자와 얼마나/왜 유사·적합한지 2~3문장(무엇이 같고 무엇이 다른지 구체적으로)",
     "items":[                       // 서식 각 칸에 넣을 '근거 조각'. 반드시 원문 한 문장·위치·대상 칸 포함.
       {"key":"ORR","label":"객관적 반응률","value":"52.6%",
        "pre":"영어 원문 앞부분 ","mark":"the ORR was 52.6%","post":" ...(원문 문장 끝).",
        "loc":"Results · Table 2",
        "field":"evidence"          // 이 항목이 들어갈 서식 칸(아래 목록 중 하나)
       }
     ]
   }
 ]
}

[items.field 배정 규칙] 각 근거 항목을 '알맞은 서식 칸' 하나로 분류한다:
- "evidence"  : 유효성·안전성 수치(반응률·생존·위험비·이상반응 발생률 등) → 의학적 근거자료
- "merits"    : 약제의 특장점·기전·표준 대비 우월성·권고 위상 → 신청약제의 특·장점
- "target"    : 대상 환자·선정 기준·바이오마커 정의 → 대상 환자 기준
- "dosage"    : 용법·용량·투여 스케줄 → 용법·용량
- "duration"  : 투여기간·투여중단 시점 → 투여기간
- "other"     : 재투여·모니터링 기준 → 기타(투여방법)
- "reason2"   : 대체약제 부재/우월성 등 고시 제2조 사유 → 고시 제2조 해당 사유
- "opinion"   : 그 외 참고 의견 → 기타 의견
  잘 모르면 "evidence".

규칙:
- **relevance 는 사용자 케이스에 대한 '문서작성 유용성'을 스스로 판단해 매긴다**. 진료지침·직접
  해당하는 RCT는 85~100, 부분적으로만 겹치면 낮게. (사용자에게 가중치를 묻지 않는다 — 모델이 판단)
- papers 6~8편, 근거수준 다양(메타분석~사례보고). 같은 질환이라도 매번 조금씩 다른 논문을
  제시해도 좋다(temperature 반영). 희귀질환이면 사례군/사례보고도 포함.
- 각 논문 items 2~5개로 '여러 칸'을 채우도록 field 를 다양하게(유효성·특장점·대상·용법 등).
  안전성 item 1개 이상(key 를 "AE"로, field 는 "evidence").
- pre/mark/post 는 실제 논문에 나올 법한 '영어 원문 한 문장'으로, mark 안에 value 가 그대로 포함.
- sim 6축을 냉정하게 매기고, sim_detail 로 근거를 남긴다. 과장 금지, 검증 전 초안."""

DRUG_SYS = """당신은 의약품 규제·급여 정보를 정리하는 의학 보조자다. 준 약제(또는 질환)에 대해
허가초과/희귀의약품/긴급(신속)승인 관점 정보를 구조화한다. 아래 JSON '하나의 객체'로만. 한국어.
확실치 않으면 '확인 필요'라고 쓰고 confidence 를 낮춘다.

{
 "drug":"약제명", "disease":"관련 질환",
 "designation":{"orphan":"희귀의약품 지정 여부/대상","emergency":"긴급·신속승인/특례","note":"주의"},
 "populations":["대표 환자군 2~4개"],
 "guidelines":[{"name":"","org":"","year":2024,"recommendation":""}],
 "papers":[ (search 와 동일한 paper 객체, 3~5편) ],
 "confidence":"high|medium|low"
}
규칙: 규제 사실은 단정 말고 '확인 필요' 적극 사용. papers 는 sim 6축·sim_detail·why·items 포함."""


# ---------------------------------------------------------------- 정합성 보정
def sanitize_papers(papers):
    out = []
    for i, p in enumerate(papers or []):
        p["id"] = p.get("id", i + 1)
        sim = p.get("sim") or {}
        p["sim"] = {a: _clamp(sim.get(a, 55)) for a in SIM_AXES}
        p["sim_detail"] = p.get("sim_detail") or {}
        try:
            p["evidence_rank"] = max(1, min(5, int(p.get("evidence_rank", 3))))
        except Exception:
            p["evidence_rank"] = 3
        if p.get("evidence_level") not in EVIDENCE_LEVELS:
            p["evidence_level"] = EVIDENCE_LEVELS[p["evidence_rank"] - 1]
        # relevance(모델 종합 판단)이 없으면 유사도 평균으로 보정
        if p.get("relevance") is None:
            vals = list(p["sim"].values())
            p["relevance"] = round(sum(vals) / len(vals)) if vals else 60
        p["relevance"] = _clamp(p["relevance"])
        items = []
        valid_fields = {"evidence", "merits", "target", "dosage", "duration", "other", "reason2", "opinion"}
        for j, it in enumerate(p.get("items") or []):
            it["key"] = it.get("key") or f"IT{i}_{j}"
            if it.get("field") not in valid_fields:
                it["field"] = "evidence"
            items.append(it)
        p["items"] = items
        out.append(p)
    return out


def _clamp(v, lo=0, hi=100):
    try:
        return max(lo, min(hi, int(v)))
    except Exception:
        return lo


# ---------------------------------------------------------------- Flask
def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True, "provider": _provider(), "model": _model(),
                        "key_present": _key_present()})

    @app.post("/api/search")
    def search():
        body = request.get_json(force=True) or {}
        pico = body.get("pico")
        text = (body.get("text") or "").strip()
        if pico:
            user = ("[PICO 입력]\n"
                    f"P(대상): {pico.get('p','')}\nI(중재): {pico.get('i','')}\n"
                    f"C(비교): {pico.get('c','')}\nO(결과): {pico.get('o','')}")
        elif text:
            user = f"[자유 서술]\n{text}"
        else:
            return jsonify({"error": "환자 상황(자유서술 또는 PICO)을 입력하세요."}), 400
        try:
            d = chat_json(SEARCH_SYS, user)
            d["papers"] = sanitize_papers(d.get("papers"))
            d["weights"] = DEFAULT_WEIGHTS
            return jsonify(d)
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"{type(e).__name__}: {e}"}), 502

    @app.post("/api/drug")
    def drug():
        body = request.get_json(force=True) or {}
        name = (body.get("name") or "").strip()
        if not name:
            return jsonify({"error": "약제/질환명을 입력하세요."}), 400
        try:
            d = chat_json(DRUG_SYS, f"[{'약제' if body.get('kind','drug')=='drug' else '질환'}] {name}")
            d["papers"] = sanitize_papers(d.get("papers"))
            d["weights"] = DEFAULT_WEIGHTS
            return jsonify(d)
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"{type(e).__name__}: {e}"}), 502

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"[OncoReg Studio] http://localhost:{port}  (provider={_provider()}, model={_model()})")
    create_app().run(host="0.0.0.0", port=port, debug=False)

"""
MediReg AI — 자유서술/PICO 검색 + 상세 유사도 가중 랭킹 + 문서 스튜디오
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

# 유사도 축(정렬은 relevance가 담당, 이 축들은 '왜 비슷한지' 설명용). 축은 유연히 늘려도 됨.
DEFAULT_WEIGHTS = {"symptom": 0.20, "age": 0.12, "comorbidity": 0.20,
                   "pathology": 0.24, "priormed": 0.24}
SIM_AXES = ["symptom", "age", "comorbidity", "pathology", "priormed"]

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
 "references": [                    // 핵심 지표의 한국·미국·유럽 '기준치/정상범위'(가이드라인 근거)
   {"metric":"예: HbA1c","unit":"%","kr":"한국 기준","us":"미국 기준","eu":"유럽 기준"}
 ],
 "guideline_links": {              // 한/미/유럽 대표 가이드라인 접속 링크
   "kr":{"name":"기관/지침명","url":"실제 접속 가능 URL"},
   "us":{"name":"","url":""}, "eu":{"name":"","url":""}
 },
 "papers": [                        // 6~8편. '연구논문 약 절반 + 증례(case report/series) 약 절반'.
   {                               //   ※ 진료지침(가이드라인)은 papers 에 넣지 않는다(문서작성 단계 담당).
     "id":1, "title":"제목(한국어)", "journal":"출처", "year":2023, "n":정수 또는 null,
     "doi":"있으면 DOI, 없으면 \\"\\"",
     "evidence_level":"체계적 문헌고찰/메타분석|무작위 대조연구(RCT)|코호트 연구|환자-대조군 연구|사례군/사례보고",
     "evidence_rank":1,             // 1(최상)~5(최하)
     "sim":{"symptom":0-100,"age":0-100,"comorbidity":0-100,"pathology":0-100,"priormed":0-100},
     "sim_detail":{"symptom":"","age":"","comorbidity":"","pathology":"","priormed":""},
     "relevance":0-100,             // 문서작성 유용성 종합판단. 정렬 기준.
     "why":"이 논문이 본 환자와 얼마나/왜 유사·적합한지 2~3문장",
     "items":[                       // 서식 각 칸에 넣을 '근거 조각'. 원문 한 문장·위치·대상 칸·한국기준 부합 포함.
       {"key":"ORR","label":"객관적 반응률","value":"52.6%",
        "pre":"영어 원문 앞부분 ","mark":"the ORR was 52.6%","post":" ...(원문 문장 끝).",
        "loc":"Results · Table 2", "field":"evidence",
        "kr_ok": true,              // 이 수치가 '한국 기준치/권고'에 부합하면 true, 어긋나면 false
        "kr_note": "한국 기준 대비 한 줄(부합/불일치 사유)"
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
- **papers 는 진료지침(가이드라인)을 넣지 않는다.** 6~8편 중 **약 절반은 원저 연구(RCT/코호트/
  메타), 나머지 절반은 증례(사례군/사례보고)**. 같은 질환이라도 매번 조금씩 다른 논문을 제시해도 좋다.
- relevance 는 '문서작성 유용성' 종합판단(원저·직접 근거 높게). 가중치는 묻지 않고 모델이 판단.
- 각 item 에 kr_ok(한국 기준 부합 여부)·kr_note 를 반드시 넣는다. **한국 기준을 벗어나는 값은 kr_ok=false.**
- references 는 3~5개 핵심 지표(한/미/유럽 기준치). **약제가 특정되면 '허가 용량'(mg 등 숫자)과
  '표준 투여기간/간격' 지표를 반드시 포함**한다(문서의 용법·용량/투여기간 칸을 사용자가 정상치와
  비교하도록). guideline_links 는 한/미/유럽 각 1개. **URL 은 접속 실패 위험을 줄이려 공식 기관의
  대표(루트) 페이지를 쓰고, 정확한 심층 URL이 불확실하면 지침명 자체를 name 에 정확히 적는다**(앱이
  이름으로 검색 링크를 만든다).
- dosage·duration·target 에 해당하는 item 을 최소 1개씩 포함해 각 칸에 넣을 숫자 근거를 제공한다.
- items 3~6개로 field 다양히(evidence·merits·target·dosage·duration 골고루). 안전성 item 1개 이상(key "AE", field "evidence").
- pre/mark/post 는 영어 원문 한 문장(value 포함), loc 에 '어느 절·표·쪽'인지 최대한 구체적으로. 과장 금지, 검증 전 초안."""

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
규칙: 규제 사실은 단정 말고 '확인 필요' 적극 사용. papers 는 sim·sim_detail·why·items 포함."""

FIELD_SYS = """당신은 허가초과 사용승인 신청서의 '특정 칸' 초안을 돕는다. 주어진 약제와 환자
상태를 바탕으로, 한국·미국·유럽 진료지침 관점에서 그 칸에 들어갈 한국어 초안을 담백하게 쓰고,
사용자가 직접 확인할 수 있도록 한국·미국·유럽 가이드라인 링크를 제시한다. 아래 JSON '하나'로만.

{
 "text":"해당 칸 초안(2~4문장, 과장 없이. 용량·기간은 지침상 범위로. 확인 필요 사항 명시).",
 "guidelines":[
   {"region":"한국","name":"발행기관/지침명","url":"실제 접속 가능한 공식/대표 페이지 URL"},
   {"region":"미국","name":"","url":""},
   {"region":"유럽","name":"","url":""}
 ]
}
규칙: 반드시 한국·미국·유럽 각 1개씩. URL은 실제 접속 가능한 공식·대표 페이지(모르면 해당 기관
대표 도메인). 규제·용량은 '지침 원문 확인 필요'를 전제로 단정하지 않는다."""

VERIFY_SYS = """당신은 허가초과 사용승인 신청서 초안을 '검증'한다. [신청서 칸]과 [사용자가 근거로
선택한 논문/근거조각]을 대조해, 각 칸에서 다음을 찾아 JSON '하나'로만 답한다.
 (a) 문맥 오류: 문장이 어색하거나 앞뒤가 맞지 않거나 칸의 목적과 다른 내용.
 (b) 근거 불일치: 초안의 수치·주장(용량·기간·반응률 등)이 [선택 근거]의 값과 다르거나, 근거에 없는데
     지어낸 값. 반드시 어떤 근거[번호]와 어떻게 다른지 note 에 적는다.
 (c) 한국 기준 위반·누락·과장.
{"ok": true, "issues":[{"field":"evidence|merits|target|dosage|duration|other|reason2|opinion",
  "severity":"high|medium|low","kind":"context|mismatch|kr|missing",
  "note":"문제와 근거[번호] 대조·수정 제안"}]}
문제 없으면 ok=true, issues=[]. 확실치 않으면 severity 는 medium 이하. 수치 불일치(mismatch)는 high."""

TRIALS_SYS = """당신은 '진행 중인 임상시험 연결(expanded access)'을 돕는 검색 보조자다. 표준치료가
소진된 환자 상황을 받아, 참여를 검토할 만한 임상시험을 구조화한다. JSON '하나'로만. 한국어.
{"summary":"해석 요약","trials":[
  {"title":"","phase":"1상|2상|3상|관찰연구","status":"모집중|모집예정|미상","where":"국내 n개 기관 등",
   "nct":"NCT번호(있으면) 또는 \\"\\"","url":"ClinicalTrials.gov 검색/등록 URL",
   "eligibility":["핵심 선정기준 3~5개"],"match":"이 환자와의 부합 한 줄"}]}
규칙: 실제 등록 확인 전 참고용(등록번호·기관은 반드시 확인 필요). url 은 접속 가능한 검색 링크라도 제공."""

COMPOSE_SYS = """당신은 '허가초과 약제 비급여 사용승인 신청서(별지 제1호)'의 초안을 **처음부터 끝까지
자동으로** 작성한다. 준 환자 정보·선택 근거·가이드라인 기준치를 종합해, 각 칸을 담백한 한국어
문장으로 완성한다. 아래 JSON '하나의 객체'로만 답한다.

{
 "fields": {
   "evidence":"의학적 근거자료(핵심 유효성·안전성 수치를 근거[번호]와 함께 2~4문장)",
   "merits":"신청약제의 특·장점(표준 대비 우월성·기전·권고 위상)",
   "target":"대상 환자 기준(질환·병기·바이오마커·이전 치료력)",
   "dosage":"용법·용량(가이드라인 허가 범위 내. 한국 기준 우선)",
   "duration":"투여기간(투여중단 시점 포함)",
   "other":"기타(재투여·모니터링 기준)",
   "reason2":"고시 제2조 해당 사유(대체약제 부재/우월성 등)",
   "opinion":"기타 의견(없으면 간단히)"
 },
 "field_refs": {                  // 각 칸을 '사용자가 수정할 때' 참고할 가이드라인별 정상치/기준치
   "dosage":[{"metric":"허가 용량","unit":"mg/kg","kr":"한국값","us":"미국값","eu":"유럽값"}],
   "target":[{"metric":"판정 기준","unit":"","kr":"","us":"","eu":""}]
   // 값이 있는 칸에만 넣는다. 관련 기준치가 없으면 생략.
 },
 "classification": {              // 서식의 '허가초과 유형/체크' 자동 판정(약사가 확인·수정)
   "drug":"주성분명(영문/한글)",
   "approved_kr":"yes|no|unknown",          // 이 약제가 국내에 허가되어 있는지
   "approved_note":"국내 허가/사용 현황 한 줄(적응증 등)",
   "off_label":true,                        // 이 '요청 사용'이 허가범위 초과인지
   "excess_type":"eff|dose|age",            // 효능효과 초과 / 용법용량 초과 / 연령대상군 초과
   "type2":"none|contra|cost",              // 대체약제 없음 / 대체약제 있으나 투여금기 / 대체약제보다 비용효과적
   "rare":true,                             // 희귀질환 여부
   "combo":false,                           // 병용 여부
   "severity":"생명을 위협하는 질환|사망에 이르는 질환|비가역적인 기능상실을 초래하는 질환|기타(해당없음 등)",
   "note":"약제 정체성·허가초과 유형 판정 근거 1~2문장"
 }
}
규칙:
- classification 은 **약제가 국내에서 쓰이는지, 그리고 이 요청이 허가초과(off-label)인지 아니면
  통상 허가 범위 내인지**를 문맥으로 판정한다. 국내 미허가면 approved_kr="no" 로 하고 note 에
  '국내 미허가—긴급/희귀 경로 검토 필요'처럼 적는다. off_label=false 로 판단되면 note 에 사유를 남긴다.
  excess_type/type2/severity 는 위 별지 제1호서식의 정식 선택지 중 가장 맞는 하나를 고른다(추정이면 note 명시).
- **숫자(용량·투여기간·투여간격·반응률 등)는 반드시 준 [선택 근거]·[가이드라인 기준치]에 있는
  실제 수치를 우선 사용**하고 [번호] 인용을 붙인다. dosage·duration 칸은 **구체적 숫자(예: 5.4
  mg/kg, 3주 간격, 중앙 10.1개월)를 반드시 포함**한다. 근거에 숫자가 없으면 '(용량 확인 필요)'처럼
  표시하되 임의 창작하지 않는다.
- **한국 기준을 벗어나는 값(kr_ok=false)은 절대 초안에 쓰지 않는다.** 그런 지표는 한국 기준치로
  대체하고 '국내 허가 기준(예: 용량 5.4 mg/kg)' 으로 명시한다.
- 과장·창작 금지. 확실치 않으면 '확인 필요'.
- field_refs 는 **관련 있는 모든 칸에 반드시 채운다**(특히 dosage·duration·target). 준 '가이드라인
  기준치'를 각 칸에 맞게 분배(용량→dosage, 투여기간/모니터링→duration/other, 판정·바이오마커→target).
  준 기준치가 부족하면 널리 알려진 한/미/유럽 표준치라도 채워, 사용자가 정상치와 비교해 고칠 수 있게 한다.
- 모든 문장은 제출 전 검증이 필요한 '초안'임을 전제로 간결하게."""


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
            if it.get("kr_ok") is None:
                it["kr_ok"] = True
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

    @app.post("/api/field")
    def field():
        b = request.get_json(force=True) or {}
        label = b.get("fieldLabel") or b.get("field", "")
        drug = b.get("drug", "")
        patient = b.get("patient", "")
        try:
            usr = f"[작성할 칸] {label}\n[약제] {drug}\n[환자 상태] {patient}"
            return jsonify(chat_json(FIELD_SYS, usr, temperature=0.4))
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"{type(e).__name__}: {e}"}), 502

    @app.post("/api/verify")
    def verify():
        b = request.get_json(force=True) or {}
        fields = b.get("fields", {})
        ev = []
        for p in (b.get("papers") or []):
            for it in (p.get("items") or []):
                ev.append(f"- [{p.get('id')}] {it.get('label','')}: {it.get('value','')} "
                          f"(kr_ok={it.get('kr_ok', True)}) {p.get('journal','')} {it.get('loc','')}")
        usr = ("[약제] " + str(b.get("drug", "")) + "\n[환자] " + str(b.get("patient", "")) +
               "\n[사용자가 근거로 선택한 논문/근거조각]\n" + ("\n".join(ev) or "(선택 근거 없음)") +
               "\n\n[신청서 칸]\n" + "\n".join(f"- {k}: {v}" for k, v in fields.items() if v))
        try:
            return jsonify(chat_json(VERIFY_SYS, usr, temperature=0.2))
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"{type(e).__name__}: {e}"}), 502

    @app.post("/api/trials")
    def trials():
        text = (request.get_json(force=True) or {}).get("text", "").strip()
        if not text:
            return jsonify({"error": "환자 상황을 입력하세요."}), 400
        try:
            return jsonify(chat_json(TRIALS_SYS, f"[환자 상황]\n{text}", temperature=0.5))
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"{type(e).__name__}: {e}"}), 502

    @app.post("/api/compose")
    def compose():
        b = request.get_json(force=True) or {}
        query = b.get("query", {})
        papers = b.get("papers", [])
        refs = b.get("references", [])
        lines = []
        for p in papers:
            for it in (p.get("items") or []):
                lines.append(
                    f"- [{p.get('id')}] {it.get('label','')}: {it.get('value','')} "
                    f"(field={it.get('field','evidence')}, kr_ok={it.get('kr_ok', True)}"
                    f"{'; '+it.get('kr_note','') if it.get('kr_note') else ''}) "
                    f"— {p.get('journal','')} {it.get('loc','')}")
        usr = ("[환자/질의]\n" + json.dumps(query, ensure_ascii=False) +
               "\n\n[선택 근거]\n" + ("\n".join(lines) or "(선택 근거 없음 — 환자 정보만으로 초안)") +
               "\n\n[가이드라인 기준치]\n" + json.dumps(refs, ensure_ascii=False))
        try:
            return jsonify(chat_json(COMPOSE_SYS, usr, temperature=0.4))
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"{type(e).__name__}: {e}"}), 502

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"[MediReg AI] http://localhost:{port}  (provider={_provider()}, model={_model()})")
    create_app().run(host="0.0.0.0", port=port, debug=False)

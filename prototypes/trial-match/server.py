"""
TrialMatch — 임상시험 연결 검색 플랫폼 (프로토타입)

시나리오: 표준치료·희귀의약품으로도 치료가 어려운 환자가 '자기 상황'을 자유롭게
검색창에 적으면 → 현재 '모집 중'인 임상시험을 찾아 적합도를 대조하고 연락처로 연결한다.

설계 원칙 (윤리/규제 경계 = "IRB/규제 승인된 부분만")
  - 임상시험 정보는 우리가 지어내지 않는다. **ClinicalTrials.gov 공개 API(v2)** 의
    '실제 등록·모집중 시험'만 가져온다. (중재연구는 IRB 승인 하에 등록됨)
  - Gemini 는 (1) 한글 자유입력을 검색어로 해석하고 (2) 각 시험의 선정/제외 기준과
    환자를 대조해 적합도를 매기는 '보조' 역할만 한다. 판단·연결의 주체가 아니다.
  - 본 도구는 환자를 직접 모집·중개하지 않는다. 표시되는 연락처는 각 시험의 '공식
    등록 연락처'이며, 최종 참여 결정과 적격 판정은 실시기관과 담당 의료진이 한다.

역할
  - /            : templates/index.html 서빙
  - /api/health  : 상태
  - /api/search  : 자유입력 → (Gemini 해석) → CT.gov 조회 → (Gemini 적합도 채점) → 결과

로컬:  GEMINI_API_KEY=... python server.py   ->  http://localhost:8000
Colab: TrialMatch_Colab.ipynb 참고 (cloudflared 터널)
"""
import os
import json
import urllib.parse
import urllib.request
from typing import List, Optional

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from google import genai
from google.genai import types
from pydantic import BaseModel

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
CTGOV_API = "https://clinicaltrials.gov/api/v2/studies"
# '진행 중'으로 볼 상태 (모집중 + 모집예정). 필요시 ACTIVE_NOT_RECRUITING 추가 가능.
OPEN_STATUSES = ["RECRUITING", "NOT_YET_RECRUITING"]
MAX_TRIALS_SCORE = 8   # 적합도 채점에 넘길 최대 시험 수(토큰/속도 관리)


# ----------------------------------------------------------------------------
# 스키마
# ----------------------------------------------------------------------------
class ExtractedQuery(BaseModel):
    condition_en: str        # CT.gov 검색용 '영어' 질환명 (한글 입력을 번역/정규화)
    other_terms: str = ""    # 개입/약물/바이오마커 등 추가 영어 키워드(공백 구분)
    location_en: str = ""    # 지역(국가/도시) 영어, 없으면 ""
    summary_ko: str          # 사용자가 확인할 한글 요약


class Criterion(BaseModel):
    status: str              # y(부합) | n(불충족) | q(확인 필요)
    text: str                # 기준 문장(한국어)


class TrialMatch(BaseModel):
    idx: int                 # 입력 시험 목록에서의 순번(0부터)
    matchPct: int            # 적합도 0~100
    summary: str             # 이 환자 기준 한 줄 한글 요약
    crit: List[Criterion]    # 핵심 선정/제외 기준 대조 3~6개
    note: str                # 점수 근거 짧게(한국어)


# ----------------------------------------------------------------------------
# Gemini
# ----------------------------------------------------------------------------
def get_client() -> genai.Client:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
    return genai.Client(api_key=key)


def gemini_json(prompt: str, schema, temperature=0.3):
    resp = get_client().models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=temperature,
        ),
    )
    parsed = getattr(resp, "parsed", None)
    if parsed is not None:
        if isinstance(parsed, list):
            return [p.model_dump() for p in parsed]
        return parsed.model_dump()
    return json.loads(resp.text)


def extract_query(text: str) -> dict:
    prompt = f"""환자/보호자가 자유롭게 적은 아래 문장에서, 임상시험 데이터베이스
(ClinicalTrials.gov, 영어) 검색에 쓸 핵심어를 뽑아라. 반드시 JSON 스키마를 따른다.

[입력]
{text}

[규칙]
- condition_en: 핵심 '질환명'을 영어로. (예: 한글 "전신성 경화증 폐동맥고혈압" ->
  "systemic sclerosis pulmonary arterial hypertension"). 가장 특이적인 진단명 위주.
- other_terms: 약물/바이오마커/이전치료/변이 등 추가 영어 키워드를 공백으로. 없으면 "".
- location_en: 지역이 드러나면 영어 국가/도시(예: "Korea","Seoul"), 없으면 "".
- summary_ko: 입력을 1~2문장 한글로 요약(사용자 확인용)."""
    try:
        return gemini_json(prompt, ExtractedQuery)
    except Exception:
        # Gemini 실패 시: 입력을 그대로 검색어로(영문 입력이면 그대로 먹힘)
        return {"condition_en": text[:120], "other_terms": "", "location_en": "",
                "summary_ko": text[:200]}


def score_trials(text: str, trials: List[dict]) -> List[dict]:
    slim = []
    for i, t in enumerate(trials):
        slim.append({
            "idx": i,
            "title": t.get("title"),
            "conditions": t.get("conditions"),
            "phases": t.get("phases"),
            "sex": t.get("sex"), "minAge": t.get("minAge"), "maxAge": t.get("maxAge"),
            "eligibility": (t.get("eligibilityText") or "")[:1200],
        })
    prompt = f"""아래는 한 환자의 상황과, 현재 모집 중인 실제 임상시험 목록이다.
각 시험의 선정/제외 기준(eligibility)을 환자와 대조해 적합도를 매겨라.
반드시 각 시험(idx)마다 하나씩, JSON 배열로 답한다.

[환자 상황]
{text}

[임상시험 목록(JSON)]
{json.dumps(slim, ensure_ascii=False)}

[규칙]
- idx: 위 목록의 순번 그대로.
- matchPct: 환자 조건이 이 시험 선정기준에 얼마나 부합하는지 0~100 정수.
- crit: 이 시험의 '핵심' 선정/제외 기준 3~6개를 골라 한국어로 요약하고, 환자 기준
  status 를 y(부합)/n(불충족)/q(정보부족·확인필요)로 표기.
- summary: 이 환자에게 이 시험이 왜 후보인지 한 줄 한국어.
- note: 점수 근거를 한 문장 한국어로.
- 정보가 부족하면 단정하지 말고 q 로. 과장 금지."""
    try:
        return gemini_json(prompt, list[TrialMatch])
    except Exception:
        return []


# ----------------------------------------------------------------------------
# ClinicalTrials.gov (실데이터)
# ----------------------------------------------------------------------------
def fetch_ctgov(q: dict, page_size=15) -> List[dict]:
    params = {
        "query.cond": q.get("condition_en", "") or "",
        "filter.overallStatus": ",".join(OPEN_STATUSES),
        "pageSize": str(page_size),
        "format": "json",
    }
    if q.get("other_terms"):
        params["query.term"] = q["other_terms"]
    if q.get("location_en"):
        params["query.locn"] = q["location_en"]

    def _req(p):
        url = CTGOV_API + "?" + urllib.parse.urlencode(p)
        req = urllib.request.Request(url, headers={"User-Agent": "TrialMatch-Prototype/1.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8"))

    try:
        data = _req(params)
    except Exception:
        # 상태 필터가 문제일 수 있으니 한 번 더 시도(필터 제거)
        p2 = {k: v for k, v in params.items() if k != "filter.overallStatus"}
        try:
            data = _req(p2)
        except Exception:
            return []

    out = []
    for study in data.get("studies", []):
        ps = study.get("protocolSection", {})
        idm = ps.get("identificationModule", {})
        stm = ps.get("statusModule", {})
        status = stm.get("overallStatus", "")
        if status and status not in OPEN_STATUSES:
            continue  # 혹시 필터 없이 온 경우 후처리
        elig = ps.get("eligibilityModule", {})
        cl = ps.get("contactsLocationsModule", {})
        locs = []
        for l in (cl.get("locations", []) or [])[:6]:
            locs.append({
                "facility": l.get("facility"), "city": l.get("city"),
                "country": l.get("country"), "status": l.get("status"),
            })
        contacts = []
        for cc in (cl.get("centralContacts", []) or [])[:3]:
            contacts.append({"name": cc.get("name"), "phone": cc.get("phone"),
                             "email": cc.get("email")})
        nct = idm.get("nctId", "")
        out.append({
            "nctId": nct,
            "title": idm.get("briefTitle") or idm.get("officialTitle") or nct,
            "status": status,
            "phases": ps.get("designModule", {}).get("phases", []) or [],
            "conditions": ps.get("conditionsModule", {}).get("conditions", []) or [],
            "interventions": [i.get("name") for i in
                              ps.get("armsInterventionsModule", {}).get("interventions", []) or []
                              if i.get("name")],
            "eligibilityText": elig.get("eligibilityCriteria", "") or "",
            "sex": elig.get("sex"), "minAge": elig.get("minimumAge"),
            "maxAge": elig.get("maximumAge"),
            "locations": locs, "contacts": contacts,
            "url": f"https://clinicaltrials.gov/study/{nct}" if nct else "",
        })
    return out


# 실 API 가 막힌 환경을 위한 '표본' 데이터 (명확히 데모 표시). 구조는 실데이터와 동일.
SAMPLE_TRIALS = [
    {"nctId": "NCT00000000",
     "title": "[표본] 결합조직질환 관련 폐동맥고혈압 대상 신규 경구제 3상",
     "status": "RECRUITING", "phases": ["PHASE3"],
     "conditions": ["Pulmonary Arterial Hypertension", "Systemic Sclerosis"],
     "interventions": ["Investigational oral agent"],
     "eligibilityText": "Inclusion: adults with CTD-associated PAH, WHO FC II-III, 6MWD 150-450m, "
                        "on stable background therapy >=3 months. Exclusion: PVOD, severe hepatic impairment.",
     "sex": "ALL", "minAge": "19 Years", "maxAge": "80 Years",
     "locations": [{"facility": "[표본] 서울 소재 대학병원", "city": "Seoul", "country": "Korea, Republic of", "status": "RECRUITING"}],
     "contacts": [{"name": "[표본] 임상시험 코디네이터", "phone": "02-000-0000", "email": "trial@example.org"}],
     "url": "https://clinicaltrials.gov/"},
    {"nctId": "NCT00000001",
     "title": "[표본] 희귀 고형암 환자 대상 표적치료제 바스켓 2상",
     "status": "RECRUITING", "phases": ["PHASE2"],
     "conditions": ["Rare Solid Tumor"],
     "interventions": ["Targeted agent (biomarker-selected)"],
     "eligibilityText": "Inclusion: advanced rare solid tumor with actionable alteration, progressed on standard therapy, "
                        "ECOG 0-1. Exclusion: untreated CNS metastases.",
     "sex": "ALL", "minAge": "18 Years", "maxAge": "N/A",
     "locations": [{"facility": "[표본] 국내 다기관", "city": "Seoul", "country": "Korea, Republic of", "status": "RECRUITING"}],
     "contacts": [{"name": "[표본] 연구간호사", "phone": "02-000-0001", "email": "basket@example.org"}],
     "url": "https://clinicaltrials.gov/"},
]


def normalize_crit(c):
    if c.get("status") not in ("y", "n", "q"):
        c["status"] = "q"
    return c


# ----------------------------------------------------------------------------
# Flask
# ----------------------------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({
            "ok": True, "model": DEFAULT_MODEL,
            "key_present": bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")),
        })

    @app.post("/api/search")
    def search():
        body = request.get_json(force=True) or {}
        text = (body.get("text") or "").strip()
        if not text:
            return jsonify({"error": "검색어(환자 상황)를 입력하세요."}), 400
        try:
            q = extract_query(text)
            trials = fetch_ctgov(q)
            source = "clinicaltrials.gov"
            if not trials:
                trials = SAMPLE_TRIALS
                source = "sample"     # 실 API 미도달 → 표본 데이터
            top = trials[:MAX_TRIALS_SCORE]
            matches = {m["idx"]: m for m in score_trials(text, top)}
            results = []
            for i, t in enumerate(top):
                m = matches.get(i, {})
                results.append({
                    **t,
                    "matchPct": max(0, min(100, int(m.get("matchPct", 0)))) if m else None,
                    "summary": m.get("summary", ""),
                    "note": m.get("note", ""),
                    "crit": [normalize_crit(c) for c in m.get("crit", [])],
                })
            results.sort(key=lambda r: (r["matchPct"] is None, -(r["matchPct"] or 0)))
            return jsonify({"query": q, "source": source, "count": len(results), "results": results})
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"[TrialMatch] http://localhost:{port}  (model={DEFAULT_MODEL})")
    create_app().run(host="0.0.0.0", port=port, debug=False)

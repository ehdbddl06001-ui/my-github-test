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
class Similarity(BaseModel):
    """이 논문의 대상 집단이 '현재 환자'와 얼마나 비슷한지 축별 점수(0~100)."""
    disease: int            # 질환/암종 일치도
    biomarker: int          # 임상지표/바이오마커 일치도
    stage: int              # 병기/중증도 일치도
    line: int               # 이전 치료 차수 일치도
    drug: int               # 검토 약제 일치도


class Paper(BaseModel):
    id: int                 # 1,2,3... 인용 번호
    t: str                  # 논문 제목(한국어)
    j: str                  # 학술지/출처명
    y: int                  # 연도
    n: Optional[int] = None # 표본 수 (지침 등은 null)
    fit: str                # 이 케이스와의 부합 사유(짧게)
    sim: Similarity         # 환자 유사도 축별 점수


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
    reason: str                 # 신청 사유 문단 (모든 서식 공통)
    alternatives: str = ""      # 대체요법 검토 (효능·효과 초과 서식)
    unmet_need: str = ""        # 대체치료 부재 근거 (희귀의약품 서식)
    approval_status: str = ""   # 국내외 허가·공급 현황 (희귀의약품 서식)
    dose_rationale: str = ""    # 용량 설정 근거 (추가 용량 서식)
    benefit_risk: str = ""      # 기존 용량 대비 이익-위해 (추가 용량 서식)


# --- 실제 정부 서식(별지 제1호/제2호) 항목 -----------------------------------
class Form1Prose(BaseModel):
    """별지 제1호서식 '제출자료(요약)'."""
    evidence_basis: str = ""    # 의학적 근거자료
    drug_merits: str = ""       # 신청약제의 특·장점
    target_criteria: str = ""   # 대상 환자 기준
    dosage: str = ""            # 용법·용량
    duration: str = ""          # 투여기간(투여중단 시기 포함)
    other_admin: str = ""       # 기타(재투여 기준 등)
    reason_type2: str = ""      # 고시 제2조 해당 사유(유형2)
    opinion: str = ""           # 기타 의견


class PaperSummary(BaseModel):
    """별지 제2호서식 '제출논문 요약표' (논문 1편)."""
    id: int
    category: str = ""          # 근거수준 범주
    classification: str = ""    # 메타분석/Systematic Review/RCT/case-control or cohort/case report or case series/기타
    purpose: str = ""           # 시험목적
    selection: str = ""         # 대상환자 선정기준
    subjects: str = ""          # 피험자 수
    test_drug: str = ""         # 시험약
    control_drug: str = ""      # 대조약
    period: str = ""            # 시험기간
    method: str = ""            # 시험방법
    endpoints: str = ""         # 평가항목
    subject_chars: str = ""     # 피험자 특성
    results: str = ""           # 시험결과 및 결론
    etc: str = ""               # 기타


class OfficialDoc(BaseModel):
    form1: Form1Prose
    papers: List[PaperSummary]


# 유사도 가중치 기본값(합=1.0). 프론트 슬라이더로 조정 가능.
DEFAULT_WEIGHTS = {"disease": 0.30, "biomarker": 0.25, "stage": 0.15, "line": 0.15, "drug": 0.15}

# 신청 서식 유형별 안내(프롬프트/문서에서 사용)
FORM_LABELS = {
    "eff": "효능·효과 초과 (일반 허가초과)",
    "orphan": "희귀의약품 (희귀질환 대상)",
    "dose": "추가 용량 의약품 (용법·용량 초과)",
}


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
1) papers: 이 케이스에 부합하는 근거 문헌 4~6개. 유사도가 서로 다른 논문을 섞어라
   (거의 동일한 집단 ~ 부분적으로만 겹치는 집단까지). 그래야 순위가 의미를 갖는다.
   - t(제목)·j(출처)·fit(부합 사유)은 한국어. 그중 1개는 진료지침(j="진료지침", n=null).
   - id 는 1부터 연속. y 는 최근 연도 위주.
   - sim: 이 논문의 '대상 집단'이 위 [검토 케이스] 환자와 얼마나 비슷한지 축별 점수
     (0~100, 정수). disease(질환/암종), biomarker(임상지표), stage(병기), line(치료차수),
     drug(약제) 각각을 환자 조건과 대조해 냉정하게 매긴다. 진료지침처럼 특정 집단이
     아니면 중간값(50~70) 정도로.
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


def build_generate_prompt(c: dict, metrics: List[dict], trials: List[dict], form: str) -> str:
    ev = "\n".join(f"- {m.get('label')}: {m.get('val')} (출처 [{m.get('src')}])" for m in metrics)
    tr = "\n".join(f"- {t.get('id')} {t.get('t')} (부합률 {t.get('pct')}%)" for t in trials) or "- 없음"
    header = f"""아래 근거를 바탕으로 '허가초과 사용승인 신청서'의 서술 문단을 한국어로 작성하라.
과장·단정 없이 사실 근거에 기반해 담백하게 쓴다. 각 문단 3~5문장. 채우라고 지정된
필드만 작성하고, 나머지 필드는 빈 문자열("")로 둔다.

[신청 서식] {FORM_LABELS.get(form, FORM_LABELS['eff'])}
[약제] {c.get('drug')}
[질환] {c.get('typeLabel')} · {c.get('stage')} · {c.get('line')}"""
    if form == "dose":
        header += f"\n[기존 허가 용량] {c.get('approvedDose') or '미기재'}\n[신청(증량) 용량] {c.get('requestDose') or '미기재'}"
    if form == "orphan":
        header += f"\n[국내 추정 환자 수] {c.get('prevalence') or '미기재'}"
    body = f"""
[유효성/안전성 근거]
{ev}
[검토된 임상시험]
{tr}
"""
    if form == "orphan":
        fields = """[채울 필드]
- reason: '신청 사유'. 희귀질환이라 허가 임상근거가 제한적인 상황과 위 근거를 들어 신청 이유를 서술.
- unmet_need: '대체치료 부재 근거'. 현재 사용 가능한 대체치료가 없거나 매우 제한적임을 서술.
- approval_status: '국내외 허가·공급 현황'. 해외 허가/오프라벨 사용 관행 등 공급·근거 현황을 서술.
(alternatives, dose_rationale, benefit_risk 는 "")"""
    elif form == "dose":
        fields = """[채울 필드]
- reason: '신청 사유'. 기존 허가 용량으로 반응이 불충분해 증량이 필요한 상황을 위 근거로 서술.
- dose_rationale: '용량 설정 근거'. 신청 용량이 근거상 용량-반응 관계로 정당화됨을 서술.
- benefit_risk: '기존 용량 대비 이익-위해 평가'. 증량의 기대 이익과 용량 관련 위해를 균형 있게 서술.
(alternatives, unmet_need, approval_status 는 "")"""
    else:  # eff
        fields = """[채울 필드]
- reason: '신청 사유'. 표준치료 소진 상황과 위 근거에 근거해 왜 이 약제를 신청하는지.
- alternatives: '대체요법 검토'. 현행 급여 대체요법 대비 본 요법의 상대적 임상 이익을 서술.
(unmet_need, approval_status, dose_rationale, benefit_risk 는 "")"""
    return header + body + fields


def build_official_prompt(c: dict, metrics: List[dict], papers: List[dict], form: str) -> str:
    ev = "; ".join(f"{m.get('label')} {m.get('val')}" for m in metrics) or "제공된 지표 없음"
    plist = "\n".join(
        f"- id {p.get('id')}: {p.get('t')} / {p.get('j')} {p.get('y')} n={p.get('n')}" for p in papers
    ) or "- 없음"
    excess = "용법·용량 초과" if form == "dose" else "효능·효과 초과"
    rare = " · 희귀질환 해당(유형5 예)" if form == "orphan" else ""
    return f"""당신은 한국 '허가초과 약제 비급여 사용승인 신청서(별지 제1호서식)'와 논문별
'제출논문 요약표(별지 제2호서식)' 항목을 채우는 의학 보조자다. 반드시 JSON 스키마를 따른다.
과장 없이 담백하게 쓰고, 아는 것만 채우고 모르면 빈 문자열("")로 둔다.

[환자/신청]
- 질환: {c.get('typeLabel')} · {c.get('stage')} · {c.get('line')}
- 임상지표: {c.get('bio')}
- 약제: {c.get('drug')}
- 허가초과 유형(유형1): {excess}{rare}
- (증량 신청 시) 기존→신청 용량: {c.get('approvedDose')} → {c.get('requestDose')}
[추출 지표] {ev}
[제출 논문]
{plist}

[form1] 별지1 '제출자료(요약)' 필드:
- evidence_basis(의학적 근거자료 요약), drug_merits(신청약제의 특·장점),
  target_criteria(대상 환자 기준, 위 질환·지표 반영), dosage(용법·용량; 증량 신청이면 신청 용량),
  duration(투여기간, 투여중단 시기 포함), other_admin(기타-재투여 기준 등),
  reason_type2(고시 제2조 해당 사유 한 문장), opinion(기타 의견; 없으면 "").

[papers] 각 제출 논문 id마다 별지2 항목을 하나씩 채운다:
- id(그대로 정수),
- classification 은 정확히 다음 중 하나: "메타분석","Systematic Review",
  "Randomized controlled trial(RCT)","case-control or cohort studies",
  "case report or case series","기타".
- category(근거수준, 모르면 ""), purpose(시험목적), selection(대상환자 선정기준),
  subjects(피험자 수; 모르면 n 기반 "약 N명" 또는 ""), test_drug(시험약), control_drug(대조약),
  period(시험기간, 모르면 ""), method(시험방법), endpoints(평가항목),
  subject_chars(피험자 특성, 모르면 ""), results(시험결과 및 결론), etc(기타, 모르면 "").
반드시 위 제출 논문 id 각각에 대해 하나씩 생성한다."""


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
    default_src = papers[0].get("id") if papers else None
    # src 가 유효하지 않으면 버리지 말고 대표(첫) 논문으로 보정 → 지표가 통째로 사라지는 것 방지
    seen_k = set()
    clean_metrics = []
    for m in metrics:
        if m.get("src") not in valid_ids:
            if default_src is None:
                continue
            m["src"] = default_src
        k = m.get("k") or f"M{len(clean_metrics)}"
        if k in seen_k:
            k = f"{k}_{len(clean_metrics)}"
        m["k"] = k
        seen_k.add(k)
        clean_metrics.append(m)

    # 유사도 점수 보정: 누락/범위이탈 방지 (프론트가 이 값으로 가중 정렬)
    axes = ("disease", "biomarker", "stage", "line", "drug")
    for p in papers:
        sim = p.get("sim") or {}
        p["sim"] = {a: _clamp(sim.get(a, 55)) for a in axes}

    for t in trials:
        t["pct"] = _clamp(t.get("pct", 0))
        for c in t.get("crit", []):
            if c.get("status") not in ("y", "n", "q"):
                c["status"] = "q"

    return {"papers": papers, "metrics": clean_metrics, "trials": trials, "weights": DEFAULT_WEIGHTS}


def _clamp(v, lo=0, hi=100):
    try:
        return max(lo, min(hi, int(v)))
    except Exception:
        return lo


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
        papers = body.get("papers", [])
        form = body.get("form", "eff")
        try:
            out = call_gemini(build_official_prompt(c, metrics, papers, form), OfficialDoc)
            return jsonify(out)
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    return app


if __name__ == "__main__":
    # 로컬 실행용. Colab 에서는 노트북 마지막 셀(cloudflared)로 띄운다.
    port = int(os.environ.get("PORT", "8000"))
    print(f"[OncoReg AI] http://localhost:{port}  (model={DEFAULT_MODEL})")
    create_app().run(host="0.0.0.0", port=port, debug=False)

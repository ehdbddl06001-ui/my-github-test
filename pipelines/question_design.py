"""
question_design.py — 문항의 「출제 설계」와 「정보 역할」을 다루는 공용 모듈 (KMLE·USMLE·영상 공통).

왜 필요한가 (2026-09-18 사용자 지시):
  문항에 정상 활력징후·정상 검사값·음성 소견·배경 정보를 넣는 것은 **의도된 설계**다 — 실제 시험처럼
  여러 정보 가운데 중요한 단서를 골라 감별과 치료를 결정하는 능력을 훈련한다. 그런데 기존 규칙은
  정상값을 「미끼·잡음」으로 부르고 그 개수를 「난이도의 핵심 축」으로 삼아, (1) 정상 소견이 실제로
  어떤 감별·처치 판단에 쓰이는지 드러나지 않고 (2) 정보가 많으면 어렵다고 착각하게 만들었다.

  이 모듈은 문항 frontmatter 의 선택 필드 `design` 을 읽는다.

    design:
      target: 치료                 # 무엇을 평가하는가 — TARGETS 중 하나
      decision: "…"               # 정답을 고르게 하는 핵심 판단(한 문장)
      rival: B                    # 학습자가 실제로 혼동할 대안(보기 letter 1~2개)
      discriminator: "…"          # 그 대안과 정답을 가르는 소견
      steps: 2                    # 정답까지 필요한 판단 단계 수(1~4) — 난이도는 이것으로 매긴다
      chain:                      # 판단 사슬 — steps 개의 「단서 → 결론」(2026-09-24 이후 문항 필수)
        - "가려움 없는 저색소 반점 + KOH 균사·포자 → 어루러기"
        - "좁은 범위 · 재발 첫 회 → 국소 항진균제"
      findings:                   # 주요 정보의 역할. 하나가 여러 역할을 가질 수 있다
        - {item: "KOH 검경", role: key, why: "…"}
        - {item: "병변 감각 / 발한", role: rule_out, why: "…"}
        - {item: "혈당", role: [management, background], why: "…"}
      summary: "…"                # 핵심 판단 요약(2~3문장) — 채점 후 해설에 보인다
      switch: {choice: E, condition: "…"}   # 선택: 어떤 조건이 바뀌면 다른 보기가 더 적절해지는가

  역할(role):
    key         정답을 지지하는 핵심 소견
    rule_out    경쟁 진단의 가능성을 낮추는 정상·음성 소견 (「배제」로 과장하지 않는다)
    management  중증도·금기·치료 선택에 영향을 주는 정보
    background  판단에 영향이 적지만 임상적으로 자연스러운 배경 정보

  **검증은 두 층이다.**
    - 형식 검사(format_findings): 코드로 확인 가능한 것 — 필드·역할·letter·「문제에 없는 정보를 해설이
      인용하는가」. lint_questions.py 가 ERROR/WARN 으로 쓴다.
    - 내용 검토 신호(review_flags): 코드로 **판정할 수 없는** 의학적 타당성에 대해, 사람이 먼저 볼 곳을
      가리키는 신호일 뿐이다. 이 신호가 없다고 의학적으로 검증된 것이 아니다 — 확인 완료 표시는
      `review_status: reviewed` + 검토자·검토 메모가 있을 때만 한다(생성 모델의 confidence 로 대신하지 않는다).
"""
from __future__ import annotations

import re
from typing import Any

TARGETS = ("진단", "감별", "검사 선택", "치료", "다음 처치", "기전", "금기", "예후")
ROLES = ("key", "rule_out", "management", "background")
ROLE_LABEL = {
    "key": "결정적 단서",
    "rule_out": "의미 있는 정상·음성 소견",
    "management": "중증도·금기·치료 선택에 영향",
    "background": "비중이 낮은 정보",
}
LETTERS = "ABCDE"
REVIEW_STATUS = ("unreviewed", "reviewed", "needs_revision")

# design 이 없으면 형식 오류가 되는 기준일 — 이날 이후 생성된 문항부터 적용(기존 문항은 일괄 재생성하지 않는다)
DESIGN_REQUIRED_FROM = "2026-09-19"
MAX_FINDINGS = 10   # 해설의 정보 선별은 빠르게 복습할 분량으로 — 전 항목 나열 금지
# 판단 사슬(design.chain) 필수 기준일(2026-09-23 사용자 채택 — 「판단 단계를 높인다」). steps 를 숫자로만 적으면
# 실제로 몇 단계 추론인지 확인할 길이 없다 — 단계마다 「어떤 단서로 무엇을 정했나」를 한 줄씩 적게 해
# steps 와 개수가 맞는지 기계로 보고, 채점 뒤 앱이 사슬을 보여 줘 어느 단계에서 갈렸는지 스스로 찾게 한다.
CHAIN_REQUIRED_FROM = "2026-09-24"
# 하루 세트의 판단 단계 구성 목표(gen-kmle 「판단 단계 구성」) — mix_report 가 이 기준으로 WARN 한다.
MIX_MIN_DEEP = 0.4       # steps ≥ 3 비율 하한
MIX_MAX_SHALLOW = 0.1    # steps = 1 비율 상한
MIX_MAX_TARGET = 0.5     # 한 평가 목표(target)가 차지하는 비율 상한
MIX_MIN_N = 5            # 이보다 적은 묶음은 구성을 따지지 않는다
MIX_MAX_MANAGEMENT = 0.55  # 「치료」+「다음 처치」 합 상한(2026-09-25 감사: 09-19 이후 73 % — 따로 세면 둘 다 50 % 아래라 못 잡았다)
MIX_ANSWER_PERIOD = 0.5    # 정답 글자가 5문항 뒤에 되풀이되는 비율 상한(ABCDE 순환 — 번호만 보고 맞힐 수 있다)

# 정상·음성 소견을 「완전 배제」로 단정하는 표현 — 내용 검토 신호(판정 아님)
_ABSOLUTE = re.compile(
    r"(완전히\s*배제|배제한다|배제된다|배제할 수 있다|가능성이 없다|절대|확실히 아니|"
    r"\brules? out\b|\bexclud(?:e|es|ed)\b|\bexcludes?\b)", re.IGNORECASE)


# ── 읽기 ────────────────────────────────────────────────────────────────────
def _roles_of(f: dict[str, Any]) -> list[str]:
    r = f.get("role", f.get("roles"))
    if isinstance(r, str):
        return [x.strip() for x in re.split(r"[,/·\s]+", r) if x.strip()]
    if isinstance(r, list):
        return [str(x).strip() for x in r if str(x).strip()]
    return []


def _letters(v: Any) -> list[str]:
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return [str(x).strip().upper()[:1] for x in v if str(x).strip()]
    return [x.strip().upper()[:1] for x in re.split(r"[,/·\s]+", str(v)) if x.strip()]


def _norm(t: str) -> str:
    return re.sub(r"[\s·/,()\[\]{}\"'：:]+", "", str(t or "")).casefold()


def question_text_pool(meta: dict[str, Any]) -> str:
    """문항이 학습자에게 보여 주는 정보 전체(발문·활력징후·검사·그림 캡션) — 설계가 인용할 수 있는 범위."""
    parts = [str(meta.get("stem", "") or "")]
    for v in meta.get("vitals") or []:
        if isinstance(v, dict):
            parts += [str(v.get("name", "")), str(v.get("value", ""))]
    for l in meta.get("labs") or []:
        if isinstance(l, dict):
            parts += [str(l.get("name", "")), str(l.get("value", ""))]
    fig = meta.get("figure")
    if isinstance(fig, dict):
        parts += [str(fig.get("caption", "")), str(fig.get("alt", ""))]
    return "\n".join(parts)


def _item_in_question(item: str, pool_norm: str, has_figure: bool) -> bool:
    it = str(item or "").strip()
    if not it:
        return False
    if has_figure and re.match(r"^(영상|그림|사진|심전도|파형|figure|image|ecg)\b", it, re.IGNORECASE):
        return True                          # 그림 자체의 소견(판독 대상)은 발문 텍스트에 없어도 된다
    n = _norm(it)
    if n and n in pool_norm:
        return True
    # 「혈당 / HIV」처럼 여러 항목을 묶은 인용은 각 조각이 모두 문항에 있으면 통과
    pieces = [_norm(p) for p in re.split(r"[/,·]| 및 | and ", it) if _norm(p)]
    return bool(pieces) and all(p in pool_norm for p in pieces)


def _sentences(t: str) -> int:
    t = str(t or "").strip()
    if not t:
        return 0
    return len([s for s in re.split(r"(?<=[.!?。])\s+|(?<=다\.)(?=\s|$)", t) if s.strip()])


# ── 형식 검사 ────────────────────────────────────────────────────────────────
def design_required(meta: dict[str, Any], qtype: str) -> bool:
    # 영상 카드(imaging)는 빌더(exam-builder)가 만드는 파생물이다 — 필수 검사는 원천(빌더 조립기)에서 한다.
    # 여기서 필수로 걸면 빌더 쪽 누락 하나로 핸드폰 앱 갱신 전체가 막힌다. 있으면 형식은 똑같이 본다.
    if qtype not in ("kmle", "usmle"):
        return False
    return str(meta.get("date", "") or "") >= DESIGN_REQUIRED_FROM


def format_findings(meta: dict[str, Any], qtype: str) -> list[tuple[str, str, str]]:
    """(level, code, msg) 목록. level ∈ ERROR·WARN. 코드로 확인 가능한 형식만 본다."""
    out: list[tuple[str, str, str]] = []
    d = meta.get("design")
    if d is None:
        if design_required(meta, qtype):
            out.append(("ERROR", "design-missing",
                        f"{DESIGN_REQUIRED_FROM} 이후 문항은 `design`(출제 설계·정보 역할)이 필요하다 — "
                        f"무엇을 평가하는지·핵심 판단·혼동 대안·정보 역할을 적어라."))
        return out
    if not isinstance(d, dict):
        return [("ERROR", "design-type", "design 은 사전(dict)이어야 한다.")]

    target = str(d.get("target", "") or "").strip()
    if target not in TARGETS:
        out.append(("ERROR", "design-target", f"design.target '{target}' 은 {'/'.join(TARGETS)} 중 하나여야 한다."))
    for key in ("decision", "summary"):
        if not str(d.get(key, "") or "").strip():
            out.append(("ERROR", f"design-{key}", f"design.{key} 가 비어 있다."))

    choices = meta.get("choices") or []
    n_choices = len(choices)
    ans = str(meta.get("answer", "")).strip().upper()[:1]
    valid = set(LETTERS[:n_choices]) if n_choices else set(LETTERS)
    rivals = _letters(d.get("rival"))
    for r in rivals:
        if r not in valid:
            out.append(("ERROR", "design-rival", f"design.rival '{r}' 는 보기에 없다."))
        elif r == ans:
            out.append(("ERROR", "design-rival", "design.rival 이 정답과 같다 — 혼동할 **오답**을 적어라."))
    if len(rivals) > 2:
        out.append(("WARN", "design-rival-many", "혼동 대안은 1~2개로 좁혀라(전부 적으면 설계가 흐려진다)."))
    if rivals and not str(d.get("discriminator", "") or "").strip():
        out.append(("ERROR", "design-discriminator", "혼동 대안을 적었으면 정답과 가르는 소견(discriminator)도 적어라."))

    steps = d.get("steps")
    if steps is not None:
        try:
            s = int(steps)
            if not 1 <= s <= 4:
                raise ValueError
        except (TypeError, ValueError):
            out.append(("ERROR", "design-steps", "design.steps 는 1~4 정수여야 한다."))
            steps = None

    chain = d.get("chain")
    if chain is None:
        if qtype in ("kmle", "usmle") and str(meta.get("date", "") or "") >= CHAIN_REQUIRED_FROM:
            out.append(("ERROR", "design-chain-missing",
                        f"{CHAIN_REQUIRED_FROM} 이후 문항은 design.chain(판단 사슬 — steps 개의 「단서 → 결론」 한 줄씩)이 필요하다."))
    elif not isinstance(chain, list) or not all(isinstance(c, str) and c.strip() for c in chain):
        out.append(("ERROR", "design-chain", "design.chain 은 비어 있지 않은 문자열 목록이어야 한다."))
    else:
        if steps is not None and len(chain) != int(steps):
            out.append(("ERROR", "design-chain-steps",
                        f"design.chain 이 {len(chain)}줄인데 steps 는 {steps} — 단계 수와 사슬 길이를 맞춰라."))
        for i, c in enumerate(chain, 1):
            if "→" not in c:
                out.append(("WARN", "design-chain-arrow", f"design.chain[{i}] 에 「단서 → 결론」 화살표가 없다."))
            if len(c) > 140:
                out.append(("WARN", "design-chain-long", f"design.chain[{i}] 이 길다({len(c)}자) — 한 단계는 한 줄로."))

    findings = d.get("findings") or []
    if not isinstance(findings, list) or not findings:
        out.append(("ERROR", "design-findings", "design.findings 에 주요 정보의 역할을 적어라(최소 결정적 단서 1개)."))
        findings = []
    pool_norm = _norm(question_text_pool(meta))
    has_figure = bool(meta.get("figure"))
    n_key = 0
    for i, f in enumerate(findings, 1):
        if not isinstance(f, dict):
            out.append(("ERROR", "design-finding-type", f"design.findings[{i}] 는 {{item, role, why}} 사전이어야 한다."))
            continue
        roles = _roles_of(f)
        bad = [r for r in roles if r not in ROLES]
        if not roles or bad:
            out.append(("ERROR", "design-role", f"design.findings[{i}] 역할 {bad or '(없음)'} — {'/'.join(ROLES)} 중에서."))
        if "key" in roles:
            n_key += 1
        item = str(f.get("item", "") or "")
        if not _item_in_question(item, pool_norm, has_figure):
            out.append(("ERROR", "design-item-not-in-question",
                        f"design.findings[{i}] '{item}' 이 발문·활력징후·검사 어디에도 없다 — "
                        f"해설이 문제에 없던 정보를 끌어오면 안 된다(표기를 문항과 맞추거나 빼라)."))
        if roles and roles != ["key"] and not str(f.get("why", "") or "").strip():
            out.append(("WARN", "design-why", f"design.findings[{i}] '{item}' 의 역할 이유(why)가 없다 — "
                                              f"왜 넘겨도 되는지·어떤 대안을 낮추는지 한 줄로."))
    if findings and n_key == 0:
        out.append(("ERROR", "design-no-key", "결정적 단서(role: key)가 하나도 없다."))
    if len(findings) > MAX_FINDINGS:
        out.append(("WARN", "design-too-many",
                    f"정보 역할을 {len(findings)}개 적었다(권장 ≤ {MAX_FINDINGS}) — 모든 자료를 하나씩 풀이하지 말고, "
                    f"판단에 쓰였거나 학습자가 끌려가기 쉬운 정보만 적어라. 아무도 끌려가지 않을 정상값은 생략한다."))

    sw = d.get("switch")
    if sw is not None:
        if not isinstance(sw, dict):
            out.append(("ERROR", "design-switch", "design.switch 는 {choice, condition} 사전이어야 한다."))
        else:
            c = _letters(sw.get("choice"))
            if not c or c[0] not in valid or c[0] == ans:
                out.append(("ERROR", "design-switch", "design.switch.choice 는 정답이 아닌 보기 letter 여야 한다."))
            if not str(sw.get("condition", "") or "").strip():
                out.append(("ERROR", "design-switch", "design.switch.condition(무엇이 바뀌면)이 비어 있다."))

    if _sentences(d.get("summary", "")) > 3 or len(str(d.get("summary", "") or "")) > 360:
        out.append(("WARN", "design-summary-long", "핵심 판단 요약은 2~3문장으로 — 빠르게 복습할 분량을 지켜라."))

    diff = meta.get("difficulty")
    try:
        diff = int(diff) if diff is not None else None
    except (TypeError, ValueError):
        diff = None
    if steps is not None and diff is not None:
        s = int(steps)
        if diff >= 4 and s < 2:
            out.append(("WARN", "difficulty-vs-steps",
                        f"difficulty {diff} 인데 판단 단계가 {s} — 난이도는 정보량이 아니라 판단 단계·대안의 그럴듯함으로 매긴다."))
        if diff <= 2 and s >= 3:
            out.append(("WARN", "difficulty-vs-steps",
                        f"difficulty {diff} 인데 판단 단계가 {s} — 난이도를 낮게 매긴 것은 아닌지 확인하라."))

    rs = meta.get("review_status")
    if rs is not None:
        if rs not in REVIEW_STATUS:
            out.append(("ERROR", "review-status", f"review_status 는 {'/'.join(REVIEW_STATUS)} 중 하나."))
        if rs == "reviewed" and not (str(meta.get("reviewed_by", "") or "").strip()
                                     and str(meta.get("review_note", "") or "").strip()):
            out.append(("ERROR", "review-unbacked",
                        "review_status: reviewed 는 reviewed_by·review_note(무엇을 어떤 근거로 확인했는지)가 있어야 한다."))
    return out


# ── 내용 검토 신호 ──────────────────────────────────────────────────────────
REVIEW_QUESTIONS = (
    "단일 최선의 답이 성립하는가(다른 보기도 정답일 여지가 없는가)",
    "정상·음성 소견의 의미를 과장하지 않았는가(가능성을 낮출 뿐 배제한다고 쓰지 않았는가)",
    "추가한 정보가 정답·해설과 모순되지 않는가(경미한 이상값이 정답의 유일성을 해치지 않는가)",
    "정보가 많아도 목표한 판단(design.target·decision)을 실제로 평가하는가",
    "해설이 문제에 없던 사실을 새로 끼워 넣지 않았는가",
    "검사·치료 근거가 해당 시험(KMLE=한국 진료 맥락, USMLE=미국)에 맞는가",
)


def review_flags(meta: dict[str, Any]) -> list[tuple[str, str]]:
    """(code, msg) — 사람이 먼저 볼 곳. **판정이 아니다.** 신호가 없어도 검증된 것이 아니다."""
    d = meta.get("design")
    if not isinstance(d, dict):
        return []
    flags: list[tuple[str, str]] = []
    findings = [f for f in (d.get("findings") or []) if isinstance(f, dict)]
    for f in findings:
        roles = _roles_of(f)
        if ("rule_out" in roles or "key" in roles) and _ABSOLUTE.search(str(f.get("why", "") or "")):
            flags.append(("absolute-exclusion",
                          f"'{f.get('item')}' 설명이 정상·음성 소견으로 「배제」를 단정한다 — 가능성을 낮춘다고 쓸 것인지 검토"))
    if _ABSOLUTE.search(str(d.get("summary", "") or "")):
        flags.append(("absolute-exclusion", "핵심 판단 요약에 단정적 배제 표현이 있다 — 과장인지 검토"))
    n_key = sum(1 for f in findings if "key" in _roles_of(f))
    try:
        diff = int(meta.get("difficulty")) if meta.get("difficulty") is not None else None
    except (TypeError, ValueError):
        diff = None
    if diff is not None and diff >= 4 and n_key <= 1 and str(d.get("target", "")) in ("진단", "감별"):
        flags.append(("single-clue",
                      "복합 추론(difficulty ≥ 4)을 목표로 했는데 결정적 단서가 하나다 — 키워드 하나로 풀리는지 검토"))
    labs = meta.get("labs") or []
    lab_names = {_norm(l.get("name", "")) for l in labs if isinstance(l, dict)}
    cited = {_norm(f.get("item", "")) for f in findings}
    uncited = [l for l in lab_names if l and not any(l in c or c in l for c in cited)]
    if len(labs) >= 8 and len(uncited) >= 5:
        flags.append(("unassigned-labs",
                      f"검사 {len(labs)}개 중 {len(uncited)}개가 어떤 역할에도 인용되지 않는다 — "
                      f"그 상황에서 실제로 시행할 검사인지(배경을 위해 만든 목록은 아닌지) 검토"))
    if not d.get("rival"):
        flags.append(("no-rival", "혼동할 대안(rival)을 적지 않았다 — 보기들이 실제로 경쟁하는지 검토"))
    return flags


# ── 웹 내보내기 ──────────────────────────────────────────────────────────────
def design_record(meta: dict[str, Any]) -> dict[str, Any] | None:
    """웹 번들용. 채점 후 「정보를 어떻게 선별했는가」 블록을 그리는 데 필요한 것만."""
    d = meta.get("design")
    if not isinstance(d, dict):
        return None
    groups: dict[str, list[dict[str, Any]]] = {r: [] for r in ROLES}
    for f in d.get("findings") or []:
        if not isinstance(f, dict):
            continue
        roles = [r for r in _roles_of(f) if r in ROLES]
        if not roles:
            continue
        # 한 정보는 첫 역할(주 역할)에 한 번만 보인다 — 나머지 역할은 꼬리표로(같은 줄 반복 방지)
        groups[roles[0]].append({"item": str(f.get("item", "") or ""), "why": str(f.get("why", "") or ""),
                                 "also": [ROLE_LABEL[r] for r in roles[1:]]})
    sw = d.get("switch") if isinstance(d.get("switch"), dict) else None
    rec = {
        "target": str(d.get("target", "") or ""),
        "decision": str(d.get("decision", "") or ""),
        "rival": _letters(d.get("rival")),
        "discriminator": str(d.get("discriminator", "") or ""),
        "steps": d.get("steps"),
        "chain": [str(c) for c in d.get("chain") or [] if isinstance(c, str) and c.strip()],
        "key": groups["key"],
        "ruleOut": groups["rule_out"],
        "management": groups["management"],
        "background": groups["background"],
        "summary": str(d.get("summary", "") or ""),
        "switch": ({"choice": (_letters(sw.get("choice")) or [""])[0], "condition": str(sw.get("condition", "") or "")}
                   if sw else None),
    }
    return rec


def mix_report(metas: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """문항 묶음(보통 하루 세트)의 판단 단계·평가 목표 구성. (요약, WARN 목록). design 없는 문항은 센다만 한다."""
    steps: dict[int, int] = {}
    targets: dict[str, int] = {}
    n = 0
    for m in metas:
        d = m.get("design") if isinstance(m.get("design"), dict) else None
        if not d:
            continue
        try:
            s = int(d.get("steps"))
        except (TypeError, ValueError):
            continue
        n += 1
        steps[s] = steps.get(s, 0) + 1
        t = str(d.get("target", "") or "")
        targets[t] = targets.get(t, 0) + 1
    summary = {"n": n, "steps": dict(sorted(steps.items())), "targets": dict(sorted(targets.items(), key=lambda x: -x[1]))}
    warns: list[str] = []
    if n >= MIX_MIN_N:
        deep = sum(v for k, v in steps.items() if k >= 3) / n
        shallow = steps.get(1, 0) / n
        top_t, top_n = max(targets.items(), key=lambda x: x[1])
        if deep < MIX_MIN_DEEP:
            warns.append(f"판단 3단계 이상이 {deep:.0%} — 목표 {MIX_MIN_DEEP:.0%} 이상(진단 → 중증도/금기 → 처치처럼 이어지는 문항을 늘린다)")
        if shallow > MIX_MAX_SHALLOW:
            warns.append(f"판단 1단계(단순 회상)가 {shallow:.0%} — 목표 {MIX_MAX_SHALLOW:.0%} 이하")
        if top_n / n > MIX_MAX_TARGET:
            warns.append(f"평가 목표 「{top_t}」가 {top_n / n:.0%} — 한 목표는 {MIX_MAX_TARGET:.0%} 이하(진단·감별·기전·검사 선택도 섞는다)")
        mg = (targets.get("치료", 0) + targets.get("다음 처치", 0)) / n
        if mg > MIX_MAX_MANAGEMENT:
            warns.append(f"「치료」+「다음 처치」가 {mg:.0%} — 합쳐서 {MIX_MAX_MANAGEMENT:.0%} 이하(진단·감별·검사 선택·기전·예후를 섞는다)")
    warns += answer_order_warnings(metas)
    return summary, warns


def answer_order_warnings(metas: list[dict[str, Any]]) -> list[str]:
    """정답 순서가 기계적인가(날짜별 세트, id 순). 글자 분포가 고르더라도 ABCDE 로 돌면 번호만 보고 풀린다."""
    by_day: dict[str, list[tuple[str, str]]] = {}
    for m in metas:
        a = str(m.get("answer", "") or "").strip().upper()[:1]
        if a in "ABCDE" and a:
            by_day.setdefault(str(m.get("date", "") or ""), []).append((str(m.get("id", "")), a))
    out = []
    for day, items in sorted(by_day.items()):
        seq = [a for _, a in sorted(items)]
        if len(seq) < 10:
            continue
        same5 = sum(seq[i] == seq[i + 5] for i in range(len(seq) - 5)) / (len(seq) - 5)
        runs = sum(1 for i in range(len(seq) - 3) if "".join(seq[i:i + 4]) in "ABCDEABCDE" or "".join(seq[i:i + 4]) in "EDCBAEDCBA")
        if same5 > MIX_ANSWER_PERIOD or runs >= 2:
            out.append(f"{day} 세트 정답 순서가 규칙적이다({''.join(seq[:15])}…, 5칸 주기 {same5:.0%}·연속 알파벳 {runs}곳) — "
                       f"문항마다 정답 위치를 무작위로 정한다(보기를 섞고 answer 를 다시 적는다)")
    return out


def review_status(meta: dict[str, Any]) -> str:
    rs = str(meta.get("review_status", "") or "")
    return rs if rs in REVIEW_STATUS else "unreviewed"

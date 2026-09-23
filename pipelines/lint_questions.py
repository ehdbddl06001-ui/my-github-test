"""
lint_questions.py — KMLE/USMLE 문항의 '시험 감각' 품질을 기계적으로 점검한다.

배경: frontmatter.py 는 '계약(필수 필드)'만 본다. 하지만 실제 실패는 계약이 아니라
'문항 품질'에서 난다 — 소견을 에포님으로 떠먹이거나, 정답 보기만 길거나, 해설의
보기별 반박이 한 줄로 뭉치는 식. 이런 건 LLM 자기검증에 맡기지 말고(누락됨) 여기서
결정론으로 잡는다(CLAUDE.md: 검증·세기는 pipelines가 한다).

기준의 근거는 실제 '임상의학종합평가' 시험지다:
  - 활력징후 4종(혈압·맥박·호흡·체온)을 **정상이라도 항상** 제시한다.
  - 검사 소견은 참고치와 함께 **정상값도** 준다 — 실제 환자에서 함께 주어지는 자료 가운데 무엇이
    판단에 쓰이고 무엇은 넘겨도 되는지 가리게 한다(정상값의 개수는 난이도가 아니다).
  - 2026-09-19 이후 문항은 `design`(출제 설계·정보 역할)을 갖는다 — question_design.py 가 형식을 본다.
  - 소견은 서술하되 그 **해석(에포님·징후명)을 괄호로 떠먹이지 않는다**.
  - 보기 5개는 **동질적·평행**(전부 약물/처치/진단)하고 길이가 고르다.

심각도:
  ERROR  — 시험 문항으로서 결함(형식). 기본 실행에서 exit 1.
  WARN   — 품질 저하(형식). 기본은 리포트만(exit 0), `--strict` 면 exit 1.
  REVIEW — **내용 검토 신호**. 의학적 타당성은 코드로 판정할 수 없으므로 실패로 치지 않고, 사람이 먼저
           볼 곳만 가리킨다. REVIEW 가 없다고 의학적으로 검증된 것이 아니다(review_questions.py 참고).

사용:
  python pipelines/lint_questions.py                      # content/ 전체 리포트
  python pipelines/lint_questions.py content/kmle/2026/kmle-2026-0129.md  # 특정 파일
  python pipelines/lint_questions.py --strict <files...>  # WARN 도 실패 처리
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

from frontmatter import load, Doc, QUESTION_TYPES
from question_design import format_findings, review_flags
from concepts import OBJECTIVE_REQUIRED_FROM, load_concepts, question_learning_errors

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
LETTERS = "ABCDE"

# 소견을 서술한 뒤 곧바로 그 해석을 괄호로 떠먹이는 패턴.
# 예: "밀어도 벗겨지지 않으며(니콜스키 음성)", "(Nikolsky 징후 양성)"
_SIGN = r"(?:니콜스키|nikolsky|[가-힣]{1,6}징후|반사|\bsign\b|무리츠|homans|murphy|머피)"
_POLARITY = r"(?:양성|음성|positive|negative|\(\+\)|\(\-\)|＋|－)"
EPONYM_GLOSS = re.compile(
    r"\([^()]*" + _SIGN + r"[^()]*" + _POLARITY + r"[^()]*\)",
    re.IGNORECASE,
)

# 임상 증례로 보이는 stem(활력징후를 줘야 마땅한) 판별용.
CLINICAL_HINT = re.compile(
    r"(\d+\s*세|\d+\s*year|응급실|내원|병원에 왔다|왔다|호소|주소로|complains|presents|brought)",
    re.IGNORECASE,
)
# 활력징후가 stem 산문 안에 이미 들어있는지(구조화 안 했어도 최소 제시는 한 경우).
VITALS_IN_STEM = re.compile(r"(혈압|맥박|호흡|체온|blood pressure|heart rate|temperature)", re.IGNORECASE)

CONJUNCTION = re.compile(r"(하고|와 함께|과 함께|및|,|\band\b|\+)", re.IGNORECASE)


class Finding:
    __slots__ = ("level", "code", "msg")

    def __init__(self, level: str, code: str, msg: str):
        self.level = level  # "ERROR" | "WARN" | "REVIEW"
        self.code = code
        self.msg = msg


def _differ_value(body: str) -> str | None:
    """'## 정답 및 해설'에서 '오답감별' 항목의 값(하위 줄 포함)을 통째로 뽑는다."""
    if "## 정답 및 해설" not in body:
        return None
    sec = body.split("## 정답 및 해설", 1)[1]
    lines = sec.splitlines()
    out: list[str] = []
    capturing = False
    for raw in lines:
        st = raw.strip()
        m = re.match(r"^-\s*\*?\*?(오답감별)\*?\*?\s*[:：]?\s*(.*)$", st)
        if m:
            capturing = True
            if m.group(2):
                out.append(m.group(2))
            continue
        if capturing:
            # 다음 최상위 '- **키**:' 항목을 만나면 종료
            if re.match(r"^-\s*\*\*.+?\*\*", st):
                break
            if st:
                out.append(st)
    return "\n".join(out) if capturing else None


def _clean_choice(opt: str) -> str:
    return re.sub(r"^\s*[A-E][.)]\s*", "", str(opt)).strip()


def lint_doc(d: Doc) -> list[Finding]:
    m = d.meta
    stem = str(m.get("stem", "") or "")
    findings: list[Finding] = []

    # 1) 에포님 떠먹임 (ERROR) — 소견 서술 + (에포님 양성/음성) 동시 노출.
    if EPONYM_GLOSS.search(stem):
        hit = EPONYM_GLOSS.search(stem).group(0)
        findings.append(Finding(
            "ERROR", "eponym-gloss",
            f"stem이 소견을 서술한 뒤 해석을 괄호로 떠먹임 {hit} — "
            f"소견(예: '밀어도 벗겨지지 않는다') 또는 징후명 중 하나만 제시하라."))

    # 2) 활력징후 부재 (WARN) — 임상 증례인데 vitals도 없고 산문에도 활력징후가 없음.
    vitals = m.get("vitals") or []
    if CLINICAL_HINT.search(stem) and not vitals and not VITALS_IN_STEM.search(stem):
        findings.append(Finding(
            "WARN", "missing-vitals",
            "임상 증례인데 활력징후가 없다. 실제 시험은 정상이라도 혈압·맥박·호흡·체온을 "
            "항상 준다 — frontmatter `vitals`(4종)를 넣어라."))

    # 3) 정상 미끼값 부재 (WARN) — labs가 있는데 참고치가 하나도 없음.
    labs = m.get("labs") or []
    if labs and not any((l.get("ref") if isinstance(l, dict) else None) for l in labs):
        findings.append(Finding(
            "WARN", "no-lab-ref",
            "labs에 참고치(ref)가 없다. 참고치를 줘야 학습자가 정상·이상을 스스로 가린다."))

    # 4) 검사 소견을 stem 산문이 그대로 복창 (WARN) — 구조화 자료와 중복.
    for l in labs:
        if not isinstance(l, dict):
            continue
        val = str(l.get("value", "") or "")
        # 값에서 숫자·단위를 뺀 '소견 문구'가 길게 stem에 그대로 있으면 중복.
        phrase = re.sub(r"[\d.,/%°]+.*", "", val).strip()
        if len(phrase) >= 6 and phrase in stem:
            findings.append(Finding(
                "WARN", "dup-stem-labs",
                f"검사 소견 '{phrase}'가 stem 산문에도 그대로 있다 — 구조화 자료(labs)로만 두고 "
                f"stem에서는 빼라(중복 = 떠먹임)."))
            break

    # 보기 분석
    choices = [_clean_choice(c) for c in (m.get("choices") or [])]
    ans = str(m.get("answer", "")).strip().upper()
    ans_idx = LETTERS.find(ans[:1]) if ans else -1
    if choices and 0 <= ans_idx < len(choices):
        lens = [len(c) for c in choices]
        correct_len = lens[ans_idx]
        distractor_lens = [l for i, l in enumerate(lens) if i != ans_idx]
        if distractor_lens:
            mx = max(distractor_lens)
            # 5) 정답 보기만 유독 김 (WARN) — 길이=정답 힌트.
            if correct_len > max(mx * 1.5, mx + 12):
                findings.append(Finding(
                    "WARN", "answer-length-tell",
                    f"정답 보기가 오답들보다 유독 길다(정답 {correct_len}자 vs 오답 최대 {mx}자). "
                    f"길이가 정답을 알려준다 — 모든 보기를 평행·비슷한 길이로."))
            # 6) 보기 길이 불균형 (WARN)
            if min(lens) and max(lens) / max(min(lens), 1) > 3.0:
                findings.append(Finding(
                    "WARN", "choices-uneven",
                    f"보기 길이가 고르지 않다(최소 {min(lens)}자, 최대 {max(lens)}자). "
                    f"동질적·평행 보기로 맞춰라."))
        # 7) 정답만 복합문(‘A하고 B도 함께’)인데 오답은 단순 (WARN) — 완결성=정답 힌트.
        if CONJUNCTION.search(choices[ans_idx]):
            simple_distractors = sum(
                1 for i, c in enumerate(choices)
                if i != ans_idx and not CONJUNCTION.search(c))
            if simple_distractors >= len(choices) - 1:
                findings.append(Finding(
                    "WARN", "answer-compound-tell",
                    "정답만 '~하고 ~도 함께' 식 복합 처치이고 오답은 단순 단일 항목이다 — "
                    "가장 완결적인 보기가 정답이라는 힌트. 보기를 같은 층위로 평행하게."))

    # 8) 오답감별 letter 커버리지 (ERROR) + 한 줄 뭉침 (WARN)
    differ = _differ_value(d.body)
    if differ is None:
        if d.type in QUESTION_TYPES:
            findings.append(Finding(
                "ERROR", "no-differ",
                "해설에 '오답감별' 항목이 없다. 보기별로 왜 틀렸는지 전부 달아라."))
    else:
        need = [LETTERS[i] for i in range(len(choices)) if i != ans_idx]
        marker_letters = set(re.findall(r"(?:^|\n|\s|\()([A-E])(?=[\s:.)])", differ))
        missing = [x for x in need if x not in marker_letters]
        if missing:
            findings.append(Finding(
                "ERROR", "differ-coverage",
                f"오답감별이 보기 {', '.join(missing)}를 다루지 않는다. 정답 외 모든 보기를 "
                f"letter별로 반박하라."))
        # 한 줄에 여러 보기 반박이 뭉쳐 있으면(줄바꿈 없이 마커 ≥3) 가독성 저하.
        if "\n" not in differ and len(re.findall(r"(?:^|\s|\()[A-E](?=[\s:.)])", differ)) >= 3:
            findings.append(Finding(
                "WARN", "differ-oneline",
                "오답감별이 한 줄에 A·B·C…로 뭉쳐 있다. 보기별로 줄을 나눠라 "
                "(각 줄 `  - (A) …` 형식 — 웹이 줄 단위로 렌더)."))

    # 9) 출제 설계·정보 역할(형식) — 2026-09-19 이후 문항은 필수
    for level, code, msg in format_findings(m, d.type):
        findings.append(Finding(level, code, msg))
    # 10) 내용 검토 신호 — 실패로 치지 않는다
    for code, msg in review_flags(m):
        findings.append(Finding("REVIEW", code, msg))
    # 11) 오답 뒤 학습 흐름 필드(objective·distractors·case_path) — 있으면 형식·도식 정합성을 본다
    if d.type in ("kmle", "usmle") and not m.get("objective")             and str(m.get("date", "") or "") >= OBJECTIVE_REQUIRED_FROM:
        findings.append(Finding("WARN", "objective-missing",
                                "학습 목표(objective)가 없다 — 이 문항을 틀려도 이론 정리본으로 이어지지 않는다. "
                                "기존 정리본 id 를 붙이거나 새 목표 id 를 정한다(/gen-concept)."))
    if any(k in m for k in ("objective", "distractors", "case_path")):
        concept = _concepts().get(str(m.get("objective") or ""))
        for level, msg in question_learning_errors(m, concept):
            findings.append(Finding(level, "learning", msg))

    return findings


_CONCEPT_CACHE: dict | None = None


def _concepts() -> dict:
    global _CONCEPT_CACHE
    if _CONCEPT_CACHE is None:
        _CONCEPT_CACHE, _ = load_concepts()
    return _CONCEPT_CACHE


def iter_question_docs(paths: Iterable[Path]) -> list[Doc]:
    docs: list[Doc] = []
    for p in paths:
        d = load(p)
        if d.type in QUESTION_TYPES:
            docs.append(d)
    return docs


def collect_paths(args: list[str]) -> list[Path]:
    if args:
        out: list[Path] = []
        for a in args:
            p = Path(a)
            if p.is_dir():
                out.extend(sorted(p.rglob("*.md")))
            else:
                out.append(p)
        return out
    return sorted((CONTENT_DIR / "kmle").rglob("*.md")) + \
        sorted((CONTENT_DIR / "usmle").rglob("*.md"))


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    files = [a for a in argv if not a.startswith("--")]
    paths = collect_paths(files)

    n_err = n_warn = n_rev = n_docs = 0
    metas = []
    for d in iter_question_docs(paths):
        metas.append(d.meta)
        fs = lint_doc(d)
        if not fs:
            continue
        n_docs += 1
        rel = d.path.relative_to(ROOT) if str(d.path).startswith(str(ROOT)) else d.path
        print(f"\n{rel}  ({d.id})")
        for f in fs:
            if f.level == "ERROR":
                n_err += 1
            elif f.level == "WARN":
                n_warn += 1
            else:
                n_rev += 1
            print(f"  [{f.level}] {f.code}: {f.msg}")

    from question_design import mix_report
    mix, mix_warns = mix_report(metas)
    print(f"\n{'─'*60}")
    print(f"판단 단계 구성(design 있는 {mix['n']}문항): 단계 {mix['steps']} · 평가 목표 {mix['targets']}")
    for w in mix_warns:
        n_warn += 1
        print(f"  [WARN] mix: {w}")
    print(f"린트 완료: 문항 {n_docs}건에서 ERROR {n_err} · WARN {n_warn} · 내용 검토 신호 {n_rev}")
    if n_rev:
        print("  (REVIEW 는 판정이 아니다 — `python pipelines/review_questions.py <파일>` 로 검토지를 만들어 확인한다)")
    if n_err or (strict and n_warn):
        print("→ 수정 필요(품질 기준 미달).")
        return 1
    print("→ 통과.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

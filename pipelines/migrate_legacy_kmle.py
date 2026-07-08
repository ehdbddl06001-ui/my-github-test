"""
migrate_legacy_kmle.py — 레거시 quiz.py KMLE 트랙(docs/questions.js, 97문항)을
content/kmle(MedKOS SoT) 규격 .md 로 **1회 이관**한다(이후 레거시 트랙은 폐기).

레거시 레코드(진단/정답근거/오답감별/임상핵심 + 일부 appendix)는 품질이 좋으므로
보존한다. 과목명은 일일 문항과 병합되도록 가능한 것은 영문 토픽으로 매핑한다.

사용(1회): python pipelines/migrate_legacy_kmle.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from state import next_id, record_topic  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "questions.js"
OUT_DIR = ROOT / "content" / "kmle" / "2026"

# 레거시 한글 과목 → 일일 문항과 통일할 영문 토픽(없는 것은 그대로 유지)
SUBJECT_MAP = {
    "순환기": "Cardiology", "호흡기": "Pulmonology", "소화기": "Gastroenterology",
    "신장": "Nephrology", "내분비": "Endocrinology", "혈액종양": "Hematology-Oncology",
    "감염": "Infectious Disease", "류마티스": "Rheumatology", "알레르기": "Allergy",
    "산부인과": "Obstetrics & Gynecology", "소아청소년과": "Pediatrics",
    "정신건강의학과": "Psychiatry", "신경과": "Neurology",
    "의학총론": "General Medicine",
    # 매핑 없는 것은 원 한글 유지: 기타마이너, 의료관계법규
}
LETTERS = ["A", "B", "C", "D", "E"]
EXPL_ORDER = ["진단", "정답근거", "오답감별", "임상핵심"]


def _str_repr(dumper, data):
    # 여러 줄 문자열(appendix 표 등)은 블록 스칼라 '|'로 — 줄바꿈 보존, 안전.
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _str_repr, Dumper=yaml.SafeDumper)


def load_legacy() -> list[dict]:
    t = SRC.read_text(encoding="utf-8")
    return json.loads(t[t.index("["): t.rindex("]") + 1])


def to_md(rec: dict, new_id: str) -> str:
    subject = rec.get("subject", "")
    topic = SUBJECT_MAP.get(subject, subject)
    options = rec.get("options", [])
    ans_idx = int(rec.get("answer", 0)) - 1
    ans_letter = LETTERS[ans_idx] if 0 <= ans_idx < len(LETTERS) else "A"
    vignette = (rec.get("vignette") or "").strip()
    question = (rec.get("question") or "").strip()
    expl = rec.get("explanation") or {}

    meta = {
        "id": new_id, "type": "kmle", "topic": topic,
        "source": rec.get("source", "KMLE 2026"), "confidence": "high",
        "date": "2026-07-01",   # 레거시(과거) — '오늘의 문항'에 안 뜨게 today 이전 날짜
        "stem": (vignette + " " + question).strip(),
        "choices": [f"{LETTERS[i]}. {o}" for i, o in enumerate(options)],
        "answer": ans_letter, "answer_separated": True,
        "explanation": expl.get("정답근거") or expl.get("진단") or "",
        "difficulty": 3,
    }
    if rec.get("appendix"):
        meta["appendix"] = rec["appendix"]

    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=100000)

    opt_lines = "\n".join(f"- {LETTERS[i]}. {o}" for i, o in enumerate(options))
    expl_lines = []
    for k in EXPL_ORDER:
        if expl.get(k):
            expl_lines.append(f"- **{k}**: {expl[k]}")
    if rec.get("source"):
        expl_lines.append(f"- **출처**: {rec['source']}")

    body = (
        f"## 문제\n{vignette}\n\n{question}\n\n{opt_lines}\n\n"
        f"## 정답 및 해설\n> 정답: {ans_letter}\n\n" + "\n".join(expl_lines) + "\n"
    )
    return f"---\n{fm}---\n\n{body}"


def main() -> int:
    recs = load_legacy()
    recs.sort(key=lambda r: str(r.get("id", "")))   # 결정론적 순서
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_subject: dict[str, int] = {}
    for rec in recs:
        new_id = next_id("kmle")
        (OUT_DIR / f"{new_id}.md").write_text(to_md(rec, new_id), encoding="utf-8")
        topic = SUBJECT_MAP.get(rec.get("subject", ""), rec.get("subject", ""))
        record_topic("kmle", f"[legacy] {topic} - {rec.get('id')}", "2026-07-01")
        by_subject[topic] = by_subject.get(topic, 0) + 1
    print(f"이관 완료: {len(recs)}문항 → {OUT_DIR.relative_to(ROOT)}")
    for k, v in sorted(by_subject.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

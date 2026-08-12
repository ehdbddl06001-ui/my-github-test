"""
frontmatter.py — 모든 .md 파일 최상단의 YAML frontmatter를 읽고 검증한다.

이 파일이 Markdown(사람용)과 SQLite(기계용)를 잇는 '계약(contract)'이다.
indexer.py 는 여기서 파싱한 결과만 신뢰한다. 규격은 schemas/frontmatter.md 참조.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "PyYAML이 필요합니다. `uv pip install pyyaml` 또는 `pip install pyyaml`\n"
    )
    raise

# 모든 문서에 필수인 필드
REQUIRED_COMMON = ["id", "type", "topic", "date", "confidence"]
# 문제형(kmle/usmle) 문서에 추가로 필수인 필드
REQUIRED_QUESTION = ["stem", "choices", "answer"]
VALID_TYPES = {"kmle", "usmle", "basic", "paper", "disease", "drug", "ailab", "anatomy"}
VALID_CONFIDENCE = {"high", "medium", "low"}
QUESTION_TYPES = {"kmle", "usmle"}
# USMLE는 웹/CLI 퀴즈에서 Step·과목으로 분류되므로 아래 두 필드를 추가로 요구한다.
REQUIRED_USMLE = ["step", "exam_subject"]
VALID_STEP = {"Step 1", "Step 2"}

# ── 해부학(anatomy) 계약 — spec: experiments/specs/anatomy-3q-2026.md ──────
# kind별 계약이 다르다. source_page/question은 출처(provenance)를 강제한다.
ANATOMY_KINDS = {
    "source_doc",    # Drive 원본 파일 1개의 inventory 카드(파일ID·해시·처리상태)
    "source_page",   # PDF 한 페이지(또는 text-lane 섹션)의 출처·분류·용어 목록
    "concept",       # 층/분지/주행/공간/인접관계 학습 카드
    "question",      # 태깅·순서·관계·분지·경로 문항
    "daily_plan",    # 그날의 학습 큐(결정론 선택 결과)
    "answer_list",   # 답만 있는 자료(tagging 2차)의 파싱 결과
    "study_guide",   # 회차 범위 전체를 다루는 종합 학습 정리(근육표·관계도·임상 포인트)
}
ANATOMY_REGIONS = {
    "back", "thorax", "upper-limb", "lower-limb", "head", "neck",
    "abdomen", "pelvis-perineum", "multi",
}
ANATOMY_QUESTION_STYLES = {
    "spotter", "layer-order", "branch-tree", "course-tracing",
    "relation", "clinical-application", "distinction",
}
ANATOMY_EXAM_PHASES = {"tagging-1", "tagging-2"}


def _validate_anatomy(meta: dict[str, Any], errors: list[str]) -> None:
    kind = meta.get("kind")
    if kind not in ANATOMY_KINDS:
        errors.append(f"anatomy kind 값 오류: {kind} (허용: {sorted(ANATOMY_KINDS)})")
        return

    region = meta.get("region")
    if region and region not in ANATOMY_REGIONS:
        errors.append(f"anatomy region 값 오류: {region} (허용: {sorted(ANATOMY_REGIONS)})")
    phase = meta.get("exam_phase")
    if phase and phase not in ANATOMY_EXAM_PHASES:
        errors.append(f"anatomy exam_phase 값 오류: {phase}")

    # 공개 게이트: publishable은 명시된 true만 참(안전 기본값 false).
    if "publishable" in meta and not isinstance(meta["publishable"], bool):
        errors.append("anatomy publishable 은 boolean 이어야 함(기본 false)")

    if kind in {"source_page", "source_doc", "answer_list"}:
        if not meta.get("source_file_id"):
            errors.append(f"anatomy {kind} 필수 필드 누락: source_file_id")
    if kind == "source_page":
        # binary lane은 페이지 번호, text lane은 extraction 마커+section이 필수.
        page = meta.get("source_page")
        if page is None and meta.get("extraction") != "drive-mcp-text":
            errors.append(
                "anatomy source_page: source_page(번호) 또는 "
                "extraction: drive-mcp-text(+section)를 명시해야 함"
            )
        if page is None and not meta.get("section"):
            errors.append("anatomy source_page(text-lane): section 필수")

    if kind in {"concept", "question", "study_guide"}:
        refs = meta.get("source_refs")
        if not refs or not isinstance(refs, list):
            errors.append(f"anatomy {kind} 필수 필드 누락: source_refs (리스트)")
        else:
            for r in refs:
                if not isinstance(r, dict) or not r.get("source_file_id"):
                    errors.append("anatomy source_refs 항목에 source_file_id 필요")
                    break

    if kind == "question":
        if meta.get("answer_separated") is not True:
            errors.append("anatomy question: answer_separated: true 필수(정답 분리 원칙)")
        if not meta.get("answer"):
            errors.append("anatomy question 필수 필드 누락: answer")
        if not meta.get("stem"):
            errors.append("anatomy question 필수 필드 누락: stem")
        style = meta.get("question_style")
        if style not in ANATOMY_QUESTION_STYLES:
            errors.append(
                f"anatomy question_style 값 오류: {style} "
                f"(허용: {sorted(ANATOMY_QUESTION_STYLES)})"
            )
        # 객관식이면 choices는 리스트, 자유응답형이면 생략 가능.
        if "choices" in meta and meta["choices"] is not None \
                and not isinstance(meta["choices"], list):
            errors.append("anatomy question choices 는 리스트여야 함")
        # 정답 문자열이 stem에 그대로 노출되지 않아야 한다(최소 누설 검사).
        ans, stem = str(meta.get("answer", "")), str(meta.get("stem", ""))
        if ans and len(ans) > 1 and not meta.get("choices") and ans in stem:
            errors.append("anatomy question: 정답 문자열이 stem에 노출됨")


@dataclass
class Doc:
    """파싱된 문서 하나. frontmatter(meta) + 본문(body) + 파일 경로."""

    path: Path
    meta: dict[str, Any]
    body: str
    errors: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @property
    def type(self) -> str:
        return str(self.meta.get("type", ""))

    @property
    def is_question(self) -> bool:
        return self.type in QUESTION_TYPES


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """'---'로 감싼 YAML 블록과 나머지 본문을 분리한다."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    if not isinstance(meta, dict):
        return {}, text
    return meta, body


def validate(meta: dict[str, Any]) -> list[str]:
    """필수 필드/값 검증. 문제가 있으면 에러 메시지 리스트를 돌려준다."""
    errors: list[str] = []
    for k in REQUIRED_COMMON:
        if k not in meta or meta[k] in (None, ""):
            errors.append(f"필수 필드 누락: {k}")

    t = meta.get("type")
    if t and t not in VALID_TYPES:
        errors.append(f"type 값 오류: {t} (허용: {sorted(VALID_TYPES)})")

    c = meta.get("confidence")
    if c and c not in VALID_CONFIDENCE:
        errors.append(f"confidence 값 오류: {c} (허용: high/medium/low)")

    if t in QUESTION_TYPES:
        for k in REQUIRED_QUESTION:
            if k not in meta or meta[k] in (None, "", []):
                errors.append(f"문제형 필수 필드 누락: {k}")
        if "choices" in meta and not isinstance(meta["choices"], list):
            errors.append("choices 는 리스트여야 함")
        # 정답이 stem 텍스트 안에 섞여 들어가지 않았는지 최소 확인
        if meta.get("answer_separated") is not True:
            errors.append("answer_separated: true 를 명시해야 함(정답 분리 원칙)")

    if t == "usmle":
        for k in REQUIRED_USMLE:
            if k not in meta or meta[k] in (None, ""):
                errors.append(f"USMLE 필수 필드 누락: {k} (Step 필터·과목 분류용)")
        s = meta.get("step")
        if s and s not in VALID_STEP:
            errors.append(f"step 값 오류: {s} (허용: 'Step 1' / 'Step 2')")

    if t == "anatomy":
        _validate_anatomy(meta, errors)
    return errors


def load(path: str | Path) -> Doc:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    doc = Doc(path=p, meta=meta, body=body)
    doc.errors = validate(meta)
    return doc


if __name__ == "__main__":
    # 단독 실행 시: 인자로 받은 파일들을 검증만 한다.
    exit_code = 0
    for arg in sys.argv[1:]:
        d = load(arg)
        if d.errors:
            exit_code = 1
            print(f"[FAIL] {arg}")
            for e in d.errors:
                print(f"       - {e}")
        else:
            print(f"[ OK ] {arg}  ({d.type} / {d.id})")
    sys.exit(exit_code)

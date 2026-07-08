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
VALID_TYPES = {"kmle", "usmle", "basic", "paper", "disease", "drug", "ailab"}
VALID_CONFIDENCE = {"high", "medium", "low"}
QUESTION_TYPES = {"kmle", "usmle"}
# USMLE는 웹/CLI 퀴즈에서 Step·과목으로 분류되므로 아래 두 필드를 추가로 요구한다.
REQUIRED_USMLE = ["step", "exam_subject"]
VALID_STEP = {"Step 1", "Step 2"}


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

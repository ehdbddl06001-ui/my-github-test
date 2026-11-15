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
VALID_TYPES = {"kmle", "usmle", "basic", "paper", "disease", "drug", "ailab", "imaging", "concept"}
# concept = 학습 목표 단위 개념 정리본(content/concepts/). 세부 계약은 pipelines/concepts.py 가 본다.
VALID_CONFIDENCE = {"high", "medium", "low"}
# imaging = 오픈데이터 실제 영상(ECG·CT·피부·병리·CTG) 문항. 의대_시험지_제작 아침 루틴이
# 만든 세트를 medkos_export 가 카드로 옮긴다. 문제형 계약(stem/choices/answer)을 그대로 따른다.
QUESTION_TYPES = {"kmle", "usmle", "imaging"}
# imaging 은 국시형/USMLE형 중 어느 형식으로 냈는지(style)와 영상 출처(figure)를 요구한다.
REQUIRED_IMAGING = ["style"]
VALID_IMAGING_STYLE = {"kmle_style", "usmle_style"}
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
        # 출제 설계(선택 필드) — 계약은 「있으면 사전」까지만. 내용 형식은 lint_questions.py(question_design.py)가 본다.
        if "design" in meta and meta["design"] is not None and not isinstance(meta["design"], dict):
            errors.append("design 은 사전(dict)이어야 함 — schemas/frontmatter.md 문제형 선택 필드 참고")
        rs = meta.get("review_status")
        if rs is not None and rs not in ("unreviewed", "reviewed", "needs_revision"):
            errors.append(f"review_status 값 오류: {rs} (허용: unreviewed/reviewed/needs_revision)")

    if t == "usmle":
        for k in REQUIRED_USMLE:
            if k not in meta or meta[k] in (None, ""):
                errors.append(f"USMLE 필수 필드 누락: {k} (Step 필터·과목 분류용)")
        s = meta.get("step")
        if s and s not in VALID_STEP:
            errors.append(f"step 값 오류: {s} (허용: 'Step 1' / 'Step 2')")

    if t == "imaging":
        for k in REQUIRED_IMAGING:
            if k not in meta or meta[k] in (None, ""):
                errors.append(f"imaging 필수 필드 누락: {k} (kmle_style/usmle_style)")
        st = meta.get("style")
        if st and st not in VALID_IMAGING_STYLE:
            errors.append(f"imaging style 값 오류: {st} (허용: kmle_style/usmle_style)")
        fig = meta.get("figure")
        if fig is not None and not isinstance(fig, dict):
            errors.append("imaging figure 는 맵이어야 함({type: image, src, caption})")
        if isinstance(fig, dict) and fig.get("type") == "image" and not fig.get("src"):
            errors.append("imaging figure.src 누락(docs/ 기준 상대경로)")

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

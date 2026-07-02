"""
indexer.py — content/ 의 모든 .md 를 읽어 SQLite 색인을 (재)빌드한다.

핵심 원칙: Markdown이 원본, SQLite는 파생물.
  - 기본(--rebuild): DB를 지우고 content/ 전체로 새로 만든다. (ephemeral 컨테이너에 안전)
  - --file <경로>: 해당 파일 하나만 upsert (로컬 편집 시 빠른 갱신)
  - --check: 색인하지 않고 frontmatter 검증만. 에러 있으면 exit code 1.

사용 예:
  python pipelines/indexer.py                 # 전체 재빌드
  python pipelines/indexer.py --file content/kmle/2026/kmle-2026-0001.md
  python pipelines/indexer.py --check         # CI/커밋 전 검증
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from frontmatter import Doc, load

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DB_PATH = ROOT / "db" / "medkos.sqlite"
SCHEMA_PATH = Path(__file__).resolve().parent / "db_schema.sql"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    # FTS5: trigram(한글 부분검색에 유리)을 우선 시도, 안 되면 unicode61로 폴백.
    try:
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts "
            "USING fts5(id UNINDEXED, title, body, tokenize='trigram')"
        )
    except sqlite3.OperationalError:
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts "
            "USING fts5(id UNINDEXED, title, body)"
        )
    conn.commit()


def iter_docs() -> list[Doc]:
    return [load(p) for p in sorted(CONTENT_DIR.rglob("*.md"))]


def _s(v) -> str | None:
    """YAML이 date/int 등으로 파싱한 값을 안전하게 문자열로. (None은 그대로)"""
    return None if v is None else str(v)


def upsert_doc(conn: sqlite3.Connection, d: Doc) -> None:
    m = d.meta
    rel = str(d.path.relative_to(ROOT))
    conn.execute("DELETE FROM documents WHERE id = ?", (d.id,))
    conn.execute("DELETE FROM docs_fts WHERE id = ?", (d.id,))
    conn.execute(
        """INSERT INTO documents
           (id, type, topic, subtopic, filepath, source, edition,
            confidence, created_date, updated_date)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (
            d.id, d.type, m.get("topic"), m.get("subtopic"), rel,
            m.get("source"), m.get("edition"), m.get("confidence"),
            _s(m.get("date")), _s(m.get("updated", m.get("date"))),
        ),
    )

    if d.is_question:
        conn.execute(
            """INSERT INTO questions
               (id, doc_id, stem, choices, answer, explanation, difficulty)
               VALUES (?,?,?,?,?,?,?)""",
            (
                d.id, d.id, m.get("stem"),
                json.dumps(m.get("choices", []), ensure_ascii=False),
                str(m.get("answer")), m.get("explanation"),
                m.get("difficulty"),
            ),
        )

    # 태그
    for tag in m.get("tags", []) or []:
        conn.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (str(tag),))
        row = conn.execute("SELECT id FROM tags WHERE name = ?", (str(tag),)).fetchone()
        conn.execute(
            "INSERT OR IGNORE INTO document_tags(doc_id, tag_id) VALUES (?,?)",
            (d.id, row[0]),
        )

    # 관계(related)
    conn.execute("DELETE FROM relations WHERE src_id = ?", (d.id,))
    for dst in m.get("related", []) or []:
        conn.execute(
            "INSERT OR IGNORE INTO relations(src_id, dst_id) VALUES (?,?)",
            (d.id, str(dst)),
        )

    # 전문검색 인덱스: 제목(topic/subtopic) + 본문 + 문제 텍스트
    title = " ".join(filter(None, [m.get("topic"), m.get("subtopic")]))
    fts_body = d.body
    if d.is_question:
        fts_body = "\n".join(
            filter(None, [
                m.get("stem", ""),
                " ".join(str(c) for c in m.get("choices", [])),
                m.get("explanation", ""),
            ])
        )
    conn.execute(
        "INSERT INTO docs_fts(id, title, body) VALUES (?,?,?)",
        (d.id, title, fts_body),
    )


def rebuild() -> int:
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = connect()
    ensure_schema(conn)
    docs = iter_docs()
    ok, failed = 0, 0
    for d in docs:
        if d.errors:
            failed += 1
            print(f"[SKIP] {d.path}")
            for e in d.errors:
                print(f"       - {e}")
            continue
        upsert_doc(conn, d)
        ok += 1
    conn.commit()
    conn.close()
    print(f"\n색인 완료: {ok}개 성공, {failed}개 실패(검증 오류로 제외)")
    return 1 if failed else 0


def index_one(path: str) -> int:
    d = load(path)
    if d.errors:
        print(f"[FAIL] {path}")
        for e in d.errors:
            print(f"       - {e}")
        return 1
    conn = connect()
    ensure_schema(conn)
    upsert_doc(conn, d)
    conn.commit()
    conn.close()
    print(f"[ OK ] {path} 색인됨 ({d.type} / {d.id})")
    return 0


def check_only() -> int:
    failed = 0
    for d in iter_docs():
        if d.errors:
            failed += 1
            print(f"[FAIL] {d.path}")
            for e in d.errors:
                print(f"       - {e}")
    if failed:
        print(f"\n검증 실패 {failed}건 — 커밋 전 수정 필요")
        return 1
    print("frontmatter 검증 통과")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="단일 파일만 색인")
    ap.add_argument("--check", action="store_true", help="검증만(색인 안 함)")
    args = ap.parse_args()
    if args.check:
        return check_only()
    if args.file:
        return index_one(args.file)
    return rebuild()


if __name__ == "__main__":
    sys.exit(main())

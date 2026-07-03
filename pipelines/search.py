"""
search.py — SQLite(FTS5) 색인을 실제로 조회하는 CLI. 색인의 '첫 소비자'.

MedKOS 원칙: Markdown이 원본, SQLite는 그 원본에서 언제든 재빌드되는 색인이다.
그동안 indexer.py 가 색인을 '만들'기만 하고 '쓰'는 곳이 없었다. 이 파일이 그 색인을
꺼내 쓴다 — 전문검색(FTS5) + 타입/주제/태그 필터 + 대시보드(--stats).

db/medkos.sqlite 는 .gitignore(파생물)라 없을 수 있다. 없으면 자동으로 재빌드한다.
(임시 컨테이너에서도 안전 — content/ 만 있으면 언제든 색인을 다시 만든다.)

사용 예:
  python pipelines/search.py 심부전                 # 전문검색
  python pipelines/search.py SGLT2 --type kmle       # KMLE 안에서만
  python pipelines/search.py --topic Cardiology      # 검색어 없이 주제 필터
  python pipelines/search.py --tag HFrEF             # 태그로
  python pipelines/search.py --stats                 # 대시보드(무엇이 얼마나 쌓였나)
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "medkos.sqlite"

# ANSI 색 (터미널이 아니면 자동으로 비활성)
_C = sys.stdout.isatty()
def _dim(s: str) -> str:  return f"\033[2m{s}\033[0m" if _C else s
def _bold(s: str) -> str: return f"\033[1m{s}\033[0m" if _C else s
def _cyan(s: str) -> str: return f"\033[36m{s}\033[0m" if _C else s


def _ensure_db() -> None:
    """색인이 없으면(파생물이므로 흔한 일) content/ 에서 재빌드한다."""
    if DB_PATH.exists():
        return
    print(_dim("색인이 없어 content/ 에서 재빌드합니다…"), file=sys.stderr)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import indexer  # noqa: E402  (같은 폴더)
    indexer.rebuild()


def connect() -> sqlite3.Connection:
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _fts_ok(conn: sqlite3.Connection, query: str) -> bool:
    try:
        conn.execute("SELECT id FROM docs_fts WHERE docs_fts MATCH ? LIMIT 1", (query,))
        return True
    except sqlite3.OperationalError:
        return False


def search(conn: sqlite3.Connection, query: str | None, doc_type: str | None,
           topic: str | None, tag: str | None, limit: int) -> list[sqlite3.Row]:
    """검색어(FTS) + 필터를 조합해 documents 를 조회한다."""
    where: list[str] = []
    params: list[object] = []
    join = ""

    if query:
        # FTS5 는 부분어에 접두 매칭(*)을 붙여 재현율을 높인다.
        fts_query = " ".join(f'{tok}*' for tok in query.split())
        ids = [r[0] for r in conn.execute(
            "SELECT id FROM docs_fts WHERE docs_fts MATCH ?", (fts_query,)
        ).fetchall()] if _fts_ok(conn, fts_query) else []
        if not ids:
            return []
        where.append(f"d.id IN ({','.join('?' * len(ids))})")
        params.extend(ids)

    if doc_type:
        where.append("d.type = ?"); params.append(doc_type)
    if topic:
        where.append("d.topic LIKE ?"); params.append(f"%{topic}%")
    if tag:
        join = ("JOIN document_tags dt ON dt.doc_id = d.id "
                "JOIN tags t ON t.id = dt.tag_id")
        where.append("t.name LIKE ?"); params.append(f"%{tag}%")

    sql = (
        "SELECT DISTINCT d.id, d.type, d.topic, d.subtopic, d.filepath, "
        "d.confidence, d.created_date "
        f"FROM documents d {join} "
        + ("WHERE " + " AND ".join(where) if where else "")
        + " ORDER BY d.type, d.created_date DESC, d.id LIMIT ?"
    )
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def print_results(rows: list[sqlite3.Row]) -> None:
    if not rows:
        print("결과 없음.")
        return
    print(f"\n{_bold(str(len(rows)) + '건')}\n")
    for r in rows:
        head = f"{_cyan(r['id'])}  {_bold(r['topic'] or '?')}"
        if r["subtopic"]:
            head += _dim(f" / {r['subtopic']}")
        print(head)
        meta = f"[{r['type']}] confidence={r['confidence']}"
        if r["created_date"]:
            meta += f" · {r['created_date']}"
        print("  " + _dim(meta))
        print("  " + _dim(r["filepath"]))
        print()


def print_stats(conn: sqlite3.Connection) -> None:
    """대시보드 — 무엇이 얼마나 쌓였나(색인이 보여주는 자산 현황)."""
    total = conn.execute("SELECT count(*) FROM documents").fetchone()[0]
    print(_bold(f"\n📊 MedKOS 대시보드 — 총 {total}개 문서\n"))

    print(_bold("타입별"))
    for r in conn.execute(
        "SELECT type, count(*) n FROM documents GROUP BY type ORDER BY n DESC"
    ):
        bar = "█" * min(r["n"], 40)
        print(f"  {r['type']:<8} {r['n']:>4}  {_cyan(bar)}")

    print(_bold("\n주제 상위 12"))
    for r in conn.execute(
        "SELECT topic, count(*) n FROM documents "
        "GROUP BY topic ORDER BY n DESC, topic LIMIT 12"
    ):
        print(f"  {r['n']:>4}  {r['topic']}")

    print(_bold("\n신뢰도(confidence)"))
    for r in conn.execute(
        "SELECT confidence, count(*) n FROM documents "
        "GROUP BY confidence ORDER BY n DESC"
    ):
        print(f"  {str(r['confidence']):<8} {r['n']:>4}")

    print(_bold("\n최근 추가 8개"))
    for r in conn.execute(
        "SELECT id, type, topic, created_date FROM documents "
        "ORDER BY created_date DESC, id DESC LIMIT 8"
    ):
        print(f"  {_dim(str(r['created_date']) or '-')}  {_cyan(r['id'])}  "
              f"[{r['type']}] {r['topic']}")

    tags = conn.execute("SELECT count(*) FROM tags").fetchone()[0]
    rels = conn.execute("SELECT count(*) FROM relations").fetchone()[0]
    print(_dim(f"\n태그 {tags}종 · 문서 연결(related) {rels}개"))
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description="MedKOS SQLite 색인 검색/대시보드")
    ap.add_argument("query", nargs="*", help="전문검색어(FTS5). 생략 가능")
    ap.add_argument("--type", dest="doc_type", help="kmle/usmle/basic/paper/disease/drug")
    ap.add_argument("--topic", help="주제(부분일치)")
    ap.add_argument("--tag", help="태그(부분일치)")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--stats", action="store_true", help="대시보드(검색 대신)")
    args = ap.parse_args()

    conn = connect()
    try:
        if args.stats:
            print_stats(conn)
            return 0
        query = " ".join(args.query).strip() or None
        if not (query or args.doc_type or args.topic or args.tag):
            ap.print_help()
            print("\n예: python pipelines/search.py 심부전 --type kmle")
            return 0
        rows = search(conn, query, args.doc_type, args.topic, args.tag, args.limit)
        print_results(rows)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())

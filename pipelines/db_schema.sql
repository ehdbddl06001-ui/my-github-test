-- db_schema.sql — 일반 테이블 정의.
-- FTS5 가상 테이블은 tokenizer 호환성 때문에 indexer.py에서 try/except로 생성한다.
-- SQLite는 Markdown의 '투영(projection)'일 뿐이며, content/ 에서 언제든 재빌드된다.

CREATE TABLE IF NOT EXISTS documents (
    id           TEXT PRIMARY KEY,
    type         TEXT NOT NULL,          -- kmle | usmle | basic | paper | disease | drug
    topic        TEXT NOT NULL,
    subtopic     TEXT,
    filepath     TEXT NOT NULL,
    source       TEXT,
    edition      TEXT,
    confidence   TEXT,                   -- high | medium | low
    created_date TEXT,
    updated_date TEXT
);

CREATE TABLE IF NOT EXISTS questions (
    id          TEXT PRIMARY KEY,
    doc_id      TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    stem        TEXT NOT NULL,
    choices     TEXT NOT NULL,           -- JSON 배열 문자열
    answer      TEXT NOT NULL,
    explanation TEXT,
    difficulty  INTEGER
);

CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS document_tags (
    doc_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (doc_id, tag_id)
);

-- related: 문서 간 연결(지식 그래프의 씨앗). 3단계에서 벡터 검색과 함께 확장.
CREATE TABLE IF NOT EXISTS relations (
    src_id TEXT NOT NULL,
    dst_id TEXT NOT NULL,
    PRIMARY KEY (src_id, dst_id)
);

CREATE INDEX IF NOT EXISTS idx_documents_type  ON documents(type);
CREATE INDEX IF NOT EXISTS idx_documents_topic ON documents(topic);
CREATE INDEX IF NOT EXISTS idx_questions_docid ON questions(doc_id);

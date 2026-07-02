---
name: index-db
description: content/ 의 Markdown을 SQLite로 재색인하거나 frontmatter를 검증한다. "색인 다시", "reindex", "DB 재빌드", "frontmatter 검증", "검색해줘" 요청에 트리거.
---

# 색인 / 검증 / 검색

SQLite는 Markdown의 파생물이다. 언제든 `content/`에서 재빌드된다.

## 명령
- 전체 재빌드: `python pipelines/indexer.py`
- 단일 파일:   `python pipelines/indexer.py --file <경로>`
- 검증만(커밋 전): `python pipelines/indexer.py --check`

## 검색 예시 (FTS5)
DB가 있으면 아래처럼 전문검색이 가능하다.
```sql
-- "심부전 SGLT2" 관련 문서
SELECT d.id, d.type, d.topic, d.subtopic
FROM docs_fts f JOIN documents d ON d.id = f.id
WHERE docs_fts MATCH 'SGLT2 OR 심부전'
ORDER BY rank LIMIT 20;
```
```sql
-- 특정 태그를 가진 KMLE 문제
SELECT d.id, d.subtopic FROM documents d
JOIN document_tags dt ON dt.doc_id = d.id
JOIN tags t ON t.id = dt.tag_id
WHERE d.type='kmle' AND t.name='SGLT2';
```

## 주의
- 검증에서 실패한 파일은 색인에서 제외된다. 커밋 전 반드시 `--check` 통과시킬 것.
- DB는 커밋하지 않는다. 필요하면 이 명령으로 언제든 다시 만든다.

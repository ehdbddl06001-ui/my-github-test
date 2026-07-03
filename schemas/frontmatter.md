# Frontmatter 규격 (Storage Contract)

MedKOS의 모든 `.md` 파일은 최상단에 `---` 로 감싼 YAML frontmatter를 가져야 한다.
이 규격이 Markdown(원본)과 SQLite(색인)를 잇는 유일한 계약이다.
`pipelines/frontmatter.py` 가 이 규격대로 검증한다.

## 공통 필수 필드 (모든 타입)

| 필드 | 예시 | 설명 |
|------|------|------|
| `id` | `kmle-2026-0142` | 전역 고유. `state.py`의 `next_id()`로 발급 |
| `type` | `kmle` | `kmle`/`usmle`/`basic`/`paper`/`disease`/`drug` 중 하나 |
| `topic` | `Cardiology` | 대주제(검색·연결의 기준) |
| `date` | `2026-07-02` | 생성일(ISO 8601) |
| `confidence` | `high` | `high`/`medium`/`low` — 출처 신뢰도 |

## 공통 선택 필드

| 필드 | 예시 | 설명 |
|------|------|------|
| `subtopic` | `Heart Failure` | 세부 주제 |
| `source` | `KMLE 2026 / Claude` | 어디서 왔는가 |
| `edition` | `Guyton 14e` | 교과서일 때 판(version) |
| `tags` | `[HFrEF, SGLT2]` | 태그(리스트) |
| `related` | `[drug-sglt2i]` | 연결된 다른 문서 id(지식 그래프 씨앗) |
| `updated` | `2026-07-10` | 마지막 수정일 |

## 논문(`paper`) 선택 필드 (스크랩)

`pipelines/scrape_papers.py`(PubMed 스크랩)가 아래 메타를 채운다. 전부 선택 필드지만,
있으면 `docs/papers.js`(홈페이지 논문 피드)와 원문 추적에 쓰인다.

| 필드 | 예시 | 설명 |
|------|------|------|
| `journal` | `Circulation` | 저널명 |
| `pmid` | `"40123456"` | PubMed ID(중복 방지 키, 문자열로 저장) |
| `doi` | `10.1056/…` | DOI |
| `authors` | `["Anker SD", …]` | 저자(최대 8 + et al.) |
| `url` | `https://pubmed.ncbi.nlm.nih.gov/…` | 원문 링크 |
| `pubdate` | `"2026-06-28"` | 저널 게재일 |

스크랩 카드는 사실 메타데이터 + 원문 초록만 담고 `confidence: medium`으로 둔다.
해석(Summary/Clinical Impact/My Ideas)은 이후 `/gen-paper`로 사람이 검수해 채운다.

## 문제형(`kmle`/`usmle`) 추가 필수 필드

| 필드 | 예시 | 설명 |
|------|------|------|
| `stem` | `62세 남성이 …` | 문제 지문(정답 힌트 포함 금지) |
| `choices` | `["A. …", "B. …"]` | 보기(리스트) |
| `answer` | `C` | 정답 |
| `answer_separated` | `true` | 정답이 stem과 분리됐음을 명시(필수) |

문제형 선택 필드: `explanation`(해설), `difficulty`(1~5 정수).

## USMLE(`usmle`) 추가 필수 필드

웹/CLI 퀴즈에서 Step·과목으로 나눠 풀 수 있도록 아래 두 필드를 반드시 넣는다.

| 필드 | 예시 | 설명 |
|------|------|------|
| `step` | `"Step 1"` | `"Step 1"`(기초의학) 또는 `"Step 2"`(임상) |
| `exam_subject` | `Pharmacology` | 퀴즈 과목 분류(아래 목록에서 하나) |

- Step 1 과목: Pharmacology, Immunology, Biochemistry, Microbiology, Pathology, Physiology
- Step 2 과목: Internal Medicine, Surgery, Neurology, Pediatrics, Obstetrics & Gynecology, Psychiatry
- 본문 `## 정답 및 해설` 섹션은 `pipelines/export_usmle_web.py`가 그대로 파싱해 웹/CLI
  해설로 쓴다. `- **키**: 값` 형식의 불릿을 유지한다.

## 원칙

1. **정답 분리**: `stem`에는 정답을 유추시키는 표현을 넣지 않는다. 정답·해설은
   `answer`/`explanation` 필드에만 둔다. `answer_separated: true`를 반드시 명시.
2. **출처 충돌 시**: 임의로 하나를 고르지 말고 `source`/`edition`/`date`를 남기고
   `confidence`를 낮춘다.
3. **id는 절대 재사용/역행 금지**: 항상 `state.next_id()`로만 발급.

## 최소 예시 (KMLE 문제)

```markdown
---
id: kmle-2026-0142
type: kmle
topic: Cardiology
subtopic: Heart Failure
source: "KMLE 2026 / Claude Routine"
confidence: high
date: 2026-07-02
tags: [HFrEF, SGLT2, GDMT]
related: [disease-heart-failure, drug-sglt2i]
stem: "62세 남성이 3개월간 악화된 호흡곤란으로 내원하였다. EF 30%. 다음 중 사망률 감소가 입증된 치료는?"
choices: ["A. 디곡신", "B. 다파글리플로진", "C. 아스피린", "D. 이뇨제 단독", "E. 칼슘차단제"]
answer: "B"
answer_separated: true
explanation: "HFrEF에서 SGLT2 억제제는 사망률·입원율 감소가 입증된 GDMT의 축이다."
difficulty: 3
---

## 문제
62세 남성이 3개월간 악화된 호흡곤란으로 내원하였다. EF 30%.
다음 중 사망률 감소가 입증된 치료는?

- A. 디곡신
- B. 다파글리플로진
- C. 아스피린
- D. 이뇨제 단독
- E. 칼슘차단제

## 정답 및 해설
> 정답은 별도 섹션. B — HFrEF에서 SGLT2 억제제는 GDMT의 핵심.
```

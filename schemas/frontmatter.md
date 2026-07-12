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

### 랜드마크(고인용) 논문 선택 필드

`pipelines/scrape_landmark_papers.py`가 파트별 '꼭 봐야 하는' 고인용 논문에 아래 메타를
채운다. 인용지표는 NIH iCite에서 온다. 있으면 `docs/papers.js`가 ⭐ 배지·인용순 정렬에 쓴다.

| 필드 | 예시 | 설명 |
|------|------|------|
| `landmark` | `true` | 파트별 고인용 랜드마크로 선정된 카드임을 표시 |
| `citations` | `1240` | 총 피인용수(iCite `citation_count`) |
| `rcr` | `18.70` | Relative Citation Ratio(분야·시기 정규화, 1.0=평균) |
| `nih_percentile` | `99.2` | NIH 기준 상위 백분위 |

랭킹은 결정론적으로 파이썬이 한다(인용수 우선, RCR로 tie-break). 카드 본문에는
선정 근거를 담는 `## Why must-read` 섹션이 추가되고, 나머지 골격은 스크랩 카드와 같다.
중복 판정은 스크랩과 같은 `state/seen_papers.json`(PMID)을 공유한다.

## AI/코딩 학습(`ailab`) 추가 선택 필드

의료 AI·코딩 공부용 카드(`type: ailab`). 공개 프로젝트(예: Keras 뇌종양 분할) 분석,
주간 실습 주제, 오픈 데이터 실습 노트를 **사람이 읽는 원본**으로 남긴다. 나머지 타입과
똑같이 공통 필수 필드(`id/type/topic/date/confidence`)를 갖고, 아래는 전부 선택이지만
있으면 `pipelines/export_ailab_web.py`(홈페이지 🤖 AI랩 피드)와 실습 링크에 쓰인다.

| 필드 | 예시 | 설명 |
|------|------|------|
| `kind` | `project` | 카드 성격: `project`(공개 프로젝트 분석)·`roadmap`(커리큘럼)·`weekly`(주간 실습)·`concept`(개념)·`mentor`(클로드와의 논의 노트)·`deepdive`(완료 주차 심화)·`log`(실제 실행 결과 로그) |
| `framework` | `Keras 3` | 사용 프레임워크/스택 (Keras·PyTorch·MONAI 등) |
| `arch` | `3D U-Net` | 모델 구조 이름 (U-Net·ResNet·ViT·Transformer 등) |
| `modality` | `brain-mri` | 데이터 양식 키 (`brain-mri`·`ecg`·`chest-xray`·`ct`·`path`·`derm`·`fundus`·`tabular`·`text`) |
| `level` | `beginner` | 난이도 (`beginner`·`intermediate`·`advanced`) |
| `project_url` | `https://keras.io/…` | 분석 대상 원본 프로젝트 링크 |
| `dataset` | `BraTS` | 사용 오픈 데이터셋 이름 (`pipelines/datasets.py`의 키와 맞춘다) |
| `dataset_url` | `https://…` | 데이터셋 접근 링크 |
| `colab_url` | `https://colab.research.google.com/…` | 바로 실습할 Colab 노트북 링크 |
| `notebook` | `notebooks/ailab_brain_tumor_segmentation.ipynb` | repo 안 노트북 경로(Colab이 GitHub에서 바로 연다) |
| `week` | `1` | 주간 실습이면 커리큘럼 주차(1~12). 멘토 노트는 ISO 주차(파일명용) |

본문 섹션 관례: `export_ailab_web.py`는 **모든 `## ` 섹션을 저작 순서대로** 담으므로 섹션
제목은 자유다(한국어 가능). 프로젝트/개념 카드 권장 골격은 `## Overview`(한눈에)·
`## Architecture`(구조 도식, Mermaid/ASCII)·`## Data`·`## Code walkthrough`·
`## Instructions`(지시어/프롬프트가 뭘 시키는지 해설)·`## Exercises`·`## Resources`.
`confidence`는 공식 문서 기반이면 `high`, 정리·해석이 섞이면 `medium`. 결정론적인 것(주차
선정·데이터셋 목록)은 `pipelines/datasets.py`가 맡고, 카드는 해석·학습 노트를 담는다.

**멘토(논의) 노트(`kind: mentor`)** — 클로드와 심화학습·코드보완·새기능을 토론하는 통로.
`content/ailab/mentor/mentor-YYYY-Www.md`에 쌓이며 섹션 골격은 `## Overview`·`## 심화 학습`·
`## 코드 보완`·`## 새 기능 아이디어`·`## 다음 주 추천`·`## 내 답변`(사용자가 채우는 빈칸,
왕복용)·`## Resources`. `/ai-mentor` 스킬이 생성하고, 홈페이지 🤖 AI랩 맨 위에 뜬다.

**심화 카드(`kind: deepdive`)** — 이미 통과(`check_week`)한 주차를 되돌아보며 깊이를 채우는
카드. `week`에 대상 주차, `related`에 원 실습 카드 id를 넣는다. 섹션 골격은 `## Overview` →
`## A.`(무엇을 했나) → `## B.`(구조·문제점) → `## C.`(다른 구조·대안) → `## D.`(모델 심화) →
`## E.`(자율학습 로드맵) → `## Architecture`(Mermaid) → `## Exercises`·`## Resources`·
`## My notes`. 대상 주차 선정(결정론)은 `pipelines/deepen.py`가 하고 `/deepen-week` 스킬이
생성한다. '이미 심화한 주차'는 별도 state가 아니라 이 카드들에서 역산한다(Source of Truth =
content). 홈페이지 🤖 AI랩에서 멘토 다음 우선순위로 뜬다.

**실행 로그 카드(`kind: log`)** — "내가 **실제로** 돌린 노트북의 결과"를 남기는 사실 기록.
클로드가 낡은 repo 노트북을 보고 **예측**하지 않도록, 실제 코드·수치의 Source of Truth를
repo에 박아두는 것이 목적이다. `content/ailab/logs/ailab-YYYY-NNNN.md`에 쌓이고, 결정론적으로
`pipelines/ingest_run.py`가 노트북이 남긴 `result.json`(또는 플래그)에서 생성한다(LLM이 수치를
지어내지 않는다). 아래 필드를 `frontmatter`에 담는다(전부 `type: ailab`, `kind: log`).

| 필드 | 예시 | 설명 |
|------|------|------|
| `week` | `1` | 어느 주차 실습의 실행인가 |
| `split` | `intra` | 데이터 분할 방식(`intra`=무작위/통과용 · `inter`=DS1/DS2 환자단위/실전) |
| `metric` | `macro_f1` | 채점 지표(커리큘럼 게이트와 같은 이름) |
| `value` | `0.8273` | 그 지표의 실측값 |
| `passed` | `true` | 게이트 통과 여부 |
| `notebook` | `notebooks/week01_ecg_1dcnn.ipynb` | **실제로 돌린** repo 안 노트북 경로(예측 방지의 핵심) |
| `checkpoint` | `drive:MedKOS/ailab/week01/week01_best.keras` | 베스트 가중치 위치(Drive는 파생물) |

`deepen.py`는 심화 대상 주차의 로그가 있으면 **glob 추정 대신 이 `notebook`·`value`를 그대로**
쓴다. 로그는 무거운 `.ipynb`를 대신하는 가벼운 요약이지만, 노트북 자체도 함께 커밋하면
클로드가 셀 단위로 실제 코드를 읽어 정확히 피드백할 수 있다(예측 0).

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
- **오답감별은 보기별 하위 불릿**으로 쓴다(한 줄에 A~E를 뭉치지 않는다). 파서가
  하위 불릿을 줄바꿈으로 보존하고 웹이 보기별로 줄을 나눠 렌더한다:
  ```
  - **오답감별**:
    - (A) …왜 틀렸는지…
    - (C) …
  ```
- 문항 품질(에포님 떠먹임 금지·활력징후 4종·동질적 보기·오답감별 letter 커버리지)은
  `pipelines/lint_questions.py`가 KMLE·USMLE 공통으로 기계 검증한다(커밋 전 ERROR 0).

## 구조화 임상 자료 & 해설 부록 (문제형 선택)

실제 시험처럼 **차트형 자료(활력징후·검사소견)**를 주고, 해설엔 **일반화 결정표**를
붙이기 위한 선택 필드. 웹 퀴즈가 이를 **박스**로 렌더한다(`app.js`의 `dataBox`·
`renderAppendix`). 영상의학 이미지는 다루지 않으므로, 필요한 이미지 소견은 `stem`에
텍스트로 기술하고 `confidence`를 조정한다.

| 필드 | 형태 | 설명 |
|------|------|------|
| `vitals` | 리스트 of `{name, value}` | 활력징후. 문제 상단 칩 박스로 렌더 |
| `labs` | 리스트 of `{name, value, ref}` | 검사 소견 표(항목/값/참고치). **정상 미끼값**을 일부러 섞어 신호·잡음 변별을 강제 |
| `appendix` | 맵 | 해설 부록. `가이드라인`(여러 줄 → 결정표 박스), `최신지견`(문자열), `참고문헌`(리스트) |
| `figure` | 맵 | 도형(파형). export가 **결정론적 SVG로 생성**해 문제 상단에 렌더. 현재 `type: ecg` 지원 |

```yaml
vitals:
  - {name: 혈압, value: "170/110 mmHg"}
labs:
  - {name: 혈소판, value: "90,000 /mm³", ref: "150,000–400,000"}   # 이상(핵심)
  - {name: AST, value: "35 U/L", ref: "< 40"}                      # 정상(미끼)
appendix:
  가이드라인: |
    (중증도 × 재태주수 × 태아상태 → 처치, 각주로 약물 factoring)
  최신지견: "핵심 한 줄."
  참고문헌: ["ACOG …", "Williams …"]
figure:                       # (1) 수식 합성 — 리듬형
  type: ecg
  rhythm: afib                # sinus·brady·tachy·afib·flutter·vtach·vfib·cavb·asystole
  rate: 112                   # 생략 시 리듬별 기본값
# 또는 (2) 실데이터 렌더 — 오픈 신호 DB
figure:
  type: ecg_signal
  source: assets/ecg/mitdb-100.json   # ingest_ecg.py 산출물
  lead: MLII
```

### `figure` (심전도) 규칙 — 매우 중요
- **type=ecg (수식 합성)**: `pipelines/gen_ecg_svg.py`가 수식으로 생성(AI 이미지
  아님). `rhythm`이 곧 정답이니 문항 정답과 **반드시 일치**시킨다.
  - 다룰 수 있는 것 = **리듬·간격·무질서형만**(위 rhythm 목록).
  - **금지 = 모양·ST·유도별 진단**(브루가다·STEMI·심막염 등): 12유도와 정확한 파형
    모양이 본질이라 합성하면 틀린 도형이 된다.
- **type=ecg_signal (실데이터·단일 유도)**: `assets/ecg/*.json`(오픈 DB 신호)을
  `render_signal_svg.py`로 렌더. **진짜 파형**이라 모양이 본질인 진단도 안전.
- **type=ecg12 (실데이터·12유도)**: PTB-XL 등 12유도 에셋을 표준 3×4 + 리듬 스트립으로
  렌더(`twelve_lead_svg`). **브루가다·STEMI·각차단 등 모양·유도별 진단은 이 경로로만**
  다룬다(합성 금지). 재배포 가능한 **오픈 라이선스만**, `source`·`참고문헌`에 출처 표기.
  새 레코드는 `pipelines/ingest_ecg.py`로 오프라인 1회 커밋(S3 미러는 assets/ecg/README).

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

# 루틴 프롬프트 — 오답 정리본 06:00·18:00 KST (매일)

Claude Routine `trig_01DzVed7kjfo6hLqyLQf1vaJ`(cron `0 9,21 * * *` UTC, 모델 claude-opus-5-5, env `env_01XNR87h8ALofRarp8hFnKR4`,
커넥터 Google Drive)의 입력 원문이다. **루틴을 고치면 이 파일도 같이 고친다**(이 파일이 원본). 세부 규칙은
`.claude/skills/gen-concept/SKILL.md` 가 원본이고, 여기에는 순서·예산·보고 형식만 둔다.

--------------------------------------------------------------------
내 오답의 이론 정리본을 채우고 해리슨으로 대조한다 — 매일 06:00·18:00 KST 발화(cron 0 9,21 * * * UTC). 저장소는 my-github-test(MedKOS).

왜 따로 있나: KMLE 루틴(월·수·금)·USMLE 루틴(화·목)도 같은 큐를 조금씩 처리하지만 주말 공백이 있고, 하루 수십 문항을 풀면 오답도 늘어난다. 이 루틴은 매일 두 번 큐를 비운다. 큐가 이미 비어 있으면 중복으로 쓰지 않는다.

0. 저장소 확보: `ls CLAUDE.md` 가 실패하면 `cd ~ && git clone https://github.com/ehdbddl06001-ui/my-github-test && cd my-github-test`(GITHUB_TOKEN 주입됨). 있으면 `git fetch origin main && git checkout main && git pull --ff-only origin main` — 폰 동기화 기록(state/learning_sync/events.json)이 main 에 있다.
1. 시작 시각을 적어 둔다: `TZ=Asia/Seoul date +%F\ %H:%M`. 항상 `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`. 먼저 `pip install -q -r requirements.txt`. 그리고 `.claude/skills/gen-concept/SKILL.md` 를 **처음부터 끝까지 읽는다**(판형 2·[restyle]·[variant]·[dist] 규칙이 거기 있다).
2. `python pipelines/concept_queue.py --limit 30`. 처리 순서는 [note]·[link] → [touch] → [variant] → [dist] → [restyle] → [gap].
   - 시간 예산: 시작 후 **50분**이 지나면 새 항목을 시작하지 않고 남은 수를 보고에 적는다(다음 실행이 이어서 한다). 개수 상한은 없다.
   - [note]·[link]: 큐 순서대로. 같은 학습 목표의 오답은 정리본 하나에 모은다. 새 정리본은 **판형 2(`note_form: 2`)** 로 쓰고, 그 목표의 틀린 문항마다 변형 둘도 함께 쓴다.
   - [touch]: 새 정리본을 쓰지 않는다 — 기존 혼동 항목의 `covers` 에 `<문항id>:<보기>` 를 더하거나 혼동 항목 하나를 추가. 본문을 고쳤으면 `version` 을 올리고 바꾼 서술만 4번 방식으로 대조. 판형 2가 아닌 정리본이면 이번에 판형 2로 옮겨도 된다(시간이 되면).
   - [variant]: 큐의 예정일 순서대로, 틀린 문항마다 flip: true 하나·flip: false 하나(SKILL 「[variant]」).
   - [dist]: 큐의 path 문항에 내가 고른 보기의 `distractors.<보기>` 하나를 더하고 문항 `version` 을 올린다. 해설과 모순되면 고치지 말고 보고에 남긴다.
   - [restyle]: 위 다섯이 모두 0일 때, **한 실행에 최대 2개**. 새로 쓰지 않고 있는 내용을 판형 2로 다시 배치한다(SKILL 「판형 2로 옮기기」, 본보기 `content/concepts/dermatology/cn.derm.pityriasis-versicolor.treatment.md`). 새 사실·수치·출처를 더하지 않는다. 도식 노드 id 는 바꾸지 않는다(문항 case_path 가 가리킨다).
   - [gap]: 위가 모두 0이고 **06시 실행일 때만** 1개. 18시 실행은 gap 을 쓰지 않는다.
3. 정리본 규칙(원문 SKILL):
   - 판형 2: summary 3~5줄에 「결론:」「시험 단서:」「왜:」 머리말, 틀린 보기별 pitfalls(covers), 기준·치료·감별은 표로 한 번만, 목표에 맞춘 본문 절(질환 교과서 골격을 채우지 않는다), 한국어(English) 용어 짝.
   - 도식 노드 글 판단 ≤ 30자·나머지 ≤ 40자·갈래 라벨 ≤ 14자. 조건 목록·용량·예외는 `diagram_notes` 나 표로. 배치는 코드가 정한다.
   - frontmatter `outline:` 슬롯 필수(`python pipelines/outline.py --find <말>` · `--book <과> --gaps`).
   - 시험 답이 갈릴 곳은 `## 시험 쟁점 — 충돌·맥락·새 근거` 절에 네 칸으로. `review_status: unreviewed`.
4. **해리슨 대조(기본)** — 정리본마다 `python pipelines/outline.py --harrison <슬롯>`:
   - 「드라이브 문서 <ID>」가 나오면 Google Drive 커넥터 `read_file_content` 로 **그 문서 하나만** 읽는다(`===== [H21 p.N] =====` 뒤가 인쇄쪽 N).
   - 맞는 서술에 `[[harrison-21: <장>장 p.<쪽>]]`, 출처 `harrison-21`(kind: textbook, verified: text, checked 에 확인한 것과 쪽). 다르면 고치거나 시험 쟁점 절에 밝힌다.
   - 「드라이브 문서 없음」이면 대조하지 않고 넘어간다. 「해리슨이 다루지 않는 자리」면 대상 아님.
   - 이 컨테이너는 PubMed·doi.org·NCBI 를 막는다. 못 연 출처는 `verified: citation` 과 사유를 적는다. PMID 를 알면 `pmid` 를 붙이고, 모르면 DOI 만 둔다(학습서 워크플로가 DOI 로 PMID 를 찾는다). 없는 출처·안 본 쪽수를 만들지 않는다.
5. 검증(오류 0 이어야 커밋): `python pipelines/concepts.py`(도식이 한 쪽에 안 들어가면 ERROR — 노드 글을 줄인다; 판형 2 정리본은 판형 WARN 도 0) → 목표·distractors 를 더한 문항이 있으면 `python pipelines/lint_questions.py <파일들>` → `python pipelines/outline.py`.
6. 게시: `python pipelines/publish.py -m "오답 정리본 <날짜 시각>: <무엇을>"`(콘텐츠 레인 → main). `state/concept_queue.json` 이 코드 레인으로 잡히면 `git checkout -- state/concept_queue.json` 뒤 다시 게시. 코드를 고쳐야 하면 고치지 말고 보고에 남긴다.
7. 조용한 무작업 종료 금지. 끝은 둘 중 하나 — (a) 커밋 해시 + 새 정리본(id·제목·슬롯·해리슨 대조: 쪽 / 문서 없음 / 대상 아님)·손질(id·더한 covers)·변형(정리본 id·문항 id·flip)·보기 설명(문항 id:보기)·판형 2로 옮긴 정리본(id) + 남은 큐 수, 또는 (b) 아무것도 만들지 않은 사유 한 문장을 첫 줄에. 보고는 한국어로, 폰 알림에서 바로 읽히게 결과·남은 큐·문제만. 새로 만들거나 손질했으면 PushNotification 으로 한 줄 요약.
--------------------------------------------------------------------

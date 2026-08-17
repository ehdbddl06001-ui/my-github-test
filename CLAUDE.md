# ecg-lab — ECG 부정맥 실험 저장소

MIT-BIH SVEB(상심실 이소성) 검출을 **정직한 inter-patient 세팅**에서 논문 수준까지
끌고 가는 실험 repo. 이 파일은 매 세션 자동 로드된다. 규칙은 여기에 두고, 과제
프롬프트는 얇게 유지한다.

원래 `ehdbddl06001-ui/my-github-test`(MedKOS) 안에 있던 실험 부분을 2026-08-17에
분리했다. 히스토리는 그대로 가져왔으므로 `git log`로 분리 이전 이력을 볼 수 있다.

## 이 repo의 범위

| 여기(ecg-lab) | 저기(my-github-test = MedKOS) |
|---|---|
| 실험 명세·실험 코드·실행 노트북·연구 결론 | 국시(KMLE/USMLE)·논문 카드·해부학·질환/약물 |
| `mit-bih/` `experiments/` `research/` `notebooks/` | `content/` `pipelines/` `docs/`(홈페이지) |
| 목적: **논문** | 목적: **학습 자산** |

AI 학습 트랙(`content/ailab/`, 주차 실습 카드, `kind: quest` 로드맵)은 **MedKOS에
남아 있다**. 저기가 "공부", 여기가 "연구"다. 퀘스트 카드가 여기 실험을 부르는 형태로
두 repo가 이어진다 — 한쪽 저장소에서 다른 쪽 파일을 만들지 않는다.

## 대원칙

- **실측만이 결과다.** 실행되지 않은/낡은 노트북에서 수치를 추론하지 않는다.
  숫자를 쓰려면 그 숫자가 나온 실행 산출물(`result.json`·실행된 노트북)을 근거로 댄다.
- **DS2로 절대 튜닝하지 않는다.** de Chazal DS1(22명) 학습 → DS2(22명) 테스트.
  모든 하이퍼파라미터는 DS1 클래스 카운트/공식에서 유도한다. DS2 라벨은 최종 평가에만.
- 주지표는 **S PR-AUC**(Average Precision). 환자단위 하위꼬리 실패와 매크로 지표를
  함께 보고한다. 벤치마크는 Farag(SVEB F1≈0.82).
- 환자 split·시드·환경·전처리·임계값 규칙·bootstrap 방법은 보존한다. 명세가 명시적으로
  바꾸지 않는 한 임의로 건드리지 않는다.
- 닫힌 아이디어를 새 근거·중단 규칙 없이 다시 시험하지 않는다.
- 없는 것을 추정으로 채우지 않는다. 측정 불가면 `측정 불가`로 남기고 원인을 적는다.
  (실측 사례: Q5-B-0 `B_SUBTYPE` — 조인 성공률 1.9%를 26% 부분집합으로 때우지 않고 종결)
- 가설이 틀렸으면 **철회한다.** 음성 결과도 `FINDINGS.md`·`PROJECT_STATE.md`에 남긴다.

## 저장 위치

- 실험 명세 → `experiments/specs/EXP-YYYY-NNN-<slug>.md` (양식: `TEMPLATE.md`)
- 실험 코드·회귀 테스트 → `mit-bih/` (`q*_*.py` / `test_q*_*.py` 짝)
- 실행 노트북 → `notebooks/questNN_<slug>.ipynb`, 실행본은 `notebooks/executed/`
- 연구 상태·인수인계 → `research/`
  · `PROJECT_STATE.md` — **현재 진실**. 각 실험의 판정과 다음 단계
  · `ASSETS.md` — Drive 자산 레지스트리(경로를 옮기기 전에 여기 먼저 등록)
  · `HANDOFF_<날짜>_<주제>_to_<수신자>.md` — 에이전트 간 과제 전달
- 작은 결과 요약 → `experiments/results/`
- 큰 산출물(체크포인트·npy·figure)은 **커밋하지 않는다** → Google Drive
  `MyDrive/MedKOS/ecg-model/` 에 두고 `research/ASSETS.md`에 경로만 등록한다.

## 작업 순서 (반드시 이 순서)

1. `CLAUDE.md`(이 파일) · `AGENTS.md` · `docs/AI_COLLABORATION.md` ·
   `research/PROJECT_STATE.md` · 배정된 명세를 읽는다.
2. 최신 `main`에서 시작한다 (`git fetch origin main && git switch main && git pull`).
3. 브랜치를 판다 — Claude Code는 `claude/<task>`, Codex는 `codex/<task>`,
   공용 정비는 `agent/<task>`. **두 에이전트가 같은 브랜치를 동시에 만지지 않는다.**
4. 명세가 `status: approved_for_implementation` 이고 `implementation_owner` 가
   나와 일치할 때만 구현을 시작한다. 아니면 멈추고 사용자에게 확인한다.
5. **acceptance criteria만** 구현한다. 과학적 질문·split·지표·중단 조건을 조용히
   바꾸지 않는다. 벗어난 판단은 명세의 Decision log에 남긴다.
6. 회귀 테스트를 돌린다(아래 「커밋 전 필수」).
7. GPU 실행은 **사용자가 Colab에서** 한다. 노트북이 Drive에 run bundle을 남긴다.
8. 실행된 노트북과 `result.json`을 커밋하고, 결과 해석은 PR/HANDOFF로 넘긴다.
9. 연구 결론·상태 변경은 PR 리뷰를 거친다.

## 커밋 전 필수

`mit-bih/test_*.py` 는 전부 **합성 데이터 자립형**이다 — 네트워크·Drive·실데이터가
필요 없다. 그러니 변명 없이 돌릴 수 있다. 단 라이브러리는 필요하다.

```bash
pip install -r requirements.txt
for t in mit-bih/test_*.py; do echo "== $t"; python3 "$t" || break; done
```

**"테스트가 깨졌다"고 결론 내리기 전에 `ModuleNotFoundError` 인지부터 본다.**
2026-08-17 실측(빈 컨테이너, 14개): 아무 것도 없으면 전부 죽고, numpy·scikit-learn·
scipy·matplotlib 만 넣으면 10개가 통과하며, 나머지 4개(`q4o`·`q4p`·`q4q`·
`svdb_rhythm`)는 **torch 가 있어야** 통과한다. 이건 실패가 아니라 환경 문제다.

건드린 모듈의 짝 테스트는 **반드시** 통과해야 한다. 실패를 남긴 채 PR을 열지 않는다.

`main` 직접 푸시는 하지 않는다 — 실험 코드는 전부 판단이 필요한 변경이다.
`claude/<task>` 브랜치 → PR → 리뷰 → **같은 세션에서 병합**. 열어 두고 끝내지 않는다.

## 금지

- 원시 ECG 데이터셋·체크포인트·비밀키·토큰·rclone 설정을 커밋하는 것.
- 정리 목적으로 Drive 기존 자산을 옮기는 것. 옛 노트북이 그 경로에 의존한다.
  먼저 `research/ASSETS.md`에 등록하고, 구경로·신경로·영향받는 소비자·롤백·검증을
  담은 **migration spec 승인 후에만** 옮긴다.
- 실행 안 된 노트북으로 결과를 말하는 것.
- 테스트 픽스처에 실데이터에서 뽑은 실측값을 박는 것 — 답을 외워서 통과할 수 있다.
- 읽기 전용으로 지정된 모듈(예: 인수검사 중인 동결 모듈) 수정.

## 에이전트 프롬프트

과제를 다른 에이전트에게 넘길 때는 `prompts/` 의 템플릿을 쓴다.
- `prompts/codex_task.md` — Codex에게 설계·리뷰·인수검사를 맡길 때
- `prompts/claude_task.md` — Claude Code에게 승인된 명세의 구현을 맡길 때

채운 프롬프트는 `research/HANDOFF_<날짜>_<주제>_to_<수신자>.md` 로 커밋해서
왕복 기록을 repo에 남긴다.

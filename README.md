# ecg-lab — MIT-BIH SVEB 검출 실험

정직한 **inter-patient** 세팅(de Chazal DS1 22명 학습 → DS2 22명 테스트)에서
상심실 이소성 박동(SVEB, S)을 검출하는 연구 저장소. 목표는 논문이다.

주지표는 **S PR-AUC**(Average Precision), 보조로 F1/PREC/SEN과 **환자단위 하위꼬리
실패**를 함께 본다. 벤치마크는 Farag(SVEB F1≈0.82).

> **철칙**: DS2로 절대 튜닝하지 않는다. DS2 라벨은 최종 평가에만 쓴다.
> 모든 하이퍼파라미터는 DS1 클래스 카운트/공식에서 유도한다.

## 어디부터 읽나

| 파일 | 내용 |
|---|---|
| `research/PROJECT_STATE.md` | ★ **현재 진실** — 각 실험의 판정과 다음 단계 |
| `mit-bih/PAPER.md` | 논문 형식 종합 보고서 — 정직한 성능·발견·음성결과 |
| `mit-bih/INDEX.md` | 전체 알고리즘 설계 인덱스(파일별 역할) |
| `mit-bih/FINDINGS.md` | 발견 요약(승리·실패·방법론) |
| `mit-bih/LARGESCALE_PLAN.md` | 대규모 DB 확장 계획(검정력·DB 비교·단계별 실행) |
| `CLAUDE.md` · `AGENTS.md` | 에이전트 운영 규칙 |
| `docs/AI_COLLABORATION.md` | Codex ↔ Claude Code 협업 워크플로 |

## 디렉터리

```
experiments/specs/   실험 명세 (EXP-YYYY-NNN-<slug>.md, 양식 TEMPLATE.md)
experiments/results/ 작은 결과 요약
mit-bih/             실험 코드 + 회귀 테스트 (q*_*.py / test_q*_*.py 짝)
notebooks/           Colab 실행 노트북 (questNN_*.ipynb), 실행본은 executed/
research/            PROJECT_STATE · ASSETS · HANDOFF 왕복 기록
prompts/             Codex·Claude Code 과제 프롬프트 템플릿
```

큰 산출물(체크포인트·npy·figure)은 커밋하지 않는다. Google Drive
`MyDrive/MedKOS/ecg-model/` 에 두고 `research/ASSETS.md` 에 경로만 등록한다.

## 테스트

`mit-bih/test_*.py` 는 전부 합성 데이터 자립형이다 — 네트워크·Drive·실데이터 불필요.

```bash
pip install -r requirements.txt
for t in mit-bih/test_*.py; do echo "== $t"; python3 "$t" || break; done
```

## 실험 한 바퀴

```
Codex 가 명세 작성 → 사용자 승인 → implementation_owner 가 브랜치에서 구현
  → 회귀 테스트 통과 → PR → 사용자가 Colab 에서 GPU 실행
  → 실행 노트북 + result.json 커밋 → Codex 리뷰 → PROJECT_STATE 갱신
```

브랜치는 `codex/<task>` · `claude/<task>` · `agent/<task>`. `main` 직접 푸시는 없다.
두 에이전트가 같은 브랜치를 동시에 만지지 않는다.

## 관련 저장소

학습 자산(국시·논문 카드·해부학·AI랩 공부 트랙)은
[`ehdbddl06001-ui/my-github-test`](https://github.com/ehdbddl06001-ui/my-github-test)(MedKOS)에 있다.
2026-08-17에 이 repo가 거기서 분리됐고, 분리 이전 히스토리는 여기 `git log`에 그대로 남아 있다.

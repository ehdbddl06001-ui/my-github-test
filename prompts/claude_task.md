# Claude Code 과제 프롬프트 템플릿

`research/HANDOFF_<날짜>_<주제>_to_claude.md` 로 복사해 채운 뒤 커밋하고,
아래 코드블록 안쪽만 Claude Code에 그대로 붙여넣는다.

머리말(파일 상단, 프롬프트 밖):

```
# Claude Code 과제 — <한 줄 제목>

작성: <YYYY-MM-DD> · 작성자: Codex · 수신: Claude Code
대상 명세: `experiments/specs/EXP-....md`
  (`status: approved_for_implementation` · `implementation_owner: claude`)
근거: <Codex 설계 / 직전 인수검사 판정 / run id>
```

---

## 프롬프트 본문 (Claude Code 에 그대로 전달)

```text
너는 Claude Code 다. repo: ehdbddl06001-ui/ecg-lab (ECG 실험 전용).
학습 콘텐츠(MedKOS)는 ehdbddl06001-ui/my-github-test 에 따로 있다.
이 과제에서 그쪽 repo 는 건드리지 마라.

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. research/PROJECT_STATE.md
3. experiments/specs/<명세>.md 전체 — 특히 acceptance criteria 와 Decision log
4. mit-bih/<대상 모듈>.py 와 mit-bih/test_<대상 모듈>.py
5. <읽기 전용 파일들> — 읽기 전용. 절대 수정하지 마라.

[시작 조건 — 하나라도 어긋나면 멈추고 사용자에게 물어라]
- 명세의 status 가 approved_for_implementation 인가
- implementation_owner 가 claude 인가
- 같은 파일을 만지는 codex/* 브랜치가 열려 있지 않은가

[네가 할 일]
1. git switch main && git pull origin main
2. git switch -c claude/<task>
3. acceptance criteria 만 구현한다. 변경 허용 파일: <목록>
4. 회귀 테스트를 추가/갱신한다. 픽스처는 합성 데이터만 — 실데이터 실측값을
   박지 마라(답을 외워서 통과할 수 있다).
5. 전체 테스트를 돌린다:
     for t in mit-bih/test_*.py; do echo "== $t"; python3 "$t" || break; done
6. 명세의 Decision log 에 벗어난 판단을 기록한다.
7. PR 을 열고, 본문에 실행한 테스트 명령과 결과를 그대로 붙인다.

[하지 마라]
- main 에 직접 푸시하지 마라.
- 과학적 질문·환자 split·지표·시드·중단 조건을 조용히 바꾸지 마라.
- GPU 학습을 돌리려 하지 마라 — 실행은 사용자가 Colab 에서 한다.
- 실행 안 된 노트북의 수치를 결과처럼 쓰지 마라.
- 원시 데이터셋·체크포인트·토큰·rclone 설정을 커밋하지 마라.
- Drive 자산 경로를 정리 목적으로 옮기지 마라(migration spec 필요).

[끝났을 때 보고할 것]
- 변경 파일 목록과 이유 한 줄씩
- 테스트 출력 그대로
- 명세 대비 미구현/보류 항목과 그 이유
```

---

## 응답 기록

구현 결과는 PR 링크와 함께 같은 파일 하단에 `## Claude Code 결과 <날짜>` 로 붙여 커밋한다.

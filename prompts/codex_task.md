# Codex 과제 프롬프트 템플릿

`research/HANDOFF_<날짜>_<주제>_to_codex.md` 로 복사해 채운 뒤 커밋하고,
아래 코드블록 안쪽만 Codex에 그대로 붙여넣는다.

머리말(파일 상단, 프롬프트 밖):

```
# Codex 과제 — <한 줄 제목>

작성: <YYYY-MM-DD> · 작성자: Claude Code · 수신: Codex
대상 명세: `experiments/specs/EXP-....md`
  (`status: ...` · `design_owner: ...` · `implementation_owner: ...`)
근거: PR #<번호> / run `<run_id>`
승인 체인상 위치: <예: 2차 인수검사(BLOCKED, 7 blocker) → 교정 구현 → Codex 3차 인수검사(지금) → 사용자 실행 승인>
```

---

## 프롬프트 본문 (Codex 에 그대로 전달)

```text
너는 Codex 다. repo: ehdbddl06001-ui/ecg-lab (ECG 실험 전용).
학습 콘텐츠(MedKOS)는 ehdbddl06001-ui/my-github-test 에 따로 있다.
이 과제에서 그쪽 repo 는 건드리지 마라.

[먼저 읽어라]
1. CLAUDE.md, AGENTS.md, docs/AI_COLLABORATION.md
2. research/PROJECT_STATE.md — 현재 판정과 다음 단계
3. experiments/specs/<명세>.md 전체. 특히 <acceptance criteria·Decision log 항목>
4. mit-bih/<대상 모듈>.py
5. mit-bih/test_<대상 모듈>.py
6. notebooks/<대상 노트북>.ipynb
7. <읽기 전용으로 지정할 파일> — 읽기 전용. 절대 수정하지 마라.
8. PR #<번호> 의 diff 전체

[네가 할 일]
<검토 / 설계 / 인수검사 중 하나를 명시. 예: "인수검사만 한다. 코드를 고치지 마라.">

[판정 형식]
각 blocker 마다: 근거 파일:줄 · 무엇이 명세와 어긋나는지 · 최소 수정안.
최종 한 줄 판정: ACCEPTED / IMPLEMENTATION_BLOCKED(blocker N건) / NEEDS_USER_DECISION

[하지 마라]
- 실행하지 마라(GPU 실행은 사용자가 Colab 에서 한다).
- 과학적 질문·split·지표·중단 조건을 임의로 바꾸지 마라. 바꿔야 하면
  Decision log 에 남길 제안으로만 적어라.
- 실행되지 않은 노트북에서 결과를 추론하지 마라.
- DS2 로 튜닝하는 변경을 승인하지 마라.
- 측정 불가한 값을 추정으로 채우는 구현을 통과시키지 마라.
```

---

## 응답 기록

Codex 응답은 같은 파일 하단에 `## Codex 응답 <날짜>` 로 붙여 커밋한다.

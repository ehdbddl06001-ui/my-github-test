# 루틴 프롬프트 — 해부학 일일 학습 (05:00 Asia/Seoul)

> 예약: **2026-08-13 ~ 2026-10-19, 매일 05:00 KST** (= cron `0 20 * * *` UTC).
> 종료 제어는 스케줄러가 아니라 코드가 한다 — 10-20부터 anatomy_daily.py가
> `completed`를 반환하고 스킬은 아무것도 만들지 않는다. 10-19 이후 이 루틴을
> 삭제해 달라고 사용자에게 알린다.

/anatomy-daily 를 실행하라.

- KST 오늘 날짜 기준으로 `.claude/skills/anatomy-daily/SKILL.md` 절차를 그대로 따른다.
- 규칙은 CLAUDE.md와 spec(experiments/specs/anatomy-3q-2026.md)에 있다. 이 프롬프트는
  얇게 유지한다.
- 완료 보고에는 phase, D-day, 생성 항목 id, needs_review 대기, Drive 변경 현황을 담는다.

# 루틴 프롬프트 — 해부학 일일 학습 (05:00 Asia/Seoul)

> 예약: **2026-08-13 ~ 2026-10-19, 매일 05:00 KST** (= cron `0 20 * * *` UTC).
> 종료 제어는 스케줄러가 아니라 코드가 한다 — 10-20부터 anatomy_daily.py가
> `completed`를 반환하고 스킬은 아무것도 만들지 않는다. 10-19 이후 이 루틴을
> 삭제해 달라고 사용자에게 알린다.

> 등록된 Routine: `anatomy-daily 05:00 KST (2026-08-13~10-19)`
> (`trig_0146ZhuKmgmQ5Xm6bqajN3Hq`, fresh session per fire, push 알림 on).
> 서버 스케줄러 지터로 실제 발화는 **05:00~05:15 KST** 사이다(예: 첫 발화 05:12).

/anatomy-daily 를 실행하라.

- **시각 기준은 KST**. 컨테이너는 UTC이므로 날짜는 `TZ=Asia/Seoul date +%F` 또는
  `anatomy_schedule.today_kst()` 로만 판단한다(UTC `date`를 쓰면 하루 밀린다).
- 우선순위: ① 회차 종합 학습정리(`kind: study_guide`) → ② 예습시험 문항 → ③ daily plan.
- KST 오늘 날짜 기준으로 `.claude/skills/anatomy-daily/SKILL.md` 절차를 그대로 따른다.
- 규칙은 CLAUDE.md와 spec(experiments/specs/anatomy-3q-2026.md)에 있다. 이 프롬프트는
  얇게 유지한다.
- 완료 보고에는 phase, D-day, 생성 항목 id, needs_review 대기, Drive 변경 현황을 담는다.

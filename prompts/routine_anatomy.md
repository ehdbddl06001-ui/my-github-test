# 루틴 프롬프트 — 해부학 일일 학습 (05:00 Asia/Seoul)

> 예약: **2026-08-13 ~ 2026-10-19, 매일 05:00 KST** (= cron `0 20 * * *` UTC).
> 종료 제어는 스케줄러가 아니라 코드가 한다 — 10-20부터 anatomy_daily.py가
> `completed`를 반환하고 스킬은 아무것도 만들지 않는다. 10-19 이후 이 루틴을
> 삭제해 달라고 사용자에게 알린다.

> 등록된 Routine: `anatomy-daily 05:00 KST (2026-08-13~10-19)`
> (`trig_0146ZhuKmgmQ5Xm6bqajN3Hq`, fresh session per fire, push 알림 on).
> 서버 스케줄러 지터로 실제 발화는 **05:00~05:15 KST** 사이다(예: 첫 발화 05:12).

> **알려진 함정(2026-08-14 실측, 2회 연속 빈손의 원인)**: 이 Routine은 meta-MCP로
> 만들어져 트리거 설정에 **git source가 없다** → 발화 세션의 작업 디렉터리가
> 비어 있다. "환경 문제"로 보고하고 끝내지 말고 **직접 클론해서 진행**한다
> (`GITHUB_TOKEN`·프록시는 주입돼 있다).

/anatomy-daily 를 실행하라.

- **0순위 — 저장소 확보**: `ls CLAUDE.md` 가 실패하면
  `cd ~ && git clone https://github.com/ehdbddl06001-ui/my-github-test && cd my-github-test`.
  클론까지 실패할 때만 실패로 보고한다.
- **시각 기준은 KST**. 컨테이너는 UTC이므로 날짜는 `TZ=Asia/Seoul date +%F` 또는
  `anatomy_schedule.today_kst()` 로만 판단한다(UTC `date`를 쓰면 하루 밀린다).
- **Drive는 선택 단계**다(루틴 컨테이너엔 MCP가 없다). 미접근이면 그 단계만 건너뛰고
  큐 계산·생성은 그대로 진행한다.
- **조용한 무작업 종료 금지**: 커밋/PR을 남기거나, 아무것도 안 만든 사유를 보고
  첫 줄에 한 문장으로 밝힌다. 만들 게 없으면 daily plan 카드라도 커밋한다.
- 우선순위: ① 회차 종합 학습정리(`kind: study_guide`) → ② 예습시험 문항 → ③ daily plan.
- KST 오늘 날짜 기준으로 `.claude/skills/anatomy-daily/SKILL.md` 절차를 그대로 따른다.
- 규칙은 CLAUDE.md와 spec(experiments/specs/anatomy-3q-2026.md)에 있다. 이 프롬프트는
  얇게 유지한다.
- 완료 보고에는 phase, D-day, 생성 항목 id, needs_review 대기, Drive 변경 현황을 담는다.

"""learning_log.py — 학습자 기록(오답 뒤 학습 흐름)의 병합과 상태 계산(결정론).

내용 상태(content/concepts — 정리본의 목표·출처·버전)와 **학습자 상태**(이 파일)를 섞지 않는다.

기록 원본
  - 브라우저 localStorage `medkos_learning_events` (docs/learn.js) — 덧붙이기만 한다.
  - `state/learning_sync/events.json` — Cloudflare 함수(/api/learning)나 이 스크립트가 합친 결과(사용자 데이터라 커밋).
  - `state/learning_inbox/*.json` — 앱의 「학습 기록 내보내기」 파일(드라이브 수신함에서 books.yml 이 가져옴).
병합은 사건 id(eid) 합집합이다. **기존 기록을 고치거나 지우지 않는다**(되풀이해도 결과가 같다 — 멱등).

상태 규칙(docs/learn.js 의 states() 와 같다 — 한쪽을 바꾸면 다른 쪽도, test_learning_books.py 가 같은 픽스처로 본다)
  - 열람(해설·정리본)은 학습의 증거가 아니다. 해설 열람 · 정리본 읽음 · 이해 표시 · 이후 적용 성공을 따로 둔다.
  - 복습 필요: 오답·표시가 있고 아직 능동적 후속 확인이 없다.
  - 복습 중: 인출 확인·같은 날 변형 문제·이해 표시 등 후속 활동이 있다.
  - 재확인 완료: 마지막 오답 **다음 날 이후** 같은 목표의 **다른 문항 또는 변형 문제**를 맞혔다. 이후 다시 틀리면 되돌아간다.
  - 우선순위 = 반복 오답·후속 확인 실패·표시. 고정된 「최적 간격」은 두지 않는다.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SYNC_FILE = ROOT / "state" / "learning_sync" / "events.json"
INBOX = ROOT / "state" / "learning_inbox"
FORMAT = "medkos-learning-events/1"
KINDS = {"answer", "view", "check", "understood", "later", "flag", "reason", "memo"}
STATUS = {"need": "복습 필요", "doing": "복습 중", "done": "재확인 완료"}
REASONS = {
    "missed_clue": "결정적 단서를 놓쳤다", "misread_clue": "단서의 의미를 다르게 해석했다",
    "two_options": "두 보기 사이에서 망설였다", "priority": "순서·우선순위가 헷갈렸다",
    "criteria": "기준·수치를 다르게 기억했다", "misread_q": "질문을 다르게 읽었다", "unsure": "확신 없이 골랐다",
}
FLAGS = {"guessed": "찍었다", "not_understood": "해설이 이해되지 않았다", "confused": "반복해서 헷갈린다",
         "want_note": "정리본으로 보고 싶다"}


def kst_day(t: str) -> str:
    try:
        dt = datetime.fromisoformat(str(t).replace("Z", "+00:00"))
    except ValueError:
        return ""
    return (dt.astimezone(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d")


def valid(e: Any) -> bool:
    return (isinstance(e, dict) and isinstance(e.get("eid"), str) and 0 < len(e["eid"]) <= 80
            and e.get("kind") in KINDS and isinstance(e.get("t"), str))


def read_events(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    evs = data if isinstance(data, list) else (data.get("events") if isinstance(data, dict) else None)
    return [e for e in (evs or []) if valid(e)]


def merge(base: list[dict], *incoming: list[dict]) -> tuple[list[dict], int]:
    """eid 합집합. base 의 기록은 그대로 두고 새 것만 덧붙인다. (합친 목록, 새로 붙은 수)."""
    seen = {e["eid"] for e in base}
    out = list(base)
    n = 0
    for evs in incoming:
        for e in evs:
            if valid(e) and e["eid"] not in seen:
                out.append(e); seen.add(e["eid"]); n += 1
    out.sort(key=lambda e: (str(e.get("t", "")), e["eid"]))
    return out, n


def sync_inbox(sync_file: Path = SYNC_FILE, inbox: Path = INBOX) -> int:
    """수신함 파일들을 events.json 에 합친다. 수신함 파일은 지우지 않는다(드라이브 원본도 건드리지 않음)."""
    base = read_events(sync_file) if sync_file.exists() else []
    files = sorted(inbox.glob("*.json")) if inbox.exists() else []
    merged, n = merge(base, *[read_events(p) for p in files])
    if n or not sync_file.exists():
        sync_file.parent.mkdir(parents=True, exist_ok=True)
        sync_file.write_text(json.dumps({"format": FORMAT, "events": merged}, ensure_ascii=False, indent=0),
                             encoding="utf-8", newline="\n")
    return n


@dataclass
class State:
    key: str
    objective: str | None
    qids: list[str] = field(default_factory=list)
    wrongs: int = 0
    wrong_qids: list[str] = field(default_factory=list)
    last_wrong_t: str = ""
    last_wrong_day: str = ""
    follow_fails: int = 0
    follow_ok: int = 0
    applied: bool = False
    applied_t: str = ""
    viewed_expl: bool = False
    viewed_note: bool = False
    understood: bool = False
    later: bool = False
    flags: dict[str, bool] = field(default_factory=dict)
    reasons: dict[str, int] = field(default_factory=dict)
    chosen: list[dict] = field(default_factory=list)       # 오답에서 고른 보기(반복 혼동)
    checks_ok: int = 0
    checks_miss: int = 0
    memo: str = ""
    memo_t: str = ""
    last_t: str = ""
    active: bool = False                                    # 마지막 오답 뒤 능동적 후속 활동
    status: str | None = None
    priority: int = 0

    def evidence(self) -> dict[str, bool]:
        return {"해설 열람": self.viewed_expl, "정리본 읽음": self.viewed_note,
                "이해 표시": self.understood, "이후 적용 성공": self.applied}


def states(events: list[dict]) -> dict[str, State]:
    S: dict[str, State] = {}
    for e in sorted(events, key=lambda e: (str(e.get("t", "")), e.get("eid", ""))):
        key = e.get("objective") or (f"q:{e['qid']}" if e.get("qid") else None)
        if not key:
            continue
        s = S.setdefault(key, State(key=key, objective=None if key.startswith("q:") else key))
        s.last_t = max(s.last_t, str(e.get("t", "")))
        day = e.get("day") or kst_day(e.get("t", ""))
        if e.get("qid") and e.get("mode") != "variant" and e["qid"] not in s.qids:
            s.qids.append(e["qid"])
        k = e.get("kind")
        if k == "answer":
            if not e.get("ok"):
                s.wrongs += 1
                if e.get("qid") not in s.wrong_qids:
                    s.wrong_qids.append(e.get("qid"))
                s.last_wrong_t, s.last_wrong_day = e["t"], day
                s.applied = False
                s.active = False
                if e.get("chosenText"):
                    s.chosen.append({"qid": e.get("qid"), "text": e["chosenText"], "answer": e.get("answerText", ""),
                                     "day": day, "mode": e.get("mode", "deck")})
                if s.wrongs > 1 or e.get("mode") == "variant":
                    s.follow_fails += 1
            elif s.wrongs:
                later = day > s.last_wrong_day
                other = e.get("mode") == "variant" or e.get("qid") not in s.wrong_qids
                if later and other:
                    s.applied, s.applied_t = True, e["t"]
                else:
                    s.follow_ok += 1
                    s.active = True
        elif k == "view":
            if e.get("what") == "explanation":
                s.viewed_expl = True
            if e.get("what") == "note":
                s.viewed_note = True
        elif k == "check":
            if e.get("result") == "ok":
                s.checks_ok += 1
                if s.wrongs:
                    s.follow_ok += 1
            else:
                s.checks_miss += 1; s.follow_fails += 1
            s.active = True
        elif k == "understood":
            s.understood = True
            s.active = True
        elif k == "later":
            s.later = True
        elif k == "flag":
            s.flags[str(e.get("flag"))] = bool(e.get("on"))
        elif k == "reason":
            for r in e.get("reasons") or []:
                s.reasons[r] = s.reasons.get(r, 0) + 1
        elif k == "memo":
            s.memo, s.memo_t = str(e.get("text", "") or ""), e["t"]
    for s in S.values():
        flagged = any(s.flags.values())
        if not s.wrongs and not flagged and not s.later:
            s.status = None
            continue
        if s.applied:
            s.status = "done"
        elif s.active:
            s.status = "doing"
        else:
            s.status = "need"
        s.priority = (s.wrongs * 2 + s.follow_fails * 2 + (2 if s.flags.get("confused") else 0)
                      + (1 if s.flags.get("not_understood") else 0) + (1 if s.flags.get("guessed") else 0)
                      + (-10 if s.status == "done" else 0))
    return S


def main(argv: list[str]) -> int:
    n = sync_inbox()
    evs = read_events(SYNC_FILE)
    S = states(evs)
    print(f"수신함 병합 +{n}건 · 전체 {len(evs)}건 · 복습 대상 {sum(1 for s in S.values() if s.status)}개")
    for s in sorted(S.values(), key=lambda s: -s.priority):
        if s.status:
            print(f"  {STATUS[s.status]:6} p{s.priority:>2}  {s.key}  오답 {s.wrongs}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

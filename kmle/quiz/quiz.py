#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMLE 대화형 퀴즈 러너
- 상세 증례형 문항을 화면에 출력하고, 사용자가 1~5 중 답을 선택하면 즉시 채점합니다.
- 오답이 발생하면 해당 과목의 오답노트 파일(kmle/오답노트/NN_과목.md)에 '자동으로' 기록을 추가합니다.

사용법:
    python3 quiz.py                # 전체 과목 대상, 과목 선택 메뉴
    python3 quiz.py --subject 순환기   # 특정 과목만
    python3 quiz.py --all              # 전 과목 연속 풀이
    python3 quiz.py --shuffle -n 10    # 무작위 10문항
    python3 quiz.py --review           # 오답노트에 쌓인 문항만 다시 풀기
    python3 quiz.py --export           # JSON → 사람이 읽는 마크다운 문항집 재생성

의존성 없음(파이썬 표준 라이브러리만 사용). 파이썬 3.7+.
"""
import argparse
import datetime
import glob
import json
import os
import random
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # kmle/quiz
KMLE_DIR = os.path.dirname(BASE_DIR)                            # kmle
REPO_ROOT = os.path.dirname(KMLE_DIR)                           # repo 루트
QUESTIONS_DIR = os.path.join(BASE_DIR, "questions")
WRONG_DIR = os.path.join(KMLE_DIR, "오답노트")
MUNHANG_DIR = os.path.join(KMLE_DIR, "문항")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")                     # GitHub Pages 웹 퀴즈

CIRCLED = {1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤"}


# ----------------------------------------------------------------------------
# 데이터 로딩
# ----------------------------------------------------------------------------
def load_questions():
    """questions/*.json 을 모두 읽어 문항 리스트로 반환."""
    questions = []
    for path in sorted(glob.glob(os.path.join(QUESTIONS_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for q in data:
            q["_file"] = os.path.basename(path)
            questions.append(q)
    return questions


def subjects_of(questions):
    seen = []
    for q in questions:
        if q["subject"] not in seen:
            seen.append(q["subject"])
    return seen


def is_today(q):
    """created 필드가 오늘 날짜인 문항인지. created가 없으면 기존(baseline) 문항."""
    return q.get("created") == datetime.date.today().isoformat()


# ----------------------------------------------------------------------------
# 출력 헬퍼
# ----------------------------------------------------------------------------
def hr(char="─", width=70):
    print(char * width)


def print_question(q, idx=None, total=None):
    hr("═")
    header = f"[{q.get('type', '')}]  {q['subject']}"
    if idx is not None and total is not None:
        header = f"({idx}/{total})  " + header
    print(header)
    hr()
    # 워드 파일처럼 긴 증례를 자연스럽게 줄바꿈해 출력
    print(q["vignette"].strip())
    print()
    print("Q. " + q["question"].strip())
    print()
    for i, opt in enumerate(q["options"], start=1):
        print(f"  {CIRCLED[i]} {opt}")
    print()


def print_explanation(q, chosen):
    correct = q["answer"]
    ex = q.get("explanation", {})
    hr()
    if chosen == correct:
        print(f"✅ 정답입니다!  정답: {CIRCLED[correct]}")
    else:
        print(f"❌ 오답입니다.  당신의 선택: {CIRCLED[chosen]}   /   정답: {CIRCLED[correct]}")
    hr()
    print("【해설】")
    if ex.get("진단"):
        print(f"  ▸ 진단     : {ex['진단']}")
    if ex.get("정답근거"):
        print(f"  ▸ 정답근거 : {ex['정답근거']}")
    if ex.get("오답감별"):
        print(f"  ▸ 오답감별 : {ex['오답감별']}")
    if ex.get("임상핵심"):
        print(f"  ▸ 임상핵심 : {ex['임상핵심']}")
    if q.get("source"):
        print(f"  ▸ 출처     : {q['source']}")
    print()


# ----------------------------------------------------------------------------
# 오답노트 자동 기록
# ----------------------------------------------------------------------------
def wrong_file_for(q):
    """문항의 subject_file(예: 02_순환기)에 해당하는 오답노트 경로."""
    name = q.get("subject_file")
    if not name:
        # subject_file이 없으면 과목명으로 매칭 시도
        name = q["subject"]
    return os.path.join(WRONG_DIR, f"{name}.md")


def _bump_summary(text):
    """요약 표의 '총 오답 수'와 🔴 카운트를 +1."""
    pattern = re.compile(r"^\|[ \t]*(\d+)[ \t]*\|[ \t]*(\d+)[ \t]*\|[ \t]*(\d+)[ \t]*\|[ \t]*(\d+)[ \t]*\|[ \t]*$", re.M)
    m = pattern.search(text)
    if not m:
        return text
    total, red, yellow, green = (int(x) for x in m.groups())
    new_row = f"| {total + 1} | {red + 1} | {yellow} | {green} |"
    return text[:m.start()] + new_row + text[m.end():]


def append_wrong_note(q, chosen):
    """오답을 해당 과목 오답노트 파일에 자동 추가하고, 요약 카운트를 갱신."""
    path = wrong_file_for(q)
    if not os.path.exists(path):
        # 파일이 없으면 최소 골격 생성
        os.makedirs(os.path.dirname(path), exist_ok=True)
        text = (
            f"# 오답노트 — {q['subject']}\n\n"
            "## 요약 (복습 시 갱신)\n\n"
            "| 총 오답 수 | 🔴 | 🟡 | 🟢 |\n|:---:|:---:|:---:|:---:|\n| 0 | 0 | 0 | 0 |\n\n"
            "---\n\n## 오답 기록\n\n_(아직 기록 없음)_\n"
        )
    else:
        with open(path, encoding="utf-8") as f:
            text = f.read()

    # 기존 오답 번호 계산
    existing = re.findall(r"### \[오답 #(\d+)\]", text)
    n = (max(int(x) for x in existing) + 1) if existing else 1

    today = datetime.date.today().isoformat()
    ex = q.get("explanation", {})
    keyword = q["question"].strip()
    if len(keyword) > 30:
        keyword = keyword[:30] + "…"

    entry = (
        f"\n### [오답 #{n}] {q.get('id', '')} {keyword}\n\n"
        "| 항목 | 내용 |\n|------|------|\n"
        f"| 기록일 | {today} |\n"
        f"| 과목 | {q['subject']} |\n"
        f"| 세부 주제 | 문항 유형 {q.get('type', '')} |\n"
        f"| 출처 문항 | quiz #{q.get('id', '')} |\n"
        f"| 내가 고른 답 | {CIRCLED[chosen]} {q['options'][chosen - 1]} |\n"
        f"| 정답 | {CIRCLED[q['answer']]} {q['options'][q['answer'] - 1]} |\n"
        "| 틀린 이유(지식 공백) | _(직접 작성)_ |\n"
        f"| 핵심 정리 | {ex.get('임상핵심', '')} |\n"
        f"| 감별 포인트 | {ex.get('오답감별', '')} |\n"
        f"| 관련 개념 연결 | {q.get('source', '')} |\n"
        "| 복습 상태 | 🔴 |\n"
        "| 복습 예정일 | _(직접 작성)_ |\n"
    )

    # '_(아직 기록 없음...)_' 플레이스홀더 제거
    text = re.sub(r"_\(아직 기록 없음[^)]*\)_\s*", "", text)
    text = _bump_summary(text).rstrip() + "\n" + entry

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# ----------------------------------------------------------------------------
# 퀴즈 실행
# ----------------------------------------------------------------------------
def ask(q, idx, total):
    """한 문항을 출제하고 (정답여부, 선택) 반환. q 입력 시 중단."""
    print_question(q, idx, total)
    while True:
        raw = input("정답 선택 [1-5, s=건너뛰기, q=종료]: ").strip().lower()
        if raw in ("q", "quit", "종료"):
            return None
        if raw in ("s", "skip", "건너뛰기"):
            print("↷ 건너뜁니다.\n")
            return ("skip", None)
        if raw in ("1", "2", "3", "4", "5"):
            chosen = int(raw)
            correct = chosen == q["answer"]
            print_explanation(q, chosen)
            if not correct:
                path = append_wrong_note(q, chosen)
                rel = os.path.relpath(path, KMLE_DIR)
                print(f"📝 오답을 오답노트에 자동 저장했습니다 → {rel}")
                print()
            input("계속하려면 Enter…")
            print()
            return (correct, chosen)
        print("  1~5 중에서 선택하세요.")


def run_quiz(questions):
    if not questions:
        print("출제할 문항이 없습니다.")
        return
    total = len(questions)
    correct_cnt = 0
    wrong_list = []
    for idx, q in enumerate(questions, start=1):
        result = ask(q, idx, total)
        if result is None:  # 종료
            print("\n중단했습니다.")
            break
        ok, _ = result
        if ok == "skip":
            continue
        if ok:
            correct_cnt += 1
        else:
            wrong_list.append(q)
    else:
        idx = total

    # 결과 요약
    hr("═")
    graded = correct_cnt + len(wrong_list)
    print("📊 결과 요약")
    if graded:
        print(f"  채점 문항: {graded}   정답: {correct_cnt}   오답: {len(wrong_list)}"
              f"   정답률: {correct_cnt / graded * 100:.0f}%")
    if wrong_list:
        print("  오답 문항(오답노트에 저장됨):")
        for q in wrong_list:
            print(f"    - [{q['subject']}] #{q.get('id', '')} {q['question'][:30]}")
    hr("═")


# ----------------------------------------------------------------------------
# 리뷰 모드: 오답노트에 기록된 문항만 다시 풀기
# ----------------------------------------------------------------------------
def collect_review_ids():
    ids = set()
    for path in glob.glob(os.path.join(WRONG_DIR, "*.md")):
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        for m in re.finditer(r"quiz #([\w-]+)", txt):
            ids.add(m.group(1))
    return ids


# ----------------------------------------------------------------------------
# export: JSON → 마크다운 문항집
# ----------------------------------------------------------------------------
def export_markdown(questions):
    by_file = {}
    for q in questions:
        by_file.setdefault(q["subject_file"], []).append(q)
    os.makedirs(MUNHANG_DIR, exist_ok=True)
    for sf, qs in by_file.items():
        lines = [f"# {qs[0]['subject']}\n"]
        for i, q in enumerate(qs, start=1):
            ex = q.get("explanation", {})
            lines.append(f"\n---\n\n## 문항 {i} — {q.get('type', '')}\n")
            lines.append(q["vignette"].strip() + "\n")
            lines.append(f"\n**Q.** {q['question'].strip()}\n")
            for j, opt in enumerate(q["options"], start=1):
                lines.append(f"{CIRCLED[j]} {opt}  ")
            lines.append(f"\n\n**정답:** {CIRCLED[q['answer']]}\n")
            lines.append("\n**해설**\n")
            for key in ("진단", "정답근거", "오답감별", "임상핵심"):
                if ex.get(key):
                    lines.append(f"- **{key}**: {ex[key]}")
            if q.get("source"):
                lines.append(f"- **출처**: {q['source']}")
            lines.append("")
        out = os.path.join(MUNHANG_DIR, f"{sf}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  생성: {os.path.relpath(out, KMLE_DIR)}")


def export_web_bundle(questions):
    """웹 퀴즈(GitHub Pages)가 fetch/CORS 없이 읽을 수 있도록 JS 번들로 내보낸다."""
    clean = []
    for q in questions:
        clean.append({k: v for k, v in q.items() if not k.startswith("_")})
    os.makedirs(DOCS_DIR, exist_ok=True)
    payload = json.dumps(clean, ensure_ascii=False, indent=1)
    out = os.path.join(DOCS_DIR, "questions.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 — 수정하지 마세요.\n")
        f.write("// 문항 원본: kmle/quiz/questions/*.json  →  `python3 quiz.py --export`로 재생성\n")
        f.write("window.KMLE_QUESTIONS = " + payload + ";\n")
    print(f"  생성: {os.path.relpath(out, REPO_ROOT)} ({len(clean)}문항)")


# ----------------------------------------------------------------------------
# 메뉴
# ----------------------------------------------------------------------------
def choose_mode(questions):
    """학습 구역 선택: 오늘의 문항 / 전체 문항 / 오답 복습."""
    today_cnt = sum(1 for q in questions if is_today(q))
    wrong_cnt = len(collect_review_ids())
    print("무엇을 풀까요?")
    print(f"  1) 오늘의 문항 (오늘 생성된 새 문항: {today_cnt}개)")
    print(f"  2) 전체 문항 (누적 {len(questions)}개)")
    print(f"  3) 오답 복습 (오답노트에 쌓인 문항: {wrong_cnt}개)")
    while True:
        raw = input("번호 입력 [1-3]: ").strip()
        if raw in ("1", "2", "3"):
            return {"1": "today", "2": "all", "3": "review"}[raw]
        print("  1~3 중에서 선택하세요.")


def choose_subject(questions):
    subs = subjects_of(questions)
    print("과목을 선택하세요:")
    print("  0) 전체")
    for i, s in enumerate(subs, start=1):
        cnt = sum(1 for q in questions if q["subject"] == s)
        print(f"  {i}) {s} ({cnt}문항)")
    while True:
        raw = input("번호 입력 [0-{}]: ".format(len(subs))).strip()
        if raw.isdigit():
            k = int(raw)
            if k == 0:
                return None
            if 1 <= k <= len(subs):
                return subs[k - 1]
        print("  다시 입력하세요.")


def main():
    p = argparse.ArgumentParser(description="KMLE 대화형 퀴즈")
    p.add_argument("--subject", help="특정 과목만 풀기")
    p.add_argument("--all", action="store_true", help="전 과목 연속 풀이")
    p.add_argument("--shuffle", action="store_true", help="문항 순서 무작위")
    p.add_argument("-n", type=int, default=0, help="출제 문항 수 제한")
    p.add_argument("--review", action="store_true", help="오답노트에 쌓인 문항만 다시 풀기")
    p.add_argument("--today", action="store_true", help="오늘 생성된 문항만 풀기")
    p.add_argument("--export", action="store_true", help="JSON을 마크다운 문항집으로 재생성")
    args = p.parse_args()

    questions = load_questions()
    if not questions:
        print(f"문항 JSON이 없습니다. ({QUESTIONS_DIR})")
        sys.exit(1)

    if args.export:
        print("마크다운 문항집을 재생성합니다…")
        export_markdown(questions)
        print("웹 퀴즈용 문항 번들을 재생성합니다…")
        export_web_bundle(questions)
        return

    # 모드 결정: 플래그가 없으면 대화형 메뉴로 학습 구역을 고른다.
    mode = None
    if args.review:
        mode = "review"
    elif args.today:
        mode = "today"
    elif args.subject or args.all:
        mode = "all"
    else:
        mode = choose_mode(questions)

    if mode == "review":
        ids = collect_review_ids()
        questions = [q for q in questions if q.get("id") in ids]
        if not questions:
            print("오답노트에 기록된 문항이 없습니다. 먼저 퀴즈를 풀어보세요.")
            return
        print(f"\n[오답 복습] 오답노트 문항 {len(questions)}개를 다시 풉니다.\n")
    elif mode == "today":
        questions = [q for q in questions if is_today(q)]
        if not questions:
            print("\n오늘 생성된 문항이 아직 없습니다. (매일 오전 6시 루틴이 새 문항을 추가합니다)")
            return
        print(f"\n[오늘의 문항] {len(questions)}개를 풉니다.\n")
    else:  # all
        if args.subject:
            questions = [q for q in questions if q["subject"] == args.subject]
            if not questions:
                print(f"'{args.subject}' 과목 문항을 찾지 못했습니다.")
                return
        elif not args.all:
            sub = choose_subject(questions)
            if sub:
                questions = [q for q in questions if q["subject"] == sub]
        print(f"\n[전체 문항] {len(questions)}개 대상.\n")

    if args.shuffle:
        random.shuffle(questions)
    if args.n and args.n > 0:
        questions = questions[: args.n]

    print()
    run_quiz(questions)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n종료합니다.")

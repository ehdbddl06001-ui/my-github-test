"""kmle_scope.py — 국시 평가목표(의사직무상황 105개) ↔ 학습서 기본틀 대조표.

  python pipelines/kmle_scope.py                 # 요약(과별 · 정리본 없는 직무상황)
  python pipelines/kmle_scope.py --book 안과     # 그 과의 슬롯마다 대응 직무상황 · 정리본 유무
  python pipelines/kmle_scope.py --md <파일>     # 전 과목 대조표를 마크다운으로
  python pipelines/kmle_scope.py --check         # 대응표의 슬롯 id 가 기본틀에 있는가

대응표(content/outline/kmle_encounters.yaml)는 추정이다 — 평가목표집이 필수질환 이름을 공개하지 않는다.
「직무상황 대응 없음」은 국시 범위 밖이라는 뜻이 아니다.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load():
    enc = yaml.safe_load((ROOT / "content/outline/kmle_encounters.yaml").read_text(encoding="utf-8"))
    out = subprocess.run([sys.executable, str(ROOT / "pipelines/outline.py"), "--json"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return enc, json.loads(out)


def index(enc, books):
    slot_book = {s["id"]: b for b, sl in books.items() for s in sl}
    slot = {s["id"]: s for sl in books.values() for s in sl}
    by_slot = {}
    for e in enc["encounters"]:
        for sid in e["slots"]:
            by_slot.setdefault(sid, []).append(e)
    return slot_book, slot, by_slot


def check(enc, slot):
    bad = [(e["n"], sid) for e in enc["encounters"] for sid in e["slots"] if sid not in slot]
    for n, sid in bad:
        print(f"✗ 직무상황 {n}: 슬롯 '{sid}' 가 기본틀에 없다")
    if [e["n"] for e in enc["encounters"]] != list(range(1, 106)):
        print("✗ 직무상황 번호가 1~105 가 아니다")
        return 1
    return 1 if bad else 0


def book_rows(sl, by_slot):
    rows = []
    for s in sl:
        es = by_slot.get(s["id"], [])
        rows.append((s["id"], s["title"], ", ".join(f'{e["n"]} {e["name"]}' for e in es) or "—",
                     len(s["concepts"])))
    return rows


def summary(books, by_slot):
    lines = ["| 과 | 슬롯 | 직무상황에 대응 | 그중 정리본 있음 | 그중 비어 있음 |", "|---|---|---|---|---|"]
    for b, sl in books.items():
        m = [s for s in sl if s["id"] in by_slot]
        f = [s for s in m if s["concepts"]]
        lines.append(f"| {b} | {len(sl)} | {len(m)} | {len(f)} | {len(m) - len(f)} |")
    return lines


def encounter_rows(enc, slot, slot_book):
    rows = []
    for e in enc["encounters"]:
        filled = [s for s in e["slots"] if slot[s]["concepts"]]
        n = sum(len(slot[s]["concepts"]) for s in e["slots"])
        bk = sorted({slot_book[s] for s in e["slots"]})
        if not e["slots"]:
            state = "슬롯 없음"
        elif not filled:
            state = "정리본 없음"
        else:
            state = f"{len(filled)}/{len(e['slots'])}"
        rows.append((e["n"], e["name"], " · ".join(bk) or "—", state, n))
    return rows


def md(enc, books, slot_book, slot, by_slot):
    o = ["# 국시 평가목표 ↔ 학습서 기본틀 대조표", "",
         f"출처: {enc['source']} · 대응 점검일 {enc['checked_at']}", "",
         "대응은 슬롯 제목으로 붙인 **추정**이다. 평가목표집은 필수질환 522개의 이름을 공개하지 않으므로 "
         "「—」(직무상황 대응 없음)는 국시 범위 밖이라는 뜻이 아니다.", "",
         "## 과별 요약", ""] + summary(books, by_slot)
    o += ["", "## 직무상황 105개 — 어느 책에 있고 정리본이 있는가", "",
          "| # | 직무상황 | 책 | 정리본 있는 슬롯/대응 슬롯 | 정리본 수 |", "|---|---|---|---|---|"]
    for n, name, bk, state, cnt in encounter_rows(enc, slot, slot_book):
        o.append(f"| {n} | {name} | {bk} | {state} | {cnt} |")
    for b, sl in books.items():
        o += ["", f"## {b}", "", "| 슬롯 | 제목 | 직무상황 | 정리본 |", "|---|---|---|---|"]
        for sid, title, es, c in book_rows(sl, by_slot):
            o.append(f"| {sid} | {title} | {es} | {c or '·'} |")
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book")
    ap.add_argument("--md")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    enc, books = load()
    slot_book, slot, by_slot = index(enc, books)
    rc = check(enc, slot)
    if a.check or rc:
        print("대응표 점검:", "오류" if rc else "이상 없음")
        return rc
    if a.md:
        Path(a.md).write_text(md(enc, books, slot_book, slot, by_slot), encoding="utf-8")
        print("저장:", a.md)
        return 0
    if a.book:
        for sid, title, es, c in book_rows(books[a.book], by_slot):
            print(f"{'✓' if c else '·'} {sid:26} {title[:40]:40}  ← {es}")
        return 0
    print("\n".join(summary(books, by_slot)))
    print("\n정리본이 하나도 없는 직무상황:")
    for n, name, bk, state, cnt in encounter_rows(enc, slot, slot_book):
        if state in ("슬롯 없음", "정리본 없음"):
            print(f"  {n:3} {name} — {state} ({bk})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

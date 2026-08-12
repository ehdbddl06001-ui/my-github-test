"""
restore_scan.py — 필기 스캔 페이지에서 필기를 지우고 주변 기반으로 복원한다.

용도(실사 lane): e-Anatomy 영상 캡처 + 학생 필기 스캔에서
  1) 색 필기(빨간 펜 / 올리브 형광 / 파란 형광)를 채널 임계값으로 자동 검출
  2) 검정 손글씨는 클로드가 눈으로 지정한 bbox(config)로 마스크
  3) OpenCV TELEA inpainting으로 주변 질감 기반 복원 → clean 판
  4) quiz 판: 정답 라벨 bbox는 inpaint로 가리고, 좌상단 타이틀 존은
     **무조건 검은 박스**(영상 타이틀에 답이 노출되므로), 번호핀을 얹는다.

원칙:
  - 원본은 절대 수정하지 않는다(별도 출력 파일).
  - 산출물은 `.private/anatomy/render/`(gitignore) — 카데바·영상 캡처
    파생물은 공개 게시 금지(publishable는 사람만 true로).
  - bbox 지정·검수는 결정론이 아니라 시각 판단 → 스킬 4b QA 루프 필수.

config(JSON) 예:
{
  "colors": {"red": true, "olive": true, "blue": true},
  "protect": [[350,225,770,432]],          // 색 검출에서 보호(장갑·프로브·영상 라벨)
  "olive_region": [1300,0,9999,400],       // 올리브 검출 제한 영역(영상 노란 라벨 보호)
  "erase_boxes": [[770,146,935,192]],      // 검정 손글씨 bbox
  "title_box": [38,145,240,270],           // quiz에서 검은 박스로 덮을 타이틀 존
  "label_boxes": [[640,522,870,598]],      // quiz에서 inpaint로 가릴 정답 라벨
  "pins": [{"x":560,"y":610,"to":[705,505],"n":1}]
}

사용:
  python pipelines/restore_scan.py --image page.png --config cfg.json \
      --out-clean clean.png --out-quiz quiz.png
  python pipelines/restore_scan.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PIN_FILL = (8, 179, 234)   # BGR — 번호핀(노랑)
PIN_TEXT = (38, 24, 14)


def _color_mask(img, colors: dict, protect: list, olive_region: list | None):
    import cv2
    import numpy as np

    b, g, r = cv2.split(img.astype(np.int16))
    mask = np.zeros(img.shape[:2], np.uint8)
    if colors.get("red"):
        mask |= (((r > 120) & (g < 85) & (b < 85)).astype(np.uint8) * 255)
    if colors.get("blue"):
        mask |= ((((b - r) > 22) & (b > 85)).astype(np.uint8) * 255)
    if colors.get("olive"):
        ol = ((r > 105) & (g > 95) & (b < 70)).astype(np.uint8) * 255
        if olive_region:
            x0, y0, x1, y1 = olive_region
            keep = np.zeros_like(ol)
            keep[max(0, y0):y1, max(0, x0):x1] = 255
            ol &= keep
        mask |= ol
    for x0, y0, x1, y1 in protect or []:
        mask[y0:y1, x0:x1] = 0
    return mask


def restore(image: Path, cfg: dict, out_clean: Path, out_quiz: Path | None) -> dict:
    import cv2
    import numpy as np

    img = cv2.imread(str(image))
    if img is None:
        raise SystemExit(f"이미지를 읽을 수 없음: {image}")
    mask = _color_mask(img, cfg.get("colors", {}), cfg.get("protect"),
                       cfg.get("olive_region"))
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    for x0, y0, x1, y1 in cfg.get("erase_boxes", []):
        mask[y0:y1, x0:x1] = 255
    clean = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
    out_clean.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_clean), clean)
    stats = {"mask_px": int(mask.sum() / 255), "quiz": None}

    if out_quiz:
        quiz = clean.copy()
        lb = np.zeros(quiz.shape[:2], np.uint8)
        for x0, y0, x1, y1 in cfg.get("label_boxes", []):
            lb[y0:y1, x0:x1] = 255
        if lb.any():
            quiz = cv2.inpaint(quiz, lb, 9, cv2.INPAINT_TELEA)
        tb = cfg.get("title_box")
        if tb:  # 좌상단 타이틀은 답 노출 → 항상 검은 박스(주변 맞춤 불필요)
            cv2.rectangle(quiz, (tb[0], tb[1]), (tb[2], tb[3]), (0, 0, 0), -1)
        for p in cfg.get("pins", []):
            if p.get("to"):
                cv2.line(quiz, (p["x"], p["y"]), tuple(p["to"]), PIN_FILL, 3)
            cv2.circle(quiz, (p["x"], p["y"]), 26, PIN_FILL, -1)
            cv2.putText(quiz, str(p.get("n", 1)), (p["x"] - 10, p["y"] + 11),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, PIN_TEXT, 3, cv2.LINE_AA)
        out_quiz.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_quiz), quiz)
        stats["quiz"] = str(out_quiz)
    return stats


def selftest() -> int:
    import tempfile

    import cv2
    import numpy as np

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        img = np.full((400, 600, 3), (240, 235, 225), np.uint8)
        cv2.circle(img, (300, 220), 90, (200, 190, 180), -1)
        cv2.putText(img, "MEMO", (430, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (40, 40, 200), 3)                      # 빨간 필기
        cv2.putText(img, "note", (60, 350), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (20, 20, 20), 2)                       # 검정 손글씨
        src = td / "p.png"; cv2.imwrite(str(src), img)
        cfg = {"colors": {"red": True}, "erase_boxes": [[50, 320, 160, 365]],
               "title_box": [0, 0, 120, 40],
               "pins": [{"x": 300, "y": 100, "to": [300, 170], "n": 1}]}
        st = restore(src, cfg, td / "c.png", td / "q.png")
        assert st["mask_px"] > 0
        clean = cv2.imread(str(td / "c.png"))
        b, g, r = cv2.split(clean[60:90, 420:580].astype(np.int16))
        assert not bool(((r > 120) & (g < 85) & (b < 85)).any()), "빨간 필기 잔존"
        quiz = cv2.imread(str(td / "q.png"))
        assert (quiz[5:35, 5:115] == 0).all(), "타이틀 검은 박스 미적용"
    print("[ OK ] restore_scan selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image"); ap.add_argument("--config")
    ap.add_argument("--out-clean"); ap.add_argument("--out-quiz")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.image and a.config and a.out_clean):
        print("--image/--config/--out-clean 필요 (또는 --selftest)")
        return 2
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    st = restore(Path(a.image), cfg, Path(a.out_clean),
                 Path(a.out_quiz) if a.out_quiz else None)
    print(f"restore: mask {st['mask_px']}px → {a.out_clean}"
          + (f" · quiz {st['quiz']}" if st["quiz"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

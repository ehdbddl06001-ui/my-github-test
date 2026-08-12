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


def _donor_blend(img, mask, donor_path: Path, cfg: dict):
    """인접 페이지(같은 영상의 이웃 프레임)에서 마스크 영역을 가져와 복원.

    확산 인페인팅의 '블라인드(뭉개짐)' 현상을 없애는 1순위 경로: 같은 카메라
    구도의 donor 프레임을 ECC로 정렬해 진짜 조직 질감을 복사한다.
    donor 자체의 필기·자막·손 위치 차이는 제외하고(그 부분은 인페인팅 폴백),
    경계는 feather 블렌드로 잇는다. 반환: (부분 복원 이미지, 남은 마스크).
    """
    import cv2
    import numpy as np

    don = cv2.imread(str(donor_path))
    if don is None:
        return img, mask
    h, w = img.shape[:2]
    g1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(don, cv2.COLOR_BGR2GRAY)
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        cv2.findTransformECC(
            g1[h // 3:h * 5 // 6, w // 4:w * 4 // 5],
            g2[h // 3:h * 5 // 6, w // 4:w * 4 // 5], warp,
            cv2.MOTION_EUCLIDEAN,
            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5))
    except cv2.error:
        return img, mask  # 정렬 실패 → donor 사용 안 함
    don = cv2.warpAffine(don, warp, (w, h),
                         flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    # donor 오염 제외: donor 자신의 필기 + 지정 박스 + 프레임 차이 큰 곳.
    # 주의: 밝은 흰 근막(스페큘러)은 b가 높아 파란 필기로 오검출되기 쉬움 —
    # 무채색·고휘도 픽셀은 제외해야 donor의 진짜 질감이 살아남는다(2026-08-12 실측).
    b, g, r = cv2.split(don.astype(np.int16))
    bright_neutral = (r + g + b) > 560
    bad = ((((r > 120) & (g < 85) & (b < 85))
            | (((b - r) > 22) & (b > 85) & ~bright_neutral)
            | ((r > 105) & (g > 95) & (b < 70))).astype(np.uint8) * 255)
    bad = cv2.dilate(bad, np.ones((13, 13), np.uint8))
    for x0, y0, x1, y1 in cfg.get("donor_bad_boxes", []):
        bad[y0:y1, x0:x1] = 255
    diff = cv2.absdiff(cv2.GaussianBlur(g1, (21, 21), 0),
                       cv2.GaussianBlur(cv2.cvtColor(don, cv2.COLOR_BGR2GRAY),
                                        (21, 21), 0))
    bad[diff > int(cfg.get("donor_diff_thresh", 60))] = 255
    use = cv2.bitwise_and(mask, cv2.bitwise_not(bad))
    # 광도 매칭: 마스크 밖 공통 영역 기준으로 donor 밝기를 타깃에 맞춘다
    ok = (mask == 0) & (bad == 0)
    if ok.any():
        t = img[ok].astype(np.float32); d = don[ok].astype(np.float32)
        gain = (t.std(axis=0) + 1e-3) / (d.std(axis=0) + 1e-3)
        gain = np.clip(gain, 0.7, 1.4)
        don = np.clip((don.astype(np.float32) - d.mean(axis=0)) * gain
                      + t.mean(axis=0), 0, 255).astype(np.uint8)
    # 마스크 내부는 donor 100%, feather는 마스크 '바깥'으로만 —
    # 안쪽으로 feather하면 지워야 할 필기가 반투명하게 비친다(고스트).
    alpha = cv2.GaussianBlur(cv2.dilate(use, np.ones((9, 9), np.uint8)),
                             (15, 15), 0).astype(np.float32)
    alpha = np.maximum(alpha, use.astype(np.float32))[..., None] / 255.0
    out = (img.astype(np.float32) * (1 - alpha)
           + don.astype(np.float32) * alpha).astype(np.uint8)
    return out, cv2.bitwise_and(mask, bad)


def _tight_strokes(img, box: list, drop: int = 35, pad: int = 2):
    """박스 전체가 아니라 '펜 획 픽셀'만 마스크로 뽑는다(얇은 펜 마스킹).

    검정 손글씨는 주변 배경보다 어두운 얇은 획이다 — 국소 배경(중앙값 블러)
    대비 drop 이상 어두운 픽셀만 마스킹하면 지울 면적이 수 배 줄어 인페인팅
    품질이 크게 올라간다. 획이 거의 안 잡히면(어두운 배경 위 글씨 등)
    박스 전체로 폴백한다.
    """
    import cv2
    import numpy as np

    x0, y0, x1, y1 = box
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bg = cv2.medianBlur(gray, 31).astype(np.int16)
    m = np.zeros(gray.shape, np.uint8)
    roi = (bg - gray.astype(np.int16)) > drop
    m[y0:y1, x0:x1] = roi[y0:y1, x0:x1].astype(np.uint8) * 255
    area = (y1 - y0) * (x1 - x0)
    if area and m[y0:y1, x0:x1].sum() / 255 < 0.02 * area:
        m[y0:y1, x0:x1] = 255          # 획 검출 실패 → 박스 전체 폴백
    else:
        m = cv2.dilate(m, np.ones((2 * pad + 1, 2 * pad + 1), np.uint8))
    return m


def _inpaint_progressive(img, mask, band: int = 4, radius: int = 4):
    """넓은 마스크를 한 번에 채우지 않고 바깥 테두리부터 얇은 띠로 반복해 채운다.

    확산 인페인팅은 채울 폭이 넓을수록 뭉개진다 — 매 pass 방금 채워진 픽셀을
    이웃으로 삼아 band px씩 안쪽으로 전진하면 질감 전파가 훨씬 좋다
    ('얇은 펜으로 여러 번' 방식).
    """
    import cv2
    import numpy as np

    k = np.ones((2 * band + 1, 2 * band + 1), np.uint8)
    m = mask.copy()
    img = img.copy()
    for _ in range(200):                # 안전 상한
        if not m.any():
            break
        inner = cv2.erode(m, k)
        ring = cv2.subtract(m, inner)
        if not ring.any():
            ring, inner = m, np.zeros_like(m)
        # 전체 남은 마스크를 넣어 인페인팅(안쪽 오염 픽셀이 소스로 쓰이지 않게)
        # 하되, 이번 pass에서는 바깥 띠 결과만 확정한다.
        filled = cv2.inpaint(img, m, radius, cv2.INPAINT_TELEA)
        sel = ring > 0
        img[sel] = filled[sel]
        m = inner
    return img


def _match_grain(img, filled_mask):
    """인페인팅 영역에 주변 질감 수준의 고주파 노이즈를 입혀 '너무 매끈함'을 줄인다."""
    import cv2
    import numpy as np

    ring = cv2.dilate(filled_mask, np.ones((25, 25), np.uint8)) & ~filled_mask
    if not ring.any():
        return img
    high = img.astype(np.float32) - cv2.GaussianBlur(img, (0, 0), 2).astype(np.float32)
    std = float(np.clip(high[ring > 0].std(), 1.0, 12.0))
    rng = np.random.default_rng(0)  # 결정론(재현 가능)
    noise = cv2.GaussianBlur(rng.normal(0, std, img.shape).astype(np.float32), (0, 0), 0.8)
    m = (filled_mask > 0)[..., None]
    return np.clip(img.astype(np.float32) + noise * m, 0, 255).astype(np.uint8)


def restore(image: Path, cfg: dict, out_clean: Path, out_quiz: Path | None) -> dict:
    import cv2
    import numpy as np

    img = cv2.imread(str(image))
    if img is None:
        raise SystemExit(f"이미지를 읽을 수 없음: {image}")
    mask = _color_mask(img, cfg.get("colors", {}), cfg.get("protect"),
                       cfg.get("olive_region"))
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    for x0, y0, x1, y1 in cfg.get("erase_boxes", []):
        mask[y0:y1, x0:x1] = 255
    for box in cfg.get("stroke_boxes", []):   # 얇은 펜: 획 픽셀만 마스킹
        mask |= _tight_strokes(img, box)
    remaining = mask
    clean = img
    if cfg.get("donor"):  # 1순위: 인접 프레임에서 진짜 질감 복사
        clean, remaining = _donor_blend(img, mask, Path(cfg["donor"]), cfg)
    if remaining.any():   # 폴백: 점진(테두리→안쪽) 인페인팅 + 질감 매칭
        clean = _inpaint_progressive(clean, remaining)
        clean = _match_grain(clean, remaining)
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
        for x0, y0, x1, y1 in cfg.get("black_boxes", []):  # 자막 등 — 검은 박스가 깔끔
            cv2.rectangle(quiz, (x0, y0), (x1, y1), (0, 0, 0), -1)
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

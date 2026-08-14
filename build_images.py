#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""원본 사진을 웹용으로 줄여 assets/ 에 넣는다.

    python3 build_images.py [원본_디렉터리]

원본은 저장소에 두지 않는다. 이미 만들어진 assets/*.jpg 가 결과물이고,
사진을 갈아 끼울 때만 다시 돌리면 된다.
EXIF 회전 정보는 파일에 구워 넣으므로 어디서 열어도 바로 선다.
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps

OUT = Path(__file__).parent / "assets"

# 결과 이름: (원본 파일명 일부, 긴 변 최대 길이, JPEG 품질)
PLAN = {
    "hero-pour":   ("IMG_7926", 1200, 80),   # 칵테일 한 잔과 백바 — 히어로
    "backbar":     ("IMG_2702", 1500, 80),   # 백바 전경 — 소개
    "tasting":     ("IMG_2188", 1600, 78),   # 테이스팅 클래스 — 즐기는 법
    "flight":      ("IMG_2176", 1600, 78),   # 플라이트와 치즈 — 메뉴
    "storefront":  ("CCE7C181", 1100, 82),   # 외관 간판 — 오시는 길
}


def main(srcdir):
    src = Path(srcdir)
    files = list(src.iterdir())
    OUT.mkdir(exist_ok=True)

    for name, (needle, long_edge, quality) in PLAN.items():
        match = next((f for f in files if needle in f.name), None)
        if match is None:
            print(f"  건너뜀 {name}: '{needle}' 를 포함한 파일이 없습니다")
            continue

        im = ImageOps.exif_transpose(Image.open(match)).convert("RGB")
        scale = long_edge / max(im.size)
        if scale < 1:
            im = im.resize(
                (round(im.width * scale), round(im.height * scale)),
                Image.LANCZOS,
            )
        dst = OUT / f"{name}.jpg"
        im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
        print(f"  {dst.name:16s} {im.width}x{im.height}  {dst.stat().st_size // 1024:>4d} KB")


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"원본: {d}")
    main(d)

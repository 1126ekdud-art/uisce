#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사진까지 전부 파일 하나에 담은 미리보기 HTML을 만든다.

    python3 build_preview.py [출력_디렉터리]

assets/*.jpg 를 data URI 로 바꿔 넣으므로, 결과 파일 하나만 있으면
같은 폴더에 아무것도 없어도 그대로 열린다. 링크로 보내거나
외부 호스팅에 올릴 때 쓴다. 저장소용 원본은 index.html / menu.html 이다.
"""

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ["index.html", "menu.html"]


def inline_images(html, root):
    """src="assets/x.jpg" 를 base64 data URI 로 바꾼다."""
    cache = {}

    def sub(m):
        rel = m.group(1)
        if rel not in cache:
            data = (root / rel).read_bytes()
            cache[rel] = "data:image/jpeg;base64," + base64.b64encode(data).decode()
        return f'src="{cache[rel]}"'

    return re.sub(r'src="(assets/[^"]+)"', sub, html)


def main(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    for page in PAGES:
        html = (ROOT / page).read_text(encoding="utf-8")
        html = inline_images(html, ROOT)
        dst = out / page.replace(".html", "-preview.html")
        dst.write_text(html, encoding="utf-8")
        print(f"  {dst.name:24s} {dst.stat().st_size // 1024:>5d} KB")


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "preview"
    main(d)

"""교과서 PDF → 쪽별 텍스트(text.txt) + 필요한 쪽 PNG 렌더링

사용법:
  python extract_pdf.py <pdf> <출력폴더>                # text.txt
  python extract_pdf.py <pdf> <출력폴더> --render 4-8   # page_004.png ... (숫자·수식 확인용)
"""
import argparse
import os

import pymupdf

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("out")
ap.add_argument("--render", help="렌더링할 쪽 범위, 예: 4-8 또는 5")
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
doc = pymupdf.open(args.pdf)

if args.render:
    a, _, b = args.render.partition("-")
    for n in range(int(a), int(b or a) + 1):
        path = os.path.join(args.out, f"page_{n:03d}.png")
        doc[n - 1].get_pixmap(dpi=110).save(path)
        print(path)
else:
    path = os.path.join(args.out, "text.txt")
    with open(path, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc, 1):
            f.write(f"\n=== PAGE {i} (그림 {len(page.get_images())}개) ===\n{page.get_text()}")
    print(f"{doc.page_count}쪽 → {path}")

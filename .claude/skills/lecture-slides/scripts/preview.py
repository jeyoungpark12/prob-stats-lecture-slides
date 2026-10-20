"""PowerPoint로 .pptx의 모든 슬라이드를 PNG로 내보내고 sheet.png(2열 한눈에 보기)로 합치기

사용법: python preview.py <pptx> <출력폴더>
Windows + PowerPoint 설치 필요. 없으면 "NO_POWERPOINT"를 출력하고 종료.
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("s*.png"):
    old.unlink()

ps = r"""
try {
  $app = New-Object -ComObject PowerPoint.Application -ErrorAction Stop
  $p = $app.Presentations.Open($env:PV_SRC, $true, $false, $false)
  $i = 1
  foreach ($sl in $p.Slides) { $sl.Export("$env:PV_OUT\s$i.png", "PNG", 1280, 720); $i++ }
  $p.Close(); $app.Quit()
} catch { Write-Output "NO_POWERPOINT: $($_.Exception.Message)"; exit 1 }
"""
env = dict(os.environ, PV_SRC=str(src), PV_OUT=str(out))  # 한글 경로는 환경변수로 넘겨야 안전
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], env=env, capture_output=True, text=True)
if r.returncode:
    print(r.stdout.strip() or r.stderr.strip())
    sys.exit(1)

shots = sorted(out.glob("s*.png"), key=lambda p: int(p.stem[1:]))
tw, th = 640, 360
sheet = Image.new("RGB", (tw * 2, th * ((len(shots) + 1) // 2)), "white")
for i, p in enumerate(shots):
    sheet.paste(Image.open(p).resize((tw, th)), ((i % 2) * tw, (i // 2) * th))
sheet.save(out / "sheet.png")
print(f"{len(shots)}장 → {out / 'sheet.png'}")

"""Wikimedia Commons에서 자유 라이선스 사진 검색 → 후보 다운로드 + meta.json(작가·라이선스) + _sheet.jpg(한눈에 보기)

사용법: python commons_fetch.py <출력폴더> "검색어1" "검색어2" ...   (검색어당 최대 3장)
요청 제한(429)에 걸리면 자동으로 기다렸다 재시도하므로 검색어가 많으면 몇 분 걸림.
"""
import json, re, sys, os, time, urllib.request, urllib.parse, urllib.error
from PIL import Image, ImageDraw

OUT = sys.argv[1]
QUERIES = sys.argv[2:]
def get(url):
    for i in range(5):
        try:
            time.sleep(2)
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (i + 1))
    raise RuntimeError("rate limited")

UA = {"User-Agent": "lecture-slides/1.0 (personal teaching use)"}
OK = re.compile(r"^(CC0|Public domain|CC BY(-SA)? [0-9.]+|PD.*)$", re.I)

os.makedirs(OUT, exist_ok=True)
meta = {}
for q in QUERIES:
    params = {"action": "query", "format": "json", "generator": "search",
              "gsrsearch": f"filetype:bitmap {q}", "gsrnamespace": 6, "gsrlimit": 8,
              "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 960,
              "iiextmetadatafilter": "LicenseShortName|Artist"}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    data = json.loads(get(url))
    n = 0
    for p in data.get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        lic = m.get("LicenseShortName", {}).get("value", "")
        if not OK.match(lic) or n >= 3:
            continue
        key = f"{re.sub(r'[^a-z0-9]+', '_', q.lower())}_{n}"
        path = os.path.join(OUT, key + ".jpg")
        try:
            raw = get(ii["thumburl"])
            with open(path, "wb") as f:
                f.write(raw)
            Image.open(path).convert("RGB").save(path, "JPEG", quality=88)
        except Exception as e:
            print("skip", key, e); continue
        meta[key] = {"title": p["title"], "license": lic,
                     "artist": re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip(),
                     "page": ii.get("descriptionurl")}
        n += 1

with open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)

# contact sheet
keys = list(meta)
cols, tw, th = 4, 360, 260
sheet = Image.new("RGB", (cols * tw, ((len(keys) + cols - 1) // cols) * (th + 24)), "white")
d = ImageDraw.Draw(sheet)
for i, k in enumerate(keys):
    im = Image.open(os.path.join(OUT, k + ".jpg")); im.thumbnail((tw - 8, th - 8))
    x, y = (i % cols) * tw, (i // cols) * (th + 24)
    sheet.paste(im, (x + 4, y + 4)); d.text((x + 4, y + th), k, fill="black")
sheet.save(os.path.join(OUT, "_sheet.jpg"))
print(len(keys), "images")

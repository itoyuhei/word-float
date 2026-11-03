
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

URL = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"

req = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)

words = set()

for item in root.findall(".//item"):
    title = item.findtext("title", "")

    # 見出しから不要な文字を除去
    title = re.sub(r"\s+-\s+[^-]+$", "", title)

    if 2 <= len(title) <= 40:
        words.add(title)

output = {
    "updated": __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).isoformat(),
    "words": sorted(words)
}

Path("trends.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(words)} news headlines")

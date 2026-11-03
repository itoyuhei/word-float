"""Public RSS trends, no X API; runs on GitHub Actions."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
feeds = [
    'https://trends.google.com/trending/rss?geo=JP',
    'https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja',
]
words=[]
for url in feeds:
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'WordFloat/1.0 (RSS reader)'})
        with urllib.request.urlopen(req,timeout=15) as res:
            root=ET.fromstring(res.read())
        for item in root.findall('.//item'):
            title=(item.findtext('title') or '').strip()
            if 'news.google' in url:
                title=re.sub(r'\s+-\s+[^-]+$','',title)
                for part in re.split(r'[、，,:：／/｜|「」『』（）()]',title):
                    part=part.strip()
                    if 2<=len(part)<=20: words.append(part)
            elif 2<=len(title)<=35:
                words.append(title)
    except Exception as e:
        print('Could not fetch',url,repr(e))
old=Path('trends.json')
if old.exists():
    try: words+=json.loads(old.read_text(encoding='utf-8')).get('words',[])
    except Exception: pass
words=list(dict.fromkeys(words))[:500]
old.write_text(json.dumps({'source':'Google Trends RSS / Google News RSS (not X)','words':words},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved',len(words),'words')

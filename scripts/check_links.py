#!/usr/bin/env python3
"""Audit local links; optionally check public URLs with --external (requires curl)."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[]; self.ids=set(); self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ('href','src'):
            if key in a:self.links.append(a[key])

pages={p.name:Links(p.read_text()) for p in ROOT.glob('*.html')}
external=set(); failures=[]; local=0
for filename,doc in pages.items():
    for link in doc.links:
        u=urlsplit(link)
        if u.scheme in ('https','http'): external.add(link); continue
        if u.scheme: continue
        target=unquote(u.path) or filename
        if not (ROOT/target).is_file():failures.append(f'{filename}: missing {target}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:failures.append(f'{filename}: missing fragment {link}')
        local+=1
print(f'Local audit: {len(pages)} pages, {local} references, {len(failures)} failures')
for failure in failures:print(failure)
if '--external' in sys.argv:
    def check(url):
        result=subprocess.run(['curl','-sSL','--max-time','25','--output','/dev/null','--write-out','%{http_code}\t%{url_effective}',url],capture_output=True,text=True)
        parts=result.stdout.split('\t',1)
        return {'url':url,'status':parts[0] if parts else '000','destination':parts[-1],'error':result.stderr.strip()}
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,sorted(external)))
    (ROOT/'docs/link-audit.json').write_text(json.dumps(results,indent=2)+'\n')
    for result in results:print(result['status'],result['url'],'→',result['destination'])
if failures:sys.exit(1)

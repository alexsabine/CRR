#!/usr/bin/env python3
"""Put the whole Museum on a site, in museum/. Takes the publishing build (MUSEUM/build_artifact.py output) and the narration folders.
Usage: mk_museum.py <publishing build dir> <site museum dir>"""
import os, shutil, sys, glob
pub, out = sys.argv[1], sys.argv[2]; S = '/home/user/Phoenix-1-/MUSEUM/studio/'; os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(pub + '/*.html')):
    n = os.path.basename(f)
    if n == 'blake.html':
        t = open(f, encoding='utf-8').read()
        home = ('<a id="sitehome" href="../index.html">&larr; Alexander Sabine</a>\n<style>#sitehome{position:fixed;left:18px;top:66px;z-index:6;font:400 .86rem/1 "IM Fell English SC","IM Fell English",Georgia,serif;letter-spacing:.03em;'
                'color:var(--ink);text-decoration:none;background:var(--chip);border:1px solid var(--paper-edge);border-radius:3px;padding:8px 12px 9px;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}'
                '#sitehome:hover{border-color:var(--gilt)}@media (max-width:760px){#sitehome{left:10px;top:50px;padding:6px 9px 7px;font-size:.8rem}}</style>\n')
        home += open('/home/user/temporalgrammar/src/palimpsest_snippet.html', encoding='utf-8').read()
        t = ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n</head>\n<body>\n' + t + home + '</body>\n</html>\n')
        open(out + '/index.html', 'w', encoding='utf-8').write(t)
    else: shutil.copy(f, out + '/' + n)
for d in ['held-audio', 'potters-wheel-audio']:
    os.makedirs(out + '/' + d, exist_ok=True)
    for m in glob.glob(S + d + '/*.mp3'): shutil.copy(m, out + '/' + d + '/')
print('museum on site:', sum(os.path.getsize(f) for f in glob.glob(out + '/**', recursive=True) if os.path.isfile(f)) // 1024 // 1024, 'MB')

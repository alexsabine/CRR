"""Fetch the four Project Gutenberg books that SEC-PG-LLM-H's block-hash lottery admitted, and check each sha256 against
the committed draw_log.json. Written for this area (not frozen; MIT). Standard library + curl.
The lottery itself (data_step.py draw) cannot be redone by an outsider: it needs the freeze commit's history, a Bitcoin
block-explorer lookup and a date window that closed. This script takes the recorded outcome instead.
    python3 fetch_books.py <draw_log.json> <dest dir>      (dest is RUNS/SEC-PG-LLM-H-2026-10-08/raw/books in the work tree)
Gutenberg texts are public domain in the USA; they are fetched from gutenberg.org, not redistributed here."""
import hashlib, json, pathlib, subprocess, sys
draw = json.load(open(sys.argv[1])); dest = pathlib.Path(sys.argv[2]); dest.mkdir(parents=True, exist_ok=True); bad = []
for a in draw['attempts']:
    if not a.get('admitted'): continue
    n = a['ebook']; p = dest / f'pg{n}.txt'
    if not p.exists():
        subprocess.run(['curl', '-sSfL', '--retry', '3', '--max-time', '300', '-o', str(p), f'https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt'], check=True)
    h = hashlib.sha256(p.read_bytes()).hexdigest(); ok = h == a['sha256']; bad += [] if ok else [n]
    print(f"pg{n}.txt  sha256 {h}  {'matches draw_log.json' if ok else 'DIFFERS from draw_log.json ' + a['sha256']}")
if bad: sys.exit(f'Gutenberg has changed {bad}; the frozen runner will refuse (run_heldout.py asserts the hash). Re-score instead.')

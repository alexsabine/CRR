#!/usr/bin/env python3
"""Seen-data register tooling (RT-05). DATA/SEEN.md is append-only: this script adds rows and checks IDs against it.
Row format (one per line, after the header): `| <id> | <kind> | <sha256 or 'n/a'> | <study or source> | <opened_utc> |`.
  python scripts/seen_register.py add --id mnist/train-images-idx3-ubyte --kind dataset-file --sha <hex> --source studies/BENCH1-REAL-DATA-2026-10-06 --when 2026-10-06
  python scripts/seen_register.py check id1 id2 ...      # exit 2 if any id is already seen
  python scripts/seen_register.py list
Used by guard_strict.py to refuse held-out claims on IDs the register already carries."""
import argparse, datetime, fcntl, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]; REG = ROOT / 'DATA' / 'SEEN.md'
def rows():
    out = []
    for line in REG.read_text(encoding='utf-8').splitlines():
        if line.startswith('## Verbatim import'): break  # the verbatim upstream tables below have another column layout and are indexed by the derived IDs above (2026-10-07 fix: their cells were being read as IDs)
        if line.startswith('| ') and not line.startswith('| id ') and not line.startswith('|---'):
            parts = [x.strip() for x in line.strip('|').split('|')]
            if len(parts) >= 5: out.append(dict(id=parts[0], kind=parts[1], sha256=parts[2], source=parts[3], opened_utc=parts[4]))
    return out
def seen_ids(): return {r['id'] for r in rows()}
def add(args):
    lock = ROOT / 'EPISTEMIC' / '.append.lock'; lock.parent.mkdir(exist_ok=True); lf = lock.open('w'); fcntl.flock(lf, fcntl.LOCK_EX)  # exclusive lock while appending (the lock file is git-ignored)
    txt = REG.read_text(encoding='utf-8')
    if '| id |' not in txt: txt = txt.rstrip('\n') + '\n\n| id | kind | sha256 | source | opened_utc |\n|---|---|---|---|---|\n'
    if args.id in seen_ids(): print('already registered:', args.id); return 0
    row = f"| {args.id} | {args.kind} | {args.sha or 'n/a'} | {args.source} | {args.when or datetime.datetime.now(datetime.timezone.utc).date().isoformat()} |"
    if '\n## Verbatim import' in txt:  # 2026-10-09 fix: rows() stops at this heading, so a row appended below it was never indexed; insert above it, as data_step.py register does
        i = txt.index('\n## Verbatim import'); head = txt[:i].rstrip('\n'); j = head.rfind('\n| ')
        k = head.find('\n', j + 1) if j >= 0 else -1  # just after the last table row above the heading, so the row stays inside its table
        txt = (head + '\n' + row if k < 0 else head[:k] + '\n' + row + head[k:]) + '\n' + txt[i:]
    else:
        txt = txt.rstrip('\n') + '\n' + row + '\n'
    REG.write_text(txt, encoding='utf-8'); print('added', args.id); return 0
def check(ids):
    s = seen_ids(); hit = [i for i in ids if i in s]
    print({'seen': hit, 'clean': [i for i in ids if i not in s]}); return 2 if hit else 0
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True); a = sub.add_parser('add'); a.add_argument('--id', required=True); a.add_argument('--kind', required=True); a.add_argument('--sha'); a.add_argument('--source', required=True); a.add_argument('--when'); c = sub.add_parser('check'); c.add_argument('ids', nargs='+'); sub.add_parser('list'); args = ap.parse_args()
    if args.cmd == 'add': sys.exit(add(args))
    elif args.cmd == 'check': sys.exit(check(args.ids))
    else: [print(r) for r in rows()]

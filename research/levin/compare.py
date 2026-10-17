#!/usr/bin/env python3
"""Compare a fresh output with the committed one: byte-identical, else JSON-equal, else report the largest
relative difference between numbers. Usage: python compare.py out/FILE expected/FILE"""
import json, sys

def walk(a, b, path="$"):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            yield path, "keys differ", float("inf"); return
        for k in a: yield from walk(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            yield path, "lengths differ", float("inf"); return
        for i, (x, y) in enumerate(zip(a, b)): yield from walk(x, y, f"{path}[{i}]")
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if a != b: yield path, f"{a!r} vs {b!r}", abs(a - b) / max(abs(a), abs(b), 1e-300)
    elif a != b:
        yield path, "values differ", float("inf")

new, ref = sys.argv[1], sys.argv[2]
if open(new, "rb").read() == open(ref, "rb").read():
    print(f"{ref}: byte-identical"); sys.exit(0)
try:
    diffs = list(walk(json.load(open(new)), json.load(open(ref))))
except json.JSONDecodeError:
    print(f"{ref}: DIFFERS (not JSON, not byte-identical)"); sys.exit(1)
if not diffs:
    print(f"{ref}: JSON-equal"); sys.exit(0)
worst = max(d[2] for d in diffs)
for p, msg, r in diffs: print(f"  {p}: {msg} (relative {r:.1e})")
print(f"{ref}: {len(diffs)} number(s) differ, largest relative difference {worst:.1e}")
sys.exit(0 if worst < 1e-12 else 1)

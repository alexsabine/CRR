"""Byte-level public-domain text (Project Gutenberg, fetched 2026-10-06 into the scratchpad; sha256 in the manifest). Domain A: English fiction (Pride and Prejudice, Moby Dick). Domain B: non-English text (Les Miserables tome I in French; Faust I in German), chosen after the first development pass showed the English-science shift (On the Origin of Species, kept as domain C) forgot only 0.06 nats. Splits: the byte stream is cut into 20 000-byte chunks; chunk i goes to validation if i % 10 == 8, test if i % 10 == 9, development otherwise (contiguity within chunks, representativeness across the whole text; the first pass's tail-split put the book's index into the test slice). No selection decision reads the test slice; the benchmark records test losses during runs."""
import numpy as np, pathlib, hashlib, re
ROOT = pathlib.Path('/tmp/claude-0/-home-user-Phoenix-1-/0f3a1c65-9980-56a0-a5a1-03e6726ded72/scratchpad/gutenberg')
DOMAINS = {'A': ['pg1342.txt', 'pg2701.txt'], 'B': ['pg17489.txt', 'pg2229.txt'], 'C': ['pg1228.txt'], 'D': ['pg4300.txt']}
def _strip(t):
    s = t.find('*** START OF'); e = t.find('*** END OF'); t = t[t.find('\n', s) + 1:e] if s >= 0 and e > s else t
    return re.sub(r'\r\n', '\n', t)
def load(domain):
    txt = ''.join(_strip(open(ROOT / f, encoding='utf-8', errors='replace').read()) for f in DOMAINS[domain]); b = np.frombuffer(txt.encode('utf-8', errors='replace'), dtype=np.uint8)
    CH = 20000; chunks = [b[i:i + CH] for i in range(0, len(b), CH)]; parts = {'dev': [], 'val': [], 'test': []}
    for i, c in enumerate(chunks): parts['val' if i % 10 == 8 else 'test' if i % 10 == 9 else 'dev'].append(c)
    return {k: np.concatenate(v) for k, v in parts.items()}
def sha(): return {f: hashlib.sha256(open(ROOT / f, 'rb').read()).hexdigest() for d in DOMAINS.values() for f in d}
def batches(arr, rng, batch, ctx):
    """random contiguous windows; returns (x, y) int64 arrays"""
    ix = rng.integers(0, len(arr) - ctx - 1, batch); x = np.stack([arr[i:i + ctx] for i in ix]).astype(np.int64); y = np.stack([arr[i + 1:i + ctx + 1] for i in ix]).astype(np.int64); return x, y
def fixed_eval_set(arr, seed, n, ctx):
    rng = np.random.default_rng(seed); return batches(arr, rng, n, ctx)

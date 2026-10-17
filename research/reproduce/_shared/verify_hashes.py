#!/usr/bin/env python3
"""Check that frozen files in this reproduce area are byte-identical to what was hashed before the data were seen.

Not part of the original studies (written for this area; MIT). Standard library only.

    python3 _shared/verify_hashes.py                 # every study under ai-safety/ and continual-learning/
    python3 _shared/verify_hashes.py <study folder>  # one study

Two hash formats occur:
  * Phoenix: src/studies/<ID>/FREEZE.json lists sha256 for every file in the study folder (and HASHES.sha256 is
    the manifest whose sha256 FREEZE.json records). Any extra file (e.g. __pycache__) also breaks the freeze.
  * Ashes: src/prereg/<s>/HASH.txt is `sha256sum` output with paths relative to src/prereg/<s>/.
A match shows the copy equals the hashed bytes. It does NOT show when the hash was made: that rests on the
OpenTimestamps proofs and commits named in each README (anchor status is stated there).
"""
import hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent.parent
# Lines that cannot match, both recorded upstream (they are reported as KNOWN, not as failures):
#  * SCL3 HASH.txt lists ./HASH.txt itself, hashed while it was being written; a file cannot hold its own final hash
#    (Ashes runs/scl3/hash_check.txt, copied to continual-learning/SCL3/expected/hash_check.txt).
#  * SOTA1 HASH.txt lists three vendored-Mammoth files that Mammoth's own .gitignore (*.txt, *.pkl) kept out of the
#    Ashes git history, so they are absent from the public repo at a403a96 and from this copy. None is imported by
#    the SOTA1 code path (two pip requirement lists and an ImageNet-R label table).
KNOWN = {'./HASH.txt': 'self-reference (cannot match by construction)',
         '../../runs/sota1/frozen/mammoth/datasets/imagenet_r_utils/label_to_class_name.pkl': 'never committed upstream (mammoth/.gitignore *.pkl)',
         '../../runs/sota1/frozen/mammoth/requirements.txt': 'never committed upstream (mammoth/.gitignore *.txt)',
         '../../runs/sota1/frozen/mammoth/requirements-optional.txt': 'never committed upstream (mammoth/.gitignore *.txt)'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def phoenix(d):
    m = json.loads((d / 'FREEZE.json').read_bytes())
    files = {p.relative_to(d).as_posix(): sha(p) for p in sorted(d.rglob('*')) if p.is_file()
             and p.relative_to(d).as_posix() not in ('FREEZE.json', 'HASHES.sha256')}
    bad = sorted(k for k in set(files) | set(m['files']) if files.get(k) != m['files'].get(k))
    manifest = ''.join(h + '  ' + k + '\n' for k, h in sorted(m['files'].items())).encode()
    man_ok = (d / 'HASHES.sha256').read_bytes() == manifest and hashlib.sha256(manifest).hexdigest() == m['manifest_sha256']
    return (not bad and man_ok), len(m['files']), bad + ([] if man_ok else ['HASHES.sha256/manifest_sha256'])


def ashes(h):
    bad = []; known = []; n = 0
    for line in h.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1); rel = rel.lstrip('*'); n += 1
        p = (h.parent / rel)
        if not p.exists() or sha(p) != digest:
            (known if rel in KNOWN else bad).append(rel)
    for k in known:
        print(f'KNOWN {h.relative_to(HERE).as_posix()}: {k}: {KNOWN[k]}')
    return not bad, n, bad


def check(study):
    out = []
    for f in sorted(study.glob('src/studies/*/FREEZE.json')):
        out.append((f.parent.relative_to(HERE).as_posix(), *phoenix(f.parent)))
    for h in sorted(study.glob('src/prereg/*/HASH.txt')):
        out.append((h.relative_to(HERE).as_posix(), *ashes(h)))
    return out


if __name__ == '__main__':
    targets = [pathlib.Path(a).resolve() for a in sys.argv[1:]] or \
        sorted({p.parents[3] for p in HERE.glob('*/*/src/studies/*/FREEZE.json')} |
               {p.parents[3] for p in HERE.glob('*/*/src/prereg/*/HASH.txt')} |
               {p.parents[3] for p in HERE.glob('*/*/*/src/prereg/*/HASH.txt')})
    fail = 0
    for t in targets:
        for name, ok, n, bad in check(t):
            print(f"{'OK  ' if ok else 'FAIL'} {name}: {n} hashed files" + ('' if ok else f'; mismatched: {bad}'))
            fail += not ok
    sys.exit(1 if fail else 0)

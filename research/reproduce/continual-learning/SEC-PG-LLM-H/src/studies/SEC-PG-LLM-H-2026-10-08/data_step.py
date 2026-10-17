"""SEC-PG-LLM-H data step (frozen). Run from Phoenix_Egg/ with python3 -I, in this order:
  data_step.py anchor    checks, records RUNS/<id>/anchor_check.json; fetches nothing. Commit and push the file and the upgraded .ots.
  data_step.py draw      fetches and screens the books; appends every attempt to RUNS/<id>/draw_attempts.jsonl as it happens; writes
                         draw_log.json at the end. Resumable: a re-run replays recorded attempts and continues; it never re-decides one.
  data_step.py register  inserts one DATA/SEEN.md row per fetched file (admitted or not) above the '## Verbatim import' header, where
                         scripts/seen_register.py reads them, then checks them with seen_register.

anchor requires (ok = all of them):
  A1 the frozen folder is unchanged: guard.fileset(folder) equals FREEZE.json['files'], sha256(HASHES.sha256) equals manifest_sha256;
  A2 receipts/<id>/FREEZE.json is byte-identical to the study's FREEZE.json, and the OpenTimestamps proof receipts/<id>/FREEZE.json.ots
     (after `ots upgrade`) is a proof for that file: its file digest equals sha256(FREEZE.json);
  A3 the proof carries at least one Bitcoin block-header attestation, and for each one, both public explorers (blockstream.info,
     mempool.space) give the same block hash, and that block's merkle root equals the proof's commitment;
  A4 the earliest attested block's timestamp plus 7200 s (the protocol's tolerance on block times) precedes now;
  A5 the UTC date is on or after max(2026-10-09, the freeze date + 1 day) (R3: the configuration was selected on development data on
     2026-10-08 and must not be used on new data the same calendar day);
  A6 the clone is not shallow, and the freeze commit (the only commit that adds the study's FREEZE.json) holds a FREEZE.json whose
     sha256 equals the stamped one.
  A7 the draw block (Bitcoin height DRAW_BLOCK_HEIGHT, fixed in this file before the freeze) has at least 6 confirmations, and both
     explorers give the same hash for it;
  A8 no draw has started (draw_attempts.jsonl absent), so the anchor record that authorised the draw cannot be rewritten afterwards.
It also records, without requiring it, whether the tag prereg-SEC-PG-LLM-H-2026-10-08 is on origin as an annotated tag object that
points at the freeze commit and carries a signature block (its validity is the reviewer's to verify); a lightweight tag does not count.
draw requires: anchor_check.json ok, identical to its committed version, and that commit contained in origin's branch or main; now before
FINAL_DRAW (earliest data date + 7 days; after that the study is NOT DECIDABLE); and either the tag present at the anchor check, or now >=
the tag deadline (earliest data date + 12 h), after which the draw proceeds without the tag and the study is capped at a weak-anchor PASS-0.
Draw rule: for pool P and ebook n, key = sha256('<freeze commit>|<hash of block DRAW_BLOCK_HEIGHT>|<P>|<n>'). The height was fixed when this
file was frozen, about 12 hours ahead of the chain tip, so the hash was unknowable at the freeze and cannot be chosen afterwards. Candidates
are tried in increasing key order until the quota is admitted (EN 2, FR 1, DE 1), at most MAX_TRIES per pool (else NOT DECIDABLE); a
candidate already in DATA/SEEN.md at draw time is skipped and recorded as 'S0 already seen'. Seeds: for i = 0..N_SEEDS-1,
100000 + int(sha256('<freeze commit>|<block hash>|seed|<i>')[:8], 16) mod 800000.
Fetch: URL https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt. HTTP 404 or 410 is a rejection under S1. Any other HTTP error or a
network error is retried (4 attempts, 5/10/20 s apart); if it persists, the draw stops without recording a decision for that candidate
and can be resumed later.
Screens: S1 HTTP 200; S2 at most 0.1 % replacement characters after UTF-8 decoding; S3 '*** START OF' and '*** END OF' present in that
order; S4 stripped size (T4's data._strip, UTF-8 bytes) within SIZE[P]; S5 the most frequent lower-case word of the stripped text in WORDS[P]."""
import sys; sys.dont_write_bytecode = True
import os, json, re, time, hashlib, datetime, subprocess, pathlib, urllib.request, urllib.error, collections
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; SID = HERE.name; RUN = ROOT / 'RUNS' / SID; RAW = RUN / 'raw'; REC = ROOT / 'receipts' / SID
sys.path.insert(0, str(ROOT / 'scripts'))
FIXED_EARLIEST = '2026-10-09'; TAG = 'prereg-SEC-PG-LLM-H-2026-10-08'; TAG_GRACE_H = 12; FINAL_DRAW_DAYS = 7; DRAW_BLOCK_HEIGHT = 970552; CONFIRMATIONS = 6
N_SEEDS = 8; QUOTA = {'EN': 2, 'FR': 1, 'DE': 1}; MAX_TRIES = 12; PAUSE = 2.0; BLOCK_SLACK = 7200
SIZE = {'EN': (300_000, 2_500_000), 'FR': (200_000, 2_500_000), 'DE': (200_000, 2_500_000)}
WORDS = {'EN': {'the', 'and', 'of', 'to', 'a', 'i'}, 'FR': {'de', 'la', 'le', 'et', 'les', 'à', 'il'}, 'DE': {'der', 'die', 'und', 'sie', 'ich', 'er', 'das', 'zu'}}
URL = 'https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt'; EXPLORERS = ['https://blockstream.info/api', 'https://mempool.space/api']
class Transient(Exception): pass
def now(): return datetime.datetime.now(datetime.timezone.utc)
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)
def get(url, timeout=60, tries=4):
    req = urllib.request.Request(url, headers={'User-Agent': 'Phoenix-SEC-PG-LLM-H data step'})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r: return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410): return e.code, b''
            err = f'HTTP {e.code}'
        except Exception as e: err = repr(e)[:200]
        if i < tries - 1: time.sleep(5*2**i)
    raise Transient(err)
def frozen_ok(study=HERE):
    """A1: the folder's files and bytes equal FREEZE.json's record (the same test append_result_v2 applies); also used by the runner and the scorer"""
    import guard
    m = json.loads((study / 'FREEZE.json').read_bytes()); fs = guard.fileset(study); bad = sorted(k for k in set(fs) | set(m['files']) if fs.get(k) != m['files'].get(k))
    man = sha((study / 'HASHES.sha256').read_bytes()) == m['manifest_sha256']; return (not bad and man), bad, m
def freeze_commit():
    out = git('log', '--diff-filter=A', '--format=%H', '--', str(HERE / 'FREEZE.json')).stdout.split()
    return out[0] if len(out) == 1 else None
def block(h):
    res = {}
    for ex in EXPLORERS:
        try:
            _, bh = get(f'{ex}/block-height/{h}', 30); _, blk = get(f'{ex}/block/{bh.decode().strip()}', 30); b = json.loads(blk)
            res[ex] = dict(hash=b['id'], merkle_root=b['merkle_root'], timestamp=b['timestamp'])
        except Exception as e: res[ex] = dict(error=repr(e)[:300])
    return res
def anchor():
    from opentimestamps.core.timestamp import DetachedTimestampFile
    from opentimestamps.core.serialize import StreamDeserializationContext
    from opentimestamps.core.notary import BitcoinBlockHeaderAttestation
    RUN.mkdir(parents=True, exist_ok=True); t = now(); res = dict(checked_utc=t.isoformat())
    if (RUN / 'draw_attempts.jsonl').exists(): raise SystemExit('A8: the draw has started; the anchor record is final')
    ok1, bad, m = frozen_ok(); res['A1_frozen_unchanged'] = ok1; res['A1_mismatched_files'] = bad
    fz = (HERE / 'FREEZE.json').read_bytes(); res['freeze_sha256'] = sha(fz)
    rec_same = (REC / 'FREEZE.json').exists() and (REC / 'FREEZE.json').read_bytes() == fz
    up = subprocess.run(['ots', 'upgrade', str(REC / 'FREEZE.json.ots')], capture_output=True, text=True); res['ots_upgrade_output'] = (up.stdout + up.stderr)[-3000:]
    with open(REC / 'FREEZE.json.ots', 'rb') as fd: dtf = DetachedTimestampFile.deserialize(StreamDeserializationContext(fd))
    res['ots_file_digest'] = dtf.file_digest.hex(); res['A2_proof_for_this_freeze'] = bool(rec_same and res['ots_file_digest'] == res['freeze_sha256'])
    atts = sorted({(a.height, msg[::-1].hex()) for msg, a in dtf.timestamp.all_attestations() if isinstance(a, BitcoinBlockHeaderAttestation)}); res['attestations'] = []
    for h, root in atts:
        b = block(h); hashes = {v.get('hash') for v in b.values()}; roots = {v.get('merkle_root') for v in b.values()}
        res['attestations'].append(dict(height=h, proof_merkle_root=root, explorers=b, explorers_agree=len(hashes) == 1 and None not in hashes, merkle_matches=roots == {root}))
    good = [a for a in res['attestations'] if a['explorers_agree'] and a['merkle_matches']]
    res['A3_bitcoin_attestation_verified'] = bool(atts) and len(good) == len(atts)
    if good:
        e = min(good, key=lambda a: a['height']); ts = max(v['timestamp'] for v in e['explorers'].values())
        res['earliest_block'] = dict(height=e['height'], hash=next(iter(e['explorers'].values()))['hash'], timestamp=ts, utc=datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).isoformat())
        res['A4_attested_before_now_with_slack'] = ts + BLOCK_SLACK < t.timestamp()
    else: res['A4_attested_before_now_with_slack'] = False
    fdate = datetime.datetime.fromisoformat(m['local_created_utc']).date(); earliest = max(FIXED_EARLIEST, (fdate + datetime.timedelta(days=1)).isoformat())
    res['earliest_data_date'] = earliest; res['A5_date_ok'] = t.date().isoformat() >= earliest
    shallow = git('rev-parse', '--is-shallow-repository').stdout.strip() == 'true'; fc = freeze_commit(); res['freeze_commit'] = fc
    rel = (HERE / 'FREEZE.json').relative_to(ROOT).as_posix(); at_fc = subprocess.run(['git', 'show', f'{fc}:./{rel}'], cwd=ROOT, capture_output=True).stdout if fc else b''
    res['A6_history_ok'] = bool(not shallow and fc and sha(at_fc) == res['freeze_sha256'])
    lr = git('ls-remote', '--tags', 'origin', TAG, TAG + '^{}').stdout.split(); refs = dict(zip(lr[1::2], lr[0::2])); tsha = refs.get(f'refs/tags/{TAG}')
    peeled = refs.get(f'refs/tags/{TAG}^{{}}'); ttype = ''; tagobj = ''
    if tsha:
        git('fetch', '-q', 'origin', f'+refs/tags/{TAG}:refs/phoenix-check/{TAG}')
        if git('rev-parse', f'refs/phoenix-check/{TAG}').stdout.strip() == tsha: ttype = git('cat-file', '-t', tsha).stdout.strip(); tagobj = git('cat-file', 'tag', tsha).stdout if ttype == 'tag' else ''
    res['tag'] = dict(name=TAG, on_origin=bool(tsha), tag_object_sha=tsha, object_type=ttype, annotated=ttype == 'tag', points_to_freeze_commit=bool(fc) and peeled == fc,
                      signature_block_present=('BEGIN PGP SIGNATURE' in tagobj or 'BEGIN SSH SIGNATURE' in tagobj), verified_by='the reviewer (git tag -v, or GitHub verification)')
    res['tag_ok_for_draw'] = bool(res['tag']['on_origin'] and res['tag']['annotated'] and res['tag']['points_to_freeze_commit'] and res['tag']['signature_block_present'])
    db = block(DRAW_BLOCK_HEIGHT); hs = {v.get('hash') for v in db.values()}; tip = []
    for ex in EXPLORERS:
        try: tip.append(int(get(f'{ex}/blocks/tip/height', 30)[1]))
        except Exception: pass
    res['draw_block'] = dict(height=DRAW_BLOCK_HEIGHT, explorers=db, hash=next(iter(hs)) if len(hs) == 1 and None not in hs else None, tip=min(tip) if tip else None)
    res['A7_draw_block_confirmed'] = bool(res['draw_block']['hash'] and tip and min(tip) >= DRAW_BLOCK_HEIGHT + CONFIRMATIONS - 1)
    res['tag_deadline_utc'] = (datetime.datetime.fromisoformat(earliest + 'T00:00:00+00:00') + datetime.timedelta(hours=TAG_GRACE_H)).isoformat()
    res['final_draw_utc'] = (datetime.datetime.fromisoformat(earliest + 'T00:00:00+00:00') + datetime.timedelta(days=FINAL_DRAW_DAYS)).isoformat()
    res['ok'] = all(res[k] for k in ('A1_frozen_unchanged', 'A2_proof_for_this_freeze', 'A3_bitcoin_attestation_verified', 'A4_attested_before_now_with_slack', 'A5_date_ok', 'A6_history_ok', 'A7_draw_block_confirmed'))
    json.dump(res, open(RUN / 'anchor_check.json', 'w'), indent=1); print(json.dumps({k: v for k, v in res.items() if k not in ('ots_upgrade_output', 'attestations')}, indent=1)); return 0 if res['ok'] else 2
def strip_words(b):
    sys.path.insert(0, str(HERE / 'llm')); from data import _strip
    t = _strip(b.decode('utf-8', errors='replace')); words = re.findall(r'\w+', t.lower())
    return len(t.encode('utf-8', errors='replace')), (collections.Counter(words).most_common(1)[0][0] if words else '')
def draw():
    p = RUN / 'anchor_check.json'; a = json.loads(p.read_bytes())
    if not a.get('ok'): raise SystemExit('anchor check not ok')
    rel = p.relative_to(ROOT).as_posix(); head = subprocess.run(['git', 'show', f'HEAD:./{rel}'], cwd=ROOT, capture_output=True).stdout
    if head != p.read_bytes(): raise SystemExit('anchor_check.json differs from its committed version')
    c = git('log', '-1', '--format=%H', '--', rel).stdout.strip(); git('fetch', '-q', 'origin')
    if not any(git('merge-base', '--is-ancestor', c, f'origin/{b}').returncode == 0 for b in ('main', 'claude/ecstatic-hawking-26npxo')): raise SystemExit('anchor_check.json commit is not on origin')
    if now() >= datetime.datetime.fromisoformat(a['final_draw_utc']): raise SystemExit('past the final draw date: the study is NOT DECIDABLE')
    if not a['tag_ok_for_draw'] and now() < datetime.datetime.fromisoformat(a['tag_deadline_utc']): raise SystemExit(f"signed tag {TAG} not on origin at the anchor check; re-run anchor once it is, or draw after {a['tag_deadline_utc']}")
    ok1, bad, _ = frozen_ok()
    if not ok1: raise SystemExit(f'frozen files changed: {bad}')
    if (RUN / 'draw_log.json').exists(): raise SystemExit('draw_log.json exists: the draw is complete')
    import seen_register
    fc, bh = a['freeze_commit'], a['draw_block']['hash']; pools = json.load(open(HERE / 'pools.json'))['pools']; (RAW / 'books').mkdir(parents=True, exist_ok=True)
    AT = RUN / 'draw_attempts.jsonl'; prior = {}; seen_now = seen_register.seen_ids()
    if AT.exists():
        if AT.read_bytes() and not AT.read_bytes().endswith(b'\n'):
            with open(AT, 'a') as fh: fh.write('\n')
        for line in AT.read_text().splitlines():
            try: r = json.loads(line); prior[(r['pool'], r['ebook'])] = r
            except ValueError: pass
    key = lambda P, n: sha(f'{fc}|{bh}|{P}|{n}'.encode()); admitted = {}; started = now().isoformat()
    for P in ('EN', 'FR', 'DE'):
        got = []
        for n in sorted(pools[P], key=lambda n: key(P, n))[:MAX_TRIES]:
            if len(got) == QUOTA[P]: break
            if (P, n) in prior:
                rec = prior[(P, n)]
                if rec.get('key') != key(P, n): raise SystemExit(f'recorded attempt for {P} pg{n} has a different key')
            elif f'gutenberg/pg{n}.txt' in seen_now:
                rec = dict(pool=P, ebook=n, key=key(P, n), fetched_utc=None, sha256=None, admitted=False, reason='S0 already seen')
                with open(AT, 'a') as fh: fh.write(json.dumps(rec) + '\n')
            else:
                rec = dict(pool=P, ebook=n, url=URL.format(n=n), key=key(P, n), fetched_utc=now().isoformat())
                try: status, b = get(rec['url'])
                except Transient as e: raise SystemExit(f'transient fetch failure at {P} pg{n}: {e}; nothing recorded for it; re-run draw later')
                rec['http'] = status; rec['bytes'] = len(b); rec['sha256'] = sha(b) if b else None; reason = None
                if status != 200 or not b: reason = 'S1 not available'
                else:
                    (RAW / 'books' / f'pg{n}.txt').write_bytes(b); txt = b.decode('utf-8', errors='replace'); rep = txt.count('�')/max(1, len(txt)); rec['replacement_frac'] = rep
                    s, e = txt.find('*** START OF'), txt.find('*** END OF')
                    if rep > 0.001: reason = 'S2 decoding'
                    elif not (s >= 0 and e > s): reason = 'S3 markers'
                    else:
                        size, top = strip_words(b); rec['stripped_bytes'] = size; rec['top_word'] = top
                        if not (SIZE[P][0] <= size <= SIZE[P][1]): reason = 'S4 size'
                        elif top not in WORDS[P]: reason = 'S5 language word'
                rec['admitted'] = reason is None; rec['reason'] = reason or 'admitted'
                with open(AT, 'a') as fh: fh.write(json.dumps(rec) + '\n')
                print(json.dumps(rec), flush=True); time.sleep(PAUSE)
            if rec['admitted']: got.append(n)
        admitted[P] = got
    attempts = []
    for l in AT.read_text().splitlines():
        try: attempts.append(json.loads(l))
        except ValueError: pass
    log = dict(freeze_commit=fc, block_hash=bh, block_height=DRAW_BLOCK_HEIGHT, anchor_commit=c, anchor_check_sha256=sha(p.read_bytes()), anchor_checked_utc=a['checked_utc'], tag_ok_at_anchor=a['tag_ok_for_draw'],
               attested_block_utc=a['earliest_block']['utc'], attested_block_timestamp=a['earliest_block']['timestamp'], started_utc=started, attempts=attempts, admitted=admitted,
               ok=all(len(admitted[P]) == QUOTA[P] for P in QUOTA), domain_A_files=[f'pg{n}.txt' for n in admitted['EN']], domain_B_files=[f'pg{n}.txt' for n in admitted['FR'] + admitted['DE']])
    seeds = [100000 + int(sha(f'{fc}|{bh}|seed|{i}'.encode())[:8], 16) % 800000 for i in range(N_SEEDS)]; assert len(set(seeds)) == N_SEEDS; log['seeds'] = seeds
    fetched = [r['fetched_utc'] for r in attempts if r.get('fetched_utc')]; log['first_fetch_utc'] = min(fetched) if fetched else None; log['finished_utc'] = now().isoformat()
    json.dump(log, open(RUN / 'draw_log.json', 'w'), indent=1); print(json.dumps({k: log[k] for k in ('ok', 'admitted', 'domain_A_files', 'domain_B_files', 'seeds')}, indent=1)); return 0 if log['ok'] else 2
def register():
    import seen_register
    log = json.load(open(RUN / 'draw_log.json')); reg = ROOT / 'DATA' / 'SEEN.md'; txt = reg.read_text(encoding='utf-8'); have = seen_register.seen_ids(); rows = []
    for r in log['attempts']:
        rid = f"gutenberg/pg{r['ebook']}.txt"
        if r.get('sha256') and rid not in have: rows.append(f"| {rid} | public-domain text (byte-level corpus; LLM-exposed; {'admitted' if r['admitted'] else 'fetched, rejected by ' + r['reason']}) | {r['sha256']} | studies/{SID} data step | {r['fetched_utc'][:10]} |")
    if rows:
        i = txt.index('## Verbatim import'); reg.write_text(txt[:i].rstrip('\n') + '\n' + '\n'.join(rows) + '\n\n' + txt[i:], encoding='utf-8')
    ids = [f"gutenberg/pg{r['ebook']}.txt" for r in log['attempts'] if r.get('sha256')]; import importlib; importlib.reload(seen_register); missing = [i for i in ids if i not in seen_register.seen_ids()]
    print(len(rows), 'rows inserted;', len(ids), 'fetched ids;', 'not registered:', missing); return 0 if ids and not missing else 1
if __name__ == '__main__': sys.exit({'anchor': anchor, 'draw': draw, 'register': register}[sys.argv[1]]())

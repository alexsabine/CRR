"""SEC-PG-LLM-H receipts (frozen). From Phoenix_Egg/, after the scorer: python3 -I studies/SEC-PG-LLM-H-2026-10-08/make_receipts.py
Writes into receipts/<id>/ the files scripts/append_result_v2.py (LA-1) reads:
  exposure_log.json   study_id; holdout_ids = every fetched file (admitted or rejected); first_exposure_utc = the first fetch (draw_log.json)
  data_manifest.json  records: one per fetched file (id, sha256, pool, admitted, reason)
  rerun_a.json, rerun_b.json  the frozen scorer's stdout from two further executions; each must equal RUNS/<id>/score.json byte for byte
  receipt.json        study_id, freeze_sha256, outcomes_sha256 (score.json), the paths above, and the provenance facts recorded at draw
                      time (tag_ok_at_anchor, attested block time, anchor check time). It is self-declared: the reviewer verifies the tag
                      signature and the Bitcoin attestation independently, and fills in their own fields in the ledger entry.
anchor_github_commit.json (the freeze commit as GitHub records it) is written by the operator at step 2 of PREREG.md's order of operations.
Exits non-zero if either rerun differs from score.json."""
import sys; sys.dont_write_bytecode = True
import json, hashlib, pathlib, subprocess, datetime
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; SID = HERE.name; RUN = ROOT / 'RUNS' / SID; REC = ROOT / 'receipts' / SID
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    REC.mkdir(parents=True, exist_ok=True); draw = json.load(open(RUN / 'draw_log.json')); outcomes = (RUN / 'score.json').read_bytes()
    fetched = [a for a in draw['attempts'] if a.get('sha256')]
    exp = dict(study_id=SID, holdout_ids=[f"gutenberg/pg{a['ebook']}.txt" for a in fetched], first_exposure_utc=draw['first_fetch_utc'])
    man = dict(study_id=SID, records=[dict(id=f"gutenberg/pg{a['ebook']}.txt", sha256=a['sha256'], pool=a['pool'], admitted=a['admitted'], reason=a['reason']) for a in fetched])
    (REC / 'exposure_log.json').write_text(json.dumps(exp, indent=1) + '\n'); (REC / 'data_manifest.json').write_text(json.dumps(man, indent=1) + '\n')
    ok = True
    for name in ('rerun_a.json', 'rerun_b.json'):
        out = subprocess.run([sys.executable, '-I', str(HERE / 'score_llmh.py'), str(HERE)], capture_output=True, cwd=str(HERE)).stdout
        (REC / name).write_bytes(out); ok = ok and out == outcomes
    rc = dict(study_id=SID, freeze_sha256=sha((HERE / 'FREEZE.json').read_bytes()), outcomes_sha256=sha(outcomes), outcomes_path=f'RUNS/{SID}/score.json',
              exposure_log=dict(path='exposure_log.json', sha256=sha((REC / 'exposure_log.json').read_bytes())), data_manifest=dict(path='data_manifest.json', sha256=sha((REC / 'data_manifest.json').read_bytes())),
              rerun_a=dict(path='rerun_a.json', sha256=sha((REC / 'rerun_a.json').read_bytes())), rerun_b=dict(path='rerun_b.json', sha256=sha((REC / 'rerun_b.json').read_bytes())), reruns_identical_to_outcomes=ok,
              provenance_at_draw=dict(freeze_commit=draw['freeze_commit'], anchor_commit=draw['anchor_commit'], anchor_checked_utc=draw['anchor_checked_utc'], attested_block_utc=draw['attested_block_utc'], tag_ok_at_anchor=draw['tag_ok_at_anchor'], first_fetch_utc=draw['first_fetch_utc']),
              signed_tag_rule="enter signed_tag='verified' in the LA-1 entry only if tag_ok_at_anchor is true and the reviewer verifies the signature; otherwise 'none' (PREREG.md)",
              self_declared='written by the operator; not independent verification', recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (REC / 'receipt.json').write_text(json.dumps(rc, indent=1) + '\n'); print(json.dumps({k: rc[k] for k in ('freeze_sha256', 'outcomes_sha256', 'reruns_identical_to_outcomes')})); return 0 if ok else 2
if __name__ == '__main__': sys.exit(main())

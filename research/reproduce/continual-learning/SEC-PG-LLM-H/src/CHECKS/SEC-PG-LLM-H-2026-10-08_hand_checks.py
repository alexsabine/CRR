"""Hand checks for SEC-PG-LLM-H RESULT (Daniel Friedman's audit asks; written 2026-10-09 before the run finished).
Not part of the frozen protocol and not a scorer: it reads the run's outputs and reports facts RESULT.md must state.
Run from Phoenix_Egg/:  python3 -I CHECKS/SEC-PG-LLM-H-2026-10-08_hand_checks.py  (writes RUNS/<id>/hand_checks.json)

#6  repeat pair: units_rerun.jsonl holds exactly (seed0, 128, 2M, 'pretrain+pg') and (seed0, 64, 1M, 'sec'), once each, and
    score.json reports both identical (deterministic_repeat alone only counts two identical rows).
#10 sensitivity: every one of the 8 cells appears exactly once for every (seed, width, tokens); a duplicate would silently
    overwrite another in score_llmh.py's dict. The same uniqueness is checked for main and pretrain units.
#27 timers: 'seconds' measures different work across arms; the code lines that show it are quoted, and RESULT must draw no
    SEC-vs-PG cost comparison from them.
Timing: first fetch, attestation block time and anchor time from the run's own records; committer dates are not used.
#25: path_length is a checkpoint chord length (stride 100); the code line is quoted.
"""
import json, pathlib, collections, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
SID = 'SEC-PG-LLM-H-2026-10-08'
RUN = ROOT / 'RUNS' / SID; STUDY = ROOT / 'studies' / SID
CFG = json.load(open(STUDY / 'config.json')); DRAW = json.load(open(RUN / 'draw_log.json'))
SEEDS = DRAW['seeds']; WIDTHS = [64, 128, 192]; MAT = [1_000_000, 2_000_000, 8_000_000]
GRID = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4]
MAIN_ARMS = ['frozen', 'none'] + [f'grid_{int(l)}' for l in GRID] + ['sec', 'pg', 'light', 'pgconst', 'gpm_only']
SENS = [f'sens_{k}' for k in CFG['sensitivity']]


def load(stage):
    p = RUN / f'units_{stage}.jsonl'
    return [json.loads(l) for l in open(p) if l.strip()] if p.exists() else []


def counts(rows):
    return collections.Counter((r['seed'], r['d'], r['tokens'], r['arm']) for r in rows)


out = {'study': SID}
cells = [(s, d, t) for s in SEEDS for d in WIDTHS for t in MAT]
for stage, arms in (('pretrain', ['pre']), ('main', MAIN_ARMS), ('sens', SENS)):
    c = counts(load(stage))
    expected = {(*cell, a) for cell in cells for a in arms}
    out[stage] = dict(rows=sum(c.values()), expected=len(expected),
                      missing=sorted(map(str, expected - set(c))), duplicates=sorted(str(k) for k, v in c.items() if v > 1),
                      unexpected=sorted(str(k) for k in set(c) - expected))
    out[stage]['ok'] = not out[stage]['missing'] and not out[stage]['duplicates'] and not out[stage]['unexpected']
rr = counts(load('rerun'))
want = {(SEEDS[0], 128, 2_000_000, 'pretrain+pg'): 1, (SEEDS[0], 64, 1_000_000, 'sec'): 1}
score = json.load(open(RUN / 'score.json')) if (RUN / 'score.json').exists() else {}
out['repeat_pair_6'] = dict(rows={str(k): v for k, v in rr.items()}, exactly_prescribed=dict(rr) == want,
                            scorer_rerun=score.get('rerun'), scorer_deterministic_repeat=(score.get('pass1_scorer_preconditions') or {}).get('items', {}).get('deterministic_repeat'))
out['repeat_pair_6']['ok'] = bool(out['repeat_pair_6']['exactly_prescribed'] and score.get('rerun') and all(x['identical'] for x in score['rerun']))
out['sensitivity_10'] = dict(all_8_once_per_cell=out['sens']['ok'], keys=SENS)


def grep(path, pat):
    for i, l in enumerate(open(path), 1):
        if re.search(pat, l):
            return f'{path.relative_to(ROOT)}:{i}: {l.strip()[:200]}'
    return None


out['timers_27'] = dict(note="RESULT must draw no SEC-vs-PG cost comparison from 'seconds' or descriptive.seconds; arms pg, light, pgconst, gpm_only include 4 evaluations, while none, sec and grid_* exclude them",
                        sec_pg_seconds_line=grep(STUDY / 'sec_pg.py', r'seconds'), cl_seconds_line=grep(STUDY / 'llm' / 'cl.py', r'out = dict\(rule=rule, lam=lam'))
out['path_length_25'] = dict(note='path_length is a checkpoint chord length at stride 100, not optimizer-step travel',
                             line=grep(STUDY / 'llm' / 'cl.py', r's % 100 == 0: cur = flat'))
anchor = json.load(open(RUN / 'anchor_check.json'))
out['timing'] = dict(attested_block=anchor.get('earliest_block'), anchor_checked_utc=anchor.get('checked_utc'), tag=anchor.get('tag'),
                     first_fetch_utc=DRAW.get('first_fetch_utc'), draw_block=DRAW.get('block_height'), tag_ok_at_anchor=DRAW.get('tag_ok_at_anchor'),
                     note='chronology from the OTS attestation and the run records; push times from GitHub push events; committer dates not used')
out['frozen_unchanged_at_score'] = score.get('frozen_unchanged')
out['all_ok'] = all([out['pretrain']['ok'], out['main']['ok'], out['sens']['ok'], out['repeat_pair_6']['ok']]) if score else None
(RUN / 'hand_checks.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps({k: (v.get('ok') if isinstance(v, dict) and 'ok' in v else v) for k, v in out.items() if k in ('pretrain', 'main', 'sens', 'repeat_pair_6', 'all_ok')}, indent=1))

# Inspect and re-run the code

This folder holds the code, the preregistrations and the recorded outputs behind the AI-safety and continual-learning
results of the CRR programme, and one thermodynamics check, arranged so that a machine-learning specialist can read them, re-run them, and check the
outputs against what was recorded.

**What the record shows, in one paragraph.** Where these studies pass, they **match established methods**: utility
indifference and safe interruptibility, the Kalman missing-observation filter, EWC with a tuned penalty weight, GPM with
a constant anchor, ordinary checkpoint resume. **None of them clearly beats an established method.** Several reduce
to one exactly, and the scorers say so (`REDUCES`). The failures are **included on purpose**: SEC3, SEC5, SOTA1, EQ3,
EQ4 and the P18B pilot are part of the honest record, with the same code, data recipes and committed outputs as the
passes. No result here is a CRR-specific effect, and none has been independently replicated.

## The studies

Verdicts are quoted as the record states them, with the source file and line in each study's README. Effort is for a
4-core CPU machine; **no study needs a GPU**.

| ID | area | question (one line) | verdict as recorded | what it matched | effort | folder |
|---|---|---|---|---|---|---|
| P16-PAUSE1 | AI safety | Does valuing time on the agent's own clock (a lossless pause) remove the incentive to disable the off-switch? | **REDUCES** (H1 100 %/100 %; limits L1 59 %, L2 100 %) | utility indifference; safe interruptibility | Easy (~6 min) | [ai-safety/P16-PAUSE1](ai-safety/P16-PAUSE1) |
| SCL1-1 (Ashes) | AI safety | The same pause inside a real continual learner, 12 seen PMLB sets | **holds** 12/12 (a check of the construction, not support for CRR) | (construction check) | Easy rescore; Easy–moderate full | [ai-safety/P16-PAUSE1/companion-ashes-SCL1](ai-safety/P16-PAUSE1/companion-ashes-SCL1) |
| SCL2-1 (Ashes) | AI safety | The same on 9 unseen PMLB sets | **holds** 9/9 (construction check) | (construction check) | Easy rescore; Easy–moderate full | [ai-safety/P16-PAUSE1/companion-ashes-SCL2](ai-safety/P16-PAUSE1/companion-ashes-SCL2) |
| P14-EMPTY1 | AI safety | Should a bit-identical repeated observation be treated as "no evidence" (no update, keep propagating)? | **SCORED, threshold met** 600/600 (Hoeffding lower bound +0.1796); no verdict word claimed until a reviewer completes the receipt; ceiling PASS-0 | Kalman missing-observation filter | Easy (~5 min) | [ai-safety/P14-EMPTY1](ai-safety/P14-EMPTY1) |
| SEC-OBS1-H | AI safety | Does observation-awareness help a continual learner decide when to protect old knowledge? | H1 **PASS**, H2 **NO**, H3 **FAIL**, H4 **PASS** (abstention, balanced accuracy 0.944) | EWC-style anchor + GPM; H4 gives no gain over a transferred constant | Easy rescore (~10 min); Moderate full (16 min wall) | [ai-safety/SEC-OBS1-H](ai-safety/SEC-OBS1-H) |
| P18-LOOP1 | AI safety | Can provenance (which of my outputs re-entered my inputs) localise a gamed channel in a feedback loop? | **development only** (no prereg): provenance 0.96–0.985 vs event log 0.32–0.645, but causal intervention 0.975–0.98 | randomised intervention (native causal rival) does as well | Easy (~20 CPU-min) | [ai-safety/P18-LOOP1](ai-safety/P18-LOOP1) |
| P18B | AI safety | Pre-freeze pilot of a lagged-provenance test | **NO-GO** (MP5/C1: passive_ri sensitivity 0.627 < 0.80); nothing frozen | — | Easy tiny (~2 min); Moderate pilot (0.9 CPU-h) | [ai-safety/P18B](ai-safety/P18B) |
| RW1 (Ashes) | AI safety | Is Hugging Face Trainer's resume already an "empty cut" (bitwise-identical continuation)? | **holds**: "the existing stack's resume is an empty cut on this setting" (declared note, R4; not a prereg) | ordinary checkpoint resume | Moderate (~1 h, ~2.5 GB models, ~10 GB disk) | [ai-safety/RW1](ai-safety/RW1) |
| SEC-PG-LLM-H | continual learning | Held-out Gutenberg books, byte-level Transformer: does SEC-PG beat tuned and constant anchors? | **REDUCES** (K5: SEC-PG − pgconst +0.0013 [−0.0008, +0.0035]); grade none | GPM with a constant anchor of matched size | Easy rescore (~1 min); **Hard** full (~27 CPU-h) | [continual-learning/SEC-PG-LLM-H](continual-learning/SEC-PG-LLM-H) |
| SCL3 (Ashes) | continual learning | Can one self-calibrated EWC weight (SEC) replace a 17-point λ sweep? 10 unseen OpenML sets | **PASS-0** on SCL3-1..4 (SCL3-3 9/10); PASS-1 not reached (FRAGILE) | EWC with a tuned λ (prior art: KNOWN) | Easy rescore; Easy–moderate full (~98 MB) | [continual-learning/SCL3](continual-learning/SCL3) |
| SEC3 (Ashes) | continual learning | Replication of SCL3-3 on a second family | **FAIL** (SEC3-3 4/6, need 5) | — | Easy rescore; Moderate full (~328 MB) | [continual-learning/SEC3](continual-learning/SEC3) |
| SEC4 (Ashes) | continual learning | Clipped SEC within a step of tuned λ, third family | **PASS-1** (SEC4-1 6/6); post hoc: a learner frozen after task 1 also meets the criterion on 5/6 | EWC with a tuned λ (prior art: KNOWN) | Easy rescore; Easy–moderate full (~21 MB, ~4 min) | [continual-learning/SEC4](continual-learning/SEC4) |
| SEC5 (Ashes) | continual learning | Replication of SEC4-1 on a fourth family | **FAIL** (4/8, need 6) | — | Easy rescore; Moderate full (~204 MB) | [continual-learning/SEC5](continual-learning/SEC5) |
| SEC6R (Ashes) | continual learning | Same criterion with an instrument gate (does a frozen learner also pass?) | gate **CLOSED**; SEC6R-1 **PASS-0, UNINFORMATIVE** (7/9) | a learner frozen after task 1 | Easy rescore; Moderate full (~140 MB) | [continual-learning/SEC6R](continual-learning/SEC6R) |
| SOTA1 (Ashes) | continual learning | Online Split-CIFAR-100: CRR learner vs ER, ER-ACE, DER++, X-DER (Mammoth) | **FAIL / FAIL** (behind ER-ACE, d = −3.30); SOTA1-2 **FAIL**; pause check holds | ER-ACE best (21.90 vs CRR 18.60) | Easy rescore (seconds); **Hard** full (~30 unit-h) | [continual-learning/SOTA1](continual-learning/SOTA1) |
| EQ2 (Ashes) | continual learning | Does the equanimity rule (Ω = 1) replace a tuned EWC λ? 3 PMLB sets | **PASS, FRAGILE** → relabelled **PASS-0 (provisional)**; replication failed (EQ3) | EWC with a tuned λ | Easy rescore; Easy–moderate full | [continual-learning/EQ2](continual-learning/EQ2) |
| EQ3 (Ashes) | continual learning | Replication of EQ2 on 6 unseen PMLB sets | **FAIL** (fars behind by 3.74) | — | Easy rescore; Easy–moderate full | [continual-learning/EQ3](continual-learning/EQ3) |
| EQ4 (Ashes) | continual learning | Bounded equanimity rule on 6 PMLB sets | **FAIL** (4/6); EQ4-1r **FAIL** | — | Easy rescore; Easy–moderate full | [continual-learning/EQ4](continual-learning/EQ4) |
| LANDAUER-CRR | thermodynamics | Does each cut release one bit as heat, and what does settling a choice cost? | literal hypothesis **WRONG**; one prediction **FAIL** (P4b); corrected reading holds and **REDUCES** to Landauer + Sivak–Crooks (declared-synthetic, no PASS possible) | Landauer bound; thermodynamic length (Sivak & Crooks 2012) | Easy (~2 min) | [thermodynamics/LANDAUER-CRR](thermodynamics/LANDAUER-CRR) |

Verdict words (from the programme's own scale): **PASS-0** a preregistered pass on unseen data with a weak ceiling;
**PASS-1** additionally robust to its sensitivity cells, controls hold and the anchor is strong; **REDUCES** the method is
shown not to differ from a named established method; **FAIL**; **NOT DECIDABLE**; **NO-GO** a pilot's go/no-go rule
said "do not freeze"; **holds** a check that can only fail on an implementation error.

## What was verified for this folder (2026-10-17)

Each study README has a "Verified re-run" line. In short:

| study | what was re-run here | outcome |
|---|---|---|
| P16-PAUSE1 | full: generate 600 worlds + frozen scorer | data manifest and `outcomes.json` **byte-identical** |
| P14-EMPTY1 | full: generate 2400 worlds + frozen scorer + locked decision engine | manifest and `outcomes.json` **byte-identical**; decision table reproduced |
| P18-LOOP1 | full: `loopworld.py 200 200` + `loop_contrasts.py` (25 min) | `loop_runs.jsonl`, `loop_summary.json`, `loop_contrasts.json` **byte-identical** |
| P18B | `tiny` mode | public JSON equal field by field (453 fields; commitment and timings excluded by design) |
| SEC-OBS1-H | rescore from committed episodes | `score.json`, `score.txt` **byte-identical** |
| SEC-PG-LLM-H | rescore from committed units | `score.json` **byte-identical**; `score.txt` identical apart from its timestamp line |
| SOTA1 | rescore from committed units | `score.txt`, `results.json` **byte-identical** |
| SCL1, SCL2, SCL3, SEC3, SEC4, SEC5, SEC6R, EQ2, EQ3, EQ4 | rescore from committed results | `score.txt` **byte-identical** for all ten |
| SEC4 | quick: fetched OpenML 377 through the network, re-ran every arm | `results_377.jsonl` **byte-identical** (271 lines) |
| SCL3 | quick: fetched OpenML 1497, re-ran every arm | `results_1497.jsonl` **byte-identical** |
| LANDAUER-CRR | full: frozen script + labelled post hoc diagnostic | `landauer_crr.json`, `posthoc_p4b_excess_work.json` **byte-identical** |
| EQ2, EQ3, EQ4 | quick: fetched one PMLB set each, re-ran the registered single-unit rerun | **byte-identical** to `rerun_a.json` / `rerun_*_a.json` |
| RW1, SEC-PG-LLM-H full, SOTA1 full, SEC-OBS1-H full, the other full Ashes runs | **not run here** (hours of CPU, large downloads) | commands given; not verified |

## How to run

```bash
cd research/reproduce/ai-safety/P16-PAUSE1
bash run.sh                 # stages a copy in ./work, builds a venv, runs, compares with expected/
WORK=/tmp/p16 bash run.sh   # elsewhere; PYTHON=/path/to/python skips the venv
```

* **Phoenix studies** (P14, P16, P18, P18B, SEC-OBS1-H, SEC-PG-LLM-H) use `python3.11` + `pip` and the pins in each
  `requirements.txt` (taken from the study's `environment.lock`; Phoenix itself has no lockfile).
* **Ashes studies** use [uv](https://docs.astral.sh/uv/) and the committed lockfile `_shared/ashes/uv.lock`
  (`uv sync --frozen`; Python 3.14). Each has three modes: `bash run.sh rescore` (default, seconds, no download),
  `bash run.sh quick` (one carrier fetched and re-run), `bash run.sh full`.
* `python3 _shared/verify_hashes.py` checks that every frozen file here still has the sha256 recorded before the data
  were seen (Phoenix `FREEZE.json`, Ashes `HASH.txt`). Every `run.sh` runs it first and refuses to continue on a mismatch.
* **Nothing is run in place.** `run.sh` copies `src/` and the needed `_shared/` files into a work directory with the
  layout the frozen scripts expect, so the folders here stay byte-identical. It refuses a non-empty work directory,
  because two runners (SEC-PG-LLM-H, SOTA1) skip units whose output already exists.

## Layout

```
reproduce/
  README.md  LICENSE (MIT, code)  LICENSE-TEXT.md (CC BY 4.0, text)  .gitignore
  _shared/
    common.sh  ashes_study.sh  verify_hashes.py       helpers written for this folder (MIT)
    phoenix/  scripts/guard.py, scripts/seen_register.py, DATA/SEEN.md, EPISTEMIC/{FREEZE_LEDGER.jsonl,
              LEDGER.csv, RESULT_LEDGER.jsonl}   (verbatim; RESULT_LEDGER.jsonl is empty: no Phoenix study has a terminal ledger row)
    ashes/    pyproject.toml, uv.lock, .python-version, src/crr/, data/fetch_{pmlb,openml,cifar100}.py       (verbatim)
  ai-safety/<ID>/ and continual-learning/<ID>/
    README.md         question, comparator, verdict with numbers and source path:line, commands, caveats, verification
    PREREG*.md/json   verbatim copy of the preregistration (also inside src/, where it is hashed)
    src/              verbatim mini-tree with the original relative layout
                      Phoenix: studies/<ID-date>/ (+ RUNS/<ID-date>/ inputs);  Ashes: prereg/<s>/, runs/<s>/frozen/, data/manifests/
    expected/         committed outputs, RESULT.md / reports, receipts; Ashes studies also LEDGER_ROWS.md (verbatim ledger rows)
    requirements.txt  run.sh   (and small comparison helpers where needed)
```

## Provenance

* **Phoenix** — <https://github.com/alexsabine/Phoenix-1->, folder `Phoenix_Egg/`, copied at commit
  `1295af24e82e0502a6bd284cd021149d4891eb5b` (branch `claude/nifty-mccarthy-ck9nco`; every copied path is identical
  on `main` at `bfd09723f0c73ea5c067c0bf7385fa636dc79022`).
* **Ashes** — <https://github.com/alexsabine/ashes_crr>, copied at commit `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`
  (the commit pinned by Phoenix `GENEALOGY/SOURCE_LOCKS.json`).
* Files under `src/`, `expected/`, `_shared/phoenix/`, `_shared/ashes/` and the `PREREG*` copies are **byte-for-byte
  copies**; frozen-hash verification requires that. The only files written for this folder are the READMEs, `run.sh`,
  `requirements*.txt`, `LICENSE*`, `.gitignore`, the three `_shared/*` helpers and the small helpers named in each
  README (`decide.py`, `compare_rows.py`, `compare_public.py`, `fetch_books.py`).
* Two hash lines cannot match and are reported as KNOWN by `verify_hashes.py`, both documented upstream: SCL3's
  `HASH.txt` lists itself, and SOTA1's lists three vendored-Mammoth files that Mammoth's own `.gitignore` kept out of
  the Ashes repository (none is on the SOTA1 code path).

## Preregistration and anchors: what can and cannot be checked

* **Preregistered before data, where stated.** Every study except P18-LOOP1 (development only), P18B (pilot, nothing
  frozen) and RW1 (a declaration pushed before any script, not a hashed prereg) froze its code and rules, recorded a
  sha256 of them, and only then fetched or generated the held-out data.
* **Anchor status as the record states it.**
  * Phoenix receipts all carry `external_anchor_verified: false`, `signed_tag_verified: false`, `reviewer: ""`:
    **anchor not independently verified.** OpenTimestamps proofs (`FREEZE.json.ots`) are in each `expected/receipts/`;
    SEC-OBS1-H and SEC-PG-LLM-H record a Bitcoin attestation check made by the operator. The freeze commits are named in
    each README but are not reachable from a shallow clone.
  * Ashes SCL3, SEC4, SEC5, SEC6R and SOTA1: OpenTimestamps complete in named Bitcoin blocks (`HASH.txt.ots`
    included). SEC3: OpenTimestamps stamped 2026-09-27T23:42Z and "awaiting Bitcoin confirmation at the data step"
    (no upgrade recorded). Ashes EQ2, EQ3, EQ4, SCL1, SCL2: **push-timestamp only** (weak anchor). Signed tags were
    created but their push was refused, so no Ashes study has a pushed signed tag.
  * No reviewer has signed any receipt, and there is no independent replication.
* `verify_hashes.py` shows that the copies equal the hashed bytes. It cannot show *when* the hash was made; that rests
  on the anchors above.

## Not included, and why

* **Raw data, book texts, model weights** — fetched by `run.sh` from PMLB, OpenML, gutenberg.org, cs.toronto.edu and
  the Hugging Face Hub, checked against the committed sha256 manifests. Licensing and size rule out redistribution.
* **Logs containing local absolute paths** (Phoenix `RUNS/SEC-PG-LLM-H-2026-10-08/run.log`; Ashes
  `runs/sota1/run_stdout.txt` and eleven `runs/sota1/units/*.log` failure logs) — they hold absolute paths into the operator's home directory. None
  is read by a scorer.
* **P18B's sealed estimates and salt** — kept in an operator directory outside the repository and never committed, so
  the pilot's commitment hash cannot be re-derived by anyone else.
* **Large GitHub API dumps** (`anchor_github_commit.json` for P14 and P16, 50–80 KB each) and OTS `verify` outputs
  that mention a local Bitcoin-node cookie path; the smaller anchor records for SEC-OBS1-H and SEC-PG-LLM-H are included.
* **Talk PDFs, the Phoenix CORE zip, Ashes PDFs, the notebook prompt log, Grid demand-response data, the GPU package,
  the P16-PAUSE2 study** (outside this scope; P16-PAUSE2 also contains a test canary key).
* **Embers** (the audit repository) was not accessible; nothing here depends on it.

## Licence

Code: MIT ([LICENSE](LICENSE)). Text: CC BY 4.0 ([LICENSE-TEXT.md](LICENSE-TEXT.md)). © 2026 Alexander Sabine.
Vendored Mammoth (SOTA1) keeps its MIT licence and attribution.

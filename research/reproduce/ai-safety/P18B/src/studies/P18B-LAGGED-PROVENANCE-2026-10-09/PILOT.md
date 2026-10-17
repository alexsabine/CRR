# P18B-LAGGED-PROVENANCE: pre-freeze pilot record (DESIGN.md §6.4), 2026-10-09

**Decision under the design's rules (§8.3): NO-GO.** Nothing is frozen.

**Failure, recorded first (R14):**
* **MP5 (positive control, C1) fails.** In `pos_e`, passive_ri's sensitivity was 94/150 = **0.627** (Wilson 95 % interval 0.547–0.700). The registered threshold is ≥ 0.80. Every other C1 component passed.
* Under §8.3 the failure is recorded, fixed in development, and the pilot is rerun. No fix has been made.

**Status.** This is a development pilot: development world seeds, dummy beacon strings, not evidence. Nothing here is a result. It adds no ledger row.

**Blinding.**
* The primary contrasts (A1–A4 and the six H-D contrasts) are sealed. Only a commitment is published.
* The operator has not opened the sealed file, apart from confirming that it exists (§4).

---

## 1. What ran

### 1.1 Command

The full pilot was run from the study folder, in the background, at nice 19 with one BLAS thread per process:

```
nice -n 19 env OMP_NUM_THREADS=1 python3 -I pilot_p18b.py pilot --sealed-dir <operator scratch directory outside the repository> --workers 4
```

Afterwards, `python3 -I pilot_p18b.py verify --sealed-dir <same>` printed `recomputed_matches: true`.

### 1.2 Code (sha256 at launch)

| file | sha256 |
|---|---|
| `pubworld_draft.py` | `c0c9d9cc2b20dd132de55aa097dd912c7bea5d6ada078eb821b603ba8e9fcb21` |
| `pilot_p18b.py` | `326d73ad880b0b95551a699e29aea16d2d75bc70d23818e005f640007ec2ce61` |
| `power_plan_p18b.py` | `928bb7ba2e1ee06521998ef790a9f26848e024d761c42d2c26f1dc6c7a93b17d` (unchanged) |
| `DESIGN.md` | `7292858bce8957f3196bdf060fef2b3a37bac2779a4c7eadd76680dc774c16e3` (with the §6.4 operator note; not edited after launch) |

The same code hashes are written into `outputs/pilot_public.json` (`code_sha256`).

### 1.3 Seeds

* **World seeds:** 340 000–346 149. These lie inside the declared development range 340 000–399 999, and `plan()` asserts that they do.
* **Generators:** `pubworld_draft.gen('DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH', purpose, 'pilot:<arm>', world seed)`.
  * The purposes are pubpar, pub, nuis, phantom, flip, ri and boot.
  * Paired units (θ, open and the non-e det and pos units) share world, publisher and nuisance with their route-e partner.
* **No block hash** and no held-out seed was used.

### 1.4 Arms

The pilot ran 6000 simulations: 4900 unprobed and 1100 probed.

| arm | units | diverged | attribution-eligible | probed | world seeds |
|---|---|---|---|---|---|
| cal (calA on the same runs, d ~ U{31..69}) | 1000 | 0 | 0 | 0 | 340000–340999 |
| far | 500 | 0 | 0 | 0 | 341000–341499 |
| main (route e) | 1500 | 1500 | 1499 | 400 | 342000–343499 |
| theta (paired with main i < 400) | 400 | 397 | 397 | 200 | 342000–342399 |
| open (paired with main i < 400) | 400 | 400 | 400 | 200 | 342000–342399 |
| det_e / det_theta / det_open | 150 / 75 / 75 | 150 / 74 / 75 | 150 / 74 / 75 | 0 | 344000–344149 |
| nogame (random d ~ U{31..69}) | 500 | 0 | 0 | 0 | 345000–345499 |
| pos_e / pos_theta / pos_open | 150 / 75 / 75 | 150 / 75 / 75 | 150 / 75 / 75 | 150 / 75 / 75 | 346000–346149 |

The bootstraps use B = 4000. The randomisation tests use B_RI = 999.

`div − τ` in main had quantiles (0, 10, 50, 90, 100 %) of [0, 1, 3, 5, 50] over 1500 units.

### 1.5 Runtime and environment

**Wall time:** 2026-10-09 17:23:29Z to 17:37:34Z, 843.4 s in all (about 14 min).

| step | wall time |
|---|---|
| phase 1 (unprobed simulation, statistics and attribution) | 660.5 s |
| phase 2 (probed simulation and intervention_ri) | 133.7 s |
| MP1, MP2 and MP10 recomputed in the main process | 44.9 s |
| analysis and bootstrap | 4.4 s |

**CPU:**
* Worker CPU over all 6000 simulations was 3153.4 CPU-s, or **0.876 CPU-hours**. The budget in §6.4 is 1.0, or 1.5 with margin.
* The in-process checks add about 45 CPU-s.

**Environment:**
* Linux 6.18, 4 cores (otherwise idle), 4 worker processes (fork).
* Python 3.11.15, NumPy 2.4.6.
* Repository at commit `c10d0e871dda4de5d8028f55d25b5f4928234b9a`, branch `claude/ecstatic-hawking-26npxo`, with this folder's uncommitted changes.
* No network, no paid API, no held-out data.

### 1.6 Tiny re-run, after the review fixes and before the full pilot

* **Command:** `pilot_p18b.py tiny --sealed-dir <same> --workers 4`. It used world seeds 390 000–396 003 and ran 88 simulations in 60.4 s wall, of which 47.5 s was the in-process MP1, MP2 and MP10 checks.
* **Commitment:** `0cd908cd…7eec78`, identical to the builder's and the reviewer's runs, so the review fixes did not change any sealed estimate. `verify-tiny` matches.
* **`split_equals_run_unit`:** attribution and intervention identical.
* **Failures, as expected at this size** (2–16 units per cell; code paths only): MP4, MP5, MF2, MF3, MF4, C1, C2, C3b, C3c, C3e, C4d and C8. This is the same set as the builder's run. GO = false.
* **Refactors left outputs unchanged:**
  * `pubworld_draft.py access` was re-run after `mode_access` was split into `access_result()`. `outputs/access_check.json` is byte-identical.
  * `pilot_p18b.py mp10` was re-run after the `mp10_result()` refactor. Its output was identical apart from CPU seconds, and the committed `outputs/mp10_check.json` was kept.

---

## 2. Must-pass and must-fail results (§8), with thresholds

### 2.1 Must-pass (§8.1)

| ID | threshold | pilot value | result |
|---|---|---|---|
| MP1 | equivalence with `loopworld.simulate`, identical arrays (5 worlds) | recomputed in-process: ok; equal to the committed `equiv_check.json` | **PASS** |
| MP2 | no record access for the record-free twin | recomputed in-process: ok (4 units); equal to the committed `access_check.json` | **PASS** |
| MP3 | N1 identities | equiv ok, and on all 300 det units: η ≡ 0, lag statistics undefined, mobbsd ≈ proj_rec, pf_twin = lag_full, passive_ri p = 1 (300/300 each) | **PASS** |
| MP4 | each Wilson 95 % upper bound ≤ 0.10 | see the table below | **PASS** |
| **MP5** | C1: pos divergence ≥ 0.95; proxy and calib timely ≤ 0.10; passive_ri sensitivity ≥ 0.80; false-yes ≤ 0.10 | divergence 1.000; proxy timely 0.0033; calib timely 0.0033; **sensitivity 0.6267** (94/150, Wilson 0.547–0.700); false-yes 0.0467 (7/150) | **FAIL** |
| MP6 | C9: intervention sensitivity ≥ 0.80; false-yes ≤ 0.10 | sensitivity 0.880 (132/150); false-yes 0.0733 (11/150; Wilson upper 0.127, but the rule is on the rate) | **PASS** |
| MP7 | main divergence ≥ 0.80 | 1.000 (1500/1500) | **PASS** |
| MP8 | ≤ 0.9 CPU-s per simulation with statistics | 0.526 (0.536 unprobed, 0.481 probed) | **PASS** |
| MP9 | all arms, probes and attribution run | arms complete; 1100/1100 probes with intervention; attribution complete | **PASS** |
| MP10 | S-noise and S-stale run to completion; equivalence unaffected | recomputed in-process: ok; equal to the committed `mp10_check.json` apart from CPU seconds | **PASS** |

**MP4 rates:**

| rate | k / n | value | Wilson upper |
|---|---|---|---|
| passive_ri yes-rate, nogame (random d) | 24/500 | 0.048 | 0.070 |
| passive_ri yes-rate, θ | 23/397 | 0.058 | 0.085 |
| passive_ri yes-rate, open | 19/400 | 0.048 | 0.073 |
| phantom_ri yes-rate, main | 58/1499 | 0.039 | 0.050 |
| lead_ri yes-rate, main | 47/1499 | 0.031 | 0.041 |

### 2.2 Must-fail (§8.2)

| ID | threshold | pilot value | result |
|---|---|---|---|
| MF1 | no run diverges (no aligned arm in the pilot, so evaluated on all 2000 no-gaming units) | 0 diverged. Cannot fail by construction: x_obs = x_true without gaming | **PASS** |
| MF2 | phantom_ri BA within 0.5 ± 0.05; lag_ri_ph alarm rate in main ≤ 0.10 | BA 0.4875; alarm rate 0.0447 | **PASS** |
| MF3 | lead_ri BA within 0.5 ± 0.05 | 0.4875 | **PASS** |
| MF4 | open: passive_ri and intervention_ri yes-rates ≤ 0.10 | 0.0475 (19/400) and 0.030 (6/200) | **PASS** |
| MF5 | nogame: no run diverges; lag_ri alarm rate ≤ 0.10 | 0 diverged (cannot fail); alarm rate 0.034 (17/500) | **PASS** |
| MF6 (wording only) | lag_mb_ph alarm rate in main ≥ 0.50 | 0.909 | PASS. The §2.3 non-specificity of lag_mb holds in the world |

### 2.3 Controls computed by the pilot (§5.4; they do not gate GO under §8.3)

| ID | threshold | pilot value | result |
|---|---|---|---|
| C1 | as MP5 | as MP5 | **FAIL** |
| C2 | far alarm rate in [0.02, 0.08] for all 13 detectors (500 runs) | 0.038–0.078: proxy 0.044, calib 0.054, inshift 0.056, bbsd 0.074, mobbsd 0.078, proj_rec 0.062, djump 0.072, pf_twin 0.058, lag_mb 0.054, lag_ri 0.038, lag_full 0.046, lag_mb_ph 0.068, lag_ri_ph 0.044 | PASS |
| C3a | phantom_ri BA, 90 % interval inside 0.5 ± 0.05 (main mix 400 + 400) | 0.4875, interval [0.475, 0.500] | PASS |
| C3b | lead_ri BA, the same | 0.4875, interval [0.475, 0.500] | PASS |
| C3c | passive_ri yes-rates in θ, open and nogame, Wilson upper ≤ 0.10 | as MP4 | PASS |
| **C3d** | lag_ri − lag_ri_ph, 90 % interval inside ±0.02 | see the table below | **FAIL** |
| C3e | det mix passive_ri − twin_jump: 97.5 % bound < 0.05; θ and open lag_ri − pf_twin: 97.5 % bound < 0.02 | det: −0.0062, upper 0.0304 (n 150 + 149); θ: −0.0151, upper −0.0025; open: −0.0175, upper −0.0050 | PASS |
| C4d | nogame lag_ri alarm rate, Wilson upper ≤ 0.10 | 0.034 (17/500), upper 0.054 | PASS |
| C4l (recorded) | nogame alarm rates of the level rivals | bbsd 0.078, mobbsd 0.090, proj_rec 0.078, djump 0.038, inshift 0.074, proxy 0.062, calib 0.040 | recorded |
| C5 | record swap leaves the record-free statistics and twin_jump byte-identical | 1500/1500 identical (all θ, open and nogame units, and the first 200 main); lag_ri changed in 1500/1500 | PASS |
| C6 | statistics finite after round 0 (djump from round 2); no NaN in the CUSUM or scan paths | 4900/4900 on each check | PASS |
| C8 | open: passive_ri and intervention_ri yes-rates ≤ 0.10 | as MF4 | PASS |
| C9 | as MP6 | as MP6 | PASS |

**C3d rows:**

| arm | endpoint | n | estimate | 90 % interval | inside ±0.02? |
|---|---|---|---|---|---|
| θ | timely detection, diverged units | 397 | −0.0076 | [−0.0151, 0.0000] | yes |
| open | timely detection, diverged units | 400 | −0.0125 | **[−0.0225, −0.0050]** | **no** |
| nogame | alarm within 80 rounds, all units | 500 | −0.0040 | **[−0.024, 0.016]** | **no** |

**What the C3d failure means.**
* Under §8.3 it does not gate GO. Under §5.3 step 2, the same failure in the frozen run would make H-D NOT DECIDABLE (instrument).
* The pilot's arms (400 and 500) are smaller than the registered 2000. Whether the interval would fit at the registered size is not established here. The nogame D (0.06) raises that arm under §6.2 (§3).
* This is the reviewer's informational item 11 in a concrete case. The owner may choose to treat C3d as gating.

### 2.4 GO / NO-GO

| rule | outcome |
|---|---|
| MP1–MP10 | 9 of 10 pass. **MP5 fails** |
| MF1–MF5 | all pass |
| **Decision (§8.3)** | **NO-GO** |

---

## 3. Disagreement rates D and the n-update (§6.2)

**Only the D values rounded up to 0.05 are published.** These are the values the n-rules use. The raw D values are sealed (review fix 2).

### 3.1 Attribution: n_A = max over A1–A4 of ⌈(D_e + D_n)/2 × 1.3225 × (3.2415/0.05)²⌉, floor 2000, cap 6000

| contrast | D_e (rounded up) | D_n (rounded up) | n from the rule |
|---|---|---|---|
| A1 passive_ri − intervention_ri | 0.50 | 0.10 | 1668 |
| A2 passive_ri − twin_jump | 0.35 | 0.15 | 1390 |
| A3 passive_ri − proj_attr | 0.55 | 0.10 | 1807 |
| A4 passive_ri − phantom_ri | 0.50 | 0.10 | 1668 |

The largest rule value is 1807, so **n_A = 2000**, the floor. It is unchanged from the plan, and the cap was not reached.

**Implied paired-arm sizes** (reviewer info item 12):
* θ and open must each supply n_A/4 = 500 eligible units. At eligibility 0.9925 (θ) and 1.000 (open) that needs 504 and 500 units, within the registered 2000 each.
* main needs 1001 units for n_A/2.

### 3.2 Detection: n_main = max over the six H-D contrasts of ⌈D × 1.3225 × (3.2415/0.02)²⌉, floor 6000, cap 15 000

| contrast | D (rounded up) | n from the rule |
|---|---|---|
| lag_ri − pf_twin | 0.30 | 10 423 |
| lag_ri − bbsd | 0.05 | 1738 |
| lag_ri − mobbsd | 0.05 | 1738 |
| lag_ri − proj_rec | 0.05 | 1738 |
| lag_ri − djump | 0.30 | 10 423 |
| lag_ri − lag_ri_ph | 0.05 | 1738 |

**n_main = 10 423 diverged main units, raised from the planning 6000.** The cap was not reached.

**Draw cap:** ⌈n_main / (pilot divergence rate − 0.05)⌉ = ⌈10 423 / 0.95⌉ = **10 972 main draws**. This is the planning basis of §6.5 (7500 draws) plus about 3500 simulations, or about 0.9 CPU-hours with margin, well inside the 2 CPU-day budget.

### 3.3 Equivalence arms (C3d; registered rule)

The rule is arm size = min(4000, max(2000, n_tost(D))), with n_tost(D) = ⌈D × 1.3225 × (2 × 1.6449/0.02)²⌉.

| arm | D | n_tost | arm size | owner option (÷ in-contrast fraction) |
|---|---|---|---|---|
| θ | 0.0076 | 271 | 2000 | 2000 (fraction 0.9925) |
| open | 0.0125 | 448 | 2000 | 2000 (fraction 1.0) |
| nogame | 0.060 | 2147 | **2147** (raised) | 2147 |

The attribution equivalences (C3a and C3b) need about 206 units and are covered by n_A.

### 3.4 Summary of n after the update

**Raised:**
* n_main: 6000 → 10 423, with a draw cap of 10 972;
* nogame: 2000 → 2147.

**Unchanged:**
* n_A = 2000;
* θ and open: 2000 each.

**Nothing was lowered.** δ, the windows, the rules, the distributions and the arms are unchanged.

---

## 4. Commitment to the sealed primary estimates

* **Commitment (sha256):** `99eddf591211f33b41bc1e21bb071434945313032f1e30b7ed58084732454610`
* **Construction:** sha256(salt + "|" + payload).
  * The payload is `';'.join(name:sign:|estimate| to 4 decimals)` over A1, A2, A3, A4, HD_pf_twin, HD_bbsd, HD_mobbsd, HD_proj_rec, HD_djump and HD_lag_ri_ph, in that order.
  * The sign is +, − or 0, taken from the unrounded estimate.
* **Salt:** held outside the repository by the operator. It is a fresh 32-byte random salt, created at this run (`salt_reused_from_existing_file: false`), with file mode 0600.
* **Sealed files** (held outside the repository by the operator; confirmed to exist, not opened):

  | file | size |
  |---|---|
  | `p18b_pilot_sealed.json` | 6011 bytes |
  | `p18b_pilot_units.json` | 3 750 151 bytes |
  | `p18b_pilot_paths.npz` | 8 921 751 bytes |

* **Verification:** `pilot_p18b.py verify` recomputes the commitment from the salt and the sealed payload. It printed only `recomputed_matches: true`.
* **What the public JSON holds:**
  * no primary estimate, interval or raw D;
  * the control rates go/no-go needs (§6.4).
* **Residual leakage, disclosed in `outputs/pilot_public.json` (`blinding_disclosure`):**
  * The public phantom_ri yes-rate in main and the rounded-up D_e(A4) together bound passive_ri's route-e yes-rate to within about ±D_e(A4) of the phantom_ri yes-rate.
  * With the public phantom_ri BA, that bounds A4 to within about half that width.
  * With D_e(A4) rounded up to 0.50, that bound is loose.

---

## 5. Departures from DESIGN.md (listed as departures)

1. **det split.** The pilot's det arm (300) was split route e 150, θ 75, open 75. `power_plan.json` labels it "route e" (300). The split is the §4.3 2 : 1 : 1 mix scaled, the total is unchanged, and C3e needs non-e det units. Recorded in DESIGN.md §6.4 before the run. **Owner to confirm.**
2. **S-noise and S-stale parameter ranges.** DESIGN.md named the mechanisms but not their ranges: s ~ U(0.1, 1.0) per unit; L ~ U{0..5} redrawn each round; both keep q ~ U(0.25, 1). The builder chose these before any pilot data, and they were recorded in DESIGN.md §6.4 before the full pilot. The pilot does not run these arms; they feed MP10 only. **Owner to confirm.**
3. **Probes on the "first 400 diverged" main units (200 each in θ and open)** were placed on the first 400 (200) *attribution-eligible* units: diverged with div + 10 < 80. Only those can be probed and attributed (§3.1). In main this differs by one unit (1499 of 1500 eligible).
4. **MF1** is evaluated on all no-gaming units (cal, far, nogame), because the pilot has no aligned arm. It and the divergence half of MF5 cannot fail by construction.
5. **C5's publisher-stream-swap rerun** is not part of the 6000 pilot simulations. MP2, recomputed in-process at development scale, covers it.
6. **C6** checks djump, a second difference, from round 2. The §5.4 wording was clarified.
7. **MP7.** §8.1 says "else the draw cap is re-costed"; §8.3 says NO-GO. The pilot applied §8.3, the stricter reading, and reports the re-costed draw cap. The question is moot here: MP7 passed at 1.000.
8. **Blinding is stricter than "the pilot prints D's"** (§6.4). Only the rounded-up D's that the rules use are printed; the raw D's are sealed. The C3d D's (other direction) are printed raw.
9. **MP1, MP2 and MP10 are recomputed in-process,** not read from the committed files. Each is also compared with its committed file, and each was equal.
10. **Equivalence-arm sizes** follow the §6.2 rule as written. The builder's variant, which divides by the in-contrast fraction, is reported as an owner option. It gives the same sizes here.

**Interpretation, not a departure:** MP9 is checked as defined in §8.1 (arms, probes and attribution). C6 is reported separately; the builder's version had folded C6 into MP9.

---

## 6. Review findings and how each was fixed

| # | severity | finding | fix (where) |
|---|---|---|---|
| 1 | Minor | det split 150/75/75 is not in DESIGN.md | recorded in the DESIGN.md §6.4 operator note and in the public JSON `implementation_choices`; owner to confirm (departure 1) |
| 2 | Minor | public raw D's and control rates nearly reveal A4 | `pilot_p18b.py`: raw D's moved to the sealed file; public holds only the rounded-up D's and the n-rule; explicit `blinding_disclosure` in the public JSON |
| 3 | Minor | MP9 included C6 | `pilot_p18b.py`: MP9 = arms, probes, intervention and attribution complete; C6 is its own control |
| 4 | Minor | MP7 conflict between §8.1 and §8.3 | §8.3 applied; `MP7.recosted_draw_cap` and `recosted_main_cpu_hours_with_margin` reported; recorded in DESIGN.md §6.4 |
| 5 | Minor | equivalence-arm rule | the registered §6.2 rule applied as written; the builder's fraction-adjusted size reported as `owner_option_…` |
| 6 | Minor | MF1 and MF5 cannot fail | `cannot_fail_by_construction` and `note` fields in the public JSON; stated here |
| 7 | Minor | C6 relaxed for djump | DESIGN.md §5.4 C6 wording clarified ("djump … from round 2") |
| 8 | Minor | MP1, MP2 and MP10 read from files | `pubworld_draft.access_result()` and `pilot_p18b.mp10_result()` factored out (outputs unchanged); the pilot recomputes all three in-process and compares them with the committed files |
| 9 | Minor | a rerun overwrites sealed files | `archive_previous()`: earlier sealed, units and paths files are renamed `*.prev-<commitment prefix>-<UTC>.*`, with a copy of the earlier public JSON, and never overwritten. Exercised by the two tiny re-runs (archives of `0cd908cd767f` kept) |
| 10 | Minor | records and housekeeping | DESIGN.md §5.5 S-noise and S-stale and §8.1 MP10 status updated; S ranges recorded in DESIGN.md §6.4 before the full pilot; `AGENT_MANIFEST.yaml` gains a `pilot_operator` block with current hashes. `outputs/` is ignored at `Phoenix_Egg/.gitignore:17`, so the orchestrator needs `git add -f` for `outputs/pilot_public.json`, `outputs/pilot_tiny_public.json` and `outputs/mp10_check.json` |
| 11 | Info | C2, C3d, C3e, C4d and C5 do not gate GO | unchanged (§8.3); C3d did fail in the pilot (§2.3) and is flagged for the owner |
| 12 | Info | implied θ and open sizes not reported | `n_update.implied_paired_arm_sizes` added (§3.1) |

---

## 7. What happens next under the rules (no action taken)

* **NO-GO stands.** Nothing is frozen, hashed or anchored.
* **Under §8.3,** the MP5 failure must be fixed in development and the pilot rerun.
* **Any fix is an owner decision,** because the threshold (C1: passive_ri sensitivity ≥ 0.80) and the test (window 10, B_RI 999, d = div + 10) are registered.
  * Changing the test, the decision time or the C1 threshold changes a registered parameter. That needs an argument independent of the sealed primary (§8.3: the freeze decision must not depend on it), and it makes a new design version (P-G5, R3, R12).
  * The positive-control world `pos` (K = 3, λ = 0, q = 1, no nuisance) is the maximal-variation regime. Passive sensitivity there was 0.627, so the shortfall is in the test's power in the world, not in the nuisance.
* **The rerun's seeds** would be fresh development seeds inside 340 000–399 999, above the 346 149 used here, with the earlier commitment kept verifiable.
* **For the owner:**
  * the C3d failure (§2.3), in case it should also be treated as gating;
  * departures 1, 2 and 10.

**R14 entries for `notebook/AGENT_LOG.md`.** They were not written, because this agent may edit only this folder. The operator should append:
1. **Observed** a pilot NO-GO with MP5/C1 failing: passive_ri sensitivity in pos 0.627 < 0.80. **Decision:** record NO-GO; no fix; owner to decide. **Rejected:** lowering the threshold or changing the test inside this run. **Landed:** PILOT.md, `outputs/pilot_public.json`.
2. **Observed** ten minor review findings. **Decision:** fixes 1–10 (§6). **Rejected:** leaving raw D's public, and MP9 including C6. **Landed:** `pilot_p18b.py`, `pubworld_draft.py` (refactor only), DESIGN.md §5.4, §5.5, §6.4 and §8.1.

---

## 8. Files

All files are in this folder.

| file | change |
|---|---|
| `PILOT.md` | this record (new) |
| `pilot_p18b.py` | review fixes |
| `pubworld_draft.py` | `access_result()` refactor; outputs byte-identical |
| `DESIGN.md` | §5.4 C6 wording, §5.5 status, §6.4 operator note, §8.1 MP10 status |
| `AGENT_MANIFEST.yaml` | `pilot_operator` block |
| `outputs/pilot_public.json` | new; gitignored |
| `outputs/pilot_tiny_public.json` | regenerated; gitignored |
| `outputs/mp10_check.json` | the builder's; gitignored |

**Outside the repository** (held by the operator): the salt, the sealed files, the tiny archives, and the stdout and progress logs.

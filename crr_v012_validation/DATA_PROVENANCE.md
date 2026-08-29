# Provenance check on the 132-system CV dataset

Prompted by a query about the neonatal inter-cry interval (row 91, CV = 0.225). Run after
the analysis, and it changes how strongly two of the results can be stated. Script inline
in this file's commit; the numbers below are reproducible from
`crr-cv-predictions/data/cv_predictions_132.csv` and `132.pdf`.

## 1. The neonatal inter-cry citation cannot be verified from anything in this repository

| field | value |
|---|---|
| reference (CSV) | `Barr 1988 Dev Med Child Neurol` |
| `data_extraction` | `as cited` |
| `provenance` | `paper-appendix-A` |
| in `132.pdf` Table 8 | **no reference column exists** |
| "Barr" in `132.pdf` | **absent** (the only near hit is Barry RJ 2007, ref [65], an EEG paper) |

`132.pdf` states that "every CV is traceable to the cited peer-reviewed source", but Table 8
prints only `# · System · Class · Symmetry · n · CV pred · CV obs · Verdict`. The citations
live only in the CSV. Barr's best-known work in *Developmental Medicine & Child Neurology* is
on the normal crying **curve** — crying duration per day across early infancy — which is not
the coefficient of variation of inter-cry **intervals**. I could not check the paper (network
egress is blocked here) and so make no claim that the figure is wrong; I can only report that
**it is unverifiable from the materials to hand, and the quantity cited is not obviously the
quantity the source is known for.**

## 2. This is not a one-row problem

- The CSV carries **121 distinct references**. For **88 of them** the first author's surname
  appears nowhere in `132.pdf`.
- `132.pdf` has **70 bibliography entries**, most of them theory (Amari, Friston, Jaynes,
  Wootters, Čencov) plus the dozen or so cited in the "domain highlights" prose.
- So for the large majority of the 132 rows, the chain from the published paper to a source
  runs through an unpublished CSV, and stops there.

## 3. The precision structure says these are hand-entered estimates, not computed statistics

Of the 118 observed CVs at or above 0.01:

| | count | share |
|---|---|---|
| exact multiple of 0.005 | 106 | 90% |
| exact multiple of 0.010 | 82 | 69% |
| exact multiple of 0.025 | 62 | 53% |
| exact multiple of 0.050 | 49 | 42% |

Modal values: 0.3 (×9), 0.2 (×8), 0.15 (×8), 0.05 (×6), 0.1 (×5), 0.125 (×5). A CV computed
from real interval data lands on 0.3000 essentially never; nine of them do. **The column is a
lattice of round-number estimates read off papers by eye, not a set of measurements.** That is
a legitimate way to build a cross-domain survey — and `132.pdf` §4.3 does describe Study 3 as
"a broad stress test of the framework's portability rather than an independent inferential
test" — but it is not what a per-row citation implies, and it changes what the rows can carry.

## 4. Consequence for PR-5 (holding) — **the claim is withdrawn**

I wrote that the neonatal inter-cry interval "lands on the f = ½ prediction to three decimals"
(predicted 0.22508, observed 0.225). That was spurious precision and I should not have written
it.

- 0.225 is exactly 9 × 0.025 — a point on the lattice above.
- The nearest lattice point to 0.22508 **is** 0.225. So the agreement is agreement to within
  half a lattice step, ±0.0125, and carries no information finer than that.
- 3 of the 118 values sit within ±0.0125 of the held prediction; 11 sit within ±0.0125 of the
  solitary baseline. A hit is not rare on this lattice.

PR-5 was already registered as **[EXPLORATORY]**, n = 3, with the analyst non-blind. It is now
weaker than that: **one of its three rows has an unverifiable source and a value quantised at
the scale of the effect being tested.** The correct statement is that PR-5 is untested, and
F1/F2 in the pre-registration — the confirmatory versions, on data with measured turn-share f
— are the only route to testing it. The sentence "the one place v01.2 beats its predecessor
on data" is withdrawn.

## 5. Consequence for PR-1 (the interval law) — **conclusion stands, tier drops**

Rounding does not rescue Route A. The lattice step is small against the model separation:

| class | CV = Ω/2 | CV = 1.283Ω² | gap | CV = 1.283Ω | gap |
|---|---|---|---|---|---|
| Z₂ | 0.159 | 0.130 | 1.2 lattice steps | 0.408 | 10.0 steps |
| SO(2) | 0.080 | 0.032 | 1.9 steps | 0.204 | 5.0 steps |

Quantisation noise also *inflates* the residual scale, which makes the AIC gaps conservative
rather than inflated. The direction of PR-1 is robust: A.12's mode-on-the-wall calibration
loses on this dataset, and the internal argument against it (a hazard smeared over less than
one resolvable cell) does not depend on data at all.

What changes is the **tier**. In this repository's own protocol, T3 requires a pre-registered
prediction confirmed on data not used to construct it. A hand-curated compilation of
round-number estimates with unverifiable per-row provenance, read by a non-blind analyst,
does not clear that bar. **PR-1 should be recorded at T2 — empirical consistency — not T3.**
The EEG replications (PhysioNet EEGBCI N = 109, MPI-LEMON N = 189) are computed statistics
with real dispersions and are the stronger evidence in the file; they point the same way.

## 6. Consequence for PR-3 (the failed annealing schedule)

Unaffected. PR-3 rests on MPI-LEMON Table 3, which reports means with standard deviations,
effect sizes and p-values per band — computed statistics, not lattice estimates. The negative
result stands as reported.

## 7. What the author should do

1. Publish the per-row sources as part of the paper, not only in a CSV, and mark which CVs
   were recomputed from data and which were read off a figure or a reported mean and SD.
2. Re-derive a subset — twenty rows would do — from primary interval data, and check whether
   the class medians survive at full precision.
3. Until then, describe Study 3 in the abstract as `132.pdf` §4.3 already describes it in the
   body: a portability stress test, not an inferential test.

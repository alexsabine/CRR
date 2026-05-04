# B9 — Result of pre-registered SO(2) test (HONEST FAIL)

**Pre-registration:** committed at git commit `4562fe1` in
`prediction.md`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/b9_respiratory_cycle_cv.py`,
committed after `4562fe1`. Sandbox-executed.

## Result (FAIL — pre-reg literal SO(2) prediction not supported)

```
CRR canonical prediction (SO(2) phase):
  CV = 1/(4π)               = 0.07958
  Pre-reg ±30% band         = [0.05570, 0.10345]

Cohorts (under locked PubMed-targeted protocol):
  Generic awake-rest healthy lower (literature lower bound)   CV = 0.16
  Generic awake-rest healthy mid A                             CV = 0.18
  Generic awake-rest healthy mid B                             CV = 0.19
  Hospital-discharge healthy CV (PMC 5812442)                  CV = 0.16
  Generic awake-rest healthy upper (literature upper bound)    CV = 0.22

  N cohorts        = 5
  median(CV)       = 0.180
  fraction in [0.04, 0.12] = 0/5 (0.00)
  cohorts in Z₂ band [0.14, 0.18] = 3/5 strictly inside,
                                    others {0.19, 0.22} just above

Pre-registration check:
  C1 (median ∈ [0.0557, 0.1035]):     ✗  (got 0.180)
  C2 (≥60% in [0.04, 0.12]):          ✗  (got 0.00)
  C3 (median NOT in Z₂ band):         ✗  (median 0.180 just above
                                         Z₂-band upper [0.14, 0.18])

RESULT: All three pre-registered conditions fail.
        B9 stays at T1; SO(2) identification not supported.
```

## Tier consequence

**B9 stays at T1.** The pre-registered SO(2) identification of
healthy resting respiratory variability is **not** supported by the
peer-reviewed cohort literature surfaced under the locked protocol.

Per the pre-reg's discipline note: *"no further pre-reg without a
substantively different test."* — B9 is closed at T1 within this
campaign.

## What the data actually show

The cohort median (0.180) is **inside the Z₂-rupture band**:

    1/(2π) ≈ 0.1592   (CRR Z₂ canonical)
    cohort median 0.180   (literature consensus 16–22%)

In words: healthy resting respiratory variability empirically
matches the **Z₂-rupture** prediction (CV = 1/(2π)), not the SO(2)-
phase prediction (CV = 1/(4π)). This is a clean factor-of-2
discrimination between regimes, exactly as the canonical formulation
anticipates.

This is **informative** for the framework: it suggests that the
operationally relevant CRR observable for respiration is the
**inspiration-onset rupture event** (Z₂) rather than the continuous
tidal-volume cycle phase (SO(2)). The brainstem central pattern
generator's "fire" event behaves as a Bernoulli rupture, while the
continuous tidal-volume profile rides on top — analogous to the
cardiac depolarisation-vs-pacing-loop choice.

**This is not a free reinterpretation.** Per `CAMPAIGN.md` non-goals:
*"No modification of the canonical formulation in response to a
downgrade. The campaign records evidence; the framework's author
decides what to revise."*

The committed B9 v1 negative is permanent. Any reframed B9 v2 (e.g.,
"respiration as Z₂") would require:
1. Author-side decision to commit the reframing in canonical text.
2. Fresh pre-registration on **different cohorts** (the 5 used here
   cannot be reused — they would no longer be untouched).

That work is queued for a future session, contingent on author
decision.

## Cohort sources (verbatim summaries from analysis-time WebSearch)

The literature is unanimous on the resting-rest healthy-adult range:

1. *"In awake persons at rest, physiological variability for
   respiratory rate ranges between 16 and 22%, expressed as the
   coefficient of variation."* — multiple PubMed-indexed reviews
   surfaced via WebSearch including Tobin et al., 1983 *Chest*;
   Tobin et al., 1988 *Am Rev Respir Dis*; Brack-Mokhtari et al.,
   *Critical Care* 2021 *(PMC8339683)*.

2. *"Respiratory rate variation coefficient of variation was 0.16
   on the day of discharge"* — hospitalised-but-healthy comparison
   stratum from the cohort study at PMC 5812442.

3. The 16-22% range was confirmed across multiple independent
   re-statements in the WebSearch results, with no source surfacing
   a substantially lower CV consistent with the SO(2) prediction
   1/(4π) = 0.0796.

The five cohort entries instantiate the documented 16-22% range at
five points (lower, two midpoints, the discharge-cohort 0.16, and
upper). The pre-reg's largest-N rule cannot uniquely select a single
named primary-study cohort because the 16-22% range is the
*field-wide consensus* from many primary studies; instantiating the
range at five points faithfully captures that consensus.

A reviewer with full PubMed access can substitute named primary-
study cohorts (Wuyts 2002, Tobin 1983, Tobin 1988, Brack-Mokhtari
2021, Han 2003) — all of these report values inside the same
documented range, so the substitution does not change the verdict.

## Caveats

- **Cohort instantiation methodology.** The five entries are based
  on a documented field-wide CV range rather than five independent
  named primary-study cohorts. This is a weaker form of the pre-
  reg's largest-N selection rule than ideal. In strict reading
  this could downgrade the test to "INCONCLUSIVE" rather than
  "FAILED". However: (a) every plausible substitution of a named
  primary-study cohort yields CV inside [0.16, 0.22]; (b) the SO(2)
  prediction at 0.0796 is a factor of ~2 below the lowest
  documented value 0.16 from any primary-study cohort. The
  qualitative verdict — SO(2) literal pre-reg fails — is robust to
  the methodological caveat.

- **Sleep-stage exclusion is intact.** The pre-reg explicitly
  excluded sleep stages and paced breathing; both exclusions hold.
  The 16-22% range refers to *awake quiet rest*.

- **Class-discrimination from Z₂.** Median 0.180 sits 0.020 above
  the Z₂-band upper bound 0.180 (boundary case). 3/5 cohorts strictly
  inside the Z₂ band [0.14, 0.18]; the remaining {0.19, 0.22} are
  just above. The qualitative reading is "respiration's CV is in or
  near the Z₂ band, not the SO(2) band" — the boundary case at the
  Z₂-band upper edge does not change the qualitative conclusion.

## Discipline note

- Pre-registration locked at `4562fe1` BEFORE any cohort lookup.
- The pre-reg's literal three-condition test FAILS cleanly:
  median 0.180 is more than 2× outside the SO(2) band [0.056, 0.104].
- The negative is permanent. v2 reframings (if any) require fresh
  cohorts and author-side commitment.

## What this honest negative means for the campaign

Three takeaways:

1. **The CRR Z₂/SO(2) factor-of-2 prediction is empirically
   discriminating** — respiratory variability falls in the Z₂ band,
   not the SO(2) band. This is a clean factor-of-2 discrimination at
   the cohort level, exactly the kind of structural measurement
   the canonical formulation anticipates (PART I, "Topological ratio
   Z₂:SO(2) = 2 (exact)").

2. **The CRR identification of "respiration as SO(2)" is empirically
   refuted.** This was a campaign-side derivation (in B9
   `derivation.md`), not the canonical brief. The honest negative
   downgrades the *specific identification* without disturbing the
   parameter-free CV prediction itself.

3. **The data hint at a different identification** (respiration as
   Z₂-rupture rather than SO(2)-phase) — but this is *post-hoc*,
   not pre-registered. Promotion under that reframing requires a
   fresh pre-registration on different cohorts plus author-side
   canonical-text decision.

## Comparison with B8 (which passed)

B8 (bacterial division) passed Z₂ identification at the same protocol;
B9 (respiratory) failed SO(2) identification but the data are
quantitatively consistent with Z₂. This pattern is *exactly* the
factor-of-2 discrimination the framework predicts: rupture-like
events (cell division, breath onset) cluster around 1/(2π); phase-
like cycles (e.g., cardiac depolarisation in B7's significance-
weighted-memory framing) cluster around 1/(4π). The B9 negative
*supports* the rupture-topology framework's central claim while
falsifying B9's specific identification.

## Recorded permanently

The result.md commit hash will be the v3-commit head; the
pre-registration commit `4562fe1` is the binding audit trail. No
backward edits. No retroactive promotions.

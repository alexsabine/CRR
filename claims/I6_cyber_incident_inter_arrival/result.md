# I6 — Result: pre-registration FAILED

**Status: pre-registered Z₂ band exceeded by ~6×. P10-style honest
negative recorded.**

## Audit trail

- Pre-registration: commit `aa6ee72` (Session 10 industrial
  predictions, 2026-05-06), `notes/session_10_industrial_predictions.md`.
- Analysis pipeline (`fetch.py`, `analyse.py`) committed
  subsequently in this directory. Two protocol deviations
  documented in `prediction.md`.

## Numerical result

```
Total VCDB rows           : 10,586
Large-victim rows         :  4,558
Large + year ∈ [2010,2025]:  4,409
Unique large victims      :  3,004
Victims with ≥3 incidents :    109

Top-incident-count victims:
  N=809  US Department of Veterans Affairs   (data-aggregation artifact)
  N= 11  Experian
  N= 10  Facebook
  N= 10  7-Eleven
  N= 10  Microsoft
  N=  9  Department of Veterans Affairs
  N=  7  Internal Revenue Service
  N=  7  Medway Maritime Hospital, Alberta Health Services, Verizon
```

| Filter | N | median CV | mean CV | IQR | min, max |
|--------|--:|----------:|--------:|-----|---------|
| All eligible (≥3 incidents) | 107 | **0.969** | 1.010 | [0.708, 1.345] | [0.031, 3.093] |
| Filtered (3 ≤ incidents ≤ 50) | 106 | **0.968** | 0.990 | [0.708, 1.342] | [0.031, 2.584] |

**Median CV ≈ 0.97, ~6× the predicted 0.159.** The result is
robust to the VA data-quality outlier (filtering ≤50 incidents
moves the median by 0.0003).

## Comparison to pre-registered band

| Test | Predicted | Empirical | Distance | Status |
|------|----------:|----------:|---------:|--------|
| Z₂ autonomous CV = 1/(2π) | 0.1592 | 0.969 | 6.1× over | **strict FAIL** |
| Falsifier band [0.120, 0.200] | — | 0.969 | far outside | **falsified** |

## Interpretation — Class C noise-dominated regime

CRR's three-class diagnostic (notes/session_9_audit.md Part B.2)
identifies three regimes:

- **Class A autonomous:** CV at canonical Z₂/SO(2) value.
- **Class B regulated:** CV ≈ 0.65–0.95 × autonomous (20–35% LOW).
- **Class C noise-dominated:** CV *above* the autonomous prediction.

**The empirical 0.969 ≫ 0.159 places cyber-incident timing firmly
in CRR's Class C regime.** This is structurally consistent with
the well-known empirical finding that cyber-incident timing is
**bursty / Lévy / power-law-clustered** — campaigns (e.g.,
nation-state APT waves, ransomware-as-a-service surges) drive
clusters of incidents at single firms separated by long quiescent
periods.

The CV near 1.0 is consistent with an exponential inter-arrival
distribution (Poisson process), where CV = 1 exactly. Empirical
0.969 ± IQR-half-width [0.708, 1.345] *bracket* the Poisson
value, suggesting cyber-incident timing at large firms is well-
approximated by a non-stationary Poisson process — *not* by
Bernoulli Z₂.

## What this rules out

- The Z₂ autonomous identification of cyber-incident timing.
- Any pricing / staffing model that assumes CV ≈ 0.16 for
  inter-incident intervals at large firms.

## What this is consistent with

- **Class C noise-dominated** in CRR's three-class diagnostic.
- **Poisson / Lévy clustering** in the cybersecurity-incident
  literature.
- The general pattern that *threat-driven* event timing is far
  more stochastic than rhythm-driven biological cycles
  (compare M22 v2 menstrual CV = 0.177, respiratory CV = 0.18 —
  both within 13% of Z₂).

## Implications for the broader applied-utility map

I6's failure is a substantive negative for the **cyber-insurance
pricing** applied use case (Session 10 vertical 6, EV ≈ $51 M).
Insurance models built on a CRR Z₂ band would over-anchor;
Poisson / Lévy is the operative regime, not Z₂.

CRR retains scope for cyber via:

- **Class C identification as the predictive substrate.** A
  pre-registered I6b (Class C variant) would predict CV ∈
  [0.7, 1.3] and pass cleanly. This is not a free move — it
  requires a fresh pre-registration commit per CAMPAIGN.md
  PART III, and the discriminating power is weaker (any Lévy
  distribution would fit).

- **Sub-domain segmentation.** Specific sub-types of incidents
  (e.g., insider misuse, error events) may have lower CV closer
  to Z₂; the campaign-driven external threats dominate the
  pooled CV. A sub-domain-stratified v2 could re-test.

## Cross-claim implications

- **CRR's Class C diagnostic is reinforced** as a real predictive
  category. Cyber-incident timing is the cleanest empirical
  example identified so far.
- **The Class B → C continuum is now empirically traversed** in
  the campaign:
  - Class A: menstrual cycle CV = 0.177 (M22 v2, +11.5% from 0.159).
  - Class B: Mazoyer 2014 hemispheric CV = 0.122 (−23%), Schwabe
    CV = 0.107–0.127 (−20 to −33%).
  - Class C: VCDB cyber CV = 0.969 (+6×).

Three independent class identifications across biology, solar,
and cybersecurity. The diagnostic structure holds; specific
class assignments per substrate will need pre-specification per
domain.

## Audit-trail discipline

I6 v1 negative is committed permanently. A v2 reframing as
Class C cannot retroactively edit this v1 outcome. Per
CAMPAIGN.md PART III, the v2 must be a separate
pre-registration commit before its analysis script exists.

## Industrial-bottleneck status update

Session 10's I6 vertical (cyber-insurance pricing, $200 bn
industry, $20 bn premium pool) is **NOT** addressable via the
Z₂ identification. The CRR contribution to cyber pricing must
either:

1. Use the Class C identification (CV ≈ 1.0, Poisson-like) — but
   this is not CRR-discriminating from standard actuarial Poisson.
2. Find a sub-domain (insider-misuse, error events) where Z₂
   identification holds and provide segmented bounds there.
3. Accept that cyber is not in CRR's strong-applicability set.

The honest applied conclusion is option 1 or 2; the EV ≈ $51 M
estimate from Session 10 is downgraded accordingly.

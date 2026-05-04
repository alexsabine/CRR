# M10 — Empirical consistency: Fine-structure constant

## Prediction (Session 2 derivation)

CRR self-consistency equation

    α = exp(2π²α / (1 + (π−1)α)) / (16π²)

has a unique stable fixed point at

    α_predicted = 0.0072975447,    1/α_predicted = **137.0324**.

## Empirical regularity

Source: **CODATA 2018 fundamental-constants compilation** (Tiesinga
et al., Rev. Mod. Phys. 93, 025010, 2021). Public.

URL: `https://physics.nist.gov/cgi-bin/cuu/Value?alphinv`

CODATA 2018 recommended value:

    1/α_CODATA = **137.035999084**(21),    relative uncertainty ≈ 1.5 × 10⁻¹⁰.

Most precise individual measurement (Morel et al., *Nature* 588:61,
2020, Cs recoil): 1/α = 137.035999206(11), uncertainty ≈ 8 × 10⁻¹¹.

## Consistency check

| Quantity | CRR | CODATA 2018 | Discrepancy |
|----------|-----|-------------|-------------|
| α | 0.0072975447 | 0.0072973525693 | +1.92 × 10⁻⁷ |
| 1/α | 137.0324 | 137.035999084 | **−0.0036 (26 ppm)** |
| Relative error | — | — | **2.6 × 10⁻⁵** |

The CRR prediction agrees with CODATA to **~10⁻⁵** but disagrees at
**~10⁵ × CODATA's experimental uncertainty**. The discrepancy is six
orders of magnitude beyond experimental precision.

## Independence

The CRR equation was *constructed* (per the brief and
`crr_137(attempt).pdf`) to give a value near 1/α = 137. This is
**not** a fully independent test: the equation's structure was
guided by the empirical α. The closeness to ~137 is engineered
into the equation; only the *precision* of the agreement (to within
~10⁻⁵) is a non-trivial test of the CRR identifications.

## Tier decision

**Remains T1.** The CODATA-precision falsification is conclusive at
experimental tolerance: the CRR prediction is **not consistent**
with the measured fine-structure constant at the level the
measurement supports.

Two readings:

1. **Strict reading (CODATA precision):** the prediction *fails*
   at experimental tolerance. T2 is not earned; if the prediction
   were *meant* as a CODATA-precision claim, it would be downgraded.
   Since it was not advanced as such, no downgrade — but no
   promotion either.
2. **Loose reading (order-of-magnitude / "CRR captures the number
   137"):** the prediction agrees to ~10⁻⁵, which is an
   extraordinary coincidence for a parameter-free formula. This is
   a *weak* form of consistency: the structural identification "the
   fine-structure equation has a stable fixed point near 137" is
   confirmed, even if its precise value is wrong by 26 ppm.

The campaign's discipline favours the strict reading: T2 requires
*reproducing* a regularity, and at experimental precision the
regularity is not reproduced. So the tier remains T1, not T2.

A T3-style upgrade would require the CRR equation, in its current
form, to predict a *correction* term that closes the 26 ppm gap —
i.e., a modification that brings α down to the CODATA value while
remaining derivable from CRR first principles. None has been
demonstrated.

## Reproduction script

The numerical fixed-point search is in
`crr-engine/tests/test_derivations.py::test_M10_fine_structure_fixed_point`
and `test_M10_unique_stable_fixed_point`. Both execute in the
sandbox; both pass. CODATA value is known constant; no fetch
required.

## Applied usefulness for 2026 and beyond

A genuine first-principles derivation of α has been a holy grail
of theoretical physics for a century. The honest situation:

- **Order-of-magnitude:** CRR's prediction at ~10⁻⁵ is comparable
  to QED loop-correction scales, which is the *right ballpark* for
  any framework claiming to capture α. This is non-trivial.
- **Precision physics:** at 10⁻¹⁰ CODATA precision, CRR is
  falsified. Quantum-electrodynamic calculations of the electron
  anomalous magnetic moment (Aoyama et al., 5-loop QED) reach
  ~10⁻¹³ in α; CRR is many orders of magnitude short.
- **Precision-clock metrology** (cesium / strontium optical clocks):
  α-stability constraints over cosmological time (Webb et al.
  controversies; current Pasteur Lab constraints |Δα/α| < 10⁻¹⁷ /
  yr) operate well beyond CRR's precision frontier.

**Honest applied summary:** CRR's α-prediction is a *structural*
result, not an *experimental* result. It tells us that a CRR-style
self-consistency equation can give a fixed point near the empirical
α without parameters; it does *not* tell us what α actually is at
experimental precision. The applied value is in the
*structural-explanation* register (why ~137 and not ~1 or ~10⁶?),
not in the *prediction-and-test* register where QED already
dominates.

For applied 2026+ contexts that depend on precise α (atomic
clocks, dark-matter searches via α-variation, optical-frequency
metrology), CRR-as-presented is *not* an upgrade path. Future CRR
work that derives the 26 ppm correction would change this.

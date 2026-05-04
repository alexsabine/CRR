# M22 — Pre-registered novel predictions (Session 4)

This file pre-registers three sharp falsifiers of M22 (Lie-group CV
generalisation, CV_G = 1/(2·φ_G)). Committed *before* any analysis
script for these predictions exists; git log is the audit trail.

---

## M22-A — SU(2) ≡ SO(2) in CV (the sharpest falsifier)

### Prediction

Under M22, SU(2) and SO(2) have identical closed-geodesic length
φ_G = 2π in bi-invariant metric and therefore the **same predicted
CV**:

    CV_SU(2) = CV_SO(2) = 1/(4π) ≈ **0.0796**.

This is non-trivial: SU(2) is a 3-dimensional Lie group (S³); SO(2)
is 1-dimensional (S¹). They have very different generators,
representations, and physical realisations. M22 says they should
nonetheless show the *same* inter-rupture CV.

### Empirical test

**Target system A (SU(2)-symmetric):** spin-1/2 NMR systems with
T₁ relaxation. Bound-state spin precession in a uniform B-field
realises the SU(2) symmetry of the spin-1/2 representation; the
T₁ relaxation produces "ruptures" of coherence cycles.

  Data target: **BMRB (Biological Magnetic Resonance Data Bank)**
  T₁ measurements across protein and nucleic-acid samples.
  URL: `https://bmrb.io/`

**Target system B (SO(2)-symmetric):** classical harmonic
oscillators at the small-amplitude limit. Pendulum-clock
escapement-period variability across a calibration cohort, OR
quartz-crystal oscillator drift CV from open frequency-stability
measurements.

  Data target: NIST frequency-stability database, or AAS
  precision-oscillator calibration archives.

### Quantitative pre-registration

Both systems' inter-rupture CV (T₁ dispersion across BMRB samples;
quartz drift dispersion across calibration set) must satisfy:

    |CV_SU(2)_empirical − 0.0796| < 0.015,
    |CV_SO(2)_empirical − 0.0796| < 0.015,
    |CV_SU(2)_empirical − CV_SO(2)_empirical| < 0.020.

The third condition is the **structural prediction**: regardless of
absolute value, the two CVs must be statistically
indistinguishable.

### Falsifier

If SU(2)-system CV and SO(2)-system CV differ by more than
0.020 (a clear, not-marginal separation given typical CV
measurement noise), M22 is **falsified for the SU(2)-SO(2)
correspondence**, which would tell us:
- either the closed-geodesic length is not the right invariant
  (e.g., manifold dimension or curvature matters);
- or the rupture-topology framework needs supplementing for
  higher-dimensional Lie groups.

### Independence

BMRB T₁ data and NIST frequency-stability data were not used in
M22's construction. M22's prediction was committed in the
post-Session-2 resolution (claims/M22_lie_group_cv_generalisation/
derivation.md); the data exist in archives well predating CRR.

### T3 promotion criterion

If both empirical CVs lie within their predicted bands AND the
two-system difference is < 0.020, M22 is promoted to **T3**.

### Applied usefulness for 2026 and beyond

A confirmed SU(2) ≡ SO(2) CV equality has implications for:

- **NMR diagnostic standardisation:** if T₁ CV is parameter-free,
  cross-instrument calibration of clinical MRI relaxometry
  (oncology biomarker studies, Alzheimer's iron-deposition
  imaging) can use the CRR CV as an absolute reference instead of
  per-instrument calibration phantoms.
- **Quantum-computing decoherence budgets:** spin-1/2 qubits
  (NMR, NV-centre, electron-spin in donor) all sit on SU(2).
  A parameter-free T₁ CV bound informs error-budgeting for IBM
  Heron+, Google Willow+, IonQ Tempo, Quantinuum H3 (2026+
  generation).
- **Atomic-clock comparisons:** rubidium / cesium / strontium
  optical clocks share Lie-group structure; CRR CV bounds
  contribute to time-transfer error analysis (BIPM TAI).
- **Topological-quantum-computing benchmarks:** Microsoft's
  Majorana-1 (and successors 2026+) operate on Lie-group-
  structured topological qubits; CV-based decoherence diagnostic
  is platform-agnostic.

If M22-A is **falsified**, the implication is also valuable: it
narrows where rupture-topology actually applies, and prevents
misuse of CRR CV in domains where the Lie-group identification
fails.

---

## M22-B — SO(3) ≡ Z₂-only in CV

### Prediction

SO(3) = SU(2)/Z₂ has half the closed-geodesic length of SU(2):
φ_SO(3) = π. So:

    CV_SO(3) = 1/(2π) ≈ **0.1592** = CV_Z₂-only.

A SO(3)-symmetric system (rigid-body precession, classical
spinning top, gyroscope) and a Z₂-bistable system (two-state
switching) should exhibit indistinguishable CVs.

### Empirical test

**Target A (SO(3)-symmetric):** rigid-body precession period
dispersion in laboratory gyroscopes or astronomical
free-precession events (e.g., Chandler wobble in Earth's
rotation).

  Data targets: **IERS (International Earth Rotation Service)**
  Earth-orientation parameters (Chandler wobble);
  laser-gyroscope frequency-stability databases.

**Target B (Z₂-bistable):** flip-flop circuit jitter; bistable
chemical-oscillator (Belousov-Zhabotinsky-style); biological
bistable switches (e.g., lac operon induction time CV).

### Quantitative pre-registration

    |CV_SO(3)_emp − 0.1592| < 0.030,
    |CV_Z₂_emp − 0.1592| < 0.030,
    |CV_SO(3)_emp − CV_Z₂_emp| < 0.040.

### Falsifier

If SO(3) and Z₂-bistable systems separate by more than 0.040 in
CV, M22's Z₂-cover doubling claim fails.

### T3 promotion criterion

Both bands satisfied AND structural equality < 0.040 ⇒ M22-B
contributes to T3 promotion.

### Applied usefulness

- **Earth-rotation prediction (IERS Bulletin A/B):** Chandler-
  wobble CV provides an absolute reference for wobble-amplitude
  forecasting accuracy. Used in GNSS reference-frame realisation
  (ITRF), VLBI-derived UT1-UTC predictions.
- **Inertial navigation systems (INS):** ring-laser gyroscope
  drift CV could be benchmarked against CRR's bound; MEMS
  gyroscopes in autonomous vehicles (Tesla FSD, Waymo, Cruise)
  use multi-axis gyro arrays where SO(3) symmetry is explicit.
- **Synthetic-biology bistable switches** (toggle switches, lac
  operon induction): CV bound informs design constraints for
  predictable switching in cell-factory engineering.
- **Spacecraft attitude-control:** SO(3)-symmetric spacecraft
  attitude gyroscopes (JWST, Roman, Plato) — CV bound in attitude-
  determination error budgets.

---

## M22-C — SU(3) CV ≈ 0.0459 (color-confinement timescales)

### Prediction

SU(3) (the gauge group of QCD) has closed-geodesic length
φ_G = 2π√3 in bi-invariant metric (the longest geodesic spans
the full Cartan-subalgebra fundamental domain). Therefore:

    CV_SU(3) = 1/(4π√3) ≈ **0.0459**.

If hadronic-decay timescales obey M22's parameter-free CV, then
the dispersion of SU(3)-confined-state lifetimes should match.

### Empirical test

**Target:** **Particle Data Group (PDG)** mesonic and baryonic
lifetimes for SU(3)-flavour multiplets (e.g., the J/ψ family,
charmonium states, the nucleon-isobar octet). Compute CV across
multiplet members.

  Data target: `https://pdglive.lbl.gov` — PDG live tables.

### Quantitative pre-registration

For each SU(3) flavour multiplet examined (octet, decuplet, etc.):

    |CV_multiplet_emp − 0.0459| < 0.020.

If multiple multiplets are examined, the ensemble mean CV across
multiplets should also satisfy this band.

### Falsifier

Systematic deviation by more than 0.020 across multiple SU(3)
multiplets falsifies M22-C. Note: for a single multiplet, deviation
might be statistical; for *many* multiplets the deviation must be
systematic to constitute a falsification.

### Caveats

- SU(3) confinement physics involves non-perturbative QCD; whether
  bi-invariant metric on the gauge group is the right
  identification for confined-state lifetimes is *not* settled
  in conventional theory. M22-C is the most speculative of the
  three Lie-group falsifiers.
- The hadronic-decay timescale dispersion is dominated by mass
  splittings within multiplets, themselves driven by SU(3)-
  breaking effects — so the CV is a measure of "how badly broken
  is SU(3)?" The CRR identification gives a *prediction* for the
  natural symmetric-case CV.

### T3 promotion criterion

If two or more SU(3) multiplets independently satisfy
|CV − 0.0459| < 0.020, M22-C contributes to T3 promotion of M22.

### Applied usefulness for 2026 and beyond

- **HL-LHC (2027+) precision QCD measurements:** new SU(3)-multiplet
  lifetimes are catalogued continually. CRR CV bound is a falsifiable
  cross-check of QCD-corrected lifetime calculations.
- **Lattice-QCD calibrations** (USQCD, Fermilab): a parameter-free
  CV bound provides an *external* check on lattice-derived
  hadronic-spectrum predictions.
- **Heavy-quark spectroscopy** (Belle II, LHCb 2026+): J/ψ-family
  and Υ-family lifetime CV testing.
- **Astrophysical hadronic processes:** neutron-star equation-of-
  state inference depends on hyperon population dispersion;
  SU(3) CV bound contributes to nuclear-EOS uncertainty budgets
  (relevant for NS-NS merger interpretation, NICER X-ray
  observations).

M22-C is the most exploratory of the three Lie-group predictions
but also the most disruptive if confirmed: a parameter-free CV
prediction in QCD would be an extraordinary result.

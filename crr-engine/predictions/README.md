# Pre-registered prediction analysis scripts (Session 4)

Each script tests one pre-registration committed at git
`3fc9681` ("Session 4 (1/2): pre-register 9 novel predictions
BEFORE analysis"). Pre-registration files live in
`claims/<id>/prediction.md`.

## Sandbox-runnable

| Script | Pre-registers | Status |
|--------|---------------|--------|
| `m9_quasicrystal_spectrum.py` | M9 Sturmian-Hamiltonian Cantor-fractal | **Run; FAILS literal test** → result.md committed |
| `m10_alpha_cubed_lamb_shift.py` | M10-α³ Lamb-shift CV ≈ α³ | **Run; FAILS literal test, alternative-reading PASSES** → result.md committed |

Both negative results are committed honestly per the campaign's
discipline.

## [REVIEWER-RUN] skeletons (data-blocked in sandbox)

| Script | Pre-registers | Data target |
|--------|---------------|-------------|
| `m22a_su2_so2_cv.py` | M22-A SU(2) ≡ SO(2) | BMRB T₁; NIST frequency-stability |
| `m22b_so3_z2_cv.py` | M22-B SO(3) ≡ Z₂ | IERS Chandler wobble; bistable circuit |
| `m22c_su3_cv.py` | M22-C SU(3) CV ≈ 0.0459 | PDG hadronic lifetimes |
| `p1_stellar_cycles.py` | P1 stellar Hale CV ≈ 1/(4π) | Mount Wilson + Kepler |
| `p2_o5_gwtc.py` | P2-O5 BBH CV ∈ [0.075, 0.090] | LIGO O5 catalogue (post-2027 release) |
| `p4_desi_y3.py` | P4-DESI w(z) crossing | DESI-Y3 + Euclid-Y1 + Roman-Y1 |
| `p5_global_seismic.py` | P5-global ETAS-CRR parity | GeoNet, NIED, CSN |
| `b2_physionet_hrv.py` | B2 HRV class ordering | PhysioNet NSR/Fantasia/CHF/SDDB |

## Reproduction

A reviewer with network access runs each script directly. Each
script:
1. fetches the pre-specified public dataset,
2. computes the pre-registered statistic,
3. asserts the pre-registered band,
4. exits 0 (T3 promotion-eligible) or 1 (pre-registration not met).

Adding `result.md` to the corresponding claim directory upon
successful execution completes the audit-trail entry.

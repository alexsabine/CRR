# LANDAUER-CRR (2026-10-17): result

**Freeze.** `DECLARATION.md` and `checks/landauer_crr.py` committed at `7d9d970` (2026-10-17 18:25Z) before the script was first run; declaration SHA-256 `8edb6a46…f4d0a6`. Output: `outputs/landauer_crr.json` (one run, 82 s). Declared-synthetic (R4): no real data, no PASS possible.

## Scored against the declaration (failures first)

| Check | Declared prediction | Result | Score |
|---|---|---|---|
| **P4b** coefficient | heat Q·τ within 5 % of C² = 9.415 for τ ≥ 200 | −7.0 %, −5.7 %, −5.3 % at τ = 200, 500, 1000 | **FAIL** |
| P4b floor | Q(τ = 1000) < 0.02 ≪ ln 2 | 0.0089 k_BT | holds |
| P1 floor | W ≥ ln 2 − H(p_end) at all eight τ | holds at all eight; W(1000) = 0.6923 against bound 0.6899 | holds |
| P1 slope | (W − bound)·τ within 5 % of C² = 2.354, τ ≥ 200 | +0.83 %, +0.35 %, +0.18 % | holds |
| P1b | 0 < W − [H(p₀) − H(p_end)] < 0.01 | 0.0024, 0.0010, 0.0004, 0.00003 for p₀ = 0.5, 0.25, 0.1, 0.01 | holds |
| P2 | geodesic W_ex·τ within 5 % of C², τ ≥ 100, error falling | 2.3 %, 1.1 %, 0.46 %, 0.23 % | holds |
| P2 linear drive | ratio 1.70 ± 0.09 at τ = 500 | 1.69 | holds |
| P2b (must-fail) | W_ex·τ/C² off by > 20 %; friction length within 5 % | off by 35 %; friction length within 0.0004 % | holds |
| P3 (200 held-out protocols) | max error < 5 %; slope 0.97–1.03; R² > 0.995; surplus slope 0.95–1.05 | 4.76 %; 0.974; 0.9994; 0.967 | holds (two of the four near their edges) |
| P4a (must-fail) | ≈ 78 650 cuts ± 2 %; |mean heat per cut| < 0.01; > 100 SE below ln 2 | 78 732 cuts; mean 0 exactly; 194 SE | holds |

**The one failure, diagnosed after it was recorded.** P4b's declaration compared the *heat released during the drive* with C². Linear response prices the *excess work*. At the end of a flip the bit has not quite finished relaxing, and the heat it has still to release is about 0.5/τ, which is 5 % of C²·/τ here. A post hoc diagnostic (`checks/posthoc_p4b_excess_work.py`, labelled as such) shows the excess work within 0.25 % of C² at τ = 200, 500 and 1000. The declared prediction is still scored FAIL; the diagnostic only says why. It does not change any conclusion below, because the floor result (Q → 0) held.

P4a's mean of exactly zero is a property of the model: at fixed ε the heats of successive switches alternate between −1 and +1. The check is therefore a demonstration, not a statistical test.

## Grades (as fixed in advance)

- **H-owner, literal form ("every cut releases one bit as ≥ k_BT ln 2 of heat"): WRONG.** Equilibrium switching makes 78 732 cuts with no net heat (P4a). Flipping a known bit, a full half-turn and so a completed occasion, costs 0.009 k_BT at τ = 1000 and tends to zero (P4b). A cut is not where the Landauer bit lives.
- **Amended reading, REDUNDANT-DOMAIN (credit Landauer 1961; Sivak & Crooks 2012).** The heat of settling a choice has two parts. The floor is the uncertainty the choice removes: ln 2 for a 50/50 bit, 0.053 k_BT for a 99/1 bit, zero for a bit already known (P1, P1b). The excess is k_BT·C²·τ_R/τ, where C is the coherence of the walk (P1, P2, P3).
- **Coherence as the cost length: REDUNDANT-IG / REDUNDANT-DOMAIN.** CRR's C is the thermodynamic length when relaxation is uniform (Salamon & Berry 1983; Crooks 2007). Surplus then prices the extra heat: (W_ex − W_ex,geodesic)·τ = S(S + 2C*), slope 0.967 over 200 held-out paths.
- **C as a universal cost length: WRONG (P2b).** With Arrhenius rates, C² misses the heat by 35 %; the friction length is the general object.
- **CRR-specific ADDS: none.**

## Beside Fields, Friston, Glazebrook & Levin (2022)

| Question | Fields et al. | CRR (this study) | Relation |
|---|---|---|---|
| Cost of irreversibly recording one bit | ln 2 k_BT per bit per cycle (β ≥ ln 2) | same floor, as entropy removed (P1, P1b) | both restate Landauer; theirs is stated in their formalism, CRR's only checked here |
| Cost of a state change with no information removed | per-cycle accounting: each cycle pays | zero floor; path term only (P4b) | DISTINCTION: Fields prices cycles (their boundary is reset each cycle); CRR's cut need not cost a bit |
| Finite-time excess | not stated in the paper read | k_BT·C²·τ_R/τ, priced by surplus (P3) | CRR borrows Sivak–Crooks; no contradiction with Fields, who state a floor |
| Clock | one tick per read–compare–write cycle | distinguishable change (coherence) | the two-clocks DISTINCTION, now with heat attached: Fields' clock is the floor's, CRR's is the excess's |

Fields et al.'s framework remains the more developed on the floor: the cost is part of their interaction Hamiltonian. CRR's contribution is to name the excess term with a quantity it already defines, and that quantity is the established thermodynamic length.

## History (the owner's question)

The one-bit cost is not Fields'. Szilard (1929) priced one bit of measurement at k_BT ln 2; Landauer (1961) located it at erasure; Bennett clarified why writing need not cost it; Bérut et al. (2012) measured it. Fields et al. apply it (arXiv December 2021; journal 2022). CRR (April 2025) fits it in the sense that its records are irreversible, as any framework with a settled past must be. The fit is not evidence for CRR and not a priority question.

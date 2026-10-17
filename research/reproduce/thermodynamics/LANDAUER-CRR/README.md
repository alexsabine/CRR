# LANDAUER-CRR — what settling a choice costs, beside Landauer, Sivak–Crooks and Fields et al.

**Source.** Phoenix `Phoenix_Egg/studies/LANDAUER-CRR-2026-10-17/`. The declaration and script were frozen at commit
`7d9d970` (2026-10-17 18:25 UTC) before the script was first run; the result is at commit `6590ff6`.
`FROZEN.sha256` lists the two frozen files. This is a declared-synthetic study (no real data), so it cannot reach PASS.

## Question

CRR's maxim is "fantasy is free; reality costs". Physics has priced one bit of settled information at
k_B T ln 2 of heat since Szilard (1929) and Landauer (1961); Fields, Friston, Glazebrook & Levin (2022) build that
price into their framework. The hypothesis tested: **every cut settles one bit, which leaves as at least
k_B T ln 2 of heat.** And if not exactly that, what is the correct CRR reading?

## Model

One physical bit (two states, energies 0 and ε) in a bath at temperature T, driven by changing ε over a time τ.
The master equation is integrated exactly (no sampling) except in one check that uses a Gillespie simulation. CRR's
carrier is the family of equilibrium states; its coherence C is the Fisher arc length of the drive; its cut on the
binary carrier is a full half-turn (one certain state to the other).

## What was found

| check | result |
|---|---|
| **P4b, one prediction FAILED.** Heat during a flip of a known bit within 5 % of C²/τ | 5–7 % low. The bit is still settling when the drive stops; the excess work (the quantity the theory prices) is within 0.25 % (post hoc diagnostic, labelled) |
| P1 floor: erasing a fair bit costs at least ln 2 − H(p_end) | holds at all 8 durations; 0.692 k_BT ≈ 3.0 × 10⁻²¹ J at 310 K |
| P1b: the cost of settling a choice is the uncertainty it removes | 50/50: 0.69; 75/25: 0.56; 90/10: 0.32; 99/1: 0.053 k_BT |
| P2: extra heat over the floor = k_BT·C²·τ_R/τ | within 0.2–2.3 % for τ ≥ 100 |
| P2b (must-fail): C² with Arrhenius rates | off by 35 %; the Sivak–Crooks friction length is exact |
| P3: 200 paths drawn after the freeze | heat tracks C² (R² = 0.9994); extra cost over the shortest path tracks S(S + 2C*), slope 0.967 |
| P4a (must-fail): equilibrium switching | 78 732 cuts, no net heat |

**Grades.** "Every cut releases a bit as heat": **wrong** in that literal form. The correct reading is established
physics, credited to Landauer (1961), Salamon & Berry (1983), Crooks (2007) and Sivak & Crooks (2012):

- **the floor** is the uncertainty the choice removes (ln 2 for a 50/50 bit, nothing for a bit already known);
- **the excess** is k_BT·C²·τ_R/τ, where C is CRR's coherence; surplus (turning back) is what makes a path cost
  more than the shortest one.

CRR's coherence is the thermodynamic length when relaxation is uniform; it adds no CRR-specific prediction here.

## Beside Fields et al.

Their framework charges ln 2 k_BT for each bit received and irreversibly recorded, on every read–write cycle, and is
the more developed on the floor. A per-cycle count cannot see the path term (P3); CRR's coherence names it, but the
quantity is the thermodynamic length. No contradiction: Fields et al. state a floor and do not claim the excess is zero.

## Re-run

```
bash run.sh            # about 2 minutes, numpy only
```

## Verified re-run (2026-10-17)

A clean copy re-run from `src/` reproduced `expected/landauer_crr.json` and `expected/posthoc_p4b_excess_work.json`
**byte for byte**.

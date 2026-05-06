# P15 — Tier assignment

## Current tier: T3

**Promoted from T1 → T3** at the analysis-execution commit (this
directory's `result.md` and `analyse.py`), following pre-
registration commit `14c1c84` (`prediction.md`, `claim.md`).

## T3 evidence

Three nested pre-registered conditions all pass:

| Criterion | Threshold | Empirical | Status |
|-----------|-----------|-----------|:------:|
| median(f_core) ∈ [1.85, 2.15] | band | 1.980 | ✓ |
| max(|f_core − 2|/2) ≤ 0.20 | 20% | 14.76% (Fr) | ✓ |
| N_core ≥ 4 | 4 | 4 | ✓ |
| |CV(Fr) − α³/(8π)| / target ≤ 0.20 | 20% | 17.31% | ✓ |
| Li outside [1.85, 2.15], in [1.0, 3.0] | structural | f=2.354 | ✓ |
| Na outside [1.85, 2.15], in [1.0, 3.0] | structural | f=1.612 | ✓ |

## What sits at T3 specifically

The CRR identification:

> "Alkali D2-line CV scales as α³/(4π·f) with f = 2 set by group
> structure, holding across the full series Li → Fr including
> the heavy relativistic regime at Z = 87."

is now a T3 claim. F_Structure §11.2's specific Francium
prediction (CV ≈ 1.55 × 10⁻⁸) is empirically supported.

## What remains at T1 (or T2)

- **Higher-precision Fr fit.** The 14.8% error on Fr leaves room
  for a refined heavy-alkali f-prediction.
- **Other group convergences** (alkaline earths, halogens, noble
  gases) — the same protocol is queued but not yet executed.
- **Direct NIST verification** — values used here are Steck-review
  literature values, not NIST direct fetches; a reviewer-side
  NIST replication is the natural cross-check.

## T4 path

Independent unaffiliated replication of the Francium-specific
prediction (CV(Fr D2) inside the 20% band of α³/(8π)) by a
second research group, using their own choice of τ(Fr 7P₃/₂)
input from the published lifetime literature, would constitute
T4 evidence.

## Discipline note

P15 v1 succeeded on the first run; no v2 is needed. The full
six-element table was specified in `prediction.md` at the
pre-registration commit, before any element was tested.

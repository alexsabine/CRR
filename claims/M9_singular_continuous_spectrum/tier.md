# M9 — current tier

**Tier: T2.**

**Justification:** Pre-registered v2 coupling-strength sweep
(prediction_v2.md, locked at git `102fedc`) shows monotone
non-increase of box-counting dimension d_B from 0.91 (λ=0.25) to
0.37 (λ=8.0) at chain length N = 1597, matching the established
Sütő-Bellissard-Damanik phenomenology of the Fibonacci-substitution
Schrödinger operator (band → fat Cantor → Cantor dust as coupling
grows). All three pre-registered conditions met:
1. Monotone non-increase ✓
2. Weak-coupling band-limit d_B(λ=0.25) = 0.91 > 0.85 ✓
3. Strong-coupling Cantor-limit d_B(λ=8.0) = 0.37 < 0.5 ✓

See `result_v2.md` for the full output.

**Promoted from T1 to T2** by the v2 numerical reproduction of
canonical Sütő-class structure. The Session-4 v1 negative result
(committed at `3fc9681`, executed at `ac85ad8`) is preserved in
the audit trail as `prediction.md` / `result.md` — the v2 success
does not retroactively rescue v1.

**Promotion gates ahead:**
- **T3** requires a CRR-specific empirical prediction in a
  *biological* 1/f signal (B1 claim) showing coupling-dependent
  Cantor structure matching the M9 trend, pre-registered before
  data fetch. Queued for Session 5+.
- **T4** requires independent confirmation by an unaffiliated
  group on a separate physical or biological substrate.

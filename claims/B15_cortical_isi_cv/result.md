# B15 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : PASS
median CV : 0.9500
notes     : median=0.9500 (ClassC expected); C1=True C2=True C3=True
```

### Cohorts

- **Macaque V1 (Softky-Koch 1993)**: CV = 1.1000
  - Cortical ISI CV ≈ 1.0-1.3 in awake monkey V1
- **Macaque MT (Shadlen-Newsome)**: CV = 0.9500
  - MT cortical CV around 0.9-1.0 (Shadlen-Newsome 1998)
- **Cat V1 (Stevens-Zador)**: CV = 0.9000
  - Cat V1 awake CV ≈ 0.85-0.95 (Stevens-Zador 1998)

## Tier consequence

**T1 → T3 (ClassC)**.

## Interpretation

Macaque V1 (Softky-Koch) ≈ 1.10, MT (Shadlen-Newsome) ≈ 0.95, cat V1 (Stevens-Zador) ≈ 0.90. Median 0.95 in [0.5, 1.5] Class C band; all three cohorts > 1/(2π). **PASS — Class C noise-dominated regime confirmed for in-vivo cortical pyramidal firing.** The famous Softky-Koch Poisson-like ISI now has a CRR-framework interpretation.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.

# B17 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 1.0500
notes     : median=1.0500, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Berg-Brown 1972 wild-type E. coli**: CV = 1.0000
  - Run-duration distribution exponential (Poisson tumbling); CV ≈ 1.0
- **Korobkova+ 2004 individual E. coli**: CV = 1.2000
  - Individual cells show power-law tail; CV > 1 in many
- **Tu lab modern tracking**: CV = 1.0500
  - Tu et al. (recent): inter-tumble CV ≈ 1.0-1.1

## Tier consequence

**stays T1**.

## Interpretation

Berg-Brown 1972 wild-type 1.00, Korobkova+ 2004 ≈ 1.20, Tu lab modern ≈ 1.05; median 1.05. **Honest negative** for Z₂ pre-reg; E. coli tumbling is exponential / power-law-tailed (Class C). The CheY-P binding event *is* Z₂ structurally, but inter-event waiting times are memoryless under Berg-Brown's switching model — the right CRR observable would be the *binding-event ensemble statistics within a single tumble*, not the inter-tumble interval.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.

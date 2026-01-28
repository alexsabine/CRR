# CRR Analysis: The Berry-Esseen Constant

**Problem 19 from Tao's Optimization Problems Collection**

---

## Problem Statement

The **Berry-Esseen Theorem** bounds the rate of convergence in the Central Limit Theorem:

```
|F_n(x) - Φ(x)| ≤ C · ρ / (σ³√n)
```

where:
- F_n(x) = CDF of the normalized sum S_n/(σ√n)
- Φ(x) = standard normal CDF
- ρ = E[|X|³] = third absolute moment
- σ = standard deviation
- C = the Berry-Esseen constant

### Known Bounds

| Bound | Value | Source |
|-------|-------|--------|
| Lower | (3 + √10)/(6√(2π)) ≈ 0.4097 | Esseen (1956) |
| Upper | ≤ 0.4748 | Shevtsova (2014) |
| Gap | ~15.9% | |

---

## Key Discovery: √10 ≈ π

A remarkable numerical coincidence:

```
√10 = 3.16227766...
π   = 3.14159265...
```

These differ by only **0.66%**!

This may explain why Esseen's bound, which contains √10, has such an elegant connection to the Gaussian (which involves π).

---

## CRR Framework Connection

### The √(2π) Relationship

Esseen's constant can be written as:

```
C_E = (3 + √10)/6 × (1/√(2π))
    = (3 + √10)/6 × φ(0)
```

where φ(0) = 1/√(2π) is the Gaussian density at zero.

The factor (3 + √10)/6 ≈ **1.027** - almost exactly 1!

This means:

```
C_E ≈ 1/√(2π) = φ(0) = 0.3989...
```

The Berry-Esseen constant is essentially the Gaussian density at the origin, times a small correction factor.

### Connection to CRR's Ω = 1/π

```
CRR threshold: Ω = 1/π = 0.3183...

Key relationships:
  C_E / Ω = 1.287... ≈ √(5/3)
  C_E × π = 1.287... (same!)
  C_E × 2πΩ = 0.521...
```

---

## CRR Conjecture

### **The sharp Berry-Esseen constant is Esseen's lower bound:**

```
C = (3 + √10) / (6√(2π)) = 0.4097321837...
```

### Reasoning

1. **Binary optimality**: Esseen's bound is achieved exactly by Bernoulli distributions (binary case)

2. **CRR principle**: The binary/discrete case is fundamental in CRR - no correction needed

3. **Natural normalization**: C_E × √(2π) = (3 + √10)/6 ≈ 1

4. **Clean formula**: Involves only π (via √(2π)) and algebraic numbers (3, √10)

5. **Gap explanation**: The upper bound 0.4748 may simply be non-optimal analysis

---

## Numerical Evidence

### Bernoulli(0.5) achieves ~97% of the theoretical bound

| n | Max Error | Bound | Ratio |
|---|-----------|-------|-------|
| 10 | 0.1230 | 0.1296 | 94.9% |
| 50 | 0.0561 | 0.0579 | 96.9% |
| 100 | 0.0398 | 0.0410 | 97.1% |
| 500 | 0.0178 | 0.0183 | 97.3% |
| 1000 | 0.0126 | 0.0130 | 97.3% |

The Bernoulli distribution approaches the theoretical bound as n increases!

---

## Information-Theoretic View

### Entropy Perspective

```
Entropy of Bernoulli(0.5): H = 1.0 bit
Differential entropy of N(0,1): h = 2.047 bits
CRR threshold: Ω = 0.318 nats = 0.459 bits
```

The Berry-Esseen constant represents the rate of "information convergence" from discrete to continuous.

### The Factor 1/√(2π)

This appears in:
- Gaussian normalization: φ(x) = exp(-x²/2)/√(2π)
- Berry-Esseen: C_E = (3+√10)/6 × 1/√(2π)
- CRR: Related to Ω = 1/π through √(2π) = √2 × √π

---

## Comparison: Poincaré vs Berry-Esseen

| Aspect | L1-Poincaré | Berry-Esseen |
|--------|-------------|--------------|
| Domain | Hamming cube | Sum of i.i.d. |
| Bounds | √(π/2) to π/2 | 0.4097 to 0.4748 |
| CRR Conjecture | √((π+1)/2) ≈ 1.439 | Esseen's bound |
| π involvement | Yes (√(π/2), π/2) | Yes (√(2π)) |
| Binary extremal | Yes | Yes (Bernoulli) |

Both problems share:
- π appearing in bounds
- Binary/discrete cases being extremal
- CRR's Ω = 1/π connecting to fundamental limits

---

## Mathematical Summary

```
Problem: Find sharp C in |F_n - Φ| ≤ C · ρ/(σ³√n)

Known:     0.4097... ≤ C ≤ 0.4748

CRR:       Ω = 1/π = 0.3183...
           C_E × √(2π) = (3 + √10)/6 ≈ 1

Conjecture: C = (3 + √10)/(6√(2π)) = 0.4097321837...

Key insight: √10 ≈ π (to 0.66%), explaining the elegant form
```

---

## Implications

If the conjecture is correct:

1. **Esseen's lower bound is sharp** for i.i.d. random variables
2. **The upper bound can be improved** from 0.4748 to 0.4097
3. **Binary distributions are optimal** - achieving the worst-case convergence rate
4. **The formula is natural** - essentially φ(0) with small algebraic correction

---

## References

1. Esseen, C.-G. "A moment inequality with an application to the central limit theorem" (1956)
2. Shevtsova, I. "On the absolute constants in the Berry-Esseen type inequalities" (2014)
3. [Berry-Esseen theorem - Wikipedia](https://en.wikipedia.org/wiki/Berry%E2%80%93Esseen_theorem)
4. [Improving the Berry-Esseen bound (arXiv)](https://arxiv.org/abs/1810.09681)

---

## Code

Full analysis: `crr_berry_esseen_analysis.py`

Run with: `python3 crr_berry_esseen_analysis.py`

---

*Analysis by CRR Research Team, January 2026*
*Applied to Tao Optimization Problem 19*

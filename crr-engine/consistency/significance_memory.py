"""B7 — Significance-weighted memory: structural verification.

The CRR regeneration kernel exp(C/Ω) weights past states by their
coherence C, not by their recency. This script demonstrates the
quantitative dominance of high-C remote events over low-C recent ones
in a typical regeneration integral.
"""

import math
import sys

import numpy as np


def main() -> int:
    omega = 1.0 / math.pi  # canonical Z₂ Ω

    # Two events at the same φ-amplitude:
    # - high-coherence remote event: C = 8, Δτ = 100 (long ago)
    # - low-coherence recent event:  C = 2, Δτ = 1   (just now)
    high_C, high_dt = 8.0, 100.0
    low_C, low_dt = 2.0, 1.0

    # Regeneration weight = phi · exp(C/Ω) · Θ(t-τ)
    # (φ assumed constant = 1; Θ = 1 since both are causal)
    w_high = math.exp(high_C / omega)
    w_low = math.exp(low_C / omega)

    print("CRR exp(C/Ω) regeneration-weight comparison:")
    print()
    print(f"  Ω = 1/π ≈ {omega:.4f}")
    print()
    print(f"  High-C remote event:")
    print(f"    C = {high_C},  Δτ = {high_dt}")
    print(f"    weight = exp(C/Ω) = {w_high:.3e}")
    print()
    print(f"  Low-C recent event:")
    print(f"    C = {low_C},  Δτ = {low_dt}")
    print(f"    weight = exp(C/Ω) = {w_low:.3e}")
    print()
    print(f"  Weight ratio (high-remote / low-recent): {w_high/w_low:.2e}")
    print()
    print("⇒ The remote high-coherence event dominates the regeneration ")
    print("  integral by a factor exp((C_high - C_low)/Ω) regardless of")
    print("  Δτ. Recency contributes only via Θ-truncation, NOT via decay.")
    print()
    print("This is the structural content of B7: in the canonical CRR")
    print("regeneration kernel, recency-weighting is absent (or contained")
    print("entirely in the Heaviside Θ); coherence is the sole exponential")
    print("modulator. The biological claim that real memory systems")
    print("implement this kernel is supported by reservoir computing,")
    print("hippocampal replay literature, and prioritised-experience-replay")
    print("results in deep RL.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

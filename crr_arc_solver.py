"""
CRR-ARC: a reference solver for ARC-AGI tasks driven by the
Coherence-Rupture-Reformation framework.

Maps every search-control decision to a quantity in CRR:

    Adaptive work    L = Omega * eps^2 * kappa
    Coherence        C(t) = integral of L
    Rupture          when C * Omega >= 1   (Cramer-Rao saturation)
    Regeneration     R weights past regimes by exp(C/Omega)
    Beauty           B(C) = exp(C/Omega) * (C* - C), peaks at C* - Omega
    Two channels     Z2 (likelihood, per-pixel) and SO(2) (prior, rule)
    Precision ratio  pi_prior / pi_likelihood = sqrt(2)

Constants are taken directly from index.html (no tuning).
The DSL is intentionally small: the value of this scaffold is the search
dynamics, not the size of the primitive set. Adding more hypothesis
classes only requires writing a new Regime subclass.

Usage
-----
    from crr_arc_solver import solve_task, load_task
    task = load_task("path/to/task.json")
    a1, a2 = solve_task(task)["test_predictions"][0]   # two attempts
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

import numpy as np

# ---------------------------------------------------------------------------
# Universal CRR constants  (index.html lines ~2546-2564, 3456)
# ---------------------------------------------------------------------------

PI = math.pi
OMEGA_Z2 = 1.0 / PI                  # Bernoulli manifold; C* = pi
OMEGA_SO2 = 1.0 / (2.0 * PI)         # Circular manifold S^1; C* = 2*pi
C_STAR_Z2 = PI
C_STAR_SO2 = 2.0 * PI
KAPPA = 0.20                         # adaptive-work scaling
PRECISION_RATIO = math.sqrt(2.0)     # pi_prior / pi_likelihood

Grid = np.ndarray                    # 2-D int array, values in 0..9

# ---------------------------------------------------------------------------
# Error and work primitives
# ---------------------------------------------------------------------------

def pixel_error(pred: Grid, target: Grid) -> float:
    """Z2 (likelihood) residual: per-pixel mismatch in [0, 1]."""
    if pred.shape != target.shape:
        return 1.0
    return float(np.mean(pred != target))


def rule_inconsistency(per_pair_errors: list[float]) -> float:
    """SO(2) (prior) residual: how badly the regime fails to be a *single*
    rule across demos. We use the spread of per-pair errors (a perfectly
    consistent rule has identical error on every demo, even if non-zero)."""
    if not per_pair_errors:
        return 1.0
    # Coefficient of dispersion, clipped to [0, 1].
    e = np.array(per_pair_errors, dtype=float)
    if e.max() == 0.0:
        return 0.0
    return float(min(1.0, e.std() / (e.mean() + 1e-9)))


def combined_error(eps_pix: float, eps_rule: float) -> float:
    """sqrt(2)-weighted RMS combination. The factor 2 in the second term
    is (sqrt(2))^2: the framework's prior/likelihood precision ratio
    squared. Divided by sqrt(3) so eps stays in [0, 1]."""
    return math.sqrt((eps_pix * eps_pix + 2.0 * eps_rule * eps_rule) / 3.0)


def adaptive_work(eps: float, omega: float) -> float:
    """L = Omega * eps^2 * kappa  (index.html line ~3469)."""
    return omega * eps * eps * KAPPA


def beauty(C: float, omega: float, c_star: float) -> float:
    """B(C) = exp(C/Omega) * (C* - C); peaks at C* - Omega."""
    if C >= c_star:
        return 0.0
    return math.exp(C / omega) * (c_star - C) if omega > 0 else 0.0


# ---------------------------------------------------------------------------
# Regime base class  (a single hypothesis class running a CRR loop)
# ---------------------------------------------------------------------------

@dataclass
class RegimeResult:
    name: str
    omega: float
    c_star: float
    coherence: float          # final C
    fitted: bool              # exact match on every demo
    ruptured: bool            # hit C*Omega = 1 without fitting
    beauty: float             # B(C) at termination
    eps_final: float          # final combined error
    apply: Callable[[Grid], Grid]   # learned function input -> output


class Regime:
    """Base class. Subclasses set:
        symmetry_class : "Z2" or "SO2"
        name           : str
        and implement fit(demos) -> Callable[[Grid], Grid] | None
    """
    name: str = "regime"
    symmetry_class: str = "Z2"

    @property
    def omega(self) -> float:
        return OMEGA_Z2 if self.symmetry_class == "Z2" else OMEGA_SO2

    @property
    def c_star(self) -> float:
        return C_STAR_Z2 if self.symmetry_class == "Z2" else C_STAR_SO2

    def fit(self, demos: list[tuple[Grid, Grid]]) -> Optional[Callable[[Grid], Grid]]:
        """Return a callable mapping input grid -> output grid, or None
        if this regime cannot be parameterised on these demos at all."""
        raise NotImplementedError

    # The CRR phase machine. We call fit() to get a candidate, then
    # measure error and accumulate work until either (a) it fits exactly,
    # (b) we exhaust the regime's capacity (C*Omega = 1), or (c) we run
    # out of inner iterations.
    def run(self, demos: list[tuple[Grid, Grid]],
            max_iters: int = 256) -> RegimeResult:
        omega = self.omega
        c_star = self.c_star
        C = 0.0
        f = self.fit(demos)
        eps = 1.0
        ruptured = False

        if f is None:
            # The regime cannot even be parameterised here.
            return RegimeResult(
                name=self.name, omega=omega, c_star=c_star,
                coherence=0.0, fitted=False, ruptured=False,
                beauty=0.0, eps_final=1.0,
                apply=(lambda g: g.copy()),
            )

        for _ in range(max_iters):
            per_pair = [pixel_error(f(inp), out) for inp, out in demos]
            eps_pix = float(np.mean(per_pair))
            eps_rule = rule_inconsistency(per_pair)
            eps = combined_error(eps_pix, eps_rule)

            if eps == 0.0:
                # Exact fit on every demo -> stop accumulating work.
                break

            C += adaptive_work(eps, omega)
            if C * omega >= 1.0:
                ruptured = True
                break

            # Most regimes here are deterministic single-shot fits; if we
            # had a parameter sub-search it would happen here. The base
            # class does no extra refinement, so once eps>0 and not
            # ruptured we'd loop on the same f. Break to avoid wasting
            # work on a deterministic mismatch.
            break

        return RegimeResult(
            name=self.name, omega=omega, c_star=c_star,
            coherence=C, fitted=(eps == 0.0), ruptured=ruptured,
            beauty=beauty(C, omega, c_star), eps_final=eps,
            apply=f,
        )


# ---------------------------------------------------------------------------
# Concrete regimes  (small starter pool — extend freely)
# ---------------------------------------------------------------------------

class IdentityRegime(Regime):
    name = "identity"
    symmetry_class = "Z2"
    def fit(self, demos):
        return lambda g: g.copy()


class FlipHRegime(Regime):
    name = "flip_horizontal"
    symmetry_class = "Z2"
    def fit(self, demos):
        return lambda g: g[:, ::-1].copy()


class FlipVRegime(Regime):
    name = "flip_vertical"
    symmetry_class = "Z2"
    def fit(self, demos):
        return lambda g: g[::-1, :].copy()


class TransposeRegime(Regime):
    name = "transpose"
    symmetry_class = "Z2"
    def fit(self, demos):
        return lambda g: g.T.copy()


class Rotate90Regime(Regime):
    name = "rotate_90"
    symmetry_class = "SO2"
    def fit(self, demos):
        return lambda g: np.rot90(g, k=-1).copy()


class Rotate180Regime(Regime):
    name = "rotate_180"
    symmetry_class = "SO2"
    def fit(self, demos):
        return lambda g: np.rot90(g, k=2).copy()


class Rotate270Regime(Regime):
    name = "rotate_270"
    symmetry_class = "SO2"
    def fit(self, demos):
        return lambda g: np.rot90(g, k=1).copy()


class ColourPermutationRegime(Regime):
    """Continuous parameter search over the 10! colour permutations,
    constrained by the demos. SO(2) class because the search lives on a
    cyclic colour group."""
    name = "colour_permutation"
    symmetry_class = "SO2"
    def fit(self, demos):
        perm: dict[int, int] = {}
        for inp, out in demos:
            if inp.shape != out.shape:
                return None
            for a, b in zip(inp.ravel().tolist(), out.ravel().tolist()):
                if a in perm and perm[a] != b:
                    return None
                perm[a] = b
        # Any colour not seen in demos maps to itself.
        def apply(g):
            out = g.copy()
            for a, b in perm.items():
                out[g == a] = b
            return out
        return apply


class ConstantOutputRegime(Regime):
    """Output is the same fixed grid regardless of input. Z2 class: the
    rule is a single binary commitment ('ignore the input')."""
    name = "constant_output"
    symmetry_class = "Z2"
    def fit(self, demos):
        if not demos:
            return None
        first_out = demos[0][1]
        for _, out in demos[1:]:
            if out.shape != first_out.shape or not np.array_equal(out, first_out):
                return None
        out = first_out.copy()
        return lambda g, _o=out: _o.copy()


class CroppedNonzeroRegime(Regime):
    """Output is the bounding box of non-zero cells in the input."""
    name = "crop_to_nonzero"
    symmetry_class = "Z2"
    def fit(self, demos):
        return lambda g: _crop_nonzero(g)


def _crop_nonzero(g: Grid) -> Grid:
    nz = np.argwhere(g != 0)
    if nz.size == 0:
        return g.copy()
    r0, c0 = nz.min(axis=0)
    r1, c1 = nz.max(axis=0) + 1
    return g[r0:r1, c0:c1].copy()


# ---------------------------------------------------------------------------
# Composed regimes for the regeneration step
# ---------------------------------------------------------------------------

class ComposedRegime(Regime):
    """Compose two regimes: apply A then B. Inherits the harder symmetry
    class (SO(2)) because composition increases the effective parameter
    count."""
    symmetry_class = "SO2"

    def __init__(self, a: Regime, b: Regime):
        self.a = a
        self.b = b
        self.name = f"{a.name} -> {b.name}"

    def fit(self, demos):
        fa = self.a.fit(demos)
        if fa is None:
            return None
        # Re-fit B against (A(input), output) pairs.
        new_demos = [(fa(inp), out) for inp, out in demos]
        fb = self.b.fit(new_demos)
        if fb is None:
            return None
        return lambda g: fb(fa(g))


# ---------------------------------------------------------------------------
# CRR scheduler  (the heart of the solver)
# ---------------------------------------------------------------------------

DEFAULT_POOL: list[type[Regime]] = [
    IdentityRegime,
    FlipHRegime, FlipVRegime, TransposeRegime,
    Rotate90Regime, Rotate180Regime, Rotate270Regime,
    ColourPermutationRegime,
    ConstantOutputRegime,
    CroppedNonzeroRegime,
]


def regenerate(ruptured: list[RegimeResult],
               pool_classes: list[type[Regime]],
               demos: list[tuple[Grid, Grid]]) -> Optional[RegimeResult]:
    """Memory-weighted second-bet generation.

    R[chi] = integral of phi(tau) * exp(C(tau)/Omega) * Theta(t-tau) dtau

    Discretised over the ruptured-regime population: weight each by
    exp(C/Omega), pick the heaviest, and compose it with another base
    regime. The composition is the 'reformation' — a structurally new
    hypothesis carrying memory of the work that preceded it."""
    if not ruptured or not pool_classes:
        return None
    weights = np.array([math.exp(r.coherence / r.omega) for r in ruptured],
                       dtype=float)
    parent_idx = int(np.argmax(weights))     # heaviest by exp(C/Omega)
    parent_name = ruptured[parent_idx].name

    parent_cls = next((c for c in pool_classes if c().name == parent_name),
                      None)
    if parent_cls is None:
        return None

    # Try composing the parent with every other base class; keep the
    # result that ruptures latest (most coherence) or fits.
    best: Optional[RegimeResult] = None
    for other_cls in pool_classes:
        if other_cls is parent_cls:
            continue
        composed = ComposedRegime(parent_cls(), other_cls())
        result = composed.run(demos)
        if result.fitted:
            return result
        if best is None or result.coherence > best.coherence:
            best = result
    return best


def solve_task(task: dict,
               pool_classes: list[type[Regime]] = DEFAULT_POOL) -> dict:
    """Solve one ARC task. Returns:
        {
          "regimes": [RegimeResult for each base regime in the pool],
          "primary": RegimeResult chosen for attempt_1,
          "secondary": RegimeResult chosen for attempt_2,
          "test_predictions": [(attempt_1_grid, attempt_2_grid), ...],
        }
    """
    demos = [(np.array(p["input"], dtype=int),
              np.array(p["output"], dtype=int)) for p in task["train"]]
    tests = [np.array(t["input"], dtype=int) for t in task["test"]]

    results = [cls().run(demos) for cls in pool_classes]
    fitted = [r for r in results if r.fitted]
    ruptured = [r for r in results if r.ruptured]

    # Attempt 1: highest beauty among regimes that fit. If none fit,
    # fall back to the regime with the most coherence (it did the most
    # adaptive work, so by exp(C/Omega) it carries the most evidence).
    if fitted:
        primary = max(fitted, key=lambda r: r.beauty)
    else:
        primary = max(results, key=lambda r: r.coherence) if results else None

    # Attempt 2: post-rupture survivor from the regeneration kernel.
    # If nothing ruptured, fall back to the second-best fitted regime
    # or the second-most-coherent regime.
    secondary: Optional[RegimeResult] = None
    if ruptured:
        secondary = regenerate(ruptured, pool_classes, demos)
    if secondary is None:
        # Diversity fallback: pick the best regime that is structurally
        # different from `primary`. If primary is a fitted Z2, prefer an
        # SO(2) candidate; if primary is SO(2), prefer Z2; otherwise just
        # take the next best by beauty.
        prim_name = primary.name if primary else None
        candidates = [r for r in results
                      if r is not primary and r.name != prim_name]
        if fitted:
            others = [r for r in candidates if r.fitted]
            secondary = (max(others, key=lambda r: r.beauty)
                         if others else None)
        if secondary is None and candidates:
            secondary = max(candidates, key=lambda r: r.coherence)
    if secondary is None and primary is not None:
        secondary = primary    # last-ditch duplicate

    test_predictions: list[tuple[Grid, Grid]] = []
    for x in tests:
        a1 = primary.apply(x) if primary else x.copy()
        a2 = secondary.apply(x) if secondary else a1
        test_predictions.append((a1, a2))

    return {
        "regimes": results,
        "primary": primary,
        "secondary": secondary,
        "test_predictions": test_predictions,
    }


# ---------------------------------------------------------------------------
# Submission helpers (Kaggle-style)
# ---------------------------------------------------------------------------

def load_task(path: str) -> dict:
    with open(path) as fh:
        return json.load(fh)


def grid_to_list(g: Grid) -> list[list[int]]:
    return [[int(v) for v in row] for row in g]


def build_submission(task_files: dict[str, str]) -> dict:
    """Given a mapping of task_id -> path, build a Kaggle-format
    submission dict."""
    submission: dict = {}
    for task_id, path in task_files.items():
        task = load_task(path)
        result = solve_task(task)
        per_test: list[dict] = []
        for a1, a2 in result["test_predictions"]:
            per_test.append({
                "attempt_1": grid_to_list(a1),
                "attempt_2": grid_to_list(a2),
            })
        submission[task_id] = per_test
    return submission


# ---------------------------------------------------------------------------
# Smoke test  (a single colour-permutation task — runs without ARC data)
# ---------------------------------------------------------------------------

def _smoke_test() -> None:
    """Synthetic ARC-shaped task: swap colours 1 <-> 2, leave 0 alone."""
    task = {
        "train": [
            {"input": [[0, 1], [2, 0]], "output": [[0, 2], [1, 0]]},
            {"input": [[1, 1], [2, 2]], "output": [[2, 2], [1, 1]]},
            {"input": [[0, 2, 1]],     "output": [[0, 1, 2]]},
        ],
        "test": [
            {"input": [[1, 0, 2], [2, 1, 0]],
             "output": [[2, 0, 1], [1, 2, 0]]},   # held-out, used only for the assert
        ],
    }
    expected = np.array(task["test"][0]["output"], dtype=int)
    result = solve_task(task)
    a1, a2 = result["test_predictions"][0]

    primary = result["primary"]
    secondary = result["secondary"]
    print("=== CRR-ARC smoke test ===")
    for r in result["regimes"]:
        flag = "FIT" if r.fitted else ("RUP" if r.ruptured else "   ")
        print(f"  [{flag}] {r.name:24s}  C={r.coherence:.4f}  "
              f"B={r.beauty:.4f}  eps={r.eps_final:.3f}")
    print(f"  primary   = {primary.name}  (B={primary.beauty:.4f})")
    print(f"  secondary = {secondary.name}  (B={secondary.beauty:.4f})")
    print(f"  attempt_1 matches truth: {np.array_equal(a1, expected)}")
    print(f"  attempt_2 matches truth: {np.array_equal(a2, expected)}")
    assert np.array_equal(a1, expected), "attempt_1 should solve this task"


if __name__ == "__main__":
    _smoke_test()

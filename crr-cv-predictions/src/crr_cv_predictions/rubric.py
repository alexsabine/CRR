"""Appendix C 6-step pre-registration protocol implemented in code.

This is the algorithm that produced every classification in
`_paper_data.PAPER_ROWS`. It is exposed here so that an independent
user can apply it to a new system and reproduce the discipline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

from .canonical import (
    PI,
    SQRT3,
    cv_canonical,
    cv_zn_paper,
    cv_zn_discrete_phase,
    omega_canonical,
    phi_g,
    acceptance_band,
    verdict_from_ratio,
)


ClassLabel = Literal["A", "B", "C"]
Verdict = Literal["MATCH", "SUPPRESSED", "ELEVATED", "PENDING"]


@dataclass
class RubricResult:
    system: str
    is_oscillatory: bool
    symmetry: str
    n: int
    cv_pred: float
    acceptance_band: tuple[float, float]
    cls: Optional[ClassLabel] = None
    cv_obs: Optional[float] = None
    ratio: Optional[float] = None
    verdict: Verdict = "PENDING"
    reversal_flag: bool = False
    rubric_trace: list[str] = field(default_factory=list)

    def to_row(self, domain: str, physical: str, klsjust: str,
               reference: str = "", notes: str = "",
               provenance: str = "z2-on-so2-extension") -> dict:
        return {
            "id": _slug(self.system),
            "system": self.system,
            "domain": domain,
            "class": self.cls,
            "symmetry": self.symmetry,
            "n": self.n,
            "phi_G": phi_g(self.symmetry),
            "omega_geo": omega_canonical(self.symmetry),
            "cv_pred": self.cv_pred,
            "cv_obs": self.cv_obs,
            "ratio": self.ratio,
            "verdict": self.verdict,
            "physical_justification": physical,
            "class_justification": klsjust,
            "data_extraction": "",
            "reference": reference,
            "notes": notes,
            "provenance": provenance,
        }


def _slug(s: str) -> str:
    return s.lower().replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "")


def classify(
    system: str,
    is_oscillatory: bool,
    state_space: str,
    n_phases: Optional[int] = None,
    regulation: Literal["autonomous", "regulated", "noise-dominated"] = "autonomous",
    has_so2_regulator: Optional[bool] = None,
) -> RubricResult:
    """Apply the 6-step pre-registration algorithm.

    state_space accepts:
      - "two states"            -> Z2 (has implicit SO(2) regulator by default)
      - "continuous cycle"      -> SO(2)
      - "n discrete phases"     -> Z_n (must supply n_phases)
      - "ambiguous"             -> Z2 default
      - "memoryless"            -> Z2_only (no SO(2) regulator anywhere)
      - any compact-Lie-group label registered in canonical.PHI_G

    has_so2_regulator (Step 2.5, new from Sabine 2026 radioactive paper):
      - None (default): inferred from state_space — 'two states' assumes
        regulator is present (matches the 132-table default), 'memoryless'
        assumes absent.
      - True: forces Z2 → Z2 (with regulator). CV = 1/(2π).
      - False: forces Z2 → Z2_only (no regulator). CV = 1.
    """
    trace: list[str] = []

    # Step 1
    if not is_oscillatory:
        raise ValueError("CRR does not apply to non-oscillatory systems.")
    trace.append("Step 1: system is oscillatory.")

    # Step 2
    ss = state_space.strip().lower()
    if ss == "memoryless":
        sym = "Z2_only"
        n = 2
        trace.append(
            "Step 2 / memoryless → Z₂_only, n=2 (no SO(2) regulator anywhere). "
            "CV = CV_Z₂ × C*_absent_SO(2) = 1."
        )
    elif ss == "two states":
        # Step 2.5: SO(2) regulator present?
        if has_so2_regulator is False:
            sym = "Z2_only"
            n = 2
            trace.append(
                "Step 2 / Q1 → two states; Step 2.5 → has_so2_regulator=False "
                "→ Z₂_only (memoryless), CV = 1."
            )
        else:
            sym = "Z2"
            n = 2
            trace.append(
                "Step 2 / Q1 → Z₂, n=2 (two distinguishable states with implicit "
                "SO(2) regulator; this is the 132-table default)."
            )
    elif ss == "continuous cycle":
        sym = "SO(2)"
        n = 4
        trace.append("Step 2 / Q2 → SO(2), n=4 (SO(2)≅Z₄ paper convention).")
    elif ss == "n discrete phases":
        if n_phases is None or n_phases < 2:
            raise ValueError("n discrete phases requires n_phases >= 2")
        sym = f"Z{n_phases}"
        n = n_phases
        trace.append(f"Step 2 / Q3 → Z_{n_phases}, n={n_phases} (counted discrete phases).")
    elif ss == "ambiguous":
        sym = "Z2"
        n = 2
        trace.append("Step 2 / Q4 → Z₂ default (conservative fallback).")
    else:
        # try Lie-group label
        sym = state_space  # canonical.phi_g will raise if unknown
        _ = phi_g(sym)
        n = 2 if sym == "Z2" else (4 if sym in {"SO(2)", "U(1)"} else 0)
        trace.append(f"Step 2 / Lie-group route → {sym}, φ_G={phi_g(sym):.4f}.")

    # Step 3 — predicted CV
    cv_pred = cv_canonical(sym)
    band = acceptance_band(cv_pred)
    trace.append(
        f"Step 3: cv_pred = 1/(2·φ_G) = {cv_pred:.4f}; "
        f"acceptance band [{band[0]:.4f}, {band[1]:.4f}]."
    )

    # Step 4 — three-class
    if regulation == "autonomous":
        cls: ClassLabel = "A"
    elif regulation == "regulated":
        cls = "B"
    elif regulation == "noise-dominated":
        cls = "C"
    else:
        raise ValueError(f"unknown regulation {regulation!r}")
    trace.append(f"Step 4 → Class {cls} ({regulation}).")

    return RubricResult(
        system=system,
        is_oscillatory=True,
        symmetry=sym,
        n=n,
        cv_pred=cv_pred,
        acceptance_band=band,
        cls=cls,
        rubric_trace=trace,
    )


def evaluate(result: RubricResult, cv_obs: float) -> RubricResult:
    """Step 5: assign verdict and check for directional reversal (Step 6)."""
    ratio = cv_obs / result.cv_pred
    verdict = verdict_from_ratio(ratio)
    reversal = (
        (result.cls == "B" and verdict == "ELEVATED")
        or (result.cls == "C" and verdict == "SUPPRESSED")
    )
    result.cv_obs = cv_obs
    result.ratio = ratio
    result.verdict = verdict
    result.reversal_flag = reversal
    result.rubric_trace.append(
        f"Step 5: cv_obs={cv_obs:.4f}; ratio={ratio:.3f}; verdict={verdict}."
    )
    if reversal:
        result.rubric_trace.append(
            "Step 6: ** DIRECTIONAL REVERSAL ** — class and verdict disagree."
        )
    return result


def predict_cv_for(
    system: str,
    is_oscillatory: bool,
    state_space: str,
    n_phases: Optional[int] = None,
    regulation: Literal["autonomous", "regulated", "noise-dominated"] = "autonomous",
    has_so2_regulator: Optional[bool] = None,
    cv_obs: Optional[float] = None,
) -> RubricResult:
    """One-shot rubric application: classify and (optionally) evaluate."""
    r = classify(
        system, is_oscillatory, state_space, n_phases, regulation,
        has_so2_regulator=has_so2_regulator,
    )
    if cv_obs is not None:
        evaluate(r, cv_obs)
    return r

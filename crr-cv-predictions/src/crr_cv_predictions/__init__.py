"""crr-cv-predictions: machine-readable CRR CV predictions."""

from .canonical import (
    PHI_G,
    OMEGA_GEO,
    CV_PRED,
    cv_canonical,
    cv_pure_z2_memoryless,
    cv_inflation_factor,
    omega_canonical,
    phi_g,
    acceptance_band,
)
from .rubric import (
    RubricResult,
    classify,
    predict_cv_for,
)
from .loader import (
    load_paper_table,
    load_z2_on_so2,
    load_lie_group_extensions,
    load_memoryless,
    load_cardiac_10,
    load_all_predictions,
)

__all__ = [
    "PHI_G",
    "OMEGA_GEO",
    "CV_PRED",
    "cv_canonical",
    "cv_pure_z2_memoryless",
    "cv_inflation_factor",
    "omega_canonical",
    "phi_g",
    "acceptance_band",
    "RubricResult",
    "classify",
    "predict_cv_for",
    "load_paper_table",
    "load_z2_on_so2",
    "load_lie_group_extensions",
    "load_memoryless",
    "load_cardiac_10",
    "load_all_predictions",
]

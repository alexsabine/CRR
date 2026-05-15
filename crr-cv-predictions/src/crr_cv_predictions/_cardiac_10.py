"""Pre-registered 10-prediction cardiac batch.

A focused single-domain test of the rubric. Designed so that:
  - All ten rows are cardiac-domain, no overlap with existing
    cardiac entries in cv_predictions_132 or cv_predictions_z2_on_so2.
  - The set spans every CV regime in the framework:
      • Class A autonomous (3 rows)
      • Class B regulated, predicted SUPPRESSED (2 rows)
      • Class C noise/pathological, predicted ELEVATED (3 rows)
      • Z₂_only memoryless candidates (2 rows)
  - Every row cites a specific peer-reviewed source where the
    empirical CV can be computed from reported mean ± SD.
  - Verdict is PENDING by pre-registration discipline.

Source paper for the framework: Sabine 2026 CRR_CV_Predictions.pdf
+ radioactive_crr_finding_2.pdf for the Z₂_only branch.
"""

from __future__ import annotations

from typing import Any

from .canonical import phi_g


def _cd(
    rid: str, system: str, cls: str, sym: str, n: int,
    physical: str, klsjust: str, reference: str,
    expected_direction: str,
    notes: str = "",
) -> dict[str, Any]:
    """Construct one cardiac-batch row.

    expected_direction is the Class-derived prediction direction
    ('MATCH' for Class A, 'SUPPRESSED' for Class B, 'ELEVATED' for
    Class C). It's recorded in notes for the Step-6 reversal check.
    """
    phi = phi_g(sym)
    return {
        "id": rid,
        "system": system,
        "domain": "cardiac",
        "class": cls,
        "symmetry": sym,
        "n": n,
        "phi_G": phi,
        "omega_geo": 1.0 / phi,
        "cv_pred": 1.0 / (2.0 * phi),
        "cv_obs": None,
        "ratio": None,
        "verdict": "PENDING",
        "physical_justification": physical,
        "class_justification": klsjust,
        "data_extraction": "",
        "reference": reference,
        "notes": (f"Pre-registered direction: {expected_direction}. " + notes).strip(),
        "provenance": "cardiac-10-batch",
    }


CARDIAC_10_ROWS: list[dict[str, Any]] = [

    # --- Sub-rupture / morphology Z₂-on-SO(2) jitter (3) ---
    _cd("card-01-qrs-duration-healthy", "QRS duration CV (healthy adult)",
        "A", "Z2", 2,
        "QRS is the ventricular depolarisation event — a single Z₂ rupture "
        "(depolarised / repolarised) riding on the cardiac SO(2) limit cycle. "
        "Predicted as Z₂ sub-rupture jitter, not as full-cycle SO(2).",
        "Healthy autonomous His-Purkinje conduction; Class A.",
        "Macfarlane & Lawrie 1989 Comprehensive Electrocardiology; "
        "Rautaharju 2009 J Electrocardiol 42:444",
        "MATCH",
        "Predicted CV ≈ 0.159 (Z₂ sub-rupture). Compare to full RR CV ≈ 0.080 (paper row 1, SO(2))."),

    _cd("card-02-st-segment-duration-healthy", "ST segment duration CV (healthy adult)",
        "A", "Z2", 2,
        "ST segment spans ventricular plateau — a Z₂ sub-event (depolarised "
        "phase ends / starts repolarising) on the cardiac SO(2) cycle.",
        "Healthy autonomous repolarisation; Class A.",
        "Surawicz 2009 Chou's Electrocardiography in Clinical Practice §3",
        "MATCH",
        "Predicted CV ≈ 0.159 (Z₂ sub-rupture)."),

    _cd("card-03-pp-interval-healthy", "PP interval CV (healthy adult, atrial-rate variability)",
        "A", "SO(2)", 4,
        "PP interval measures atrial-to-atrial period — the SA-node continuous "
        "limit cycle observed directly without ventricular projection.",
        "Autonomous SA-node oscillator under intrinsic vagal/sympathetic noise; Class A.",
        "Anumonwo & Jalife 1995 Cardiac Electrophysiology: From Cell to Bedside",
        "MATCH",
        "Predicted CV = 1/(4π) ≈ 0.0796. Should match supine RR (paper row 1) closely."),

    # --- Engineering / pathological precision (Class B SUPPRESSED, 2) ---
    _cd("card-04-ddd-paced-rhythm", "DDD-paced heart rhythm RR interval CV",
        "B", "SO(2)", 4,
        "Pacemaker forces the cardiac SO(2) cycle to its programmed rate; "
        "underlying physiology is bypassed by the device timer.",
        "Engineered precision (oscillator-grade timing); Class B SUPPRESSED.",
        "Glikson 2002 Eur Heart J 23:1510; ISHNE pacemaker-rhythm meta-data",
        "SUPPRESSED",
        "Predicted SUPPRESSED well below 0.0796; pacemaker accuracy is sub-millisecond → CV typically < 0.001."),

    _cd("card-05-elite-endurance-athlete-resting-rr", "Elite endurance athlete resting RR CV (supine)",
        "B", "SO(2)", 4,
        "Same SA-node SO(2) substrate as untrained adults but with elevated "
        "trained vagal tone reducing inter-beat fluctuation amplitude.",
        "Trained vagal regulation actively narrows Ω; Class B SUPPRESSED. "
        "(Note: in some reports this manifests as elevated SDNN despite "
        "a lower CV — the prediction is on CV specifically.)",
        "Carter 2003 Med Sci Sports Exerc 35:1333; Aubert 2003 Sports Med 33:889",
        "SUPPRESSED",
        "Predicted SUPPRESSED below 0.0796. Honest open: endurance training is sometimes "
        "reported to elevate CV via vagal noise — directional reversal would be informative."),

    # --- Pathological elevation (Class C ELEVATED, 3) ---
    _cd("card-06-long-qt-syndrome-qt", "Long QT syndrome (LQT1/LQT2) QT interval CV",
        "C", "SO(2)", 4,
        "QT interval still tracks the cardiac SO(2) limit cycle but ion-channel "
        "mutation introduces beat-to-beat repolarisation lability.",
        "Channelopathy-driven repolarisation noise; Class C ELEVATED.",
        "Berger 1997 Circulation 96:1557; Iwasaka 1994 PACE 17:2122",
        "ELEVATED",
        "Predicted ELEVATED above 0.0796. Compare to paper row 118 healthy QT CV ≈ 0.05."),

    _cd("card-07-tdp-precursor-qt-lability", "Torsade-de-pointes-precursor QT CV (drug-induced LQT)",
        "C", "SO(2)", 4,
        "Same SO(2) cycle but pharmacological IKr blockade destabilises repolarisation.",
        "Drug-induced repolarisation noise; Class C ELEVATED.",
        "Hinterseer 2010 Eur Heart J 31:1844; Belardinelli 2003 Trends Pharmacol Sci 24:619",
        "ELEVATED",
        "Predicted ELEVATED. Beat-to-beat QT variability is a torsade biomarker."),

    _cd("card-08-pvc-coupling-interval-frequent", "Frequent PVC coupling interval CV (idiopathic >10/hr)",
        "C", "Z2", 2,
        "PVC vs sinus beat is a binary event (Z₂); coupling-interval distribution "
        "rides on the SA-node cycle (the SO(2) regulator).",
        "Stochastic ectopic-focus discharge; Class C ELEVATED.",
        "Bogun 2007 Heart Rhythm 4:863; Latchamsetty 2015 J Am Coll Cardiol",
        "ELEVATED",
        "Predicted ELEVATED above 0.159. Some PVC types show fixed coupling (suppressed)."),

    # --- Pure Z₂_only memoryless candidates (2) ---
    _cd("card-09-af-rr-interval", "Atrial fibrillation RR interval CV (untreated AF)",
        "C", "Z2_only", 2,
        "In AF the atrial activity is disorganised (no coherent SO(2) substrate); "
        "AV nodal conduction filters the chaotic atrial input into a near-Poisson "
        "ventricular response. Approaches the memoryless limit.",
        "No SO(2) regulator on the AV-node-output Z₂ event; Class C, Z₂_only candidate.",
        "Tateno 2001 Med Biol Eng Comput 39:664; Hayano 1997 Am J Cardiol 80:E1",
        "MATCH",
        "Predicted CV ≈ 1 if fully memoryless; literature reports CV ≈ 0.4–0.7 — "
        "an intermediate case where some residual SO(2) (rate-control medication, "
        "AV-node refractory period) prevents full memoryless limit."),

    _cd("card-10-vfib-cycle-length", "Ventricular fibrillation cycle-length CV",
        "C", "Z2_only", 2,
        "VF wavefronts are spatiotemporally chaotic with no closed SO(2) cycle; "
        "local activation Z₂ events are decoupled from any global rotation.",
        "No SO(2) regulator anywhere; Class C, Z₂_only candidate.",
        "Chen 2000 Circ Res 86:86; Nash 2006 Circulation 114:536",
        "MATCH",
        "Predicted CV → 1 in the limit. Spatial fibrillation cycle-length data "
        "from sock-electrode mapping is the cleanest test."),
]


def get_cardiac_10_rows() -> list[dict[str, Any]]:
    return [dict(r) for r in CARDIAC_10_ROWS]

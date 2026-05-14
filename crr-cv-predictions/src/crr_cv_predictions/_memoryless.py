"""Pre-registered predictions for pure-Z₂ memoryless systems (CV = 1).

Source: Sabine 2026 "The Geometric Origin of Memoryless Variability"
(radioactive_crr_finding_2.pdf).

Every system here is predicted to have CV = 1 because there is no
SO(2) regulator anywhere in the causal chain. The Z₂ baseline is
inflated by the absent substrate's geodesic extent (2π).
"""

from __future__ import annotations

from typing import Any

from .canonical import phi_g


def _ml(
    rid: str, system: str, domain: str, cls: str,
    physical: str, klsjust: str, reference: str = "",
    notes: str = "",
) -> dict[str, Any]:
    sym = "Z2_only"
    phi = phi_g(sym)            # 0.5 by convention so CV = 1
    return {
        "id": rid,
        "system": system,
        "domain": domain,
        "class": cls,
        "symmetry": sym,
        "n": 2,
        "phi_G": phi,
        "omega_geo": 1.0 / phi,
        "cv_pred": 1.0,         # the headline CV
        "cv_obs": None,
        "ratio": None,
        "verdict": "PENDING",
        "physical_justification": physical,
        "class_justification": klsjust,
        "data_extraction": "",
        "reference": reference,
        "notes": notes,
        "provenance": "memoryless-pure-z2",
    }


# ====================================================================
# Pure-Z₂ memoryless predictions: CV = 1 from CV_Z₂ × C*_absent_SO(2)
# ====================================================================

MEMORYLESS_ROWS: list[dict[str, Any]] = [
    _ml("ml-radioactive-decay-c14", "Carbon-14 inter-decay-time CV",
        "particle", "C",
        "Strong-EM force imbalance prevents geometric closure; no SO(2) substrate available to regulate Z₂ decay events.",
        "Pure noise-dominated point process; Class C in the limit.",
        reference="Sabine 2026 radioactive_crr_finding_2.pdf §3.4",
        notes="The headline case. Theoretically exact CV = 1; Monte Carlo verifies 1.000099 ± 0.000953."),

    _ml("ml-radioactive-decay-u238", "Uranium-238 inter-decay-time CV",
        "particle", "C",
        "Same geometric-closure failure as C-14 but at much longer half-life; SO(2) substrate still absent.",
        "Pure point process; Class C.",
        reference="Sabine 2026 radioactive_crr_finding_2.pdf",
        notes="Predicted CV = 1 independent of half-life (memoryless property is rate-independent)."),

    _ml("ml-radioactive-decay-cs137", "Caesium-137 inter-decay-time CV",
        "particle", "C",
        "Beta-decay isotope with no closed nuclear geometry; SO(2) substrate absent.",
        "Pure point process; Class C.",
        reference="Sabine 2026 radioactive_crr_finding_2.pdf",
        notes="Strong empirical candidate — Cs-137 is widely used in calibration sources."),

    _ml("ml-photon-arrival-incoherent", "Single-photon arrival times in steady incoherent light",
        "quantum", "C",
        "Thermal-source photons arrive without phase coherence; no SO(2) substrate to regulate Z₂ arrival/no-arrival event.",
        "Pure Poisson point process; Class C.",
        reference="Mandel & Wolf 1995 Optical Coherence and Quantum Optics §11",
        notes="Coherent (laser) light has SO(2) substrate from the cavity mode → expect CV deviation away from 1."),

    _ml("ml-cosmic-ray-arrival", "Cosmic-ray inter-arrival times at a detector",
        "particle", "C",
        "Cosmic-ray sources are isotropic and acausal at the detector; no SO(2) substrate locally.",
        "Pure Poisson; Class C.",
        reference="Grieder 2001 Cosmic Rays at Earth"),

    _ml("ml-mm1-queue-arrival", "M/M/1 queue inter-arrival times",
        "engineering", "C",
        "Memoryless arrival assumption is the defining hypothesis of M/M/1; no SO(2) substrate by construction.",
        "Class C by construction.",
        reference="Kleinrock 1975 Queueing Systems Vol I",
        notes="Definitional CV = 1; falsifies trivially if M/M/1 queue ever has CV ≠ 1."),

    _ml("ml-single-molecule-unbinding", "Single-molecule unbinding event times (rate-limited)",
        "cellular", "C",
        "In the rate-limited (Kramers) regime far from any oscillatory binding/unbinding feedback, the unbinding event has no SO(2) substrate.",
        "Pure Poisson point process; Class C.",
        reference="Bell 1978 Science 200:618; Schwesinger 2000 PNAS 97:9972",
        notes="Empirical CV ≈ 1 for force-free single-molecule unbinding in optical tweezers."),

    _ml("ml-mini-EPSC-NMJ", "Spontaneous miniature EPSC inter-event times at low-Ca²⁺ NMJ",
        "neural", "C",
        "Low-Ca²⁺ minis are independent vesicular fusion events with no presynaptic oscillation; no SO(2) substrate.",
        "Pure Poisson; Class C.",
        reference="Fatt & Katz 1952 J Physiol 117:109",
        notes="Classic test case — Fatt & Katz's original demonstration of Poisson minis."),

    _ml("ml-quantum-tunneling-escape", "Single-particle quantum-tunneling escape times",
        "quantum", "C",
        "Wavefunction in a metastable well tunnels stochastically; no oscillatory regulator below the barrier.",
        "Pure Poisson; Class C.",
        reference="Caldeira & Leggett 1981 Phys Rev Lett 46:211",
        notes="Tunneling out of a quasi-stable well — the canonical quantum memoryless process."),

    _ml("ml-thermal-bit-flip", "Thermal bit-flip times in a no-feedback magnetic memory cell",
        "engineering", "C",
        "Without write-back feedback the cell sits in either of two minima; thermal escape is Z₂ with no SO(2) regulator.",
        "Pure Poisson; Class C.",
        reference="Néel 1949 Ann Géophys 5:99",
        notes="Néel-Brown relaxation in single-domain magnets."),

    _ml("ml-bacterial-flagellar-motor-switch", "Flagellar motor CW/CCW switch times in absence of CheY signalling",
        "microbial", "C",
        "With CheY signalling deactivated the motor switches stochastically with no chemotactic SO(2) substrate.",
        "Pure Poisson; Class C.",
        reference="Korobkova 2004 Nature 428:574",
        notes="With chemotaxis intact, switching is Z₂-on-SO(2) and CV ≪ 1; ablation moves CV → 1."),

    _ml("ml-dna-tunneling-mismatch", "DNA spontaneous tautomerisation event times",
        "cellular", "C",
        "Quantum tunneling between Watson-Crick tautomers is spontaneous with no biochemical feedback substrate.",
        "Pure Poisson; Class C.",
        reference="Slocombe 2022 Commun Phys 5:109",
        notes="Highly speculative; included as edge-case test."),
]


def get_memoryless_rows() -> list[dict[str, Any]]:
    return [dict(r) for r in MEMORYLESS_ROWS]

"""Extension prediction tables (Z₂-on-SO(2) compositional + Lie-group beyond M22).

Pre-registered predictions: cv_pred is computed from canonical
constants; cv_obs is null until an empirical look-up has been
done by an independent process. verdict = "PENDING" by convention.
"""

from __future__ import annotations

from typing import Any, Optional

from .canonical import (
    PI,
    SQRT3,
    PHI_G,
    cv_canonical,
    omega_canonical,
    phi_g,
)


def _ext(
    rid: str, system: str, domain: str, sym: str, n: Optional[int], cls: str,
    physical: str, klsjust: str, reference: str = "",
    notes: str = "", provenance: str = "z2-on-so2-extension",
) -> dict[str, Any]:
    phi = phi_g(sym)
    return {
        "id": rid,
        "system": system,
        "domain": domain,
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
        "notes": notes,
        "provenance": provenance,
    }


# ====================================================================
# Z₂-on-SO(2) compositional extensions
# ====================================================================

Z2_ON_SO2_ROWS: list[dict[str, Any]] = [
    # P1 — two-channel ρ = -1/2 anti-correlation predictions
    # (the *prediction* is the correlation, not a CV; we record CV of
    # each channel as the carrier)
    _ext("z2so2-cardio-resp-channel-heart", "Cardio-respiratory coupled — heart Z₂ channel",
         "cardiac", "Z2", 2, "A",
         "On the shared cardio-respiratory SO(2) substrate the heart contributes a Z₂ rupture (systole/diastole).",
         "Autonomous in resting healthy adult; Class A.",
         reference="Heitmann 2020 Front Physiol 11:494",
         notes="Companion prediction: ρ(heart_rate, breath_rate) = -1/2 (M11)."),
    _ext("z2so2-cardio-resp-channel-resp", "Cardio-respiratory coupled — respiratory Z₂ channel",
         "respiratory", "Z2", 2, "A",
         "On the same shared SO(2) substrate the breath contributes the second Z₂ rupture.",
         "Autonomous in NREM / quiet rest; Class A.",
         reference="Heitmann 2020 Front Physiol 11:494",
         notes="Companion prediction: ρ(heart_rate, breath_rate) = -1/2 (M11)."),
    _ext("z2so2-eeg-theta-gamma-burst", "EEG theta-gamma — gamma Z₂ burst on theta SO(2)",
         "neural", "Z2", 2, "A",
         "Gamma burst on/off (Z₂) phase-locked to a continuous theta substrate (SO(2)).",
         "Autonomous network oscillator; Class A.",
         reference="Canolty 2010 Trends Cogn Sci 14:506",
         notes="Two simultaneous gamma channels on one theta cycle should anti-correlate at ρ = -1/2."),

    # P2 — nested CV: cycle vs sub-rupture
    _ext("z2so2-cardiac-pq-subinterval", "Cardiac PQ sub-interval CV (sub-rupture jitter on RR cycle)",
         "cardiac", "Z2", 2, "A",
         "PQ sub-interval is one Z₂ rupture (atrial-ventricular conduction) on the cardiac SO(2) limit cycle.",
         "Autonomous within healthy adult; Class A.",
         reference="Malik 2008 Heart Rhythm",
         notes="Predicted CV ≈ 0.1592 (Z₂ sub-rupture); compare to RR cycle CV ≈ 0.0796 (SO(2)) for ratio = 2."),
    _ext("z2so2-respiratory-inspiration-subcv", "Respiratory inspiration sub-interval CV (Z₂ on SO(2))",
         "respiratory", "Z2", 2, "A",
         "Inspiration is one Z₂ phase of the SO(2) breath limit cycle.",
         "Autonomous in NREM; Class A.",
         reference="Stone 2021 npj Digit Med",
         notes="Predicted CV ≈ 0.1592 vs full-breath CV ≈ 0.0796."),
    _ext("z2so2-neural-burst-intra-isi", "Intra-burst inter-spike interval CV (Z₂ jitter on burst SO(2))",
         "neural", "Z2", 2, "A",
         "Each spike within a burst is a Z₂ rupture on the burst's continuous depolarisation phase (SO(2)).",
         "Autonomous burst pacemaker; Class A.",
         reference="Krahe 2004 Nat Rev Neurosci 5:13",
         notes="Predicted intra-burst ISI CV ≈ 0.1592 vs burst-period CV ≈ 0.0796."),

    # P3 — k-channel ρ = -1/(k-1) anti-correlation
    _ext("z2so2-kaic-site-occupancy", "KaiC site-occupancy correlation (k=24 Z₂ on SO(2))",
         "circadian", "SO(2)", None, "B",
         "24 phosphorylation sites each acting as Z₂ events on a single SO(2) circadian cycle.",
         "Evolutionarily-tuned; Class B (cycle-period CV from KaiC was paper row 36, suppressed).",
         reference="Rust 2007 Science 318:809; Nakajima 2005 Science 308:414",
         notes="Predicted pairwise site-occupancy correlation ρ_ij = -1/23 ≈ -0.043."),
    _ext("z2so2-drosophila-syncytial-divs", "Drosophila syncytial division correlation (k=13 Z₂ on SO(2))",
         "developmental", "SO(2)", None, "A",
         "13 rapid nuclear divisions on a maternally-loaded SO(2) developmental clock.",
         "Autonomous; Class A.",
         reference="Foe 1983 J Cell Sci",
         notes="Predicted pairwise division-time correlation ρ_ij = -1/12 ≈ -0.083."),
    _ext("z2so2-theta-gamma-burst-correlation", "Theta-locked gamma burst correlation (k≈7 Z₂ on SO(2))",
         "neural", "SO(2)", None, "A",
         "6-8 gamma bursts per theta cycle on the hippocampal theta SO(2).",
         "Autonomous; Class A.",
         reference="Canolty 2010 Trends Cogn Sci 14:506",
         notes="Predicted pairwise gamma-burst correlation ρ_ij ≈ -1/6 ≈ -0.167."),

    # P4 — Z₂ rupture on larger Lie group: substrate sets CV
    _ext("z2so2-spin12-nmr-t2-jitter", "Spin-1/2 NMR T₂ jitter (Z₂ on SU(2))",
         "quantum", "SU(2)", None, "A",
         "T₂ relaxation is a Z₂ flip on the SU(2) Bloch-sphere substrate (φ_SU(2) = 2π).",
         "Autonomous in clean sample; Class A.",
         reference="Levitt 2008 Spin Dynamics; Slichter 1990 Principles of Magnetic Resonance",
         notes="Should be CV-indistinguishable from SO(2) systems (paper row 5 NREM respiration)."),
    _ext("z2so2-rigid-rotor-precession-flip", "Rigid-body precession reversal (Z₂ on SO(3))",
         "engineering", "SO(3)", None, "A",
         "Precession reversal is a Z₂ flip on the SO(3) rigid-body substrate (φ_SO(3) = π).",
         "Autonomous gyroscope; Class A.",
         reference="Goldstein 1980 Classical Mechanics §5; Fitzpatrick 2012 Newtonian Dynamics",
         notes="Should be CV-indistinguishable from Z₂-only systems (paper row 70 solar cycle)."),
    _ext("z2so2-bicommensurate-clock-cardiac-resp", "Cardio-respiratory bicommensurate clock (Z₂ on T²)",
         "cardiac", "T2", None, "A",
         "Cardiac and respiratory rotations on a 2-torus substrate; each generator carries one Z₂ rupture.",
         "Autonomous in NREM rest; Class A.",
         reference="Schäfer 1998 Nature 392:239",
         notes="Predicted per-generator CV = 1/(4π) ≈ 0.0796."),
    _ext("z2so2-cardiac-resp-circadian-t3", "Cardio-respiratory-circadian coupled clock (Z₂ on T³)",
         "cardiac", "T3", None, "B",
         "Three coupled rotational substrates (heart, breath, day) → T³ substrate.",
         "Circadian regulation tightens; Class B.",
         reference="Glass 2001 Nature 410:277",
         notes="Predicted per-generator CV = 1/(4π) ≈ 0.0796."),

    # P-anticorr — direct correlation predictions (the M11 prediction)
    _ext("z2so2-m11-anticorr-prediction", "M11: ρ = -1/2 between any two Z₂ ruptures sharing one SO(2) circuit",
         "neural", "SO(2)", None, "A",
         "Any two Z₂ rupture channels constrained to complete one shared SO(2) revolution must satisfy variance-preservation, forcing Cov = -1/8 → ρ = -1/2.",
         "Structural; class is irrelevant (correlation prediction, not CV).",
         reference="claims/M11_z2_compose_so2_anticorrelation/derivation.md",
         notes="The cv_pred field here is for reference (per-channel SO(2) cycle CV); the actual prediction is ρ = -1/2."),
]


# ====================================================================
# Lie-group extensions beyond M22
# ====================================================================

LIE_GROUP_ROWS: list[dict[str, Any]] = [
    # SU(2) — already in M22 but extended with concrete candidates
    _ext("lie-su2-nv-rabi", "NV-centre electron-spin Rabi cycle CV",
         "quantum", "SU(2)", None, "A",
         "Rabi cycle is rotation in SU(2) Bloch sphere; φ_SU(2) = 2π.",
         "Autonomous in clean sample; Class A.",
         reference="Doherty 2013 Phys Rep 528:1",
         notes="Should equal CV(SO(2)) = 0.0796 (M22-A topological equivalence).",
         provenance="lie-group-extension"),

    # SO(3) — already in M22, candidate test
    _ext("lie-so3-iers-lod-jitter", "Earth length-of-day jitter (SO(3) rigid-rotor return CV)",
         "astronomy", "SO(3)", None, "B",
         "Earth's rotation phase return time on the SO(3) substrate; φ_SO(3) = π.",
         "Tidally regulated; Class B.",
         reference="IERS Bulletin A; Gross 2000 Geophys J Int",
         notes="Should equal CV(Z₂) = 0.1592 if autonomous, but is suppressed by tidal regulation (Class B).",
         provenance="lie-group-extension"),

    # SO(4) — new
    _ext("lie-so4-hydrogen-orbital-degeneracy", "Hydrogen orbital degeneracy lifetime CV",
         "atomic", "SO(4)", None, "B",
         "Hydrogen has SO(4) accidental degeneracy (Pauli 1926); φ_SO(4) = π in canonical normalisation.",
         "QED-regulated; Class B.",
         reference="Pauli 1926 Z Phys 36:336; Dickson 1989",
         notes="Should equal CV(Z₂) = CV(SO(3)) = 0.1592 (topological prediction).",
         provenance="lie-group-extension"),

    # U(2) — new
    _ext("lie-u2-transmon-cavity", "Transmon + cavity coherence cycle CV",
         "quantum", "U(2)", None, "A",
         "Transmon qubit + cavity = SU(2)×U(1)/Z₂ = U(2); φ_U(2) = 2π.",
         "Autonomous in dilution refrigerator; Class A.",
         reference="Krantz 2019 Appl Phys Rev 6:021318",
         notes="Should equal CV(SO(2)) = CV(SU(2)) = 0.0796.",
         provenance="lie-group-extension"),

    # SU(3) — already in M22 v2
    _ext("lie-su3-charmonium-psi-family", "Charmonium ψ-family log-lifetime CV (SU(3))",
         "particle", "SU(3)", None, "A",
         "Charmonium states under SU(3) flavour; φ_SU(3) = 2π√3.",
         "Strong-interaction autonomous; Class A.",
         reference="PDG; M22 v2 result_v2.md",
         notes="Predicted 0.0459; M22 v2 reports 0.060 (within ±50% exploratory band).",
         provenance="lie-group-extension"),

    # SU(4) — new
    _ext("lie-su4-atomic-clock-4level", "4-level atomic clock transition CV",
         "atomic", "SU(4)", None, "B",
         "4-level system has SU(4) coherence substrate; φ_SU(4) = 4π.",
         "Engineered precision; Class B.",
         reference="Marciniak 2022 Nature 603:69",
         notes="Predicted CV = 0.0398 = CV(Sp(2)) (topological equivalence).",
         provenance="lie-group-extension"),

    # Sp(2) ≅ Spin(5) — new
    _ext("lie-sp2-pentaquark-lifetime", "Pentaquark Pc(4380)/Pc(4450) lifetime CV",
         "particle", "Sp(2)", None, "A",
         "Pentaquark spin substrate is Spin(5) ≅ Sp(2); φ_Sp(2) = 4π.",
         "Strong-interaction autonomous; Class A.",
         reference="LHCb 2015 Phys Rev Lett 115:072001",
         notes="Predicted CV = 0.0398 = CV(SU(4)) (topological equivalence).",
         provenance="lie-group-extension"),

    # G2 — exceptional, speculative
    _ext("lie-g2-colour-confinement-timescale", "G₂ colour-confinement timescale CV (speculative)",
         "particle", "G2", None, "A",
         "G₂ holonomy compactification or G₂-symmetric lattice gauge theory; φ_G2 normalisation here uses Killing-form (4π/3).",
         "Strong-interaction autonomous; Class A.",
         reference="Greiner & Schäfer 1994 QCD; lattice G₂ Yang-Mills literature",
         notes="Highly speculative; G₂ normalisation ambiguity gives CV in [0.069, 0.097].",
         provenance="lie-group-extension"),

    # Spin(7) — speculative
    _ext("lie-spin7-octonionic-quasicrystal", "Octonionic quasicrystal cycle CV (Spin(7))",
         "condensed-matter", "Spin(7)", None, "A",
         "Spin(7) holonomy quasicrystal substrate; φ_Spin(7) = 2π√3.",
         "Autonomous; Class A.",
         reference="Joyce 1996 Inv Math 123:507; quasicrystal literature",
         notes="Should equal CV(SU(3)) = 0.0459 (topological equivalence).",
         provenance="lie-group-extension"),

    # T² — already in M22, concrete candidate
    _ext("lie-t2-double-pendulum", "Double-pendulum period CV per generator (T²)",
         "engineering", "T2", None, "A",
         "Two coupled rotational degrees of freedom in the planar regular regime trace T² substrate; φ_T² = 2π per generator.",
         "Autonomous; Class A.",
         reference="Strogatz 2014 Nonlinear Dynamics §6",
         notes="Predicted per-generator CV = 0.0796 = CV(SO(2)).",
         provenance="lie-group-extension"),

    # T³ — new (cardio-resp-circadian)
    _ext("lie-t3-cardio-resp-circadian", "Cardio-respiratory-circadian coupled clock per generator (T³)",
         "circadian", "T3", None, "B",
         "Three commensurate rotational rhythms on T³; each generator has φ_T³ = 2π.",
         "Circadian regulation; Class B.",
         reference="Glass 2001 Nature 410:277",
         notes="Per-generator CV = 0.0796; circadian generator should suppress.",
         provenance="lie-group-extension"),

    # T⁴ — new (full ultradian stack)
    _ext("lie-t4-ultradian-stack", "Cardiac × respiratory × ultradian × circadian per generator (T⁴)",
         "circadian", "T4", None, "B",
         "Four commensurate rotational rhythms on T⁴; each generator has φ_T⁴ = 2π.",
         "Multiple regulatory layers; Class B per generator.",
         reference="Refinetti 2016 Circadian Physiology",
         notes="Per-generator CV = 0.0796.",
         provenance="lie-group-extension"),

    # Z₃ paper extrapolation (one row to record discrepancy)
    _ext("lie-z3-trefoil-repressilator-paper", "Repressilator-style Z₃ system (paper convention 1/(3π))",
         "synthetic-biology", "Z3", 3, "A",
         "Three discrete inhibitory phases on the circle; paper extrapolation uses CV = 1/(nπ).",
         "Autonomous in symmetric design; Class A.",
         reference="Elowitz 2000 Nature 403:335; M15 derivation.md",
         notes="DISCREPANCY: M15 derives CV = n/(4π) = 0.2387; paper uses 1/(nπ) = 0.1061. Repressilator empirical: 0.14-0.32.",
         provenance="lie-group-extension"),

    # PHI golden rotation — new
    _ext("lie-phi-quasicrystal-icosahedral", "Icosahedral / golden-ratio rotation cycle CV",
         "condensed-matter", "PHI", 4, "A",
         "Golden-ratio rotation φ = 1.618; φ_PHI = π·φ ≈ 5.083 in this package's convention.",
         "Autonomous in pure system; Class A.",
         reference="Penrose 1974; Levitov 1988",
         notes="Predicted CV = 1/(2·π·φ) ≈ 0.0984.",
         provenance="lie-group-extension"),
]


def get_z2_on_so2_rows() -> list[dict[str, Any]]:
    return [dict(r) for r in Z2_ON_SO2_ROWS]


def get_lie_group_rows() -> list[dict[str, Any]]:
    return [dict(r) for r in LIE_GROUP_ROWS]

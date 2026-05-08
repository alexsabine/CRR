"""
Generate a clean PDF of CRR canonical equations + axiomatic commitments.

Synthesises:
- F_Structure.pdf §1.1 axioms (6 axioms)
- CRR_FINAL_CANONICAL.md §1 three core equations
- notes/conventions.md C1–C5 conventions
- claims/M22_lie_group_cv_generalisation/ Lie-group CV
- notes/session_11_no_regulator_baseline.md no-regulator boundary
- notes/session_12_pre_registrations.md → result for Hawkes regime
- F_Structure.pdf α³ embedding cost
- notes/relabellings.md √2 precision-allocation ratio

Output: notes/CRR_canonical_equations.pdf
"""
from __future__ import annotations
import sys
sys.path.insert(0, '/root/.local/lib/python3.11/site-packages')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
import pathlib

OUT = pathlib.Path("/home/user/CRR/notes/CRR_canonical_equations.pdf")

# ============================================================
# Styles
# ============================================================
_styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=_styles["Title"], fontSize=20, leading=24,
    alignment=TA_CENTER, spaceAfter=14, fontName="Helvetica-Bold")
subtitle_style = ParagraphStyle(
    "Subtitle", parent=_styles["Normal"], fontSize=11, leading=14,
    alignment=TA_CENTER, textColor=colors.grey, spaceAfter=18)
h1_style = ParagraphStyle(
    "H1", parent=_styles["Heading1"], fontSize=15, leading=18,
    spaceBefore=14, spaceAfter=8, textColor=colors.HexColor("#1a3a6e"),
    fontName="Helvetica-Bold")
h2_style = ParagraphStyle(
    "H2", parent=_styles["Heading2"], fontSize=12, leading=15,
    spaceBefore=10, spaceAfter=5, fontName="Helvetica-Bold",
    textColor=colors.HexColor("#2a5598"))
body_style = ParagraphStyle(
    "Body", parent=_styles["BodyText"], fontSize=10, leading=14,
    alignment=TA_JUSTIFY, spaceAfter=5)
math_style = ParagraphStyle(
    "Math", parent=_styles["BodyText"], fontSize=11, leading=15,
    alignment=TA_CENTER, spaceBefore=4, spaceAfter=8,
    fontName="Helvetica", textColor=colors.HexColor("#202020"),
    leftIndent=20, rightIndent=20)
note_style = ParagraphStyle(
    "Note", parent=_styles["BodyText"], fontSize=9, leading=12,
    alignment=TA_LEFT, textColor=colors.HexColor("#555555"),
    leftIndent=15, spaceAfter=4)


# ============================================================
# Document content
# ============================================================
def P(text, style=body_style):
    return Paragraph(text, style)


def make_story():
    s = []

    # Title page
    s.append(Spacer(1, 4*cm))
    s.append(P("CRR — Canonical Equations<br/>and Axiomatic Commitments", title_style))
    s.append(P("Coherence&nbsp;–&nbsp;Rupture&nbsp;–&nbsp;Regeneration", subtitle_style))
    s.append(Spacer(1, 1.2*cm))
    s.append(P(
        "Synthesised post-campaign canonical reference. "
        "Equations and conventions consistent with "
        "<i>CRR_FINAL_CANONICAL.md</i>, "
        "<i>F_Structure.pdf</i> (Sabine 2025), and the corrections / "
        "extensions recorded across Sessions 1–15 of the "
        "campaign audit (<i>notes/conventions.md</i>, "
        "<i>notes/session_11_no_regulator_baseline.md</i>, "
        "<i>notes/session_12_pre_registrations.md</i>, "
        "<i>notes/session_14_literature_audit.md</i>).",
        note_style))
    s.append(Spacer(1, 0.5*cm))
    s.append(P(
        "Axiom numbering follows F_Structure.pdf §1.1. "
        "Convention dictionary (C1–C5) follows notes/conventions.md. "
        "Mathematical-claim numbering (M1–M22) follows "
        "notes/decomposition.md.", note_style))

    s.append(PageBreak())

    # ----- AXIOMS (F_Structure §1.1) -----
    s.append(P("1. The six axioms", h1_style))

    s.append(P(
        "The canonical CRR axiom set, as committed in F_Structure.pdf "
        "§1.1 and reproduced verbatim:", body_style))

    s.append(P("Axiom 1 — Temporal Primacy", h2_style))
    s.append(P(
        "Process is ontologically prior to substance. Every entity "
        "at every scale is constituted by a temporal cycle of "
        "accumulation, transition, and reconstruction.", body_style))

    s.append(P("Axiom 2 — Coherence Accumulation", h2_style))
    s.append(P(
        "Any bounded system accumulates coherence over time:", body_style))
    s.append(P(
        "<b>C(x, t) = ∫<sub>0</sub><sup>t</sup> L(x, τ) dτ</b>",
        math_style))
    s.append(P(
        "where L(x, τ) is the local coherence rate. Under the M13 "
        "identification, L is the Fisher-Rao squared infinitesimal "
        "speed on the system's statistical manifold, so C is "
        "accumulated Fisher information.", body_style))

    s.append(P("Axiom 3 — Instantaneous Rupture", h2_style))
    s.append(P(
        "The transition between regimes is a Dirac delta δ(now), "
        "scale-invariant: the same topology governs a synapse "
        "firing and a star collapsing.", body_style))

    s.append(P("Axiom 4 — Memory-Weighted Regeneration", h2_style))
    s.append(P(
        "After rupture, the system reconstructs via:", body_style))
    s.append(P(
        "<b>R[χ](x, t) = ∫<sub>−∞</sub><sup>t</sup> φ(x, τ) · "
        "exp(C(x, τ)/Ω) · Θ(t − τ) dτ</b>", math_style))
    s.append(P(
        "where high-coherence past states are exponentially amplified, "
        "and Θ is the Heaviside causal cut.", body_style))

    s.append(P("Axiom 5 — Universal Rupture Condition", h2_style))
    s.append(P(
        "Rupture occurs when the saturation condition holds:", body_style))
    s.append(P(
        "<b>C · Ω = 1</b>", math_style))
    s.append(P(
        "This is the Cramér-Rao bound saturated under the M13 "
        "identification: the system has extracted the maximum "
        "information available from its current configuration.",
        body_style))

    s.append(P("Axiom 6 — Symmetry Determines Ω", h2_style))
    s.append(P(
        "The system precision Ω is the inverse of the closed-geodesic "
        "length on the continual memory-bearing manifold:", body_style))
    s.append(P(
        "<b>Ω = 1 / φ<sub>G</sub></b>", math_style))
    s.append(P(
        "For Z<sub>2</sub> (rupture-only, π geodesic): <b>Ω = 1/π</b>. "
        "For SO(2) (continuous-phase circle, 2π geodesic): "
        "<b>Ω = 1/(2π)</b>.", body_style))

    s.append(PageBreak())

    # ----- CORE THREE EQUATIONS -----
    s.append(P("2. The three core equations", h1_style))

    s.append(P(
        "CRR is a temporal grammar with three canonical operations on "
        "the coherence trajectory of a bounded system:", body_style))

    s.append(P("2.1 Coherence (the past)", h2_style))
    s.append(P(
        "<b>C(x, t) = ∫<sub>0</sub><sup>t</sup> L(x, τ) dτ</b>", math_style))
    s.append(P(
        "with the canonical M13 identification: L(x, τ) = (dθ/dτ)<sup>T</sup> "
        "G(θ) (dθ/dτ), the Fisher-Rao squared speed on the statistical "
        "manifold parameterised by θ, with G the Fisher information matrix. "
        "Coherence is the squared arc-length action.", body_style))

    s.append(P("2.2 Rupture (the present)", h2_style))
    s.append(P(
        "<b>δ(now)   when   C · Ω = 1</b>", math_style))
    s.append(P(
        "Three independent arguments force this rupture event to be "
        "structurally Z<sub>2</sub> (binary, Bernoulli(½)):", body_style))
    s.append(P("• Dirac-delta form: δ has codomain {0, 1}.", body_style))
    s.append(P("• Heaviside-derivative form: cumulative-rupture-counting N(t) has integer increments.", body_style))
    s.append(P("• Cramér-Rao saturation: at C·Ω = 1 the natural sufficient statistic is binary.", body_style))

    s.append(P("2.3 Regeneration (the future)", h2_style))
    s.append(P(
        "<b>R[χ](x, t) = ∫<sub>−∞</sub><sup>t</sup> φ(x, τ) · "
        "exp(C(x, τ)/Ω) · Θ(t − τ) dτ</b>", math_style))
    s.append(P(
        "Three components: φ(x, τ) the resource field; exp(C/Ω) the "
        "coherence-weight (high-C past states amplified exponentially); "
        "Θ(t − τ) the Heaviside causal cut. M14 identifies exp(C/Ω) as "
        "the unique MaxEnt distribution under a mean-coherence "
        "constraint (Boltzmann-Gibbs, capped at T1*).", body_style))
    s.append(P(
        "M20 identifies R[χ] as the right Kan extension of the "
        "coherence-history functor along the rupture-inclusion functor.",
        body_style))

    s.append(P("2.4 The precision parameter Ω", h2_style))
    s.append(P(
        "<b>Ω = 1 / φ<sub>G</sub></b>", math_style))
    s.append(P(
        "where G is a compact connected Lie group acting as the "
        "continual memory-bearing manifold and φ<sub>G</sub> is its "
        "bi-invariant closed-geodesic length. Convention C4: Ω is "
        "<i>inverse</i> geodesic length — short geodesic ⇔ high precision. "
        "Convention C5: Ω = μ(A<sub>coherent</sub>) under Kac's lemma "
        "for ergodic systems.", body_style))

    s.append(PageBreak())

    # ----- KEY DERIVED IDENTITIES -----
    s.append(P("3. Key derived identities", h1_style))

    s.append(P("3.1 The CV = Ω/2 prediction (M1)", h2_style))
    s.append(P(
        "<b>CV = std(τ<sub>rupture</sub>) / E[τ<sub>rupture</sub>] = "
        "Ω / 2</b>", math_style))
    s.append(P(
        "Bernoulli(½) noise model at the rupture threshold gives "
        "std = ½ and mean = 1/Ω, so CV = Ω/2. Independent of the "
        "phase manifold G; the noise scale is intrinsic to Z<sub>2</sub> rupture.",
        body_style))

    s.append(P("3.2 Lie-group generalisation (M22)", h2_style))
    s.append(P(
        "<b>CV<sub>G</sub> = 1 / (2 · φ<sub>G</sub>)</b>", math_style))
    s.append(P(
        "Predicted CV across canonical compact connected Lie groups:",
        body_style))

    lie_cell = ParagraphStyle(
        "LieCell", parent=body_style, fontSize=9, leading=11,
        spaceAfter=0, alignment=TA_CENTER)
    lie_rows = [
        ["<b>G</b>", "<b>φ<sub>G</sub></b>", "<b>Ω<sub>G</sub></b>", "<b>CV<sub>G</sub></b>"],
        ["Z<sub>2</sub> (rupture only)", "π", "1/π", "1/(2π) ≈ 0.1592"],
        ["U(1) ≅ SO(2)", "2π", "1/(2π)", "1/(4π) ≈ 0.0796"],
        ["SU(2) ≅ S³", "2π", "1/(2π)", "1/(4π) ≈ 0.0796"],
        ["SO(3) = SU(2)/Z<sub>2</sub>", "π", "1/π", "1/(2π) ≈ 0.1592"],
        ["T² (per generator)", "2π", "1/(2π)", "1/(4π) ≈ 0.0796"],
        ["SU(3)", "2π√3", "1/(2π√3)", "1/(4π√3) ≈ 0.0459"],
    ]
    lie_table_data = [[Paragraph(c, lie_cell) for c in row] for row in lie_rows]
    lie_table = Table(lie_table_data,
        colWidths=[4*cm, 2*cm, 3*cm, 5*cm], hAlign="CENTER")
    lie_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e8eef7")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#aaaaaa")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    s.append(lie_table)
    s.append(Spacer(1, 0.4*cm))

    s.append(P("3.3 Cramér-Rao / Heisenberg-Gabor saturation (M3, M4, M5)", h2_style))
    s.append(P(
        "<b>Var(θ̂) ≥ 1/I(θ)   ⇔   Δt² · Δω² ≥ 1   ⇔   C · Ω ≥ 1</b>",
        math_style))
    s.append(P(
        "Three equivalent forms of the same uncertainty bound under "
        "(time ↔ frequency, parameter ↔ estimator) parameterisations. "
        "Saturation at C·Ω = 1 is the rupture condition.", body_style))

    s.append(P("3.4 The beauty function (M12)", h2_style))
    s.append(P(
        "<b>B(C) = exp(C/Ω) · (C* − C)</b>", math_style))
    s.append(P(
        "Peaks at <b>C* − Ω</b> by setting dB/dC = 0. "
        "Identifies the optimal coherence — the location of maximal "
        "agency / aesthetic tension — as just before the rupture "
        "threshold.", body_style))

    s.append(P("3.5 Anti-correlation under rupture composition (M11)", h2_style))
    s.append(P(
        "Two Z<sub>2</sub> rupture channels composing on a single SO(2) phase manifold "
        "produce anti-correlation:", body_style))
    s.append(P("<b>ρ = −1/2</b>", math_style))
    s.append(P(
        "Derived from variance-preservation Var(X+Y) = Var(X) when "
        "X, Y are equal-variance Z<sub>2</sub> ruptures composing on shared SO(2).",
        body_style))

    s.append(P("3.6 The α³ embedding cost (F_Structure §6.2)", h2_style))
    s.append(P(
        "For atomic-scale transitions, where the rupture event "
        "(spontaneous emission) couples through 3D EM vacuum:", body_style))
    s.append(P(
        "<b>CV<sub>atomic</sub> = α<sup>3</sup> / (4π · f)</b>",
        math_style))
    s.append(P(
        "with α the fine-structure constant and f a periodic-table-"
        "group-determined geometric factor. α³ is the cost of embedding "
        "an SO(2) coherence cycle in 3D EM space (one factor of α per "
        "spatial dimension).", body_style))
    s.append(P(
        "Empirically validated across 49 elements (88% within 20%, "
        "median error 5.4%) and the alkali series Li → Fr (P15, T3 promotion).",
        body_style))

    s.append(P("3.7 The √2 precision-allocation ratio", h2_style))
    s.append(P(
        "Optimal Kelly / log-utility precision allocation between two "
        "channels:", body_style))
    s.append(P(
        "<b>π<sub>p</sub> / π<sub>s</sub> = √2 ≈ 1.414</b>",
        math_style))
    s.append(P(
        "Under the precision = 1/variance identification, this is the "
        "same algebraic identity as the variance-summation √2 for "
        "two i.i.d. equal-variance channels — the two derivations "
        "coincide. Empirically observed in the SILSO sunspot / "
        "Hale-cycle CV ratio (1.382, 2.3% from √2; Session 9 audit).",
        body_style))

    s.append(PageBreak())

    # ----- THE CV LADDER (Sessions 11+12) -----
    s.append(P("4. The CV ladder — substrate identification", h1_style))

    s.append(P(
        "Empirical / mathematical tier structure for inter-rupture-CV "
        "identifications, formalised post-campaign:", body_style))

    cv_cell_left = ParagraphStyle(
        "CvCellLeft", parent=body_style, fontSize=8, leading=10,
        spaceAfter=0, alignment=TA_LEFT)
    cv_cell_ctr = ParagraphStyle(
        "CvCellCtr", parent=body_style, fontSize=8, leading=10,
        spaceAfter=0, alignment=TA_CENTER)
    cv_rows_raw = [
        ["<b>Tier</b>", "<b>CV</b>", "<b>Mechanism</b>", "<b>Empirical examples</b>"],
        ["Deterministic limit", "→ 0", "rich G, perfect sync", "atomic clocks"],
        ["SU(3) / higher", "0.0459", "richer compact group", "(speculative)"],
        ["SO(2) / SU(2) / T²", "0.0796", "continuous closed-geodesic", "solar Hale, GW BBH, intra-woman menstrual"],
        ["Class B regulated", "0.04 – 0.13", "autonomous + feedback control", "gait stride, hemispheric, Schwabe"],
        ["Z<sub>2</sub> / SO(3)", "0.1592", "discrete binary phase", "menstrual pooled, respiratory (Bull 2019)"],
        ["Mid-regime", "0.30 – 0.70", "partial regulation", "NBER recessions, Cascadia α, Vela glitches"],
        ["No regulator", "≈ 1.00", "no phase manifold (Poisson)", "cyber, Kp storms, UHECR, M-dwarf flares"],
        ["Self-exciting (Hawkes)", "> 1.30", "event-triggered intensity", "VIX spikes, SPX drawdowns (financial only)"],
    ]
    cv_table_data = [
        [Paragraph(row[0], cv_cell_left), Paragraph(row[1], cv_cell_ctr),
         Paragraph(row[2], cv_cell_left), Paragraph(row[3], cv_cell_left)]
        for row in cv_rows_raw
    ]
    cv_table = Table(cv_table_data,
        colWidths=[3.4*cm, 2.0*cm, 4.5*cm, 5.5*cm], hAlign="CENTER")
    cv_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e8eef7")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#aaaaaa")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("BACKGROUND", (0,7), (-1,7), colors.HexColor("#fff5e8")),
        ("BACKGROUND", (0,8), (-1,8), colors.HexColor("#fef0e0")),
    ]))
    s.append(cv_table)
    s.append(Spacer(1, 0.3*cm))
    s.append(P(
        "Critical structural points (per Session 14 literature audit):", body_style))
    s.append(P(
        "• <b>No-regulator boundary CV = 1</b> is the upper edge of "
        "the M22 framework (G = ∅, Ω → 0) and is the most empirically "
        "robust tier (5+ independent domains).", body_style))
    s.append(P(
        "• <b>The Hawkes (CV > 1) regime appears human-social-system-"
        "specific.</b> Pulsar glitches, volcanic eruptions, and M-dwarf "
        "flares all FAILED Hawkes pre-registrations and instead sit at "
        "no-regulator. Hawkes requires explicit positive-feedback dynamics.",
        body_style))
    s.append(P(
        "• <b>Mid-regime (0.3 – 0.7)</b> is the partially-regulated tier "
        "where neither autonomous Lie-group identification nor full "
        "no-regulator applies. Empirical examples cluster near √2/2 ≈ 0.71 "
        "(boundary of two-channel precision-allocation).", body_style))

    s.append(PageBreak())

    # ----- Convention dictionary -----
    s.append(P("5. Convention dictionary (notes/conventions.md)", h1_style))

    s.append(P("C1 — Rupture is Z<sub>2</sub> by construction", h2_style))
    s.append(P(
        "Forced by three independent structural arguments (Dirac-delta "
        "form, Heaviside-derivative form, Cramér-Rao saturation under "
        "M3). The 'Z<sub>2</sub>' label refers always to the rupture topology, not "
        "to a substrate alongside SO(2).", body_style))

    s.append(P("C2 — Phase manifold is a compact connected Lie group", h2_style))
    s.append(P(
        "G is the continual memory-bearing manifold with bi-invariant "
        "Riemannian metric and closed-geodesic length φ<sub>G</sub>. "
        "Canonical examples: U(1)≅SO(2), SU(2)≅S³, SO(3) = SU(2)/Z<sub>2</sub>, "
        "T<sup>n</sup>, SU(3).", body_style))

    s.append(P("C3 — Two distinct Ω's", h2_style))
    s.append(P(
        "<b>Ω<sub>geo</sub></b> = 1/φ<sub>G</sub> (geometric Ω of phase "
        "manifold). <b>Ω<sub>int</sub></b> = Z<sub>2</sub>-intrinsic precision in "
        "normalised Bernoulli units = 1 by construction. The brief's "
        "'exp(C/Ω) → e at C·Ω = 1' is correct in intrinsic units only. "
        "Default convention: Ω refers to Ω<sub>geo</sub>.", body_style))

    s.append(P("C4 — Ω is inverse geodesic length", h2_style))
    s.append(P(
        "Large Ω ⇔ short geodesic ⇔ high precision. On positively curved "
        "manifolds (Bonnet-Myers): <b>Ω ≥ √κ/π</b> with equality on the "
        "round sphere. Brief's earlier 'Ω = π/√κ' is an inversion typo "
        "(M16 corrected).", body_style))

    s.append(P("C5 — Ω is rate-like under Kac's lemma", h2_style))
    s.append(P(
        "For ergodic systems with coherent region A ⊂ X: "
        "<b>Ω = μ(A<sub>coherent</sub>)</b>, not 1/μ(A). Brief's earlier "
        "inverse reading is a typo (M19 corrected).", body_style))

    # ----- 22 mathematical claims (compact list) -----
    s.append(P("6. The 22 mathematical claims (M1 – M22)", h1_style))

    cell_style = ParagraphStyle(
        "CellStyle", parent=body_style, fontSize=8.5, leading=11,
        spaceAfter=0, alignment=TA_LEFT)
    cell_id_style = ParagraphStyle(
        "CellIdStyle", parent=body_style, fontSize=8.5, leading=11,
        spaceAfter=0, alignment=TA_CENTER, fontName="Helvetica-Bold")

    claims_raw = [
        ("M1",     "CV = Ω/2 with no free parameters"),
        ("M2",     "Z<sub>2</sub> : SO(2) CV ratio is exactly 2 from arc-to-ring topology"),
        ("M3",     "C·Ω = 1 saturates the Cramér-Rao bound"),
        ("M4",     "C·Ω = 1 saturates the Heisenberg-Gabor uncertainty"),
        ("M5*",    "M3 and M4 are the same theorem (relabelling cap T1*)"),
        ("M6",     "Fourier transform is the trivial CRR specialisation"),
        ("M7",     "φ is the dominant eigenvalue of the depth-two regeneration operator"),
        ("M8",     "Depth two is the minimum for KAM-stable ergodicity"),
        ("M9",     "φ-rotated CRR has singular-continuous (Sütő-class) spectrum"),
        ("M10",    "1/α = 137.0324 fixed point of CRR self-consistency equation"),
        ("M10-α³", "Subatomic CV scales as α<sup>3</sup> × (8/3π) at leading Bethe order (T3)"),
        ("M11",    "Z<sub>2</sub> + Z<sub>2</sub> → SO(2) composition gives ρ = −1/2"),
        ("M12",    "Beauty B(C) = exp(C/Ω)·(C* − C) peaks at C* − Ω"),
        ("M13",    "C is identified with accumulated Fisher information I(θ)"),
        ("M14*",   "exp(C/Ω) is the unique MaxEnt regeneration kernel (relabelling cap T1*)"),
        ("M15",    "Z<sub>n</sub> hierarchy: CV = n/(4π) for cyclic Z<sub>n</sub>"),
        ("M16",    "Bonnet-Myers gives Ω ≥ √κ/π on positively curved statistical manifolds"),
        ("M17",    "C is quadratic variation [μ,μ]<sub>t</sub> in martingale formulation"),
        ("M18",    "Rupture time τ<sub>Ω</sub> is an optimal stopping time (SPRT)"),
        ("M19",    "Poincaré + Kac make rupture inevitable for ergodic systems"),
        ("M20",    "R[χ] is the right Kan extension of coherence-history along rupture-inclusion"),
        ("M21",    "C·Ω = 1 saturates Cramér-Rao + Heisenberg-Gabor + TUR"),
        ("M22",    "CV<sub>G</sub> = 1/(2·φ<sub>G</sub>) for any compact connected Lie group G"),
    ]
    cl_table_data = [
        [Paragraph("<b>#</b>", cell_id_style),
         Paragraph("<b>Claim</b>", cell_style)]
    ]
    for cid, claim in claims_raw:
        cl_table_data.append([
            Paragraph(cid, cell_id_style),
            Paragraph(claim, cell_style),
        ])
    cl_table = Table(cl_table_data, colWidths=[2.2*cm, 12.8*cm], hAlign="CENTER")
    cl_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e8eef7")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("ALIGN", (1,0), (1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#aaaaaa")),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    s.append(cl_table)

    s.append(Spacer(1, 0.3*cm))
    s.append(P(
        "Tier-equivalent conventions: T0 = speculation; T1 = derivation "
        "consistent; T1* = canonical-result relabelling cap; T2 = empirical "
        "consistency; T3 = pre-registered prediction confirmed; T4 = "
        "independent unaffiliated replication. Campaign-current campaign "
        "T3 count: M10-α³, P15. T4 count: 0.", body_style))

    s.append(PageBreak())

    # ----- The Two-Ω disambiguation -----
    s.append(P("7. The two-Ω disambiguation (per C3)", h1_style))

    s.append(P(
        "Ω in CRR refers to two distinct quantities that should be "
        "disambiguated:", body_style))

    om_rows = [
        ["<b>Symbol</b>", "<b>Definition</b>", "<b>Domain</b>", "<b>Canonical value</b>"],
        ["Ω<sub>geo</sub>", "1 / φ<sub>G</sub> (inverse geodesic length)", "Geometry", "1/(2π) for SO(2)"],
        ["Ω<sub>int</sub>", "Z<sub>2</sub>-intrinsic Bernoulli-unit precision",
         "Z<sub>2</sub> rupture", "1 by normalisation"],
    ]
    om_table_data = [[Paragraph(c, lie_cell) for c in row] for row in om_rows]
    omega_table = Table(om_table_data,
        colWidths=[2.4*cm, 5.5*cm, 3.0*cm, 4.0*cm], hAlign="CENTER")
    omega_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e8eef7")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#aaaaaa")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    s.append(omega_table)
    s.append(Spacer(1, 0.3*cm))

    s.append(P(
        "In Z<sub>2</sub>-intrinsic units (Ω<sub>int</sub> = 1, C measured in "
        "Bernoulli draws), exp(C/Ω) = e at the rupture C·Ω = 1.<br/>"
        "In geometric units (Ω<sub>geo</sub> = 1/φ<sub>G</sub>), "
        "exp(C/Ω<sub>geo</sub>) = exp(φ<sub>G</sub><sup>2</sup>) at the "
        "rupture, much larger than e for canonical phase manifolds "
        "(e<sup>π²</sup> ≈ 19,334 for Z<sub>2</sub>; e<sup>4π²</sup> ≈ 1.4 × 10<sup>17</sup> "
        "for SO(2)).", body_style))

    s.append(P(
        "Convention adopted: unless otherwise noted, Ω in CRR formulas "
        "refers to Ω<sub>geo</sub>. The brief's 'exp → e at rupture' "
        "framing is correct only in intrinsic units.", body_style))

    # ----- Coda -----
    s.append(P("8. Coda — what CRR commits to, and what it does not", h1_style))

    s.append(P("CRR commits to:", h2_style))
    s.append(P(
        "• Process is ontologically prior to substance (Axiom 1).<br/>"
        "• Coherence accumulation is integration of Fisher-Rao squared "
        "speed (Axiom 2 + M13).<br/>"
        "• Rupture is a Z<sub>2</sub> Bernoulli event (C1) at the Cramér-Rao "
        "saturation bound (Axiom 5 + M3).<br/>"
        "• Regeneration is exponential weighting of past coherence (Axiom 4).<br/>"
        "• Precision Ω is the inverse geodesic length of a compact "
        "connected Lie-group memory manifold (Axiom 6 + C2 + C4).<br/>"
        "• CV scales as 1/(2 · φ<sub>G</sub>) per Lie group (M22).",
        body_style))

    s.append(P("CRR does NOT commit to:", h2_style))
    s.append(P(
        "• Predicting CV = 1/(4π) for systems without an identified "
        "SO(2) phase manifold. Externally-driven event timing defaults "
        "to no-regulator CV ≈ 1.<br/>"
        "• Predicting Hawkes CV > 1 universally. The self-exciting "
        "regime requires explicit positive-feedback dynamics; physical "
        "event timing typically relaxes to equilibrium.<br/>"
        "• Beating ETAS in California seismicity (P5 null). Single-Ω "
        "CRR matches; nested-CRR underperforms.<br/>"
        "• Numerical agreement at full CODATA precision for the fine-"
        "structure fixed point (1/α = 137.0324 vs CODATA 137.036, "
        "26 ppm discrepancy at T1).",
        body_style))

    s.append(Spacer(1, 0.4*cm))
    s.append(P(
        "Per CAMPAIGN.md PART III: this canonical document does not "
        "promote any claim's tier. It records the post-Session-15 state "
        "of CRR's axiomatic and equational commitments, with corrections "
        "(M16, M19, Class C → no-regulator) integrated, relabellings "
        "(M5, M14) capped at T1*, and the CV ladder formalised. "
        "Tier promotions remain governed by per-claim evidence files in "
        "<i>claims/</i>.", note_style))

    s.append(Spacer(1, 0.4*cm))
    s.append(P(
        "—— END OF CANONICAL REFERENCE ——", note_style))

    return s


def main():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="CRR Canonical Equations and Axiomatic Commitments",
        author="CRR Campaign Audit (post-Session 15)")
    story = make_story()
    doc.build(story)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

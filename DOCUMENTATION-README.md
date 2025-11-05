# CRR Comprehensive Documentation

This directory contains comprehensive documentation of the Coherence-Rupture-Regeneration (CRR) framework.

## Files

### Main Document
- **`crr-comprehensive-documentation.tex`**: Complete LaTeX document (~1500 lines) covering:
  - Mathematical framework with full operator definitions
  - Rigorous connection to Free Energy Principle (FEP)
  - Comprehensive documentation of all 56+ simulations
  - LLM methodology for emergent value exploration
  - Coarse-graining and universal active inference patterns
  - Discussion of applications, limitations, and future directions

### Supporting Diagrams
- **`crr-cycle-diagram.png`**: Visual representation of Coherence → Rupture → Regeneration cycle
- **`coherence-accumulation-graph.png`**: Time series showing coherence buildup and rupture events
- **`regeneration-visualization.png`**: Exponential weighting of historical states in regeneration
- **`fep-crr-connection.png`**: Mapping between Free Energy Principle and CRR operators
- **`scale-invariance-diagram.png`**: CRR operating across scales (quantum to cosmological)
- **`memory-signatures-diagram.png`**: Five dynamical regimes (fragile/resilient/oscillatory/chaotic/dialectical)

### Code
- **`generate_crr_diagrams.py`**: Python script to regenerate all diagrams

## Compiling the LaTeX Document

### Requirements
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required packages (all standard):
  - amsmath, amssymb, amsthm
  - graphicx, tikz
  - hyperref, cleveref
  - booktabs, subcaption

### Compilation
```bash
pdflatex crr-comprehensive-documentation.tex
pdflatex crr-comprehensive-documentation.tex  # Run twice for references
```

Or use your preferred LaTeX editor (TeXstudio, Overleaf, etc.)

### Output
Generates `crr-comprehensive-documentation.pdf` (~50-60 pages)

## Regenerating Diagrams

If you modify the diagram generation code:

```bash
python3 generate_crr_diagrams.py
```

Requires: `numpy` and `matplotlib`

```bash
pip install numpy matplotlib
```

## Document Structure

1. **Introduction** (Section 1)
   - Motivation and core insights
   - Problem of identity through change

2. **Mathematical Framework** (Section 2)
   - Canonical formulation
   - Operator definitions (C, δ, R)
   - Complete dynamics and parameter space

3. **Connection to Free Energy Principle** (Section 3)
   - Coherence as inverse free energy
   - Rupture as model switching
   - Regeneration as Bayesian model selection
   - Active inference and coarse-graining

4. **Comprehensive Simulation Documentation** (Section 4)
   - Biological systems (ocean waves, hurricanes, bees, ants, birds, fish, butterflies)
   - Physical systems (thermodynamics, black holes, atmospheres)
   - Cognitive systems (maze navigation, spatial exploration)
   - Emergent phenomena (self-organized criticality, iridescence)
   - Mathematical life and cultural systems

5. **LLM Methodology** (Section 5)
   - AI-assisted scientific discovery
   - Iterative dialectical refinement
   - Cross-domain pattern recognition
   - Hypothesis generation and validation
   - Ethical considerations

6. **Coarse-Graining and Active Inference** (Section 6)
   - CRR as universal coarse-grain framework
   - Scale invariance proofs
   - Universal patterns in adaptive systems
   - Connecting disparate natural systems
   - Predictive power demonstrations

7. **Discussion** (Section 7)
   - Theoretical contributions
   - Open questions (mathematical, empirical, philosophical)
   - Practical applications (AI safety, climate, ecosystems, ML)
   - Limitations and critiques
   - Future directions

## Key Contributions

1. **Rigorous Mathematical Formalization**: Complete operator definitions with thermodynamic consistency proof

2. **FEP Integration**: Establishes CRR as coarse-grain active inference framework

3. **Comprehensive Empirical Validation**: 56+ simulations across biology, physics, cognition

4. **Novel Methodology**: LLM-assisted exploration as scientific tool

5. **Universal Patterns**: Scale-invariant description of adaptive systems

## Citations

If you use this framework in your research:

```bibtex
@misc{sabine2025crr,
  author = {Sabine, Alexander},
  title = {Coherence-Rupture-Regeneration: A Unified Mathematical Framework
           for Identity Through Discontinuous Change},
  year = {2025},
  url = {https://alexsabine.github.io/CRR/},
  note = {Patent Pending, European Patent Office}
}
```

## Contact

**Alexander Sabine**
Independent Researcher
Website: [https://alexsabine.github.io/CRR/](https://alexsabine.github.io/CRR/)

## License

This documentation is available for academic research and education. Commercial applications require explicit licensing. See main README.md for details.

---

**Last Updated**: November 5, 2025
**Document Version**: 1.0
**LaTeX Lines**: 1,500+
**Simulations Documented**: 56+
**Diagrams**: 6

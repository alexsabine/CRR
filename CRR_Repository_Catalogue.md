# CRR Repository Catalogue

> **Status (October 2026):** This is a file inventory (v1.0, January 2026), kept for provenance; many listed files use superseded notation (C·Ω = 1, Ω = 1/2π for SO(2), exp(C/Ω) kernels, CV = Ω/2). Words such as "proof", "validation", "evidence" and "publication-ready" in the entries describe what the files set out to do, not their status; their claims were not upheld by later pre-registered testing. Current definitions: https://www.cohere.org.uk/crr-explained.html and the README (https://github.com/alexsabine/crr#readme).

## A Complete Guide to the Coherence-Rupture-Regeneration Framework

**Version 1.0 | January 2026**

**Website:** https://alexsabine.github.io/CRR/

---

## About This Catalogue

This document provides a complete inventory of all files in the CRR repository, organised for researchers, practitioners, and curious minds across disciplines. Each entry includes:

- **File**: Name and link
- **Description**: What the file contains
- **Key Content**: Core mathematical or conceptual elements
- **Audience**: Who would find this most valuable
- **2026 Relevance**: Why this matters now

---

## Repository Overview

| Metric | Value |
|--------|-------|
| Total Files | 141 |
| Markdown Proofs | 15 files (~8,500 lines) |
| PDF Treatises | 14 files (~2.7 GB) |
| HTML Simulations | 78 interactive demos |
| Python Scripts | 6 validation tools |
| Images & Diagrams | 28 files |

---

# Section 1: Core Documentation

## 1.1 Primary Framework Documents

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [README.md](https://alexsabine.github.io/CRR/) | Master introduction to CRR; complete framework overview with implementation guide | Core operators C(t)=∫L(τ)dτ, δ(t-t*), R[φ]=∫φ·exp(C/Ω)dτ; Ω=1/π parameter; Python implementation | Everyone; start here | Entry point for understanding temporal dynamics in AI, biology, psychology |
| [CRR_COMPREHENSIVE_SUMMARY.md](https://github.com/alexsabine/CRR/blob/main/CRR_COMPREHENSIVE_SUMMARY.md) | Complete synthesis addressing psychology, physics, AI alignment, and scientific status | All equations; 8 fundamental questions answered; empirical validation summary | Researchers seeking complete overview | Single-document comprehensive reference |

## 1.2 Mathematical Foundations

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr_meta_theorem.md](https://github.com/alexsabine/CRR/blob/main/crr_meta_theorem.md) | Unifying principle: all 24 proofs arise from "CRR is structure on bounded observation" | Categorical (Kan extension), Variational (Morse theory), Information-theoretic (MaxEnt) formulations | Mathematicians; theoretical physicists | Proves CRR is necessary, not arbitrary—critical for scientific acceptance |
| [crr_advanced_proof_sketches.md](https://github.com/alexsabine/CRR/blob/main/crr_advanced_proof_sketches.md) | 12 proofs from mathematical frontiers | Sheaf theory, HoTT, Floer homology, CFT, spin geometry, persistent homology, RMT, large deviations, non-equilibrium thermo, causal sets, operads, tropical geometry | Advanced mathematicians; theoretical physicists | Connects CRR to cutting-edge mathematics; enables cross-disciplinary research |
| [crr_first_principles_proofs.md](https://github.com/alexsabine/CRR/blob/main/crr_first_principles_proofs.md) | 12 independent derivations from distinct axiom systems | Category theory, information geometry, optimal transport, topology, RG theory, martingales, symplectic geometry, Kolmogorov complexity, gauge theory, ergodic theory, homological algebra, quantum mechanics | Mathematicians across specialties | Robust theoretical grounding; multiple entry points for different backgrounds |
| [crr_full_proofs.md](https://github.com/alexsabine/CRR/blob/main/crr_full_proofs.md) | Three complete rigorous proofs with all steps justified | Information geometry (Bonnet-Myers → Ω=π/√κ), Martingale theory (Wald's identity, Optional Stopping), Ergodic theory (Kac's lemma → Ω=1/μ(A), Poincaré recurrence) | Peer reviewers; formal verification researchers | Reference-quality proofs for academic publication |
| [CRR canonical proof sketch.md](https://github.com/alexsabine/CRR/blob/main/CRR%20canonical%20proof%20sketch.md) | Canonical proof of core CRR structure | Coherence accumulation axioms; rupture threshold derivation; regeneration operator construction | Mathematicians; implementers | Concise formal foundation for building on CRR |
| [canonical_crr_rigorous_proof_sketch.md](https://github.com/alexsabine/CRR/blob/main/canonical_crr_rigorous_proof_sketch.md) | Concise formal proof with explicit axioms | Core operator definitions; stated assumptions; key lemmas | Mathematicians needing quick reference | Fast verification of mathematical claims |
| [CRR_Complete_Proof_Sketch.md](https://github.com/alexsabine/CRR/blob/main/CRR_Complete_Proof_Sketch.md) | Comprehensive proof covering all foundations | Full derivation chain from axioms to applications | Graduate students; self-study | Complete self-contained learning resource |
| [multiscale_crr_proof_sketch.md](https://github.com/alexsabine/CRR/blob/main/multiscale_crr_proof_sketch.md) | Multi-scale CRR: "same process all the way down" | Scale coupling L^(n+1)=Σλ·R^(n)·δ(t-t_k); CV regularisation CV^(n+1)≈CV^(n)/√M; inevitable rupture theorem | AI architects; complexity scientists | Critical for hierarchical memory in AI; explains macro-regularity from micro-stochasticity |

## 1.3 FEP & Active Inference Integration

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [fep_crr_integration.md](https://github.com/alexsabine/CRR/blob/main/fep_crr_integration.md) | Complete synthesis of Free Energy Principle and CRR | C=F₀-F(t) duality; Π=(1/Ω)·exp(C/Ω) precision-rigidity; rupture as Bayesian model comparison; FEP-CRR Active Inference loop | Cognitive scientists; neuroscientists; AI researchers | Bridges Friston's framework with discontinuous transitions; essential for next-gen cognitive architectures |
| [crr_active_reasoning.md](https://github.com/alexsabine/CRR/blob/main/crr_active_reasoning.md) | CRR reformulation of Friston et al. (2025) active reasoning | Expected Coherence Gain replacing Expected Free Energy; explicit model switching; "aha moments" as rupture events | Computational cognitive scientists; AI researchers | Explains insight, learning phase transitions; basis for reasoning AI systems |

## 1.4 Empirical Validation

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr_16_nats_hypothesis.md](https://github.com/alexsabine/CRR/blob/main/crr_16_nats_hypothesis.md) | Testing universal information threshold at rupture | Ω≈16 nats≈23 bits prediction; 16 systems tested; mean 15.6 nats (p>0.4); working memory, consciousness, protein folding, T-cell activation, network cascades | Information theorists; neuroscientists; biologists | Universal capacity limit; implications for AI context windows, cognitive load, biological signalling thresholds |
| [crr_empirical_validation_test.md](https://github.com/alexsabine/CRR/blob/main/crr_empirical_validation_test.md) | Empirical test results across biological systems | R² values: wound healing 0.9989, muscle hypertrophy 0.9985, saltatory growth 11/11 predictions | Medical researchers; biologists | Evidence base for therapeutic applications |
| [CRR_Analysis_Report.md](https://github.com/alexsabine/CRR/blob/main/CRR_Analysis_Report.md) | Statistical analysis of prediction accuracy | Detailed metrics across validation domains | Statisticians; peer reviewers | Quality assessment documentation |

---

# Section 2: Formal Treatises (PDF)

## 2.1 Comprehensive Theory

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr_unified_theory.pdf](https://github.com/alexsabine/CRR/blob/main/crr_unified_theory.pdf) | Unified mathematical theory | Complete formal treatment of all operators and relationships | Theorists; archivists | Comprehensive reference for theoretical development |
| [crr_comprehensive_treatise.pdf](https://github.com/alexsabine/CRR/blob/main/crr_comprehensive_treatise.pdf) | Full academic treatment | Extended derivations with mathematical rigour | Academic publishers; reviewers | Publication-ready theoretical treatment |
| [crr_complete_unified.pdf](https://github.com/alexsabine/CRR/blob/main/crr_complete_unified.pdf) | Complete unified formulation | Synthesis of all proof approaches | Graduate students; researchers | Single-document complete theory |

## 2.2 Specialised Proofs

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr_full_proofs.pdf](https://github.com/alexsabine/CRR/blob/main/crr_full_proofs.pdf) | Rigorous formal proofs (PDF) | Information geometry, martingale, ergodic theory proofs | Mathematicians; archivists | Archival-quality formal mathematics |
| [crr_martingale_derivation.pdf](https://github.com/alexsabine/CRR/blob/main/crr_martingale_derivation.pdf) | Martingale theory derivation | Quadratic variation; stopping times; Optional Stopping Theorem | Stochastic process researchers; quants | Financial/risk applications; algorithmic trading |
| [crr_solomonoff_analysis.pdf](https://github.com/alexsabine/CRR/blob/main/crr_solomonoff_analysis.pdf) | Solomonoff induction integration | Kolmogorov complexity; algorithmic probability; MDL | AI theorists; compression researchers | Theoretical foundations for learning algorithms |
| [crr_coherence-FE.pdf](https://github.com/alexsabine/CRR/blob/main/crr_coherence-FE.pdf) | Coherence-Free Energy analysis | C=F₀-F(t) derivation; implications for precision | FEP researchers; neuroscientists | Core theoretical bridge document |

## 2.3 Validation & Reference

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr_validation_report.pdf](https://github.com/alexsabine/CRR/blob/main/crr_validation_report.pdf) | Comprehensive validation report | Statistical analysis across systems | Peer reviewers; sceptics | Evidence quality documentation |
| [crr_validation_report_extended.pdf](https://github.com/alexsabine/CRR/blob/main/crr_validation_report_extended.pdf) | Extended validation | Additional systems tested | Researchers seeking breadth | Broader evidence base |
| [fep_crr_cheatsheet.pdf](https://github.com/alexsabine/CRR/blob/main/fep_crr_cheatsheet.pdf) | Quick reference card | Key equations; correspondences | Practitioners; implementers | Practical implementation guide |
| [fep_crr_driving_analysis.pdf](https://github.com/alexsabine/CRR/blob/main/fep_crr_driving_analysis.pdf) | Driving dynamics analysis | Active inference with CRR transitions | Roboticists; autonomous systems engineers | Vehicle/robot control applications |

## 2.4 Extended Topics

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [aha.pdf](https://github.com/alexsabine/CRR/blob/main/aha.pdf) | Insight/"aha moments" as rupture | Phenomenology of insight; cognitive rupture mechanics | Creativity researchers; therapists; educators | Understanding breakthroughs; therapeutic applications |
| [Inner_screen(Fields).pdf](https://github.com/alexsabine/CRR/blob/main/Inner_screen(Fields).pdf) | Field theory of inner experience | Field-theoretic consciousness formulation | Consciousness researchers; phenomenologists | Formalising subjective experience |
| [elements_CRR_frequency_Omega.pdf](https://github.com/alexsabine/CRR/blob/main/elements_CRR_frequency_Omega.pdf) | Frequency-domain Ω analysis | Oscillatory dynamics; frequency-dependent rupture | Signal processing researchers; neuroscientists | Neural oscillation research; EEG analysis |

## 2.5 Diagrams (PDF)

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [diagrams/bifurcation_standalone.pdf](https://github.com/alexsabine/CRR/blob/main/diagrams/bifurcation_standalone.pdf) | Bifurcation diagrams | Phase space C→Ω transitions | Dynamical systems researchers | Understanding stability and tipping points |
| [diagrams/crr_cycle_standalone.pdf](https://github.com/alexsabine/CRR/blob/main/diagrams/crr_cycle_standalone.pdf) | CRR cycle diagram | C→δ→R cycle visualisation | Educators; communicators | Teaching and presentation tool |
| [diagrams/unified_model_standalone.pdf](https://github.com/alexsabine/CRR/blob/main/diagrams/unified_model_standalone.pdf) | Unified model diagram | Complete system architecture | System architects | Overview for complex implementations |

---

# Section 3: Interactive Simulations (HTML)

## 3.1 Core Demonstrations

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [index.html](https://alexsabine.github.io/CRR/index.html) | Main navigation hub | Links to all simulations | Everyone | Entry point for exploration |
| [crr-explained.html](https://alexsabine.github.io/CRR/crr-explained.html) | Educational walkthrough | Step-by-step concept introduction | Beginners; educators | Onboarding tool; classroom use |
| [crr-simulations.html](https://alexsabine.github.io/CRR/crr-simulations.html) | Simulation directory | Catalogue of all demos | Explorers | Navigation aid |
| [guide.html](https://alexsabine.github.io/CRR/guide.html) | User guide | Usage instructions | New users | Practical orientation |
| [about.html](https://alexsabine.github.io/CRR/about.html) | Project overview | Background; motivation | Curious visitors | Context and framing |
| [crr_equation_visual.html](https://alexsabine.github.io/CRR/crr_equation_visual.html) | Equation visualiser | Dynamic equation display | Visual learners | Understanding operator relationships |
| [crr-three-phase-visualiser.html](https://alexsabine.github.io/CRR/crr-three-phase-visualiser.html) | Three-phase animation | C→δ→R cycle dynamics | Intuitive learners | Grasping core cycle |
| [dirac-delta-crr.html](https://alexsabine.github.io/CRR/dirac-delta-crr.html) | Rupture visualisation | δ(t-t*) instantaneous transition | Mathematicians; physicists | Understanding discontinuity |
| [crr-benchmarks.html](https://alexsabine.github.io/CRR/crr-benchmarks.html) | Performance benchmarks | Metrics across systems | Validators | Testing framework claims |
| [Maths.html](https://alexsabine.github.io/CRR/Maths.html) | Mathematics animation | Core equation animations | Visual mathematical learners | Educational mathematics |
| [maths_q.html](https://alexsabine.github.io/CRR/maths_q.html) | Extended mathematics | Advanced concepts | Advanced learners | Deeper understanding |
| [crr_time.html](https://alexsabine.github.io/CRR/crr_time.html) | Time and precision | Temporal structure; possibility space | Philosophers; physicists | Understanding CRR's temporal grammar |

## 3.2 FEP & Active Inference

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [fep-crr-finale-wspeech.html](https://alexsabine.github.io/CRR/fep-crr-finale-wspeech.html) | Complete FEP-CRR demo with narration | 5 developmental stages; full synthesis | Cognitive scientists; AI researchers | Comprehensive FEP-CRR understanding |
| [fep-crr-5stages.html](https://alexsabine.github.io/CRR/fep-crr-5stages.html) | Five-stage process | Stage-by-stage learning dynamics | Developmental psychologists | AI training phase design |
| [fep-crr-game.html](https://alexsabine.github.io/CRR/fep-crr-game.html) | Interactive game | Gamified prediction-error learning | General public; students | Engaging public education |
| [fep-agent-shapes.html](https://alexsabine.github.io/CRR/fep-agent-shapes.html) | Shape-learning agent | Active inference with visual prediction | AI/robotics researchers | Learning algorithm demonstration |
| [fep_crr_dynamics.html](https://alexsabine.github.io/CRR/fep_crr_dynamics.html) | Dynamic integration | Real-time coherence-FE relationship | Researchers | Precision-rigidity dynamics |
| [perceiving-agent.html](https://alexsabine.github.io/CRR/perceiving-agent.html) | Perceptual agent | Active inference in perception | Cognitive scientists | Perceptual decision-making models |

## 3.3 Biological Systems — Animals

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [fish.html](https://alexsabine.github.io/CRR/fish.html) | Fish predator-prey | Survival behaviour coherence | Ecologists; behaviourists | Behavioural prediction models |
| [crr-fish-learning.html](https://alexsabine.github.io/CRR/crr-fish-learning.html) | Fish learning curves | Learning as coherence accumulation | Education researchers | Skill acquisition modelling |
| [fish_irridescence.html](https://alexsabine.github.io/CRR/fish_irridescence.html) | Fish iridescence | Structural colour dynamics | Materials scientists | Bio-inspired photonics |
| [birds.html](https://alexsabine.github.io/CRR/birds.html) | Bird flocking | Swarm coherence; flock rupture | Collective intelligence researchers | Coordination algorithms |
| [bees.html](https://alexsabine.github.io/CRR/bees.html) | Bee swarms | Distributed coherence | Swarm robotics engineers | Consensus algorithms |
| [bee_vision.html](https://alexsabine.github.io/CRR/bee_vision.html) | Bee vision | Insect visual coherence | Bio-inspired vision researchers | Computer vision applications |
| [dolphin_crr_optimized.html](https://alexsabine.github.io/CRR/dolphin_crr_optimized.html) | Dolphin echolocation | Sonar coherence-building | Underwater robotics engineers | Sonar system design |
| [bats.html](https://alexsabine.github.io/CRR/bats.html) | Bat navigation | Echolocation; flight rupture | Navigation AI researchers | SLAM systems |
| [butterfly.html](https://alexsabine.github.io/CRR/butterfly.html) | Metamorphosis | Larva→pupa→adult ruptures | Developmental biologists | Transformational change models |
| [drosophila_anatomical_crr (2).html](https://alexsabine.github.io/CRR/drosophila_anatomical_crr%20(2).html) | Fruit fly development | Morphogen gradient coherence | Developmental geneticists | Body planning algorithms |
| [fixed_ant_colony.html](https://alexsabine.github.io/CRR/fixed_ant_colony.html) | Ant colonies | Pheromone trail coherence | Optimisation researchers | ACO algorithm improvements |

## 3.4 Biological Systems — Plants & Fungi

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr-forest-seasonal.html](https://alexsabine.github.io/CRR/crr-forest-seasonal.html) | Forest seasons | Annual cycles; seasonal rupture | Ecologists; climate scientists | Climate adaptation modelling |
| [tree_ring.html](https://alexsabine.github.io/CRR/tree_ring.html) | Tree rings | Dendrochronology as CRR | Paleoclimatologists | Historical climate reconstruction |
| [mycelium.html](https://alexsabine.github.io/CRR/mycelium.html) | Fungal networks | Network coherence | Network scientists | Distributed computing design |
| [lichen.html](https://alexsabine.github.io/CRR/lichen.html) | Lichen growth | Multi-organism coherence | Symbiosis researchers | Partnership dynamics |
| [moss.html](https://alexsabine.github.io/CRR/moss.html) | Moss colonisation | Slow coherence | Succession ecologists | Long-term system dynamics |
| [moss_a.html](https://alexsabine.github.io/CRR/moss_a.html) | Moss variant | Alternative patterns | Comparative ecologists | Variant dynamics study |

## 3.5 Biological Systems — Human Body

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr-body-accurate.html](https://alexsabine.github.io/CRR/crr-body-accurate.html) | Anatomical CRR | Organ-level coherence | Medical researchers | Health monitoring systems |
| [crr-body-scientific.html](https://alexsabine.github.io/CRR/crr-body-scientific.html) | Scientific body model | Physiological coherence mapping | Medical educators | Systems medicine education |
| [crr-brain-photorealistic.html](https://alexsabine.github.io/CRR/crr-brain-photorealistic.html) | Brain visualisation | Neural coherence | Neuroscientists | Consciousness research |
| [child_dev.html](https://alexsabine.github.io/CRR/child_dev.html) | Child development | Piagetian stages as rupture | Developmental psychologists | Educational intervention design |
| [inner_screen.html](https://alexsabine.github.io/CRR/inner_screen.html) | Inner experience | Phenomenological coherence | Consciousness researchers | Meditation/contemplative research |

## 3.6 Ecological & Environmental

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [ecosystem.html](https://alexsabine.github.io/CRR/ecosystem.html) | Ecosystem dynamics | Cascade ruptures | Conservation biologists | Biodiversity management |
| [biological-systems.html](https://alexsabine.github.io/CRR/biological-systems.html) | Biology overview | General biological CRR | Life scientists | Cross-domain integration |
| [marine.html](https://alexsabine.github.io/CRR/marine.html) | Ocean ecosystems | Marine coherence | Marine biologists | Fisheries management |
| [marine2.html](https://alexsabine.github.io/CRR/marine2.html) | Extended marine | Deeper dynamics | Oceanographers | Marine research |
| [marine_enhanced(FPS_slow).html](https://alexsabine.github.io/CRR/marine_enhanced(FPS_slow).html) | Detailed marine | High-detail creatures | Educators | Educational visualisation |
| [atmosphere.html](https://alexsabine.github.io/CRR/atmosphere.html) | Atmospheric circulation | Weather coherence | Climate scientists | Weather prediction |
| [hurricane.html](https://alexsabine.github.io/CRR/hurricane.html) | Hurricane dynamics | Storm intensification | Meteorologists | Disaster preparedness |
| [weather.html](https://alexsabine.github.io/CRR/weather.html) | Weather patterns | Meteorological coherence | General public | Climate understanding |
| [abiogenesis.html](https://alexsabine.github.io/CRR/abiogenesis.html) | Origin of life | Prebiotic→life rupture | Astrobiologists | Origin of life research |

## 3.7 Physical Systems — Cosmological

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [black_hole.html](https://alexsabine.github.io/CRR/black_hole.html) | Black hole dynamics | Horizon coherence; Hawking rupture | Theoretical physicists | Information paradox |
| [black_hole_enhanced.html](https://alexsabine.github.io/CRR/black_hole_enhanced.html) | Enhanced black hole | Detailed horizon dynamics | Cosmologists | Advanced cosmology |
| [blackhole_a.html](https://alexsabine.github.io/CRR/blackhole_a.html) | Black hole variant | Alternative visualisation | Physics educators | Comparative teaching |
| [crr_bh_grounded.html](https://alexsabine.github.io/CRR/crr_bh_grounded.html) | Grounded BH physics | Rigorous BH-CRR connection | Peer reviewers | Publication-ready physics |
| [sun.html](https://alexsabine.github.io/CRR/sun.html) | Solar dynamics | Solar coherence; flare rupture | Heliophysicists | Space weather prediction |
| [sun2.html](https://alexsabine.github.io/CRR/sun2.html) | Extended solar | Solar cycle dynamics | Solar physicists | Solar cycle research |
| [darkenergy.html](https://alexsabine.github.io/CRR/darkenergy.html) | Dark energy | Cosmic coherence | Cosmologists | Fundamental cosmology |
| [crr_holographic_final.html](https://alexsabine.github.io/CRR/crr_holographic_final.html) | Holographic principle | Bulk-boundary coherence | String theorists | AdS/CFT applications |

## 3.8 Physical Systems — Materials & Chemistry

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [atom_advanced.html](https://alexsabine.github.io/CRR/atom_advanced.html) | Atomic structure | Quantum coherence; orbital transitions | Quantum physicists | Quantum computing |
| [crr_periodic_table.html](https://alexsabine.github.io/CRR/crr_periodic_table.html) | Periodic table | Elements as coherence structures | Chemistry educators | Chemistry education |
| [ice.html](https://alexsabine.github.io/CRR/ice.html) | Ice crystals | Nucleation rupture | Materials scientists | Cryogenics |
| [crr-snowflakes.html](https://alexsabine.github.io/CRR/crr-snowflakes.html) | Snowflake formation | Dendritic growth | Crystal growth researchers | Self-organisation |
| [crr-bubble-simulation__2_.html](https://alexsabine.github.io/CRR/crr-bubble-simulation__2_.html) | Bubble dynamics | Membrane coherence | Soft matter physicists | Fluid dynamics |
| [crr_water_realistic.html](https://alexsabine.github.io/CRR/crr_water_realistic.html) | Realistic water | Phase transition coherence | Fluid dynamicists | Fluid physics |
| [CRR_Water.html](https://alexsabine.github.io/CRR/CRR_Water.html) | Water art | Artistic fluid patterns | Artists; public | Art-science integration |
| [kettle.html](https://alexsabine.github.io/CRR/kettle.html) | Boiling water | Liquid→gas rupture | Physics educators | Everyday physics teaching |
| [Zippo.html](https://alexsabine.github.io/CRR/Zippo.html) | Lighter combustion | Ignition rupture | Combustion scientists | Fire safety |
| [crr_mother_of_pearl.html](https://alexsabine.github.io/CRR/crr_mother_of_pearl.html) | Nacre structure | Layered coherence | Biomaterials researchers | Bio-inspired materials |
| [golden_beetle_crr.html](https://alexsabine.github.io/CRR/golden_beetle_crr.html) | Beetle iridescence | Structural colour | Photonics engineers | Bio-inspired optics |

## 3.9 Physical Systems — Thermodynamics

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr-thermo-rupture-rate.html](https://alexsabine.github.io/CRR/crr-thermo-rupture-rate.html) | Thermodynamic rates | Arrhenius-like rupture kinetics | Chemical engineers | Reaction rate prediction |
| [entropic-crr.html](https://alexsabine.github.io/CRR/entropic-crr.html) | Entropy dynamics | ΔS at rupture | Thermodynamicists | Understanding irreversibility |
| [crr_temperature_clean.html](https://alexsabine.github.io/CRR/crr_temperature_clean.html) | Temperature effects | Ω modulation by temperature | Climate scientists | Thermal management |
| [crr_sandpile_sim__2_.html](https://alexsabine.github.io/CRR/crr_sandpile_sim__2_.html) | Sandpile SOC | Power-law rupture; criticality | Complexity scientists | Earthquake/cascade prediction |

## 3.10 Cognitive & Psychological

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [room.html](https://alexsabine.github.io/CRR/room.html) | Spatial navigation | Room-switch rupture | Spatial cognition researchers | Navigation AI |
| [Maze.html](https://alexsabine.github.io/CRR/Maze.html) | Maze solving | Dead-end rupture | Planning AI researchers | Problem-solving algorithms |
| [soduku.html](https://alexsabine.github.io/CRR/soduku.html) | Sudoku solving | Contradiction rupture | Constraint satisfaction researchers | Logical reasoning AI |
| [nostalgia_trap.html](https://alexsabine.github.io/CRR/nostalgia_trap.html) | Nostalgia dynamics | Low-Ω regeneration traps | Therapists; psychologists | Mental health interventions |
| [crr-shepard-canonical (1).html](https://alexsabine.github.io/CRR/crr-shepard-canonical%20(1).html) | Shepard tone illusion | Coherence without rupture | Perception researchers | Illusion/perception science |
| [peanut.html](https://alexsabine.github.io/CRR/peanut.html) | Pattern exploration | Novel pattern recognition | Cognitive scientists | Cognitive flexibility |

## 3.11 Collective Intelligence

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [ucf_swarm_crr.html](https://alexsabine.github.io/CRR/ucf_swarm_crr.html) | UCF swarm research | Collective rupture | Swarm robotics researchers | Drone coordination |
| [mathematical-life.html](https://alexsabine.github.io/CRR/mathematical-life.html) | Mathematical life | Conway-style patterns | A-life researchers | Emergence studies |

## 3.12 Art & Special

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [CRR_Art.html](https://alexsabine.github.io/CRR/CRR_Art.html) | CRR art | Aesthetic coherence | Artists; public | Science communication |
| [Christmas_Greetings.html](https://alexsabine.github.io/CRR/Christmas_Greetings.html) | Holiday greeting | Seasonal coherence | Community | Community building |

---

# Section 4: Computational Validation (Python)

| File | Description | Key Content | Audience | 2026 Relevance |
|------|-------------|-------------|----------|----------------|
| [crr_simulation.py](https://github.com/alexsabine/CRR/blob/main/crr_simulation.py) | Core implementation | C, δ, R operators in Python; FEP integration | AI/ML engineers | Reference implementation for integration |
| [crr_martingale_verification.py](https://github.com/alexsabine/CRR/blob/main/crr_martingale_verification.py) | Martingale verification | Quadratic variation; stopping time tests | Stochastic modellers | Mathematical validation |
| [crr_validation.py](https://github.com/alexsabine/CRR/blob/main/crr_validation.py) | General validation | Cross-system testing | QA engineers | Quality assurance |
| [crr_wound_analysis.py](https://github.com/alexsabine/CRR/blob/main/crr_wound_analysis.py) | Wound healing analysis | 80% ceiling; fetal vs adult Ω | Medical researchers | Regenerative medicine |
| [crr_muscle_predictions.py](https://github.com/alexsabine/CRR/blob/main/crr_muscle_predictions.py) | Muscle predictions | R²=0.9985 growth curves | Sports scientists | Training optimisation |
| [crr_muscle_validation.py](https://github.com/alexsabine/CRR/blob/main/crr_muscle_validation.py) | Muscle validation | Prospective testing | Researchers | Evidence quality |

---

# Section 5: Diagrams & Images

## 5.1 Core Diagrams

| File | Description | Audience | 2026 Relevance |
|------|-------------|----------|----------------|
| [diagrams/bifurcation-1.png](https://github.com/alexsabine/CRR/blob/main/diagrams/bifurcation-1.png) | Bifurcation (PNG) | Presenters | Quick reference slides |
| [diagrams/crr_cycle-1.png](https://github.com/alexsabine/CRR/blob/main/diagrams/crr_cycle-1.png) | CRR cycle (PNG) | Educators | Teaching materials |
| [diagrams/unified_model-1.png](https://github.com/alexsabine/CRR/blob/main/diagrams/unified_model-1.png) | Unified model (PNG) | Architects | System overview |
| [diagrams/fep_crr_page-01.png](https://github.com/alexsabine/CRR/blob/main/diagrams/fep_crr_page-01.png) — [page-13.png](https://github.com/alexsabine/CRR/blob/main/diagrams/fep_crr_page-13.png) | FEP-CRR slides (13 pages) | FEP community | Conference presentations |

## 5.2 Concept Visualisations

| File | Description | Audience | 2026 Relevance |
|------|-------------|----------|----------------|
| [coherence_accumulation.png](https://github.com/alexsabine/CRR/blob/main/coherence_accumulation.png) | C(t) curve | Visual learners | Core concept |
| [precision_coherence.png](https://github.com/alexsabine/CRR/blob/main/precision_coherence.png) | Π-C relationship | FEP researchers | Bridge visualisation |
| [fep_crr_correspondence.png](https://github.com/alexsabine/CRR/blob/main/fep_crr_correspondence.png) | Equation mapping | Implementers | Quick reference |
| [master_equation.png](https://github.com/alexsabine/CRR/blob/main/master_equation.png) | Master equation | Everyone | Core equation |
| [memory_kernel.png](https://github.com/alexsabine/CRR/blob/main/memory_kernel.png) | exp(C/Ω) kernel | ML researchers | Regeneration visualisation |
| [exploration_exploitation.png](https://github.com/alexsabine/CRR/blob/main/exploration_exploitation.png) | E/E trade-off | RL researchers | Decision-making |
| [proof_sketches_overview.png](https://github.com/alexsabine/CRR/blob/main/proof_sketches_overview.png) | 24 proofs overview | Theorists | Cross-domain map |
| [q_omega_correlation.png](https://github.com/alexsabine/CRR/blob/main/q_omega_correlation.png) | Q-Ω correlation | Statisticians | Parameter analysis |
| [multi.png](https://github.com/alexsabine/CRR/blob/main/multi.png) | Multi-scale diagram | System architects | Scale coupling |

## 5.3 Validation Plots

| File | Description | Audience | 2026 Relevance |
|------|-------------|----------|----------------|
| [crr_muscle_validation_plot.png](https://github.com/alexsabine/CRR/blob/main/crr_muscle_validation_plot.png) | Muscle validation | Medical researchers | Biological evidence |
| [crr_wound_validation_plot.png](https://github.com/alexsabine/CRR/blob/main/crr_wound_validation_plot.png) | Wound validation | Medical researchers | Medical evidence |
| [crr_wound_validation_results.txt](https://github.com/alexsabine/CRR/blob/main/crr_wound_validation_results.txt) | Numerical results | Statisticians | Detailed data |

## 5.4 Illustrative Images

| File | Description | Audience | 2026 Relevance |
|------|-------------|----------|----------------|
| [albion.png](https://github.com/alexsabine/CRR/blob/main/albion.png) | Blake's Albion | Philosophers | Artistic framing |
| [bees.png](https://github.com/alexsabine/CRR/blob/main/bees.png) | Bee swarm | General public | Collective imagery |
| [fish.png](https://github.com/alexsabine/CRR/blob/main/fish.png) | Fish | Biologists | Biological imagery |
| [marine.png](https://github.com/alexsabine/CRR/blob/main/marine.png) | Marine life | Oceanographers | Ecological imagery |
| [moss.png](https://github.com/alexsabine/CRR/blob/main/moss.png) | Moss | Ecologists | Slow dynamics |
| [mycelium.png](https://github.com/alexsabine/CRR/blob/main/mycelium.png) | Mycelium | Network scientists | Network imagery |
| [tree.png](https://github.com/alexsabine/CRR/blob/main/tree.png) | Tree | General public | Growth cycles |
| [jacob.png](https://github.com/alexsabine/CRR/blob/main/jacob.png) | Jacob | Storytellers | Narrative |
| [newton.png](https://github.com/alexsabine/CRR/blob/main/newton.png) | Newton | Scientists | Heritage |
| [stock.png](https://github.com/alexsabine/CRR/blob/main/stock.png) | Stock market | Quants | Financial application |
| [thunder.png](https://github.com/alexsabine/CRR/blob/main/thunder.png) | Lightning | General public | Rupture imagery |

---

# Quick Reference: Who Should Read What

## By Role

| Role | Start Here | Then Read | Key Simulations |
|------|-----------|-----------|-----------------|
| **AI/ML Researcher** | README.md | crr_solomonoff_analysis.pdf, multiscale_crr_proof_sketch.md | fep-agent-shapes.html, perceiving-agent.html |
| **Cognitive Scientist** | fep_crr_integration.md | crr_active_reasoning.md, aha.pdf | fep-crr-5stages.html, child_dev.html |
| **Physicist** | crr_full_proofs.md | crr_advanced_proof_sketches.md | black_hole_enhanced.html, crr-thermo-rupture-rate.html |
| **Biologist** | [crr-explained.html](https://www.cohere.org.uk/crr-explained.html) | README.md | butterfly.html, ecosystem.html |
| **Mathematician** | crr_meta_theorem.md | crr_first_principles_proofs.md | dirac-delta-crr.html |
| **Therapist/Psychologist** | README.md (contemplative section) | aha.pdf, nostalgia_trap.html | inner_screen.html |
| **Educator** | crr-explained.html | guide.html | fep-crr-game.html, CRR_Art.html |
| **General Public** | index.html | crr-explained.html | CRR_Art.html, fep-crr-game.html |

---

# Summary Statistics

| Category | Count | Description |
|----------|-------|-------------|
| **Markdown** | 15 | Core proofs and documentation |
| **PDF** | 17 | Formal treatises and diagrams |
| **HTML** | 78 | Interactive simulations |
| **Python** | 6 | Validation scripts |
| **Images** | 25 | Diagrams and illustrations |
| **Total** | **141** | Complete repository |

---

**Document Version:** 1.0
**Generated:** January 2026
**Repository:** https://github.com/alexsabine/CRR
**Website:** https://alexsabine.github.io/CRR/

---

*This catalogue is designed for conversion to PDF. Use any markdown-to-PDF converter or print from a markdown viewer.*

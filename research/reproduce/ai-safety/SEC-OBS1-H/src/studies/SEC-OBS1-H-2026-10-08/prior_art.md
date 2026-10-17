# Prior art for SEC-OBS1-H (summary; the full review is `studies/SEC-OBS1-2026-10-08/SEC_OBS1_PRIOR_ART.md`)

No novelty is claimed for any component tested here.

| element tested | native counterpart |
|---|---|
| anchor penalty `κ F` with a proximal step (SEC v2 and its /16 variant) | EWC / online Laplace (Kirkpatrick et al. 2017); SEC v2's calibration, `CRR-LLM-CALIBRATION/SEC_V2_RULE.md` |
| GPM update projection onto the complement of stored old-task input subspaces | Gradient Projection Memory (Saha, Garg and Roy, ICLR 2021, arXiv:2103.09762); QGPM (Kim et al., ICLR 2026) compresses its memory; SplitLoRA and JANUS-LoRA (2026) apply related subspace splits to LoRA; FOPNG (arXiv:2601.12816) projects in the Fisher metric |
| switching the projection on after a light-anchored pilot (the schedule H1 tests) | combines the two families above. Not searched specifically before this freeze; listed as an open prior-art question in `SEC_OBS1_PRIOR_ART.md` |
| anchor re-evaluated on the same observed probes | matched-reference evaluation; prediction drift against a reference model (as monitored in distillation-based continual learning) |
| observability ι of the anchor on the probes | a chance-normalised performance of the reference model; ordinary |
| direction visibility η(v) | the data-processing (monotonicity) property of the Fisher metric (Čencov; Amari and Nagaoka 2000); standard |
| Fisher-subspace overlap, gradient conflict, CKA, effective gradient rank (the native set N) | FiUni (arXiv:2608.27070) and the Phoenix A6 comparator; gradient-interference measures; Kornblith et al. 2019 (CKA) |
| feature overlap against forgetting | Melton, Brito da Silva and Wunsch, AAAI-26 student abstract (DOI 10.1609/aaai.v40i48.42255); Lanzillotta et al., ICLR 2026 (arXiv:2512.07400): "heads collapse, features stay" |
| Fisher–Rao path coherence and apparent surplus (H3) | Fisher–Rao arc length (thermodynamic length; natural-gradient path length). The CRR-specific choice is to use the path minus the chord as a feature. Phoenix's heuristic ledger already grades surplus MISLED as a predictor |

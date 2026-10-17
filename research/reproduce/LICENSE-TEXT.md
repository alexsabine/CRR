# Licence for the text in this folder

Copyright (c) 2026 Alexander Sabine.

The written material in `research/reproduce/` (the README files, preregistrations, result write-ups, reports, ledger
excerpts and other prose and data records) is licensed under the
**Creative Commons Attribution 4.0 International licence (CC BY 4.0)**:
<https://creativecommons.org/licenses/by/4.0/>.

You may share and adapt it for any purpose, including commercially, provided you give appropriate credit, link to the
licence, and indicate if changes were made. Suggested credit:

> Alexander Sabine (2026), CRR reproduce area, research/reproduce/, CC BY 4.0.

**Code** (`*.py`, `*.sh`, `*.toml`, lockfiles and other source files) is licensed under the MIT licence in
[`LICENSE`](LICENSE).

**Third-party material keeps its own licence.**

| what | where | licence |
|---|---|---|
| Mammoth continual-learning library (aimagelab/mammoth, commit e75a491), vendored and trimmed by the SOTA1 study | `continual-learning/SOTA1/src/runs/sota1/frozen/mammoth/` | MIT, Copyright (c) 2020 Pietro Buzzega, Matteo Boschini, Angelo Porrello, Davide Abati, Simone Calderara (`mammoth/LICENSE`; also `mammoth/gem_license`, `mammoth/NOTICE.md`) |
| Project Gutenberg catalogue metadata (titles, authors, subjects) | `continual-learning/SEC-PG-LLM-H/src/studies/SEC-PG-LLM-H-2026-10-08/pools.json` | public catalogue data from gutenberg.org |
| OpenML dataset descriptions saved at preregistration | `continual-learning/*/src/prereg/*/descriptions/`, `openml_*.json` | OpenML metadata; each dataset's own licence is in its description |

**No dataset, book text or model weight is redistributed here.** Every run script fetches data from its public source
(PMLB, OpenML, gutenberg.org, cs.toronto.edu for CIFAR-100, the Hugging Face Hub) and checks it against the committed
sha256 manifest. Those sources' own terms apply to what you download.

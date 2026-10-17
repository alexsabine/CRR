# P23-AGING-CRR (2026-10-16): does CRR's account of time help decide when and from what to repair?

Start with `REPORT.md`. The derivation of every CRR operation for this system is in `DESIGN.md` §1, the arms and
must-pass controls in §2, and the development calibration in §3. The protocol is `PREREG.md`, frozen at commit
7fd6b14 (hashes in `FREEZE.sha256`) before any test seed.

**System.** The ageing NCA of Pio-Lopez, Hartl & Levin (2025, Adv. Sci. e09872), run unchanged from
github.com/bhartl/muse @ 9404ec3 with mindcraft (github.com/bhartl/NeurEvo) @ c93ac2c9. Environment as in
`../P23-AGING-2026-10-16/README.md`.

**Scripts.**
- `crr_repair.py` runs one arm over a seed range. Each organ has a tracker for:
  - the CRR quantities: Fisher–Rao arc of the cell-type distributions, cuts at a = π, and the past-weighted seed
    with prior equal to the primordial state;
  - the ordinary rivals: a clock-sampled moving average, a healthy checkpoint, the canonical target, a clock
    trigger, an early damage trigger and immediate repair.

  It re-implements the paper's repair trigger, and reproduces the authors' own run exactly.
- `analyze_crr.py`: per-arm summary (fitness, organs, cell writes, cuts) and the frozen paired-contrast rule.
- `results/`: development calibration (`dev_*.json`) and test analyses.

```bash
python -I crr_repair.py --muse MUSE --mindcraft NEUREVO --arm S_CRR --seeds 1000:1050 --out S_CRR.npz
python -I crr_repair.py --muse MUSE --mindcraft NEUREVO --arm S_CLOCK --delta 21,18,10 --seeds 1000:1050 --out S_CLOCK.npz
python3 analyze_crr.py results/test.json TEST_DIR --contrasts S_CRR:S_CLOCK,S_CRR:S_ANY,C_CRR:C_PRIM,C_CRR:C_EMACLOCK,S_CRR:C_PRIM
```

CPU only, no API use. Raw lifetimes are not committed; every run is seeded and deterministic.

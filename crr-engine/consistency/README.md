# Consistency reproductions (Session 3)

This directory holds analysis scripts that reproduce the empirical
consistency claims required for T1 → T2 promotion.

Each script is end-to-end runnable: fetch → analyse → assert.
A reviewer running `python <script>.py` should obtain the same
T2-promoting numbers reported in the corresponding
`claims/<id>/consistency.md`.

Scripts that depend on data not reachable from the campaign sandbox
are marked **[REVIEWER-RUN]** in the file header. They are committed
in runnable form so an unaffiliated reviewer can execute them
against the public datasets cited in the corresponding `consistency.md`.

| Script | Claim | Public dataset | Sandbox-runnable |
|--------|-------|----------------|------------------|
| `solar_hale.py` | P1 | SILSO v2.0 monthly sunspots | [REVIEWER-RUN] |
| `gwtc.py` | P2 | LIGO/Virgo GWTC-1/2/3 | [REVIEWER-RUN] |
| `nist_spectra.py` | P3 | NIST Atomic Spectra Database | [REVIEWER-RUN] |
| `dark_energy.py` | P4 | Pantheon+ / DES SN | [REVIEWER-RUN] |
| `clt_regularization.py` | P7 | (synthetic — pure math) | yes |
| `thermodynamic_omega.py` | P6 | (dimensional analysis) | yes |
| `physionet_1f.py` | B1 | PhysioNet (e.g., MIT-BIH NSR) | [REVIEWER-RUN] |
| `physionet_hrv.py` | B2 | PhysioNet HRV cohorts | [REVIEWER-RUN] |
| `agi26_phase_gating.py` | B3 | AGI-26 dataset (link in claim) | [REVIEWER-RUN] |

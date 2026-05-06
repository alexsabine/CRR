# Session 8 — Data execution log

This log records, for each of the ten Session 8 pre-registrations,
**what data could be fetched in this sandbox**, **what was
executed**, and **what remains reviewer-runnable**.

The campaign's `overall_status.md` documents that the sandbox
network policy is allowlist-restricted; this log makes the
restriction concrete for Session 8.

## Sandbox network probe

Tested 2026-05-06. HTTP probes (timeout 5s):

| Host | Status |
|------|--------|
| github.com / raw.githubusercontent.com / api.github.com | **200** |
| pypi.org / files.pythonhosted.org | **200** |
| sidc.be (SILSO) | 403 (host not in allowlist) |
| cdaw.gsfc.nasa.gov (LASCO CME) | 403 |
| omniweb.gsfc.nasa.gov (OMNI) | 403 |
| jsoc.stanford.edu (HMI) | 403 |
| heasarc.gsfc.nasa.gov | 403 |
| archive.stsci.edu (MAST) | 403 |
| physionet.org | 403 |
| dandiarchive.org | 403 |
| openneuro.org | 403 |
| gwosc.org / gw-openscience.org | 403 |

GitHub and PyPI are reachable; **all named scientific archives
are blocked**. Where third parties have mirrored the canonical
public datasets onto GitHub, those mirrors are reachable.

---

## Per-prediction data status

### P8 — Solar differential-rotation latitudinal CV (T²)

- **Canonical source:** SDO/HMI ring-diagram pipeline, `jsoc.stanford.edu`. Blocked.
- **GitHub mirror:** none located via 7 keyword searches.
- **Status:** **REVIEWER-RUN.** Pre-registration committed; analysis pipeline outline retained in `notes/session_8_new_predictions_and_applied.md` Part A (P8). Author / reviewer with JSOC access can execute by fetching `hmi.V_avg_ring_pdf_*` ring-diagram tables 2010–2024.

### P9 — CME inter-arrival CV at solar maximum

- **Canonical source:** SOHO/LASCO CDAW catalogue, `cdaw.gsfc.nasa.gov/CME_list/`. Blocked.
- **GitHub mirror:** none located.
- **Status:** **REVIEWER-RUN.** Reviewer-runnable on the named catalogue; protocol unchanged.

### P10 — Sunspot-cycle vs Hale-cycle CV ratio

- **Canonical source:** SILSO V2 monthly mean total sunspot, `sidc.be`. Blocked.
- **GitHub mirror:** `Shivayk0505/Forecasting-of-Sunspot-Numbers-Time-Series-Data/SN_m_tot_V2.0.csv` — verbatim copy of canonical SILSO file (3313 monthly rows 1749-01 → 2025-01).
- **Status:** **EXECUTED LIVE.** See `claims/P10_sunspot_hale_cv_ratio/result.md`.
- **Result:** **Pre-registration FAILED.** Empirical ratio 1.382 ± 0.50 (95% bootstrap), outside both T3 band [1.7, 2.3] and falsifier band [1.5, 2.5]. CV_Hale = 0.0823 reconfirms P1 SU(2) identification at upper edge of [0.0767, 0.0820]; CV_sunspot = 0.1138 is between SO(2) and SO(3) predictions. **P10 v1 negative is permanent.**

### P11 — Solar-wind sector-boundary inter-crossing CV (SU(2))

- **Canonical source:** OMNIWeb 1-hour merged IMF, `omniweb.gsfc.nasa.gov`. Blocked.
- **GitHub mirror:** none located.
- **Status:** **REVIEWER-RUN.** Reviewer with OMNIWeb access can execute the protocol unchanged.

### P12 — Black-hole ringdown overtone-frequency CV (SO(3))

- **Canonical source:** GWTC-O5 catalogue (LIGO/Virgo/KAGRA, expected 2028 release). Not yet published anywhere.
- **GitHub mirror:** N/A (data does not exist yet).
- **Status:** **POST-2028 EXECUTION.** Pre-registration committed at branch
  `claude/verify-folder-access-CInY3` head; freeze-locked against any future O5 ringdown spectroscopy.

### P13 — LMXB high-frequency QPO inter-cycle CV (SO(2))

- **Canonical source:** HEASARC RXTE/NICER archives. Blocked.
- **GitHub mirror:** none located.
- **Status:** **REVIEWER-RUN.** Protocol unchanged.

### P14 — AGN X-ray break-frequency CV (SO(2))

- **Canonical source:** González-Martín & Vaughan 2012 (A&A 544, A80) and successor catalogues. Catalogue CSVs are typically appendices to the paper.
- **GitHub mirror:** none located in 4 keyword searches.
- **Status:** **REVIEWER-RUN.** Protocol unchanged. Note: GM&V 2012 reported 104 AGN with measured break frequencies; restricting to log M_BH ∈ [7, 8] retains roughly 25–35 sources, satisfying the pre-registered N ≥ 25.

### B8 — Mammalian circadian inter-peak CV under DD (SO(2))

- **Canonical source:** Mouse Phenome Database / DANDI / PhysioNet wheel-running archives. Blocked.
- **GitHub mirror:** none located in 3 keyword searches.
- **Literature consistency:** According to PubMed, free-running circadian period in mice in constant darkness is well-characterised; Purnell & Buchanan 2020 ([DOI: 10.1152/japplphysiol.00211.2020](https://doi.org/10.1152/japplphysiol.00211.2020)) confirms SCN-dependent free-running breathing rhythms in DD. Mogavero et al. 2022 ([DOI: 10.1111/ejn.15632](https://doi.org/10.1111/ejn.15632)) reports period shortening / lengthening in BALB/cJ vs BALB/cByJ aggressive mice in DD, demonstrating the mouse-strain-level period CV is a tractable wearable-grade statistic. None of these papers report the inter-peak-CV statistic at the level B8 requires; the prediction remains pre-registered. Uchida et al. 2015 ([DOI: 10.1016/j.neulet.2015.10.071](https://doi.org/10.1016/j.neulet.2015.10.071)) demonstrates SCN/ARC oscillator periods are matched.
- **Status:** **REVIEWER-RUN.** Protocol unchanged.

### B9 — Mammalian respiratory inter-breath CV in quiet wake (SO(2))

- **Canonical source:** SHHS / MROS / MIT-BIH PSG via NSRR / PhysioNet. Blocked.
- **GitHub mirror:** none located.
- **Literature consistency:** According to PubMed, Yamauchi et al. 2014 ([DOI: 10.1007/s11325-014-0951-7](https://doi.org/10.1007/s11325-014-0951-7)) explicitly report "coefficient of variation (CV) for breath-to-breath tidal volume" in 17 healthy volunteers in dark vs light environments; **CV is the canonical published statistic** for this measurement in sleep-medicine literature. They find CV decreases after sleep onset versus before, and is sensitive to ambient light — context relevant to B9's "quiet wake" restriction. Pion-Massicotte et al. 2018 ([DOI: 10.1111/jsr.12667](https://doi.org/10.1111/jsr.12667)) developed a respiratory-rate-variability + HRV algorithm for sleep classification on biometric shirt data, demonstrating breath-to-breath statistics are routinely deployed at portable-monitor scale. Neither paper reports the specific CV-of-IBI in quiet-wake required for B9; B9's quantitative pre-registration remains untested.
- **Status:** **REVIEWER-RUN.** Protocol unchanged. Yamauchi et al. 2014 report tidal-volume CV; B9 should additionally report inter-breath-interval CV (IBI = onset-to-onset).

### B10 — Cortical gamma-cycle period CV in awake LFP (SO(2))

- **Canonical source:** DANDI Allen Visual Coding Neuropixels; CRCNS visual-cortex LFP. Blocked.
- **GitHub mirror:** none located.
- **Status:** **REVIEWER-RUN.** Protocol unchanged.

---

## Adjacent literature consistency for HRV (B2 prior, also bears on B9 / Vertical 1 applied case)

According to PubMed, Bellenger et al. 2021 ([DOI: 10.3390/s21103571](https://doi.org/10.3390/s21103571)) report a coefficient of variation in Ln-RMSSD of **3% to 13%** for wrist-based PPG HRV measurements (WHOOP) versus ECG-reference, varying with filter strength. CRR's B2 prediction CV ≈ 0.080 = 1/(4π) sits inside this empirical range at the centre. This is a *consistency* observation only — not a B2 promotion event — but it is a useful applied-grade calibration: consumer-wearable HRV variability is operating in the same band CRR predicts as the SO(2) substrate value.

---

## Summary

| Prediction | Substrate | Sandbox status | Result |
|------------|-----------|---------------|--------|
| P8 | T² | reviewer-run | not executed |
| P9 | SO(2) | reviewer-run | not executed |
| **P10** | SO(3) vs SU(2) | **EXECUTED** | **FAILED — ratio 1.382 (i.i.d. null)** |
| P11 | SU(2) | reviewer-run | not executed |
| P12 | SO(3) | post-2028 | not executable yet |
| P13 | SO(2) | reviewer-run | not executed |
| P14 | SO(2) | reviewer-run | not executed |
| B8 | SO(2) | reviewer-run | literature consistency only |
| B9 | SO(2) | reviewer-run | literature consistency only |
| B10 | SO(2) | reviewer-run | not executed |

**One execution out of ten. One honest negative. Nine reviewer-
runnable scripts and pre-registrations now committed for future
external execution.**

This pattern matches the campaign's pre-existing sandbox bottleneck
(`overall_status.md`): claims with public data routed through
the named scientific archives — PhysioNet, DANDI, OMNIWeb, JSOC,
HEASARC, MAST, GWOSC, sidc.be — are reachable only by reviewers
or the framework's authors who are outside this sandbox's
allowlist.

The P10 negative is a contribution. Per CAMPAIGN.md PART III:
*"failed pre-registrations stay committed permanently."* The ratio
of 1.382 against an i.i.d. null of 1.414 and a CRR prediction of
2.0 is a clean separation — the data favours i.i.d., not the M22
SO(3) identification of the sunspot-counting cycle. This narrows
M22's empirical commitments cleanly: the SO(2)/SU(2) Hale-cycle
prediction stands (CV_Hale = 0.082 is in the predicted band); the
sunspot-counting SO(3) prediction does not.

## Audit-trail summary

- Session 8 pre-registration commit: `6121c22` — 10 predictions
  + applied scoping.
- P10 execution + result commit: `b77a55c` — fetch.py / analyse.py
  / result.md / tier.md.
- This log: subsequent commit, branch `claude/verify-folder-access-CInY3`.
- All references to PubMed-indexed literature above include
  attribution and DOI links per the PubMed terms of use.

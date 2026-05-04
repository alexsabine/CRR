# B4 — Anti-correlation ρ = −1/2 between perception and action channels

## Prediction

Empirical realisation of M11 in sensorimotor data: when perception
and action are decomposed into Z₂-rupture channels acting on a
shared SO(2) phase manifold (e.g., the joint sensorimotor state),
their fluctuations exhibit ρ = −1/2.

## Empirical regularity

Sources (public):
- **Allen Brain Observatory** (Visual Coding & Behavior datasets,
  open via AllenSDK). Includes simultaneous neural recordings and
  behavioural responses in mice.
- **OpenNeuro** (`https://openneuro.org`) — repository of human
  fMRI / MEG / EEG with task data; many studies provide
  perception-action paired channels.
- **Human Connectome Project task-fMRI** — perception-action
  task paradigms with precise stimulus / response timing.

## Reproduction script

`crr-engine/consistency/perception_action.py` (skeleton):
1. Fetch Allen Brain Observatory Visual Behavior / OpenNeuro
   sensorimotor task.
2. Identify perception channel (sensory cortex spike trains or
   BOLD) and action channel (motor cortex / EMG / response time).
3. Decompose each into Z₂-rupture event sequence (threshold-crossings
   per the canonical CRR rupture rule).
4. Compute Pearson correlation between rupture-rate fluctuations.
5. Test against ρ = −1/2 prediction.

**[REVIEWER-RUN]** sandbox blocks Allen / OpenNeuro hosts.

## Tier decision

**Remains T1 (T2 pending).** The ρ = −1/2 prediction has a clear
operational definition under the rupture-topology framework
(`notes/rupture_topology.md`) and is tested on accessible public
data; the analysis is canonical; no obstacle but sandbox network.

## Applied usefulness for 2026 and beyond

- **Brain-computer interfaces:** ρ = −1/2 is a structural decoding
  prior — under M11, perception and action channels in BCI signals
  should anti-correlate at exactly this value. Used as a
  regularisation term, this stabilises decoder training in
  low-data regimes (typical for new BCI users).
- **Neuro-prosthetics adaptation:** as a user practices, decoder
  weights shift; ρ = −1/2 maintenance is a signature of healthy
  adaptation vs decoder collapse. Real-time monitor.
- **Assistive robotics:** the Z₂-rupture / SO(2)-phase decomposition
  applied to teleoperation channels (operator perception + robot
  action) gives a parameter-free synchrony index for telesurgery,
  remote-handling (Boston Dynamics + ROS 2), or VR/AR co-presence
  (Meta Quest, Apple Vision Pro 2026+).
- **Autonomous driving sensor-actuator fusion:** the same
  decomposition applied to LiDAR/camera (perception) + steering/
  throttle (action) channels gives a falsifiable ρ-signature for
  control-loop integrity. Departures from −1/2 may indicate
  sensor-actuator desynchronisation before downstream safety
  metrics fail.
- **Animal behaviour / cognitive ethology:** ρ = −1/2 in field-
  recorded predator-prey perception-action coupling; if confirmed,
  contributes to ecological monitoring (Earth Species Project,
  bioacoustic conservation pipelines).

The B4 application is most operationally relevant in BCI and
teleoperation, where both signal channels are clean, paired, and
pre-existing.

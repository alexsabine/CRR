# Audit of `bees.html` (the old "Honeybee Colony" page)

Written before any new code. Line numbers refer to `bees.html` as it stands (7,125 lines, about 350 KB). The file was read, not edited.

## 1. What it models

| Part | What the code does | Where |
|---|---|---|
| Per-bee task switching ("Layer A") | Each bee carries one number, `coherenceState`. Every frame it adds a hand-made "task fit" `L` (0.10 × a "visual coherence" score, ± 0.06 for neighbours on the same task, a penalty for "environmental pressure", ± 0.04 to 0.10 for being inside or outside). When the number reaches π the bee flips between two tasks, `forage` and `hive_task`, and the number returns to zero. | 2639–2685, 3200–3246 |
| Comb construction ("Layer B") | Bees aged 200 to 2000 frames with a "construction gene" cling to the nearest cell. A stretch counter rises by 0.05 a frame; at π a new circular cell is placed tangent to the anchor cell. Circles grow to a target radius. When two circles overlap a "wall" is recorded. Any three mutually touching cells are called a triple junction. | 1336–1540 |
| Forage heat-map ("Layer C", "distributed posterior") | A grid on the outdoor canvas. Each bee adds a Gaussian bump at its own position, weighted by exp(C/Ω); the grid decays by 0.985 a frame. | 4528–4540, `updateSharedPosterior` |
| Guards, soldiers, alarm ("Layer D") | 5% guards see a predator and fire at C = π. 30% soldiers read an alarm-pheromone grid; their chance of joining is a hand-made curve exp(C/Ω)(C*−C) named the "beauty function". Stinging bees die. Each sting adds (C*−Ω)/8 to a predator "venom" counter. | 2380–2560, 2850–2860, 4310–4470 |
| Swarm view ("Layer E") | 1,500 Vicsek-style particles. Each particle adds 0.04 × alignment to a counter, with a 0.998 decay; at π it re-randomises its direction. | 3565–4075 |
| "Webcam" | A second canvas showing the hive interior. No camera is used (`getUserMedia` does not appear). | toggle at 373 |
| Weather, seasons, predators, mutation, "RNA encoding", harvest | Buttons that change environment constants, add a predator, randomise trait strings. | 366–375 |
| Sound | One loop of filtered brown noise with band-passes at 234 Hz and 602 Hz, plus ticks and a 4:5:6 chord on events. This is the best-made part of the file. | 860–1200 |
| Mathematical layer visualisation | Fifty checkboxes ("Air Pressure", "Decision Trees", "Nutrient Networks" …). Most draw decoration. | 541–628 |

## 2. What rests on real bee science, and what does not

Real, and worth keeping:
- Cells begin round and become hexagonal as warm wax flows (Pirk et al. 2004; Karihaloo et al. 2013). The old page cites both. It also notes the rival view that bees build flat walls directly, which is fair.
- Wax is secreted by workers of middle age hanging in festoons. True in outline.
- Colony hum centred near 230 to 250 Hz. Reasonable.
- Alarm pheromone (isopentyl acetate) recruits defenders. True.
- Guards are a small minority at the entrance. True.

Named but not actually modelled:
- **The waggle dance.** There is a `waggleDances` list and a drawing of a figure of eight, but no bee reads direction or distance from a dance and nobody is recruited by one. The page has no von Frisch, no Seeley, no recruitment and no abandonment.
- **Response thresholds.** No Bonabeau, no Robinson. Task "switching" is a two-state flip driven by an invented fit score.
- **The 120° junction.** Junctions are not walls meeting. The code takes three touching circles, puts a point at the centroid of their centres, and measures the angles between the lines from that point to the three centres (1543–1553). No wax moves. Nothing relaxes. See section 3.
- **The dose-response of stinging.** The "beauty function" is an invented curve. The header says it "reproduces" Nouvian et al. 2018; nothing is compared with data.
- **Predator death.** The sting increment is chosen so that eight stings land on the peak of the curve, then the result is described as "matching" a pigeon LD100. That is a tuned constant presented as agreement.

Not bee science at all: "visual cortex", "RNA behavioural encoding", "mutation through rupture/rebirth", "memory entanglement", "Markovian bees in a non-Markovian field", "evolution pressure". These are labels on random numbers.

## 3. Every CRR quantity or "prediction" shown, and what it really is

| Readout (id) | Verdict | Why |
|---|---|---|
| Mean evidence ⟨C⟩ (`avgCoherence`) | Measured, but of an invented quantity | A true average of `coherenceState`. The thing averaged is the hand-made fit score, so the number has no outside meaning. |
| Population | Measured | Count of bees. |
| Hive Progress | Decorative | `hiveConstructionProgress / 20`, capped at 100%. The 20 is arbitrary. |
| Resources | Measured (arbitrary units) | Running sum of nectar brought back. |
| Honey Stores | Measured (arbitrary units) | Sum over cells of a rate times "gene" strengths. |
| Bees Inside | Measured | Count. |
| **Switch interval CV** (`cvObserved`) | **Measured** | Standard deviation over mean of the last intervals between flips (6963–6971). Honest arithmetic. What it measures is the spread of an invented score reaching π. |
| **Predicted CV (Ω/2) 0.159** (`cvPredicted`) | **A constant** | `1/(2π)` printed every frame (7002). Labelled "Predicted". It is a candidate value from the research programme, not a prediction about this run or about bees. |
| Task switches (last 5 s) | Measured | Count in a 300-frame window. |
| **Diagnostic class** A/B/C (`diagnosticClass`) | **Decorative** | The ratio of the two numbers above, cut at 0.85 and 1.15, with the words "autonomous", "regulated", "noise". The cut points are arbitrary and the classes mean nothing outside the page. The header calls a miss "the framework working, not a failure mode", which makes the readout unfalsifiable. |
| **Mean junction angle (→ 120°)** | **Misleading** | It prints the literal text "120°" (`(120).toFixed(0)`, line 7013) followed by a deviation. The mean of three angles round a point is always exactly 120° because they sum to 360°. The deviation is real arithmetic but is taken between cell centres, not walls, and no process drives it down. The arrow "→ 120°" promises a convergence the model does not contain. |
| Triple junctions (SO(2) closures) | Measured count, decorative label | Number of touching triples. "SO(2) closure" adds nothing. |
| Wall merges / 5 s (Z₂) | Measured count, decorative label | New circle overlaps in the window. |
| Active defenders | Measured | Count. |
| Peak IPA | Measured (arbitrary units) | Maximum of the alarm grid. |
| **Beauty peak C*−Ω 2.82** | **A constant** | `π − 1/π` printed every frame (7041). Never changes. Shown as if it were a result. |
| **Swarm CV (Layer E, target 0.159)** | Measured, with a target beside it | Honest arithmetic on particle intervals. The source comment admits it usually misses and suggests moving the φ slider until it lands, which is tuning to match. |
| Swarm ruptures (sample) | Measured | Length of a capped list, so it stops at the cap. |
| Defender losses (autotomy) | Measured | Count. |
| **Predator C_venom (peak at 2.82)** | Measured, of a tuned quantity | The increment per sting was chosen so that eight stings hit the "peak". |
| "Behavioural plasticity (φ)" slider | A setting | Multiplies every invented rate. Changes the CV. |

Other claims in the header text that the page cannot support: "Active Inference at four scales", "each bee maintains a generative model", "the colony's shared belief", "topologically fixed, not free parameters", "Layer D prediction … testable".

**Summary.** Two readouts are constants dressed as results (0.159 and 2.82). One is a verdict with no meaning (class A/B/C). One states a mathematical triviality as a finding (120°). The CVs are measured honestly but measure invented rates, and one is steered towards its target by a slider. The counts are real counts. No number on the page was compared with any observation of bees.

## 4. What the new page keeps, changes and drops

Keep:
- The subject, and the best idea in the old page: comb that starts round and settles into hexagons.
- The sound: the brown-noise hum at 234 and 602 Hz and the soft wax tick. Ported.
- Hornet, weather, a flower bloom.

Change:
- **Task switching** becomes the fixed response-threshold model of Bonabeau, Theraulaz and Deneubourg (1996), with real stimuli that work reduces (hungry brood, a queue of loaded foragers, full stores, heat, an unguarded door, alarm scent). CRR supplies only the timing form: a bee counts stimulus that exceeds what her present task offers, measured against her own threshold; at a fixed count she switches and the count restarts. The page says this model already has that shape, and says where the two differ (Bonabeau's rule is a memoryless probability, the count is not).
- **Comb** becomes a wall network with real triple junctions that move under line tension (Plateau's rule), only while the wax is warm. The page reports the mean distance of junction angles from 120°, never the mean angle, and says why.
- **The forage map** becomes a leaky sum of waggle runs at the places the dancers advertised. Bees outside do not write to it.
- **The waggle dance** is modelled: angle from vertical is the patch's bearing from the sun, run length in time is its distance, the number of runs follows profit, followers are recruited with error, and a forager abandons a patch by a count of shortfall. Stop signals shorten dances for a failing patch.
- **Defence**: guards count evidence of the hornet and release alarm; alarm is a stimulus in the same threshold model; mobbing drives the hornet off. No sting deaths, no venom counter, no "beauty function".

Drop: swarm view, "webcam" naming, mutation and RNA, harvest, the fifty checkboxes, the φ slider, the diagnostic class, the beauty peak, every use of "predicted", "posterior", "generative model", Z₂ and SO(2) on the page.

Readouts on the new page, all measured from the run: foragers out; nectar loads in during the last minute; task switches in the last minute; the CV of switch intervals with its sample size; the share of recent waggle runs for the leading patch; the mean distance of junction angles from 120°. The candidate value 0.159 appears once, beside the measured CV, labelled as a candidate. No rate in the model was set with it in mind, and the tests record whatever CV comes out.

# Song of Willow: notes on the original (song_of_willow.html)

Read top to bottom before the rebuild. These are working notes, not page copy.

## Clock
- BPM 66, one beat = 60/66 = 0.90909 s. TOTAL_BEATS 384 = 349.09 s (5:49). A tempo slider (0.7 to 1.3) scales the beat.
- Scheduling is per animation frame: `tickAudio` fires every score event whose beat has passed, at `ac.currentTime`. So every onset is late by up to one frame. Robins use `setTimeout`. The parrot uses a frame countdown (`noteTimer -= dt; noteTimer = noteDur`), so it drifts late by up to a frame per syllable.

## Movements (beats; seconds = beats x 0.909)
| # | name | label | beats | seconds | wind level `ar` |
|---|------|-------|-------|---------|------|
| 1 | SEED | seed | 0-31 | 0:00 | 0 |
| 2 | ROOT | roots reaching | 32-63 | 0:29 | .08 |
| 3 | SAPWOOD | first sap | 64-95 | 0:58 | .15 |
| 4 | CANOPY UNFOLDS | leaves unfurling | 96-135 | 1:27 | .25 |
| 5 | THE WIND ARRIVES | the wind arrives | 136-175 | 2:04 | .45 |
| 6 | LEAF SONG | ten thousand leaves | 176-215 | 2:40 | .6 |
| 7 | STORM | the storm | 216-247 | 3:16 | .85 |
| 8 | DELTA | δ(now) | 248-263 | 3:45 | 1 |
| 9 | AFTER RAIN | after rain | 264-295 | 4:00 | .4 |
| 10 | REFLECTION | still water | 296-327 | 4:29 | .25 |
| 11 | CATKIN | catkin release | 328-351 | 4:58 | .15 |
| 12 | STILLNESS | one leaf | 352-383 | 5:20 | .05 |

## Harmony
D minor throughout the score. Chords as MIDI lists [bass, +octave, three upper tones]:
Dm [38,50,53,57,62], Dm7 [..65], Dm9 [..64], Gm [43,55,58,62,67], Gm7 [..65], Am [45,57,60,64,69], Am7 [..67], Bb [46,58,62,65,70], Bbmaj7 [..69], Fmaj7 [41,53,57,60,64], C [36,48,55,60,64], Cmaj7 [36,48,55,59,64], Dsus [38,50,55,57,62], Eaug [40,52,56,64,68].
Progressions per movement (changing every 4 beats, or 5 in IV to VI, 3 in XI):
- ROOT: Dm Dm Fmaj7 Dm Gm Dm Am Dm
- SAPWOOD: Dm Dm7 Gm7 Am7 Fmaj7 Dm Gm C
- CANOPY: Dm9 Gm7 Bbmaj7 Fmaj7 Am7 Dm7 C Gm
- WIND: Gm Dm Am Bb Fmaj7 Gm C Dm7
- LEAF SONG: Dm9 Gm Am7 Bbmaj7 Fmaj7 Dm7 Gm7 C
- STORM: Dm Gm Am Eaug Bb Dm Gm Dm
- AFTER RAIN: Dm9 Fmaj7 Bbmaj7 Gm7 Am7 Cmaj7 Dm7 Gm
- REFLECTION: Dm9 Cmaj7 Fmaj7 Dm7 Bbmaj7 Gm7 Am7 Dm9
- CATKIN: Dm Dsus Dm9 Fmaj7 Gm Dm Am Dm9

## Score (buildScore), event kinds
`section, drone, tone, shim, bass, pad, arp, leaf, creak, wind, drip, cavit, choir, water, rupture, rbchoir, robin, parrot`.
The score uses Math.random for: which chord tone a tone/shimmer takes, arp velocities, leaf burst sizes and velocities, some creak, cavitation and drip velocities. So every performance of the original differs in those choices; rhythm and harmony do not.
- SEED: drone .02; single tones D4 (b0), A3 (b8), F3 (b16), D3+D4 (b24); shimmer D5 on beats 4, 12, 20, 28.
- ROOT: bass every 8, sub-octave tone every 4, cavitation click every 6, water wash every 8 (+4).
- SAPWOOD: bass + third every 4, shimmer every 2, cavitation every 6, water every 8.
- CANOPY: bass + pad every 4, shimmer every 2, leaf bursts every 3 (growing), rising arp every 8, cavitation every 6, water.
- WIND: bass + pad every 4; leaf bursts + tone every 2; wind gusts on l%4==2 (growing); falling-rising arp every 8; creak every 6; cavitation every 3.
- LEAF SONG: leaf bursts every beat (8-15 leaves); wind + tone every 2; arp every 4 (0.45 beat); creak every 8; choir (formant "ah" pad) on l%4==2; drips every 3.
- STORM: leaf bursts every beat (12-23); wind every beat, rising; tone + creak every 2; arp every 4 (0.35 beat); cavitation every 3; choir every 6; water.
- DELTA: beat 248 `rupture` (lightning); leaf and wind dying over 8 beats; creaks 4 beats; drips from l=4; sparse Dm tones; water and D4 shimmer from l=8; pad at l=8.
- AFTER RAIN: rainbow choir init at 263, seven voices enter at 264 + 1.5 i, morph to Ah at 280 (4 beats), to Eh at 290 (3 beats), fade from 298 over 12 beats. Bass + pad every 4, drips every 2, shimmer every 3, soft leaves, light wind every 6, arp every 8.
- REFLECTION: robins init 301, land 302, sing 306. Parrot lands 310, sings 315. Bass + pad every 4, shimmer, slow arp (0.8 beat) every 8, water every 6, leaves every 4, single drip.
- CATKIN: thinning bass and high tones (an octave up), pad every 6, two-leaf bursts every 2, faint wind.
- STILLNESS: D4 shimmer at 352, 360, 368; A3 tone at 352; one leaf at 352; drone to .005 at 376.

## Sound sources
Master: sources -> group gains -> master gain .65 -> compressor (-14 dB, 4:1, knee 8) -> dry (1 - .25 x reverb) + convolver (6 s noise IR with 40 early taps) x reverb .65 -> analyser -> out.
Group gains: wind, leaf, wood, water = slider x .5 (default .55, .55, .5, .5); tone .4; pad .35; choir .3; robin .45; parrot .55.
- Drone: sines at 36.7, 55, 73.4, 110.1, 29.1 Hz (gains .15 .08 .06 .04 .1), each lowpassed at 2.5 f; a .035 Hz LFO of 2 Hz depth on all; lowpassed noise (120 Hz) at .008. Level set by `drone` events with a linear ramp over the section length.
- Leaf: `cnt` noise grains within 0.25 s, bandpass at 340/(2 L) Hz with L in .08-.16 m (1060-2125 Hz), Q 2-5, high shelf +3-7 dB at 4 kHz, 2 ms attack, 20-50 ms decay.
- Wind: looped noise through four bandpasses (80, 350, 1400, 2500 Hz), swell envelope (20% up, hold, down), slow LFO on level.
- Creak: sawtooth 80-300 Hz falling to 70%, bandpass 1.5 f Q 3, plus bandpassed noise; 10 ms attack, exponential decay.
- Cavitation: sine 2-6 kHz chirping down to 40% in 80 ms, bandpass Q 8-16, 60-100 ms.
- Drip: sine at 3287/R Hz (R 1-4 mm, Minnaert) falling an octave in 40 ms, plus a highpassed noise tick.
- Water: looped noise through bandpasses near 250 and 1000 Hz, slow swell.
- Tone: two sines (f and 1.002 f), lowpass 3 f; 150 ms attack. Shimmer: FM, modulator at f x golden ratio, index .2 f. Bass: triangle + sub sine, lowpass 2 f. Pad: three sines per note (0, +-1.2 Hz), 1.5 s attack. Arp: sine, lowpass 4 f, 40 ms attack. Choir: five detuned sines per note through a bandpass near 700-900 Hz.
- Rupture (beat 248): highpassed noise crack, 30 ms sawtooth sizzle, lowpassed thunder rumble (to master directly), second roll at +0.8 s, thirty wood-crack grains, and a D minor "memory hum" (38 50 53 57 62) decaying over about 3 s + .8 ln(exp(C/Ω)).
- Rainbow choir: seven voices D3 F3 A3 C4 D4 F4 A4, two sawtooths each (5 cents apart), vibrato 4.8-5.8 Hz, breath noise, three formant bandpasses per vowel (Oo Oh Ah Ah Oo Mm Ee), each fading in over 3 s; group at .35.
- Robins: FM sine notes 1.8-8.5 kHz with a falling sweep, 45-85 ms long, in phrases whose interval shapes are taken from three Doris Day melodies ("Que Sera Sera", "Dream a Little Dream of Me", "Sentimental Journey"), found by a small genetic algorithm (12 phrases, 40 generations, fitness exp(-err/4n)). Male base MIDI 88, female 96. Antiphonal: male phrase, pause .35 s (+-16%), female phrase, pause .6-1.4 s. This runs from beat 306 until the parrot sings at 315; after that the robins give single backing chirps on every third parrot syllable, and a few single notes in STILLNESS.
- Parrot: "What a Lovely Day", an original tune in D major. Formant voice: two sawtooths + octave sine, three vowel formants (ARPABET table), presence peak 3.2 kHz, nasal peak 300 Hz, notch 950 Hz, consonant bursts (plosive, fricative, nasal, liquid, glide) and codas.

### The song at the end (MIDI, beats, word)
62 1 What | 64 .5 a | 66 1.5 love- | 69 1 ly | 74 2.5 day! | rest 1
74 1 Oh | 71 1 what | 69 .5 a | 66 1.5 love- | 64 1 ly | 62 2.5 day! | rest 1.5
62 1 The | 66 1 sun | 69 .75 is | 71 1.5 shin- | 69 .75 ing | 69 2 bright | rest .75
66 1 And | 69 1 ev- | 66 .75 ry- | 64 1.5 thing's | 62 1 al- | 62 3 right! | rest 2
69 1.5 Love- | 71 1 ly | 74 4 day! | rest 2
Total 43 beats (39.1 s). It starts at beat 315 and ends at 358. The original then waits 2.5-4 s and loops for ever, so a second pass begins near beat 361.5 and is still running when the score stops at 384; the parrot carries on after the end.

## Visuals in the original
Canvas 2D. Horizon at 62% of the height; below it a dark band that is both water and soil, with a root system drawn in it. A small stylised willow of straight segments and short green and silver dashes for leaves. Sky gradient from night through orange dawn to blue day and back, driven by `sunPhase` (a piecewise curve of the beat). Rain intensity is another piecewise curve (starts 190, peaks .9 at 248-264, clears by 296).
- SEED: night, nothing. Trunk grows over beats 5-60. Roots from 28. Main branches 58-110, whips and leaves after.
- WIND / LEAF SONG: whips swing as pendulums, leaves flip between a green and a silver state on random timers.
- STORM: rain streaks, distant lightning flashes from 230, some leaves torn off from 220.
- DELTA: at 248 a bolt strikes near the tree and a white flash; at 250 every leaf is released and falls.
- AFTER RAIN: leaves return one by one (each has a regrow beat between 268 and 328); a rainbow from 260 to 310.
- REFLECTION: two robins fly in and sing; a green parrot lands and sings with the words shown as karaoke with a bouncing dot. A draggable candle appears at 296; rainbow particles swirl into the flame; "move candle to reveal wind".
- Blue sap dots rise from the roots through the trunk.

## What the annotations claim, and what I do with each
- "leaf flutter: Z2 bistable, CV = 1/(2π) ≈ 0.159", "10,000 coupled oscillators". The CV was injected (a uniform jitter of that width on the threshold), not measured, and the leaves are not coupled. New page: each leaf integrates wind load and flips at a fixed threshold; the CV of flip intervals is measured from the run and shown beside 0.159 as a candidate. No tuning.
- "xylem cavitation = δ(now)", "Ω = 1/π (blocked/open)", "exp(C/Ω): strongest vessels first". Cavitation and its clicks are real (Milburn and Johnson 1966; Tyree and Dixon 1983; Tyree and Sperry 1989). The clicks in the piece are placed by the score. Keep the science, drop the Ω claims.
- "wind IS the driving L", "Kolmogorov = nested CRR", "C·Ω = 1 all δ(now) together", "reflection = C inversion", "Ω_water ≈ Ω_air", "pollen release = δ(now)", "exp(C/Ω)→1: all memories equally accessible". Assertions with nothing measured. Dropped.
- Candle "Ω = 1/π → rupture every π frames ≈ 7-10 Hz, the observed candle flicker frequency". Frame-rate dependent, dropped.
- Physics lines kept where standard: pendulum period 2π√(L/g) for a hanging withy; Hagen-Poiseuille; cohesion-tension; drag ½ρv²C_D A with reconfiguration (Vogel 1989); bending stress My/I; Minnaert bubble frequency for drips; lanceolate leaves, dark above and glaucous below. Numbers I cannot source (σ_yield ≈ 30 MPa, stomatal density, LAI 5-7, "flutter 5-20 Hz", sap velocity) are left off the page.
- "Robin song: 40 generations evolved, GA fitness → Doris Day intervals". That is how the robin phrases are made; it is a composing device, not ornithology. Say so.

## Bugs noticed in the original (not carried over)
- `rs.maleGA.getBestPhrase` does not exist (unreachable in practice).
- Threshold jitter makes the realised CV about 0.159/√3, not 0.159.
- `pCreak` noise gain starts at full level with no attack (click). Several `setValueAtTime` steps.
- `setTimeout` robin notes and frame-quantised onsets.

## Found later, while testing
- The original's "second pass" of the song starts 2.5 to 4 s after the last sung note ends at beat 356 (the timer for the final two-beat rest is overwritten by the pause), so between beats 358.75 and 360.4. The rebuild starts it at beat 360.
- In the original the lightning hum length works out at 5.28 s (the piece-level count reaches about 1.13 by beat 248). Used as a constant.
- Chrome's DynamicsCompressor adds make-up gain, so the original's compressor settings are part of its sound. Kept exactly; a second compressor as limiter and a fixed trim follow it.

## What the rebuild changed (for the report)
- Kept: every score event (kind, beat, pitch, length, velocity), tempo, all instrument recipes, mixer gains, compressor, the song's notes and words, robin procedure.
- Changed: onsets scheduled on the audio clock ahead of time; one fixed random seed (1887) instead of a new draw each play; stereo panning; reverb impulse with a darker tail; 1 to 2 ms ramps where gains stepped; limiter and trim; the song's voice gets a softer source, a fourth formant, breath, and vibrato that grows in; second pass at a fixed beat with a hummed third below; the piece ends at beat 408 instead of looping for ever; no tempo slider.
- Dropped from the picture: the draggable candle and rainbow particles, the underground root cutaway and blue sap dots, the bouncing karaoke dot, the CRR read-outs.

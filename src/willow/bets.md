# Song of Willow: bets, written before any run

Each bet states what would count as a pass and what as a fail. Results go in `test_output*.txt` as they come out; failed outputs are kept.

**B1. The score is the same score.** Feed the original `buildScore` (text lifted from song_of_willow.html, lines of §2 and §3, untouched) and the new `WILLOW.buildScore(seed)` the same seeded random stream. Pass: identical event count, and for every index the same kind, the same beat exactly, the same pitch or chord, the same duration, and velocity equal to within 1e-12. Three seeds. Any mismatch is a fail.

**B2. The onsets are where the score says.** For every score event the new engine's scheduled time minus the start time equals beat x 60/66 s to within 1e-6 s. Against the original page run on a simulated 60 fps clock with its own code (audio functions replaced by loggers): every new onset is at or before the original's dispatch time and no more than 1/60 s + 1e-6 s earlier. Fail if any event lies outside that.

**B3. The song at the end is the same tune.** The new first pass has the same 26 sung syllables in the same order with the same MIDI pitch, the same length in beats and the same word as PARROT_SONG in the original, starting at beat 315. Against the original on the simulated 60 fps clock: syllable k (counting rests) starts no later than the original and no more than (k + 1)/60 s earlier (the original loses up to a frame per note). Fail otherwise.

**B4. No clipping.** Render the whole piece through an OfflineAudioContext at 44.1 kHz stereo with default mixer settings. Pass: absolute peak below 1.0 (0 dBFS). Target: at or below 0.891 (-1 dBFS). Also report the peak with every mixer slider at maximum; that must be below 1.0 too.

**B5. Frame cost.** In headless Chromium at 1280x800, desktop quality, during the storm (the busiest movement): the JavaScript side of a frame (model step, buffer fill, GL calls issued, overlay) has a median under 4 ms and a 95th centile under 8 ms over 300 frames; draw calls per frame at most 16. In Node, the model step alone at desktop quality has a median under 2 ms. (GPU time under software WebGL is not a fair measure and is not part of the bet.)

**B6. The CV shown is the CV measured.** Collect the raw leaf-turn intervals from a run of the model through LEAF SONG, recompute sd/mean in the test from those raw numbers, and compare with the figure the page would print. Pass: equal to 3 decimal places. No bet is made on its value; the value is recorded beside the candidate 1/(2π) = 0.159 whatever it is. The model is not to be adjusted afterwards to move it.

**B7. Leonardo's rule holds in the model.** At every fork of the built tree, parent cross-section equals the sum of the daughters' (shoots included) to a relative error under 1e-9.

**B8. Wind seen follows wind heard.** Over the whole piece, sampled every quarter beat, the correlation between the wind-sound envelope taken from the score (sum of the wind events' gain envelopes) and the mean speed of the withy tips in the model is above 0.5. Fail at or below 0.5.

**B9. Page hygiene.** Zero page errors and zero console errors at 1280x800 and on the iPhone 13 profile; no horizontal scroll at 390 px; every button at least 44 px high; no sound before the Play gesture (AudioContext not created until click).

**B10. Robins (structure only; the original is random and frame-timed, so no note-for-note bet).** Between beats 306 and 315 the robins alternate male and female phrases, every note lies between 1.8 and 8.5 kHz, and the number of robin notes in that window is within 50% of the count from the original on the simulated clock with the same seed. Every third sung syllable of the song carries a male chirp at the same instant.

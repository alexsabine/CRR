# Bets for the hive, written before the model was run

Written before `hive_model.js` had been run once. Each bet has a threshold. The test script is `test_hive.js`; its outputs are kept in this folder, failures included. Settings are not to be changed in order to pass a bet without recording the earlier failure here.

All times are model seconds. "Employed" means a forager committed to a patch.

**B1. The colony favours the richer of two patches, and follows a swap.**
Two patches at equal distance (900 m), bearings −30° and +30°, nectar quality 0.9 and 0.45, no other patches, patches do not fade. Five seeds.
Pass if, in at least 4 of 5 seeds, at t = 300 s at least 60% of employed foragers are on the richer patch; and, with the qualities swapped at t = 300 s, at t = 660 s at least 60% are on the newly richer patch.

**B2. Junctions settle to 120°.**
Start from an unbuilt lower comb, let the bees build with warm wax for 600 s, then measure every complete junction older than 120 s.
Pass if the mean absolute distance of their angles from 120° is under 2.0°, AND the same junctions at the moment they formed averaged more than 4.0° (so the test is not empty). Control: with wax flow switched off the mean distance of the same class of junctions stays above 4.0°.
Note: the mean angle itself is always exactly 120° (three angles round a point sum to 360°), so it is not a bet.

**B3. The dance matters.**
Default world with patches that bloom and fade, 900 s, five seeds, same seeds with the dance on and off (off: no forager dances, so no recruitment; scouting unchanged).
Pass if mean nectar loads over the run are at least 20% lower with the dance off.
I expect this to pass but it may not: Sherman & Visscher (2002) and Dornhaus & Chittka (2004) found the benefit of the dance depends on how the flowers are spread.

**B4. Task-switch interval CV is reported, not judged.**
Default world, 900 s, five seeds, intervals between successive switches by the same bee, after a 120 s warm-up.
No pass mark. Record n, mean, CV per seed. The candidate value from the CRR programme is Ω/2 = 1/(2π) ≈ 0.159. My guess before running: the measured CV will be well above it, between 0.5 and 1.5, because thresholds differ between bees and the stimuli come and go. Nothing will be tuned towards 0.159.

**B5. Alarm recruits guards and they stand down afterwards.**
Default world, hornet sent at t = 120 s, five seeds.
Pass if, in at least 4 of 5 seeds, the number of bees on guard duty at its peak within 60 s is at least double the mean number in the 60 s before, the hornet is driven off within 90 s, and 120 s after it leaves the number on guard is back within 2 of the earlier mean.

**B6. Work answers need (response thresholds).**
Default world, fair weather for 200 s, then hot for 200 s.
Pass if the mean number of fanners in the last 100 s of the hot spell is at least 3 more than in the last 100 s of the fair spell, in at least 4 of 5 seeds, and the hive temperature in the last 100 s of the hot spell averages under 36.5 °C.

**B7. The dance says where.**
For every waggle run recorded in a default 600 s run: the run's angle from vertical equals the advertised patch's bearing from the sun to within the stated dancer scatter, and its duration equals distance/1000 s to within the stated scatter. This is a consistency check of the code, not a discovery. Pass if the mean signed errors are under 2° and under 3%.

---

# Log

**v1 (`test_output_v1.txt`)** First model. B1 pass 5/5. B2 pass (but nobody was building in the default world, see below). **B3 FAIL: fall 15.9%, under the 20% mark.** B4 CV 0.81 to 1.33. B5 pass 4/5, but the hornet left after 15 s before recruits mattered and only two alarms were released. B6 pass 5/5 with heavy overshoot (27 fanners in one seed). B7 pass.

**Change after v1, and why.** A trace of the default world showed whole cohorts switching together (55 receivers at once, then none; builders dropping to zero). That is a fault of the rule, not of a bet, so I changed the rule, not the thresholds of the bets:
- the response to a stimulus now saturates, using Bonabeau's own function s²/(s²+θ²);
- a bee meets stimuli by chance (one tick in four), so counts rise in steps;
- finishing a piece of work restarts her counts;
- a seventh state, rest, with a fixed small pull;
- the receive stimulus counts only foragers nobody has met;
- nurses search the larvae, not all cells; brood hunger time 40 → 90 s;
- mobbing needed to drive off the hornet 10 → 60 bee-seconds; guards release alarm repeatedly;
- dances shortened (maximum 14 → 8 runs, dance threshold 0.3 → 0.4) because a third of all foragers were dancing at once;
- wax time 12 → 20 s and deposits 3 → 4 so the comb does not finish in ten minutes.
None of these was chosen by looking at the CV or at 0.159.

**v2 (`test_output_v2.txt`)** B1 pass 5/5. B2 pass. B3 pass (27.4%). B4 CV 0.62 to 0.65 in the seeds I read. **B5 FAIL 2/5.** B6 pass. B7 pass.

**Change after v2**, for the picture only: dance floor radius 150 → 200, bees keep 38 units apart instead of 28, builders fill the frontier row by row, festoons hang as short chains, more flowers in a patch. No setting was changed to rescue B5.

**v3, final (`test_output_v3.txt`)** B1 PASS 5/5. B2 PASS (5.30° at formation, 0.24° after 120 s; control 6.66°). B3 PASS (29.9%; per seed 27 to 38%). B4 CV 0.605, 0.548, 0.942, 0.612, 0.489 (n = 48, 52, 36, 26, 44); my guess of 0.5 to 1.5 was right at the low end; nowhere near 0.159. **B5 FAIL 2/5**: hornet gone in 29 to 30 s and guards back to 4 every time, but the guard at least doubled in only 2 seeds (peaks 12, 7, 7, 10, 4 from about 4). The standing guard of four nearly drives the hornet off before recruits arrive. Left as it is and reported. B6 PASS 5/5 (overshoot to 37.5 fanners in one seed). B7 PASS.

B3 passed only after the rule change. The change was not made to pass it, but it did alter foraging (shorter dances, fewer bees stuck receiving), so the honest summary is: fail at 16% in v1, pass at 27 to 30% in v2 and v3.

# Results (bets in BETS.md were written first)

- test_output_v1.txt: first run, original settings. 21 of 25. Failed B1b, B3b, B3c, B4b.
- test_output_v2.txt / test_output.txt: final model. 22 of 25. Failed B1b, B3b, B3c.

Changes made between v1 and final, and why:
1. Chlorophyll absorption curve: green window widened (590-625 nm terms reduced) after the first render showed a transmitted
   colour that was too narrow a green, and B4b had read 0.903. Now 0.867. This is a calibration of approximate coefficients, not a test passed.
2. Anthocyanin curve made a little stronger and broader (0.055/35 nm to 0.07/40 nm) for a deeper red. Calibration, as above.
3. Venation: finer distances, more steps, and the blade lengthens before it broadens (gives a midrib with side veins). B5 thresholds unchanged.
4. Busy time of a centre changed from a fixed 10 ms to first-order recovery with mean 10 ms. Reason: with a fixed time, centres
   hit together stayed in step and oxygen came in long waves after any sudden change of light, which swamped the on-screen reading.
   The mean-rate formula is the same.
5. Colours outside the sRGB gamut are brought in by adding white, not by clipping.

Failures kept as they are:
- B1b: flash 11 was not above flash 12 in 1 seed of 5. The exact chain gives 0.287 and 0.283 for flashes 11 and 12, so my bet was too strong. Flash 7 was a local maximum 5/5.
- B3b: 1000 to 2000 umol raised oxygen x1.16 (bet: under x1.15). A rectangular hyperbola saturates slowly.
- B3c: 0.0985 O2 per absorbed photon at 25 umol (bet: 0.100 to 0.125). Misses, a little non-antenna absorption and the first busy losses bring it under 0.1.
- B4b as bet was about absorptance inside the blade; with surface reflection the share of incident light absorbed is about 0.84.

Live check (leaf.html?nogl, real-time loop, no WebGL): long-run oxygen rate 4.54 against formula 4.64 in October; 28.2 against 28.3 in July.
Short on-screen windows are noisy in autumn, when few centres remain (about 6% standard error).

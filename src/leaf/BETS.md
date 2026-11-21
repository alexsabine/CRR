# Bets for leaf.html, written before any run

Model settings fixed in advance: miss probability 0.10, double-hit probability 0.05 (flashes only),
dark-adapted centres 25% S0 and 75% S1, turnover time 10 ms, half of antenna photons to photosystem II.

B1 Kok flashes (6000 centres, dark-adapted start, 40 flashes, 5 seeds). Pass needs all of:
  a. of flashes 1 to 4 the largest oxygen yield is on flash 3, in 5 of 5 seeds;
  b. flashes 7 and 11 are local maxima (higher than both neighbours), in 5 of 5 seeds;
  c. yield on flash 1 is under 5% of flash 3 and yield on flash 2 is under 25% of flash 3;
  d. damping: (max minus min) over flashes 17 to 20 is under half of (max minus min) over flashes 1 to 4;
  e. mean yield over flashes 21 to 40 is within 5% of 0.2375 per centre per flash (= (0.85 + 2 x 0.05) / 4);
  f. every flash 1 to 12 lies within 4 standard errors of the exact Markov-chain value.

B2 Cosine law (steady light, sun fixed at 60 degrees elevation, blade tilted, photons counted in the stochastic run).
  a. at 0, 15, 30, 45, 60 degrees of incidence, absorbed photons / (absorbed at 0 x cos) lies within 0.95 to 1.05;
  b. at 80 degrees the same ratio is below 0.90 (the cuticle reflects more at grazing angles).

B3 Light response (steady light, midsummer leaf, light on the blade 25 to 2000 umol m-2 s-1).
  a. oxygen rate never falls by more than 3% as light rises;
  b. doubling light from 50 to 100 raises oxygen by more than 60%; doubling from 1000 to 2000 raises it by less than 15%;
  c. at 25 umol, oxygen per absorbed photon is between 0.100 and 0.125 (ceiling 1/8);
  d. every measured point is within 5% of the dead-time formula N(1-a)r / (1 + (1-a) r tau) / 4.

B4 Colour from pigments (no textures; this also checks my pigment coefficients, which are approximations).
  a. midsummer: light leaving the leaf (reflected + transmitted) at 550 nm is more than twice that at 450 nm and at 680 nm;
     reflected colour has G > R > B in linear sRGB;
  b. midsummer PAR-mean absorptance is between 0.78 and 0.90 (leaves measure about 0.84);
  c. chlorophyll gone, carotenoids present, no anthocyanin: reflected colour has R/G between 0.9 and 1.5 and B < 0.6 G (yellow);
  d. same with anthocyanin at 12 ug cm-2: R > 1.5 G (red);
  e. R + T + A = 1 and all three in [0,1] at every wavelength for 200 random pigment mixes;
  f. with scattering near zero the slab's transmittance equals exp(-K d) to 1 part in 1000 (Beer-Lambert limit).

B5 Venation (space colonisation, 5 seeds).
  a. the result is one tree: every node but the root has an earlier parent;
  b. 95% of 4000 random points in the blade lie within 0.03 leaf lengths of a vein;
  c. between 800 and 9000 nodes, and the whole growth computes in under 2 s here;
  d. the widest vein is at the base of the midrib (first segment).

B6 Season.
  a. chlorophyll never rises from 1 July to 20 November; b. carotenoid:chlorophyll ratio on 25 October is over 3 times that on 15 July;
  c. anthocyanin on 25 October with full light and cold nights is over 3 times that with a quarter of the light and mild nights.

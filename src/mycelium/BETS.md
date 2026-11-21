# Bets for mycelium.html, written before the model was first run

The model is a graph of strands on a 20 cm square of soil. Flow is solved on the graph (pressure at wood, leaks at growing
tips and at wood being colonised). Five things are timed by the same rule (a count builds from a signal the fungus supplies,
reaches a fixed threshold, something happens, the count restarts): a tip branching, a tip fusing with a strand it has come
close to, a strand gaining one more hypha because flow keeps passing, a strand losing one (or being withdrawn) because flow
does not, and a fruit body starting. Settings are those in the page's model script at the time of the run. Any change made
after a run is listed in RESULTS.md and the earlier output is kept.

Standard run: seed s in {1,2,3,4,5}; one inoculum block at (6,10); moisture 0.7; no other food; step 0.02 day.
"Contact" means the first strand reaching a new block. G(a,b) is the effective conductance between two blocks, found by a
separate solve with no leaks. Material M is the sum over strands of length times number of hyphae.
Efficiency E = G d^2 / (kappa M), d the centre distance; it is 1 for all material laid as one straight cord and cannot exceed 1.

B1 Loops. At day 12:
  a. with fusion switched off the cyclomatic number (edges - nodes + components) is 0 in 5 of 5 seeds;
  b. with fusion on it is at least 5 in 5 of 5 seeds.

B2 New food. At day 12 a wood block is placed centred 6 cm to the right of the inoculum centre, at (12,10).
  a. contact within 5 days of placing, 5 of 5 seeds;
  b. 10 days after contact, the widest path between the two blocks (the path whose thinnest strand is thickest) has a
     thinnest strand of at least 3 hyphae, and is no longer than 1.5 times the straight distance; 4 of 5 seeds;
  c. of the strand length present at contact that lay more than 3 cm from the straight line between the blocks, at least
     30% has been withdrawn 15 days after contact; 4 of 5 seeds;
  d. control: in the same seeds with no block placed, the share withdrawn of that same set over the same days is at least
     10 percentage points lower; 4 of 5 seeds.

B3 A cut. 15 days after contact every strand crossing a 4 cm line, set across the straight line between the blocks at its
   middle, is cut (discs of radius 0.45 cm along the line).
  a. G between the blocks just after the cut is under half of G just before; 4 of 5 seeds;
  b. 8 days later the blocks are connected and G is at least half of its value before the cut; 4 of 5 seeds;
  c. at least one new fusion has happened within 1.5 cm of the cut line in those 8 days; 4 of 5 seeds.

B4 Efficiency. E between inoculum and new block 20 days after contact is at least 1.5 times E one day after contact,
   4 of 5 seeds; and E never exceeds 1 at any sampled time in any seed.

B5 Branch timing. For each seed at day 30 of the standard run: report the coefficient of variation of the time between
   branchings (one full count of one tip) and the sample size. No target. My guess, which can fail: because the signal a tip
   receives varies a great deal across the colony, CV will lie between 0.3 and 1.2 in 5 of 5 seeds, that is, above the
   candidate value 1/(2 pi) = 0.159. Nothing will be changed to move it.

B6 Bookkeeping, checked on seed 1 over days 0 to 20 with the block of B2 placed at day 12.
  a. after a tight solve, the net current at every plain junction is under 1e-6 of the total leaving the wood;
  b. current leaving sources and reserves equals current entering sinks within 1e-6 of the total;
  c. after every step every count lies in [0, threshold).

B7 Moisture. With the block of B2 placed at day 12:
  a. at moisture 0.8 at least one fruit body has started by day 60; 4 of 5 seeds;
  b. at moisture 0.3 none has started by day 60; 5 of 5 seeds;
  c. total strand length at day 8 at moisture 0.2 is under 0.75 of that at moisture 0.7; 5 of 5 seeds.

B8 Dense near food, sparse far out. Standard run to day 14: branchings per cm of new strand grown within 3 cm of the
   inoculum centre is at least twice that beyond 5 cm; 4 of 5 seeds.

B9 Cost. Standard run with the block of B2, to day 60: mean time for one model step under 2 ms here; never more than
   6000 live nodes, 600 tips or 2500 cm of strand.

B10 The page. Desktop 1280x800, iPhone 13, and with WebGL off: no page errors and no console errors; at 390 px the page
   is no wider than the window; the day, length and loop figures on screen equal the model's own at the moment of reading.

# Murmuration: bets

Written before `test_murmuration.js` was first run. The model had already been run informally while it was being
built (to make the flock wheel over the roost instead of folding back on itself), so the author had seen
polarisation values of roughly 0.85 to 0.94 at seven neighbours before writing B1. B1 is therefore not a blind bet.
None of the other quantities had been measured when these were written.

All runs: dt = 1/60 s, default settings in `model.js`, "rule" = count-and-commit timing, "plain" = continuous steering.

- **B1 Order at seven neighbours.** N = 2000, 60 s, mean polarisation over the second half is at least 0.85,
  for 3 of 3 seeds, in both modes.
- **B2 One or two neighbours is not a flock.** N = 2000, 40 s, rule mode, 3 seeds each. With k = 1 the largest set of
  birds linked through who attends to whom holds under 10% of the birds and polarisation is under 0.6. With k = 2 the
  largest set holds under 60%. With k = 7 it holds at least 95%.
- **B3 Seven is enough.** Same runs at k = 1, 2, 3, 5, 7, 10, 12 (one seed). Polarisation at 12 exceeds polarisation at
  7 by less than 0.05.
- **B4 A turn started at one edge crosses the flock.** N = 1500, roost switched off, 12 s to settle. Then the 2% of
  birds furthest out on one side are held on a course 60 degrees toward their own side for 3 s. Bet: the quarter of the
  flock furthest from them turns by at least 20 degrees (mean heading) within 3 s of the start, in both modes.
  B4b: the same with 10% of birds. Same bet.
  Also measured, with no bet on the value: when each slice of the flock reaches half of its own final turn, and from
  that the speed of the front. Bet on the shape only: the front speed exceeds the flight speed (10 m/s), so the turn
  travels through the flock faster than the birds fly.
- **B5 One bird cannot do it.** As B4 with a single bird held off course. Bet: the far quarter turns by less than
  5 degrees within 3 s. (A bet that the flock ignores one bird.)
- **B6 Scale-free correlation.** N = 500, 1000, 2000, 4000, 40 s, rule mode. The correlation length (first zero of the
  correlation of heading fluctuations) divided by flock size L lies between 0.2 and 0.5 at every N, and the
  correlation length at 4000 is at least 1.5 times that at 500.
- **B7 What the timing rule changes.** (a) Mean polarisation in B1 differs between rule and plain by less than 0.05.
  (b) In B4b the turn reaches the far quarter later under the rule than under plain steering.
- **B8 The falcon.** N = 2000, falcon sent at 20 s, rule mode. (a) The largest linked set falls below 90% of birds at
  some time in the 15 s after launch (the flock splits). (b) It is back to at least 95% by 40 s after launch
  (the flock rejoins). (c) Birds that are never frightened themselves (the falcon is beyond their range at that moment)
  turn harder than before: their mean turn rate during the attack is at least 1.5 times its value in the 5 s before.
- **B9 Cost.** One step of 4000 birds takes under 4 ms in node on this machine (which is busy with other work).

No bet is made about any CRR constant. The interval between a bird's commits is reported (mean and coefficient of
variation) as a plain measurement.

## Amendments after the first run (`test_output_v1.txt`, kept)

Written after v1 and before v2. v1 results stand as they came out: B1 pass, B2 fail, B3 pass, B4 fail, B4b fail,
B5 fail, B6 fail, B7a pass, B8a pass, B8b pass, B8c fail, B9 fail.

What v1 showed was wrong with the tests and the model, and what was changed:

1. **B4 and B5 were confounded.** With the roost switched off the flock drifted and split by itself (in plain mode
   polarisation fell to 0.44), so "the far quarter turned" could not be told from the flock's own wandering: one bird
   appeared to turn the far quarter by 21 degrees. v2 keeps the roost on and measures every turn as the difference
   from an identical flock (same seed) in which no bird is held. Thresholds unchanged. N raised to 3000. The front is
   now timed by first arrival (a slice differs from the control by 3 degrees for a quarter of a second) instead of
   half of the final turn. The roost-off instability is real and is reported as a limit of the model.
2. **B2 as written was wrong about order.** With one neighbour the birds were no longer one linked set (0.6%), but
   polarisation stayed at 0.85, because the roost pulls every bird round the same way whether or not it has
   neighbours. With two neighbours 86 to 91% of birds were still linked. B2 is re-run unchanged and expected to fail
   again. A second form is added, **B2v2**: after 60 s the flock's rms radius at k = 1 is at least 1.5 times its
   radius at k = 7 (the flock thins out). This is not blind: informal runs of 30 s had shown roughly 13 to 19 m
   against 7 m.
3. **B8c could not be measured** because the fear radius (30 m) was larger than the flock, so no bird was out of the
   falcon's range. Model change: fear radius 15 m, flight response stronger (wf 3 to 5). "Not frightened" now means
   fear below 0.02. B8b is now read at exactly 40 s after launch (v1 took the first return to 95%, which came between
   the falcon's two passes).
4. **Model changes between v1 and v2**, made because birds wobbled at about 1 rad/s in calm flight: separation
   weight 0.5 to 0.3 and capped, damping ratio 0.5 to 0.7, noise 0.22 to 1.0, starting flock thinner.
   B1, B3, B6, B7, B9 are re-run with the thresholds as first written.

## Amendments after the second run (`test_output_v2.txt`, kept)

Written after v2 and before v3. v2 results stand: B1 pass, B2 fail, B2v2 fail (ratio 1.26), B3 pass, B4 fail, B4b fail,
B5 pass, B6 fail, B7a pass, B7b not measurable, B8a pass/fail (one seed each), B8b fail, B8c fail, B9 fail.

What v2 showed: **a turn seeded at the edge did not travel at all** (0 degrees at every slice beyond the first), in
either mode. The held birds simply flew away from the flock. Working it through: the alignment in the v2 model was
soft and heavily damped (response time 0.15 s, damping ratio 0.7), which makes a change of heading diffuse through the
flock at a few metres a second, slower than the birds fly. Attanasi et al. (2014) measured turns crossing real flocks
at 20 to 40 m/s with little damping, and the inertial spin model needs stiff alignment and weak damping to do that.

Model changes for v3 (exploratory runs of the turn test were made while choosing them, so B4 in v3 is not blind):
- alignment stiff and lightly damped: response time 0.045 s, damping ratio 0.2
- the timing rule's count runs faster to keep up (base rate 10 to 40 per second, neighbour mismatch gain 55 to 300,
  memory time 0.12 to 0.03 s), and each neighbour's contribution to a bird's count is now kept separately; when the
  bird commits, each neighbour is weighted by exp(its share of the count / Omega) with Omega = 1/Cstar
- the flock is less flattened (1.8 instead of 3), the roost lean is 0.7, the air has slow eddies that deform the
  flock, spacing 2.2 m, roost nearer the viewer. These were chosen for the look of the flock.

Expectation written down now: in the exploratory runs plain steering carried a pulse of turning across the flock in
about 2 s and the timing rule carried a weaker one. So I expect B7b to pass (the rule is later or weaker) and B4/B4b
as first written to fail still, because the turn is a passing pulse and is over by 3 s. v3 also reports the largest
turn of the far quarter within 4 s, as a measurement. All other thresholds stay as first written.
Without the roost the flock still spreads and splits (seen informally: polarisation 0.4 to 0.6 after 30 s). That is
a limit of the model and is not tested further.

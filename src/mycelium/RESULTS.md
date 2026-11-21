# Results (bets in BETS.md were written before the model was first run)

- test_output_v1.txt: first run. 14 of 19 model bets. Failed B1a, B2d, B4, B6a, B8.
- test_output_v2.txt / test_output.txt: final model. 14 of 19. Failed B1a, B2d, B3b, B4, B8.
- test_output_page.txt: B10 passed (desktop, iPhone 13, WebGL off). test_output_page_v1_harness_fault.txt is an earlier run in
  which the test clicked with a stale position after the page had scrolled and pressed "Begin again"; the page was not at fault.

Before the bets were run the model was tuned by eye and by printed totals (dev runs, not kept) so that it grew at all:
fusion range and rate, supply from wood, crowding, slower thinning of thick cords, the round patch, withdrawal running back
from free ends. Those were choices about the fungus, made without looking at any bet.

Changes between v1 and the final run, both made after seeing v1:
1. Fault: material taken back was fed in as a fixed current. A fragment cut off from everything then rose to pressures near
   a million, and the solver stopped converging (B6a: junction residual 3e-3). It is now offered at the pressure of fresh wood,
   so it cannot exceed that. B6a then held (3e-9).
2. New wood made a stronger sink while it is being colonised (gCol 60 to 300, colNeed 150 to 600). In v1 the new wood made
   no difference to how much thread was taken back (B2d 0 of 5). This is a change made in the direction of a failed bet and
   should be read that way. B2d is still a failure (3 of 5).
No other setting was changed after v1. Nothing was changed after v2.

Failures as they stand:
- B1a: 1 to 3 loops by day 12 with fusion off. Tips grow back into their own wood and join it. The bet was wrong about the
  model: fusion is not the only way it closes a loop.
- B2d: thread off the route taken back by +15 d: 80, 87, 81, 79, 82% with new wood; 61, 73, 72, 72, 65% without. Most of the
  taking back is crowding, the rim and the wood running down, not the new wood.
- B3b: conductance between the blocks 8 days after the cut, as a share of before: 0.29, 0.43, 0.58, 0.16, 0.31. Reconnection
  happens in every run (it was 0 or near 0 just after the cut) but slower than I bet.
- B4: economy E at +1 d against +20 d: 0.27/0.25, 0.22/0.22, 0.23/0.21, 0.28/0.24, 0.27/0.24; peaks of 0.31 to 0.42 in
  between. Contact is immediate (threads already lie under the wood), so "+1 d" is not an exploring phase, and later regrowth
  from the new wood adds material. E never exceeded 1.
- B8: branchings per cm near / far: ratios 1.95, 1.92, 1.97, 2.06, 2.08. I bet at least 2.

Reported, not bet on as a target: time between branchings, CV 0.454, 0.438, 0.468, 0.444, 0.476 (n = 404, 402, 386, 388, 416)
at day 30. The candidate value 1/(2 pi) = 0.159 is shown on the page for comparison only. Nothing was tuned towards it.

Not checked: frame rate on real hardware (only software WebGL here, several seconds a frame); the look on a real phone;
every reference (all cited from memory). Software WebGL logs a driver performance warning ("GPU stall due to ReadPixels")
when the strand picture is uploaded; it is a warning, not an error.

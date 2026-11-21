# Bets for forest.html (written before any check was run)

Each bet states what counts as a pass. Results are appended by the test scripts to `results-*.txt` in this folder; failed outputs are kept.

B1. Festival table. For 2026 and 2027, each of the ten movable feasts in `MOV` comes out of `generateYearEvents(year)` on exactly the month and day in the table, with no "(about)". In 2028 (no table) the same ten names carry "(about)". Pass: 20 of 20 equal, 10 of 10 marked.

B2. Computed feasts. Easter 2027 is 28 March. Easter 2026 is 5 April. US Thanksgiving 2026 is 26 November; 2027 is 25 November. Pass: all four.

B3. Sun. At longitude 0, for latitudes -35, 0, 35, 52, 60 and the 15th of every month of 2026: altitude at 00:00 UTC is below 0, and the highest altitude of the day (1-minute scan) falls within 20 minutes of 12:00 UTC. At London (51.5 N, 0.1 W) the altitude at 12:00 UTC is within 0.5 degrees of 61.9 on 21 June 2026 and of 15.1 on 21 December 2026. Pass: all.

B4. Moon. Elongation from the sun is under 3 degrees at 2026-08-12 17:46 UTC (a solar eclipse) and over 177 degrees at 2026-03-03 11:34 UTC (a lunar eclipse). Pass: both.

B5. Tree structure. For three grown trees: at every node the pipe rule holds (parent radius^n equals the sum of child radius^n, relative error under 1e-4); no child is thicker than its parent; trunk diameter is between 1/50 and 1/15 of tree height; node count between 1,500 and 16,000. Pass: all.

B6. Leaf calendar (northern unless stated). 15 Jan cover < 0.08. 15 Apr cover between 0.1 and 0.9. 1 Jul cover > 0.95 and turn = 0. 20 Oct turn > 0.5 and cover > 0.3. 21 Nov cover between 0.02 and 0.3. At latitude -35 on 15 Jan cover > 0.95. Pass: all.

B7. Frame cost, model only. Mean time of one `FOREST.step` (walkers, dogs, birds, leaves; full daytime crowd, autumn, wind 0.6) over 20,000 steps at dt = 1/60 s is under 0.10 ms. Pass: mean < 0.10 ms.

B8. Frame cost, drawing. In the browser, averaged over at least 5 animation frames of a full scene (autumn afternoon, leaves falling, birds, walkers): exactly 1 WebGL draw call per frame; 0 gradient objects created per frame; at most 220 Canvas 2D fill/stroke/drawImage calls per frame; at most 2,500 Canvas 2D method calls per frame in total. The old page is measured the same way for comparison; bet that the new page makes at most one quarter of the old page's 2D method calls per frame. Pass: all five.

B9. Timing rule. Over two simulated hours of daytime walking, at least one pause happens and no party's count is ever outside [0, 1) after a step. Over ten simulated minutes on 25 October at wind 0.5 at least one leaf is released; over ten minutes on 1 July none is. Pass: all.

B10. Robustness. With geolocation denied, with the weather request failing, and with no WebGL, the page raises no page errors and no console errors, and still shows the clock and three events. Pass: zero errors in each case.

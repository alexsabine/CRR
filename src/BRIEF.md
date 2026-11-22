# Brief for rebuilding a simulation on alexander sabine's site

You are rebuilding ONE simulation as a single self-contained HTML page in `/home/user/temporalgrammar/`. Read this whole brief first.

## Who it is for
Alexander Sabine: educator (early years to higher education), simulation designer, researcher. The site's idea is *Being and Becoming*. His touchstones are Blake, Eliot, Winnicott. Pedagogy matters most to him. Visitors are students, teachers, scientists and curious people, often on a phone.

## Look (match the existing pages exactly in spirit)
Read these first for quality, conventions and tone: `index.html` (the hero shader, windows, stitched figure), `fish-tank.html`, `duet.html`, `growing-up.html`, `workshop.html`.
- Palette: paper `#fffdf8`, wash `#f8f3e4`, ink `#14202a`, soft `#4d5a61`, hairline `#d9cfae`, gold `#b98619`, gold leaf `#e0ae35`, viridian `#0d7a70`, deep viridian `#0a5651`.
- Type: headings and quotations in "IM Fell English" (italic for verse), labels in "IM Fell English SC" with letter-spacing, body "Source Serif 4". Load from Google Fonts as the other pages do.
- Square corners everywhere (`border-radius:0`). Hairline borders. Pictures sit in a "plate": 1px hairline border with a gold inner rule (see `.plate` in `duet.html`).
- The simulation itself should be the most beautiful thing you can make: physically plausible light, real materials, depth, restraint. Subtle, not showy. Photoreal where the subject allows; where a painterly look is asked for, make it painterly on purpose.
- A small link top-left: `<a href="workshop.html">← The workshop</a>` styled like `.home` in `duet.html`.
- Very few words on the page. One title, one italic line, short control labels, and an About section or sheet.

## Words
Plain British English. Short sentences. No hype. Never mention AI, Claude, any model name, or "simulation built with". No em-dash asides, no rhetorical flourishes. Say what the model shows, what to try, and what it leaves out.

## CRR: what it is, technically, and how to use it
CRR (Coherence, Rupture, Regeneration) is Alexander's research programme on temporality. Use it for what it is and do not make a thing of it.
- **Coherence C**: a running count, since the last event, of accumulated change. Technically: Fisher–Rao arc length travelled on a chosen statistical carrier, divided by a resolution σ that must be fixed independently. In a simulation: integrate a non-negative rate L(t) that the *domain* supplies (prediction error, photons absorbed, mismatch with neighbours, growth signal).
- **Rupture**: a first-passage event. The cut happens the first time the count reaches a fixed threshold C* (convention C*·Ω = 1; Ω = 1/π for two-state "Z2" systems, 1/2π for rotational "SO(2)" systems are the programme's candidate values, not established constants). After the cut the count restarts at zero.
- **Regeneration**: what comes next is rebuilt from the past, with a past-only memory update (for example a Kalman-style seed update m' = m + K(arrives − m)), or a weighting exp(C/Ω) over contributions. This kernel is a modelling choice.
- CRR fixes the *timing grammar* (count, threshold, restart, weighted past). It does NOT supply the dynamics: the flow, the metric, the rates and the biology or physics come from the domain and must be real, cited science.
- Status: under investigation. Some tests hold, some fail. Never write that CRR "predicts", "explains" or "is confirmed by" anything. If the old page displays a "CRR prediction" (for example CV = Ω/2 ≈ 0.159) keep it only as a stated candidate value next to the value actually measured in the run, and never tune the model to make them match.
- On the page, CRR gets at most two plain sentences in About ("The timing rule here is ..."). The page is about the leaf, the birds, the tree, the bees.

## Science and honesty rules (non-negotiable)
- Use real, established biology, physics and mathematics for the dynamics. Cite sources by author and year in About. If you cite from memory, add "(cited from memory; check)".
- Before running any numerical check, write the bet (the threshold that would count as pass or fail) in a test file. Then run it and report the result as it came out, including failures. Keep failed outputs.
- Every number shown on screen must be measured from the run or clearly labelled as a setting. No decorative numbers. No estimated counts presented as counts.
- About must have: what is known (cited), the rule used here, what is left out.

## Engineering
- One self-contained `.html` file (inline CSS and JS). If you need three.js use exactly `<script src="https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.min.js"></script>`. Plain WebGL or Canvas 2D are fine and often better. No other external scripts. No build step.
- Keep the model (no drawing) in functions that can be run without rendering, exposed on `window` for tests.
- Must work at 390 px wide with no horizontal scroll, touch targets at least 44 px, visible focus rings, `prefers-reduced-motion` respected, canvases with a text alternative (`aria-label`). Pause work when the tab is hidden or the canvas is off screen. Cap device pixel ratio at 2 (1.5 on small screens). Adapt quality if frames are slow. It must feel smooth on an ordinary laptop and run on a phone.
- Sound only after a user gesture, with a clear on/off control.
- Do not use localStorage for anything essential.

## Testing (do this; do not skip looking at the pictures)
Playwright and Chromium are installed (`require('playwright')` works anywhere). WebGL needs these launch args: `['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']`. If you load three.js, route the CDN URL to the local copy in tests: `page.route('**/three.min.js', r => r.fulfill({ body: fs.readFileSync('/home/user/Phoenix-1-/MUSEUM/studio/vendor/three-0.158.0.min.js','utf8'), contentType:'application/javascript' }))`. Images used as WebGL textures taint on `file://`; serve over a tiny local http server if you need that.
- Capture `pageerror` and console errors (shader compile errors show there). Zero errors required.
- Take screenshots at 1280×800 and with `devices['iPhone 13']`, and READ them with the Read tool. Fix what looks wrong. Iterate until it is genuinely beautiful.
- The machine is also rendering video, so software WebGL is slow (several seconds a frame). Be patient; use `waitForTimeout` generously. Do not conclude it is slow in real browsers from this; instead reason about draw calls, overdraw and loop costs.
- Put test scripts and screenshots in your own folder under `/tmp/claude-0/-home-user/1edd5cc0-6987-5771-b57b-68d2ef3dbc39/scratchpad/` (make a subfolder named after your piece). Put bet files and outputs in `/home/user/temporalgrammar/src/<piece>/`.

## Boundaries
- Write only your own new page, and files under `src/<piece>/`. Do not edit, move or delete any other file. Do not run git commit or git push. Do not start servers that outlive your tests.
- Finish with a short report: file written, what it does, the bets and their results (including failures), what is cited from memory, what you could not check, and the paths of two or three final screenshots.

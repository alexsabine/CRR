# The Wall and the Beach (draft, not linked from the site)

A film on doing, remembering and dreaming. Fifth cut, 11 min 17, 27 November 2026.

- `the-wall-and-the-beach.mp4`: the current cut.
- `src/`: everything needed to rebuild it. `script.json` is the narration; `voice.py` speaks it and writes `timing.json`; `film7.py` draws the frames; `song7.py` writes the score; `cut.py` joins picture, subtitles, score and voice.
- `sim.py` is the sand simulation (run `python3 sim.py 21.5` to remake `sand.npz`, left out here for size). `maths.py`, `maths2.py` and `check.py` are the small simulations behind the curves and the second jigsaw.
- `wall-soft.jpg` is the photograph with the children softened. The unblurred original is not kept here.
- Earlier narrations are kept as `script_v1.json` to `script_v4.json`.

The scripts expect the IM Fell fonts and the Piper voice used when the film was made; their paths are at the top of `film7.py` and `voice.py`.

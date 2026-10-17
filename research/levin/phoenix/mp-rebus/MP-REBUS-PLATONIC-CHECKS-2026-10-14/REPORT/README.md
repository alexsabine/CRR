# REPORT

`SORTING_ARRAYS_REPORT_2026-10-14.md` is the source; `SORTING_ARRAYS_REPORT_2026-10-14.pdf` is built from it with `pandoc --mathml` and headless Chromium (`--print-to-pdf`), styled by `report.css`. Rebuild:

```
pandoc SORTING_ARRAYS_REPORT_2026-10-14.md -s --mathml --css report.css --embed-resources -o report.html
chromium --headless --no-sandbox --no-pdf-header-footer --print-to-pdf=SORTING_ARRAYS_REPORT_2026-10-14.pdf report.html
```

Status: R4 / new replication; grade DESCR; one operator; no second-person review. The literature sections (§7) rest on two same-day sweeps and should be checked against the originals before citation in print.

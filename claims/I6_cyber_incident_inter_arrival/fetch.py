"""
I6 — Fetch script.

Fetches VERIS Community Database (VCDB) CSV from canonical
GitHub mirror at vz-risk/VCDB. The .zip is ~15 MB; unzipped CSV
is ~172 MB and contains 13,225 incident rows × 2640 VERIS schema
columns.

Run: python fetch.py
Output: vcdb.csv (large, .gitignored).
"""
from __future__ import annotations
import urllib.request
import zipfile
import pathlib

URL = "https://raw.githubusercontent.com/vz-risk/VCDB/master/data/csv/vcdb.csv.zip"
DIR = pathlib.Path(__file__).parent
ZIP = DIR / "vcdb.csv.zip"
CSV = DIR / "vcdb.csv"


def main() -> None:
    print(f"Fetching {URL}")
    urllib.request.urlretrieve(URL, ZIP)
    print(f"Wrote {ZIP} ({ZIP.stat().st_size:,} bytes)")
    with zipfile.ZipFile(ZIP) as z:
        # The zip contains both vcdb.csv and data/dbir/VCDB/data/csv/vcdb.csv;
        # extract only the top-level vcdb.csv.
        for name in z.namelist():
            if name == "vcdb.csv":
                with z.open(name) as src, CSV.open("wb") as dst:
                    dst.write(src.read())
                break
    print(f"Extracted {CSV} ({CSV.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

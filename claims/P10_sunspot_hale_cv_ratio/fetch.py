"""
P10 — Fetch script.

Fetches SILSO V2 monthly mean total sunspot number from a public
GitHub mirror of the canonical SILSO file 'SN_m_tot_V2.0.csv'
(originally hosted at https://www.sidc.be/SILSO/datafiles, which
is not reachable from this sandbox).

The mirror is a verbatim copy of the SILSO file. Anyone with
direct SIDC access should re-fetch from sidc.be and verify byte
equality before relying on this file for publication.

Run: python fetch.py
Output: SN_m_tot_V2.0.csv (semicolon-separated; SILSO V2 schema).
"""
from __future__ import annotations
import urllib.request
import pathlib

URL = (
    "https://raw.githubusercontent.com/"
    "Shivayk0505/Forecasting-of-Sunspot-Numbers-Time-Series-Data/"
    "main/SN_m_tot_V2.0.csv"
)
OUT = pathlib.Path(__file__).parent / "SN_m_tot_V2.0.csv"


def main() -> None:
    print(f"Fetching {URL}")
    urllib.request.urlretrieve(URL, OUT)
    n = sum(1 for _ in OUT.open())
    print(f"Wrote {OUT} ({n} rows)")


if __name__ == "__main__":
    main()

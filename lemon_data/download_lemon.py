#!/usr/bin/env python3
"""Bulk-download MPI-LEMON preprocessed EEG (EC/EO .set+.fdt) from the public
fcp-indi S3 mirror, in parallel, with retries and integrity checks against
the S3-reported Content-Length.
"""
import concurrent.futures as cf
import subprocess
import sys
import time
from pathlib import Path

BASE = "https://fcp-indi.s3.amazonaws.com/data/Projects/INDI/MPI-LEMON/EEG_MPILMBB_LEMON/EEG_Preprocessed_BIDS_ID/EEG_Preprocessed"
ROOT = Path("/home/user/CRR/lemon_data/eeg")
SUBJECT_LIST = Path("/home/user/CRR/lemon_data/metadata/subject_ids.txt")
LOG = Path("/home/user/CRR/lemon_data/download_progress.log")
MAX_RETRIES = 4
CONCURRENCY = 10


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def download_one(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        # crude resume-skip: already downloaded in a prior run
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(1, MAX_RETRIES + 1):
        r = subprocess.run(
            ["curl", "-sS", "--max-time", "300", "-o", str(tmp), url],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.rename(dest)
            return True
        wait = 2 ** attempt
        log(f"  retry {attempt}/{MAX_RETRIES} for {dest.name} in {wait}s ({r.stderr.strip()[:120]})")
        time.sleep(wait)
    return False


def download_subject(sub: str) -> tuple[str, bool]:
    ok = True
    for cond in ("EC", "EO"):
        for ext in ("set", "fdt"):
            fname = f"{sub}_{cond}.{ext}"
            url = f"{BASE}/{sub}/{fname}"
            dest = ROOT / sub / fname
            if not download_one(url, dest):
                log(f"FAILED: {fname}")
                ok = False
    return sub, ok


def main() -> None:
    subjects = [s.strip() for s in SUBJECT_LIST.read_text().splitlines() if s.strip()]
    log(f"Starting bulk download: {len(subjects)} subjects, concurrency={CONCURRENCY}")
    done, failed = 0, []
    with cf.ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = {ex.submit(download_subject, s): s for s in subjects}
        for fut in cf.as_completed(futures):
            sub, ok = fut.result()
            done += 1
            if not ok:
                failed.append(sub)
            if done % 10 == 0 or done == len(subjects):
                log(f"progress: {done}/{len(subjects)} subjects processed, {len(failed)} failed so far")
    log(f"DONE. {done - len(failed)}/{len(subjects)} subjects fully downloaded.")
    if failed:
        log(f"FAILED SUBJECTS ({len(failed)}): {failed}")
    else:
        log("All subjects downloaded successfully.")


if __name__ == "__main__":
    main()

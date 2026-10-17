# Shared helpers for the run.sh scripts in this area (sourced, not executed). MIT; see ../LICENSE.
# Nothing here edits a frozen file: every run works on a staged copy under $WORK, so the folders you
# downloaded stay byte-identical and can be checked with `python3 _shared/verify_hashes.py` at any time.

SHARED="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0

say() { printf '\n== %s\n' "$*"; }

# stage <study_dir> <work_dir> phoenix|ashes
#   Copies <study_dir>/src/ to <work_dir>, then the shared files the frozen code expects beside it:
#   phoenix -> scripts/guard.py, scripts/seen_register.py, DATA/SEEN.md, EPISTEMIC/FREEZE_LEDGER.jsonl
#   ashes   -> pyproject.toml, uv.lock, .python-version, src/crr/, data/fetch_*.py
#   Refuses to reuse a non-empty work dir, because some runners skip units whose output already exists.
stage() {
  local study="$1" work="$2" kind="$3"
  if [ -e "$work" ] && [ -n "$(ls -A "$work" 2>/dev/null | grep -v '^\.venv$' || true)" ]; then
    echo "refusing: $work is not empty (a resumable runner would skip finished units). Remove it or set WORK=<new dir>." >&2; exit 2
  fi
  mkdir -p "$work"; cp -a "$study/src/." "$work/"
  case "$kind" in
    phoenix) cp -a "$SHARED/phoenix/." "$work/" ;;
    ashes)   cp -a "$SHARED/ashes/." "$work/" ;;
  esac
  python3 -B "$SHARED/verify_hashes.py" "$study" >/dev/null || { echo "frozen files differ from their recorded hashes; stop" >&2; exit 3; }
}

# pyenv <requirements.txt> : sets $PY. Uses $PYTHON if given (an interpreter that already has the packages),
# else creates $VENV (default $WORK/.venv) with $BASE_PYTHON (default python3.11, the recorded version) and pip-installs.
pyenv() {
  if [ -n "${PYTHON:-}" ]; then PY="$PYTHON"; return; fi
  local base="${BASE_PYTHON:-python3.11}"; command -v "$base" >/dev/null || base=python3
  VENV="${VENV:-$WORK/.venv}"
  if [ ! -x "$VENV/bin/python" ]; then "$base" -m venv "$VENV"; "$VENV/bin/pip" install -q --upgrade pip; fi
  "$VENV/bin/pip" install -q -r "$1"
  PY="$VENV/bin/python"; "$PY" -c 'import sys; print("python", sys.version.split()[0])'
}

# same <produced> <expected> : byte comparison with a one-line verdict (non-zero exit only at the end of run.sh)
MISMATCH=0
same() {
  if cmp -s "$1" "$2"; then echo "MATCH   $(basename "$2")"; else echo "DIFFERS $(basename "$2")  (produced: $1)"; MISMATCH=1; fi
}
finish() {
  if [ "$MISMATCH" = 0 ]; then say "all compared outputs match expected/ (byte for byte unless the line says otherwise)"; else say "some outputs differ from expected/ (see above)"; exit 1; fi
}

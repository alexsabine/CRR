"""Pytest path setup.

The canonical engine lives at crr-engine/index.py; the hyphen blocks Python
import-as-package, so we expose `index` directly by inserting the engine
directory on sys.path.
"""

import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent.parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

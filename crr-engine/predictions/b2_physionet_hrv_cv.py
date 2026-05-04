"""b2_physionet_hrv — pre-registered prediction reviewer-run skeleton.

Pre-registration locked at git commit 3fc9681 in the corresponding
claims/<id>/prediction.md.

[REVIEWER-RUN] Sandbox blocks the upstream data host. Reviewer
runs against pre-specified public datasets per prediction.md.
"""
import sys


def main() -> int:
    print("b2_physionet_hrv skeleton.")
    print("See claims/<id>/prediction.md for pre-registered protocol,")
    print("data target, quantitative band, and falsifier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

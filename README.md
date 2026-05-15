# Zone-of-Avoidance Foreground-Screen Audit

This repository is the public reproducibility package for:

**Milky Way foreground-screen stratification in a SPARC/HECATE residual audit: a Zone-of-Avoidance motivated method note**

The package follows the Paper 1 public-repository style: a small, reproducible
packet with a narrow claim boundary, derived evidence tables, source manifests,
tests, and a draft manuscript.

## Main Claim Boundary

The repository does **not** claim a physical detection of a new force, a
replacement for standard galaxy dynamics, or a proof of any private parent
theory.

It only records this reproducible diagnostic:

```text
Using HECATE positions for exact-name SPARC overlaps, the low-Galactic-latitude
foreground-screen proxy |b| <= 24 deg selects 18 galaxies. In the reviewed A/C
subset this screen is C-dominant: A=1, C=6, with 11 ambiguous B systems.
```

This is an observer-screen / selection-audit result. It is interesting because
Zone-of-Avoidance studies show that the Milky Way foreground is a real
observational layer, but the present SPARC/HECATE diagnostic is not yet a
paper-grade physical inference.

## Motivating External Paper

Nilo-Castellon et al. report that Galactic extinction, stellar crowding, and
confusion noise limit background-galaxy detection in the Zone of Avoidance, and
that JWST/NIRCam can reveal faint galaxies through heavily contaminated Milky
Way regions:

```text
Faint galaxies in the Zone of Avoidance revealed by JWST/NIRCam
J. L. Nilo-Castellon et al.
arXiv:2510.12488
https://arxiv.org/abs/2510.12488
```

## Reproduce

Install the package and regenerate the packet:

```bash
python -m pip install -e .
python studies/zoa_foreground_screen_audit_v01/make_foreground_screen_packet.py
PYTHONPATH=src python -m pytest -q
```

The script downloads HECATE v1.1 if it is missing locally, computes Galactic
coordinates from RA/DEC, joins the Paper 1 class labels, and writes the packet:

```text
studies/zoa_foreground_screen_audit_v01/paper_packet_v01/
```

## Included Evidence

```text
outputs/hecate_crossmatch_summary.csv
studies/zoa_foreground_screen_audit_v01/coherence_labels_v06_distance_balanced.csv
studies/zoa_foreground_screen_audit_v01/paper_packet_v01/foreground_screen_audit_table.csv
studies/zoa_foreground_screen_audit_v01/paper_packet_v01/foreground_screen_threshold_scan.csv
studies/zoa_foreground_screen_audit_v01/paper_packet_v01/foreground_screen_summary.csv
```

Raw HECATE is downloaded on demand and remains untracked.

## Scope

This is a standalone public method note. It deliberately avoids private theory
machinery and keeps the result framed as a foreground-screen audit.

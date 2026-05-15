# Data Notice

This repository contains derived audit artifacts and source manifests.

It does not redistribute the full HECATE raw catalog. The audit script downloads
the public HECATE v1.1 CSV into `data/external/raw/hecate/` when needed. That
path is intentionally excluded from git.

The included SPARC class labels and HECATE crossmatch summary are public
derived artifacts inherited from the Paper 1 reproducibility package:

`sparc-residual-disturbance-paper1`

The included `outputs/sparc_residual_summary.csv` is also a derived public
artifact from that package. It is used only for the residual-signal stress test
and does not contain raw SPARC rotation-curve files.

The foreground-screen audit is a selection/observability diagnostic. It is not
a claim that low Galactic latitude physically causes galaxy disturbance.

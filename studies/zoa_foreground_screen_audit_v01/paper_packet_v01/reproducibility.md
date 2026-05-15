# Reproducibility

Run:

```bash
python studies/zoa_foreground_screen_audit_v01/make_foreground_screen_packet.py
PYTHONPATH=src python -m pytest -q
```

The script downloads HECATE v1.1 into an untracked raw-data path if necessary,
computes Galactic coordinates, and rebuilds all packet tables.

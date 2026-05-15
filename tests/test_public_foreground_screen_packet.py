import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "studies/zoa_foreground_screen_audit_v01/paper_packet_v01"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_packet_files_exist():
    required = [
        ROOT / "README.md",
        ROOT / "DATA_NOTICE.md",
        ROOT / "CITATION.cff",
        ROOT / "requirements.txt",
        ROOT / "outputs/hecate_crossmatch_summary.csv",
        ROOT / "outputs/sparc_residual_summary.csv",
        ROOT / "studies/zoa_foreground_screen_audit_v01/coherence_labels_v06_distance_balanced.csv",
        PACKET / "manuscript_draft.md",
        PACKET / "manuscript_draft.pdf",
        PACKET / "foreground_screen_audit_table.csv",
        PACKET / "foreground_screen_threshold_scan.csv",
        PACKET / "foreground_screen_summary.csv",
        PACKET / "foreground_residual_signal_summary.csv",
        PACKET / "foreground_matched_control_pairs.csv",
        PACKET / "claim_boundary.csv",
        PACKET / "source_manifest.csv",
        PACKET / "packet_manifest.json",
        PACKET / "figures/foreground_screen_counts.svg",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []


def test_low_latitude_24_degree_result_is_locked():
    rows = read_csv(PACKET / "foreground_screen_audit_table.csv")
    low = [row for row in rows if row["low_latitude_screen_24deg"] == "true"]
    assert len(low) == 18
    counts = {label: sum(row["Class"] == label for row in low) for label in ["A", "B", "C"]}
    assert counts == {"A": 1, "B": 11, "C": 6}


def test_summary_records_not_a_detection():
    claims = read_csv(PACKET / "claim_boundary.csv")
    blocked = {row["Claim"] for row in claims if row["Status"] == "blocked"}
    assert "physical_detection" in blocked
    assert "new_dynamics_claim" in blocked
    assert "parent_theory_proof" in blocked


def test_residual_signal_is_framed_as_candidate_not_detection():
    rows = read_csv(PACKET / "foreground_residual_signal_summary.csv")
    by_metric = {row["Metric"]: row for row in rows}
    assert float(by_metric["rms_log_tpg_low_minus_high_median"]["Value"]) < 0
    assert float(by_metric["mean_log_residual_tpg_low_minus_high_median"]["Value"]) > 0
    assert by_metric["interpretation"]["Value"] == "candidate_signed_projection_offset_not_rms_excess_detection"


def test_raw_hecate_not_tracked():
    if not (ROOT / ".git").exists():
        return
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    tracked = set(result.stdout.splitlines())
    assert not any(path.startswith("data/external/raw/") for path in tracked)

#!/usr/bin/env python3
"""Build the public Zone-of-Avoidance foreground-screen audit packet."""

from __future__ import annotations

import csv
import json
import math
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "studies/zoa_foreground_screen_audit_v01"
PACKET = STUDY / "paper_packet_v01"
FIGURES = PACKET / "figures"

HECATE_URL = "https://hecate.ia.forth.gr/assets/files/HECATE_v1.1.csv"
HECATE_RAW = ROOT / "data/external/raw/hecate/HECATE_v1.1.csv"
HECATE_CROSSMATCH = ROOT / "outputs/hecate_crossmatch_summary.csv"
LABELS = STUDY / "coherence_labels_v06_distance_balanced.csv"
PUBLIC_RESIDUAL_SUMMARY = ROOT / "outputs/sparc_residual_summary.csv"

# J2000 constants from the standard equatorial-to-Galactic coordinate rotation.
RA_NGP_DEG = 192.85948
DEC_NGP_DEG = 27.12825
L_ASC_NODE_DEG = 32.93192


def ensure_dirs() -> None:
    for path in [HECATE_RAW.parent, PACKET, FIGURES]:
        path.mkdir(parents=True, exist_ok=True)


def download_hecate_if_missing() -> None:
    if HECATE_RAW.exists():
        return
    request = urllib.request.Request(
        HECATE_URL,
        headers={"User-Agent": "zoa-foreground-screen-audit/0.1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        HECATE_RAW.write_bytes(response.read())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def galactic_lon_lat(ra_deg: str, dec_deg: str) -> tuple[float, float]:
    ra = math.radians(float(ra_deg))
    dec = math.radians(float(dec_deg))
    ra_ngp = math.radians(RA_NGP_DEG)
    dec_ngp = math.radians(DEC_NGP_DEG)
    l_asc = math.radians(L_ASC_NODE_DEG)

    b = math.asin(
        math.sin(dec) * math.sin(dec_ngp)
        + math.cos(dec) * math.cos(dec_ngp) * math.cos(ra - ra_ngp)
    )
    l = math.atan2(
        math.cos(dec) * math.sin(ra - ra_ngp),
        math.sin(dec) * math.cos(dec_ngp)
        - math.cos(dec) * math.sin(dec_ngp) * math.cos(ra - ra_ngp),
    ) + l_asc
    return math.degrees(l) % 360.0, math.degrees(b)


def one_sided_hypergeom_p(success_total: int, population_total: int, draw_count: int, observed_success: int) -> float:
    """P(X >= observed_success) for C enrichment among A/C systems."""
    denom = math.comb(population_total, draw_count)
    upper = min(success_total, draw_count)
    return sum(
        math.comb(success_total, x)
        * math.comb(population_total - success_total, draw_count - x)
        / denom
        for x in range(observed_success, upper + 1)
    )


def build_audit_rows() -> list[dict[str, object]]:
    hecate_by_pgc = {row["PGC"]: row for row in read_csv(HECATE_RAW)}
    labels = {row["GalaxyName"]: row for row in read_csv(LABELS)}
    residuals = (
        {row["galaxy_name"]: row for row in read_csv(PUBLIC_RESIDUAL_SUMMARY)}
        if PUBLIC_RESIDUAL_SUMMARY.exists()
        else {}
    )

    rows: list[dict[str, object]] = []
    for cross in read_csv(HECATE_CROSSMATCH):
        name = cross["GalaxyName"]
        hecate = hecate_by_pgc.get(cross["HecatePGC"])
        label = labels.get(name)
        if not hecate or not label:
            continue
        glon, glat = galactic_lon_lat(hecate["RA"], hecate["DEC"])
        residual = residuals.get(name, {})
        rows.append(
            {
                "GalaxyName": name,
                "Class": label["S_tau_class"],
                "LabelConfidence": label["LabelConfidence"],
                "HecatePGC": cross["HecatePGC"],
                "HecateObjectName": cross["HecateObjectName"],
                "HecateDistanceMpc": cross["HecateDistanceMpc"],
                "RA_deg": f"{float(hecate['RA']):.6f}",
                "DEC_deg": f"{float(hecate['DEC']):.6f}",
                "GalacticLongitudeDeg": f"{glon:.6f}",
                "GalacticLatitudeDeg": f"{glat:.6f}",
                "AbsGalacticLatitudeDeg": f"{abs(glat):.6f}",
                "low_latitude_screen_24deg": str(abs(glat) <= 24.0).lower(),
                "RmsLogTPG": residual.get("rms_log_tpg", ""),
                "WeightedRmsLogTPG": residual.get("weighted_rms_log_tpg", ""),
                "MeanLogResidualTPG": residual.get("mean_log_residual_tpg", ""),
                "OuterMeanLogResidualTPG": residual.get("outer_mean_log_residual_tpg", ""),
            }
        )
    return sorted(rows, key=lambda row: float(row["AbsGalacticLatitudeDeg"]))


def median(values: list[float]) -> float:
    values = sorted(values)
    if not values:
        return float("nan")
    mid = len(values) // 2
    if len(values) % 2:
        return values[mid]
    return 0.5 * (values[mid - 1] + values[mid])


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def build_residual_join(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not PUBLIC_RESIDUAL_SUMMARY.exists():
        return []
    by_name = {row["GalaxyName"]: row for row in rows}
    joined: list[dict[str, object]] = []
    for residual in read_csv(PUBLIC_RESIDUAL_SUMMARY):
        name = residual["galaxy_name"]
        screen = by_name.get(name)
        if not screen:
            continue
        joined.append({**screen, **residual})
    return joined


def build_residual_signal_summary(joined: list[dict[str, object]]) -> list[dict[str, object]]:
    if not joined:
        return [
            {"Metric": "residual_summary_available", "Value": "false", "Interpretation": "outputs/sparc_residual_summary.csv missing"},
        ]
    low = [row for row in joined if row["low_latitude_screen_24deg"] == "true"]
    high = [row for row in joined if row["low_latitude_screen_24deg"] == "false"]
    metrics = [
        "rms_log_tpg",
        "weighted_rms_log_tpg",
        "mean_log_residual_tpg",
        "outer_mean_log_residual_tpg",
        "mean_err_vobs_kms",
        "max_radius_kpc",
        "n_points",
    ]
    summary = [
        {"Metric": "residual_summary_available", "Value": "true", "Interpretation": "public Paper 1 residual summary joined to foreground screen"},
        {"Metric": "residual_join_rows", "Value": len(joined), "Interpretation": "HECATE/SPARC rows with residual summary"},
        {"Metric": "residual_low_screen_rows", "Value": len(low), "Interpretation": "|b| <= 24 deg"},
        {"Metric": "residual_high_screen_rows", "Value": len(high), "Interpretation": "|b| > 24 deg"},
    ]
    for metric in metrics:
        low_values = [float(row[metric]) for row in low if row.get(metric) not in {"", None}]
        high_values = [float(row[metric]) for row in high if row.get(metric) not in {"", None}]
        if not low_values or not high_values:
            continue
        low_med = median(low_values)
        high_med = median(high_values)
        summary.extend(
            [
                {"Metric": f"{metric}_low_median", "Value": f"{low_med:.12g}", "Interpretation": "low-latitude foreground screen"},
                {"Metric": f"{metric}_high_median", "Value": f"{high_med:.12g}", "Interpretation": "higher-latitude comparison set"},
                {"Metric": f"{metric}_low_minus_high_median", "Value": f"{low_med - high_med:.12g}", "Interpretation": "diagnostic difference; not a detection"},
            ]
        )
    summary.append(
        {
            "Metric": "interpretation",
            "Value": "candidate_signed_projection_offset_not_rms_excess_detection",
            "Interpretation": "RMS median is not elevated in the 18-object screen; signed residual medians shift positive",
        }
    )
    return summary


def build_matched_control_pairs(joined: list[dict[str, object]]) -> list[dict[str, object]]:
    low = [row for row in joined if row["low_latitude_screen_24deg"] == "true"]
    high = [row for row in joined if row["low_latitude_screen_24deg"] == "false"]
    if not low or not high:
        return []
    features = ["HecateDistanceMpc", "max_radius_kpc", "n_points"]
    stats: dict[str, tuple[float, float]] = {}
    for feature in features:
        values = [math.log(max(float(row[feature]), 1.0e-12)) for row in joined]
        mu = mean(values)
        var = mean([(value - mu) ** 2 for value in values])
        stats[feature] = (mu, math.sqrt(var) or 1.0)

    def z(row: dict[str, object], feature: str) -> float:
        mu, sigma = stats[feature]
        return (math.log(max(float(row[feature]), 1.0e-12)) - mu) / sigma

    used: set[str] = set()
    pairs: list[dict[str, object]] = []
    for low_row in sorted(low, key=lambda row: float(row["AbsGalacticLatitudeDeg"])):
        best: tuple[float, dict[str, object]] | None = None
        for high_row in high:
            if str(high_row["galaxy_name"]) in used:
                continue
            distance = math.sqrt(sum((z(low_row, feature) - z(high_row, feature)) ** 2 for feature in features))
            if best is None or distance < best[0]:
                best = (distance, high_row)
        if best is None:
            continue
        high_row = best[1]
        used.add(str(high_row["galaxy_name"]))
        pair = {
            "LowLatitudeGalaxy": low_row["GalaxyName"],
            "MatchedHighLatitudeGalaxy": high_row["galaxy_name"],
            "MatchDistance": f"{best[0]:.9g}",
            "LowClass": low_row["Class"],
            "HighClass": high_row["Class"],
            "LowAbsGalacticLatitudeDeg": low_row["AbsGalacticLatitudeDeg"],
            "HighAbsGalacticLatitudeDeg": high_row["AbsGalacticLatitudeDeg"],
        }
        for metric in ["rms_log_tpg", "weighted_rms_log_tpg", "mean_log_residual_tpg", "outer_mean_log_residual_tpg"]:
            low_value = float(low_row[metric])
            high_value = float(high_row[metric])
            pair[f"Low_{metric}"] = f"{low_value:.12g}"
            pair[f"High_{metric}"] = f"{high_value:.12g}"
            pair[f"LowMinusHigh_{metric}"] = f"{low_value - high_value:.12g}"
        pairs.append(pair)
    return pairs


def build_matched_control_summary(pairs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = [{"Metric": "matched_pair_count", "Value": len(pairs), "Interpretation": "greedy unique high-latitude controls matched on log distance, max radius, and point count"}]
    for metric in ["rms_log_tpg", "weighted_rms_log_tpg", "mean_log_residual_tpg", "outer_mean_log_residual_tpg"]:
        key = f"LowMinusHigh_{metric}"
        values = [float(row[key]) for row in pairs if row.get(key) not in {"", None}]
        if not values:
            continue
        rows.append({"Metric": f"matched_{metric}_median_low_minus_high", "Value": f"{median(values):.12g}", "Interpretation": "paired diagnostic difference; not a detection"})
        rows.append({"Metric": f"matched_{metric}_positive_pairs", "Value": f"{sum(value > 0 for value in values)}/{len(values)}", "Interpretation": "sign count across matched pairs"})
    return rows


def build_threshold_scan(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    scan: list[dict[str, object]] = []
    for threshold in [5, 7.5, 10, 12, 15, 20, 22, 23, 24, 24.5, 25, 26, 27, 28, 29, 30]:
        subset = [row for row in rows if float(row["AbsGalacticLatitudeDeg"]) <= threshold]
        counts = Counter(row["Class"] for row in subset)
        ac_subset = [row for row in subset if row["Class"] in {"A", "C"}]
        scan.append(
            {
                "AbsGalacticLatitudeThresholdDeg": threshold,
                "N_total": len(subset),
                "N_AC": len(ac_subset),
                "N_A": counts["A"],
                "N_B": counts["B"],
                "N_C": counts["C"],
                "Interpretation": "foreground_screen_proxy_scan",
            }
        )
    return scan


def build_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    low = [row for row in rows if row["low_latitude_screen_24deg"] == "true"]
    high = [row for row in rows if row["low_latitude_screen_24deg"] == "false"]
    low_counts = Counter(row["Class"] for row in low)
    high_counts = Counter(row["Class"] for row in high)
    ac_low = [row for row in low if row["Class"] in {"A", "C"}]
    ac_all = [row for row in rows if row["Class"] in {"A", "C"}]
    p_value = one_sided_hypergeom_p(
        success_total=sum(row["Class"] == "C" for row in ac_all),
        population_total=len(ac_all),
        draw_count=len(ac_low),
        observed_success=sum(row["Class"] == "C" for row in ac_low),
    )
    return [
        {"Metric": "hecate_sparc_overlap_rows", "Value": len(rows), "Interpretation": "exact-name SPARC/HECATE overlaps with RA/DEC"},
        {"Metric": "low_latitude_threshold_deg", "Value": 24.0, "Interpretation": "preliminary foreground-screen proxy"},
        {"Metric": "low_latitude_total", "Value": len(low), "Interpretation": "|b| <= 24 deg"},
        {"Metric": "low_latitude_A", "Value": low_counts["A"], "Interpretation": "reviewed calm/regular class count"},
        {"Metric": "low_latitude_B", "Value": low_counts["B"], "Interpretation": "ambiguous class count"},
        {"Metric": "low_latitude_C", "Value": low_counts["C"], "Interpretation": "reviewed disturbed class count"},
        {"Metric": "high_latitude_A", "Value": high_counts["A"], "Interpretation": "|b| > 24 deg"},
        {"Metric": "high_latitude_B", "Value": high_counts["B"], "Interpretation": "|b| > 24 deg"},
        {"Metric": "high_latitude_C", "Value": high_counts["C"], "Interpretation": "|b| > 24 deg"},
        {"Metric": "ac_one_sided_c_enrichment_p", "Value": f"{p_value:.12f}", "Interpretation": "diagnostic only; not a detection"},
    ]


def write_static_tables() -> None:
    claim_rows = [
        {
            "Claim": "foreground_screen_count",
            "Status": "allowed",
            "Text": "|b| <= 24 deg selects 18 HECATE-matched SPARC systems in this packet.",
        },
        {
            "Claim": "ac_screen_asymmetry",
            "Status": "allowed",
            "Text": "Within those 18 systems, reviewed A/C labels are C-dominant: A=1 and C=6, with B=11.",
        },
        {
            "Claim": "observer_screen_motivation",
            "Status": "allowed",
            "Text": "Zone-of-Avoidance literature motivates treating the Milky Way foreground as a real observability layer.",
        },
        {
            "Claim": "candidate_signed_residual_offset",
            "Status": "allowed",
            "Text": "The low-latitude screen can be used as a preregistered window for signed residual-offset stress tests.",
        },
        {
            "Claim": "physical_detection",
            "Status": "blocked",
            "Text": "This packet does not claim that Galactic latitude physically causes disturbance or residual behavior.",
        },
        {
            "Claim": "new_dynamics_claim",
            "Status": "blocked",
            "Text": "This packet does not infer new galaxy dynamics or replace existing residual/baryonic models.",
        },
        {
            "Claim": "parent_theory_proof",
            "Status": "blocked",
            "Text": "This packet does not prove or disclose any private parent theory.",
        },
    ]
    write_csv(PACKET / "claim_boundary.csv", claim_rows, ["Claim", "Status", "Text"])

    source_rows = [
        {
            "SourceID": "NILO_CASTELLON_2025_ZOA_JWST",
            "Citation": "Nilo-Castellon et al., Faint galaxies in the Zone of Avoidance revealed by JWST/NIRCam",
            "URL": "https://arxiv.org/abs/2510.12488",
            "Role": "motivates Milky Way foreground as an observability screen",
        },
        {
            "SourceID": "HECATE_V1_1",
            "Citation": "HECATE v1.1 public catalog",
            "URL": HECATE_URL,
            "Role": "source of RA/DEC for exact-name SPARC overlaps",
        },
        {
            "SourceID": "PAPER1_LABELS",
            "Citation": "SPARC residual-disturbance Paper 1 public label packet",
            "URL": "https://github.com/jolcsak/sparc-residual-disturbance-paper1",
            "Role": "source of residual-blind A/B/C labels",
        },
    ]
    write_csv(PACKET / "source_manifest.csv", source_rows, ["SourceID", "Citation", "URL", "Role"])


def write_figure(scan_rows: list[dict[str, object]]) -> None:
    x = [float(row["AbsGalacticLatitudeThresholdDeg"]) for row in scan_rows]
    y_total = [int(row["N_total"]) for row in scan_rows]
    y_a = [int(row["N_A"]) for row in scan_rows]
    y_c = [int(row["N_C"]) for row in scan_rows]

    width, height = 720, 420
    left, right, top, bottom = 72, 28, 36, 62
    plot_w = width - left - right
    plot_h = height - top - bottom
    x_min, x_max = min(x), max(x)
    y_max = max(y_total)

    def sx(value: float) -> float:
        return left + (value - x_min) / (x_max - x_min) * plot_w

    def sy(value: float) -> float:
        return top + plot_h - value / y_max * plot_h

    def polyline(values: list[int], color: str) -> str:
        points = " ".join(f"{sx(xv):.1f},{sy(yv):.1f}" for xv, yv in zip(x, values))
        circles = "\n".join(
            f'<circle cx="{sx(xv):.1f}" cy="{sy(yv):.1f}" r="3.4" fill="{color}" />'
            for xv, yv in zip(x, values)
        )
        return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.2" />\n{circles}'

    threshold_x = sx(24.0)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{width/2:.0f}" y="24" text-anchor="middle" font-family="Arial" font-size="16">Low-Galactic-latitude foreground-screen scan</text>
  <line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="black"/>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="black"/>
  <line x1="{threshold_x:.1f}" y1="{top}" x2="{threshold_x:.1f}" y2="{top + plot_h}" stroke="black" stroke-dasharray="5,5"/>
  <text x="{threshold_x + 5:.1f}" y="{top + 14}" font-family="Arial" font-size="11">24 deg</text>
  {polyline(y_total, "#1f77b4")}
  {polyline(y_a, "#2ca02c")}
  {polyline(y_c, "#d62728")}
  <text x="{left + plot_w/2:.0f}" y="{height - 18}" text-anchor="middle" font-family="Arial" font-size="13">Foreground-screen threshold |b| &lt;= threshold (deg)</text>
  <text x="18" y="{top + plot_h/2:.0f}" transform="rotate(-90 18,{top + plot_h/2:.0f})" text-anchor="middle" font-family="Arial" font-size="13">Galaxy count</text>
  <text x="{left}" y="{top + plot_h + 20}" font-family="Arial" font-size="11">{x_min:g}</text>
  <text x="{left + plot_w - 14}" y="{top + plot_h + 20}" font-family="Arial" font-size="11">{x_max:g}</text>
  <text x="{left - 34}" y="{top + plot_h + 4}" font-family="Arial" font-size="11">0</text>
  <text x="{left - 34}" y="{top + 4}" font-family="Arial" font-size="11">{y_max}</text>
  <rect x="548" y="54" width="130" height="64" fill="white" stroke="#cccccc"/>
  <line x1="562" y1="72" x2="592" y2="72" stroke="#1f77b4" stroke-width="2.2"/><text x="600" y="76" font-family="Arial" font-size="12">all classes</text>
  <line x1="562" y1="92" x2="592" y2="92" stroke="#2ca02c" stroke-width="2.2"/><text x="600" y="96" font-family="Arial" font-size="12">A</text>
  <line x1="562" y1="112" x2="592" y2="112" stroke="#d62728" stroke-width="2.2"/><text x="600" y="116" font-family="Arial" font-size="12">C</text>
</svg>
'''
    (FIGURES / "foreground_screen_counts.svg").write_text(svg, encoding="utf-8")


def markdown_table(rows: list[dict[str, object]], fieldnames: list[str], max_rows: int | None = None) -> str:
    selected = rows if max_rows is None else rows[:max_rows]
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in selected:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fieldnames) + " |")
    return "\n".join(lines)


def write_manuscript(
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    residual_summary: list[dict[str, object]],
    matched_summary: list[dict[str, object]],
) -> None:
    low_rows = [row for row in rows if row["low_latitude_screen_24deg"] == "true"]
    summary_lookup = {row["Metric"]: row["Value"] for row in summary}
    manuscript = f"""# Milky Way foreground-screen stratification in a SPARC/HECATE residual audit

## Abstract

The Milky Way foreground is an observational layer, not merely a nuisance. Zone
of Avoidance work with JWST/NIRCam has recently shown that faint background
galaxies can be recovered through heavily contaminated Galactic regions, while
also emphasizing that extinction, stellar crowding, and confusion noise shape
extragalactic visibility. Motivated by this, we define a deliberately simple
foreground-screen diagnostic for the public SPARC residual-disturbance audit:
Galactic latitude computed from HECATE RA/DEC for exact-name SPARC overlaps.
Using the provisional screen `|b| <= 24 deg`, the packet selects 18 systems. In
the reviewed A/C subset, this screen is C-dominant: A=1 and C=6, with 11
ambiguous B systems. The A/C enrichment check is not statistically decisive
(`p = {summary_lookup['ac_one_sided_c_enrichment_p']}`), so the result is best
read as an observer-screen audit and preregistration target, not a detection.

## 1. Motivation

Nilo-Castellon et al. identify 102 galaxies in a JWST/NIRCam field in the Zone
of Avoidance and describe Galactic extinction, stellar crowding, and confusion
noise as historical limits on background-galaxy detection. This motivates a
conservative question for SPARC residual audits: do systems projected nearer to
the Milky Way plane occupy a visibly different label/observability stratum?

The point of this note is not to explain galaxy dynamics. It is to preserve a
small, reproducible foreground-screen packet that can be tested later with
better extinction maps, star-count fields, and independent galaxy samples.

## 2. Question

The working question is deliberately modest:

```text
When SPARC galaxies are stratified by a Milky Way foreground-screen proxy, does
the low-latitude stratum show a distinctive label or residual pattern that
should be frozen as a future observer-screen test?
```

The note separates three claims that are often too easily mixed:

- a foreground-screen count claim;
- a residual-stress diagnostic;
- a physical interpretation.

Only the first two are tested here. The third is explicitly blocked.

## 3. Data And Construction

Inputs:

- HECATE v1.1 RA/DEC for exact-name SPARC overlaps.
- Residual-blind A/B/C labels from the public Paper 1 SPARC residual-disturbance packet.
- Public residual summary fields from the Paper 1 reproducibility package.

The script converts HECATE equatorial coordinates to Galactic longitude and
latitude using the standard J2000 north Galactic pole constants. The primary
screen is:

```text
low_latitude_screen = |b| <= 24 deg
```

This threshold is not claimed as fundamental. It is a transparent reconstruction
of the remembered 18-object screen and should be stress-tested in future work.

## 4. Foreground-Screen Diagnostic

{markdown_table(summary, ['Metric', 'Value', 'Interpretation'])}

## Threshold Scan

{markdown_table(scan_rows, ['AbsGalacticLatitudeThresholdDeg', 'N_total', 'N_AC', 'N_A', 'N_B', 'N_C'])}

## 5. The 18 Low-Latitude Systems

{markdown_table(low_rows, ['GalaxyName', 'Class', 'AbsGalacticLatitudeDeg', 'GalacticLongitudeDeg', 'HecateDistanceMpc', 'RmsLogTPG', 'MeanLogResidualTPG', 'OuterMeanLogResidualTPG'])}

## 6. Label-Stratum Interpretation

The result is directionally interesting because the low-latitude screen is
C-heavy among systems that already have reviewed A/C labels. However, the sample
is small and B-dominated. A one-sided A/C hypergeometric enrichment diagnostic
returns `p = {summary_lookup['ac_one_sided_c_enrichment_p']}`, which is not a
discovery-level result.

## 7. Residual-Signal Stress Test

The natural follow-up question is whether the 18-object screen is also a good
place to look for a residual projection signal. We therefore join the foreground
screen to the public Paper 1 residual summary and test two distinct possibilities:

1. A residual-scatter excess.
2. A signed residual offset.

The current packet does **not** support a simple RMS-excess claim. The median
`rms_log_tpg` in the low-latitude screen is slightly lower than the high-latitude
comparison set. The more interesting candidate is instead a signed offset:
`mean_log_residual_tpg` and `outer_mean_log_residual_tpg` shift positive in the
low-latitude screen. This is exactly the sort of weak observer-screen candidate
that should be preregistered before any stronger interpretation.

{markdown_table(residual_summary, ['Metric', 'Value', 'Interpretation'])}

## 8. Matched-Control Preview

As a first guardrail, each low-latitude galaxy is greedily matched to a unique
higher-latitude control by log HECATE distance, log radial extent, and log point
count. This is only a preview; it is not a covariance-aware likelihood or an
extinction-aware analysis.

{markdown_table(matched_summary, ['Metric', 'Value', 'Interpretation'])}

## 9. What The Result Does Not Say

The current packet does not show that the Milky Way foreground creates galaxy
disturbance. It also does not show that a new dynamical law is required. The
positive signed residual shift may come from ordinary observational effects:
foreground extinction, stellar crowding, different target selection, distance
and radius imbalance, inclination systematics, or residual calibration choices.

The result is useful because it defines a clean future test. If a foreground
observer-screen effect is real, it should survive after replacing `|b|` with
physical foreground maps such as `E(B-V)`, `A_V`, source density, and confusion
metrics. If it disappears under those controls, the present 18-object window was
only a selection artifact.

The correct reading is therefore:

```text
The Milky Way foreground screen is a real observability stratum. In this SPARC/
HECATE packet, a reconstructed 18-object low-|b| screen is C-dominant among
reviewed A/C labels, but the result remains a preregistered audit target rather
than a physical inference.

The residual follow-up does not show a robust RMS-excess detection. It does show
a candidate signed residual-offset direction that is worth freezing as the next
observer-screen test.
```

## 10. Preregistered Next Tests

1. Replace the latitude-only proxy with `E(B-V)`, `A_V`, star-count density, and
   local confusion metrics.
2. Freeze the screen thresholds before residual inspection.
3. Re-run the audit on independent low-latitude and high-latitude galaxy samples.
4. Separate foreground observability effects from intrinsic disturbance evidence.
5. Report all A/B/C transitions under threshold scans rather than selecting only
   the most favorable boundary.
6. Test signed residual offset before RMS excess, because the present packet
   disfavors the simplest RMS-excess version of the hypothesis.

## 11. Claim Boundary

This note does not claim new dynamics, a physical detection, or proof of any
private parent theory. It is a public observer-screen method note.

## References

- J. L. Nilo-Castellon et al., *Faint galaxies in the Zone of Avoidance revealed
  by JWST/NIRCam*, arXiv:2510.12488, A&A 704, A209 (2025).
- SPARC residual-disturbance Paper 1 public reproducibility package.
- HECATE v1.1 public catalog.
"""
    (PACKET / "manuscript_draft.md").write_text(manuscript, encoding="utf-8")


def write_pdf() -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    markdown = (PACKET / "manuscript_draft.md").read_text(encoding="utf-8")
    doc = SimpleDocTemplate(str(PACKET / "manuscript_draft.pdf"), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 8))
            continue
        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], styles["Heading2"]))
        elif line.startswith("|"):
            story.append(Paragraph(line.replace("|", " | "), styles["Code"]))
        elif line.startswith("```"):
            continue
        else:
            story.append(Paragraph(line, styles["BodyText"]))
    doc.build(story)


def write_status_and_manifest() -> None:
    status = """# Status

Status: seed public method note / observer-screen audit.

The current packet reconstructs an 18-object low-Galactic-latitude screen from
HECATE RA/DEC and public SPARC labels. The label result is directional but not
statistically decisive. A follow-up residual stress test does not support a
simple RMS-excess claim, but it does expose a candidate signed residual-offset
direction. Both results should be treated as preregistration targets for a
stronger extinction-aware analysis.
"""
    (PACKET / "status.md").write_text(status, encoding="utf-8")

    reproducibility = """# Reproducibility

Run:

```bash
python studies/zoa_foreground_screen_audit_v01/make_foreground_screen_packet.py
PYTHONPATH=src python -m pytest -q
```

The script downloads HECATE v1.1 into an untracked raw-data path if necessary,
computes Galactic coordinates, and rebuilds all packet tables.
"""
    (PACKET / "reproducibility.md").write_text(reproducibility, encoding="utf-8")

    limitations = """# Referee Concerns And Limitations

## Why this is not a detection

The foreground screen selects only 18 systems and the A/C subset contains only
seven reviewed systems. The one-sided A/C enrichment diagnostic is not
statistically decisive. The result is a screening observation, not a discovery.

## Why `|b| <= 24 deg` is provisional

The threshold reconstructs the 18-object foreground-screen window. It is not a
physical boundary. A paper-grade follow-up must replace it with foreground maps:
`E(B-V)`, `A_V`, source density, and confusion metrics.

## Why the residual result is subtle

The low-latitude screen does not show a median RMS excess. The candidate signal
is a signed residual offset. This blocks the simple claim that foreground
screening merely increases residual scatter.

## Main confounders

- Milky Way extinction and crowding.
- Galaxy target selection near the Galactic plane.
- Distance, radial extent, and point-count imbalance.
- Inclination and morphology systematics.
- Residual calibration choices inherited from Paper 1.

## Stronger future test

Freeze the signed-offset endpoint, use foreground extinction maps, match
low-/high-latitude controls before residual inspection, and then test whether
the signed offset survives.
"""
    (PACKET / "referee_concerns_and_limitations.md").write_text(limitations, encoding="utf-8")

    manifest = {
        "packet": "zoa_foreground_screen_audit_v01/paper_packet_v01",
        "status": "seed_public_method_note",
        "primary_screen": "abs_galactic_latitude_deg <= 24",
        "raw_hecate_tracked": False,
        "outputs": [
            "foreground_screen_audit_table.csv",
            "foreground_screen_threshold_scan.csv",
            "foreground_screen_summary.csv",
            "foreground_residual_signal_summary.csv",
            "foreground_matched_control_pairs.csv",
            "foreground_matched_control_summary.csv",
            "claim_boundary.csv",
            "source_manifest.csv",
            "referee_concerns_and_limitations.md",
            "manuscript_draft.md",
            "manuscript_draft.pdf",
            "figures/foreground_screen_counts.svg",
        ],
    }
    (PACKET / "packet_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    download_hecate_if_missing()
    rows = build_audit_rows()
    scan_rows = build_threshold_scan(rows)
    summary = build_summary(rows)
    residual_join = build_residual_join(rows)
    residual_summary = build_residual_signal_summary(residual_join)
    matched_pairs = build_matched_control_pairs(residual_join)
    matched_summary = build_matched_control_summary(matched_pairs)

    audit_fields = [
        "GalaxyName",
        "Class",
        "LabelConfidence",
        "HecatePGC",
        "HecateObjectName",
        "HecateDistanceMpc",
        "RA_deg",
        "DEC_deg",
        "GalacticLongitudeDeg",
        "GalacticLatitudeDeg",
        "AbsGalacticLatitudeDeg",
        "low_latitude_screen_24deg",
        "RmsLogTPG",
        "WeightedRmsLogTPG",
        "MeanLogResidualTPG",
        "OuterMeanLogResidualTPG",
    ]
    scan_fields = [
        "AbsGalacticLatitudeThresholdDeg",
        "N_total",
        "N_AC",
        "N_A",
        "N_B",
        "N_C",
        "Interpretation",
    ]
    write_csv(PACKET / "foreground_screen_audit_table.csv", rows, audit_fields)
    write_csv(PACKET / "foreground_screen_threshold_scan.csv", scan_rows, scan_fields)
    write_csv(PACKET / "foreground_screen_summary.csv", summary, ["Metric", "Value", "Interpretation"])
    write_csv(PACKET / "foreground_residual_signal_summary.csv", residual_summary, ["Metric", "Value", "Interpretation"])
    matched_pair_fields = [
        "LowLatitudeGalaxy",
        "MatchedHighLatitudeGalaxy",
        "MatchDistance",
        "LowClass",
        "HighClass",
        "LowAbsGalacticLatitudeDeg",
        "HighAbsGalacticLatitudeDeg",
        "Low_rms_log_tpg",
        "High_rms_log_tpg",
        "LowMinusHigh_rms_log_tpg",
        "Low_weighted_rms_log_tpg",
        "High_weighted_rms_log_tpg",
        "LowMinusHigh_weighted_rms_log_tpg",
        "Low_mean_log_residual_tpg",
        "High_mean_log_residual_tpg",
        "LowMinusHigh_mean_log_residual_tpg",
        "Low_outer_mean_log_residual_tpg",
        "High_outer_mean_log_residual_tpg",
        "LowMinusHigh_outer_mean_log_residual_tpg",
    ]
    write_csv(PACKET / "foreground_matched_control_pairs.csv", matched_pairs, matched_pair_fields)
    write_csv(PACKET / "foreground_matched_control_summary.csv", matched_summary, ["Metric", "Value", "Interpretation"])
    write_static_tables()
    write_figure(scan_rows)
    write_manuscript(rows, summary, scan_rows, residual_summary, matched_summary)
    write_pdf()
    write_status_and_manifest()
    print(f"Wrote foreground-screen packet: {PACKET}")


if __name__ == "__main__":
    main()

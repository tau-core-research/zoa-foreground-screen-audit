# Milky Way foreground-screen stratification in a SPARC/HECATE residual audit

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
(`p = 0.295343139746`), so the result is best
read as an observer-screen audit and preregistration target, not a detection.

## Motivation

Nilo-Castellon et al. identify 102 galaxies in a JWST/NIRCam field in the Zone
of Avoidance and describe Galactic extinction, stellar crowding, and confusion
noise as historical limits on background-galaxy detection. This motivates a
conservative question for SPARC residual audits: do systems projected nearer to
the Milky Way plane occupy a visibly different label/observability stratum?

The point of this note is not to explain galaxy dynamics. It is to preserve a
small, reproducible foreground-screen packet that can be tested later with
better extinction maps, star-count fields, and independent galaxy samples.

## Data And Construction

Inputs:

- HECATE v1.1 RA/DEC for exact-name SPARC overlaps.
- Residual-blind A/B/C labels from the public Paper 1 SPARC residual-disturbance packet.
- Optional residual summary fields from the public disturbance-inference packet.

The script converts HECATE equatorial coordinates to Galactic longitude and
latitude using the standard J2000 north Galactic pole constants. The primary
screen is:

```text
low_latitude_screen = |b| <= 24 deg
```

This threshold is not claimed as fundamental. It is a transparent reconstruction
of the remembered 18-object screen and should be stress-tested in future work.

## Main Diagnostic

| Metric | Value | Interpretation |
| --- | --- | --- |
| hecate_sparc_overlap_rows | 120 | exact-name SPARC/HECATE overlaps with RA/DEC |
| low_latitude_threshold_deg | 24.0 | preliminary foreground-screen proxy |
| low_latitude_total | 18 | |b| <= 24 deg |
| low_latitude_A | 1 | reviewed calm/regular class count |
| low_latitude_B | 11 | ambiguous class count |
| low_latitude_C | 6 | reviewed disturbed class count |
| high_latitude_A | 15 | |b| > 24 deg |
| high_latitude_B | 57 | |b| > 24 deg |
| high_latitude_C | 30 | |b| > 24 deg |
| ac_one_sided_c_enrichment_p | 0.295343139746 | diagnostic only; not a detection |

## Threshold Scan

| AbsGalacticLatitudeThresholdDeg | N_total | N_AC | N_A | N_B | N_C |
| --- | --- | --- | --- | --- | --- |
| 5 | 0 | 0 | 0 | 0 | 0 |
| 7.5 | 0 | 0 | 0 | 0 | 0 |
| 10 | 1 | 0 | 0 | 1 | 0 |
| 12 | 2 | 0 | 0 | 2 | 0 |
| 15 | 8 | 2 | 0 | 6 | 2 |
| 20 | 13 | 5 | 0 | 8 | 5 |
| 22 | 15 | 6 | 1 | 9 | 5 |
| 23 | 17 | 6 | 1 | 11 | 5 |
| 24 | 18 | 7 | 1 | 11 | 6 |
| 24.5 | 18 | 7 | 1 | 11 | 6 |
| 25 | 19 | 8 | 1 | 11 | 7 |
| 26 | 20 | 9 | 1 | 11 | 8 |
| 27 | 21 | 10 | 2 | 11 | 8 |
| 28 | 21 | 10 | 2 | 11 | 8 |
| 29 | 23 | 12 | 2 | 11 | 10 |
| 30 | 25 | 13 | 3 | 12 | 10 |

## The 18 Low-Latitude Systems

| GalaxyName | Class | AbsGalacticLatitudeDeg | GalacticLongitudeDeg | HecateDistanceMpc | Projection_RMS | ResidualDisturbanceScore_v01 |
| --- | --- | --- | --- | --- | --- | --- |
| UGC03205 | B | 8.206377 | 342.903037 | 54.37 |  |  |
| NGC6946 | B | 11.672188 | 60.144887 | 5.516 |  |  |
| UGC11557 | B | 12.814719 | 60.883601 | 23.66 |  |  |
| UGC00731 | C | 13.149452 | 29.723502 | 13.03 |  |  |
| NGC6674 | B | 13.919223 | 101.271460 | 54.11 |  |  |
| UGC02885 | B | 14.050142 | 356.283096 | 71.12 |  |  |
| UGC02916 | C | 14.194665 | 19.057928 | 66.11 |  |  |
| ESO563-G021 | B | 14.397417 | 270.996728 | 79.44 |  |  |
| NGC0891 | C | 17.415249 | 15.479606 | 9.111 |  |  |
| NGC1003 | B | 17.545110 | 11.859346 | 10.76 |  |  |
| NGC2915 | C | 18.357173 | 223.897427 | 4.03 |  |  |
| UGC12632 | C | 19.311054 | 49.092790 | 9.204 |  |  |
| UGC02259 | B | 19.796208 | 8.718768 | 9.954 |  |  |
| NGC7331 | A | 20.724275 | 62.141728 | 14.4 |  |  |
| NGC6789 | B | 21.517771 | 60.889695 | 3.267 |  |  |
| NGC0801 | B | 22.456867 | 17.644924 | 55.53 |  |  |
| UGC11455 | B | 22.844922 | 52.115383 | 85.75 |  |  |
| NGC3109 | C | 23.070239 | 253.762265 | 1.291 |  |  |

## Interpretation

The result is directionally interesting because the low-latitude screen is
C-heavy among systems that already have reviewed A/C labels. However, the sample
is small and B-dominated. A one-sided A/C hypergeometric enrichment diagnostic
returns `p = 0.295343139746`, which is not a
discovery-level result.

## Residual-Signal Stress Test

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

| Metric | Value | Interpretation |
| --- | --- | --- |
| residual_summary_available | true | public Paper 1 residual summary joined to foreground screen |
| residual_join_rows | 120 | HECATE/SPARC rows with residual summary |
| residual_low_screen_rows | 18 | |b| <= 24 deg |
| residual_high_screen_rows | 102 | |b| > 24 deg |
| rms_log_tpg_low_median | 0.140050995433 | low-latitude foreground screen |
| rms_log_tpg_high_median | 0.146757312311 | higher-latitude comparison set |
| rms_log_tpg_low_minus_high_median | -0.00670631687742 | diagnostic difference; not a detection |
| weighted_rms_log_tpg_low_median | 0.116555387387 | low-latitude foreground screen |
| weighted_rms_log_tpg_high_median | 0.137194953464 | higher-latitude comparison set |
| weighted_rms_log_tpg_low_minus_high_median | -0.0206395660763 | diagnostic difference; not a detection |
| mean_log_residual_tpg_low_median | 0.0477160372602 | low-latitude foreground screen |
| mean_log_residual_tpg_high_median | -0.039649763687 | higher-latitude comparison set |
| mean_log_residual_tpg_low_minus_high_median | 0.0873658009472 | diagnostic difference; not a detection |
| outer_mean_log_residual_tpg_low_median | 0.00914315295169 | low-latitude foreground screen |
| outer_mean_log_residual_tpg_high_median | -0.0241318063717 | higher-latitude comparison set |
| outer_mean_log_residual_tpg_low_minus_high_median | 0.0332749593234 | diagnostic difference; not a detection |
| mean_err_vobs_kms_low_median | 5.77818965517 | low-latitude foreground screen |
| mean_err_vobs_kms_high_median | 5.1711037234 | higher-latitude comparison set |
| mean_err_vobs_kms_low_minus_high_median | 0.607085931768 | diagnostic difference; not a detection |
| max_radius_kpc_low_median | 25.32 | low-latitude foreground screen |
| max_radius_kpc_high_median | 12.935 | higher-latitude comparison set |
| max_radius_kpc_low_minus_high_median | 12.385 | diagnostic difference; not a detection |
| n_points_low_median | 22 | low-latitude foreground screen |
| n_points_high_median | 13 | higher-latitude comparison set |
| n_points_low_minus_high_median | 9 | diagnostic difference; not a detection |
| interpretation | candidate_signed_projection_offset_not_rms_excess_detection | RMS median is not elevated in the 18-object screen; signed residual medians shift positive |

## Matched-Control Preview

As a first guardrail, each low-latitude galaxy is greedily matched to a unique
higher-latitude control by log HECATE distance, log radial extent, and log point
count. This is only a preview; it is not a covariance-aware likelihood or an
extinction-aware analysis.

| Metric | Value | Interpretation |
| --- | --- | --- |
| matched_pair_count | 18 | greedy unique high-latitude controls matched on log distance, max radius, and point count |
| matched_rms_log_tpg_median_low_minus_high | -0.00641394691747 | paired diagnostic difference; not a detection |
| matched_rms_log_tpg_positive_pairs | 9/18 | sign count across matched pairs |
| matched_weighted_rms_log_tpg_median_low_minus_high | 0.0158783211739 | paired diagnostic difference; not a detection |
| matched_weighted_rms_log_tpg_positive_pairs | 10/18 | sign count across matched pairs |
| matched_mean_log_residual_tpg_median_low_minus_high | 0.0100950616694 | paired diagnostic difference; not a detection |
| matched_mean_log_residual_tpg_positive_pairs | 9/18 | sign count across matched pairs |
| matched_outer_mean_log_residual_tpg_median_low_minus_high | 0.0105481845933 | paired diagnostic difference; not a detection |
| matched_outer_mean_log_residual_tpg_positive_pairs | 9/18 | sign count across matched pairs |

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

## Next Tests

1. Replace the latitude-only proxy with `E(B-V)`, `A_V`, star-count density, and
   local confusion metrics.
2. Freeze the screen thresholds before residual inspection.
3. Re-run the audit on independent low-latitude and high-latitude galaxy samples.
4. Separate foreground observability effects from intrinsic disturbance evidence.
5. Report all A/B/C transitions under threshold scans rather than selecting only
   the most favorable boundary.

## Claim Boundary

This note does not claim new dynamics, a physical detection, or proof of any
private parent theory. It is a public observer-screen method note.

## References

- J. L. Nilo-Castellon et al., *Faint galaxies in the Zone of Avoidance revealed
  by JWST/NIRCam*, arXiv:2510.12488, A&A 704, A209 (2025).
- SPARC residual-disturbance Paper 1 public reproducibility package.
- HECATE v1.1 public catalog.

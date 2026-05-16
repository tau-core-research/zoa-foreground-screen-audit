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

## 5. The 18 Low-Latitude Systems

| GalaxyName | Class | AbsGalacticLatitudeDeg | GalacticLongitudeDeg | HecateDistanceMpc | RmsLogTPG | MeanLogResidualTPG | OuterMeanLogResidualTPG |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC03205 | B | 8.206377 | 342.903037 | 54.37 | 0.11600949975788537 | 0.0873983245850471 | 0.055565320187085834 |
| NGC6946 | B | 11.672188 | 60.144887 | 5.516 | 0.0896359090075854 | -0.0831693606116379 | -0.09256925858478726 |
| UGC11557 | B | 12.814719 | 60.883601 | 23.66 | 0.7431151375673428 | -0.6040787203825251 | -0.35763864335701157 |
| UGC00731 | C | 13.149452 | 29.723502 | 13.03 | 0.339703437495753 | 0.21001308628006135 | -0.0782044521386274 |
| NGC6674 | B | 13.919223 | 101.271460 | 54.11 | 0.1261360715254176 | 0.10826931615214701 | 0.10598763897950496 |
| UGC02885 | B | 14.050142 | 356.283096 | 71.12 | 0.06662315534970306 | 0.04685592336981314 | 0.0463394047425374 |
| UGC02916 | C | 14.194665 | 19.057928 | 66.11 | 0.13928911042196776 | -0.06831440677751897 | -0.07903890648018923 |
| ESO563-G021 | B | 14.397417 | 270.996728 | 79.44 | 0.29404072405040915 | 0.07931689655380693 | 0.1691008384002877 |
| NGC0891 | C | 17.415249 | 15.479606 | 9.111 | 0.1259442118714204 | -0.09347531570220223 | -0.05008617779939154 |
| NGC1003 | B | 17.545110 | 11.859346 | 10.76 | 0.12113411141685551 | 0.024974111717001073 | 0.14932873924545975 |
| NGC2915 | C | 18.357173 | 223.897427 | 4.03 | 0.44092390599176534 | 0.27527781688707265 | 0.3774115856001438 |
| UGC12632 | C | 19.311054 | 49.092790 | 9.204 | 0.1052568716207706 | 0.0485761511506591 | -0.07054854024451106 |
| UGC02259 | B | 19.796208 | 8.718768 | 9.954 | 0.26943439551068704 | 0.24286674478824713 | 0.15148615161698695 |
| NGC7331 | A | 20.724275 | 62.141728 | 14.4 | 0.09804264249274548 | -0.08633593090910359 | -0.03659801898184237 |
| NGC6789 | B | 21.517771 | 60.889695 | 3.267 | 0.3895854018308549 | 0.35690932806891795 | 0.5020305791744587 |
| NGC0801 | B | 22.456867 | 17.644924 | 55.53 | 0.1408128804442707 | -0.08465940603010062 | -0.17407443093346248 |
| UGC11455 | B | 22.844922 | 52.115383 | 85.75 | 0.14196092541106067 | -0.06123895742954915 | -0.028053098839149467 |
| NGC3109 | C | 23.070239 | 253.762265 | 1.291 | 0.17587234171290073 | 0.1284165505065754 | 0.24323203399945445 |

## 6. Label-Stratum Interpretation

The result is directionally interesting because the low-latitude screen is
C-heavy among systems that already have reviewed A/C labels. However, the sample
is small and B-dominated. A one-sided A/C hypergeometric enrichment diagnostic
returns `p = 0.295343139746`, which is not a
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

## 8. Matched-Control Preview

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

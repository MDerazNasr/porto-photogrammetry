# Colour calibration pilot — 21 September 2026

## Outcome

The museum archive contains one genuine 24-patch ColorChecker reference image per camera for `UF_Herp_3998`. They are stored directly under `images/`, not inside `images/scale/`:

- `camera1_IMG_9401.JPG`
- `camera2_IMG_8226.JPG`
- `camera3_IMG_6883.JPG`

The existing `.mask.png` files segment the specimen/foreground; they do not isolate the chart.

## Imageomics trial

Imageomics `color-calibration` was validated on synthetic data, then run on the three real references using explicit chart masks and camera 1 as the reference. It independently matches each BGR histogram and applies the lookup tables to the full image; it does not use corresponding patches or known chart values.

| Target | Chart CDF distance before (B/G/R) | After (B/G/R) | Mean patch ΔE76 before → after | Whole-image mean change |
|---|---:|---:|---:|---:|
| Camera 2 | 0.055/0.060/0.059 | 0.008/0.008/0.009 | 12.39 → 17.99 | 28.66 |
| Camera 3 | 0.122/0.139/0.132 | 0.009/0.006/0.007 | 25.61 → 23.05 | 33.19 |

Although the histograms converged, camera 2 became washed out and camera 3 acquired a severe dark/magenta-green cast. Histogram convergence is not an adequate colour-accuracy criterion, so Imageomics is rejected as the production correction step.

## Patch-correspondence pilot

The replacement pilot rectified each chart, sampled the same 24 patch interiors, converted sRGB JPEG values to linear RGB, fitted a 3×3 least-squares transform from each target camera to camera 1, applied it to the full image, and converted back to sRGB.

| Target | Mean patch ΔE76 before | After | Median after | Whole-image mean change |
|---|---:|---:|---:|---:|
| Camera 2 | 9.29 | 3.11 | 2.61 | 9.48 |
| Camera 3 | 3.74 | 1.47 | 1.43 | 6.70 |

The corrected images remained visually natural. Camera 2's mostly white background clips more because the fitted transform raises exposure; production evaluation should report clipping on the specimen mask separately from the background.

## Recommended implementation

1. Discover per-camera reference frames at the root of each specimen's `images/` directory.
2. Detect or manually provide the four chart corners. OpenCV MCC detection was unreliable on the originals, so retain a reviewed-corners fallback.
3. Rectify the chart and sample all 24 patch interiors, excluding the black frame and gaps.
4. Work in linear RGB.
5. Fit one regularized 3×3 transform per camera and lighting group. Use camera 1 as the relative reference until the physical chart model/value edition is verified.
6. Apply each transform to that camera's reconstruction images and save to a separate output tree.
7. Emit patch ΔE, clipping, coefficients, chart coordinates, reference identity, and before/after previews.
8. Gate acceptance on colour metrics plus a small COLMAP/reconstruction regression.

Metric scaling remains separate and uses the `0.05 m` coded scale bars.

## Implementation status — 22 September 2026

The pilot is now implemented in the team repository as the `augenblick color` command.

- Core module: `team-repo/src/augenblick/preparation/color.py`
- CLI integration: `team-repo/src/augenblick/cli/main.py`
- Verified specimen configuration: `team-repo/examples/color/uf_herp_3998.json`
- Tests: `team-repo/tests/test_color.py`

The implementation automatically locates patch interiors after the four chart corners are supplied, fits one regularized 3×3 linear-RGB transform per camera, processes images in bounded-memory chunks, excludes chart references, preserves reference-camera files and masks byte-for-byte, retains JPEG EXIF, and writes a JSON report with matrices, ΔE, clipping, patch centres, processed counts, and skipped files.

The documented command was first run on one real reconstruction image per camera. It processed all three without skips and reproduced the pilot result: camera 2 mean patch ΔE76 changed from 9.218 to 3.131 and camera 3 from 3.698 to 1.432.

## Full-batch and COLMAP regression — 22 September 2026

The command then processed the full `UF_Herp_3998` capture set: 276 photographs and 276 masks (92 image-mask pairs per camera across `scale/` and `noscale/`). No photographs were skipped. The 92 camera 1 files were copied byte-for-byte; sampled masks were also byte-identical. Corrected JPEGs retained their original 6240×4160 dimensions and all 12 sampled EXIF tags. The output also contains three rectified chart-preview PNGs. The machine-readable report is stored at `outputs/color-calibration-report-uf-herp3998-full-2026-09-22.json`.

The full run used the same chart fit as the pilot:

| Camera | Mean patch ΔE76 before | After | Change |
|---|---:|---:|---:|
| Camera 1 (reference) | 0.000 | 0.000 | — |
| Camera 2 | 9.218 | 3.131 | −66.0% |
| Camera 3 | 3.698 | 1.432 | −61.3% |

A controlled masked-COLMAP regression used 36 evenly spaced `scale/` photographs (12 per camera), identical masks, COLMAP 4.0.4 CPU SIFT, a 2400-pixel extraction limit, exhaustive matching, `SIMPLE_PINHOLE`, per-image cameras, and random seed 0.

| Metric | Original | Calibrated | Change |
|---|---:|---:|---:|
| Registered images | 36/36 | 36/36 | unchanged |
| SIFT features | 242,829 | 249,981 | +2.9% |
| Verified image pairs | 171 | 171 | unchanged |
| Verified inliers | 28,084 | 28,658 | +2.0% |
| Sparse points | 3,845 | 3,929 | +2.2% |
| Observations | 14,423 | 14,750 | +2.3% |
| Mean track length | 3.751 | 3.754 | +0.1% |
| Mean reprojection error | 0.670 px | 0.676 px | +0.006 px |

This regression passes: calibration preserved complete registration and effectively unchanged geometric precision while modestly increasing feature, match, point, and observation coverage. It is evidence that the colour stage does not harm this specimen's SfM initialization, not proof that it improves every specimen or final dense mesh.

## Second-specimen validation — 25 September 2026

The same relative-calibration stage was run on `UF_birds_ivory2`, an independent four-camera bird capture. Three chart references were fully visible; camera 4's chart was partly hidden by foam and was excluded rather than estimating missing patches. The run processed 138 full-resolution photographs (46 each from cameras 1–3). The 47 camera-4 photographs were explicitly reported as skipped.

### Held-out higher-order model check (2 October 2026)

A second-order root-polynomial model was compared with the existing 3 by 3 transform using leave-one-patch-out validation on both specimens. Across four non-reference cameras and 96 held-out predictions, mean Delta E76 increased from 2.573 (linear) to 2.791 (root-polynomial). Three of four cameras worsened; the paired bootstrap interval included no improvement. Although clipping, visual-preview, and exposure-homogeneity checks passed, the held-out accuracy gate failed. The linear transform therefore remains the validated default; see `documentation/root-polynomial-held-out-comparison-2026-10-02.md`.

The unchanged production stage also passed a controlled naturally multicoloured-content test on eight real fish texture maps. Across two simulated camera responses and 16 corrected outputs, mean foreground Delta E76 fell from 3.136 to 0.158, the minimum reduction was 89.2%, all images processed without skips, and foreground clipping did not increase. Because the archive provides reconstructed textures rather than raw fish photographs and fish-specific chart frames, this is stress evidence rather than independent field calibration; see `documentation/multicolor-fish-pipeline-stress-test-2026-10-02.md`.

| Camera | Mean patch ΔE76 before | After | Mask clipping before | After |
|---|---:|---:|---:|---:|
| Camera 1 (reference) | 0.000 | 0.000 | 0.081% | 0.081% |
| Camera 2 | 7.998 | 2.866 | 0.050% | 0.612% |
| Camera 3 | 7.380 | 1.614 | 0.163% | 0.0001% |

Camera 2 crossed the conservative review gate because foreground clipping increased by 0.562 percentage points, slightly above the configured 0.5-point limit; it remains an explicit warning rather than an automatic rejection. Whole-image clipping reached 69.34% for camera 2 because the white background was driven to white, confirming why foreground-mask metrics are the useful decision signal. A visual spot check found the specimen natural while the background clipped. The machine-readable report is `outputs/color-calibration-report-uf-birds-ivory2-2026-09-25.json`.

This archive also revealed a second real mask convention, `<image-name>.mask.png` (for example, `capture.jpg.mask.png`). The implementation now supports it alongside `<image-stem>.mask.png`; 14 focused tests pass. One malformed camera-1 mask filename was not associated, so mask metrics cover 45/46 camera-1 images and 46/46 for cameras 2–3. Sampled copied-mask hashes were identical.

Automatic chart detection correctly declined these references because the small dark chart touches a much larger dark specimen; reviewed manual corners were used. This is a safe failure with the intended fallback, but it identifies an occlusion/contact case for future detector work.

## Mesh-level regression — 25 September 2026

A controlled 36-view `UF_birds_ivory2` subset (12 evenly spaced photographs per usable camera) was reconstructed independently before and after calibration with identical masks and COLMAP 4.0.4 CPU settings. Both runs registered the same 33/36 images. Because the local COLMAP build requires CUDA for PatchMatch and PACE was unreachable, the comparison uses COLMAP's CPU sparse-Delaunay mesher; it is mesh-level topology-stability evidence, not a full dense-MVS result.

| Metric | Original | Calibrated | Change |
|---|---:|---:|---:|
| Registered images | 33/36 | 33/36 | unchanged |
| Sparse points | 5,008 | 4,999 | −0.18% |
| Observations | 20,203 | 20,157 | −0.23% |
| Mean reprojection error | 0.8510 px | 0.8530 px | +0.0020 px |
| Mesh vertices | 3,506 | 3,476 | −0.86% |
| Mesh faces | 6,962 | 6,905 | −0.82% |

The meshes were similarity-aligned using all 33 shared camera centres. The symmetric mean nearest-vertex distance was 0.169% of the robust original-mesh bounding-box diagonal; directional 95th-percentile distances were 0.690% and 0.725%. This supports stable coarse surface topology after calibration but does not establish anatomical accuracy: there is no external reference surface or physical scale, and the meshes originate from sparse SfM points. The reproducible comparison utility is `scripts/compare_colmap_meshes.py`, and the machine-readable result is `outputs/color-calibration-mesh-regression-uf-birds-ivory2-2026-09-25.json`.

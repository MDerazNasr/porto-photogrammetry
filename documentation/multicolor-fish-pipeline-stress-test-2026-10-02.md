# Multicolour fish pipeline stress test — 2 October 2026

## Outcome

The production `augenblick color` stage passed a controlled multicolour-content stress test on eight real project fish texture maps.

Across two simulated camera conditions and 16 corrected outputs, mean foreground pixel Delta E76 fell from 3.136 to 0.158, a 95.7% reduction. The least-improved output still reduced error by 89.2%. All 24 generated camera images were processed without skips, no foreground clipping increase was measured, and all eight comparison previews were visually checked without finding a residual cast or obvious texture damage.

## Scope and limitation

The colour content is real: the inputs are eight 8192 by 8192 RGBA diffuse texture maps from the shared project fish-model archive, including Mchenga, Nimbochromis, and five yellowhead specimens. The test downsamples them to 1024 by 1024 while preserving their alpha-derived foreground masks.

The camera responses are controlled simulations generated from two real correction matrices previously fitted on `UF_Herp_3998`. Matching simulated chart observations provide known pixel ground truth. This makes the run a reproducible full-pipeline stress test of multicoloured content, chart fitting, mask handling, correction, clipping, and output generation.

It is **not** an independent field-calibration result. The shared fish archive contains reconstructed models and texture maps, not the original raw fish photographs or fish-specific ColorChecker frames. Therefore this result demonstrates correct recovery under controlled camera responses; it does not establish colour accuracy for the original fish acquisition.

## Predeclared acceptance criteria

- Every corrected output reduces foreground Delta E76 by at least 50%.
- Mean reduction across all outputs is at least 75%.
- No output increases foreground clipping by more than 0.50 percentage points.
- Every generated image is processed without a skip.
- Visual comparisons show no persistent cast or obvious texture damage.

All criteria passed.

## Results

| Camera condition | Textures | Mean Delta E76 before | After | Minimum reduction | Maximum clipping increase |
|---|---:|---:|---:|---:|---:|
| Camera 2 simulation | 8 | 3.927 | 0.299 | 89.2% | 0.000 pp |
| Camera 3 simulation | 8 | 2.345 | 0.017 | 96.9% | 0.000 pp |
| **Combined** | **16 outputs** | **3.136** | **0.158** | **89.2%** | **0.000 pp** |

The pipeline processed eight images for each of cameras 1, 2, and 3 and reported zero skipped images.

## Visual evidence

Eight preview strips are stored in `outputs/multicolor-fish-pipeline-previews-2026-10-02/`. Each strip is ordered:

1. target texture;
2. simulated camera 2 before correction;
3. camera 2 after correction;
4. simulated camera 3 before correction;
5. camera 3 after correction.

The corrected third and fifth panels visually return to the first-panel target while retaining fine scale and texture variation.

## Reproducibility

- Script: `scripts/run_multicolor_pipeline_stress_test.py`
- Machine-readable result: `outputs/multicolor-fish-pipeline-stress-test-2026-10-02.json`
- Preview strips: `outputs/multicolor-fish-pipeline-previews-2026-10-02/`
- Source provenance: the shared project fish-model archive; the private share token is intentionally not copied into public documentation.

## Next evidence upgrade

Obtain raw photographs and per-camera ColorChecker captures for a naturally colourful fish specimen. Run the unchanged pipeline without simulated responses and compare held-out chart patches plus masked specimen clipping. Until then, describe this result as controlled multicolour stress evidence rather than independent acquisition validation.

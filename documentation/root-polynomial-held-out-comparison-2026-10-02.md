# Root-polynomial held-out comparison — 2 October 2026

## Decision

Retain the current 3 by 3 linear-RGB transform. Do not add second-order root-polynomial correction to PR 18.

The higher-order model did not generalize better to held-out chart patches. Across two specimens, four non-reference cameras, and 96 leave-one-patch-out predictions, its mean Delta E76 was 2.791 versus 2.573 for the linear model: an 8.4% increase in error. The paired root-minus-linear mean was +0.217 Delta E76, with a bootstrap 95% interval of -0.017 to +0.454; the interval does not establish an improvement.

## Method

- Real 24-patch measurements were recovered from the original `UF_Herp_3998` and `UF_birds_ivory2` chart-reference frames.
- Camera 1 remained the relative target within each specimen.
- Each patch was held out in turn. Both models were fitted to the other 23 patches and evaluated only on the omitted patch.
- The baseline used the existing three linear-RGB terms: R, G, and B.
- The second-order root-polynomial model used six exposure-homogeneous terms: R, G, B, square-root(RG), square-root(RB), and square-root(GB).
- Both used the existing ridge value of `1e-6` and an identity prior on the linear terms.
- Adoption thresholds were fixed before the run: at least 10% pooled held-out improvement; bootstrap interval excluding no improvement; no camera more than 0.25 Delta E76 worse; no reference-frame clipping increase above 0.10 percentage points; and exposure-homogeneity residual below `1e-6`.

## Held-out results

| Specimen / camera | Linear mean Delta E76 | Root-polynomial | Root minus linear | Root wins / losses |
|---|---:|---:|---:|---:|
| UF_Herp_3998 / camera 2 | 3.579 | 3.685 | +0.106 | 10 / 13 |
| UF_Herp_3998 / camera 3 | 1.605 | 2.012 | +0.407 | 6 / 18 |
| UF_birds_ivory2 / camera 2 | 3.247 | 3.072 | -0.174 | 11 / 11 |
| UF_birds_ivory2 / camera 3 | 1.862 | 2.393 | +0.531 | 4 / 19 |
| **Mean** | **2.573** | **2.791** | **+0.217** | — |

Only one of four camera comparisons improved on average. The largest camera-level regression was +0.531 Delta E76.

## Why held-out evaluation changed the conclusion

On all 24 fitted patches, the root model reduced error for both camera-2 comparisons (3.131 to 2.752 and 2.866 to 2.325) but slightly worsened both camera-3 comparisons (1.432 to 1.500 and 1.614 to 1.708). Leave-one-patch-out evaluation then showed that the apparent camera-2 gains did not generalize consistently. Choosing the model from fitted-patch error alone would therefore have rewarded added flexibility rather than better prediction.

The recovered measurements reproduce the archived all-patch linear results exactly, providing a regression check on chart extraction and the comparison implementation.

## Safety diagnostics

- Maximum root-versus-linear clipping increase on the four full chart-reference frames: `0.000143` percentage points, below the `0.10` threshold.
- Maximum exposure-homogeneity residual in linear RGB: `2.22e-16`, below the `1e-6` threshold.
- All eight full-frame previews were visually inspected. No obvious additional cast or exposure failure was observed.

These safety checks passed, but they do not override the failed held-out accuracy criteria.

## Artifacts

- Machine-readable results: `outputs/color-model-held-out-comparison-2026-10-02.json`
- Full-frame previews: `outputs/color-model-previews-2026-10-02/`
- Reproducible comparison: `scripts/compare_color_models.py`

## Recommendation

Keep the linear model as the validated default and close the higher-order-model checklist item as evaluated and rejected. Revisit a higher-order model only with substantially more independent chart observations spanning lighting/exposure conditions, using nested model selection rather than fitted-patch error.

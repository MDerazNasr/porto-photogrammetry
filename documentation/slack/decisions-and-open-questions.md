# Decisions and Open Questions

## Settled or strongly supported decisions

| Decision | Rationale | Status |
|---|---|---|
| Use masked COLMAP as the stable pose default | Correct masking removed static-background failure and outperformed VGGT on tested specimens | Adopted direction |
| Use COLMAP format as the interchange contract | Lets pose and reconstruction stages be swapped without rewriting downstream tools | Adopted architecture |
| Evaluate appearance and geometry separately | PSNR/SSIM improvements can coexist with unusable meshes | Required evaluation principle |
| Preserve high-poly geometry | Morphometrics and color analysis matter more than game-ready polygon budgets | Project requirement |
| Use matched masks across methods | Reduces unfair differences caused by background handling | Comparison rule |
| Store large datasets in HiperGator Blue storage | Login/home quotas are too small for images, splats, and meshes | Operational practice |
| Keep RealityScan/Metashape as references | They indicate practical quality but are not open-source dependencies or true ground truth | Baseline role |
| Center the next publication on a dataset/benchmark | Achievable within a semester and valuable when structured around biodiversity and difficulty | Recommended main goal |
| Begin benchmark validation with dry, rigid specimens and structured-light scans | Existing paired scans capture the relevant external surface and avoid wet-specimen deformation | Adopted Fall 2026 direction |
| Do not replace masked-COLMAP initialization with visual hull yet | Novel-view metrics improved, but the gain did not materially survive mesh extraction | Current experimental conclusion |
| Use 24-patch correspondence, not whole-chart histogram matching, for colour calibration | A real three-camera pilot reduced mean patch error to 3.11/1.47 ΔE76; Imageomics histogram matching created severe colour casts despite matching histograms | Adopted implementation direction |
| Retain the 3 by 3 linear model instead of second-order root-polynomial correction | Across two specimens and 96 leave-one-patch-out predictions, root-polynomial mean Delta E76 was 2.791 versus 2.573 for linear; three of four cameras worsened and the paired bootstrap interval included no improvement | Higher-order model evaluated and rejected, 2 October 2026 |
| Treat the fish-texture run as controlled multicolour stress evidence, not field calibration | Eight real fish textures and 16 controlled corrected outputs reduced mean foreground Delta E76 3.136 to 0.158 without added clipping, but the archive lacks raw fish photographs and fish-specific chart frames | Pipeline stress test passed; independent colourful acquisition still needed |
| Revisit neural implicit surfaces with background masks | Older neural-implicit trials did not mask the background; masking produced the largest gains in 3DGS, and Syed wants more method diversity than Meshroom versus 3DGS | Method sweep requested from Mohamed and Om; first reproducible baseline not yet selected |
| Merge active PRs in dependency order | Syed announced PR 19, PR 17, PR 20, then PR 18, with each later author resolving conflicts against main | PR 18 must be conflict-checked after the first three land |
| Accept the implemented colour stage for wider testing | Full `UF_Herp_3998` processing completed without skips; a controlled 36-image masked-COLMAP regression retained 36/36 registrations and increased sparse points by 2.2% with only +0.006 px mean reprojection error | Pilot acceptance passed |
| Treat colour calibration as geometry-neutral at the current evidence level | An independent 36-view run retained 33/36 registrations, changed sparse-Delaunay vertices/faces by under 1%, and produced a 0.169%-of-bounding-box aligned vertex difference | Supported for coarse topology; dense/anatomical validation pending |
| Compare method runtimes only on matched hardware | Hardware availability and device differences confound wall-clock comparisons | Meeting 4 reporting rule |
| Use windowed coded-bar scaling as the current validated metric-scale path | Ihor's mandible protocol passed predeclared spread/check-bar gates; the global static-marker model and cranium replication did not | One-specimen acceptance; generalization pending |

## Current open questions

### Research design

- Which of the eight available paired structured-light scans can be transferred and used immediately?
- Do the supplied structured-light meshes retain enough anatomical detail for ground-truth evaluation, despite apparent export decimation, and can the scanner software produce denser exports?
- Which additional structured-light scans can be produced for the final dataset?
- What taxonomic and difficulty sampling plan gives both breadth and a manageable compute budget?
- Should visual-hull plus 2DGS be the main method contribution, or one of several secondary experiments?
- Can silhouette regularization or hybrid SfM-plus-hull initialization improve final mesh geometry where hull-only initialization did not?
- How should two turntable positions with materially different illumination be modeled or calibrated?
- Which geometric metrics and alignment protocol should be authoritative across partial fossils and complete specimens?
- How many commercial reference runs are needed, and should RealityScan or Metashape be the primary practical baseline?

### Data and access

- Has museum-wide MorphoSource download access been granted to the researchers?
- Have all eight paired structured-light scans been transferred to project storage?
- Are prior PACE files retained while access is renewed?
- Where will CT, source photography, masks, commercial reconstructions, and derived outputs be versioned long-term?
- Which additional specimens include per-camera 24-patch reference frames at the root of `images/`, as `UF_Herp_3998` does?
- Is the observed chart an X-Rite/Calibrite ColorChecker Classic or compatible clone, and which patch-value edition should be used for absolute calibration?
- Should the current 0.5-percentage-point increase remain a warning-only specimen-mask clipping threshold after more specimens are tested?
- Can the physical colour chart's make and patch-value edition be confirmed so PR 18 can support a defensible absolute target?

### Compute

- How will the team coordinate HiperGator jobs under the eight-GPU group limit?
- Should installation/setup tasks move to CPU-only nodes by policy?
- Is a shared queue or job calendar needed to prevent simultaneous long-running allocations?
- What is the current PACE concurrent-job ceiling? Meeting 4 reported a reduction from 500 to 50; verify before array submission.

### Reproducibility

- Which branch is the release baseline after the repository rename?
- Which backends are mandatory for the first stable release versus experimental?
- What is the smallest benchmark subset that still covers easy, hard, complete, partial, soft-tissue, and hard-tissue cases?

## Near-term action queue

1. Confirm compute availability and coordinate HiperGator GPU use.
2. Resolve museum/MorphoSource and CT-data access.
3. Freeze the dataset taxonomy and challenge axes.
4. Define alignment, ground-truth, and geometry metrics before running large experiments.
5. Reproduce the masked COLMAP baseline in a clean environment.
6. Select the first reconstruction backends and resource budget.
7. Archive each run’s config, logs, cameras, renders, mesh, metrics, and failure state.
8. **Completed 22 September 2026:** calibrated all 276 `UF_Herp_3998` photographs and passed a 36-image masked-COLMAP regression (36/36 registered; +2.2% sparse points).
9. Keep coded-marker metric scaling separate from colour calibration.
10. Validate the supplied structured-light mesh detail before fixing the geometry benchmark protocol.
11. Coordinate Mohamed's coded-marker follow-up with Ihor's accepted windowed-scale work to avoid duplication.
12. Review Om, Ihor, and Syed's Week 4 reports before fixing the next experimental batch.

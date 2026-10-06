# Project Timeline

## May-June 2025: formation and pipeline decomposition

- The Slack channel was created on 21 May 2025.
- The team split initial exploration between OpenMVS and SuGaR while investigating VGGT as a replacement for older pose/reconstruction components.
- The pipeline was decomposed into input, preprocessing, pose/initial geometry, dense reconstruction, surface extraction, and post-processing.
- Museum fish and skull datasets were organized; HiperGator access was requested as PACE memory and build constraints became clear.

## July-August 2025: SDF experiments and compute migration

- NeuS2, Neuralangelo, VolSDF, HeatSDF, marching cubes, and Instant-NGP components were tested.
- Camera-coordinate mistakes, dependency conflicts, and high-resolution image memory became central engineering issues.
- Pre-cropping was identified as important for retaining small-specimen detail through VGGT.
- Work moved toward HiperGator, separate environments, and a modular script structure.

## September-November 2025: simplified pipelines and mesh quality

- MapAnything and FastVGGT were evaluated as possible simplifications; MapAnything underperformed VGGT on a lionfish and appeared better suited to rooms/scenery.
- High-resolution meshes were produced, but camera views and benchmark rendering needed refinement.
- The semester wound down without a fully reliable museum-grade pipeline.

## January-May 2026: Augenblick and Gaussian reconstruction study

- The channel was renamed `porto-photogrammetry`.
- The project moved to the Human Augment Analytics repository.
- Syed Fahad Rizvi formalized a modular COLMAP/VGGT-to-Gaussian pipeline and compared SuGaR, 2DGS, PGSR, and Gaussian Wrapping against Meshroom and RealityScan.
- Background masking emerged as a dominant quality factor.
- Pull request 8 and the Spring final report captured the implementation and evaluation.

## June-August 2026: corrected COLMAP baseline and deeper evaluation

- New work reproduced the Spring pipeline and investigated turntable priors, bundle adjustment, VGGT variants, COLMAP, 2DGS, PGSR, MILo, Plenoxels, and Metashape.
- A masking omission in the prior COLMAP path was corrected. Masked COLMAP became the strongest and most practical pose baseline.
- Tianshu Wu completed a systematic pose-by-method evaluation; Ihor Vilkhovyi completed turntable and masked-COLMAP work.
- RealityScan was free for academic use and was rerun with matched masked images; outputs moved to Blue storage.
- The team began planning a biodiversity dataset/benchmark paper with CT ground truth and optional method novelty.

## Fall 2026: publication and onboarding

- Mohamed Deraz Nasr and Om Kshatriya joined the project overview.
- Friday 10-11 AM Eastern meetings were established.
- MorphoSource/Florida Museum resources, CT-based evaluation, and dataset design became immediate priorities.
- On 1 September, HiperGator group GPU capacity was exhausted, creating the first operational blocker of the term.
- Zach Randall joined Slack and confirmed eight photogrammetry specimens with paired structured-light scans. The Artec Space Spider was identified as the preferred scanner for the target specimen sizes.
- Forty-two rigid specimens were shortlisted, and cleaned photography was staged under `/blue/arthur.porto/data/datasets/photogrammetry/neurips/raw`.
- A 20-run visual-hull initialization ablation improved novel-view metrics but not extracted meshes enough to displace masked COLMAP. Work moved toward silhouette regularization and hybrid initialization.
- The team retained weekly project meetings and weekly time logs, with no Museum unit representative required under the 11 September administrative update.
- Anthony Abruzzini joined as the 8803 manager/admin for tracker and weekly-report coordination while Riyam remained available.
- All 76 current specimen elements received new SAM 3 masks and were staged under the `neurips/prepared` Blue-storage path.
- Review of the available structured-light exports raised an unresolved concern that the meshes may be too decimated for authoritative geometry evaluation.
- Mohamed completed and reported the relative colour-calibration pilot: 276 photographs processed without skips and a 36-image masked-COLMAP regression passed.
- PR 18 packaged the colour stage with automatic chart detection and safe manual fallback. A second-specimen run processed 138 images and a controlled sparse-Delaunay mesh regression retained the same 33/36 registrations before and after calibration.
- Ihor formalized point-to-triangle geometry evaluation and demonstrated one accepted independent coded-bar scale using a predeclared sliding-window protocol; oblique-view detection blocked replication on the cranium.
- Om delivered review-ready SuGaR held-out evaluation and full-resolution photo-baking work, while Syed completed SAM 3 masks for all 76 elements.
- Anthony's weekly-report bot was confirmed to detect posted reports without tags or keywords. Meeting 4 also set matched hardware as a requirement for wall-clock comparisons.

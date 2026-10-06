# Results and Reports

## Syed Fahad Rizvi - Spring 2026

**Report:** *Augenblick: A Modular Photogrammetry Pipeline*

The work standardized pose and surface-reconstruction stages around COLMAP-compatible inputs and compared COLMAP and VGGT with SuGaR, 2DGS, PGSR, and Gaussian Wrapping. RealityScan and Meshroom were used as qualitative references.

Main findings:

- COLMAP took about 10 minutes, VGGT about 3 minutes, and VGGT plus bundle adjustment about 15 minutes in the reported setup.
- End-to-end reconstruction paths stayed under 90 minutes on one GPU.
- Approximate total runtimes were Meshroom 60 minutes, SuGaR 80, 2DGS 40, PGSR 70, and Gaussian Wrapping 65; method times included COLMAP where applicable.
- Gaussian Wrapping gave the best overall balance of runtime and geometric fidelity in that study.
- Good masks were essential. Several apparent method failures were actually masking or background-handling problems.
- VGGT’s 50-60 GB memory footprint made it difficult to scale to large image collections on commodity hardware; COLMAP remained the practical default.

The corresponding code was submitted in project pull request 8, and the final PDF already exists in the repository’s main documentation folder.

## Tianshu Wu - Summer 2026

**Report:** *Multi-View Photogrammetry for Museum Specimens: Pose Estimation, Neural Rendering, and Mesh Reconstruction*

This study evaluated COLMAP, VGGT, VGGT-BA, and VGG-TTT poses across Plenoxels, MVSGaussian, 3DGS, PGSR, and related variants on a fixed 15-view foreground evaluation.

Main findings:

- COLMAP poses were strongest on the primary mammal-skull data.
- Base PGSR reached 27.21 dB foreground PSNR.
- A 45,000-iteration PGSR schedule reached 27.80 dB without scale normalization and 28.12 dB with scale normalization.
- PGSR provided the best trade-off between novel-view quality and mesh extraction among the tested paths.
- PGSR and MILo recovered cranial geometry from the same strong COLMAP poses but had complementary failure modes.
- Metashape remained the most complete reference surface.
- Geometry-aware methods were much more sensitive to pose quality than appearance-only methods; VGG-TTT caused a large PGSR degradation.

Recommended next work was quantitative geometry evaluation against aligned reference meshes and broader testing across UF taxa.

## Ihor Vilkhovyi - Summer 2026

The most consequential finding was that the prior COLMAP path had not applied specimen masks. Once corrected, masked COLMAP produced substantially better structure-from-motion results than VGGT and did not require explicit turntable priors. COLMAP plus 2DGS then produced strong splats across the tested specimens.

Earlier in the term, turntable-aware pose initialization and bundle adjustment improved learned-pose results. Later work shifted toward matched commercial comparisons, RealityScan processing, and geometry evaluation. The final report and several high-resolution comparisons exceed the Slack connector’s 10 MB read limit and remain referenced in the attachment guide.

## Ihor Vilkhovyi - Fall 2026 Week 1

Ihor implemented `augenblick sfm hull` and ran a controlled 20-run ablation over five specimens, two resolutions, and two initializations. Visual-hull initialization consistently improved LPIPS and usually SSIM, but its effect largely disappeared during TSDF mesh extraction. Thin structures were a failure mode, especially when the voxel carve and largest-component filtering removed scale cards or perches. The next experiments are silhouette regularization, hybrid SfM-plus-hull seeding, mask repair, per-position appearance embeddings, and convergence-based stopping.

He also repaired the PACE environment, rebuilt CUDA rasterizers for multiple GPU architectures, increased throughput from three to 12 concurrent jobs, and replaced partial working datasets with verified canonical copies.

## Mohamed Deraz Nasr - Fall 2026 Week 3

Mohamed's report was posted late on 23 September and covers the colour-calibration implementation and validation completed on 21-22 September. It records the rejection of whole-chart histogram matching, implementation of `augenblick color`, full processing of 276 `UF_Herp_3998` image-mask pairs without skips, and a controlled 36-image masked-COLMAP regression.

The strongest result was a reduction in mean patch error from 9.218 to 3.131 Delta E76 for camera 2 and from 3.698 to 1.432 for camera 3. Both sparse reconstructions registered 36/36 images; verified inliers and sparse points increased slightly while mean reprojection error changed by only 0.006 px. The report correctly treats geometry as preserved rather than improved. Its next milestone is a review-ready pull request and reproducible demonstration; mask-only clipping, absolute chart calibration, second-specimen validation, and dense/mesh evaluation remain follow-ups.

## Week 4 team reports - 24-25 September 2026

### Mohamed Deraz Nasr

The relative colour-calibration work was packaged in upstream PR 18 with automatic chart detection plus reviewed-corner fallback and support for both observed mask-name conventions. An independent `UF_birds_ivory2` run processed 138 images across three usable cameras: camera 2 patch error fell from 7.998 to 2.866 Delta E76 and camera 3 from 7.380 to 1.614. Camera 2 crossed the conservative foreground-clipping warning by 0.562 percentage points; the partly occluded camera-4 chart was safely excluded. A 36-view sparse-Delaunay regression retained 33/36 registrations before and after, changed mesh size by under 1%, and measured a 0.169%-of-bounding-box symmetric nearest-vertex difference after camera-centre alignment. This is topology-stability evidence, not dense-MVS or anatomical validation.

### Ihor Vilkhovyi

Week 4 established the geometry-evaluation protocol: both turntable positions, masked COLMAP, a persisted split, 2DGS, mesh extraction, point-to-triangle distances in both directions, and explicit separation of shape from metric scale. Shape-only F@0.5% was 0.9037 for the 1769 mandible and 0.8645 for the cranium after similarity alignment. Object-domain and observability-domain rules remain open.

Ihor's early Week 5 report developed independent coded-bar scaling. A predeclared 24-view sliding-window protocol accepted 14 of 27 mandible windows and produced 118.97 mm/model-unit, 0.26% primary-bar spread, at most 0.40% withheld-bar disagreement, and rigid F@0.5% of 0.8966. The cranium did not pass because oblique-view target coverage was too sparse. Proposed next work is to explain the global-static-marker failure, improve oblique-view decoding, and extend the protocol to other Artec-paired specimens.

### Om Kshatriya

Om separated SuGaR held-out evaluation into a clean PR and created a stacked, method-agnostic full-resolution photo-baking prototype. A solid-skull control reconstructed successfully across 2DGS, PGSR, Gaussian-Wrapping, and SuGaR, while the prior thin translucent fish collapsed; the evidence therefore points to specimen dependence rather than a universal pipeline failure. Full-resolution baking looked better but could score worse under alignment-sensitive SSIM/LPIPS, motivating DISTS, FID/KID, coverage, seam, and contributing-camera diagnostics. Two L40S nodes were identified as unstable and excluded.

### Syed Fahad Rizvi

Syed added SAM 3 as a masking backend, selected the `skeleton` prompt, and removed a reflective-support failure with a negative `reflection` mask. He generated masks for all 76 elements: 24,361 images in 16,306 seconds, approximately 0.67 seconds/image on an RTX PRO 6000. Planned work includes COLMAP and multiple reconstruction backends on the first batch, plus review of Ihor's and Om's evaluation PRs.

## 2025 exploratory phase

The initial team compared VGGT-based paths with OpenMVS, SuGaR, NeuS2, Neuralangelo, VolSDF, HeatSDF, Poisson reconstruction, and marching-cubes extraction. This phase established several durable lessons:

- High-resolution, many-view VGGT inference can become memory bound.
- Pre-cropping protects small specimens from downsampling losses.
- Camera-coordinate conversion errors can dominate downstream reconstruction.
- Separate environments may be required for conflicting CUDA, compiler, and PyTorch dependencies.
- HiperGator’s Blue storage should hold datasets and outputs rather than login-node home storage.
- The practical target is RealityScan-comparable output in an open, reproducible workflow.

## Report inventory

The local private archive includes 30+ PDFs, including Fall Week 4 reports from Mohamed, Om, Ihor, and Syed plus Ihor's early Week 5 report. See [Attachment guide](attachment-guide.md) and the weekly-report archive inventory for preservation status.

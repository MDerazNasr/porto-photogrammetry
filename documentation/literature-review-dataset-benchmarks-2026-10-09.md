# Dataset and benchmark literature review — 9 October 2026

## Purpose

Syed asked the team to examine recent dataset and benchmark papers and determine what makes their evaluation compelling beyond a score table. The review must extract failure analysis, ablations, dataset documentation, evaluation controls, and concrete practices that the museum-photogrammetry project should adopt.

## Review 1 — Martine

**Paper:** Robin Bruneau et al., *Martine: Benchmarking Multi-View 3D Surface Reconstruction Across Viewpoint Coverage, Resolution, and Lighting*, NeurIPS 2026 Evaluations & Datasets.

**Primary record:** https://neurips.cc/virtual/2026/poster/139554  
**OpenReview record:** https://openreview.net/forum?id=IxlCfLMRly

### Evidence scope

This first-pass extraction uses the official NeurIPS title, author list, and abstract. On 9 October, OpenReview challenge-gated the PDF and supplementary-material endpoints in the current environment. Claims that require the methods, experiments, appendix, datasheet, or release package remain explicitly unverified below; the abstract is not treated as a substitute for the full paper.

### Confirmed dataset design

- 28 controlled-capture objects, including transparent materials and fine structures.
- 9568 × 6376-pixel imagery.
- 84 views distributed over a spherical cap.
- Both single-light and multi-light acquisition regimes.
- Object-independent camera calibration.
- Accurate 3D reference scans.
- Calibration and image-to-geometry alignment accuracy quantified on test images.
- 3D property masks for material properties, visibility, curvature, and fine structures.
- Evaluation spans photogrammetry, classical multi-view stereo, neural implicit surfaces, Gaussian-splatting-based reconstruction, and multi-view photometric stereo.
- The benchmark resolves sub-millimetric differences; the best reported mean one-sided Chamfer distance is 0.063 mm over the evaluated visible surface.

### Why the analysis is compelling

Martine does not reduce reconstruction quality to one aggregate leaderboard number. Its design separates three sources of variation that are otherwise confounded:

1. **Acquisition regime:** viewpoint coverage, image resolution, and lighting are controlled variables rather than undocumented properties of each run.
2. **Object properties:** per-surface property masks allow error to be stratified by material, visibility, curvature, and fine structure.
3. **Reconstruction paradigm:** classical, neural-implicit, Gaussian-based, photogrammetric, and photometric-stereo methods are evaluated in one framework.

It also quantifies the accuracy of the benchmark itself. Camera calibration, image-to-reference alignment, and reference geometry are treated as measured parts of the experiment rather than assumed ground truth. Finally, evaluation is restricted to the visible surface and the reported metric retains physical units, preventing internal or unobservable geometry from distorting the result.

### Direct implications for our project

#### Required for the first defensible benchmark

1. **Publish an acquisition manifest per specimen.** Record camera body/lens, resolution, view count, ring/position labels, lighting group, masks, scale references, and all exclusions.
2. **Quantify reference uncertainty.** Record structured-light or CT resolution, export/decimation history, registration residuals, and the usable surface domain. Do not call a mesh ground truth without this evidence.
3. **Evaluate only observable exterior surfaces.** Exclude internal CT faces and regions outside the photogrammetric visibility envelope before computing geometry metrics.
4. **Retain metric units.** Use coded-bar scale followed by rigid registration for metric evaluation; report similarity-aligned results separately as shape-only diagnostics.
5. **Report per-specimen results and failures.** Keep the aggregate table, but include registration failures, missing regions, and method-specific qualitative examples.

#### Strongly recommended analyses

1. **Specimen-property taxonomy.** At minimum annotate texture level, reflectance, translucency/wetness, thin structures, cavities/occlusion, curvature/detail, and support/background difficulty.
2. **Property-conditioned errors.** Where dense labels are impractical, begin with specimen-level strata; for reference-paired specimens, add surface-region masks for fine structures, high curvature, low visibility, and reflective/translucent regions.
3. **Acquisition ablations.** Use fixed subsets such as 24/48/96 views or full rings, one controlled resolution change, and masked versus unmasked inputs. Lighting ablation is possible only where matched captures exist.
4. **Benchmark-family coverage.** Compare at least one classical photogrammetry/MVS baseline, one neural-implicit baseline, and the Gaussian-based methods already in the project. Do not compare methods on different images, masks, crops, or hardware without labelling the difference.
5. **Benchmark sensitivity check.** Demonstrate that reference resolution and alignment error are meaningfully below the method differences being interpreted.

### Proposed failure taxonomy for the museum dataset

| Axis | Categories to record | Example evidence |
|---|---|---|
| Pipeline outcome | success; registration failure; training failure; mesh-export failure | registered-image count, exit status, logs |
| Coverage | complete exterior; local hole; large missing region; unsupported internal surface | visibility-masked completeness map |
| Material | diffuse; glossy; translucent/wet; mixed | property label and regional distance map |
| Geometry | broad smooth surface; high curvature; cavity; thin structure; fine texture | reference-region mask and per-region metrics |
| Capture | full/partial rings; view count; resolution; lighting group | acquisition manifest |
| Foreground handling | masked; unmasked; mask-error case | mask provenance and paired ablation |
| Metric scale | accepted coded-bar scale; unavailable; rejected by gates | scale JSON and COLMAP-model hashes |

### Changes to the current evaluation plan

- Add a machine-readable acquisition manifest rather than relying on folder layout and prose.
- Add an explicit visible-surface evaluation mask to the CT/structured-light protocol.
- Store reference accuracy, registration residuals, and decimation provenance alongside every reference mesh.
- Extend the results schema with pipeline-failure status and property/capture strata; do not average failed runs away.
- Predeclare the view-count, masking, and resolution ablations before running methods.
- Require per-specimen qualitative error maps for representative success and failure cases.
- Treat the current sparse-Delaunay comparison as topology-preservation evidence only; it cannot satisfy Martine-style metric surface evaluation.

### Full-text verification still required

Before this paper's review is considered complete, verify from the PDF, supplement, and release artifacts:

- exact train/validation/test or public/private split;
- complete baseline list, versions, and configuration-equality policy;
- precise definitions and thresholds for Chamfer, accuracy, completeness, and any normal metrics;
- how visibility and property masks are constructed and validated;
- scanner type, resolution, and reference-mesh preprocessing;
- image-to-geometry registration method and reported uncertainty;
- ablation grid for view coverage, resolution, and lighting;
- missing-run policy, statistical summaries, and uncertainty reporting;
- runtime, hardware, and resource reporting;
- dataset license, host, metadata/datasheet, code, versioning, and correction policy.

## Next paper

NerfBaselines: *Consistent and Reproducible Evaluation of Novel View Synthesis Methods*. This paper will be used to define configuration parity, installability, result reproduction, and protections against protocol-driven leaderboard inflation.

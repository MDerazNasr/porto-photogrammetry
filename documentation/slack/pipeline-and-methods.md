# Pipeline and Methods

## Reference pipeline

```text
Input photographs
  -> intake and quality checks
  -> masking / segmentation
  -> pose estimation and sparse reconstruction
  -> optional bundle adjustment
  -> dense or Gaussian reconstruction
  -> mesh extraction
  -> cleanup, texture/color handling, and export
  -> appearance, geometry, runtime, memory, and failure evaluation
```

Every stage should emit a manifest, configuration, logs, outputs, and a clear failure state. Derived inputs should never overwrite source photographs.

## Input and masking

Background masking is a first-order requirement for turntable captures. A static background can dominate feature matching while the specimen rotates, causing structure-from-motion to reconstruct the room or table instead of the object.

Important findings:

- In July 2026, the team discovered that its earlier COLMAP path was not applying masks. Correct masked COLMAP results were substantially better than VGGT on the tested specimens.
- Blacked-out RGB backgrounds and alpha-channel PNGs were both discussed. RealityScan also offers AI masking.
- Masks can introduce rough edges or remove thin anatomical parts, so previews and edge-quality checks are needed.
- Pre-cropping can preserve more specimen detail before models such as VGGT downsample the input.

## Pose estimation

### COLMAP

Current stable default. It performs feature extraction, matching, geometric verification, incremental registration, triangulation, and bundle adjustment. Correct masking made COLMAP both accurate and practical for the project’s turntable captures.

### VGGT

Useful as a fast feed-forward alternative or rescue path when classical registration is incomplete. Earlier experiments found substantial GPU-memory pressure as image count and resolution increased. Standalone VGGT was faster in the Spring 2026 report but slightly weaker geometrically; VGGT with bundle adjustment improved poses but remained resource intensive.

### Other explored pose paths

- VGG-TTT: test-time training; results in the Summer 2026 report were weaker than COLMAP on the mammal skull set.
- Pi3: lower-memory dense reconstruction was promising, but OpenCV camera-to-world output could not yet be converted reliably into COLMAP binaries.
- GLOMAP, FastMap, Depth Anything 3, and VGGT-Omega were identified as candidates for future evaluation.
- Metashape can provide a commercial pose-and-mesh path where RealityScan is unavailable, including macOS workflows.

## Surface reconstruction

### 2D Gaussian Splatting

Strong visual fidelity from good COLMAP poses. It remains sensitive to background and masks, but the corrected COLMAP-plus-2DGS path produced strong splats across specimens. It is also the leading candidate for visual-hull initialization or regularization research.

Ihor's Fall Week 1 ablation compared masked-COLMAP sparse initialization with visual-hull initialization across five specimens, two resolutions, and 20 matched 2DGS runs. Hull initialization improved LPIPS in all ten paired comparisons, SSIM in nine, and PSNR in seven, but the extracted meshes differed by only 0.08-0.58% of the bounding-box diagonal. On three of five specimens this was no more than normal unseeded retraining variation. The current conclusion is not to replace masked COLMAP initialization yet: silhouette regularization that remains active during optimization and a hybrid SfM-plus-hull seed are stronger next experiments.

The same study found that merging two turntable positions costs roughly 1.8 dB in appearance quality because inversion changes surface illumination. The measured between-position RGB variation was 2.46 times the within-position control. This creates a trade-off between geometric completeness and appearance fidelity and motivates per-position appearance modeling or calibration.

### PGSR

Adds plane and multi-view geometric constraints to Gaussian reconstruction and can extract TSDF-based meshes. It produced the best Gaussian-family mesh reported in an April 2026 masked VGGT-BA experiment and later delivered the best appearance/meshability trade-off in Tianshu Wu’s evaluation. Its geometric losses are sensitive to pose quality.

### SuGaR

Regularizes Gaussians toward surfaces and offers detailed mesh extraction and refinement. Earlier tests produced attractive renders but inconsistent or noisy meshes on specimen data.

### Gaussian Wrapping

In Syed Fahad Rizvi’s Spring 2026 study, Gaussian Wrapping gave the strongest balance of geometric fidelity and runtime among the evaluated extractors. Background masking logic and parameters still required tuning.

### MILo, Plenoxels, 3DGS, MVSGaussian

These were evaluated or proposed as complementary rendering and mesh paths. Tianshu Wu’s work found MILo and PGSR capable of recovering cranial geometry under the same strong COLMAP poses, with different failure modes.

### Earlier SDF and meshing work

The 2025 team explored OpenMVS, Poisson reconstruction, NeuS2, Neuralangelo, VolSDF, HeatSDF, marching cubes, and Instant-NGP components. Key lessons were that fast Poisson reconstruction sacrifices photogrammetric fidelity, SDF methods are sensitive to camera conventions and build environments, and high-quality training can require long GPU runs. These approaches remain useful historical experiments, but they are not the current default path.

On 2 October 2026, Syed asked Mohamed and Om to revisit neural implicit surface reconstruction so the evaluation is broader than Meshroom versus 3DGS. Neuralangelo, NeuS2, and NeuS are the named starting points. The renewed test must use background masks: the historical attempts did not account for masking, while masking subsequently produced the largest gains for the Gaussian-family methods. First select one maintained, camera-compatible implementation and run a provenance-complete masked baseline before expanding the method set.

## Mesh processing and exports

Recommended common processing:

- Remove small disconnected components.
- Compute and validate normals.
- Check holes, manifoldness, and self-intersections.
- Preserve or bake color/texture when supported.
- Record every cleanup operation.
- Export PLY or OBJ for analysis and GLB for web use.

Keep high-resolution reference geometry. Simplified meshes may be generated later with texture transferred from the high-poly model.

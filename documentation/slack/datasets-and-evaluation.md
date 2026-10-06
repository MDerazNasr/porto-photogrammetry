# Datasets and Evaluation

## Project datasets

### UF museum captures

Frequently referenced sets include:

- `UF_mammals_36342_skull`: the primary skull benchmark used across multiple semesters.
- `UF_Herp_3998`: a herpetology skull/specimen set used in comparative evaluation.
- Bird/ivory captures: useful for studying incomplete COLMAP registration and learned-pose fallbacks.
- Fish and lionfish captures: part of the early museum-data and MapAnything/VGGT discussions.

The captures commonly use fixed cameras around a rotating turntable. This is operationally convenient but violates the naive assumption that moving cameras around a static scene and rotating an object in a static scene are always equivalent for every reconstruction method.

Direct inspection on 21 September 2026 established that the `scale/` sequences use PhotoModeler coded scale bars, while colour references are stored separately at the root of a specimen's `images/` directory. Across 460 photographs from `UF_mammals_36342_skull/images/scale`, `UF_Herp_3998/images/scale`, and `UF_birds_ivory2/images/scale`, the visible scale references are coded bars rather than multi-patch charts. A skull marker is labelled `0.05 m` and uses coded targets `156` and `157`, making it suitable for metric scaling. A surrogate Imageomics test using that bar reduced local histogram distance but altered the full target image by 32.012 intensity levels on average, increased clipped pixels from 0.006% to 0.894%, and introduced a visible colour cast. Scale bars must therefore not be used for colour calibration.

The same archive does contain genuine 24-patch ColorChecker references for `UF_Herp_3998`, one per camera:

- `UF_Herp_3998/images/camera1_IMG_9401.JPG`
- `UF_Herp_3998/images/camera2_IMG_8226.JPG`
- `UF_Herp_3998/images/camera3_IMG_6883.JPG`

These reference frames sit outside both `scale/` and `noscale/`, which is why a folder-only sweep missed them. Each image also has a specimen mask, but the supplied masks do not isolate the chart.

The Imageomics histogram-matching pipeline ran successfully on manually isolated chart polygons, but it is unsuitable as-is. It made chart histograms numerically similar while worsening camera 2's mean 24-patch error from 12.39 to 17.99 ΔE76, changing the full image by 28.66 intensity levels on average, and producing a visibly washed-out result. Camera 3 received a severe dark/magenta-green cast. A patch-correspondence method is therefore required.

A linear-RGB 3×3 transform fitted from the 24 corresponding patch interiors produced stable results. Relative to camera 1, camera 2's mean patch error fell from 9.29 to 3.11 ΔE76 and camera 3's from 3.74 to 1.47. Mean whole-image changes were 9.48 and 6.70 intensity levels respectively, with visually natural outputs. The recommended implementation is one transform per camera/lighting group, fitted from its chart reference and applied to that group's reconstruction images. Camera 2's white background clips more after exposure matching, so clipping should be reported and either accepted for background-only pixels or controlled with highlight-preserving exposure handling.

### Shared museum sources

- Florida Museum Sketchfab models and a fossil-hall example.
- MorphoSource project `000381689`; many downloads require per-item rights, so project-wide access from the museum contact was requested.
- RealityScan outputs produced from masked data and placed in HiperGator Blue storage at `/blue/arthur.porto/data/datasets/photogrammetry/realityscan`.
- A cleaned Fall 2026 candidate dataset was staged at `/blue/arthur.porto/data/datasets/photogrammetry/neurips/raw` on 6 September.
- Historical Dropbox folders containing source images and prior outputs. Consult the local private link catalog rather than copying share tokens into public documentation.

### Fall 2026 rigid-specimen shortlist

Syed Fahad Rizvi shortlisted 42 specimens judged suitable for the rigidity requirement: 34 mammals, five reptiles, and three fish. The local private attachment archive preserves the linked table as `F0BUX72BSAW-specimens_table.pdf`. Availability and final inclusion still need confirmation with Arthur Porto and Zach Randall.

Zach reported eight existing photogrammetry objects with corresponding structured-light scans. Four were explicitly linked in Slack: `UF:Mammals:1769` (*Ateles belzebuth*), `UF:Mammals:14760` (*Hylobates lar*), `UF:Mammals:19126` (*Speothos venaticus*), and `UF:Mammals:26153` (*Neofelis nebulosa*). The short-term evaluation plan requests all eight paired scans; the final dataset may require structured-light scans for a selected subset of roughly 50-60 photogrammetry captures.

On 22 September Syed reported that all 76 current specimen elements had new SAM 3 masks and that the prepared dataset was available under `/blue/arthur.porto/data/datasets/photogrammetry/neurips/prepared`.

The structured-light meshes shared on 11 September appeared visibly decimated to Ihor and contained roughly one tenth the points/faces of prior RealityScan outputs. Arthur could not locate denser exports; Zach believed the supplied files were the highest-resolution meshes the scanner software could output, but confirmation was still pending on 18 September. Vertex count alone is not an adequate quality test, so the team should inspect retained anatomical detail and scanner precision before designating these files authoritative ground truth.

### Public and external datasets

- BlendedMVS: early standard benchmark reference.
- SALVE: consumer-video wound reconstruction benchmark; the Slack review noted that it contains only a small number of wounds.
- DTU: proposed for geometry evaluation because reference scans and known cameras support quantitative comparisons.

## Ground truth strategy

RealityScan and Metashape are useful practical references but are not true geometric ground truth. Earlier comparisons were complicated by table, label, and background geometry in commercial outputs.

Preferred hierarchy as of 11 September 2026:

1. Structured-light scans of the external surface, preferably captured close in time to photography.
2. CT-derived specimen geometry, if licensing and alignment permit and the external surface can be isolated reliably.
3. Public scans with known reference geometry, such as DTU.
4. Matched masked captures processed by commercial and open-source baselines.
5. Qualitative expert review when no independent scan exists.

If CT geometry regularizes a reconstruction method, it cannot also serve as an independent ground-truth test for that same experiment.

The museum has an Artec Space Spider used for mammal skulls, an Artec Micro II, and an Artec Leo. The Space Spider was identified as the best-resolution option for the current target size range. Dry skeletal specimens are preferred because wet specimens may shrink or change pose between photography and reference scanning.

## Evaluation matrix

Evaluate pose and reconstruction independently while using a shared data contract.

### Pose candidates

- COLMAP.
- VGGT.
- VGGT plus bundle adjustment.
- Selected emerging methods only when compute permits.

### Reconstruction candidates

- 2DGS.
- PGSR.
- SuGaR.
- Gaussian Wrapping.
- MILo or another focused extension when justified.

### Metrics

- Geometry: Chamfer distance, F-score, normal consistency, completeness, holes, floaters, connected components, and watertightness.
- Appearance: foreground PSNR, SSIM, and LPIPS on a fixed held-out split.
- Operations: runtime, peak GPU memory, storage, failure rate, repeatability, and number of registered views.
- Pose diagnostics: reprojection error, track counts, scene scale, and camera coverage.

## Dataset-paper design axes

To make the benchmark scientifically compelling, sample across:

- Taxonomic biodiversity.
- Soft to hard tissue.
- Complete specimens to partial fossils.
- Smooth/texture-poor to richly textured surfaces.
- Simple shell-like geometry to skulls and complex thin structures.
- Controlled turntable captures and selected field photogrammetry.

A large sample of relatively simple freshwater mussels could establish statistical breadth, paired with a smaller but more challenging skull/fossil subset.

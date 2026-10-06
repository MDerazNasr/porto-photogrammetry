# Dense geometry-impact evaluation readiness — 2 October 2026

## Outcome

The colour-calibration geometry-impact evaluation cannot yet be upgraded from the existing sparse-Delaunay regression proxy to a defensible dense/reference-mesh comparison. The limiting dependency is a valid matched dataset and reachable dense-compute environment, not an unimplemented metric.

Do not use the historical unlabeled PLY attachments as evidence for PR 18. Their specimen, reconstruction settings, reference relationship, and calibration condition cannot be established.

## Evidence checked

- The current proxy result is `outputs/color-calibration-mesh-regression-uf-birds-ivory2-2026-09-25.json`. It compares sparse-Delaunay surfaces, has no physical scale or external reference, and must remain described as a regression check rather than anatomical accuracy evidence.
- Six multi-megabyte `mesh_coarse_res256` / `mesh_stage_mid_res256` PLY attachments are present locally, but their Slack context only says the camera needs adjustment for benchmarks. There is no reliable specimen or before/after calibration identity.
- The named VGGT and COLMAP PLY attachments are sparse point clouds, not dense meshes or a structured-light reference pair.
- Project notes identify paired structured-light scans in the broader study, including four linked specimen records, but no corresponding usable mesh files or current storage path are available locally.
- A read-only SSH probe to `login-ice.pace.gatech.edu` timed out on port 22 on 2 October, so the expected PACE-side assets and reconstruction environment could not be inspected.
- A Slack sweep through 2 October found no newly shared mesh or path. On 1 October, Syed asked Arthur for a CT specimen; Arthur said he would look for one with both CT and photogrammetry. Syed also said densely tessellated structured-light scans remain preferred.

## Fixed evaluation protocol once the dependency arrives

1. Select one specimen for which the exact same photographs, masks, camera/reconstruction settings, and code commit can be used in both conditions.
2. Produce two dense reconstructions on the same hardware: original images and colour-calibrated images. Record the GPU/CPU, allocation, wall-clock time, environment, config, and commit.
3. Use one independently acquired, densely tessellated structured-light reference mesh for both comparisons. A CT surface is acceptable for exploratory framework work, but modality/segmentation differences must be stated.
4. Apply the same preprocessing, crop/evaluation domain, scale convention, and registration procedure to both reconstructions. Preserve all transform and metric artifacts.
5. Evaluate both meshes against the same reference using the PR 19 mesh-evaluation implementation after its review issues are resolved. At minimum report registration outcome, vertex/face counts, accuracy, completeness, F-score at fixed thresholds, and the robust scale used for normalized distances.
6. Report the paired delta (calibrated minus original), not two isolated scores. Treat negligible movement as preservation evidence; do not claim anatomical improvement unless it exceeds method variability and is consistent across specimens.
7. Repeat on additional specimens before making a general geometry claim.

## Acceptance criteria for closing the checklist item

- Provenance is complete for the images, masks, both dense meshes, and reference mesh.
- Before/after runs differ only by the colour-correction stage.
- Runtime and hardware metadata are recorded.
- Both conditions are evaluated over the same physical domain with the same settings.
- Raw metrics and machine-readable artifacts are retained.
- PR 18 wording distinguishes preservation, improvement, and inconclusive results.

## Immediate unblock request

Obtain either (preferably both):

- the storage path/access instructions for one of the existing densely tessellated structured-light reference meshes and its matched photogrammetry source set; or
- the CT-plus-photogrammetry specimen Arthur is locating, with enough provenance to construct a paired evaluation.

Once one valid specimen is accessible and a CUDA reconstruction host is reachable, the protocol above is ready to run without another scoping pass.

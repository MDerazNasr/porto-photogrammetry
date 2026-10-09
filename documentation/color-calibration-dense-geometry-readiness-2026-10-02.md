# Dense geometry-impact evaluation readiness — 2 October 2026

## Outcome

The colour-calibration geometry-impact evaluation cannot yet be upgraded from the existing sparse-Delaunay regression proxy to a defensible dense/reference-mesh comparison. A matched public specimen has now been identified, but the required source bundles, Syed's derived CT surface, and a reachable dense-compute environment are not yet available locally. The remaining limitation is access/execution, not an unimplemented metric.

Do not use the historical unlabeled PLY attachments as evidence for PR 18. Their specimen, reconstruction settings, reference relationship, and calibration condition cannot be established.

## Evidence checked

- The current proxy result is `outputs/color-calibration-mesh-regression-uf-birds-ivory2-2026-09-25.json`. It compares sparse-Delaunay surfaces, has no physical scale or external reference, and must remain described as a regression check rather than anatomical accuracy evidence.
- Six multi-megabyte `mesh_coarse_res256` / `mesh_stage_mid_res256` PLY attachments are present locally, but their Slack context only says the camera needs adjustment for benchmarks. There is no reliable specimen or before/after calibration identity.
- The named VGGT and COLMAP PLY attachments are sparse point clouds, not dense meshes or a structured-light reference pair.
- Project notes identify paired structured-light scans in the broader study, including four linked specimen records, but no corresponding usable mesh files or current storage path are available locally.
- A read-only SSH probe to `login-ice.pace.gatech.edu` timed out on port 22 on 2 October, so the expected PACE-side assets and reconstruction environment could not be inspected.
- A Slack sweep through 2 October found no newly shared mesh or path. On 1 October, Syed asked Arthur for a CT specimen; Arthur said he would look for one with both CT and photogrammetry. Syed also said densely tessellated structured-light scans remain preferred.

## Matched specimen identified on 9 October

Syed's 3 October Slack update names `UF:Herp:84427` (`Gopherus polyphemus`) and shows a CT-derived surface produced with Otsu thresholding, outside-in ray filtering, and marching cubes. The Slack attachment is a screenshot only; the derived mesh, script, parameters, and storage path were not attached, and the message has no thread replies.

Mohamed posted the matched-record finding and the precise asset/provenance request in Syed's thread on 9 October: https://humanaugmente-e7j6563.slack.com/archives/C08TNEM1WHF/p1791552733461409?thread_ts=1791047751.260929&cid=C08TNEM1WHF

The public MorphoSource API confirms that physical object `000484506` has all three relevant open media records:

| Media ID | Record | File metadata | Role |
|---|---|---|---|
| `000574722` | `Dice Ct [CTImageSeries] [CT]` | `UF-herp-84427-diceCT.zip`, 2,541,368,544 bytes, 1,809 TIFF slices, 0.04222976 mm isotropic spacing | CT source/reference candidate |
| `000484510` | `Element Unspecified [PhotogrammetryImageSeries] [Photogram]` | `Image_series.zip`, 1,474,776,814 bytes, 437 JPEGs at 6240 x 4160 | matched reconstruction source |
| `000484545` | `Preserved Head [Mesh] [Photogram]` | `Morphosource.zip`, 95,420,789 bytes, OBJ with 1,363,478 points and 2,726,960 faces | existing photogrammetry baseline/reference check |

The CT and photogrammetry records refer to the same physical-object ID, but this does not by itself prove identical pose, crop, or surface domain. The photogrammetry mesh is a prior reconstruction, not the required controlled original-versus-calibrated pair. The image bundle must also be inspected for camera-specific colour-chart frames before this specimen can exercise PR 18's calibrated condition.

The public representative thumbnail for media `000484510` shows the preserved head, foam support, and a coded metric bar; no colour chart is visible in that one preview. This is not evidence that the 437-image bundle lacks separate chart frames. The IIIF manifest requires authentication, so the remaining frames cannot be inventoried through the public preview interface.

MorphoSource's official REST specification requires a user API key, a download-use statement of at least 50 characters, a use category (or custom category), and explicit acceptance of the applicable agreements before it returns a direct download URL. The current shell has no `MORPHOSOURCE_API_KEY`; download must therefore wait for the user to configure credentials and authorize agreement acceptance. Do not place the key in source control, logs, chat, or documentation.

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

Obtain:

- user-authorized access to the open MorphoSource bundles for media `000574722`, `000484510`, and `000484545` (configure `MORPHOSOURCE_API_KEY` outside source control and explicitly accept the applicable use agreements);
- Syed's derived CT mesh, script/commit, parameters, and transform/provenance, or permission and compute to reproduce it from the CT bundle; and
- confirmation that the 437-image photogrammetry bundle contains usable colour-reference frames. If it does not, use a different same-specimen capture with chart measurements or treat `UF:Herp:84427` only as geometry-framework validation.

The existing structured-light option remains preferred if its matched source set becomes available. Once the bundles and a CUDA reconstruction host are reachable, the protocol above is ready to run without another scoping pass.

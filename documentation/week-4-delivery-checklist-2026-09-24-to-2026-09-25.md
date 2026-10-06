# Week 4 Delivery Checklist: September 24-25, 2026

## Friday outcome

Ship a reviewable colour-calibration contribution that the team can inspect without reconstructing the experiment from notes. The minimum deliverable is a clean feature branch plus a reproducible demo bundle. Open a pull request if repository permissions and fork configuration are ready; otherwise publish the branch/patch and PR-ready description as the artifact.

## 1. Freeze the scope

- [ ] Limit this delivery to relative per-camera colour calibration using the validated 3 by 3 linear-RGB transform.
- [ ] Treat camera 1 as the reference; do not claim absolute calibration.
- [ ] Keep metric scaling, automatic chart detection, second-specimen testing, dense reconstruction, and higher-order transforms out of this PR.
- [ ] State the acceptance criteria: lower chart-patch Delta E76, no skipped files, preserved masks and metadata, and no loss of COLMAP registration.

## 2. Prepare a reviewable branch

- [x] Create and configure the `MDerazNasr/porto-photogrammetry` GitHub fork while retaining the organization repository as `upstream`.
- [x] Create `mohamed/color-calibration` from the current `upstream/main` baseline.
- [x] Move only the intended implementation into the branch:
  - [x] `src/augenblick/preparation/color.py`
  - [x] `src/augenblick/cli/main.py`
  - [x] `tests/test_color.py`
  - [x] `examples/color/uf_herp_3998.json`
  - [x] README usage documentation
- [x] Review the diff for private paths, dataset URLs, generated outputs, and unrelated changes.
- [x] Confirm that no source photographs, private Slack records, credentials, or restricted dataset files are staged.

## 3. Re-run the release checks

- [x] Run the nine focused colour-calibration tests.
- [x] Run the CPU-safe repository test set. Seventy-two relevant tests passed; one unchanged upstream scene fixture fails because it omits `images/`, and NVS collection still requires PyTorch.
- [x] Run Ruff, compilation, and whitespace/diff checks.
- [x] Run `augenblick color --help` in the lightweight environment to verify lazy backend loading.
- [ ] Re-run a one-image-per-camera smoke test from the documented example configuration.
- [ ] Confirm the output report contains matrices, patch centres, Delta E76, clipping diagnostics, processed counts, and skipped files.
- [ ] Record exact commands, environment, commit, and pass/fail results in the demo README.

## 4. Build the demo artifact

- [x] Create a compact, redistributable synthetic demo that can be reviewed independently of the private dataset.
- [x] Add a short README containing:
  - [x] the problem and why histogram matching was rejected;
  - [x] the command to run `augenblick color`;
  - [x] required input layout and four-corner configuration format;
  - [x] output layout and safety behavior;
  - [x] limitations and non-claims.
- [x] Include a generator that emits the complete sanitized example configuration and inputs.
- [ ] Include one before/after comparison figure using publishable images or approved crops.
- [x] Include the patch-error table:
  - [x] Camera 2: 9.218 to 3.131 Delta E76;
  - [x] Camera 3: 3.698 to 1.432 Delta E76.
- [x] Include the COLMAP regression summary:
  - [x] 36/36 registrations before and after;
  - [x] 28,084 to 28,658 verified inliers;
  - [x] 3,845 to 3,929 sparse points;
  - [x] 0.670 to 0.676 px mean reprojection error.
- [x] Include file-preservation evidence: masks/reference files byte-identical, 6240 by 4160 dimensions retained, and sampled EXIF tags preserved.
- [ ] Link the full machine-readable reports without adding private source data to Git.

## 5. Package the review request

- [x] Write the concise PR title `Add per-camera ColorChecker calibration command`.
- [x] In the PR description, include:
  - [x] motivation;
  - [x] implementation summary;
  - [x] exact validation performed;
  - [x] quantitative results;
  - [x] known limitations;
  - [x] reviewer instructions.
- [x] Explicitly say that sparse geometry was preserved, not improved.
- [x] Explicitly say that current calibration is relative, not absolute.
- [ ] Request review from the appropriate pipeline owner and from Om to confirm there is no duplicate effort.
- [x] Open upstream pull request 18: `https://github.com/Human-Augment-Analytics/porto-photogrammetry/pull/18`.

## 6. Show the team

- [ ] Post one concise Slack update containing:
  - [ ] branch or PR link;
  - [ ] demo/artifact link;
  - [ ] before/after figure;
  - [ ] Delta E76 results;
  - [ ] COLMAP regression conclusion;
  - [ ] two requested review questions.
- [ ] Ask reviewers specifically whether the CLI/config interface is acceptable and whether specimen-mask clipping should be required before merge.
- [ ] Record reviewer feedback and convert it into named follow-up issues rather than expanding this delivery indefinitely.

## Definition of done

This week is complete when another team member can open one link, understand the method and evidence, run the documented command, review the code diff, and leave actionable feedback. A report alone does not satisfy the milestone.

## Follow-ups after delivery

- [x] Add specimen-mask-only clipping metrics and choose a warning threshold.
- [x] Locate a second specimen with per-camera chart references and repeat the validation (`UF_birds_ivory2`: 138 images across three usable cameras; camera 4 chart is occluded).
- [ ] Confirm the ColorChecker make and patch-value edition before absolute calibration.
- [x] Add mesh-level validation (controlled 36-view original/calibrated sparse-Delaunay comparison; full CUDA dense MVS remains an explicitly documented limitation).
- [ ] Compare a root-polynomial model only if held-out patch validation justifies the added complexity.

# Coded-marker scale integration review - 2 October 2026

## Outcome

Do not create a second scale-recovery implementation. Ihor's open PR 19 already provides the project-level metric-scale stage: `augenblick.eval.scale`, sliding-window triangulation, predeclared acceptance gates, a withheld check bar, COLMAP-gauge hashes, metric mesh export, documentation, and focused tests.

Mohamed's useful contribution should begin after PR 19's correctness issues are resolved and should be one of:

1. independent validation on another specimen;
2. integration/UX work around producing the required detections JSON; or
3. a controlled colour-calibration versus marker-localization interaction test.

## Existing implementation and evidence

- PR: `Human-Augment-Analytics/porto-photogrammetry#19`, branch `ihor/eval-framework`.
- Primary bar detector codes: `1675`, `1419`; check bar codes: `1181`, `1949`.
- Printed identities documented by Ihor: primary labels `162`, `163`; check labels `114`, `115`.
- Nominal centre-to-centre length: 100 mm per bar.
- Accepted mandible result: 118.97 mm/model-unit, 14/27 passing windows, 0.26% primary spread, at most 0.40% check-bar error.
- Cranium result: rejected because passing detections covered only one ring.

## Independent checks

- PR 18 and PR 19 touch separate functional areas. PR 18 changes preparation/colour and CLI files; PR 19 changes evaluation, scene, and SfM files. No direct merge conflict was found.
- `tests/test_eval_scale.py`: 14 passed; six optional Open3D export tests skipped because Open3D was not installed.
- `tests/test_eval_mesh.py`: 14 passed; seven optional Open3D/trimesh tests skipped.
- Combined scale/scene/COLMAP subset: 26 passed, six skipped, three failed on macOS because the new test attempts to monkeypatch Linux-only `os.sched_getaffinity` without `raising=False`. This is a portability issue in the unrelated CPU-allocation change, not a scale-algorithm failure.
- `git diff --check` reports CRLF/trailing-whitespace issues throughout `docs/scale-protocol.md` and one extra EOF blank line in `mesh.py`.

## Open correctness issues already raised on PR 19

Syed's review identified two unresolved scale-path edge cases:

1. Rings shorter than the 24-view window wrap and repeat images, which can leak the same observation into training and held-out sets. Short rings must be rejected and every window must contain 24 distinct images.
2. A capture with only one inferred ring cannot pass the required two-ring gate, yet the current CLI performs all work and reports only a generic rejection. The required `capture_manifest.json` format is not documented or produced elsewhere in the repository.

## Additional integration boundary

Despite the PR title mentioning detection, the committed scale module consumes a precomputed detections JSON; the PGT-Toolkit detector and codebook-generation path are out of scope and not included. This is the clearest non-overlapping integration opportunity after PR 19 stabilizes.

The exporter records COLMAP model hashes, but callers must still ensure that the supplied mesh was produced in that exact model gauge. No automatic mesh-to-model provenance verification currently exists.

## Recommendation

Wait for Ihor to address the two correctness comments or merge PR 19 with follow-up issues. Then select one independent specimen with adequate bar visibility and validate the full path from detection JSON through accepted/rejected scale output. Do not copy the 118.97 factor to another reconstruction: it belongs only to the hashed COLMAP gauge from which it was estimated.

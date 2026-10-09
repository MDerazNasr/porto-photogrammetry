# Coded-marker scale integration review - 2 October 2026

## Outcome

Do not create a second scale-recovery implementation. Ihor's merged PR 19 provides the project-level metric-scale stage: `augenblick.eval.scale`, sliding-window triangulation, predeclared acceptance gates, a withheld check bar, COLMAP-gauge hashes, metric mesh export, documentation, and focused tests.

Mohamed's selected complementary contribution is integration/UX around producing the required detections JSON. The colour stage must remain upstream-independent: scale detection reads the original unmasked photographs, not colour-corrected outputs. Independent-specimen validation remains useful once a detector and suitable capture are available.

The considered complementary options were:

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

## Post-merge closure - 9 October

PR 19 merged into canonical `main` at `874bf10`; the follow-up commit `17216f1` resolves both review issues. Rings shorter than the 24-view window are now recorded and skipped, preventing repeated-view leakage, and captures with fewer than two usable rings now receive an explicit up-front explanation. The merged protocol also documents the optional `capture_manifest.json` format.

Mohamed reran the exact merged scale suite from canonical `main` commit `78505d0` in an isolated temporary environment with `pycolmap 4.2.1`: **16 tests passed and 6 optional Open3D tests skipped**. This closes the correctness wait in the integration review.

## Additional integration boundary

Despite the PR title mentioning detection, the committed scale module consumes a precomputed detections JSON; the PGT-Toolkit detector and codebook-generation path are out of scope and not included. This is the clearest non-overlapping integration opportunity after PR 19 stabilizes.

The exporter records COLMAP model hashes, but callers must still ensure that the supplied mesh was produced in that exact model gauge. No automatic mesh-to-model provenance verification currently exists.

## Recommendation

Treat PR 19 as the accepted scale owner. The next non-duplicative implementation is a reproducible detector-to-JSON adapter with printed-label/codebook verification and a command-level handoff into `augenblick.eval.scale`; it should be validated on an independent specimen with adequate bar visibility. Do not copy the 118.97 factor to another reconstruction: it belongs only to the hashed COLMAP gauge from which it was estimated.

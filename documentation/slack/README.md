# Porto Photogrammetry Slack Wiki

This wiki distills the working knowledge in the private `#porto-photogrammetry` Slack channel from its creation on 21 May 2025 through 24 September 2026. It is organized for onboarding, research planning, and documentation maintenance rather than as a replacement for Slack.

## Start here

- [Project overview](project-overview.md): mission, users, success criteria, and current direction.
- [Pipeline and methods](pipeline-and-methods.md): the reconstruction stages, supported methods, and lessons learned.
- [Datasets and evaluation](datasets-and-evaluation.md): museum data, baselines, metrics, and proposed publication scope.
- [Results and reports](results-and-reports.md): semester outputs and the strongest findings to date.
- [Infrastructure and access](infrastructure-and-access.md): repository, HiperGator, PACE, storage, and known blockers.
- [Decisions and open questions](decisions-and-open-questions.md): settled choices, unresolved issues, and next actions.
- [Meetings and working process](meetings-and-process.md): meeting cadence, reporting, and communication norms.
- [People and roles](people-and-roles.md): project leadership and contributors by phase.
- [Timeline](timeline.md): major changes from 2025 exploration to the 2026 benchmark/publication direction.
- [Attachment guide](attachment-guide.md): locally archived reports, images, meshes, and import limitations.
- [Source policy](source-policy.md): provenance, privacy, refresh rules, and the local-only archive.

## Current snapshot

The project aims to turn multi-view photographs of museum specimens into accurate, colored 3D assets for morphometrics, color analysis, documentation, and outreach. The technical direction has converged on masked COLMAP as the stable pose-estimation default, with Gaussian-based surface reconstruction methods evaluated behind a modular interface. The emerging publication direction is a challenging biodiversity dataset and benchmark using structured-light scans as practical external-surface ground truth and testing variation in tissue, geometry, completeness, and capture conditions.

By 24 September, 42 rigid specimens had been shortlisted, all 76 current specimen elements had new SAM 3 masks, and the prepared dataset was staged under the `neurips/prepared` Blue-storage path. Four paired structured-light models were explicitly linked, with eight paired photogrammetry/light-scan specimens reported as available. The available scanner meshes may be decimated, so their retained detail and suitability as geometric ground truth still require confirmation. The colour-calibration pilot passed its initial batch and sparse-COLMAP gates. The main remaining dependencies are ground-truth validation, final benchmark selection, broader calibration/evaluation, and coordinated compute use.

## Local private archive

The local checkout also contains an ignored archive of channel messages, expanded threads, links, and permitted attachments. The latest compact refresh covers activity through 2 October 2026, including Meeting 4 additions, publication-analysis guidance, active-PR merge order, and Syed's neural-implicit-method request to Mohamed and Om. These materials are deliberately excluded from Git because this repository is public and the source channel is private.

# Project Overview

## Mission

Build an open-source, end-to-end photogrammetry pipeline that converts photographs captured in labs, museums, and field settings into high-quality 3D models with rich color information.

The intended downstream uses are:

- Morphometric measurement and biological analysis.
- Color analysis.
- Museum documentation and digital archiving.
- Research datasets and reproducible method comparisons.
- Outreach, visualization, and web-accessible specimen models.

## What “good” means

The project values scientific usefulness over game-ready efficiency. High-poly geometry, anatomical fidelity, watertight or near-watertight surfaces, and reliable color are more important than minimizing polygon count. A useful system should also be reproducible: stages must have stable inputs and outputs, captured environments, logs, fixed configurations, and explicit failures.

Two output qualities must be evaluated separately:

1. **Appearance quality:** novel-view rendering, color, PSNR, SSIM, and LPIPS.
2. **Geometry quality:** surface completeness, floaters, holes, thin structures, anatomical detail, Chamfer distance, F-score, and normal consistency when ground truth exists.

High rendering scores do not guarantee a scientifically useful mesh.

## Current research direction

By August 2026 the team was considering a dataset/benchmark paper as the safest central contribution. The proposed differentiators are:

- Broad biodiversity rather than only buildings, facades, or simple consumer scans.
- Specimens spanning soft to hard tissue.
- Complete specimens and partial fossil material.
- Controlled lab captures plus selected field photogrammetry.
- Structured-light external-surface scans as the practical first source of quantitative ground truth, with CT-derived geometry where useful and licensable.
- Matched commercial and open-source baselines.

Method novelty can be layered on top. A controlled Fall Week 1 study found that visual-hull initialization improved novel-view metrics but did not materially change extracted meshes. Silhouette regularization that remains active during optimization, plus hybrid SfM-and-hull initialization, are now the stronger variants to test for texture-poor specimens.

## Canonical repository

The team moved away from older personal Augenblick repositories to the Human Augment Analytics organization repository. The repository was renamed in August 2026 to remove a trailing dash. Confirm the current remote before following older Slack links because several historical URLs retain the previous name.

## Scope boundaries

- The pipeline integrates and evaluates existing methods; it does not require inventing a new renderer.
- COLMAP format is the common interchange contract for cameras, images, and sparse points.
- Commercial tools such as RealityScan and Metashape are references or baselines, not dependencies of the open-source deliverable.
- Raw source images must remain unchanged; masks and derived inputs should be saved separately.

# Attachment Guide

## Import summary

The initial private archive discovered 110 unique Slack file IDs; later refreshes are recorded separately.

- 104 files have been imported locally, including Mohamed's late Week 3 report from the 24 September refresh.
- Imported content includes roughly 31 PDFs, 57 images, eight binary mesh/point-cloud files, one Python script, one text/Slack canvas document, and one ZIP archive.
- File names are prefixed with the immutable Slack file ID to avoid collisions.
- Detailed per-file manifests are stored locally under the ignored `inventory/` directory.

## Major document groups

- Syed Fahad Rizvi weekly reports, research proposal, and Spring 2026 final report.
- Tianshu Wu weekly reports and Summer 2026 final report.
- Ihor Vilkhovyi weekly reports that fit within the connector limit.
- Contributor reports and project-advertisement material.
- Comparative renders for COLMAP, VGGT, RealityScan, Meshroom, PGSR, 2DGS, Gaussian Wrapping, and turntable experiments.
- PLY point clouds and meshes for reconstruction comparisons.
- The Slack Project Overview canvas and a small pipeline script.
- Fall 2026 Week 1 reports from Mohamed Deraz Nasr, Om Kshatriya, and Ihor Vilkhovyi, plus the 42-specimen shortlist.
- Mohamed Deraz Nasr's late-submitted Fall 2026 Week 3 report (`F0C44RGD14H`).

## Files not retrievable through Slack connector

The connector enforces a 10 MB read limit. These 11 files remain indexed by Slack ID and original metadata:

| Slack ID | File | Slack size | Notes |
|---|---|---:|---|
| `F09MBMM2N8Z` | `mesh_mid_res512.ply` | 19.6 MB | High-resolution 2025 mesh |
| `F0AMZ2A79LN` | `vggt_depth_output.ply` | 45.3 MB | VGGT depth point cloud |
| `F0AMZ2DJ4BY` | `vggt_w_mask_depth_output.ply` | 49.9 MB | Masked VGGT depth point cloud |
| `F0B1R9QUQF7` | `Rizvi_Porto_Lab_Spring_26_Report.pdf` | 46.0 MB | A separate copy already exists in the repository documentation folder |
| `F0BF00KCKG9` | `noscale.ply` | 61.4 MB | Large no-scale reconstruction |
| `F0BGDTV91K7` | `full_comparison (1).png` | 10.5 MB | Turntable/pose comparison |
| `F0BGH69NK0S` | `Ihor Vilkhovyi week 6.pdf` | 11.2 MB | Weekly report |
| `F0BHLNFP5RA` | `Ihor Vilkhovyi week 7.pdf` | 22.7 MB | Weekly report |
| `F0BKKHV3S05` | `splat_mesh_rs_two_row_2dgs.png` | 25.1 MB | High-resolution comparison chart |
| `F0BLH6GFC56` | `Ihor Vilkhovyi week 8.pdf` | 25.8 MB | Weekly report |
| `F0BLNAT4P25` | `Ihor Vilkhovyi Summer final.pdf` | 48.3 MB | Summer final report |

## Preservation rules

- Do not rename imported files without retaining the Slack ID.
- Do not edit originals; create derived summaries or thumbnails separately.
- Store large experiment artifacts in project storage, not Git.
- Before publishing any attachment, verify ownership, consent, and licensing.

#!/usr/bin/env python3
"""Align two COLMAP reconstructions by shared cameras and compare PLY vertices."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pycolmap
from scipy.spatial import cKDTree


def read_ply_vertices(path: Path) -> tuple[np.ndarray, int]:
    """Read xyz vertices and face count from COLMAP's binary little-endian PLY."""
    vertex_count = 0
    face_count = 0
    with path.open("rb") as stream:
        while True:
            line = stream.readline()
            if not line:
                raise ValueError(f"missing PLY header terminator: {path}")
            decoded = line.decode("ascii").strip()
            if decoded == "format binary_little_endian 1.0":
                continue
            if decoded.startswith("format "):
                raise ValueError(f"unsupported PLY encoding in {path}: {decoded}")
            if decoded.startswith("element vertex "):
                vertex_count = int(decoded.split()[-1])
            elif decoded.startswith("element face "):
                face_count = int(decoded.split()[-1])
            elif decoded == "end_header":
                break
        vertices = np.fromfile(
            stream,
            dtype=np.dtype([("x", "<f4"), ("y", "<f4"), ("z", "<f4")]),
            count=vertex_count,
        )
    xyz = np.column_stack([vertices[axis] for axis in ("x", "y", "z")]).astype(float)
    return xyz, face_count


def camera_centers(model_path: Path) -> dict[str, np.ndarray]:
    reconstruction = pycolmap.Reconstruction(str(model_path))
    return {
        image.name: np.asarray(image.projection_center(), dtype=float)
        for image in reconstruction.images.values()
        if image.has_pose
    }


def model_summary(model_path: Path) -> dict[str, float | int]:
    reconstruction = pycolmap.Reconstruction(str(model_path))
    return {
        "registered_images": reconstruction.num_reg_images(),
        "points": reconstruction.num_points3D(),
        "observations": reconstruction.compute_num_observations(),
        "mean_track_length": reconstruction.compute_mean_track_length(),
        "mean_reprojection_error_px": reconstruction.compute_mean_reprojection_error(),
    }


def similarity(source: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """Return scale, rotation, and translation mapping source onto target."""
    source_mean = source.mean(axis=0)
    target_mean = target.mean(axis=0)
    source_centered = source - source_mean
    target_centered = target - target_mean
    covariance = source_centered.T @ target_centered / len(source)
    left, singular, right_transpose = np.linalg.svd(covariance)
    sign = np.ones(3)
    if np.linalg.det(right_transpose.T @ left.T) < 0:
        sign[-1] = -1
    rotation = right_transpose.T @ np.diag(sign) @ left.T
    scale = float((singular * sign).sum() / np.mean(np.sum(source_centered**2, axis=1)))
    translation = target_mean - scale * (rotation @ source_mean)
    return scale, rotation, translation


def distance_summary(values: np.ndarray, scale: float) -> dict[str, float]:
    return {
        "mean": float(values.mean()),
        "median": float(np.median(values)),
        "p95": float(np.percentile(values, 95)),
        "mean_percent_of_bbox_diagonal": float(100 * values.mean() / scale),
        "median_percent_of_bbox_diagonal": float(100 * np.median(values) / scale),
        "p95_percent_of_bbox_diagonal": float(100 * np.percentile(values, 95) / scale),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-model", type=Path, required=True)
    parser.add_argument("--candidate-model", type=Path, required=True)
    parser.add_argument("--reference-mesh", type=Path, required=True)
    parser.add_argument("--candidate-mesh", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    reference_cameras = camera_centers(args.reference_model)
    candidate_cameras = camera_centers(args.candidate_model)
    shared = sorted(reference_cameras.keys() & candidate_cameras.keys())
    if len(shared) < 3:
        raise ValueError("at least three shared registered cameras are required")
    reference_centers = np.asarray([reference_cameras[name] for name in shared])
    candidate_centers = np.asarray([candidate_cameras[name] for name in shared])
    factor, rotation, translation = similarity(candidate_centers, reference_centers)
    aligned_centers = factor * (candidate_centers @ rotation.T) + translation
    camera_residual = np.linalg.norm(aligned_centers - reference_centers, axis=1)

    reference_vertices, reference_faces = read_ply_vertices(args.reference_mesh)
    candidate_vertices, candidate_faces = read_ply_vertices(args.candidate_mesh)
    aligned_candidate = factor * (candidate_vertices @ rotation.T) + translation
    lower, upper = np.percentile(reference_vertices, [1, 99], axis=0)
    bbox_diagonal = float(np.linalg.norm(upper - lower))
    candidate_to_reference = cKDTree(reference_vertices).query(aligned_candidate, workers=-1)[0]
    reference_to_candidate = cKDTree(aligned_candidate).query(reference_vertices, workers=-1)[0]

    result = {
        "reference_reconstruction": model_summary(args.reference_model),
        "candidate_reconstruction": model_summary(args.candidate_model),
        "alignment": {
            "shared_cameras": len(shared),
            "scale": factor,
            "camera_center_residual": distance_summary(camera_residual, bbox_diagonal),
        },
        "reference_mesh": {"vertices": len(reference_vertices), "faces": reference_faces},
        "candidate_mesh": {"vertices": len(candidate_vertices), "faces": candidate_faces},
        "robust_reference_bbox_diagonal": bbox_diagonal,
        "candidate_to_reference": distance_summary(candidate_to_reference, bbox_diagonal),
        "reference_to_candidate": distance_summary(reference_to_candidate, bbox_diagonal),
        "symmetric_chamfer_mean": float(
            (candidate_to_reference.mean() + reference_to_candidate.mean()) / 2
        ),
        "symmetric_chamfer_mean_percent_of_bbox_diagonal": float(
            50 * (candidate_to_reference.mean() + reference_to_candidate.mean()) / bbox_diagonal
        ),
        "limitations": [
            "Meshes are generated from sparse SfM points with COLMAP Delaunay meshing, not dense MVS.",
            "No physical scale or external ground-truth surface is available for this specimen.",
            "Nearest-vertex distances are a topology-stability diagnostic, not anatomical accuracy.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

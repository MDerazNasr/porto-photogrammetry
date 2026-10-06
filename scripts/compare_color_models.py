#!/usr/bin/env python3
"""Compare linear 3x3 and second-order root-polynomial colour correction.

The decision metric is leave-one-patch-out Delta E76. Full-frame reference
images are used only for clipping and change diagnostics, not model selection.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "team-repo" / "src"))

from augenblick.preparation.color import (  # noqa: E402
    delta_e76,
    linear_to_srgb,
    locate_patch_centers,
    rectify_chart,
    sample_patches,
    srgb_to_linear,
)


def features(linear_rgb: np.ndarray, model: str) -> np.ndarray:
    if model == "linear_3x3":
        return linear_rgb
    red, green, blue = np.moveaxis(np.maximum(linear_rgb, 0.0), -1, 0)
    return np.stack(
        (red, green, blue, np.sqrt(red * green), np.sqrt(red * blue), np.sqrt(green * blue)),
        axis=-1,
    )


def fit(source_rgb: np.ndarray, target_rgb: np.ndarray, model: str, ridge: float) -> np.ndarray:
    design = features(srgb_to_linear(source_rgb), model).astype(np.float64)
    target = srgb_to_linear(target_rgb).astype(np.float64)
    prior = np.zeros((design.shape[1], 3), dtype=np.float64)
    prior[:3] = np.eye(3)
    return np.linalg.solve(
        design.T @ design + ridge * np.eye(design.shape[1]),
        design.T @ target + ridge * prior,
    )


def predict(source_rgb: np.ndarray, coefficients: np.ndarray, model: str) -> np.ndarray:
    corrected = features(srgb_to_linear(source_rgb), model) @ coefficients
    return np.clip(linear_to_srgb(corrected), 0.0, 1.0)


def load_dataset(name: str, input_dir: Path, metadata_path: Path) -> dict:
    metadata = json.loads(metadata_path.read_text())
    corners = metadata.get("chart_corners")
    centers = metadata.get("patch_centers_rectified", {})
    if corners is None:
        corners = {
            camera: values["corners"] for camera, values in metadata["cameras"].items()
        }
        references = {
            camera: input_dir / values["reference_image"]
            for camera, values in metadata["cameras"].items()
        }
    else:
        references = {}
        for camera in corners:
            matches = sorted(input_dir.glob(f"{camera}_*.[Jj][Pp][Gg]"))
            if len(matches) != 1:
                raise ValueError(f"expected one {camera} reference in {input_dir}, found {matches}")
            references[camera] = matches[0]

    samples = {}
    images = {}
    for camera, path in references.items():
        image = cv2.imread(str(path))
        if image is None:
            raise ValueError(f"could not read {path}")
        chart = rectify_chart(image, np.asarray(corners[camera], dtype=np.float32))
        patch_centers = np.asarray(centers[camera], dtype=np.float32) if camera in centers else locate_patch_centers(chart)
        samples[camera] = sample_patches(chart, patch_centers)
        images[camera] = (path, image)
    return {
        "name": name,
        "reference_camera": metadata["reference_camera"],
        "ridge": float(metadata.get("ridge", 1e-6)),
        "samples": samples,
        "images": images,
    }


def loocv(source: np.ndarray, target: np.ndarray, model: str, ridge: float) -> np.ndarray:
    predictions = []
    for held_out in range(len(source)):
        training = np.arange(len(source)) != held_out
        coefficients = fit(source[training], target[training], model, ridge)
        predictions.append(predict(source[held_out : held_out + 1], coefficients, model)[0])
    return delta_e76(np.asarray(predictions, dtype=np.float32), target)


def image_diagnostics(image: np.ndarray, coefficients: np.ndarray, model: str) -> tuple[dict, np.ndarray]:
    corrected_image = np.empty_like(image)
    clipped_before = 0
    clipped_after = 0
    absolute_change = 0.0
    pixel_count = image.shape[0] * image.shape[1]
    for start in range(0, image.shape[0], 128):
        stop = min(start + 128, image.shape[0])
        bgr = image[start:stop]
        rgb = bgr[:, :, ::-1].astype(np.float32) / 255.0
        corrected = predict(rgb.reshape(-1, 3), coefficients, model).reshape(rgb.shape)
        corrected_bgr = np.round(corrected[:, :, ::-1] * 255.0).astype(np.uint8)
        corrected_image[start:stop] = corrected_bgr
        clipped_before += int(np.any((bgr == 0) | (bgr == 255), axis=2).sum())
        clipped_after += int(np.any((corrected_bgr == 0) | (corrected_bgr == 255), axis=2).sum())
        absolute_change += float(np.abs(corrected_bgr.astype(np.float32) - bgr).sum())
    return (
        {
            "clipped_percent_before": 100.0 * clipped_before / pixel_count,
            "clipped_percent_after": 100.0 * clipped_after / pixel_count,
            "mean_absolute_change_8bit": absolute_change / (pixel_count * 3),
        },
        corrected_image,
    )


def exposure_residual(source: np.ndarray, coefficients: np.ndarray, model: str) -> float:
    linear = srgb_to_linear(source).astype(np.float64)
    baseline = features(linear, model) @ coefficients
    residual = 0.0
    for scale in (0.25, 0.5, 1.5):
        scaled = features(linear * scale, model) @ coefficients
        residual = max(residual, float(np.max(np.abs(scaled - baseline * scale))))
    return residual


def bootstrap_ci(differences: np.ndarray) -> list[float]:
    random = np.random.default_rng(20261002)
    means = np.empty(20000)
    for index in range(len(means)):
        means[index] = random.choice(differences, size=len(differences), replace=True).mean()
    return [float(value) for value in np.percentile(means, (2.5, 97.5))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        action="append",
        required=True,
        metavar="NAME:INPUT_DIR:METADATA_JSON",
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()

    datasets = []
    for value in args.dataset:
        name, input_dir, metadata = value.split(":", 2)
        datasets.append(load_dataset(name, Path(input_dir), Path(metadata)))

    results = {"method": "leave-one-patch-out", "models": {}, "comparisons": []}
    paired_differences = []
    camera_mean_differences = []
    clipping_increases = []
    exposure_residuals = []
    for dataset in datasets:
        target = dataset["samples"][dataset["reference_camera"]]
        for camera, source in dataset["samples"].items():
            if camera == dataset["reference_camera"]:
                continue
            key = f"{dataset['name']}/{camera}"
            item = {"patch_count": len(source), "models": {}}
            errors = {}
            for model in ("linear_3x3", "root_polynomial_degree_2"):
                held_out = loocv(source, target, model, dataset["ridge"])
                coefficients = fit(source, target, model, dataset["ridge"])
                full_fit_error = delta_e76(
                    predict(source, coefficients, model).astype(np.float32), target
                )
                diagnostic, corrected = image_diagnostics(dataset["images"][camera][1], coefficients, model)
                residual = exposure_residual(source, coefficients, model)
                errors[model] = held_out
                item["models"][model] = {
                    "mean_held_out_delta_e76": float(held_out.mean()),
                    "median_held_out_delta_e76": float(np.median(held_out)),
                    "max_held_out_delta_e76": float(held_out.max()),
                    "mean_full_fit_delta_e76": float(full_fit_error.mean()),
                    "full_reference_image": diagnostic,
                    "exposure_homogeneity_max_abs_linear_rgb": residual,
                    "coefficients": coefficients.tolist(),
                }
                exposure_residuals.append(residual)
                if args.preview_dir:
                    args.preview_dir.mkdir(parents=True, exist_ok=True)
                    width = min(1200, corrected.shape[1])
                    height = round(corrected.shape[0] * width / corrected.shape[1])
                    preview = cv2.resize(corrected, (width, height), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(str(args.preview_dir / f"{dataset['name']}-{camera}-{model}.jpg"), preview)
            difference = errors["root_polynomial_degree_2"] - errors["linear_3x3"]
            paired_differences.extend(difference.tolist())
            camera_mean_differences.append(float(difference.mean()))
            linear_clip = item["models"]["linear_3x3"]["full_reference_image"]["clipped_percent_after"]
            root_clip = item["models"]["root_polynomial_degree_2"]["full_reference_image"]["clipped_percent_after"]
            clipping_increases.append(root_clip - linear_clip)
            item["root_minus_linear"] = {
                "mean_held_out_delta_e76": float(difference.mean()),
                "patches_better": int((difference < 0).sum()),
                "patches_worse": int((difference > 0).sum()),
                "clipped_percent_after_difference": root_clip - linear_clip,
            }
            results["comparisons"].append({key: item})

    differences = np.asarray(paired_differences)
    linear_means = [
        next(iter(entry.values()))["models"]["linear_3x3"]["mean_held_out_delta_e76"]
        for entry in results["comparisons"]
    ]
    root_means = [
        next(iter(entry.values()))["models"]["root_polynomial_degree_2"]["mean_held_out_delta_e76"]
        for entry in results["comparisons"]
    ]
    relative_reduction = 1.0 - float(np.mean(root_means)) / float(np.mean(linear_means))
    confidence_interval = bootstrap_ci(differences)
    criteria = {
        "pooled_mean_relative_reduction_at_least_10_percent": relative_reduction >= 0.10,
        "bootstrap_95_percent_ci_excludes_no_improvement": confidence_interval[1] < 0.0,
        "no_camera_mean_worse_by_more_than_0_25_delta_e76": max(camera_mean_differences) <= 0.25,
        "no_reference_frame_clipping_increase_over_0_10_percentage_points": max(clipping_increases) <= 0.10,
        "exposure_homogeneity_residual_below_1e_6": max(exposure_residuals) < 1e-6,
    }
    results["summary"] = {
        "camera_comparisons": len(linear_means),
        "held_out_predictions": len(differences),
        "mean_linear_delta_e76": float(np.mean(linear_means)),
        "mean_root_polynomial_delta_e76": float(np.mean(root_means)),
        "root_relative_reduction": relative_reduction,
        "paired_root_minus_linear_mean": float(differences.mean()),
        "paired_root_minus_linear_bootstrap_95_percent_ci": confidence_interval,
        "maximum_camera_mean_worsening": max(camera_mean_differences),
        "maximum_clipping_increase_percentage_points": max(clipping_increases),
        "maximum_exposure_homogeneity_residual": max(exposure_residuals),
        "adoption_criteria": criteria,
        "recommendation": "adopt_root_polynomial" if all(criteria.values()) else "retain_linear_3x3",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2))
    print(json.dumps(results["summary"], indent=2))


if __name__ == "__main__":
    main()

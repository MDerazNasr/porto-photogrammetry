#!/usr/bin/env python3
"""Run the production colour stage on naturally multicoloured fish textures.

The texture maps are real project assets, but the camera responses and chart
observations are controlled simulations. This is therefore a pipeline stress
test with known pixel ground truth, not an additional field calibration.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "team-repo" / "src"))

from augenblick.preparation.color import (  # noqa: E402
    calibrate_directory,
    delta_e76,
    linear_to_srgb,
    load_config,
    srgb_to_linear,
)


PATCH_COLORS_BGR = [
    (68, 82, 115), (130, 150, 194), (157, 122, 98), (67, 108, 87),
    (177, 128, 133), (170, 189, 103), (44, 126, 214), (166, 91, 80),
    (99, 90, 193), (108, 60, 94), (64, 188, 157), (46, 163, 224),
    (150, 61, 56), (73, 148, 70), (60, 54, 175), (31, 199, 231),
    (149, 86, 187), (161, 133, 8), (243, 243, 243), (200, 200, 200),
    (160, 160, 160), (122, 122, 121), (85, 85, 85), (52, 52, 52),
]

# Real correction matrices previously fitted on UF_Herp_3998. They are used
# only to create deterministic camera-response simulations with known targets.
CORRECTION_MATRICES = {
    "camera1": np.eye(3, dtype=np.float32),
    "camera2": np.asarray(
        [[1.3841367, -0.03343435, -0.03309717],
         [-0.08461196, 1.4258361, -0.04513314],
         [-0.03111402, -0.10168097, 1.3196203]], dtype=np.float32,
    ),
    "camera3": np.asarray(
        [[0.9266138, -0.00056885, -0.00391110],
         [0.00372257, 0.9142076, 0.02141470],
         [0.00187337, -0.01306454, 0.95631343]], dtype=np.float32,
    ),
}


def chart() -> np.ndarray:
    image = np.full((400, 600, 3), 20, dtype=np.uint8)
    for index, color in enumerate(PATCH_COLORS_BGR):
        row, column = divmod(index, 6)
        center_x = 75 + 90 * column - 3 * row
        center_y = 70 + 80 * row + 2 * column
        cv2.rectangle(image, (center_x - 30, center_y - 24),
                      (center_x + 30, center_y + 24), color, -1)
    return image


def simulate_camera(image: np.ndarray, correction: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rgb = image[:, :, ::-1].astype(np.float32) / 255.0
    source_linear = srgb_to_linear(rgb.reshape(-1, 3)) @ np.linalg.inv(correction)
    clipped = np.any((source_linear < 0.0) | (source_linear > 1.0), axis=1)
    source = np.clip(linear_to_srgb(source_linear), 0.0, 1.0).reshape(rgb.shape)
    return np.round(source[:, :, ::-1] * 255.0).astype(np.uint8), clipped.reshape(image.shape[:2])


def resize_texture(path: Path, maximum: int) -> tuple[np.ndarray, np.ndarray]:
    rgba = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if rgba is None or rgba.ndim != 3 or rgba.shape[2] != 4:
        raise ValueError(f"expected RGBA texture: {path}")
    scale = min(1.0, maximum / max(rgba.shape[:2]))
    size = (round(rgba.shape[1] * scale), round(rgba.shape[0] * scale))
    color = cv2.resize(rgba[:, :, :3], size, interpolation=cv2.INTER_AREA)
    alpha = cv2.resize(rgba[:, :, 3], size, interpolation=cv2.INTER_AREA)
    return color, alpha >= 128


def delta_e_sample(first: np.ndarray, second: np.ndarray, mask: np.ndarray) -> float:
    selected = np.flatnonzero(mask.ravel())[::4]
    first_rgb = first[:, :, ::-1].reshape(-1, 3)[selected].astype(np.float32) / 255.0
    second_rgb = second[:, :, ::-1].reshape(-1, 3)[selected].astype(np.float32) / 255.0
    return float(delta_e76(first_rgb, second_rgb).mean())


def clipping_percent(image: np.ndarray, mask: np.ndarray) -> float:
    return 100.0 * float((np.any((image == 0) | (image == 255), axis=2) & mask).sum()) / float(mask.sum())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("texture_dir", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--preview-dir", required=True, type=Path)
    parser.add_argument("--maximum-size", type=int, default=1024)
    args = parser.parse_args()

    textures = sorted(args.texture_dir.glob("*_diffuse.1001.png"))
    if not textures:
        raise SystemExit(f"no fish texture maps found in {args.texture_dir}")
    args.preview_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="multicolor-pipeline-") as temporary:
        root = Path(temporary)
        input_dir = root / "input"
        calibrated_dir = root / "calibrated"
        input_dir.mkdir()
        reference_chart = chart()
        config = {"reference_camera": "camera1", "camera_regex": "camera[0-9]+",
                  "ridge": 1e-6, "cameras": {}}
        for camera, correction in CORRECTION_MATRICES.items():
            simulated_chart, _ = simulate_camera(reference_chart, correction)
            canvas = np.full((600, 800, 3), 235, dtype=np.uint8)
            canvas[100:500, 100:700] = simulated_chart
            reference_name = f"{camera}_chart.png"
            cv2.imwrite(str(input_dir / reference_name), canvas)
            config["cameras"][camera] = {
                "reference_image": reference_name,
                "corners": [[100, 100], [699, 100], [699, 499], [100, 499]],
            }

        originals = {}
        synthesis_clipping = {}
        for index, texture in enumerate(textures):
            original, mask = resize_texture(texture, args.maximum_size)
            sample = f"fish{index + 1:02d}"
            originals[sample] = (texture.name, original, mask)
            synthesis_clipping[sample] = {}
            for camera, correction in CORRECTION_MATRICES.items():
                simulated, clipped = simulate_camera(original, correction)
                filename = f"{camera}_{sample}.png"
                cv2.imwrite(str(input_dir / filename), simulated)
                cv2.imwrite(str(input_dir / f"{camera}_{sample}.mask.png"), mask.astype(np.uint8) * 255)
                synthesis_clipping[sample][camera] = 100.0 * float((clipped & mask).sum()) / float(mask.sum())

        config_path = root / "config.json"
        config_path.write_text(json.dumps(config, indent=2))
        pipeline_report = calibrate_directory(input_dir, calibrated_dir, load_config(config_path))

        samples = []
        for sample, (source_name, target, mask) in originals.items():
            preview_columns = [target]
            for camera in ("camera2", "camera3"):
                before = cv2.imread(str(input_dir / f"{camera}_{sample}.png"))
                after = cv2.imread(str(calibrated_dir / f"{camera}_{sample}.png"))
                before_delta = delta_e_sample(before, target, mask)
                after_delta = delta_e_sample(after, target, mask)
                samples.append({
                    "texture": source_name,
                    "sample": sample,
                    "camera": camera,
                    "foreground_pixels": int(mask.sum()),
                    "synthesis_clipped_percent": synthesis_clipping[sample][camera],
                    "mean_delta_e76_before": before_delta,
                    "mean_delta_e76_after": after_delta,
                    "relative_delta_e76_reduction": 1.0 - after_delta / before_delta,
                    "foreground_clipped_percent_before": clipping_percent(before, mask),
                    "foreground_clipped_percent_after": clipping_percent(after, mask),
                })
                preview_columns.extend((before, after))
            preview = np.concatenate(preview_columns, axis=1)
            cv2.imwrite(str(args.preview_dir / f"{sample}-{Path(source_name).stem}.jpg"), preview)

    reductions = np.asarray([item["relative_delta_e76_reduction"] for item in samples])
    clipping_increases = np.asarray([
        item["foreground_clipped_percent_after"] - item["foreground_clipped_percent_before"]
        for item in samples
    ])
    criteria = {
        "every_sample_delta_e76_reduction_at_least_50_percent": bool(np.all(reductions >= 0.50)),
        "mean_delta_e76_reduction_at_least_75_percent": bool(reductions.mean() >= 0.75),
        "no_foreground_clipping_increase_over_0_50_percentage_points": bool(np.all(clipping_increases <= 0.50)),
        "all_images_processed_without_skips": not pipeline_report["skipped_images"] and all(
            count == len(textures) for count in pipeline_report["processed_images"].values()
        ),
    }
    result = {
        "scope": "controlled camera-response stress test on real multicolour fish texture maps",
        "limitation": "not a field calibration; raw fish photographs and fish-specific chart frames were not available",
        "texture_count": len(textures),
        "camera_conditions": 2,
        "evaluated_outputs": len(samples),
        "summary": {
            "mean_delta_e76_before": float(np.mean([item["mean_delta_e76_before"] for item in samples])),
            "mean_delta_e76_after": float(np.mean([item["mean_delta_e76_after"] for item in samples])),
            "mean_relative_delta_e76_reduction": float(reductions.mean()),
            "minimum_relative_delta_e76_reduction": float(reductions.min()),
            "maximum_foreground_clipping_increase_percentage_points": float(clipping_increases.max()),
            "acceptance_criteria": criteria,
            "result": "pass" if all(criteria.values()) else "fail",
        },
        "pipeline_report": pipeline_report,
        "samples": samples,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()

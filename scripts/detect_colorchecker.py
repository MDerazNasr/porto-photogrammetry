"""Find classic 24-patch ColorCheckers in an image directory."""

from pathlib import Path
import sys

import cv2


root = Path(sys.argv[1])
requested_width = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
images = sorted(
    path
    for path in root.rglob("*")
    if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    and not path.name.lower().endswith(".mask.png")
)
print(f"Scanning {len(images)} images under {root}", flush=True)

for index, path in enumerate(images, 1):
    image = cv2.imread(str(path))
    if image is None:
        continue
    height, width = image.shape[:2]
    scan_width = min(width, requested_width)
    scale = scan_width / width
    resized = cv2.resize(
        image,
        (scan_width, round(height * scale)),
        interpolation=cv2.INTER_AREA,
    )
    detector = cv2.mcc.CCheckerDetector_create()
    if detector.process(resized, cv2.mcc.MCC24):
        checker = detector.getBestColorChecker()
        print(f"MATCH\t{path}\tbox={checker.getBox().tolist()}", flush=True)
    if index % 50 == 0:
        print(f"PROGRESS\t{index}/{len(images)}", flush=True)

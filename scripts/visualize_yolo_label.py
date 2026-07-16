from pathlib import Path

import cv2


DATASET_DIR = Path("data/datasets/singapore-maritime")
IMAGES_DIR = DATASET_DIR / "train" / "images"
LABELS_DIR = DATASET_DIR / "train" / "labels"
OUTPUT_DIR = Path("outputs/annotated_samples")

CLASS_NAMES = [
    "Boat",
    "Buoy",
    "Ferry",
    "Flying bird-plane",
    "Kayak",
    "Other",
    "Sail boat",
    "Speed boat",
    "Vessel-ship",
]


def draw_annotations(image_path: Path, label_path: Path) -> None:
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"Image could not be opened: {image_path}")
        return

    image_height, image_width = image.shape[:2]

    if not label_path.exists():
        print(f"Label file not found: {label_path}")
        return

    with label_path.open("r", encoding="utf-8") as label_file:
        for line in label_file:
            values = line.strip().split()

            if len(values) != 5:
                continue

            class_id = int(values[0])
            x_center, y_center, box_width, box_height = map(
                float, values[1:]
            )

            x_center_px = x_center * image_width
            y_center_px = y_center * image_height
            box_width_px = box_width * image_width
            box_height_px = box_height * image_height

            x1 = int(x_center_px - box_width_px / 2)
            y1 = int(y_center_px - box_height_px / 2)
            x2 = int(x_center_px + box_width_px / 2)
            y2 = int(y_center_px + box_height_px / 2)

            class_name = CLASS_NAMES[class_id]

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                class_name,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / image_path.name
    cv2.imwrite(str(output_path), image)

    print(f"Saved: {output_path}")


def main() -> None:
    image_paths = sorted(IMAGES_DIR.glob("*.jpg"))[:5]

    if not image_paths:
        raise FileNotFoundError(f"No JPG images found in: {IMAGES_DIR}")

    for image_path in image_paths:
        label_path = LABELS_DIR / f"{image_path.stem}.txt"
        draw_annotations(image_path, label_path)


if __name__ == "__main__":
    main()

from pathlib import Path


DATASET_DIR = Path("data/datasets/singapore-maritime")
SPLITS = ["train", "valid", "test"]
NUM_CLASSES = 9

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def check_split(split: str) -> None:
    images_dir = DATASET_DIR / split / "images"
    labels_dir = DATASET_DIR / split / "labels"

    image_files = {
        file.stem: file
        for file in images_dir.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    }

    label_files = {
        file.stem: file
        for file in labels_dir.glob("*.txt")
        if file.is_file()
    }

    missing_labels = sorted(set(image_files) - set(label_files))
    missing_images = sorted(set(label_files) - set(image_files))

    empty_labels = []
    invalid_lines = []
    invalid_class_ids = []
    invalid_coordinates = []

    total_objects = 0

    for label_path in label_files.values():
        content = label_path.read_text(encoding="utf-8").strip()

        if not content:
            empty_labels.append(label_path)
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            parts = line.split()

            if len(parts) != 5:
                invalid_lines.append(
                    (label_path, line_number, line, "Expected 5 values")
                )
                continue

            try:
                class_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
            except ValueError:
                invalid_lines.append(
                    (label_path, line_number, line, "Non-numeric value")
                )
                continue

            total_objects += 1

            if not 0 <= class_id < NUM_CLASSES:
                invalid_class_ids.append(
                    (label_path, line_number, class_id)
                )

            if not (
                0 <= x_center <= 1
                and 0 <= y_center <= 1
                and 0 < width <= 1
                and 0 < height <= 1
            ):
                invalid_coordinates.append(
                    (
                        label_path,
                        line_number,
                        [x_center, y_center, width, height],
                    )
                )

    print(f"\n--- {split.upper()} ---")
    print(f"Images: {len(image_files)}")
    print(f"Labels: {len(label_files)}")
    print(f"Objects: {total_objects}")
    print(f"Missing labels: {len(missing_labels)}")
    print(f"Missing images: {len(missing_images)}")
    print(f"Empty label files: {len(empty_labels)}")
    print(f"Invalid format lines: {len(invalid_lines)}")
    print(f"Invalid class IDs: {len(invalid_class_ids)}")
    print(f"Invalid coordinates: {len(invalid_coordinates)}")

    if missing_labels:
        print("\nFirst missing labels:")
        for stem in missing_labels[:10]:
            print(f"  {image_files[stem].name}")

    if missing_images:
        print("\nFirst missing images:")
        for stem in missing_images[:10]:
            print(f"  {label_files[stem].name}")

    if empty_labels:
        print("\nFirst empty label files:")
        for path in empty_labels[:10]:
            print(f"  {path}")

    if invalid_lines:
        print("\nFirst invalid lines:")
        for path, line_number, line, reason in invalid_lines[:10]:
            print(f"  {path}:{line_number} -> {reason}: {line}")

    if invalid_class_ids:
        print("\nFirst invalid class IDs:")
        for path, line_number, class_id in invalid_class_ids[:10]:
            print(f"  {path}:{line_number} -> class_id={class_id}")

    if invalid_coordinates:
        print("\nFirst invalid coordinates:")
        for path, line_number, values in invalid_coordinates[:10]:
            print(f"  {path}:{line_number} -> {values}")


def main() -> None:
    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset directory not found: {DATASET_DIR}"
        )

    for split in SPLITS:
        check_split(split)


if __name__ == "__main__":
    main()

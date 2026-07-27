from pathlib import Path
import shutil


DATASET_DIR = Path("data/datasets/singapore-maritime")
OUTPUT_DIR = Path("outputs/dataset_check/empty_labels")
SPLITS = ["train", "valid", "test"]
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]


def main() -> None:
    total_copied = 0

    for split in SPLITS:
        labels_dir = DATASET_DIR / split / "labels"
        images_dir = DATASET_DIR / split / "images"
        split_output = OUTPUT_DIR / split
        split_output.mkdir(parents=True, exist_ok=True)

        for label_path in labels_dir.glob("*.txt"):
            if label_path.read_text(encoding="utf-8").strip():
                continue

            image_path = None

            for extension in IMAGE_EXTENSIONS:
                candidate = images_dir / f"{label_path.stem}{extension}"

                if candidate.exists():
                    image_path = candidate
                    break

            if image_path is None:
                print(f"Image not found for: {label_path.name}")
                continue

            shutil.copy2(image_path, split_output / image_path.name)
            total_copied += 1

    print(f"Copied {total_copied} empty-label images to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

from pathlib import Path
from collections import Counter
import re

ROOT = Path("data/datasets/singapore-maritime-grouped")

CLASSES = [
    "Boat",
    "Buoy",
    "Ferry",
    "Flying bird-plane",
    "Kayak",
    "Other",
    "Sail boat",
    "Speed boat",
    "Vessel-ship"
]


def source_video(filename):
    name = filename.split(".rf.")[0]
    match = re.match(r"(.+)_frame\d+", name)

    if not match:
        raise ValueError(f"Could not parse: {filename}")

    return match.group(1)


split_videos = {}
grand_class_counts = Counter()
grand_images = 0
grand_objects = 0
grand_empty = 0


for split in ["train", "valid", "test"]:

    image_dir = ROOT / split / "images"
    label_dir = ROOT / split / "labels"

    images = sorted(image_dir.iterdir())
    labels = sorted(label_dir.glob("*.txt"))

    videos = set()
    class_counts = Counter()

    empty_labels = 0
    objects = 0

    for image_path in images:

        if not image_path.is_file():
            continue

        videos.add(source_video(image_path.name))

        label_path = label_dir / f"{image_path.stem}.txt"

        if not label_path.exists():
            raise RuntimeError(
                f"Missing label for {image_path}"
            )

        lines = [
            line.strip()
            for line in label_path.read_text().splitlines()
            if line.strip()
        ]

        if not lines:
            empty_labels += 1
            continue

        for line in lines:

            parts = line.split()

            if len(parts) != 5:
                raise ValueError(
                    f"Invalid YOLO annotation: {label_path}\n{line}"
                )

            class_id = int(parts[0])

            if not 0 <= class_id < len(CLASSES):
                raise ValueError(
                    f"Invalid class ID {class_id} in {label_path}"
                )

            class_counts[class_id] += 1
            objects += 1

    split_videos[split] = videos

    grand_images += len(images)
    grand_objects += objects
    grand_empty += empty_labels

    for class_id, count in class_counts.items():
        grand_class_counts[class_id] += count

    print(f"\n=== {split.upper()} ===")
    print("Source videos:", len(videos))
    print("Images       :", len(images))
    print("Labels       :", len(labels))
    print("Empty labels :", empty_labels)
    print("Objects      :", objects)

    print("\nClass counts:")

    for class_id, class_name in enumerate(CLASSES):
        print(
            f"{class_name:<20} "
            f"{class_counts[class_id]:>6}"
        )


print("\n=== LEAKAGE CHECK ===")

print(
    "Train ∩ Valid:",
    len(split_videos["train"] & split_videos["valid"])
)

print(
    "Train ∩ Test :",
    len(split_videos["train"] & split_videos["test"])
)

print(
    "Valid ∩ Test :",
    len(split_videos["valid"] & split_videos["test"])
)


print("\n=== TOTAL ===")
print(
    "Source videos:",
    len(
        split_videos["train"]
        | split_videos["valid"]
        | split_videos["test"]
    )
)
print("Images       :", grand_images)
print("Objects      :", grand_objects)
print("Empty labels :", grand_empty)


print("\n=== TOTAL CLASS COUNTS ===")

for class_id, class_name in enumerate(CLASSES):
    print(
        f"{class_name:<20} "
        f"{grand_class_counts[class_id]:>6}"
    )


print("\n=== COVERAGE WARNINGS ===")

warnings = 0

for class_id, class_name in enumerate(CLASSES):

    missing = []

    for split in ["train", "valid", "test"]:

        label_dir = ROOT / split / "labels"
        found = False

        for label_path in label_dir.glob("*.txt"):

            for line in label_path.read_text().splitlines():

                if line.strip() and int(line.split()[0]) == class_id:
                    found = True
                    break

            if found:
                break

        if not found:
            missing.append(split)

    if missing:
        warnings += 1
        print(
            f"{class_name}: missing from "
            + ", ".join(missing)
        )

if warnings == 0:
    print("All classes occur in all splits.")

print("\nAudit complete.")

from pathlib import Path
import csv
import re
import shutil

SOURCE = Path("data/datasets/singapore-maritime")
DEST = Path("data/datasets/singapore-maritime-grouped")
MANIFEST = SOURCE / "split_manifest.csv"

OLD_SPLITS = ["train", "valid", "test"]
NEW_SPLITS = ["train", "valid", "test"]


def source_video(filename):
    name = filename.split(".rf.")[0]
    match = re.match(r"(.+)_frame\d+", name)

    if not match:
        raise ValueError(f"Could not parse source video: {filename}")

    return match.group(1)


# --------------------------------------------------
# Read split manifest
# --------------------------------------------------

assignments = {}

with MANIFEST.open() as f:
    reader = csv.DictReader(f)

    for row in reader:
        assignments[row["source_video"]] = row["split"]

print(f"Loaded {len(assignments)} source-video assignments.")


# --------------------------------------------------
# Safety check
# --------------------------------------------------

if DEST.exists():
    raise RuntimeError(
        f"{DEST} already exists.\n"
        "Delete it manually only if you intentionally want to rebuild it."
    )


# --------------------------------------------------
# Create grouped directory structure
# --------------------------------------------------

for split in NEW_SPLITS:
    (DEST / split / "images").mkdir(parents=True, exist_ok=True)
    (DEST / split / "labels").mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Copy images and corresponding labels
# --------------------------------------------------

image_counts = {
    "train": 0,
    "valid": 0,
    "test": 0
}

label_counts = {
    "train": 0,
    "valid": 0,
    "test": 0
}

missing_labels = []


for old_split in OLD_SPLITS:

    image_dir = SOURCE / old_split / "images"
    label_dir = SOURCE / old_split / "labels"

    for image_path in image_dir.iterdir():

        if not image_path.is_file():
            continue

        video = source_video(image_path.name)

        if video not in assignments:
            raise ValueError(
                f"No split assignment found for {video}"
            )

        new_split = assignments[video]

        destination_image = (
            DEST / new_split / "images" / image_path.name
        )

        shutil.copy2(
            image_path,
            destination_image
        )

        image_counts[new_split] += 1

        label_path = (
            label_dir / f"{image_path.stem}.txt"
        )

        if label_path.exists():

            destination_label = (
                DEST / new_split / "labels" / label_path.name
            )

            shutil.copy2(
                label_path,
                destination_label
            )

            label_counts[new_split] += 1

        else:
            missing_labels.append(str(image_path))


# --------------------------------------------------
# Create grouped_data.yaml
# --------------------------------------------------

yaml_path = DEST / "grouped_data.yaml"

yaml_text = """path: /home/rana/Documents/maritime-detection/data/datasets/singapore-maritime-grouped
train: train/images
val: valid/images
test: test/images

nc: 9

names:
  0: Boat
  1: Buoy
  2: Ferry
  3: Flying bird-plane
  4: Kayak
  5: Other
  6: Sail boat
  7: Speed boat
  8: Vessel-ship
"""

yaml_path.write_text(yaml_text)


# --------------------------------------------------
# Copy manifest into grouped dataset
# --------------------------------------------------

shutil.copy2(
    MANIFEST,
    DEST / "split_manifest.csv"
)


# --------------------------------------------------
# Final report
# --------------------------------------------------

print("\n=== GROUPED DATASET CREATED ===")

for split in NEW_SPLITS:
    print(
        f"{split:<6} "
        f"images={image_counts[split]:>4} "
        f"labels={label_counts[split]:>4}"
    )

print("\nTotal images:", sum(image_counts.values()))
print("Total labels:", sum(label_counts.values()))
print("Missing labels:", len(missing_labels))

if missing_labels:
    print("\nImages with missing labels:")
    for path in missing_labels:
        print(path)

print(f"\nDataset: {DEST}")
print(f"YAML   : {yaml_path}")
print("\nOriginal dataset was not modified.")

from pathlib import Path
from collections import defaultdict
import re
import random

ROOT = Path("data/datasets/singapore-maritime")

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


# --------------------------------------------------
# Collect statistics for each source video
# --------------------------------------------------

stats = defaultdict(lambda: {
    "images": 0,
    "objects": 0,
    "classes": [0] * len(CLASSES)
})

for old_split in ["train", "valid", "test"]:

    image_dir = ROOT / old_split / "images"
    label_dir = ROOT / old_split / "labels"

    for image_path in image_dir.iterdir():

        if not image_path.is_file():
            continue

        video = source_video(image_path.name)

        stats[video]["images"] += 1

        label_path = label_dir / (image_path.stem + ".txt")

        if not label_path.exists():
            continue

        for line in label_path.read_text().splitlines():

            if not line.strip():
                continue

            class_id = int(line.split()[0])

            if 0 <= class_id < len(CLASSES):

                stats[video]["classes"][class_id] += 1
                stats[video]["objects"] += 1


# --------------------------------------------------
# Reserve rare-class source videos
# --------------------------------------------------

assignments = {}

# Flying bird-plane exists in exactly 3 source videos.
# Reserve one complete source video for each split.
assignments["MVI_1463_NIR"] = "train"
assignments["MVI_1469_VIS"] = "valid"
assignments["MVI_1474_VIS"] = "test"

# Kayak exists in only 2 source videos.
# Therefore it cannot be represented in all three splits.
assignments["MVI_1609_VIS"] = "train"
assignments["MVI_1592_VIS"] = "test"

# Sail boat exists in 6 source videos.
# Reserve coverage for validation and test.
assignments["MVI_1452_VIS_Haze"] = "valid"
assignments["MVI_1478_VIS"] = "test"

# Boat exists in 6 source videos.
# Reserve source videos for validation and test coverage.
assignments["MVI_0790_VIS_OB"] = "valid"
assignments["MVI_0895_NIR_Haze"] = "test"

# --------------------------------------------------
# Assign remaining source videos
# Target approximately 70 / 20 / 10 images
# --------------------------------------------------

target_ratio = {
    "train": 0.70,
    "valid": 0.20,
    "test": 0.10
}

total_images = sum(
    s["images"]
    for s in stats.values()
)

target_images = {
    split: total_images * ratio
    for split, ratio in target_ratio.items()
}

current_images = {
    "train": 0,
    "valid": 0,
    "test": 0
}

for video, split in assignments.items():
    current_images[split] += stats[video]["images"]


remaining = [
    video
    for video in stats
    if video not in assignments
]

# Deterministic shuffle:
# running the script again gives the same result.
random.Random(42).shuffle(remaining)

# Assign larger video groups first.
remaining.sort(
    key=lambda v: stats[v]["images"],
    reverse=True
)


for video in remaining:

    # Choose the split currently furthest below
    # its target image count.
    split = max(
        ["train", "valid", "test"],
        key=lambda s: target_images[s] - current_images[s]
    )

    assignments[video] = split
    current_images[split] += stats[video]["images"]


# --------------------------------------------------
# Report proposed grouped split
# --------------------------------------------------

print("\n=== PROPOSED GROUPED SPLIT ===")

for split in ["train", "valid", "test"]:

    videos = sorted([
        video
        for video, assigned_split in assignments.items()
        if assigned_split == split
    ])

    images = sum(
        stats[v]["images"]
        for v in videos
    )

    objects = sum(
        stats[v]["objects"]
        for v in videos
    )

    percentage = 100 * images / total_images

    print(f"\n--- {split.upper()} ---")
    print("Videos :", len(videos))
    print("Images :", images, f"({percentage:.1f}%)")
    print("Objects:", objects)

    print("\nClass coverage:")

    for class_id, class_name in enumerate(CLASSES):

        count = sum(
            stats[v]["classes"][class_id]
            for v in videos
        )

        containing_videos = sum(
            stats[v]["classes"][class_id] > 0
            for v in videos
        )

        print(
            f"{class_name:<20} "
            f"objects={count:>6} "
            f"videos={containing_videos:>2}"
        )


# --------------------------------------------------
# Verify source-video leakage
# --------------------------------------------------

split_sets = {
    split: {
        video
        for video, assigned_split in assignments.items()
        if assigned_split == split
    }
    for split in ["train", "valid", "test"]
}

print("\n=== LEAKAGE CHECK ===")

print(
    "Train ∩ Valid:",
    len(split_sets["train"] & split_sets["valid"])
)

print(
    "Train ∩ Test :",
    len(split_sets["train"] & split_sets["test"])
)

print(
    "Valid ∩ Test :",
    len(split_sets["valid"] & split_sets["test"])
)


# --------------------------------------------------
# Verify total number of source videos
# --------------------------------------------------

assigned_videos = set(assignments)

print("\n=== FINAL CHECK ===")
print("Total source videos:", len(stats))
print("Assigned videos    :", len(assigned_videos))
print("Unassigned videos  :", len(set(stats) - assigned_videos))

print("\nNo files were copied or moved.")

# --------------------------------------------------
# Save split manifest
# --------------------------------------------------

import csv

manifest_path = ROOT / "split_manifest.csv"

with manifest_path.open("w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "source_video",
        "split",
        "images",
        "objects"
    ])

    for video in sorted(assignments):

        writer.writerow([
            video,
            assignments[video],
            stats[video]["images"],
            stats[video]["objects"]
        ])

print(f"\nSplit manifest saved to: {manifest_path}")

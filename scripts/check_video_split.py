from pathlib import Path
from collections import defaultdict

DATASET_DIR = Path("data/datasets/singapore-maritime")
SPLITS = ["train", "valid", "test"]

videos = defaultdict(set)

for split in SPLITS:
    images_dir = DATASET_DIR / split / "images"

    for image in images_dir.iterdir():
        if not image.is_file():
            continue

        name = image.stem

        if "_frame" in name:
            video = name.split("_frame")[0]
        else:
            video = name

        videos[video].add(split)

print("\nVideo Split Analysis\n")

shared = 0

for video, splits in sorted(videos.items()):
    if len(splits) > 1:
        shared += 1
        print(f"{video} --> {', '.join(sorted(splits))}")

print(f"\nVideos appearing in multiple splits: {shared}")
print(f"Total unique videos: {len(videos)}")


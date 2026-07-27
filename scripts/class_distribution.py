from pathlib import Path
from collections import Counter

DATASET_DIR = Path("data/datasets/singapore-maritime")
SPLITS = ["train", "valid", "test"]

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

counter = Counter()

for split in SPLITS:
    labels_dir = DATASET_DIR / split / "labels"

    for label_file in labels_dir.glob("*.txt"):
        with open(label_file, "r") as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    counter[class_id] += 1

print("\nClass Distribution\n")
total = sum(counter.values())

for i, name in enumerate(CLASS_NAMES):
    count = counter[i]
    percentage = (count / total) * 100 if total else 0
    print(f"{i:2d} {name:20s}: {count:6d} ({percentage:5.2f}%)")

print(f"\nTotal objects: {total}")

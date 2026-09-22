# Week 7 – Leak-Free Grouped Baseline

## 1. Dataset Split Reconstruction

The original Roboflow split was audited for source-video leakage.

- Total source videos: 63
- Total images: 6,350
- Total objects: 48,317
- All 63 source videos appeared in train, validation, and test in the original frame-level split.

The dataset was rebuilt using source-video-level grouping so that all frames
from one source video belong to exactly one split.

### Final grouped split

| Split | Source videos | Images | Objects |
|---|---:|---:|---:|
| Train | 41 | 4,471 | 34,555 |
| Validation | 14 | 1,257 | 8,560 |
| Test | 8 | 622 | 5,202 |

Approximate image ratio:

- Train: 70.4%
- Validation: 19.8%
- Test: 9.8%

### Leakage check

- Train ∩ Validation: 0 source videos
- Train ∩ Test: 0 source videos
- Validation ∩ Test: 0 source videos

All 6,350 images and all 48,317 annotations were preserved.

There are 83 empty label files representing background images.

## 2. Class Coverage

Total annotations:

| Class | Objects |
|---|---:|
| Boat | 382 |
| Buoy | 750 |
| Ferry | 2,237 |
| Flying bird-plane | 231 |
| Kayak | 865 |
| Other | 6,412 |
| Sail boat | 616 |
| Speed boat | 2,227 |
| Vessel-ship | 34,597 |

Kayak occurs in only two independent source videos. Therefore, it was not
possible to represent this class in train, validation, and test simultaneously
without introducing source-video leakage. The two Kayak source videos were
assigned to train and test, so Kayak is absent from the validation set.

## 3. Leak-Free YOLO11n Baseline

Model: YOLO11n pretrained weights  
Image size: 640  
Maximum epochs: 50  
Early stopping patience: 10

Training stopped automatically after epoch 17 because the validation metric
did not improve for 10 consecutive epochs. The best checkpoint was obtained
at epoch 7.

### Validation results – best.pt

- Precision: 0.694
- Recall: 0.460
- mAP@50: 0.457
- mAP@50-95: 0.303

| Class | mAP@50 | mAP@50-95 |
|---|---:|---:|
| Boat | 0.000 | 0.000 |
| Buoy | 0.872 | 0.740 |
| Ferry | 0.556 | 0.328 |
| Flying bird-plane | 0.000 | 0.000 |
| Other | 0.305 | 0.079 |
| Sail boat | 0.914 | 0.702 |
| Speed boat | 0.208 | 0.128 |
| Vessel-ship | 0.805 | 0.450 |

Kayak is not reported because it has no validation instances.

## 4. Held-Out Test Results

The best checkpoint was evaluated on the grouped test set containing
622 images and 5,202 objects.

- Precision: 0.323
- Recall: 0.201
- mAP@50: 0.185
- mAP@50-95: 0.0996

| Class | mAP@50 | mAP@50-95 |
|---|---:|---:|
| Boat | 0.010 | 0.004 |
| Buoy | 0.580 | 0.298 |
| Ferry | 0.153 | 0.076 |
| Flying bird-plane | 0.000 | 0.000 |
| Kayak | 0.000 | 0.000 |
| Other | 0.067 | 0.030 |
| Sail boat | 0.026 | 0.008 |
| Speed boat | 0.059 | 0.029 |
| Vessel-ship | 0.767 | 0.453 |

## 5. Initial Observations

Performance drops substantially when evaluated on unseen source videos,
indicating that source-video leakage in the previous frame-level split could
produce overly optimistic evaluation results.

Vessel-ship generalizes best to the held-out test videos, while several
minority classes show poor cross-video generalization.

The large validation-to-test difference for Sail boat should be interpreted
carefully because the validation instances of this class come from only one
source video.

These results will be used as the leak-free baseline for subsequent
controlled experiments.

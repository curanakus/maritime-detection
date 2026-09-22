# Error Analysis Summary

## Objective

After establishing the leak-free YOLO11n baseline, error analysis was performed to understand the poor generalization observed on the held-out source-video test set.

The analysis focused on:

- class imbalance,
- class coverage across train/validation/test,
- object-scale differences,
- source-video diversity,
- and visual differences between training and test scenes.

## Dataset Structure

The grouped dataset contains 63 independent source videos.

The source-video split remains leakage-free:

- Train: 41 source videos
- Validation: 14 source videos
- Test: 8 source videos

No source video is shared between splits.

## Class Distribution

Training set:

- Boat: 332 (0.96%)
- Buoy: 262 (0.76%)
- Ferry: 1342 (3.88%)
- Flying bird-plane: 101 (0.29%)
- Kayak: 705 (2.04%)
- Other: 4475 (12.95%)
- Sail boat: 452 (1.31%)
- Speed boat: 1529 (4.42%)
- Vessel-ship: 25357 (73.38%)

The training set is strongly dominated by Vessel-ship.

Class distributions also differ substantially between the grouped train, validation, and test sets. For example, Buoy represents 0.76% of training instances but 6.71% of test instances, while Ferry increases from 3.88% to 11.63%.

## Source-Video Diversity

The number of independent source videos containing each class is:

| Class | Total Videos | Train | Validation | Test |
|---|---:|---:|---:|---:|
| Boat | 6 | 4 | 1 | 1 |
| Buoy | 7 | 3 | 2 | 2 |
| Ferry | 18 | 10 | 4 | 4 |
| Flying bird-plane | 3 | 1 | 1 | 1 |
| Kayak | 2 | 1 | 0 | 1 |
| Other | 32 | 21 | 7 | 4 |
| Sail boat | 6 | 4 | 1 | 1 |
| Speed boat | 20 | 13 | 4 | 3 |
| Vessel-ship | 63 | 41 | 14 | 8 |

A major limitation was identified for minority classes.

All 705 Kayak instances in the training set originate from a single source video (MVI_1609). The 160 Kayak instances in the test set originate from a different source video (MVI_1592), while the validation set contains no Kayak instances.

Therefore, the apparently large number of Kayak annotations does not correspond to high scene or source-video diversity.

Flying bird-plane is similarly limited to only three source videos in the complete dataset.

## Object-Scale Analysis

Median bounding-box area as percentage of image area:

| Class | Train | Validation | Test |
|---|---:|---:|---:|
| Boat | 0.613% | 0.124% | 0.052% |
| Buoy | 0.476% | 0.724% | 0.064% |
| Ferry | 0.200% | 0.327% | 0.371% |
| Flying bird-plane | 0.038% | 0.035% | 0.051% |
| Kayak | 0.046% | N/A | 0.217% |
| Other | 0.053% | 0.042% | 0.148% |
| Sail boat | 1.307% | 7.331% | 0.050% |
| Speed boat | 0.129% | 0.132% | 0.212% |
| Vessel-ship | 0.341% | 0.367% | 0.694% |

Several classes show substantial object-scale shift between source videos.

The strongest example is Sail boat. Its median bounding-box area decreases from 1.307% in training to only 0.050% in test, meaning that the median test Sail boat occupies approximately 26 times less image area.

Boat and Buoy also appear substantially smaller in the test set.

Kayak provides an important counterexample: test Kayaks are larger on average than training Kayaks, yet detection performance remains extremely poor. Therefore, Kayak failure cannot be explained by small-object size alone.

## Visual Inspection

Training and test examples were visually compared for Kayak and Sail boat.

Kayak training examples were highly similar and originated from the same source video. Test Kayaks appeared in a different scene with different background and vessel configuration.

This supports the conclusion that the model has limited source-domain diversity for this class.

Sail boat examples showed a clear scale and scene difference. Training Sail boats were relatively large and visually prominent, while test Sail boats were distant and much smaller.

## Interpretation

The leak-free evaluation reveals several interacting limitations:

1. Strong class imbalance, particularly the dominance of Vessel-ship.
2. Limited source-video diversity for minority classes.
3. Missing validation coverage for Kayak.
4. Significant object-scale shifts between source videos.
5. Scene/domain differences between training and held-out test videos.

The low performance of minority classes should therefore not be interpreted only as a model-capacity problem.

Increasing model size or training duration alone cannot address the limited source-video diversity.

## Conclusion

The source-video-grouped split should remain fixed for controlled experiments because it prevents adjacent-frame leakage and provides a more realistic generalization benchmark.

The analysis also demonstrates an inherent dataset limitation: some minority classes occur in too few independent source videos to obtain representative train, validation, and test coverage simultaneously.

These limitations will be considered when interpreting subsequent controlled experiments.

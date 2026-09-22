# Maritime Detection Traineeship Notes

## Week 1 - Enviroment Setup 

### Completed
-Created project structure
-Initialized Git repository
-Created and activated a Python virtual enviroment
-Installed Ultralytics (v8.4.84)
-Installed PyTorch and required dependencies


### Experiments
-Ran YOLO11 prediction on the sample image (bus.jpg)
-RAn YOLO11 tracking on an underwater pipeline video


### Observations
-The pretrained COCO model correctly detected common objects such as buses and people
-It failed to recognize underwater pipelines because pipelines are not included in the COCO dataset
-This confirms that fine-tuning on maritşme-specific datasets will be necessary



##Week 2 -Maritime Small Object Detection

### Objectives
-Read the maritime small-object survey
-Understand why maritime objet detection is challenging
-Learn the basic concepts used in object detection

### Completed
-Read the introduction of the maritime survey paper
-Learned the differences between generic object detection and maritime object detection
-Studied common challenges in maritime environments:
 -Small objects
 -Long camera-object distance
 -Water reflections and glare
 -Waves and sea clutter
 -Weather conditions (fog, haze, rain)
 -Occlusion
 -Scale variation
-Learned the meaning of:
 -IoU
 -mAP
 -Precision
 -Recall
 -Bounding Box

### Observations
-Maritime images are more dif. than general images because objects are usually very small and far away
-Reflections, horizon, waves and changing weather make object detection more challing
-Generic pretrained models often perform poorly without fine-tuning on maritime datasets.

### Week 3 - Singapore Maritime Dataset

### Objectives 
-Download the Singapore Maritime dataset
-Learn the YOLO dataset structure
-Understand YOLO annotation format
-Visualize annotated images

### Completed 
-Downloaded the Singapore Maritime dataset from Roboflow 
-Exported the dataset ein YOLO11 format
-Added the dataset to the project 
-Explored the dataset structure 
-Examined the data.yaml file
-Learned the purpose of train, validation and test sets
-Visualized multiple annotated images

# Week 4 - YOLO11 Training and Initial Evaluation

## Model Training

- Fine-tuned the YOLO11n model using the Singapore Maritime dataset.
- Trained the model on the prepared train/validation split.
- Monitored training progress using loss curves and evaluation metrics.

## Training Outputs

Generated training artifacts including:

- best.pt
- last.pt
- results.png
- confusion_matrix.png
- BoxF1_curve.png
- BoxPR_curve.png
- BoxP_curve.png
- BoxR_curve.png
- labels.jpg
- train_batch*.jpg
- val_batch*.jpg

## Initial Evaluation

- Examined precision, recall, and mAP values during training.
- Reviewed the confusion matrix to identify common classification errors.
- Verified that the training completed successfully without major issues.

## Observations

- The model successfully converged during training.
- Detection performance was strong for dominant classes.
- Performance of minority classes will be further analyzed through dataset statistics and future experiments.


# Week 5 - Dataset Inspection and Quality Assessment

## Dataset Integrity Check

- Verified the dataset structure and confirmed that all images have corresponding label files.
- No missing images or missing annotation files were detected.
- All YOLO annotation files follow the correct YOLO format.
- No invalid class IDs or invalid normalized coordinates were found.

## Empty Label Inspection

- Identified 83 empty label files across the dataset.
- Manually inspected several corresponding images.
- Confirmed that these images do not contain annotated maritime objects and therefore represent valid negative samples rather than missing annotations.

## Dataset Statistics

| Split | Images | Objects |
|-------|-------:|--------:|
| Train | 4445 | 33886 |
| Validation | 1270 | 9581 |
| Test | 635 | 4850 |

**Total images:** 6350

**Total annotated objects:** 48317

## Class Distribution

| Class | Objects | Percentage |
|------|---------:|-----------:|
| Vessel-ship | 34597 | 71.60% |
| Other | 6412 | 13.27% |
| Ferry | 2237 | 4.63% |
| Speed boat | 2227 | 4.61% |
| Kayak | 865 | 1.79% |
| Buoy | 750 | 1.55% |
| Sail boat | 616 | 1.27% |
| Boat | 382 | 0.79% |
| Flying bird-plane | 231 | 0.48% |

The dataset is highly imbalanced. More than 70% of all annotations belong to the **Vessel-ship** class, while some classes contain fewer than 2% of the total objects.

## Video Split Analysis

The dataset contains **63 unique source videos**.

All 63 videos appear in the train, validation, and test splits, indicating that the dataset was split at the image/frame level rather than at the video level.

This means that visually similar frames from the same video may exist in different dataset splits, which could lead to optimistic evaluation results because the model is tested on scenes that are very similar to those used during training.

## Conclusion

The dataset is structurally clean and suitable for training.

However, two important characteristics should be considered during evaluation:

- Significant class imbalance (Vessel-ship represents 71.60% of all annotations).
- Frame-level train/validation/test splitting may introduce similarity between evaluation sets.

# Week 6 - Evaluation and Tracking Preparation

## Evaluation Protocol

- Evaluated the trained YOLO11n model on the validation split of the Singapore Maritime dataset.
- Selected **mAP@50** as the primary evaluation metric.
- Also monitored **Precision**, **Recall**, and **mAP@50-95** to evaluate detection and localization performance.

## Training Results

The training curves show consistent learning throughout the five training epochs.

- Training losses (box, classification, and DFL) decrease steadily.
- Validation losses follow the same downward trend.
- Precision, Recall, mAP@50, and mAP@50-95 all improve during training.
- No obvious signs of overfitting are observed after five epochs, although the model is still in an early training stage.

## Exploratory Analysis of Difficult Images

Inspection of the validation predictions reveals that:

- Large vessels are detected reliably with high confidence.
- Small boats and buoys near the horizon are the most challenging objects.
- Low contrast, haze, and small object size reduce detection confidence.
- Very few false positives are observed, while some distant objects are still missed.
- These observations are consistent with the higher Precision than Recall.

## SORT Overview

Reviewed the basic principles of the SORT (Simple Online and Realtime Tracking) algorithm.

- Kalman Filter predicts the next position of each tracked object.
- Hungarian Algorithm associates new detections with existing tracks using IoU.
- This allows objects to maintain consistent IDs across consecutive video frames.
- Understanding this workflow provides a foundation for the upcoming tracking tasks.

# Week 7 - Source-Video Grouped Dataset Split

## Source-Video Split Reconstruction

- Rebuilt the Singapore Maritime dataset split using source videos instead of individual frames.
- Ensured that all frames originating from the same source video belong to exactly one split.
- Created a split manifest containing the source-video assignment and image/object counts.
- Preserved the original Roboflow dataset and created a separate grouped dataset for subsequent experiments.

## Grouped Dataset Statistics

| Split | Source Videos | Images | Objects |
|-------|--------------:|-------:|--------:|
| Train | 41 | 4471 | 34555 |
| Validation | 14 | 1257 | 8560 |
| Test | 8 | 622 | 5202 |

**Total source videos:** 63  
**Total images:** 6350  
**Total annotated objects:** 48317

The resulting image distribution is approximately:

- Train: 70.4%
- Validation: 19.8%
- Test: 9.8%

## Leakage Verification

Verified source-video overlap after rebuilding the dataset:

- Train ∩ Validation: 0
- Train ∩ Test: 0
- Validation ∩ Test: 0

Therefore, no source video is shared between the training, validation, and test sets.

This removes the source-video leakage identified in the original frame-level split.

## Dataset Integrity

- All 6350 original images were preserved.
- All 48317 annotations were preserved.
- All images have corresponding label files.
- The dataset still contains 83 valid empty label files representing background images.
- No source videos were left unassigned.

## Class Coverage

Checked class coverage independently for each grouped split.

All classes are represented in the training and test sets.

The **Kayak** class is absent from the validation set because Kayak annotations occur in only two independent source videos. It is therefore impossible to place Kayak in all three splits without assigning frames from the same source video to multiple splits and reintroducing leakage.

The two Kayak source videos were assigned to the training and test sets.

## Conclusion

The original frame-level split contained complete source-video overlap, with all 63 source videos occurring across train, validation, and test.

The reconstructed grouped split eliminates this overlap while preserving the complete dataset and approximately maintaining a 70/20/10 image distribution.

This grouped dataset will be used as the leak-free basis for subsequent detector training, evaluation, and tracking experiments.

## Week 8 - Leak-Free YOLO11n Baseline

### Training
- Trained YOLO11n on the source-video-grouped dataset.
- Used the grouped split to prevent frame-level data leakage.
- Model: YOLO11n
- Image size: 640
- Maximum epochs: 50
- Patience: 10
- Training stopped early at epoch 17.
- Best checkpoint: epoch 7.

### Validation Results
- Precision: 0.6943
- Recall: 0.4592
- mAP50: 0.4575
- mAP50-95: 0.3032

### Held-Out Test Results
- Images: 622
- Instances: 5202
- Precision: 0.323
- Recall: 0.201
- mAP50: 0.185
- mAP50-95: 0.0996
- Inference time: 2.7 ms/image

### Observations
- Vessel-ship performed much better than the minority classes.
- Vessel-ship: Recall 0.812, mAP50 0.767, mAP50-95 0.453.
- Buoy: Recall 0.268, mAP50 0.580.
- Kayak and Flying bird-plane had zero precision and recall.
- Visual inspection showed that many small objects, especially kayaks, were completely missed.
- Some Ferry objects were missed or confused with other vessel classes.
- The confusion matrix showed high false-negative rates for small and minority classes.
- Performance on the grouped test set was substantially lower than the previous frame-level evaluation, confirming that the previous split gave an optimistic estimate.

### Conclusion
The grouped baseline provides a more trustworthy benchmark. The main problem is low recall and poor generalization for small and minority maritime objects. The next step is to run controlled experiments while keeping the grouped split fixed.

# Week 9 - Controlled Experiments and Error Analysis

## Controlled Experiments

Several controlled experiments were performed while keeping the leak-free source-video split fixed.

### Higher Input Resolution

YOLO11n was evaluated with an input size of 960 instead of 640.

Held-out test results:

- Precision: 0.250
- Recall: 0.223
- mAP50: 0.218
- mAP50-95: 0.112

Higher resolution improved recall and both mAP metrics compared with the 640 baseline, suggesting that object scale may contribute to detection difficulty.

### Reduced Mosaic Augmentation

YOLO11n was trained at 640 resolution with mosaic reduced to 0.5.

Held-out test results:

- Precision: 0.241
- Recall: 0.167
- mAP50: 0.183
- mAP50-95: 0.0968

Reduced mosaic augmentation did not improve the baseline.

### Longer Training

YOLO11n was forced to train for the full 50 epochs by disabling early stopping.

The best validation mAP50-95 was 0.3032 at epoch 8, while the final epoch decreased to 0.23677.

The best checkpoint produced the same held-out test performance as the original baseline:

- Precision: 0.323
- Recall: 0.201
- mAP50: 0.185
- mAP50-95: 0.0996

Therefore, longer training did not improve generalization.

### Larger Model

YOLO11s was trained at 640 resolution.

Held-out test results:

- Precision: 0.231
- Recall: 0.218
- mAP50: 0.208
- mAP50-95: 0.113
- Inference time: 4.4 ms/image

Compared with YOLO11n, YOLO11s provided a modest improvement in recall and mAP but did not solve the poor performance of minority classes.

## Error Analysis

Further analysis was performed to understand the remaining generalization errors.

### Class Imbalance

The training set contains 34,555 annotated objects.

Vessel-ship accounts for 25,357 instances, or 73.38% of all training annotations.

Several minority classes have substantially fewer annotations and much lower source-video diversity.

### Source-Video Diversity

The complete dataset contains 63 independent source videos.

Number of source videos containing each class:

- Boat: 6
- Buoy: 7
- Ferry: 18
- Flying bird-plane: 3
- Kayak: 2
- Other: 32
- Sail boat: 6
- Speed boat: 20
- Vessel-ship: 63

A particularly important limitation was found for Kayak.

All 705 training Kayak instances come from only one source video (MVI_1609). The 160 test Kayak instances come from a different source video (MVI_1592), and no Kayak examples exist in validation.

Therefore, a large annotation count does not necessarily correspond to high visual or source-video diversity.

### Object-Scale Shift

Bounding-box size distributions were compared between splits.

Several classes show substantial scale differences between training and test videos.

Examples:

- Boat median area: 0.613% train -> 0.052% test
- Buoy median area: 0.476% train -> 0.064% test
- Sail boat median area: 1.307% train -> 0.050% test
- Kayak median area: 0.046% train -> 0.217% test

Sail boats are therefore substantially smaller in the test set than in training.

Kayaks, however, are larger in test than in training while still performing poorly, showing that small-object size alone does not explain all errors.

### Visual Inspection

Kayak and Sail boat examples were visually compared between training and test source videos.

Kayak training samples were highly similar and originated from a single source video, whereas test samples came from a visually different scene.

Sail boat samples showed a strong scale and scene shift, with test objects appearing much smaller and more distant.

## Week 9 Conclusion

The controlled experiments show that increasing resolution and model capacity provides only modest improvements, while longer training and reduced mosaic augmentation do not improve generalization.

Error analysis indicates that the remaining performance gap is strongly related to dataset characteristics, particularly:

- class imbalance,
- limited source-video diversity for minority classes,
- missing Kayak validation coverage,
- object-scale shift,
- and scene/domain differences between independent source videos.

The leak-free grouped split will remain fixed for subsequent controlled experiments rather than reintroducing frame-level leakage.

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

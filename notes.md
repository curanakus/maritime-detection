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

Today I learned git status

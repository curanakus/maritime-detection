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



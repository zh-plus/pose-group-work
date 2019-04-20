## Log

### 2019.4.20

#### methods for image standardization

1. full image scaling based on the left lower corner & full image scaling based on the keypoint 1

    + code: ```util.py```
    
    + test: ```test.png```

2. partial skeleton length scaling based on the keypoint 1

    + code: ```crop_scale.py```
    
    + test: ```crop_scale_test.png```, ```crop_scale_keypoints.json```
   
#### trainer skeleton data

includes original images, skeleton images and skeleton keypoints data

  + keypoints meaning: ```configuration.py```
  
  + trainer dataset: in the folder```output```
    

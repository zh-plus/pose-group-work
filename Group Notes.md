### 2019.3.3

#### 工程化思路

1. 对多个教练的教练图片生成的关节信息做归一化（对图片缩放到一个相同的尺度）

2. 对归一化后的数据求均值、方差等关键统计信息

3. 对student图片做与1相同的归一化

4. 利用统计信息对3中的火柴人姿态示意错误位置


#### 3D角度判断思路

1. 三点成面

2. 利用这个面对第四个点的距离、正反面等信息进行分析

#### 分工

- 王森驰:
  - 收集健身数据（暂时只收集几个最典型的动作，最好正反都有），或许需对数据进行预处理
  - 研究骨架规范化及其比较

- 谭树杰:
  - 部署基于手势的人机交互模型

- 陆天鑫:
  -  部署从2D图像估计3D姿态的模型（因为懂CG）

- 刘毅阳:
  - 收集健身数据（暂时只收集几个最典型的动作，最好正反都有），或许需对数据进行预处理

- 郑浩:
  - 部署实时性较好的2D姿态估计模型，归一化处理
  - 研究骨架规范化及其比较

#### 杂项

- 按照微信群中的顺序轮流做周报

- 每周日下午或晚上，本科生一起讨论、Coding

### 2019.3.10 第二次会议 

#### 收集到的开源项目

- [Realtime Multi-Person Pose Estimation](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation)

    CVPR2017 (Oral) GTX 1080
    
    9 people : 10 fps ; 19 people : 8.8 fps
    
    TF, Pytorch 

- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

- [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose)
   
   iccv2017
   
   4.6 people : 20 fps 
   
   General version, 3X faster
   
   Pytorch

- [Deep High-Resolution Representation Learning for Human Pose Estimation](https://github.com/leoxiaobin/deep-high-resolution-net.pytorch)
   
   Microsoft
   
   CVPR2019
   
   fps not mentioned   
   
   Pytorch 

#### 下周任务

- 大家分配着跑这几个项目，并且看看代码实现，关键点在于获得关节点的位置信息。

    郑浩：Deep High-Resolution Representation Learning for Human Pose Estimation

    陆天鑫：AlphaPose

    刘毅阳：Realtime Multi-Person Pose Estimation

    谭树杰：hand pose

#### 杂项

- 可以从keep网站上获得健身视频
- 考虑用3D建模合成数据


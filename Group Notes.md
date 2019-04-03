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


### 2019.3.18 第四次讨论

#### 工程化思路

1. 收集十个以上的coach pose，人工截取【起始动作】【若干个关键帧的截图】

2. 核心思路：两次分类
    假设条件：假定我们有13个coach，每个骨骼有36个关节点，我们系统有三个动作：深蹲 俯卧撑 卷腹，每个动作包含4~5个决定性的关键帧，分别称为深蹲1，深蹲     2……

3. 【第一次分类】
    分别将13个coach某个特定动作【比如都是深蹲】的起始动作拿出来归一化，对这个起始动作的13张归一化图片进行【聚类】得到【深蹲起始真正的ground truth】
    同理可得一共三个动作起始动作的ground truth。用户开始动作的时候，前一段时间先进行对比，相似概率最大的一组即为当前用户所作动作。
    【第一次分类的目的是，判断用户所执行的动作】

4. 【第二次分类】
     提前截取13个coach深蹲的关键帧1 2 3 4.分别进行聚类得到深蹲1234的ground truth。在用户做动作时对应重合概率最高的一帧即为关键帧。
     【第二次分类的目的是截关键帧】
5. 对比关键帧和ground truth，找出概率分布，低于阈值的点标红并提示。

#### 可能存在的难点

1. 关键帧如何实时截取？关键帧截取之后又要和ground truth对比关节点，那么怎么选最合适的截图点才能保证截到最准确的关键帧？【基于经验选达到某个概率就截     图，想想看在这能用到哪些机器学习方法】

#### 分工
- 没跑完程序的把程序跑了，找一个代码测试最佳检测角度。如果某些动作性能极差那么寻找每个动作的最佳角度
- 对于遮挡，你们去看一下lstm模块是怎么融合进姿态估计的，增加鲁棒性，试一下
- 找到角度以后开始录coach数据集
- 杰哥加油早日出paper

#### 杂项

- 找felix要经费买个2d摄像头


### 2019.3.25 第五次讨论

#### 工程化思路

1. ~~搜集多个角度的coach图片，并在判断动作时找到最match的角度~~ **角度太多**

2. 利用数据库进行高效的查询 (寻找关键帧的类型、时间节点)


#### 分工
- 本科生写报告、做PPT、准备答辩
- 研究生继续泛读论文，查找可用的思路、方法等

#### 杂项

- felix同意购置微软的Kinetic摄像头，尽快购买、报销



## 第一次答辩 总结

### Approach

As this project is to solve more engineered than research problem, the majority of works is the details of building the whole system. Currently, we have come up with a rough plan for the implementation.

The approach is divided into two sections. The first one is **coach building**, which means that we should find enough videos of standard body-building action and find the statistical information among these videos. The second one is **user correction**, which on the other hand, collect user video and analyze the correctness of specific body part by comparing user action with coach action. 

#### 3.1 Coach building

##### 3.1.1 Normalization

The height or width of the analyzed people would be different because of different body shape, different distance between people and camera, or different camera degrees. In this condition, we only take the first two factors into consideration as it's unpractical to get enough video from every degree in a 3D space. The main idea of normalization in size part is crop and zoom. 

###### Size normalization

As is known to all, the length of spread arms is as long as human height. Thus, taking the middle point of shoulder as center, we leave the space of upper, left and right as $ 1.2\times length_{arm} $, in which $1.2$ is the tolerance of the bias. As for the lower space, it is the lowest point adding $0.2\times length_{arm}$. There's a raised problem: what if the user lay down? The solution is to change the space direction into when detecting the lay down of user. This arm-based normalization promises that the user would not leave out of the cropped region while keeping customization for every user.

###### Aspect ratio normalization

After normalizing cropped size, the aspect ratio may not be the same because of bias. So we should zoom them again into a pre-defined ratio ($w\_pixel \times h\_pixel$), in order to further promising the effectiveness of comparing different images.

##### 3.1.2 Statistical information

The returned data from pose-estimation network contains the label of each point, so we can compute the statistical coordinate information of each joint among different coaches. We assume that the coordinates of same joint for different people at same action frame would form a 2D gaussian distribution, which can be represented as:

![2d_gaussian_formular](https://github.com/zh-plus/pose-group-work/blob/master/images/formular/2d_gaussian.png)

According to the mean and variance value, we can compute the confidence range according to given confidence level. This range can be used in determining the correctness of user action.

For $\mu = 0 , \sigma = 1​$, the 2D confidence level can be computed as following:

![2d_gaussian_confidence_level](https://github.com/zh-plus/pose-group-work/blob/master/images/formular/2d_gaussian_confidence_level.png)

#### 3.2 User correction

After doing the same normalization mentioned above, we can start comparing the user action and coach action. Here are the other problems:

- Which action the user is doing? 
- How to determine the image frame that user action is actually at that frame?

The answer of these two questions really depends on the approach of building dataset and extract key frame. Thus, they're remined to be the task of next period.



### Difficulty

Currently, there are 4 difficulties:

1. How to build coach dataset? Which key frames we should choose?
2. Whether we should consider the different degree or not?
3. How to determine which action user is doing?
4. How to determine if the user is at the key frame of action?



### Expectation and Schedule

Having explored current pose estimation networks, we settle down our objectives and expectations. In order to implement a complete system from pose estimation to deviation detection, we are going to build a fitness dataset for pose estimation, then apply our real-time rectify architecture, designing a feedback window. At last, we will testing our system and try the best to improve the performance including the accuracy and the response time.

| Time        | Work Arrangement                                             |
| ----------- | ------------------------------------------------------------ |
| 4.4-  4.15  | Build fitness data set  and label key frame.<br />Evaluate the pose estimation performance in different angles. |
| 4.15 - 5.05 | Implement deviation detection as well as the feedback GUI.   |
| 5.05 - 5.15 | Test the system by accuracy and response time.<br />Optimize the architecture of the network. |
| 5.15-5.30   | Apply further improvement in functions <br />such as multi-persons deviation detection or 3D transfer models. |
**Abstract**: In this paper, we introduce a  fitness training system based on 2D pose estimation, which automatically evaluate a user's performance and provides real-time feedback for the user to refine his current posture.  A method to measure posture is also described. 

**Keywords**: fitness training system, pose estimation, real-time

## 1.Introduction

Fitness is more and more popular recently, accompanying with people's growing pursuit of health. If you have a little understanding or experience to do fitness exercises, you should know the importance of correct fitness action. However if one person have not been trained professionally, an amateur, he will find it hard to do the correct action through pictures or video, which may cause serious injury. As a result, we aim to design a fitness training system to the people who have suspicion on the correctness of themselves' fitness action.



## 2.Related works

Human 2D pose estimation—the problem of localizing anatomical key points or “parts”—has largely focused on ﬁnding body parts of individuals[1].  Through pose estimation, the posture of a person is detected, so that it can be used to judge the correctness of an action.   Through the focal point of the paper is to measure the posture between coach and user, a well performed pose estimation framework is needed. We search all the open source project on the [github](www.github.com).  The keyword used is real time, pose estimation and we judge it by its stars and the latest released time.  We finally got three project:  Open Pose by CMU, Alpha Pose by SJTU and Deep High-Resolution Representation Learning by Microsoft.   Through compare, we finally decided to utilize Open Pose.  

#### Open pose

Open pose is designed to solve real-time multi-person pose estimation.  A common approach is to employ a person detector and perform single-person pose estimation for each detection, which will cause three problem:  First, each image may contain an unknown number of people that can occur at any position or scale. Second, interactions between people induce complex spatial interference, due to contact, occlusion, and limb articulations,making association of parts difﬁcult. Third,runtime complexity tends to grow with the number of people in the image, making real time performance a challenge[1].  The top-down approaches lead to many problem and cost lots of  the time.  Open Pose use bottom-up approaches which is named Part Affinity Fields(PAFs), actually a set of 2D vector ﬁelds that encode the location and orientation of limbs over the image domain[1].  It works fast, reach 5 fps on 1050ti, which can reach our needs if deployed on server. The network structure is the picture below.

![微信图片_20190403230126](https://github.com/zh-plus/pose-group-work/blob/master/images/first%20defense/network1.png)

F is the feature of the picture.  S is a set of detection conﬁdence maps which represents the information of the joint point.  T is a set of part afﬁnity ﬁelds which represents the limb.   The part afﬁnity is a 2D vector ﬁeld for each limb.  Parsing is first to find  all the body part and then to ﬁnd a matching with maximum weight for the chosen edges.   Additionally, the structure of VGG-19 is below.  It only contains blue Convolutional layer and red Pooling layer.

<img src="https://github.com/zh-plus/pose-group-work/blob/master/images/first%20defense/network1.png" style="zoom:70%"/>

#### Alpha pose

Recent pose estimation work is basically using either the top-down framework or the bottom-up framework. The former first builds human bounding boxes for each people and estimates each bounding box independently. The latter first recognizes all body parts then assembles them into appropriate human poses. 

Alpha Pose is a top-down framework which proposes a regional multi-person pose estimation network based on 2 novel components, Symmetric Spatial Transformer Network (SSTN), Parametric Pose Non-Maximum-Suppression (NMS) [2]. SSTN is used to handle the inaccurate bounding boxes problem. It detect humans by region proposal network, then apply spatial transform network on region of interests, afterwards one branch goes through single person pose estimation algorithm and spatial de-transformer networks which outputs the human proposal, and the other branch goes through parallel single person pose estimation, acting as a regularized corrector for spatial transformer network. Then the output human proposal goes through NMS to get the final pose. NMS is proposed to deal with the redundant detection problem which define the pose distance based on the box center and dimensions to eliminate redundant poses and leave one with the highest confident score.

#### Others

We also find a paper on  measurement of the posture [3], which uses Microsoft’s Kinect to get 3D information.  They measure the similarity between two skeleton frames on the base of joint angles rather than joint positions, to avoid a calibration procedure which is usually used to eliminate the errors caused by the diﬀerence between people’s body shapes[3].  Additionally, they use the weighted mean of the score of nine joints (L/R shoulder, L/R elbow, L/R Hip, L/R knee, spine) to determine the score of the users.  The weights are determined by the importance of every joint in the evaluation criteria.   



## 3.Approach

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
$$
f(x, y)=\left(2\pi \sigma_1 \sigma_2 \sqrt{1-\rho^2}\right)^{-1} exp\left[-\frac{1}{2(1-\rho^2)} \left(\frac{(x-\mu)^2}{\sigma_1^2} - \frac{2\rho(x-\mu_1)(y-\mu_2)}{\sigma_1 \sigma_2} + \frac{(y-\mu_2)^2}{\sigma_2^2} \right) \right]
$$
According to the mean and variance value, we can compute the confidence range according to given confidence level. This range can be used in determining the correctness of user action.

For $\mu = 0 , \sigma = 1​$, the 2D confidence level can be computed as following:
$$
\begin{split}
P(r) = Pr\lbrace X^TX\le r^2 \rbrace &= \iint\limits_{x^2 + y^2 \le r^2} \left( \frac{1}{\sqrt{2\pi}} \right)^2 exp\lbrace -\frac{x^2+y^2}{2} \rbrace dxdy \\
&= \frac{1}{2\pi} \int_0^{2\pi} \int_0^r re^{-\frac{r^2}{2}}drd\theta \\
&= 1 - exp\lbrace {-\frac{r^2}{2}} \rbrace
\end{split}
$$

#### 3.2 User correction

After doing the same normalization mentioned above, we can start comparing the user action and coach action. Here are the other problems:

- Which action the user is doing? 
- How to determine the image frame that user action is actually at that frame?

The answer of these two questions really depends on the approach of building dataset and extract key frame. Thus, they're remined to be the task of next period.



## 4.Difficulty

Currently, there are 4 difficulties:

1. How to build coach dataset? Which key frames we should choose?
2. Whether we should consider the different degree or not?
3. How to determine which action user is doing?
4. How to determine if the user is at the key frame of action?



## 5.Expectation and Schedule

Having explored current pose estimation networks, we settle down our objectives and expectations. In order to implement a complete system from pose estimation to deviation detection, we are going to build a fitness dataset for pose estimation, then apply our real-time rectify architecture, designing a feedback window. At last, we will testing our system and try the best to improve the performance including the accuracy and the response time.

| Time        | Work Arrangement                                             |
| ----------- | ------------------------------------------------------------ |
| 4.4-  4.15  | Build fitness data set  and label key frame.<br />Evaluate the pose estimation performance in different angles. |
| 4.15 - 5.05 | Implement deviation detection as well as the feedback GUI.   |
| 5.05 - 5.15 | Test the system by accuracy and response time.<br />Optimize the architecture of the network. |
| 5.15-5.30   | Apply further improvement in functions <br />such as multi-persons deviation detection or 3D transfer models. |



## 6.Responsibility

Hao Zheng is responsible for architecture implementation. Yiyang Liu is responsible for dataset building and labeling. Tianxin Lu is responsible for network evaluation and testing.



## References:

[1] : Cao, Z., Simon, T., Wei, S. E., & Sheikh, Y. (2016). Realtime multi-person 2d pose estimation using part affinity fields.

[2] Fang, H. S., Xie, S., Tai, Y. W., & Lu, C. (2017). RMPE: Regional Multi-person Pose Estimation. *IEEE International Conference on Computer Vision*.

[3] : Jin, Y. , Hu, X. , & Wu, G. S. . (2012). *A Tai Chi Training System Based on Fast Skeleton Matching Algorithm*. *Computer Vision – ECCV 2012. Workshops and Demonstrations*. Springer Berlin Heidelberg.


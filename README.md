# Ros_Self_Control
基于ROS2的机器移动小车

## 技术环境
Ubuntu 22.04, ROS2 Humble, C++

## 已实现功能
1. **通信模块：**
基于rclcpp实现Publisher/Subscriber节点，完成Topic消息发布、订阅及实时通信

2. **模型构建：**
基于URDF/Xacro构建BumperBot模型，完成底盘、驱动轮、支撑轮及关节运动关系绘制
   <img width="600" height="389" alt="image" src="https://github.com/user-attachments/assets/d0f87917-ddcb-4439-b875-517a247918f0" />

3. **参数管理：**
基于rclcpp实现ROS2节点参数声明、动态配置与参数变更回调校验

4. **可视化启动：**
基于RViz2、URDF与TF实现模型及关节状态可视化，编写Launch统一启动节点并加载RViz配置


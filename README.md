# Ros_Self_Control
基于ROS2的机器移动小车

## 技术环境
Ubuntu 22.04, ROS2 Humble, C++

## 已实现功能
通信模块：
基于rclcpp实现Publisher/Subscriber节点，完成Topic消息发布、订阅及实时通信

模型构建：
基于URDF/Xacro构建BumperBot模型，完成底盘、驱动轮、支撑轮及关节运动关系绘制

参数管理：
基于rclcpp实现ROS2节点参数声明、动态配置与参数变更回调校验



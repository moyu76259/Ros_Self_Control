#文件路径
import os

#获取ROS2
from ament_index_python.packages import get_package_share_directory
import xacro

#Launch组件
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration

#ROS2节点参数配置
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    bumperbot_description_dir = get_package_share_directory("bumperbot_description")
    #声明model参数
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            bumperbot_description_dir,
            "urdf",
            "bumperbot.urdf.xacro"
        ),
        description="Absolute path to robot URDF file"
    )

    # 读取模型并发布 TF，支持带空格的文件路径。
    def robot_state_publisher(context):
        model_path = LaunchConfiguration("model").perform(context)
        robot_description = ParameterValue(xacro.process_file(model_path).toxml(), value_type=str)
        return [Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
        )]

    #启动关节控制GUI
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    #启动RViz2
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            os.path.join(
                get_package_share_directory("bumperbot_description"),
                "rviz",
                "display.rviz"
            )
        ]
    )

    #Launch系统执行
    return LaunchDescription([
        model_arg,
        OpaqueFunction(function=robot_state_publisher),
        joint_state_publisher_gui,
        rviz_node
    ])

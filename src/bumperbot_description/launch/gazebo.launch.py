#文件路径
import os
from pathlib import Path

#获取ROS2功能包路径
from ament_index_python.packages import get_package_share_directory
import xacro

#Launch组件
from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    ExecuteProcess,
    OpaqueFunction,
    SetEnvironmentVariable,
    Shutdown,
)
from launch.substitutions import LaunchConfiguration

#ROS2节点参数配置
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    #获取功能包目录
    bumperbot_description = get_package_share_directory("bumperbot_description")

    #声明model参数
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            bumperbot_description,
            "urdf",
            "bumperbot.urdf.xacro"
        ),
        description="Absolute path to robot urdf file"
    )

    gazebo_environment = [
        # 使用本机回环地址，避免 Gazebo 选中 VPN 或代理网卡。
        SetEnvironmentVariable(name="GZ_IP", value="127.0.0.1"),
        AppendEnvironmentVariable(
            name="GZ_SIM_RESOURCE_PATH",
            value=str(Path(bumperbot_description).parent.resolve()),
        ),
    ]
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        # 让 Gazebo 找到与 ROS 一起安装的控制插件。
        gazebo_environment.append(AppendEnvironmentVariable(
            name="GZ_SIM_SYSTEM_PLUGIN_PATH",
            value=str(Path(conda_prefix) / "lib"),
        ))

    # 解析 Xacro 并启动 TF 发布节点。直接传入文件路径，支持带空格的目录。
    def robot_state_publisher(context):
        model_path = LaunchConfiguration("model").perform(context)
        robot_description = ParameterValue(xacro.process_file(model_path).toxml(), value_type=str)
        return [Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description, "use_sim_time": True}],
        )]

    # macOS 将 Gazebo 的仿真服务端和图形界面作为独立进程启动。
    gazebo_server = ExecuteProcess(
        cmd=["gz", "sim", "-s", "-r", "empty.sdf", "--render-engine-server-api-backend", "metal"],
        output="screen",
        on_exit=Shutdown(reason="Gazebo server exited"),
    )
    gazebo_gui = ExecuteProcess(
        cmd=["gz", "sim", "-g", "--render-engine-gui", "ogre2", "--render-engine-gui-api-backend", "metal"],
        output="screen",
        on_exit=Shutdown(reason="Gazebo window closed"),
    )

    # 将 Gazebo 仿真时间同步给 ROS 2。
    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
    )

    #生成BumperBot实体
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic", "robot_description",
            "-name", "bumperbot"
        ]
    )

    #统一启动
    return LaunchDescription([
        model_arg,
        *gazebo_environment,
        OpaqueFunction(function=robot_state_publisher),
        gazebo_server,
        gazebo_gui,
        clock_bridge,
        gz_spawn_entity
    ])

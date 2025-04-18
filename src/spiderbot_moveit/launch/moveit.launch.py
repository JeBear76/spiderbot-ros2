from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    is_sim = LaunchConfiguration("is_sim")

    is_sim_args = DeclareLaunchArgument(
        name="is_sim",
        default_value='True',
        description='Are we working in the simulation'
        )


    spiderbot_description_dir = get_package_share_directory('spiderbot_description')
    spiderbot_moveit_dir = get_package_share_directory('spiderbot_moveit')

    moveit_config = MoveItConfigsBuilder(
        "spiderbot", 
        package_name="spiderbot_moveit"
        ).robot_description(
            file_path=os.path.join(spiderbot_description_dir,'urdf','spiderbot.urdf.xacro'),
        ).robot_description_semantic(
            file_path="config/spiderbot.srdf"
        ).trajectory_execution(
            file_path="config/moveit_controllers.yaml"
        ).planning_pipelines(
            pipelines=["ompl"]
        ).to_moveit_configs()
    
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": is_sim},
            {"publish_robot_description_semantic": True}
        ],
        arguments=[
            "--ros-args",
            "--log-level",
            "info"
        ]
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=["-d", os.path.join(spiderbot_moveit_dir, "rviz", "moveit.rviz")],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits
        ]
    )

    return LaunchDescription([
        is_sim_args,
        move_group_node,
        rviz2
    ])
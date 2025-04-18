from launch import LaunchDescription
# from launch.actions import RegisterEventHandler
# from launch.event_handlers import OnProcessStart
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch.conditions import UnlessCondition, IfCondition
import os

def generate_launch_description():
    is_sim_args = DeclareLaunchArgument(
        name="is_sim",
        default_value='True',
        description='Are we working in the simulation'
        )

    port_args = DeclareLaunchArgument(
        name="port",
        description="COM Port for arduino",
        default_value="/dev/ttyACM0"
    )
    
    is_sim = LaunchConfiguration("is_sim")
    port = LaunchConfiguration("port")

    spiderbot_description_dir = get_package_share_directory("spiderbot_description")

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    spiderbot_description_dir, "urdf", "spiderbot.urdf.xacro"
                ),
                " is_sim:=", is_sim,
                " port:=", port
            ]
        ),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        condition=UnlessCondition(is_sim)
    )

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": is_sim
            },
            os.path.join(
                get_package_share_directory("spiderbot_controllers"),
                "config",
                "spiderbot_controllers.yaml",
            )            
        ],
        condition=UnlessCondition(is_sim)
    )

    joint_state_broadcaster_spawnwer = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    fr_leg_controller_spawnwer = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["front_right_leg_controller", "--controller-manager", "/controller_manager"],
    )

    fl_leg_controller_spawnwer = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["front_left_leg_controller", "--controller-manager", "/controller_manager"],
    )

    br_leg_controller_spawnwer = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["back_right_leg_controller", "--controller-manager", "/controller_manager"],
    )

    bl_leg_controller_spawnwer = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["back_left_leg_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription(
        [
            is_sim_args,
            port_args,
            robot_state_publisher,
            controller_manager,
            joint_state_broadcaster_spawnwer,
            fl_leg_controller_spawnwer,
            fr_leg_controller_spawnwer,
            bl_leg_controller_spawnwer,
            br_leg_controller_spawnwer
        ]
    )

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("spiderbot_description"),
                "launch",
                "gazebo.launch.py"
            )
        )
    
    controller = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("spiderbot_controllers"),
                "launch",
                "controllers.launch.py"
            ),
            launch_arguments={"is_sim": "True"}.items()
        )
    
    moveit = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("spiderbot_moveit"),
                "launch",
                "moveit.launch.py"
            ),
            launch_arguments={"is_sim": "True"}.items()
        )
    
    return LaunchDescription([
        gazebo,
        controller,
        moveit
    ])
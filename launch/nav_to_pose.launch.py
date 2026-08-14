from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package='nr_py_nav2',
            executable='nav_to_pose',
            name='nav_to_pose',
            output='screen',
            emulate_tty=True,
        ),
    ])

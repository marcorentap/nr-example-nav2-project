from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package='py_nav2_example',
            executable='nav_to_pose',
            name='nav_to_pose',
            output='screen',
            emulate_tty=True,
        ),
    ])

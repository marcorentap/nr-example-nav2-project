"""Launch the nav_to_pose task against an already-running Nav2 stack.

The goal is a launch argument, so the same launch file covers every target:
`ros2 launch py_nav2_example nav_to_pose.launch.py x:=2.0 y:=0.5 yaw:=1.57`
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    frame_id = LaunchConfiguration('frame_id')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    yaw = LaunchConfiguration('yaw')

    return LaunchDescription([
        DeclareLaunchArgument(
            'frame_id', default_value='map',
            description='Frame the goal pose is expressed in.'),
        DeclareLaunchArgument(
            'x', default_value='-1.0',
            description='Goal position along x, in metres.'),
        DeclareLaunchArgument(
            'y', default_value='0.0',
            description='Goal position along y, in metres.'),
        DeclareLaunchArgument(
            'yaw', default_value='0.0',
            description='Goal heading, in radians.'),

        Node(
            package='py_nav2_example',
            executable='nav_to_pose',
            name='nav_to_pose',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'frame_id': frame_id,
                'x': x,
                'y': y,
                'yaw': yaw,
            }],
        ),
    ])

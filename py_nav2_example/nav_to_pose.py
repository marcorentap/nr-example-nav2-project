"""Send the robot to a single goal pose via the Nav2 simple commander.

Adapted from the Nav2 `nav_to_pose` demo. The goal is exposed as ROS
parameters instead of being hard-coded, so the same executable serves any
target without an edit-rebuild cycle.
"""

import math

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.duration import Duration

from py_nav2_example.runtime import run_navigator

DEFAULT_FRAME = 'map'
FEEDBACK_EVERY = 5


def say(navigator: BasicNavigator, message: str) -> None:
    """Report to the ROS log and to plain stdout.

    The logger is what `ros2 launch` aggregates and what ends up in
    ~/.ros/log, but it is easy to lose in a busy stack. The bare print is the
    debugging escape hatch: flush=True because stdout is block-buffered as
    soon as it is a pipe rather than a terminal, so unflushed prints would
    only appear once the process exits.
    """
    navigator.get_logger().info(message)
    print(f'[nav_to_pose] {message}', flush=True)


def _goal_pose(navigator: BasicNavigator) -> PoseStamped:
    navigator.declare_parameter('frame_id', DEFAULT_FRAME)
    navigator.declare_parameter('x', -1.0)
    navigator.declare_parameter('y', 0.0)
    navigator.declare_parameter('yaw', 0.0)

    # get_parameter_value() over .value: the typed field is what the ROS
    # parameter was declared as, no Optional to unwrap.
    yaw = navigator.get_parameter('yaw').get_parameter_value().double_value

    goal = PoseStamped()
    goal.header.frame_id = (
        navigator.get_parameter('frame_id').get_parameter_value().string_value
    )
    goal.header.stamp = navigator.get_clock().now().to_msg()
    goal.pose.position.x = navigator.get_parameter('x').get_parameter_value().double_value
    goal.pose.position.y = navigator.get_parameter('y').get_parameter_value().double_value
    # Planar goal: yaw is the only free rotation, so z/w carry the whole
    # quaternion and x/y stay at their zero defaults.
    goal.pose.orientation.z = math.sin(yaw / 2.0)
    goal.pose.orientation.w = math.cos(yaw / 2.0)
    return goal


def nav_to_pose(navigator: BasicNavigator) -> bool:
    """Drive to the parameterised goal; return True when Nav2 reports success."""
    goal = _goal_pose(navigator)
    say(navigator, f'goal pose: {goal.pose.position} {goal.pose.orientation}')

    # Nav2 is autostarted, so the action servers may not be up yet.
    say(navigator, 'waiting for Nav2 to become active')
    navigator.waitUntilNav2Active()

    say(
        navigator,
        f'navigating to x={goal.pose.position.x:g} '
        f'y={goal.pose.position.y:g} in {goal.header.frame_id!r}',
    )
    navigator.goToPose(goal)

    ticks = 0
    while not navigator.isTaskComplete():
        ticks += 1
        feedback = navigator.getFeedback()
        if feedback and ticks % FEEDBACK_EVERY == 0:
            eta = Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            say(
                navigator,
                f'eta {eta:.0f}s | {feedback.distance_remaining:.2f}m to go '
                f'| recoveries {feedback.number_of_recoveries}',
            )

    result = navigator.getResult()
    say(navigator, f'goal {TaskResult(result).name.lower()}')
    return result == TaskResult.SUCCEEDED


def main(args=None) -> None:
    run_navigator(nav_to_pose, args)


if __name__ == '__main__':
    main()

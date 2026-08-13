import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.duration import Duration


def main():
    rclpy.init()

    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = -1.0
    goal_pose.pose.position.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    navigator.goToPose(goal_pose)

    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            eta = Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            print(f'Estimated time of arrival: {eta:.0f} seconds.', flush=True)

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!', flush=True)
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!', flush=True)
    elif result == TaskResult.FAILED:
        print('Goal failed!', flush=True)
    else:
        print('Goal has an invalid return status!', flush=True)

    navigator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

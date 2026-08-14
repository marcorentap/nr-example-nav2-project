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
    goal_pose.pose.position.x = 0.0
    goal_pose.pose.position.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    navigator.goToPose(goal_pose)

    logger = navigator.get_logger()

    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            eta = Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            logger.info(f'Estimated time of arrival: {eta:.0f} seconds.')

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        logger.info('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        logger.warn('Goal was canceled!')
    elif result == TaskResult.FAILED:
        logger.error('Goal failed!')
    else:
        logger.error('Goal has an invalid return status!')

    navigator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

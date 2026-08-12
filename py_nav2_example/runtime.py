"""Shared navigator lifecycle handling."""

import signal
import sys

import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator


def run_navigator(task, args=None) -> None:
    """Run a one-shot navigation task, then tear it down exactly once.

    Navigation tasks are finite, unlike a spun node: `task` returns when the
    goal settles and the process exits with its verdict (0 on success, 1 on
    failure) so a launch file or shell caller can react.

    Ctrl-C in a terminal signals the whole foreground process group, and
    `ros2 launch` forwards SIGINT to its children on top of that, so teardown
    can be interrupted while already in progress. Ignoring SIGINT for the
    duration makes the shutdown path idempotent.
    """
    rclpy.init(args=args)
    navigator = BasicNavigator()
    succeeded = False
    try:
        succeeded = task(navigator)
    except KeyboardInterrupt:
        print('[runtime] interrupted', flush=True)
        # rclpy's default SIGINT handler may already have invalidated the
        # context, in which case cancelTask() cannot reach the action server
        # and only produces rosout publish errors.
        if rclpy.ok():
            print('[runtime] cancelling task', flush=True)
            navigator.cancelTask()
    finally:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        print('[runtime] shutting down', flush=True)
        navigator.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    print(f'[runtime] exit {0 if succeeded else 1}', flush=True)
    sys.exit(0 if succeeded else 1)

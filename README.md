# nr_py_nav2

Nav2 simple commander example: sends the robot to a goal pose and logs ETA
until the task completes.

Needs a running Nav2 stack (bringup or simulation) — the node blocks on
`waitUntilNav2Active()` until `amcl` and the navigation lifecycle are up.

## Setup

```bash
source /opt/ros/jazzy/setup.bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Build

```bash
source .venv/bin/activate
python3 -m colcon build --symlink-install
```

Use `python3 -m colcon`, not `colcon`, so the installed entry point gets the
venv interpreter.

## Run

```bash
source .venv/bin/activate
source install/setup.bash
ros2 launch nr_py_nav2 nav_to_pose.launch.py
```

Or the node directly:

```bash
ros2 run nr_py_nav2 nav_to_pose
```

Ctrl-C to stop.

The goal pose is hardcoded in `nr_py_nav2/nav_to_pose.py`
(`map` frame, x=0.0, y=0.0, yaw=0); no launch arguments.

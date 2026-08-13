ARG ROS2_DISTRO=jazzy

FROM ros:${ROS2_DISTRO}-perception
ARG ROS2_DISTRO

ENV ROS2_DISTRO=${ROS2_DISTRO}

RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3.12-venv \
    ros-${ROS2_DISTRO}-navigation2 \
    ros-${ROS2_DISTRO}-nav2-bringup \
    ros-${ROS2_DISTRO}-slam-toolbox \
    ros-${ROS2_DISTRO}-rosbridge-suite \
    ros-${ROS2_DISTRO}-ros2-control \
    ros-${ROS2_DISTRO}-ros2-controllers \
    ros-${ROS2_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS2_DISTRO}-xacro \
    libserial-dev \
    libgflags-dev \
    nlohmann-json3-dev \
    ros-${ROS2_DISTRO}-image-transport \
    ros-${ROS2_DISTRO}-image-transport-plugins \
    ros-${ROS2_DISTRO}-compressed-image-transport \
    ros-${ROS2_DISTRO}-compressed-depth-image-transport \
    ros-${ROS2_DISTRO}-theora-image-transport \
    ros-${ROS2_DISTRO}-image-publisher \
    ros-${ROS2_DISTRO}-camera-info-manager \
    ros-${ROS2_DISTRO}-diagnostic-updater \
    ros-${ROS2_DISTRO}-diagnostic-msgs \
    ros-${ROS2_DISTRO}-statistics-msgs \
    ros-${ROS2_DISTRO}-backward-ros \
    libdw-dev \
    libssl-dev \
    mesa-utils \
    libgl1 \
    libgoogle-glog-dev \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/${ROS2_DISTRO}/setup.bash" >> /etc/bash.bashrc

RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

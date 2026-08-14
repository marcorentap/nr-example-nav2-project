from glob import glob

from setuptools import find_packages, setup

package_name = 'nr_py_nav2'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='marcorentap',
    maintainer_email='marcorentap@example.com',
    description='Nav2 simple commander examples driving a robot to a goal pose.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'nav_to_pose = nr_py_nav2.nav_to_pose:main',
        ],
    },
)

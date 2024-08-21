#!/usr/bin/python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('navigation'), 'config')
    map_dir = os.path.join(get_package_share_directory('navigation'), 'map')
    map_file = os.path.join(map_dir, 'mp102.yaml')
    param_file = os.path.join(config_dir, 'params.yaml')

    if not os.path.exists(map_file):
        raise FileNotFoundError(f"Map file not found: {map_file}")
    if not os.path.exists(param_file):
        raise FileNotFoundError(f"Params file not found: {param_file}")

    return LaunchDescription([

        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen',
        #     # Uncomment and set the correct path if you have an RViz config file
        #     # arguments=['-d', os.path.join(config_dir, 'rviz_config.rviz')],
        # ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_file,
                'params_file': param_file
            }.items(),
        ),

        
    ])

if __name__ == '__main__':
    generate_launch_description()

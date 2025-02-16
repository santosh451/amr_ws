import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    world_dir = get_package_share_directory('navigation')

    world_path = os.path.join(world_dir, 'worlds', 'new5_world.world')
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world_path,
            description='Path to the world file to load'
        ),
        
        ExecuteProcess(
            cmd=['gazebo', '--verbose', LaunchConfiguration('world')],
            output='screen'
        )
    ])
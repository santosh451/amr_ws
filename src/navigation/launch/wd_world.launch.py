import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Define the path to the world file
    # world_file_path = '/home/santosh/amr_big_two_description/src/navigation/worlds/mv_world.world'
    world_dir = get_package_share_directory('navigation')

    world_path = os.path.join(world_dir, 'worlds', 'new5_world.world')
    
    return LaunchDescription([
        # Declare the launch argument for the world file
        DeclareLaunchArgument(
            'world',
            default_value=world_path,
            description='Path to the world file to load'
        ),
        
        # Start Gazebo with the specified world file
        ExecuteProcess(
            cmd=['gazebo', '--verbose', LaunchConfiguration('world')],
            output='screen'
        )
    ])
from launch import LaunchDescription
from launch_ros.actions import Node
# from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, LogInfo, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    navigation_launch_dir = get_package_share_directory('navigation')
    robot_dir = get_package_share_directory('amr_big_two_description')
    cartographer_slam_launch_dir = get_package_share_directory('cartographer_slam')
    laser_merge_dir = get_package_share_directory('ros2_laser_scan_merger')

    lidar_merge_path = os.path.join(laser_merge_dir, 'launch', 'merge_2_scan.launch.py')
    robot_launch_path = os.path.join(robot_dir, 'launch', 'gazebo.launch.py')
    ekf_launch_path = os.path.join(navigation_launch_dir, 'launch', 'ekf.launch.py')
    navigation_launch_path = os.path.join(navigation_launch_dir, 'launch', 'navigation.launch.py')
    cartographer_slam_path = os.path.join(cartographer_slam_launch_dir, 'launch', 'cartographer.launch.py')



    ld = LaunchDescription()

    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path)
    )

    lidar_merge_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(lidar_merge_path)
    )

    ekf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(ekf_launch_path)
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(navigation_launch_path)
    )
    cartographer_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(cartographer_slam_path)
    )
    tf_node = Node(
        package='navigation', 
        executable='tf_node',
        name='tf_node',
        output='screen'
    )
    robo = TimerAction(
        period=5.0,
        actions=[lidar_merge_launch, ekf_launch, navigation_launch],
    )
    robo_map = TimerAction(
        period=3.0,
        actions=[lidar_merge_launch, ekf_launch],
    )
    tf_node_tm = TimerAction(
        period=6.0,
        actions=[tf_node, LogInfo(msg="ft_done")],
    )

    ld.add_action(robot_launch)
    ld.add_action(robo)
    # ld.add_action(ekf_launch)
    # ld.add_action(navigation_launch)
    ld.add_action(tf_node_tm)
    # ld.add_action(static_tf_launch)
    # ld.add_action(cartographer_launch)


    return ld

    

#this launch file will launch odom, static_tf, lidar, ekf, navigation

from launch import LaunchDescription
# from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    motor_driver_share_dir = get_package_share_directory('motor_drive_leadshine')

    lidar_share_dir = get_package_share_directory('rplidar_ros')

    navigation_launch_dir = get_package_share_directory('navigation')

    cartographer_slam_launch_dir = get_package_share_directory('cartographer_slam')

    odom_launch_path = os.path.join(motor_driver_share_dir, 'launch', 'odom.launch.py')
    static_tf_launch_path = os.path.join(motor_driver_share_dir, 'launch', 'static_tf.launch.py')
    lidar_launch_path = os.path.join(lidar_share_dir, 'launch', 'view_rplidar_a2m12_launch.py')
    ekf_launch_path = os.path.join(navigation_launch_dir, 'launch', 'ekf.launch.py')
    navigation_launch_path = os.path.join(navigation_launch_dir, 'launch', 'navigation.launch.py')
    cartographer_slam_path = os.path.join(cartographer_slam_launch_dir, 'launch', 'cartographer.launch.py')



    ld = LaunchDescription()

    odom_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(odom_launch_path)
    )

    static_tf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(static_tf_launch_path)
    )

    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(lidar_launch_path)
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

    ld.add_action(odom_launch)
    ld.add_action(lidar_launch)
    ld.add_action(ekf_launch)
    ld.add_action(navigation_launch)
    # ld.add_action(static_tf_launch)
    # ld.add_action(cartographer_launch)


    return ld

    

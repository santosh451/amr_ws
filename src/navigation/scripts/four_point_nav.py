#! /usr/bin/env python3

import time # Time library
 
from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def main():
 
  rclpy.init()
 
  navigator = BasicNavigator()
 
  # initial_pose = PoseStamped()
  # initial_pose.header.frame_id = 'map'
  # initial_pose.header.stamp = navigator.get_clock().now().to_msg()
  # initial_pose.pose.position.x = 0.0
  # initial_pose.pose.position.y = 0.0
  # initial_pose.pose.position.z = 0.35
  # initial_pose.pose.orientation.x = 0.0
  # initial_pose.pose.orientation.y = 0.0
  # initial_pose.pose.orientation.z = 0.0
  # initial_pose.pose.orientation.w = 1.0
  # navigator.setInitialPose(initial_pose)
 
  navigator.waitUntilNav2Active()
 
  # If desired, you can change or load the map as well
  # navigator.changeMap('/path/to/map.yaml')
 
  # You may use the navigator to clear or obtain costmaps
  # navigator.clearAllCostmaps()  # also have clearLocalCostmap() and clearGlobalCostmap()
  # global_costmap = navigator.getGlobalCostmap()
  # local_costmap = navigator.getLocalCostmap()
 
  # Set the robot's goal poses
  goal_poses = []
   
  goal_pose = PoseStamped()
  goal_pose.header.frame_id = 'map'
  goal_pose.header.stamp = navigator.get_clock().now().to_msg()
  goal_pose.pose.position.x = -4.5
  goal_pose.pose.position.y = 0.0
  goal_pose.pose.position.z = 0.35
  goal_poses.append(goal_pose)

   
  goal_pose = PoseStamped()
  goal_pose.header.frame_id = 'map'
  goal_pose.header.stamp = navigator.get_clock().now().to_msg()
  goal_pose.pose.position.x = -2.5
  goal_pose.pose.position.y = -1.5
  goal_pose.pose.position.z = 0.35
  goal_poses.append(goal_pose)
   
  goal_pose = PoseStamped()
  goal_pose.header.frame_id = 'map'
  goal_pose.header.stamp = navigator.get_clock().now().to_msg()
  goal_pose.pose.position.x = -1.0
  goal_pose.pose.position.y = -1.0
  goal_pose.pose.position.z = 0.35
  goal_poses.append(goal_pose)

  goal_pose = PoseStamped()
  goal_pose.header.frame_id = 'map'
  goal_pose.header.stamp = navigator.get_clock().now().to_msg()
  goal_pose.pose.position.x = 4.0
  goal_pose.pose.position.y = 0.5
  goal_pose.pose.position.z = 0.35
  goal_poses.append(goal_pose)

  goal_pose = PoseStamped()
  goal_pose.header.frame_id = 'map'
  goal_pose.header.stamp = navigator.get_clock().now().to_msg()
  goal_pose.pose.position.x = 0.0
  goal_pose.pose.position.y = 0.0
  goal_pose.pose.position.z = 0.35
  goal_poses.append(goal_pose)
   
  
  # sanity check a valid path exists
  # path = navigator.getPathThroughPoses(initial_pose, goal_poses)
  j = 1
  while j <= 50:
    nav_start = navigator.get_clock().now()
    navigator.followWaypoints(goal_poses)
    
    i = 0
    while not navigator.isTaskComplete():
        i = i + 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print('Executing current waypoint: ' +
                    str(feedback.current_waypoint + 1) + '/' + str(len(goal_poses)))
            now = navigator.get_clock().now()
    
        # Some navigation timeout to demo cancellation
        now = navigator.get_clock().now()
        if now - nav_start > Duration(seconds=100000000.0):
            navigator.cancelNav()
    
    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')
    j = j+1
 
  # navigator.lifecycleShutdown()
 
  exit(0)
 
if __name__ == '__main__':
  main()
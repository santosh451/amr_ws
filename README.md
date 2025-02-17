## AMR navigation
Custom amr pkg with single and multiple pose navigation using nav2 stack

###

### Step 1:-
Create a pkg folder and clone the repo

### Step 2:-
build the pkg
```
colcon build
```

source the ws
```
source install/setup.bash
```

### Step 3:-
To launch Robot in gazebo, laser merge, ekf, navigation, Rviz2 run:- 
```
ros2 launch navigation bringup.launch.py
```

To run single goal navigation:-
```
ros2 run navigation single_goal
```

To run multi goal navigation:-
```
ros2 run navigation multi_goal
```


### Additional things:-

To launch only robot in gazebo with rviz2:-
```
ros2 launch amr_big_two_description gazebo.launch.py
```

To launch navigation:-
```
ros2 launch navigation navigation.launch.py
```

To launch laser merger:-
``` 
ros2 launch ros2_laser_scan_merger merger_2_scan.launch.py
```

To launch ekf:-
```
ros2 launch navigation ekf.launch.py
```

### Approach:-

Localization :-
First got data from wheel odometry, IMU and using EKF fused that data and got a corrected odometry, that odometry passed through AMCL to get more priciese data by utilizing corrected odometry data and lidar scan data and map of the environment.

Planning :-
There are two path planners local and global path planner, globle path planner plane the path based on the map and the local path planner planes using the globle path and obstricals in the path, while planning size of the robot also plays a crussial role, infletion layer there to give a path which is more secure.

Obstrical avoidance :-
To avoide obstacles I utilized laser scan data nd depth_cam point cloud because only 2D laser scan many time miss obstacles which are not comming in the field of lidar.

Final Laser scan data from merge of two lidars:-
As the robot model is a bigger model to move the boxes, So we will not be able to use single lidar on top of that, due to this I used 2 lidar and merge the data of both the lidar to get the final full field of view. 

Increased inflation layer - This gave us a more smooth path with less sharp corners and less likelyhood to collision because robot will try not to go inside the infletion layer.
Robot foolprint - This inproved robot size so that tha planner will plan accordingly.
Added obstacle_layer - this utilizes depth_cam data to detect obstecles in the path.
Updated velocity smoother for a smooth velocity output.
Changed velocity and acceleration values for smooth and fast movement
Updated AMCL params - max and min particles, update rate to get a more good and fast localization but it came at a cost of computation.



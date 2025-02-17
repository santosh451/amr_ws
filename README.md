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



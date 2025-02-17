cmake_minimum_required(VERSION 3.8)
project(navigation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)

install( DIRECTORY 
  launch
  scripts
  worlds
  config
  map
  DESTINATION share/${PROJECT_NAME})
# install( DIRECTORY scripts/
#          DESTINATION share/${PROJECT_NAME}/scripts)
# install( DIRECTORY worlds/
#          DESTINATION share/${PROJECT_NAME}/worlds)


# install( DIRECTORY config/
#          DESTINATION share/${PROJECT_NAME}/config)
# install( DIRECTORY map/
#          DESTINATION share/${PROJECT_NAME}/map)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# install(PROGRAMS scripts/four_point_nav.py DESTINATION lib/${PROJECT_NAME})

add_executable(tf_node scripts/tf_pub.cpp)
ament_target_dependencies(tf_node 
  rclcpp 
  tf2_ros 
  geometry_msgs
)

add_executable(single_goal scripts/robot_runner_single_goal.cpp)
ament_target_dependencies(single_goal 
  rclcpp 
  rclcpp_action 
  geometry_msgs 
  nav2_msgs
)

add_executable(multi_goal scripts/robot_runner.cpp)
ament_target_dependencies(multi_goal 
  rclcpp 
  rclcpp_action 
  geometry_msgs 
  nav2_msgs
)

install(TARGETS 
  tf_node
  single_goal
  multi_goal
  DESTINATION lib/${PROJECT_NAME})
# install(TARGETS robo_navi DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

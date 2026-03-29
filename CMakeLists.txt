cmake_minimum_required(VERSION 3.0.2)
project(proximity_sensors)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  proximity_sensors/sensor_node.py
  proximity_sensors/filter_node.py
  proximity_sensors/watchdog_node.py
  proximity_sensors/velocity_controller.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
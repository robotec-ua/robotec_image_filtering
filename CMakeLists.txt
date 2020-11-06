cmake_minimum_required(VERSION 2.8.3)
project(robotec_image_filtering)

#
find_package(catkin REQUIRED COMPONENTS std_msgs sensor_msgs message_generation)

#
catkin_python_setup()


#
catkin_package(CATKIN_DEPENDS message_runtime)

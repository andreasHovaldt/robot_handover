# CMake generated Testfile for 
# Source directory: /home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/moveit/moveit_ros/robot_interaction
# Build directory: /home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_ros_robot_interaction
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_moveit_ros_robot_interaction_gtest_locked_robot_state_test "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_ros_robot_interaction/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_ros_robot_interaction/test_results/moveit_ros_robot_interaction/gtest-locked_robot_state_test.xml" "--return-code" "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/devel/.private/moveit_ros_robot_interaction/lib/moveit_ros_robot_interaction/locked_robot_state_test --gtest_output=xml:/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_ros_robot_interaction/test_results/moveit_ros_robot_interaction/gtest-locked_robot_state_test.xml")
set_tests_properties(_ctest_moveit_ros_robot_interaction_gtest_locked_robot_state_test PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;98;catkin_run_tests_target;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;37;_catkin_add_google_test;/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/moveit/moveit_ros/robot_interaction/CMakeLists.txt;46;catkin_add_gtest;/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/moveit/moveit_ros/robot_interaction/CMakeLists.txt;0;")
subdirs("gtest")

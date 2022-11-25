# CMake generated Testfile for 
# Source directory: /home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/Universal_Robots_ROS_Driver/ur_robot_driver
# Build directory: /home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/ur_robot_driver
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_ur_robot_driver_rostest_test_driver.test "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/ur_robot_driver/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/ur_robot_driver/test_results/ur_robot_driver/rostest-test_driver.xml" "--return-code" "/usr/bin/python3 /opt/ros/noetic/share/rostest/cmake/../../../bin/rostest --pkgdir=/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/Universal_Robots_ROS_Driver/ur_robot_driver --package=ur_robot_driver --results-filename test_driver.xml --results-base-dir \"/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/ur_robot_driver/test_results\" /home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/Universal_Robots_ROS_Driver/ur_robot_driver/test/driver.test ")
set_tests_properties(_ctest_ur_robot_driver_rostest_test_driver.test PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/rostest/cmake/rostest-extras.cmake;52;catkin_run_tests_target;/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/Universal_Robots_ROS_Driver/ur_robot_driver/CMakeLists.txt;118;add_rostest;/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/Universal_Robots_ROS_Driver/ur_robot_driver/CMakeLists.txt;0;")
subdirs("gtest")

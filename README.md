# robot_handover
3. semester project for robot-to-human handovers, using a UR10 robotic manipulator and a Kinect for Windows V2 camera




# Dependencies:
- Numpy (https://pypi.org/project/numpy/)
- OpenCV (https://pypi.org/project/opencv-python/)
- Wheel (https://pypi.org/project/wheel/)
- libfreenect2 (https://github.com/OpenKinect/libfreenect2/)
- scikit-learn (https://github.com/scikit-learn/scikit-learn)
- scikit-image (https://github.com/scikit-image/scikit-image)

Install python wrapper for libfreenect2 (https://rjw57.github.io/freenect2-python/):
- https://www.notaboutmy.life/posts/run-kinect-2-on-ubuntu-20-lts/
  * sudo apt install pcl-tools -y
  * PKG_CONFIG_PATH=$HOME/freenect2/lib/pkgconfig pip install freenect2
- https://github.com/rjw57/freenect2-python/issues/6
  * sudo ln -s $HOME/freenect2/lib/libfreenect2.so.0.2 /usr/lib/libfreenect2.so.0.2




# How to use the program

1. Open the shell file called connect_to_ur.sh and follow the instructions.

    This will open the ROS master, UR10 driver, and MoveIt execution planner.

2. Open the move_ur.py script as a node: "rosrun robot_handover move_ur.py"

    This will open the python interface for move group.

3. Open the locate_hand_no_background_kinect.py script that sends hand coordinates to the python interface script: "rosrun robot_handover locate_hand_no_background_kinect.py"

    Make sure that the calibration marker and Kinect camera is placed as described in the report.

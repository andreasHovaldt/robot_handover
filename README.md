# robot_handover
School project for robot-to-human handovers, using a UR10 robotic manipulator and a Kinect for Windows V2 camera :)


Dependencies:
- Numpy (https://pypi.org/project/numpy/)
- OpenCV (https://pypi.org/project/opencv-python/)
- Wheel (https://pypi.org/project/wheel/)
- libfreenect2 (https://github.com/OpenKinect/libfreenect2/)

Maybe:
- Cython (https://pypi.org/project/Cython/)
- Matplotlib (https://pypi.org/project/matplotlib/)

Install python wrapper for libfreenect2 (https://rjw57.github.io/freenect2-python/):
- https://www.notaboutmy.life/posts/run-kinect-2-on-ubuntu-20-lts/
  * sudo apt install pcl-tools -y
  * PKG_CONFIG_PATH=$HOME/freenect2/lib/pkgconfig pip install freenect2
- https://github.com/rjw57/freenect2-python/issues/6
  * sudo ln -s $HOME/freenect2/lib/libfreenect2.so.0.2 /usr/lib/libfreenect2.so.0.2



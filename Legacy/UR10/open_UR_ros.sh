#! /usr/bin/bash

# The file will open the relevant node for the UR10

read -p "Enter path for catkin_ws/build: " path

if [$path -eq ''] 
then
 path='$HOME/UNI/P3/catkin_ws/build/'
fi

gnome-terminal --working-directory=${path} -- roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=172.31.1.115 kinematics_config:=${path}../../my_robot_calibration.yaml

#gnome-terminal --working-directory=${path} -- echo "test"



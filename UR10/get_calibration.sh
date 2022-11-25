#! /usr/bin/bash


# This script downloads te calibration file from a connected UR
# The specified ip is the ip for the UR10 at AAU Create


read -p "Enter path for catkin_ws/build: " path

if [$path -eq ''] 
then
 path='$HOME/UNI/P3/robot_handover/p3_ws/build'
fi


source $path/../devel/setup.bash

roslaunch ur_calibration calibration_correction.launch robot_ip:=172.31.1.115 target_filename:="${path}/../../my_robot_calibration.yaml"

echo "Calibration file saved at: ${path}/../../my_robot_calibration.yaml"

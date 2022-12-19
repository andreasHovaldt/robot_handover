#! /usr/bin/bash

# The file will open the relevant node for the UR10

path_to_ws_build=$HOME/robot_handover_ros/build/

robot_ip=172.31.1.115

config_path=${path_to_ws_build}../../my_robot_calibration.yaml

gnome-terminal --working-directory=${path_to_ws_build} -- roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=${robot_ip} #kinematics_config:=${config_path}

#Uncomment previous line if a config file exists

read -p 'Press "Enter" key when UR-Driver has started'


gnome-terminal -- roslaunch ur10_moveit_config moveit_planning_execution.launch

sleep 3

gnome-terminal -- rosrun robot_handover move_ur.py # Ændre den her hvis move_ur.py hedder noget andet

read -p 'Press "Enter" key to start the camera script'

gnome-terminal --working-directory=~/ -- rosrun robot_handover locate_hand_no_background_kinect.py  # Ændre også den her hvis filen hedder noget andet



#! /usr/bin/bash

# The file will open the relevant node for the UR10

read -p "Enter path for catkin_ws/build: " path

if [$path -eq ''] 
then
 path='$HOME/UNI/P3/robot_handover/UR10/p3_ws/build'
fi

gnome-terminal --working-directory=${path} -- roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=172.31.1.115 #kinematics_config:=${path}/../../my_robot_calibration.yaml


echo "Wait for terminal to prompt: 'Ready to receive control commands' then press any key to continue"
while [ true ] ; do
read -t 10 -n 1
if [ $? = 0 ] ; then
break ;
else
echo "waiting for the keypress"
fi
done

sleep 0.5

gnome-terminal --working-directory=${path} -- roslaunch ur10_moveit_config moveit_planning_execution.launch

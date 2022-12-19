#! /usr/bin/bash

# The file will open the relevant node for the UR10

path_to_ws_build=$HOME/UNI/P3/catkin_ws/build/


gnome-terminal --working-directory=${path_to_ws_build} -- roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=172.31.1.115 kinematics_config:=${path_to_ws_build}../../my_robot_calibration.yaml

echo "Press any key when UR-Driver has started"
while [ true ] ; do
read -t 5 -n 1
if [ $? = 0 ] ; then
exit ;
else
echo "Waiting for the keypress"
fi
done

gnome-terminal --working-directory=~/ -- roslaunch ur10_moveit_config moveit_planning_execution.launch

sleep 3

gnome-terminal --working-directory=~/ -- rosrun robot_handover move_ur.py # Ændre den her hvis move_ur.py hedder noget andet

echo "Press any key to start the camera script"
while [ true ] ; do
read -t 5 -n 1
if [ $? = 0 ] ; then
exit ;
else
echo "Waiting for the keypress"
fi
done

gnome-terminal --working-directory=~/ -- rosrun robot_handover locate_hand_no_background_kinect.py  # Ændre også den her hvis filen hedder noget andet
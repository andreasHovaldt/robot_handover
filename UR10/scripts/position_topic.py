#!/usr/bin/env python3
import rospy
from robot_handover.msg import position

rospy.init_node('position_topic')
my_pub = rospy.Publisher('positioning',position,queue_size= 10)

position_msg = position()
position_msg.pos_x = 0.3
position_msg.pos_y = 0.4
position_msg.pos_z = 1

position_msg.rot_w= 1
position_msg.rot_x= 0
position_msg.rot_y= 0
position_msg.rot_z= 0



rate = rospy.Rate(5)

while not rospy.is_shutdown():
    position_msg.pos_x = float(input("Enter 'x' position: "))
    position_msg.pos_y = float(input("Enter 'y' position: "))
    position_msg.pos_z = float(input("Enter 'z' position: "))
    # position_msg.rot_w = float(input("Enter 'w' position..."))
    # position_msg.rot_x = float(input("Enter 'x' position..."))
    # position_msg.rot_y = float(input("Enter 'y' position..."))
    # position_msg.rot_z = float(input("Enter 'z' position..."))
    
    print("Positions sent!")
    
    
    my_pub.publish(position_msg)
    rate.sleep()
    # position_msg.pos_x += 0.008
    # position_msg.pos_y += 0.006
    # position_msg.pos_z -= 0.005

    # position_msg.rot_w= 0
    # position_msg.rot_x= 0
    # position_msg.rot_y= 1
    # position_msg.rot_z= 0
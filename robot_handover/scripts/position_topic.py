#!/usr/bin/env python3
import rospy
from robot_handover.msg import Num
from math import pi

rospy.init_node('new_topic')
my_pub = rospy.Publisher('positioning',Num,queue_size= 100)

position_msg = Num()
position_msg.pos_x = 0.8
position_msg.pos_y = 0
position_msg.pos_z = 0.5

position_msg.rot_w= 0
position_msg.rot_x= 1
position_msg.rot_y= 0
position_msg.rot_z= 0



rate = rospy.Rate(100)

while not rospy.is_shutdown():
    my_pub.publish(position_msg)
    rate.sleep()
    position_msg.pos_x = 0.8
    position_msg.pos_y = 0.3
    position_msg.pos_z = 0.3

    position_msg.rot_w= 0
    position_msg.rot_x= pi/2
    position_msg.rot_y= 0
    position_msg.rot_z= pi/2+pi/4
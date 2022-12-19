#!/usr/bin/env python3
import rospy
from robot_handover.msg import joint_angles
from math import tau

rospy.init_node('joint_topic')
my_pub = rospy.Publisher('joint_angles',joint_angles,queue_size= 10,latch=True)

joint_angles_msg = joint_angles()
joint_angles_msg.jnt1 = 0
joint_angles_msg.jnt2 = 0
joint_angles_msg.jnt3 = 0
joint_angles_msg.jnt4 = 0
joint_angles_msg.jnt5 = 0
joint_angles_msg.jnt6 = 0


rate = rospy.Rate(100)
direction_scalar = 1

# Run once
if not rospy.is_shutdown():
    my_pub.publish(joint_angles_msg)
    rate.sleep()
    input("Press `Enter` to begin updating joints...")
    print("Running transmission...")

while not rospy.is_shutdown():
    my_pub.publish(joint_angles_msg)
    rate.sleep()
    
    if joint_angles_msg.jnt1 >= tau:
        direction_scalar = -1
    elif joint_angles_msg.jnt1 <= -tau:
        direction_scalar = 1
    
    joint_angles_msg.jnt1 += 0.001 * direction_scalar
    joint_angles_msg.jnt2 += 0.0005 * direction_scalar
    joint_angles_msg.jnt3 += 0.0004 * direction_scalar
    joint_angles_msg.jnt4 += 0.0002 * direction_scalar
    joint_angles_msg.jnt5 += 0.0002 * direction_scalar
    joint_angles_msg.jnt6 += 0.0002 * direction_scalar
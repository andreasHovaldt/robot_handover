#!/usr/bin/env python3

#first import our dependencies (some of these might be redundant)
import sys
import copy
import rospy
import moveit_commander
import time

#import the used messages (these might be redundant)
import moveit_msgs.msg
import geometry_msgs.msg
#from geometry_msgs.msg import PoseStamped

rospy.init_node('scene_test', anonymous=True)


scene = moveit_commander.PlanningSceneInterface()
robot = moveit_commander.RobotCommander()

p = geometry_msgs.msg.PoseStamped()

p.header.frame_id = robot.get_planning_frame()

p.pose.position.x = 0
p.pose.position.y = 0
p.pose.position.z = 0
scene.add_box('table',p, (0.5,1.5,0.6))



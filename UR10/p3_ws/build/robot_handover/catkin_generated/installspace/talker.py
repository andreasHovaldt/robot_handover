#!/usr/bin/env python3
# license removed for brevity
import rospy
from robot_handover.msg import position


def talker():
   pub = rospy.Publisher('positioning', position, queue_size=1)
   rospy.init_node('coordinate_sender', anonymous=True)
#    rate = rospy.Rate(111) # 111hz

   while not rospy.is_shutdown():

    pos_x = float(input('Enter the x-position: '))
    pos_y = float(input('Enter the y-position: '))
    pos_z = float(input('Enter the z-position: '))

    rot_x = float(input('Enter the x-rotation: '))
    rot_y = float(input('Enter the y-rotation: '))
    rot_z = float(input('Enter the z-rotation: '))
    rot_w = float(input('Enter the w-rotation_scalar: '))
    
    print("Position and orientation sent! \n")

    
    
    position_msg = position()
    position_msg.pos_x = pos_x
    position_msg.pos_y = pos_y
    position_msg.pos_z = pos_z
    position_msg.rot_x = rot_x
    position_msg.rot_y = rot_y
    position_msg.rot_z = rot_z
    position_msg.rot_w = rot_w

    pub.publish(position_msg)




if __name__ == '__main__':
   try:
       talker()
   except rospy.ROSInterruptException:
       pass

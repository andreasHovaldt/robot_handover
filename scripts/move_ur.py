#!/usr/bin/env python3


import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi, tau, dist, fabs, cos
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from robot_handover.msg import Num
import time
import random




def all_close(goal, actual, tolerance):
    """
    Convenience method for testing if the values in two lists are within a tolerance of each other.
    For Pose and PoseStamped inputs, the angle between the two quaternions is compared (the angle
    between the identical orientations q and -q is calculated correctly).
    @param: goal       A list of floats, a Pose or a PoseStamped
    @param: actual     A list of floats, a Pose or a PoseStamped
    @param: tolerance  A float
    @returns: bool
    """
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
        x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
        # Euclidean distance
        d = dist((x1, y1, z1), (x0, y0, z0))
        # phi = angle between orientations
        cos_phi_half = fabs(qx0 * qx1 + qy0 * qy1 + qz0 * qz1 + qw0 * qw1)
        return d <= tolerance and cos_phi_half >= cos(tolerance / 2.0)

    return True


class UR_python_interface():
    def __init__(self):
        ## BEGIN_SUB_TUTORIAL setup
        ##
        # First initialize `moveit_commander`_ and a `rospy`_ node:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python_interface", anonymous=True)

        # Instantiate a `RobotCommander`_ object. Provides information such as the robot's
        # kinematic model and the robot's current joint states
        robot = moveit_commander.RobotCommander()

        # Instantiate a `PlanningSceneInterface`_ object.  This provides a remote interface
        # for getting, setting, and updating the robot's internal understanding of the
        # surrounding world:
        scene = moveit_commander.PlanningSceneInterface()

        # Add surrounding environment

        # scene.add_box('Table', (0.67, 1.05, 0.03), (1.22, 2.10, 0.05))
        # scene.add_plane('Wall', (3, 0, 0))

        # Instantiate a `MoveGroupCommander`_ object.  This object is an interface
        # to a planning group (group of joints). The group name is based on information from ur10
        # if the manipulator is launched in rviz the group_name can be seen to be "manipulator"
        group_name = "manipulator"
        move_group = moveit_commander.MoveGroupCommander(group_name)

        # Create a `DisplayTrajectory`_ ROS publisher which is used to display
        # trajectories in Rviz:
        display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )


        # END_SUB_TUTORIAL

        # BEGIN_SUB_TUTORIAL basic_info
        ##
        # Getting Basic Information
        # ^^^^^^^^^^^^^^^^^^^^^^^^^
        # We can get the name of the reference frame for this robot:
        planning_frame = move_group.get_planning_frame()
        print("============ Planning frame: %s" % planning_frame)

        # We can also print the name of the end-effector link for this group:
        eef_link = move_group.get_end_effector_link()
        print("============ End effector link: %s" % eef_link)

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print("============ Available Planning Groups:", robot.get_group_names())

        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print("============ Printing robot state")
        print(robot.get_current_state())
        print("")
        # END_SUB_TUTORIAL

        # Misc variables
        self.box_name = ""
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names
        self.rot_w = 1
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0
        self.pos_x = -0.8
        self.pos_y = 0.02
        self.pos_z = 0.4

        self.add_obstacles()
                
    def add_obstacles(self):
        table = geometry_msgs.msg.PoseStamped()

        table.header.frame_id = self.robot.get_planning_frame()

        table.pose.position.x = 1.03
        table.pose.position.y = -0.08
        table.pose.position.z = -0.06

        table.pose.orientation.x = 0
        table.pose.orientation.y = 0    
        table.pose.orientation.z = 0.48717
        table.pose.orientation.w = 0.873305

        wall = geometry_msgs.msg.PoseStamped()

        wall.header.frame_id = self.robot.get_planning_frame()

        wall.pose.position.x = -0.5
        wall.pose.position.y = 0
        wall.pose.position.z = 0

        wall.pose.orientation.x = 0
        wall.pose.orientation.y = 0    
        wall.pose.orientation.z = 0.48717
        wall.pose.orientation.w = 0.873305

        self.scene.add_box('table',table, (1.72,2.60,0.05))
        self.scene.add_box('wall', wall, (0.06, 7, 7))



   

    def go_to_pose_goal(self):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        move_group = self.move_group

        ## BEGIN_SUB_TUTORIAL plan_to_pose
        ##
        ## Planning to a Pose Goal
        ## ^^^^^^^^^^^^^^^^^^^^^^^
        ## We can plan a motion for this group to a desired pose for the
        ## end-effector:
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = self.rot_w
        pose_goal.orientation.x = self.rot_x
        pose_goal.orientation.y = self.rot_y
        pose_goal.orientation.z = self.rot_z
        pose_goal.position.x = -self.pos_x
        pose_goal.position.y = -self.pos_y
        pose_goal.position.z = self.pos_z

        position_orientation = [self.pos_x, self.pos_y-random.randint(-50,50)/100, self.pos_z+random.randint(-50,50)/100,self.rot_x ,self.rot_y,  self.rot_z]

        print(position_orientation)

        #following function sets 
        move_group.set_pose_target(position_orientation)

        ## Now, we call the planner to compute the plan and execute it.
        # `go()` returns a boolean indicating whether the planning and execution was successful.
        current_pose = self.move_group.get_current_pose().pose
        if (not all_close(pose_goal, current_pose, 0.01)):
            success = move_group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
        move_group.stop()
        # It is always good to clear your targets after planning with poses.
        # Note: there is no equivalent function for clear_joint_value_targets().
        move_group.clear_pose_targets()

        ## END_SUB_TUTORIAL

        # For testing:
        # Note that since this section of code will not be included in the tutorials
        # we use the class variable rather than the copied state variable
        current_pose = self.move_group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

  
    def position_callback(self, msg):
        self.pos_x = msg.pos_x
        self.pos_y = msg.pos_y
        self.pos_z = msg.pos_z

        self.rot_x = msg.rot_x
        self.rot_y = msg.rot_y
        self.rot_z = msg.rot_z
        self.rot_w = msg.rot_w


def main():
    try:
        
        robot_UI = UR_python_interface()


        while not rospy.is_shutdown():
            
            
            try:
                rot_x_now = robot_UI.rot_x
                rot_y_now = robot_UI.rot_y
                rot_z_now = robot_UI.rot_z
                rot_w_now = robot_UI.rot_w

                rospy.Subscriber('positioning', Num, callback=robot_UI.position_callback)
                state = robot_UI.robot.get_current_state().joint_state.position

                #if ((state[0] != robot_UI.pos_x and state[1] != robot_UI.pos_y and state[2] != robot_UI.pos_z) or (rot_w_now != robot_UI.rot_w and rot_x_now != robot_UI.rot_x and rot_y_now != robot_UI.rot_y and rot_z_now != robot_UI.rot_z)):
                robot_UI.go_to_pose_goal()
            

            except rospy.ROSInterruptException:
                return
            except KeyboardInterrupt:
                return
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
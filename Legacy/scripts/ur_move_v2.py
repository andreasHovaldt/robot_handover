#!/usr/bin/env python3

import time
import sys
import rospy
import moveit_commander

import moveit_msgs.msg
import geometry_msgs.msg

from robot_handover.msg import Num

from moveit_commander.conversions import pose_to_list


try:
    from math import pi, tau, dist, fabs, cos
except:  # For Python 2 compatibility
    from math import pi, fabs, cos, sqrt

    tau = 2.0 * pi

    def dist(p, q):
        return sqrt(sum((p_i - q_i) ** 2.0 for p_i, q_i in zip(p, q)))




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
        return all_close(goal.pose, actual.poseSubsc, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
        x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
        # Euclidean distance
        d = dist((x1, y1, z1), (x0, y0, z0))
        # phi = angle between orientations
        cos_phi_half = fabs(qx0 * qx1 + qy0 * qy1 + qz0 * qz1 + qw0 * qw1)
        return d <= tolerance and cos_phi_half >= cos(tolerance / 2.0)

    return True







class robot_controller():
    def __init__(self):
        # Initialize moveit commander, used for controlling the robot
        moveit_commander.roscpp_initialize(sys.argv)
        
        #following line initiates the ros node making it possible to inject this code with data from the camera
        rospy.init_node("ur_move.py", anonymous=True)
        
        # Instantiate robot controller, provides kinematic model and current joint states
        robot = moveit_commander.RobotCommander()
        
        # Instantiate world for robot
        scene = moveit_commander.PlanningSceneInterface()
        
        # Group of joints
        # This interface can be used to plan and execute motions
        group_name = "manipulator"
        move_group = moveit_commander.MoveGroupCommander(group_name)
        
        # Create "DisplayTrajectory" node, Used to display trajectory in RViz
        display_trajectory_publisher = rospy.Publisher(
            "move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20
        ) 
        
        



        
        
        # Define variables for robot
        planning_frame = move_group.get_planning_frame()
        eef_link = move_group.get_end_effector_link()
        group_names = robot.get_group_names()
        
        self.box_name = ""
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names
        
        # Position variables
        self.pos_x = robot.get_current_state().joint_state.position[0]
        self.pos_y = robot.get_current_state().joint_state.position[1]
        self.pos_z = robot.get_current_state().joint_state.position[2]
        self.rot_w = 1
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0
        
        # Joint variables
        self.jnts = move_group.get_current_joint_values()
        
        
    def add_obstacles(self):
        p = geometry_msgs.msg.PoseStamped()

        p.header.frame_id = self.robot.get_planning_frame()

        p.pose.position.x = -1.03
        p.pose.position.y = 0.08
        p.pose.position.z = -0.06

        p.pose.orientation.x = 0
        p.pose.orientation.y = 0    
        p.pose.orientation.z = 0.48717
        p.pose.orientation.w = 0.873305


        
        self.scene.add_box('table',p, (1.72,2.60,0.05))
    
    # Go to x,y,z
    def go_to_pose_goal(self):
        move_group = self.move_group
        
        pose_goal = geometry_msgs.msg.Pose()

        # pose_goal.position.x = self.pos_x
        # pose_goal.position.y = self.pos_y
        # pose_goal.position.z = self.pos_z
        
        # pose_goal.orientation.w = self.rot_w
        # pose_goal.orientation.x = self.rot_x
        # pose_goal.orientation.y = self.rot_y
        # pose_goal.orientation.z = self.rot_z
        
        position_orientation = [self.pos_x, self.pos_y, self.pos_z, self.rot_x, self.rot_y,  self.rot_z]

        
        #ret tilbage til pose_goal
        move_group.set_pose_target(position_orientation)
        
        # Moves robot and checks whether the planning and execution was successful
        success = move_group.go(wait=True)
        
        # Apparently it is good practice to clear targets after planning with poses
        move_group.clear_pose_targets()
        
        # Define current pose of robot
        current_pose = self.move_group.get_current_pose().pose
        
        return all_close(pose_goal,current_pose,0.01)
    
    
    def go_to_joint_state(self):
        move_group = self.move_group
        
        # Define joint pose goal
        joint_goal = self.jnts
        
        # Set joint targets for robot to move to
        #move_group.set_joint_target(joint_goal)
        
        # Move robot and save whether planning and executions was succesful or not to a variable
        success = move_group.go(joint_goal,wait=True)
        
        # Get current joint states
        current_joints = move_group.get_current_joint_values()
        
        return all_close(joint_goal,current_joints,0.01)
    
        
        
    
    # Function used to update position from message
    def position_callback(self, msg):
        self.pos_x = msg.pos_x
        self.pos_y = msg.pos_y
        self.pos_z = msg.pos_z
        
        self.rot_w = msg.rot_w
        self.rot_x = msg.rot_x
        self.rot_y = msg.rot_y
        self.rot_z = msg.rot_z
        
        # print(self.pos_x)
        # print(self.pos_y)
        # print(self.pos_z)
        # print(self.rot_x)
        # print(self.rot_y)
        # print(self.rot_x)
        # print(self.rot_w)




  


def main():
    robot_control = robot_controller()
    robot_control.add_obstacles()
    while not rospy.is_shutdown():
        try:
            
            rospy.Subscriber("positioning",Num,callback=robot_control.position_callback)
            robot_control.go_to_pose_goal()
            
            #time.sleep(0.5)
            
        except rospy.ROSInterruptException:
                return
        
        except KeyboardInterrupt:
                return


if __name__ == "__main__":
    main()
        
        
        
        
        












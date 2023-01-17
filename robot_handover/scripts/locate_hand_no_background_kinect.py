#!/usr/bin/env python3
#To be able to run this program, make sure your laptop is powered in, as a low performance laptop will not be able to run the program.
#If segmantation error core dump appears, try running the program again
#If crash, make sure to read the KU-matrix to check if the pink dot was found.
#X,Y position from UR to Hand can be a bit off, if the base is shifted a bit - can be fixed by rerunning camera, or finding out where base is located.

import freenect2 as fn2
import numpy as np
import cv2
from detect_hand_as_blob import gloveDetector, create_hand_detector
from calibration_vector import calibrate_camera
import depth_video
import color_video
from math import pi

from sklearn.neighbors import KNeighborsClassifier


HIGHFRAMERATE = 6 #Used to make a high framerate once calibration is finished - 6 is high value, can make higher val for slower program
LOWFRAMERATE = 30 #Used to make a low framerate to make sure program doesn't crash during calibration.
i = 0
framerate = LOWFRAMERATE #Start off with low framerate
device = fn2.Device()
 
#Setting some values to False such that the calibration will run
color_exist = False
depth_exist = False
calibration_exist = False
calibration_vector = None 
static_background = None
static_color_background = None 

#--------------------ROS publisher------------------#
import rospy
from robot_handover.msg import position

#we initiate the topic we wish to publish to
rospy.init_node('new_topic')

#we create the publisher object
my_pub = rospy.Publisher('positioning',position,queue_size= 0)

position_msg = position()

#the following message ensures that the robot starts in its initial position
position_msg.rot_x= pi/2
position_msg.rot_y= 0
position_msg.rot_z= pi/2+pi/4

rate = rospy.Rate(5)



#-------------------- Thresholding --------------------#
def get_hsv_data(img):  #Function to obtain hsv-data from an image.
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]


glove_img = cv2.imread("/home/andreas/robot_handover_ros/src/robot_handover/Mats/glove_color_v2.jpg")
glove_hsv = get_hsv_data(glove_img)
hs = np.array(glove_hsv)*1.2 #Define a scalar to help with thresholding
ls = np.array(glove_hsv)*0.8 #Define a scalar to help with thresholding

dilate_kernel=np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]], np.uint8) #Kernel used for dilation
erode_kernel = np.ones((3,3), np.uint8) #Kernel used for erosion


#load pose hog dataset 
print("loading pose data...")
hog_pose_data = np.loadtxt("/home/andreas/robot_handover_ros/src/robot_handover/scripts/hog_pose_data.txt")

x_train = hog_pose_data[:,0:hog_pose_data.shape[1]-1]
y_train = hog_pose_data[:,hog_pose_data.shape[1]-1]
pose_classifier = KNeighborsClassifier(n_neighbors=2, metric="euclidean", algorithm="ball_tree")
pose_classifier.fit(x_train,y_train)

hand_detector = create_hand_detector()
#-------------------- Loop --------------------#

image_counter = 0
with(device.running()): #This is the loop that runs
    device.start()
    
    for type_, frame in device: #The KinevtV2 returns both the Color frametype and the Depth frametype, so we have to seperate these
        
        #get the color frame and pre-process  
        if type_ is fn2.FrameType.Color:
            #print("color")
            currentFrame = frame #Frame is what the camera returns
            color_image = currentFrame.to_array() #We convert the frame into an array to change the datatype, and can now easily show the frame                
            color_image = color_image[:,:,0:3]
            color_exist = True 
        
        #get the depth frame and pre-process 
        if type_ is fn2.FrameType.Depth: #This is the depth loop
            #print("depth")
            currentFrame_depth = frame #Frame is what the camera return
            depth_image = currentFrame_depth.to_array() #Convert frame to an array to change datatype, can now easily show frames
            depth_image = np.array(depth_image,np.uint16).reshape((424,512,1)) #needed shape for depth_video.py 
            depth_point_array = device.registration.get_points_xyz_array(currentFrame_depth)#creates the point cloud 
            depth_exist = True
            

        #calibrate the kinect    
        if color_exist and depth_exist and calibration_exist != True and (i % 20 == 0): #On startup, these are false so enter this loop
            framerate = LOWFRAMERATE #Set lowframerate for calibration - Helps to make sure program doesn't crash
            print("trying to calibrate")
            calibration_result = calibrate_camera(color_image, depth_point_array,hand_detector) #Obtain transformationmatrix from the Kinect to the UR
            
            if calibration_result[2]: #if the calibration is succsesfull 
                KU_transformation_matrix = calibration_result[0]
                base_coor = calibration_result[1] #the coordinats of the base 
                calibration_exist = True
                static_background = depth_video.create_static_backgound(depth_image) #create static background 
                static_color_background = color_video.map_rgb_to_depth_size(color_image) #create static color bacground (scaled to fit depth image)
                print("test ")
                cv2.imshow("static color background", static_color_background)
                print(f"This is KU:  \n  {KU_transformation_matrix}")
            else: 
                print("calibration error")
                color_exist = False
                depth_exist = False
        
        if calibration_exist and (i % 20 == 0): 
            print(f"looking for human {i}")
            only_human = depth_video.only_human(static_background,depth_image)
            
            if only_human[0]: #if human detecetd 
                print("human found")
                hog_data = depth_video.extract_HOG(only_human[1])
                hog_pred = pose_classifier.predict(np.array([hog_data]))

                print(f"pose {hog_pred}")

                scaled_color_image = color_video.map_rgb_to_depth_size(color_image[:,:,0:3]) #the color image is scaled to fit the depth image 
                #(1 = one hand, 2= no hands, 4 = two hands)
                scaled_color_image_no_bg = color_video.background_subtraction(static_color_background, scaled_color_image) #the background is removed from the color background 

                #cv2.imshow("color bg subtraction", scaled_color_image_no_bg) 

                #using the depth image with only the human to remove the background on the color image 
                only_human8bit = cv2.cvtColor(depth_video.conv2_8bit(only_human[1]), cv2.COLOR_GRAY2BGR) 
                only_human_mask = only_human8bit > 15
                only_human_color=np.zeros_like(scaled_color_image)
                only_human_color[only_human_mask]=scaled_color_image[only_human_mask]
                
                hsv_img = cv2.cvtColor(only_human_color,cv2.COLOR_BGR2HSV)
                only_glove_binary = cv2.inRange(hsv_img,(ls[0]*0.7,ls[1]*0.7,ls[2]*0.6),(hs[0]*1.3,hs[1]*1.3,hs[2]*1.4)) #Lower / Make these values higher to make more or less sensitive glove - Returns binary image, where the color that overlaps with the glove is shown as white
                cv2.imshow("only glove 1", only_glove_binary)
                #erode and dilate the glove to remove noise 
                for n in range(1):
                    only_glove_binary = cv2.erode(only_glove_binary,erode_kernel) 
                for n in range(5):
                    only_glove_binary = cv2.dilate(only_glove_binary,dilate_kernel)
                cv2.imshow("only glove 2", only_glove_binary)
                keypoints = gloveDetector(only_glove_binary,hand_detector) #Use gloveDetector function to obtain the keypoints where the glove is detected
                
                pts = cv2.KeyPoint.convert(keypoints) #Simple opencv function that lets us access the location of the keypoints
                print(f"pts {pts}")
                if len(pts) > 0: #remove this try except later
                    for n in range(len(pts)): #This loop attempts to draw a red circle around each of the detected keypoints
                        scaled_color_image = cv2.circle(scaled_color_image,(int(keypoints[n].pt[0]),int(keypoints[n].pt[1])),10,(0,0,255),4)
                else:
                    print("no glove")
                cv2.imshow("only human color", only_human_color)
                cv2.imshow("Video", scaled_color_image)
                
                try:
                    for n in range(len(pts)): #Map keypoints from RGB to depth
                        depth_Y = int(keypoints[n].pt[1])
                        depth_X = int(keypoints[n].pt[0])
                        cv2.circle(depth_image,(depth_X,depth_Y),5,(0,0,0),4) #Draw circle on depth'
                    
                        #Create the vector to the hand in the kinect coordinate system
                        kinect_to_hand_vector = np.append(np.round(depth_point_array[depth_Y,depth_X,:],3),[1])
                        
                        #Using the transformation matrix found in the calibration the vector is found represnted in the UR coordinate system 
                        ur_to_hand_vector = np.dot(np.linalg.inv(KU_transformation_matrix), kinect_to_hand_vector)
                        
                        #translation_vector = np.round(depth_array[depth_Y,depth_X,:],3)
                        #translation_vector = np.append(translation_vector, [1])
                        
                        print(f"Kinect to hand vector {kinect_to_hand_vector} \n UR to hand vector in ur coor {ur_to_hand_vector} ")


                        #following lines publish the  x,y,z found using the kinect to the 'positioning' topic which the move script
                        #subscribes from 

                        if hog_pred == 1:
                            position_msg.pos_x = -0.8
                            position_msg.pos_y = 0
                            position_msg.pos_z = 0.5
                        else:
                            position_msg.pos_x = ur_to_hand_vector[0]
                            position_msg.pos_y = ur_to_hand_vector[1]
                            position_msg.pos_z = ur_to_hand_vector[2]
                        
                    
                        my_pub.publish(position_msg)
                except:
                    print("error")
                    #continue
                
                
        i += 1

        K = cv2.waitKey(1)
        if K == 113: #Press Q to close program
            break


cv2.destroyAllWindows()
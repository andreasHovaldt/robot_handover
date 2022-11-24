#To be able to run this program, make sure your laptop is powered in, as a low performance laptop will not be able to run the program.
#If segmantation error core dump appears, try running the program again
#If crash, make sure to read the KU-matrix to check if the pink dot was found.
#X,Y position from UR to Hand can be a bit off, if the base is shifted a bit - can be fixed by rerunning camera, or finding out where base is located.

import freenect2 as fn2
import numpy as np
import cv2
from detect_hand_as_blob import gloveDetector
from calibration_vector import calibrate_camera
import depth_video


HIGHFRAMERATE = 6 #Used to make a high framerate once calibration is finished
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


#-------------------- Thresholding --------------------#
def get_hsv_data(img):  #Function to obtain hsv-data from an image.
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]


glove_img = cv2.imread("Mats/cameraTest/Kinect V2/glove_color_v2.jpg")
glove_hsv = get_hsv_data(glove_img)
hs = np.array(glove_hsv)*1.2 #Define a scalar to help with thresholding
ls = np.array(glove_hsv)*0.8 #Define a scalar to help with thresholding

dilate_kernel=np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]], np.uint8) #Kernel used for dilation
erode_kernel = np.ones((3,3), np.uint8) #Kernel used for erosion

#-------------------- Loop --------------------#

image_counter = 0
with(device.running()): #This is the loop that runs
    device.start()
    
    for type_, frame in device: #The KinevtV2 returns both the Color frametype and the Depth frametype, so we have to seperate these
        
        
        if type_ is fn2.FrameType.Color:
            
            
            currentFrame = frame #Frame is what the camera returns
            currentFrame = currentFrame.to_array() #We convert the frame into an array to change the datatype, and can now easily show the frames

            currentFrame_color = currentFrame
            
        
            if image_counter < 15: #This loop gives us the first 15 frames  and lets us use these for calibration
                    
                    image_counter+=1
                    color_exist = True
                    
            else: #Calibration should be done now, and then we enter the "real" loop
                if i % framerate == 0:
                    
                    framerate = HIGHFRAMERATE
                    hsv_img = cv2.cvtColor(currentFrame,cv2.COLOR_BGR2HSV)

                    color_mask = cv2.inRange(hsv_img,(ls[0],ls[1]*0.8,ls[2]*0.8),(hs[0],hs[1]*1.3,hs[2]*1.3)) #Lower / Make these values higher to make more or less sensitive glove - Returns binary image, where the color that overlaps with the glove is shown as white

                    for n in range(20):
                        glove = cv2.erode(color_mask,erode_kernel) 
                    for n in range(5):
                        glove = cv2.dilate(glove,dilate_kernel)
                    
                    
                    
                    
                    
                    keypoints, glove_with_keypoints = gloveDetector(glove) #Use gloveDetector function to obtain the keypoints where the glove is detected
                    
                    pts = cv2.KeyPoint.convert(keypoints) #Simple opencv function that lets us access the location of the keypoints
                    

                    try:
                        for n in range(len(pts)): #This loop attempts to draw a red circle around each of the detected keypoints
                            currentFrame_color = cv2.circle(currentFrame_color,(int(keypoints[n].pt[0]),int(keypoints[n].pt[1])),10,(0,0,255),4)
                            
                    except:
                        
                        continue

                    
                    
                    
                    currentFrame_color = cv2.resize(currentFrame_color,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR) #Resizer such that it doesn't fill your entire monitor
                    
                    cv2.imshow("Video", currentFrame_color)
                
                    
                    
            i += 1 #Color loop has ran once, and therefore we add i+1
                
            
            
        if type_ is fn2.FrameType.Depth:
            #print("depth")

            currentFrame_depth = frame

            currentFrame = currentFrame_depth.to_array()
            depth_image = np.array(currentFrame,np.uint16).reshape((424,512,1))
            currentFrameIkkeArray = frame
        if type_ is fn2.FrameType.Depth: #This is the depth loop
            

            currentFrame_depth = frame #Frame is what the camera returns

            currentFrame = currentFrame_depth.to_array() #Convert frame to an array to change datatype, can now easily show frames
            
            depth_array = device.registration.get_points_xyz_array(currentFrame_depth)
          


            delta1 = 240 #Calibration value for mapping from RGB to depth - Simple constant | See https://www.researchgate.net/publication/340527659_Color_and_depth_mapping_of_Kinect_v2 for more details
            delta2 = 30 #Calibration value for mapping from RGB to depth - Simple Constant
            if image_counter < 15: #This loop gives us the first 15 frames  and lets us use these for calibration
                
                depth_exist = True
            else: #Entering the "real" depth loop
                only_human_image = depth_video.only_human(static_background, depth_image)
                
                if only_human_image[0] != False:
                    print("human detected")
                    cv2.imshow("only human", depth_video.conv2_8bit(only_human_image[1]))

                try:
                    for n in range(len(pts)): #Map keypoints from RGB to depth
                        delta1_adv = - 0.02814 * keypoints[n].pt[0] - 0.00704* keypoints[n].pt[1] + 298.656 #Advanced formula for more "precise" mapping from RGB to depth
                        delta2_adv = - 0.00190 * keypoints[n].pt[0] + 0.00971* keypoints[n].pt[1] + 26.472  #See above
                        depth_X = int((keypoints[n].pt[0]-delta1)/3) #Using formula to map RGB keypoint to depth
                        depth_Y = int((keypoints[n].pt[1] / 3) + delta2) #See above
                        
                        cv2.circle(currentFrame,((depth_X,depth_Y)),5,(0,0,0),4) #Draw circle on depth

                        #Create the vector to the hand in the kinect coordinate system
                        kinect_to_hand_vector = np.append(np.round(depth_array[depth_Y,depth_X,:],3),[1])
                        
                        #Using the transformation matrix found in the calibration the vector is found represnted in the UR coordinate system 
                        ur_to_hand_vector = np.dot(np.linalg.inv(KU_transformation_matrix), kinect_to_hand_vector)
                        
                        print(f"Kinect to hand vector {kinect_to_hand_vector} \n UR to hand vector in ur coor {ur_to_hand_vector}")
                        

                        
                except:
                    #print("Hey")
                    continue
                
                
                cv2.imshow("Depth", depth_video.conv2_8bit(currentFrame))
            
        if color_exist and depth_exist and image_counter > 14 and calibration_exist != True: #On startup, these are false so enter this loop
            framerate = LOWFRAMERATE #Set lowframerate for calibration - Helps to make sure program doesn't crash
            print("trying to calibrate")
            KU_transformation_matrix = calibrate_camera(currentFrame_color, depth_array) #Obtain transformationmatrix from the Kinect to the UR
            calibration_exist = True
            
            static_background = depth_video.create_static_backgound(depth_image)
            
            print(f"This is KU:  \n  {KU_transformation_matrix}")

           


            
                    
        K = cv2.waitKey(1)
        if K == 113: #Press Q to close program
            break


cv2.destroyAllWindows()
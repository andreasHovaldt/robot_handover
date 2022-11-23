import freenect2 as fn2
import numpy as np
import cv2
import time
from detect_hand_as_blob import gloveDetector
from calibration_vector import calibrate_camera, matrix
#If the pink square used for calibration IS NOT FOUND the program will crash :)

HIGHFRAMERATE = 8
LOWFRAMERATE = 30
i = 0
framerate = LOWFRAMERATE
device = fn2.Device()

downscale_val = (960, 540)

color_exist = False
depth_exist = False
calibration_exist = False
calibration_vector = None 
#calibration_Vector = calibrate_camera()
#print(calibration_Vector)
#time.sleep(10)

#-------------------- Thresholding --------------------#
def get_hsv_data(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]

#glove_img = cv2.imread("Mats/pink.jpg")
glove_img = cv2.imread("Mats/cameraTest/Kinect V2/glove_color_v2.jpg")
glove_hsv = get_hsv_data(glove_img)
hs = np.array(glove_hsv)*1.2
ls = np.array(glove_hsv)*0.8

dilate_kernel=np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]], np.uint8)
erode_kernel = np.ones((3,3), np.uint8)
print(erode_kernel.shape)
image_counter = 0
with(device.running()):
    device.start()
    #prev_time = 0
    for type_, frame in device:
        #print(type_)
        #print(calibration_vector)
        
        if type_ is fn2.FrameType.Color:
            #print("color")
            
            currentFrame = frame 
            currentFrame = currentFrame.to_array()

            currentFrame_color = currentFrame
            
        
            if image_counter < 15:
                    
                    image_counter+=1
                    color_exist = True
                    #print(image_counter)
            else:
                if i % framerate == 0:
                    #print("color2")
                    framerate = HIGHFRAMERATE
                    hsv_img = cv2.cvtColor(currentFrame,cv2.COLOR_BGR2HSV)

                    color_mask = cv2.inRange(hsv_img,(ls[0],ls[1]*0.8,ls[2]*0.8),(hs[0],hs[1]*1.3,hs[2]*1.3)) #Lower / Make these values higher to make more or less sensitive glove 

                    for n in range(20):
                        glove = cv2.erode(color_mask,erode_kernel)
                    for n in range(5):
                        glove = cv2.dilate(glove,dilate_kernel)
                    
                    
                    #glove = cv2.resize(glove,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR)
                    
                    
                    keypoints, glove_with_keypoints = gloveDetector(glove)
                    
                    pts = cv2.KeyPoint.convert(keypoints)
                    

                    try:
                        for n in range(len(pts)):
                            currentFrame_color = cv2.circle(currentFrame_color,(int(keypoints[n].pt[0]),int(keypoints[n].pt[1])),10,(0,0,255),4)
                            #currentFrame_color = cv2.drawKeypoints(currentFrame_color, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                            #cv2.imshow("Color", glove_point)
                    except:
                        
                        continue

                    
                    
                    
                    # if i % 30 == 0:
                    #     for n in range(len(pts)):
                    #         print("Keypoint nr:", [n]," Position is: ", (int(keypoints[n].pt[0]), int(keypoints[n].pt[1])))
                    currentFrame_color = cv2.resize(currentFrame_color,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR)
                    
                    cv2.imshow("Video", currentFrame_color)
                    #cv2.imshow("Video", glove_with_keypoints)
                    #cv2.imshow("Color", glove)
                
                    
                    
            i += 1
                
            
            
        if type_ is fn2.FrameType.Depth:
            #print("depth")

            currentFrame_depth = frame

            currentFrame = currentFrame_depth.to_array()
            currentFrameIkkeArray = frame
            depth_array = device.registration.get_points_xyz_array(currentFrame_depth)
            #print(f"depth max: {currentFrame.max()}")
            
            
            # depth_mask = currentFrame > 900
            # currentFrame[depth_mask] = 0
            # depth_mask = currentFrame < 700
            # currentFrame[depth_mask] = 0


            delta1 = 240 #use this for calibration
            delta2 = 30 #Use this for calibration
            if image_counter < 15:
                
                depth_exist = True
            else:
                try:
                    for n in range(len(pts)):
                        delta1_adv = - 0.02814 * keypoints[n].pt[0] - 0.00704* keypoints[n].pt[1] + 298.656
                        delta2_adv = - 0.00190 * keypoints[n].pt[0] + 0.00971* keypoints[n].pt[1] + 26.472
                        depth_X = int((keypoints[n].pt[0]-delta1)/3)
                        depth_Y = int((keypoints[n].pt[1] / 3) + delta2)
                        
                        KH_transformation_matrix = matrix([0,0,0],np.round(depth_array[depth_Y,depth_X,:],3))
                        print(f"Vector to hand: \n {np.round(depth_array[depth_Y,depth_X,:],3)}")  #Flip method: {currentFrame[abs(depth_Y-424),abs(depth_X-512)]}")
                        print(f"KH matrix \n {KH_transformation_matrix}")
                        cv2.circle(currentFrame,((depth_X,depth_Y)),5,(0,0,0),4)
                        print(f"UH matrix \n {np.dot(np.linalg.inv(KH_transformation_matrix),KU_transformation_matrix)}")
                        print(f"This is KU:  \n  {KU_transformation_matrix}")
                        #print(f"UH matrix45z \n {np.dot(np.linalg.inv(KH_transformation_matrix),KU_transformation_matrix)}")
                        
                        
                except:
                    #print("Hey")
                    continue
                
                
                cv2.imshow("Depth", currentFrame)
            
        if color_exist and depth_exist and image_counter > 14 and calibration_exist != True:
            framerate = LOWFRAMERATE
            print("trying to calibrate")
            KU_transformation_matrix = calibrate_camera(currentFrame_color, depth_array)
            calibration_exist = True
            
            print(f"This is KU:  \n  {KU_transformation_matrix}")

            
            #cv2.imshow()
            
            #cv2.waitKey()


            
                    
        K = cv2.waitKey(1)
        if K == 113:
            break
            #if i > 1000:
            #    #device.stop()
            #    break

cv2.destroyAllWindows()
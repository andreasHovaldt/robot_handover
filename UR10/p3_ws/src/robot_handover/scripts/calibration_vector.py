import freenect2 as fn2
import numpy as np
import cv2
import time
from detect_hand_as_blob import gloveDetector
from math import cos, sin, radians



X_ANGLE_SCALER = 90/512 #Scaler used to calculate the angle to the pink dot based on the "FOV" of the camera 
Y_ANGLE_SCALER = 60/424






def create_transformation_matrix(translation_vector, rotation_y = 0, rotation_x = 0): #Can make transformation matrices about x and y using this function, default values are angle y=0 and x=0
    def trig(angle): #Takes an angle and returns cos(radian) and sin(radian)
        r = radians(angle)
        return cos(r), sin(r)
    #creates a rotation matrix around y with input deg 
    def roty_matrix(rotation):
        yC, yS = trig(rotation)
        Rotate_Y_matrix = np.array([[yC, 0, yS, 0],
                                    [0, 1, 0, 0],
                                    [-yS, 0, yC, 0],
                                    [0, 0, 0, 1]])
        return Rotate_Y_matrix
    def rotx_matrix(rotation): #Create rotation matrix about x - angle can be input
        xC, xS = trig(rotation)
        Rotate_X_matrix = np.array([[1, 0, 0, 0],
                                    [0, xC, -xS, 0],
                                    [0, xS, xC, 0],
                                    [0, 0, 0, 1]])
        return Rotate_X_matrix
    
    transformation_matrix = np.identity(4) #Create 4x4 identity matrix
    print(translation_vector)
    transformation_matrix[:,3] = translation_vector #Fourth column turns into our translationvector
    transformation_matrix[0:3,0:3]=roty_matrix(rotation_y)[0:3,0:3] #insert rot_y matrix on the rotation-matrix location in trans matrix
    transformation_matrix = np.dot(transformation_matrix,rotx_matrix(rotation_x)) #Make final transformation by dotting trans_y and trans_x
    return transformation_matrix



def calibrate_camera(color_image, depth_array): #Function used to calibrate our camera
    mark_to_ur_translation = create_transformation_matrix(np.array([0,0,-0.17,1])) #Creating transformation from red dot to the UR robot
    
    mark_to_ur_rotation_y = create_transformation_matrix(np.array([0,0,0,1]),45) #Creating the y rotation from red dot to UR
    mark_to_ur_rotation_x = create_transformation_matrix(np.array([0,0,0,1]),0,90) #Creating the x rotation from the red dot to the UR
    mark_to_ur = np.dot(np.dot(mark_to_ur_translation,mark_to_ur_rotation_y),mark_to_ur_rotation_x) #Dotting it all together to create the actual transformation matrix from the dot to the UR
    
    downscale_val = (960, 540)

    #-------------------- Thresholding --------------------#
    def get_hsv_data(img): #Comments for this are written somewhere else already - See CalibrateVectorAndRunProgram
        hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]

    pink_img = cv2.imread("Mats/pink.jpg")
    pink_hsv = get_hsv_data(pink_img)
    hs = np.array(pink_hsv)*1.2
    ls = np.array(pink_hsv)*0.8

    dilate_kernel=np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]], np.uint8)
    erode_kernel = np.ones((3,3), np.uint8)
    print(erode_kernel.shape)


    delta1 = 240 #use this for calibration
    delta2 = 30 #Use this for calibration


    #-------------------- Running camera --------------------#
    print("creating hsv")
    hsv_img = cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)
    
    color_mask = cv2.inRange(hsv_img,(ls[0],ls[1]*0.8,ls[2]*0.8),(hs[0],hs[1]*1.3,hs[2]*1.3))

    for n in range(20):
        pink_bin = cv2.erode(color_mask,erode_kernel)
    for n in range(5):
        pink_bin = cv2.dilate(pink_bin,dilate_kernel)

    print("finding keypoints")
    keypoints, pink_with_keypoints = gloveDetector(pink_bin)

    pts = cv2.KeyPoint.convert(keypoints)
    print(f"points {pts}")
    
    for n in range(len(pts)):
        print("locating keypoints on depth map")
        depth_X = int((keypoints[n].pt[0]-delta1)/3)
        depth_Y = int((keypoints[n].pt[1] / 3) + delta2)
        translation_vector = np.round(depth_array[depth_Y,depth_X,:],3)
        print(f"Calibration vector found to be: {translation_vector}")
        rot_angles=[(depth_Y-212)*Y_ANGLE_SCALER,(depth_X-256)*X_ANGLE_SCALER,0] #This is the amount of angles that the camera is turned compared to the calibration point
        print(f"rot angles are {rot_angles} \n {depth_X , depth_Y}")
    #time.sleep(10)
    translation_vector = np.append(translation_vector, [1])
    print(f"translation_vector {translation_vector}")
    #return create_transformation_matrix(translation_vector,rot_angles[1])
    return np.dot(create_transformation_matrix(translation_vector,-rot_angles[1]), mark_to_ur) #Transformationmatrix from Kinect to the UR


def main():
    calibrate_camera()

if __name__ == "__main__":
    main()
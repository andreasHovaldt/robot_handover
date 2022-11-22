import freenect2 as fn2
import numpy as np
import cv2
import time
from detect_hand_as_blob import gloveDetector



def calibrate_camera(color_image, depth_array):
    
    downscale_val = (960, 540)

    #-------------------- Thresholding --------------------#
    def get_hsv_data(img):
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
    
    color_mask = cv2.inRange(hsv_img,(ls[0],ls[1]*0.9,ls[2]*0.9),(hs[0],hs[1]*1.2,hs[2]*1.2))

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
        print(f"Calibration vector found to be: {np.round(depth_array[depth_Y,depth_X,:],3)}")

    #time.sleep(10)

    return np.round(depth_array[depth_Y,depth_X,:],3)


def main():
    calibrate_camera()

if __name__ == "__main__":
    main()
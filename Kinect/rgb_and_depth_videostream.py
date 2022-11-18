import freenect2 as fn2
import numpy as np
import cv2
import time
from detect_hand_as_blob import gloveDetector
i = 0

device = fn2.Device()
frames = {}

downscale_val = (960, 540)

#-------------------- Thresholding --------------------#
def get_hsv_data(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]

glove_img = cv2.imread("Mats/cameraTest/Kinect V2/glove_colour_v2.jpg")
glove_hsv = get_hsv_data(glove_img)
hs = np.array(glove_hsv)*1.2
ls = np.array(glove_hsv)*0.8

dilate_kernel=np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]], np.uint8)
erode_kernel = np.ones((3,3), np.uint8)
print(erode_kernel.shape)


with(device.running()):
    device.start()
    #prev_time = 0
    for type_, frame in device:
        if type_ is fn2.FrameType.Color:
            
            currentFrame = frame 
            currentFrame = currentFrame.to_array()
            
        #     currentFrame = np.array(currentFrame, np.uint16)
        #     currentFrame.astype(np.uint16)
        #     currentFrame = currentFrame[:,:,0:3]

        
            if i % 1 == 0:
                #print(f"fps = {1/(time.time()-prev_time)}")
                #prev_time = time.time()
                
                currentFrame = currentFrame[:,180:1740]
                #currentFrame = cv2.resize(currentFrame,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR)
                #cv2.imshow("Video", currentFrame)
                
                
                hsv_img = cv2.cvtColor(currentFrame,cv2.COLOR_BGR2HSV)

                color_mask = cv2.inRange(hsv_img,(ls[0],ls[1],ls[2]),(hs[0],hs[1],hs[2]))

                for n in range(1):
                    glove = cv2.erode(color_mask,erode_kernel)
                for n in range(5):
                    glove = cv2.dilate(glove,dilate_kernel)
                
                
                glove = cv2.resize(glove,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR)
                
                
                keypoints, glove_with_keypoints= gloveDetector(glove)
                
                pts = cv2.KeyPoint.convert(keypoints)
                
                
                
                # if i % 30 == 0:
                #     for n in range(len(pts)):
                #         print("Keypoint nr:", [n]," Position is: ", (int(keypoints[n].pt[0]), int(keypoints[n].pt[1])))
                
                cv2.imshow("Video", glove_with_keypoints)
            
                
                
            i += 1
        
        
        if type_ is fn2.FrameType.Depth:
            
            
            currentFrame = frame
            
            
            #print(depth(int(keypoints[n].pt[0])), int(keypoints[n].pt[1]]))
            

            currentFrame = currentFrame.to_array()
            #print(f"depth max: {currentFrame.max()}")
            
            
            # depth_mask = currentFrame > 900
            # currentFrame[depth_mask] = 0
            # depth_mask = currentFrame < 700
            # currentFrame[depth_mask] = 0

            
            
            cv2.imshow("Depth", currentFrame)
            
            try:
                if i % 30 == 0:
                    for n in range(len(pts)):
                        print("Keypoint nr:", [n]," Position is: ", (int(keypoints[n].pt[0]), int(keypoints[n].pt[1])))
                # depth = frame
                # depth_array = device.registration.get_points_xyz_array(depth)
                # print(depth_array[keypoints[0].pt[0],keypoints[0].pt[1]])
            except:
                continue
            
            
            # currentFrame /= currentFrame.max()
            # if currentFrame[int(currentFrame.shape[0]/2),int(currentFrame.shape[1]/2)] > 1:
            #     print(currentFrame[int(currentFrame.shape[0]/2),int(currentFrame.shape[1]/2)])
            #     cv2.imwrite(f'/home/andreas/Desktop/Video_save/Color/{i}.jpg',currentFrame)
            #     for type_, frame in device:
            #         if type_ is fn2.FrameType.Color:
            #             frame = frame.to_array()
            #             cv2.imwrite(f'/home/andreas/Desktop/Video_save/Color/{i}.jpg',frame)
                
            #     i+=1
                
            
            
            # cv2.imwrite(f'/home/andreas/Desktop/Video_save/{i}.png',currentFrame)
            # i+=1
            # cv2.imshow("Depth", currentFrame)
            #cv2.imwrite(f'/home/andreas/Desktop/Video_save/{i}.png',currentFrame)
            
            # if i % 10 == 0:
            #     print(i)
            #     #np.savetxt(f'/home/andreas/Desktop/Video_save/txt/{i}.txt',currentFrame)
            #     #print(currentFrame.max())
            #     cv2.imshow("Video", currentFrame)
            # i += 1
            
            
            
        K = cv2.waitKey(1)
        if K == 113:
            break
        #if i > 1000:
        #    #device.stop()
        #    break

cv2.destroyAllWindows()
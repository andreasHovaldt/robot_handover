import os
import png 
import cv2
import freenect2
import numpy as np
import cv2 
import scipy.ndimage
import time

#load images into array
def create_depth_img_array(path):
    img_array=[]
    for i in range(1000):
        try:
            pngdata = png.Reader(f"{path}/gray{i}.png").read_flat()
            img_array.append(np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1)))
            print("yeet")
        except:
            print(f"{path}/gray{i}.png not found")
    return img_array

def create_color_img_array(path):
    img_array=[]
    for i in range(1000):
        if os.path.exists(f"{path}/color{i}.png"):
            img_array.append(cv2.imread(f"{path}/color{i}.png"))
            print("img found")
        else:
            print(f"{path}/color{i}.png not found")
    return img_array

#add folder to workspace
depth_array = create_depth_img_array("/home/alfred/Desktop/hand_track_dataset/test_singlehand/depth")
color_array = create_color_img_array("/home/alfred/Desktop/hand_track_dataset/test_singlehand/color")

print(f"color array size {len(color_array)} \t depth array size {len(depth_array)}")

def conv2_8bit(img16):
    scaler2_8b = 255/(np.max(img16)+1)
    return np.array(img16*scaler2_8b, np.uint8)
prev_time = time.time()
while True:
    for color_img, depth_img in zip(color_array, depth_array):
        #cv2.imshow("color", color_img) 
        #cv2.waitKey(10)
        depth_slice_list = [] 
        
        #cv2.imshow("start", conv2_8bit(depth_img))
        #depth_img = scipy.signal.medfilt2d(depth_img,3)
        
        
        depth_img = depth_img[100:400,50:350]

        result = np.zeros_like(depth_img)
        result2 = np.zeros_like(depth_img)
        mask1 = depth_img > 1200
        mask2 = depth_img < 2400
        
        mask3 = mask1 == mask2 
        result[mask3] = depth_img[mask3]
        cv2.imshow("result1",conv2_8bit(result))
        dil_img = cv2.dilate(conv2_8bit(result), np.ones((20,20)))
        cv2.imshow("dil img ", dil_img)
        mask4 = dil_img > 0
        result2[mask4] = scipy.ndimage.median_filter(result[mask4],7)
        #result = scipy.ndimage.median_filter(result,2)

        cv2.imshow("result2",conv2_8bit(result2))

        cv2.imshow("Canny",cv2.Canny(conv2_8bit(result2), 1, 2))


        #for r in range(10):
        #    stepsize = (2300-900)/10
        #    mask1 = depth_img > int(r*stepsize+900)
        #    mask2 = depth_img < int((r+1)*stepsize+900)
        #    mask3 = mask1 == mask2 
        #    result_array = np.zeros_like(depth_img, np.uint16)
        #    result_array[mask3]=depth_img[mask3]
        #    depth_slice_list.append(result_array)
            
            #cv2.imshow(f"r{r}", conv2_8bit(result_array))
        cv2.waitKey(10)
    print(f"time to proces 336 images = {time.time()-prev_time}")
    prev_time = time.time()
            
import os
import png 
import cv2
import freenect2
import numpy as np
import cv2 
import scipy.ndimage
import time
import map_color_to_depth as map_color_to_depth
import depth_video


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


#create static backgound 
static_backgound = depth_video.create_static_backgound(depth_array[1])
cropped_static_backgound = static_backgound[100:400,50:350]



prev_time = time.time()
while True:
    for color_img, depth_img in zip(color_array[0:110], depth_array[10:110]):
        #cv2.imshow("color", color_img) 
        #cv2.waitKey(10)
        depth_slice_list = [] 

        
        #cv2.imshow("start", conv2_8bit(depth_img))
        #depth_img = scipy.signal.medfilt2d(depth_img,3)
        
        
        scaled_color = map_color_to_depth.map_rgb_to_depth_size(color_img)
        cv2.imshow("color", scaled_color)
        depth_img8bit = conv2_8bit(depth_img)
        depth_img8bit = depth_img8bit.reshape((424,512))
        depth_img8bit = cv2.cvtColor(depth_img8bit, cv2.COLOR_GRAY2BGR)
        print(f"color scaled = {scaled_color.shape} \n depth = {depth_img8bit.shape}")
        added_image = cv2.addWeighted(scaled_color,0.4,depth_img8bit,0.2,0)
        cv2.imshow("added", added_image)

        only_human = depth_video.only_human(static_backgound, depth_img)
        if only_human[0]:
            cv2.imshow("human depth", conv2_8bit(only_human[1]))
            only_human8bit = cv2.cvtColor(depth_video.conv2_8bit(only_human[1]), cv2.COLOR_GRAY2BGR)
            
            only_human_mask = only_human8bit > 10
            
            empty = np.zeros_like(scaled_color)
            empty[only_human_mask] = scaled_color[only_human_mask]
            cv2.imshow("human only color", empty)


        #for r in range(10):
        #    stepsize = (2300-900)/10
        #    mask1 = depth_img > int(r*stepsize+900)
        #    mask2 = depth_img < int((r+1)*stepsize+900)
        #    mask3 = mask1 == mask2 
        #    result_array = np.zeros_like(depth_img, np.uint16)
        #    result_array[mask3]=depth_img[mask3]
        #    depth_slice_list.append(result_array)
            
            #cv2.imshow(f"r{r}", conv2_8bit(result_array))
        cv2.waitKey(50)
    print(f"time to proces 336 images = {time.time()-prev_time}")
    prev_time = time.time()
            
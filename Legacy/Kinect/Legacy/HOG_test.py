import cv2 
import numpy as np 
import color_video
import depth_video
import time 
import os 
import png 
import skimage.feature as skifeat
import matplotlib.pyplot as plt 


HIGHER_Y_CROP = 400
LOWER_Y_CROP = 20
HIGHER_X_CROP = 400
LOWER_X_CROP = 20

sift = cv2.SIFT_create(nfeatures=5,contrastThreshold=0.01,edgeThreshold=0.01) 


#load images into array
def create_depth_img_array(path):
    img_array=[]
    for i in range(1000):
        try:
            pngdata = png.Reader(f"{path}/gray{i}.png").read_flat()
            img_array.append(np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1)))
        #    print("yeet")
        except:
            continue
            #print(f"{path}/gray{i}.png not found")
    return img_array

def create_color_img_array(path):
    img_array=[]
    for i in range(1000):
        if os.path.exists(f"{path}/color{i}.png"):
            img_array.append(cv2.imread(f"{path}/color{i}.png"))
            #print("img found")
        #else:
            #print(f"{path}/color{i}.png not found")
    return img_array

#add folder to workspace
depth_array = create_depth_img_array("/home/alfred/Desktop/hand_track_dataset/test_singlehand/depth")
color_array = create_color_img_array("/home/alfred/Desktop/hand_track_dataset/test_singlehand/color")

print(f"color array size {len(color_array)} \t depth array size {len(depth_array)}")

#def conv2_8bit(img16):
#    scaler2_8b = 255/(np.max(img16)+1)
#    return np.array(img16*scaler2_8b, np.uint8)


#create static backgound 
static_backgound = depth_video.create_static_backgound(depth_array[1])
cropped_static_backgound = static_backgound[100:400,50:350]



prev_time = time.time()
while True:
    for color_img, depth_img in zip(color_array,depth_array):
        #cv2.imshow("color", color_img) 
        #cv2.waitKey(10)
        only_human = depth_video.only_human(static_backgound, depth_img)
        if only_human[0]:
            cv2.imshow("human depth", depth_video.conv2_8bit_detailed(only_human[1]))
            only_human8bit = depth_video.conv2_8bit_detailed(only_human[1])
            rescale_human = cv2.resize(only_human8bit[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP],(50,50))
            gx = cv2.Sobel(rescale_human, cv2.CV_32F, 1, 0, ksize=1)
            gy = cv2.Sobel(rescale_human, cv2.CV_32F, 0, 1, ksize=1)
            mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
            cv2.imshow("mag", np.array(mag, np.uint8))
            cv2.imshow("angle", np.array(angle, np.uint8))
            fd, hog_image = skifeat.hog(image=rescale_human,visualize=True)
            cv2.imshow("hog",hog_image)
            print(f"mag: \n {mag}, \n angle: \n {angle}")
            print(f"fd \n {fd.shape}")

            x = np.arange(1296)
            y = fd 

            plt.scatter(x,y)

            plt.show()




            
            
            
            cv2.waitKey()
        #for r in range(10):
        #    stepsize = (2300-900)/10
        #    mask1 = depth_img > int(r*stepsize+900)
        #    mask2 = depth_img < int((r+1)*stepsize+900)
        #    mask3 = mask1 == mask2 
        #    result_array = np.zeros_like(depth_img, np.uint16)
        #    result_array[mask3]=depth_img[mask3]
        #    depth_slice_list.append(result_array)
            
            #cv2.imshow(f"r{r}", conv2_8bit(result_array))
        
    print(f"time to proces 336 images = {time.time()-prev_time}")
    prev_time = time.time()

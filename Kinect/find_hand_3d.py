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



#remember to add folder to workspace
depth_array = create_depth_img_array("/home/alfred/Desktop/hand_track_dataset/test_singlehand/depth")


print(f"depth array size {len(depth_array)}")


def conv2_8bit(img16):
    scaler2_8b = 255/(np.max(img16)+1)
    return np.array(img16*scaler2_8b, np.uint8)



def fast_median_noise_reduction(img16,dil_ksize, medfilt_ksize):
    result = np.zeros_like(img16)
    dil_img = cv2.dilate(conv2_8bit(img16), np.ones((dil_ksize,dil_ksize)))
    #cv2.imshow("dil img ", dil_img)
    mask4 = dil_img > 0
    result[mask4] = scipy.ndimage.median_filter(img16[mask4],medfilt_ksize)
    return result

def erode_dilate_noise_reduction(img16, ksize):
    result = np.zeros_like(img16)
    kernel = np.ones((ksize, ksize))
    img = cv2.erode(conv2_8bit(img16), kernel)
    img = cv2.dilate(conv2_8bit(img), kernel)
    mask = img > 0
    result[mask] = img16[mask]
    return result

def find_human_blob(img16):
    params = cv2.SimpleBlobDetector_Params()
    
    params.filterByColor = True
    params.filterByArea = True
    params.filterByCircularity = False
    params.filterByConvexity = False

    params.minCircularity = 0.1
    params.maxCircularity = 1
    params.minArea = 10000
    params.maxArea = 5000000
    params.blobColor = 255

    detector = cv2.SimpleBlobDetector_create(params)

    rest, img_thresh = cv2.threshold(conv2_8bit(img16), 20,200,cv2.THRESH_BINARY)
    #cv2.imshow("thres", img_thresh)

    keypoints = detector.detect(img_thresh)

    img_with_keypoints = cv2.drawKeypoints(conv2_8bit(img16), keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
    #cv2.imshow("img with key points", img_with_keypoints)
    if len(keypoints) != 0: 
        #print(keypoints[0].pt)
        return keypoints[0].pt
    else: 
        return False
    


def find_hand(img16):
    #find human blob 
    human_location = find_human_blob(img16)
    if human_location != False:
        #threshold the image 
        rest, img_thresh = cv2.threshold(conv2_8bit(img16), 20,200,cv2.THRESH_BINARY)
        img_thresh = cv2.erode(img_thresh, np.array([[0,1,1,0],[1,1,1,1],[1,1,1,1],[0,1,1,0]], np.uint8))
        #detect the blobs 
        labeled_img = scipy.ndimage.label(img_thresh)

        #find largest blob 
        largest_blob = 0
        for l in range(np.max(labeled_img[0])):
            bool_arr = labeled_img[0] == l+1
            current_blob_size = np.sum(bool_arr)
            if current_blob_size > largest_blob:
                largest_blob = current_blob_size
                largest_blob_lable = l+1
        
        #create image where only the largest blob is present 
        mask = labeled_img[0] == largest_blob_lable
        only_largest_blob = np.zeros_like(img16)
        only_largest_blob[mask] = img16[mask]
        #cv2.imshow("only largest blob",conv2_8bit(only_largest_blob))
        
        #find all the pixel locations of the largest blob 
        blob_locations = np.argwhere(only_largest_blob)
        #print(f"blob locations \n {blob_locations}")

        #find the pixel with the largest x value 
        hand_location = blob_locations[blob_locations[:,1].argmax()]
        #print(f"hand location \n {hand_location}")
        only_largest_blob = conv2_8bit(only_largest_blob)
        final = cv2.cvtColor(only_largest_blob,cv2.COLOR_GRAY2BGR)
        
        cv2.imshow("hand", cv2.circle(final,(hand_location[1],hand_location[0]),10,(0,0,255),-1))
        return hand_location[0:2]
    else:
        return False

        
        
    

        
#create static backgound 
def create_static_backgound(img16):
    #we copy the imput
    img = img16
    #we crop the image to the size needed 
    img = img[100:400,50:350]
    #we threshold the depth 
    result = np.zeros_like(img)

    mask_close = img > 1200
    mask_far = img < 2400
    
    mask_total = mask_close == mask_far 
    result[mask_total] = img[mask_total]
    #we reduce noice 
    result2 = fast_median_noise_reduction(result,20,(7,7))
    return np.array(result2, np.int16)

#we create a static background from the first frame which is empty 
static_background = create_static_backgound(depth_array[1])


prev_time = time.time()
while True:
    for depth_img in depth_array:
        #crop the image 
        depth_img = depth_img[100:400,50:350]

        #threshold the depth 
        result = np.zeros_like(depth_img)
        result2 = np.zeros_like(depth_img)
        mask_close = depth_img > 1200
        mask_far = depth_img < 2400
        
        mask_total = mask_close == mask_far 
        result[mask_total] = depth_img[mask_total]
        
        result2 = fast_median_noise_reduction(result, 20, (3,3))
        cv2.imshow("result1",conv2_8bit(result))

        #cv2.imshow("result2",conv2_8bit(result2))


        np_no_bg = np.subtract(np.array(result2, np.int16), static_background) #dont subtract with uint
        np_no_bg = np.array(np.absolute(np_no_bg), np.uint16)
        
        #cv2.imshow("np_no_bg", conv2_8bit(np_no_bg))

        human = np.zeros_like(np_no_bg)
    
        mask = np_no_bg > 200        
        
        human[mask] = result2[mask]
        
        #cv2.imshow("human",conv2_8bit(human))

        
        human_filt = fast_median_noise_reduction(human,30,(3,3))
        #cv2.imshow("human filt",conv2_8bit(human_filt))
        find_hand(human_filt)

        cv2.waitKey(1)
    print(f"time to proces {len(depth_array)} = {time.time()-prev_time} \t avg fps = {len(depth_array)/(time.time()-prev_time)}")
    prev_time = time.time()
            
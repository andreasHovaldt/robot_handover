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



#add folder to workspace
depth_array = create_depth_img_array("/home/alfred/Desktop/hand_track_dataset/test_singlehand/depth")


print(f"depth array size {len(depth_array)}")







def conv2_8bit(img16):
    scaler2_8b = 255/(np.max(img16)+1)
    return np.array(img16*scaler2_8b, np.uint8)



def fast_median_noise_reduction(img16,dil_ksize, medfilt_ksize):
    result = np.zeros_like(img16)
    dil_img = cv2.dilate(conv2_8bit(img16), np.ones((dil_ksize,dil_ksize)))
    cv2.imshow("dil img ", dil_img)
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
    cv2.imshow("thres", img_thresh)

    keypoints = detector.detect(img_thresh)

    img_with_keypoints = cv2.drawKeypoints(conv2_8bit(img16), keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
    cv2.imshow("img with key points", img_with_keypoints)
    if len(keypoints) != 0: 
        print(keypoints[0].pt)
        return keypoints[0].pt
    else: 
        return False
    



def find_hand(img16):
    human_blob = np.zeros_like(img16)
    human_location = find_human_blob(img16)
    if human_location != False:
        rest, img_thresh = cv2.threshold(conv2_8bit(img16), 20,200,cv2.THRESH_BINARY)
        img_thresh = cv2.erode(img_thresh, np.array([[0,1,1,0],[1,1,1,1],[1,1,1,1],[0,1,1,0]], np.uint8))
        labeled_img = scipy.ndimage.label(img_thresh)

        #print(labeled_img[0])
        largest_blob = 0
        
        for l in range(np.max(labeled_img[0])):
            bool_arr = labeled_img[0] == l+1
            current_blob_size = np.sum(bool_arr)
            if current_blob_size > largest_blob:
                largest_blob = current_blob_size
                largest_blob_lable = l+1
        #print(f"size {largest_blob}, \t \t lable {largest_blob_lable}")

        mask = labeled_img[0] == largest_blob_lable
        #print(mask)
        only_largest_blob = np.zeros_like(img16)
        
        only_largest_blob[mask] = img16[mask]
        cv2.imshow("only largest blob",conv2_8bit(only_largest_blob))
        #print(scipy.ndimage.find_objects(labeled_img[0], 1))
        #print(blob_locations)
        blob_locations = np.argwhere(only_largest_blob)
        #for row in blob_locations:
        #    print(row)

        #print(blob_locations)
        hand_location = blob_locations[np.argmax(blob_locations, axis=0)][0]
        print(hand_location)
        only_largest_blob = conv2_8bit(only_largest_blob)
        cv2.circle(only_largest_blob,(hand_location[1],hand_location[0]),5,(0,255,0),-1)
        cv2.imshow("hand", only_largest_blob)

        
        
        
            #print(f"col {np.sum(col)}")

        

        
        

        








#create static backgound 
def create_static_backgound(img16):
    img = img16

    img = img[100:400,50:350]
    result = np.zeros_like(img)


    mask1 = img > 1200
    mask2 = img < 2400
    
    mask3 = mask1 == mask2 
    result[mask3] = img[mask3]
    result2 = fast_median_noise_reduction(result,20,(7,7))
    return np.array(result2, np.int16)


static_background = create_static_backgound(depth_array[1])


prev_time = time.time()
while True:
    for depth_img in depth_array:
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
        
        result2 = fast_median_noise_reduction(result, 20, (7,7))
        cv2.imshow("result1",conv2_8bit(result))
        #dil_img = cv2.dilate(conv2_8bit(result), np.ones((20,20)))
        #cv2.imshow("dil img ", dil_img)
        #mask4 = dil_img > 0
        #result2[mask4] = scipy.ndimage.median_filter(result[mask4],7)
        #result = scipy.ndimage.median_filter(result,2)

        cv2.imshow("result2",conv2_8bit(result2))


        np_no_bg = np.subtract(np.array(result2, np.int16), static_background) #dont subtract with uint
        np_no_bg = np.array(np.absolute(np_no_bg), np.uint16)
        
        cv2.imshow("np_no_bg", conv2_8bit(np_no_bg))

        human = np.zeros_like(np_no_bg)
        #human_filt = np.zeros_like(np_no_bg)
        mask = np_no_bg > 200        
        
        human[mask] = result2[mask]
        
        cv2.imshow("human",conv2_8bit(human))

        
        human_filt = fast_median_noise_reduction(human,30,(8,8))
        cv2.imshow("human filt",conv2_8bit(human_filt))
        find_hand(human_filt)

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
            
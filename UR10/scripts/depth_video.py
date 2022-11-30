import numpy as np
import cv2
import scipy.ndimage

LOWER_DEPTH_THRESHOLD = 500
HIGHER_DEPTH_THESHOLD = 3000

HIGHER_Y_CROP = 400
LOWER_Y_CROP = 20
HIGHER_X_CROP = 400
LOWER_X_CROP = 20

def conv2_8bit(img16):
    scaler2_8b = 255/(np.max(img16)+1)
    return np.array(img16*scaler2_8b, np.uint8)


def conv2_8bit_detailed(img16):
    mask_nonzero = img16 > 1
    minimum = LOWER_DEPTH_THRESHOLD
    maximum = HIGHER_DEPTH_THESHOLD

    #print(f"min, max = ({minimum}, {maximum})")
    scaler2_8b = 255/((maximum-minimum)+100)
    img16[mask_nonzero] = img16[mask_nonzero]-minimum
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
    #print("find human")
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
    #print("find hand")
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
        return [None, only_largest_blob, True]
    else:
        return [None, None, False]

#create static backgound 
def create_static_backgound(img16):
    #print(f"creating static backgound {img16.shape}")
    #we copy the imput
    img = img16
    #we crop the image to the size needed 
    img = img[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP]
    #we threshold the depth 
    result = np.zeros_like(img)

    mask_close = img > LOWER_DEPTH_THRESHOLD
    mask_far = img < HIGHER_DEPTH_THESHOLD
    
    mask_total = mask_close == mask_far 
    result[mask_total] = img[mask_total]
    #we reduce noice 
    result2 = fast_median_noise_reduction(result,20,(7,7))
    return np.array(result2, np.int16)

def only_human(background, img16):
    depth_img = img16[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP]
    #print(f"cropped image shape {depth_img.shape}")
    #threshold the depth 
    result = np.zeros_like(depth_img)
    result2 = np.zeros_like(depth_img)
    mask_close = depth_img > LOWER_DEPTH_THRESHOLD
    mask_far = depth_img < HIGHER_DEPTH_THESHOLD

    mask_total = mask_close == mask_far 
    result[mask_total] = depth_img[mask_total]

    result2 = fast_median_noise_reduction(result, 20, (3))
    #print(f"result 2 \n {result2}")
    #cv2.imshow("result2",conv2_8bit(result2))

    #bg subtraction 
    np_no_bg = np.subtract(np.array(result2, np.int16), background) #dont subtract with uint
    np_no_bg = np.array(np.absolute(np_no_bg), np.uint16)
    #print("bg subtracted 1")
    #cv2.imshow("np_no_bg", conv2_8bit(np_no_bg))
    #print(f"no bg shape {np_no_bg.shape}")
    human = np.zeros_like(np_no_bg)
    

    mask = np_no_bg > 200        
    
    human[mask] = result2[mask]
    
    only_human = find_hand(human)
    #print("only_human 7y")
    
    correct_sized_image = np.zeros((424,512,1), np.uint16)
    if only_human[2] != False:
        #print("human found form depth videopy")
        #print(f"only human shape{only_human[1].shape} cast shape {correct_sized_image[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP].shape}")
        correct_sized_image[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP] = only_human[1]
        cv2.imshow("correct_size_only_human", conv2_8bit(correct_sized_image))
        return [True, correct_sized_image]
    else: 
        #print("no human")
        return [False, correct_sized_image]

import freenect2 as fn2
import numpy as np
import cv2
import scipy.ndimage
import png 

i = 0

device = fn2.Device()
frames = {}

downscale_val = (960, 540)

#GLOBAL CONSTANTS 
LOWER_DEPTH_THRESHOLD = 1200
HIGHER_DEPTH_THESHOLD = 3000

HIGHER_Y_CROP = 400
LOWER_Y_CROP = 50
HIGHER_X_CROP = 350
LOWER_X_CROP = 50


#----- Thresholding -----#
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
    print("find human")
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
    cv2.imshow("img with key points", img_with_keypoints)
    if len(keypoints) != 0: 
        #print(keypoints[0].pt)
        return keypoints[0].pt
    else: 
        return False
    


def find_hand(img16):
    print("find hand")
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
        hand_location = blob_locations[blob_locations[:,1].argmin()]
        #print(f"hand location \n {hand_location}")
        #only_largest_blob = conv2_8bit_detailed(only_largest_blob)
        final = cv2.cvtColor(conv2_8bit_detailed(only_largest_blob),cv2.COLOR_GRAY2BGR)
        
        cv2.imshow("hand", cv2.circle(final,(hand_location[1],hand_location[0]),50,(0,0,255),-1))
        print(img16.shape)
        return [hand_location[0:2],only_largest_blob]
    else:
        return False

#create static backgound 
def create_static_backgound(img16):
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

def get_hsv_data(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]

#glove_img = cv2.imread("cameraTest_renamed/Kinect V2/glove_colour.jpg")
#glove_hsv = get_hsv_data(glove_img)
#hs = np.array(glove_hsv)*1.2
#ls = np.array(glove_hsv)*0.8
#kernel=np.array([[0,1,1,0],[1,1,1,1],[1,1,1,1],[0,1,1,0]], np.uint8)
#print(kernel.shape)


image_counter = 0

with(device.running()):
    device.start()
    for type_, frame in device:
        #if type_ is fn2.FrameType.Color:
        #    
        #    currentFrame = frame 
        #    currentFrame = currentFrame.to_array()
        #
        #    if i % 20 == 0:
        #        print(i)
        #        #np.savetxt(f'/home/andreas/Desktop/Video_save/txt/{i}.txt',currentFrame)
        #        #print(currentFrame.max())
        #        
        #        cv2.resize(currentFrame,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR)
        #        #cv2.imshow("Video", currentFrame)
        #        
        #    i += 1
        
        
        if type_ is fn2.FrameType.Depth:
            
            currentFrame = frame
            currentFrame = currentFrame.to_array()
            
            if i % 4 == 0:
                print(i)
                    #np.savetxt(f'/home/andreas/Desktop/Video_save/txt/{i}.txt',currentFrame)
                    #print(currentFrame.max())
                    
                    #cv2.resize(currentFrame,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_LINEAR)
                    #cv2.imshow("Video", currentFrame)
                    
                
                
                print(f"depth max: {currentFrame.max()}")
                image=np.array(currentFrame, np.uint16)
                cv2.imshow("test1 ",conv2_8bit(image))
                #v2.waitKey()
                #if first frame create bg 
                if image_counter < 5:
                    print(image)
                    print(image.reshape((424,512,1)))
                    static_bg = create_static_backgound(image.reshape((424,512,1)))
                    image_counter += 1
                    print(image_counter)
                else:
                    correct_sized_image = np.zeros_like(image.reshape((424,512,1)), np.uint16)
                    
                    depth_img = image[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP].reshape((300,300,1))

                    #threshold the depth 
                    result = np.zeros_like(depth_img)
                    result2 = np.zeros_like(depth_img)
                    mask_close = depth_img > LOWER_DEPTH_THRESHOLD
                    mask_far = depth_img < HIGHER_DEPTH_THESHOLD

                    mask_total = mask_close == mask_far 
                    result[mask_total] = depth_img[mask_total]

                    result2 = fast_median_noise_reduction(result, 20, (3))
                    
                    print("depth threshold and filter")
                    #cv2.imshow("result1",conv2_8bit(result))

                    cv2.imshow("result2",conv2_8bit(result2))

                    #bg subtraction 
                    np_no_bg = np.subtract(np.array(result2, np.int16), static_bg) #dont subtract with uint
                    np_no_bg = np.array(np.absolute(np_no_bg), np.uint16)
                    print("bg subtracted 1")
                    cv2.imshow("np_no_bg", conv2_8bit(np_no_bg))
                    print(f"no bg shape {np_no_bg.shape}")
                    human = np.zeros_like(np_no_bg)
                    

                    mask = np_no_bg > 200        
                    print("test test ")
                    print(f"result2 \n {result2.shape}")
                    print(f"human \n {human.shape}")
                    human[mask] = result2[mask]
                    print("bg subtracted 2")
                    #cv2.imshow("human",conv2_8bit(human))


                    human_filt = fast_median_noise_reduction(human,30,(3))

                    #cv2.imshow("human filt",conv2_8bit(human_filt))
                    only_human = find_hand(human_filt)
                    print("only_human")
                    #cv2.imshow("only_human",conv2_8bit(only_human[1]))
                    
                    if only_human != False:
                        correct_sized_image[LOWER_Y_CROP:HIGHER_Y_CROP, LOWER_X_CROP:HIGHER_X_CROP] = only_human[1]
                        cv2.imshow("correct_size_only_human", conv2_8bit(correct_sized_image))
                        #save image 
                        writer_depth = png.Writer(512,424, bitdepth=16, greyscale=True)
                        print(correct_sized_image.shape)
                        #write_png(f"C:/Users/UNI/Desktop/hand_track_dataset/only_human/{i}.png", correct_sized_image ,bitdepth=16) 
                    
                    cv2.imshow("Depth", currentFrame)
                    
            #print("test")
            i += 1
                
            
            
        K = cv2.waitKey(1)
        if K == 113:
            break
        if i > 10000:
            #device.stop()
            break
cv2.waitKey()
cv2.destroyAllWindows()
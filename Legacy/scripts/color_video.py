import numpy as np 
import cv2 

def map_rgb_to_depth_size(rgb_image):
    delta1 = 210 #use this for calibration
    delta2 = 30 #Use this for calibration
    v_shift = -5
    h_shift = 15
    rgb = rgb_image
    print(f"inpu shape {rgb.shape}")
    rgb_crop_x = rgb[:, delta1+h_shift:1920-(delta1-h_shift)]
    resized_rgb = cv2.resize(rgb_crop_x, (512,424-delta2*2))
    print(f"shape first step {resized_rgb.shape}")
    
    rgb_scaled = resized_rgb#[delta2:424-delta2,:]

    empty = np.zeros((424,512,3),np.uint8)

    empty[delta2+v_shift:424-(delta2-v_shift),:] = rgb_scaled
    rgb_final = empty
    return rgb_final
    
#function to remove the the bzcground from the color image based on the colors in the static color image 
def background_subtraction(static_color_background, rgb_image_scaled):
    #convert images to grayscale 
    bg_gray = cv2.cvtColor(static_color_background, cv2.COLOR_BGR2GRAY) 
    img_gray = cv2.cvtColor(rgb_image_scaled, cv2.COLOR_BGR2GRAY)
    
    #convert to signed int arrays 
    background_array = np.array(bg_gray, np.int16)
    image_array = np.array(img_gray, np.int16)

    #subtract the two images 
    subtracted = np.absolute(np.subtract(background_array, image_array))

    #create a mask where there is no change 
    mask = subtracted < 10 
    
    #where there is no change set the input image to zero 
    rgb_image_scaled[mask] = 0 
    return rgb_image_scaled




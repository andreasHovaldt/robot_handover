import numpy as np 
from skimage.transform import resize #pip install -U scikit-image
import cv2 

def map_rgb_to_depth_size(rgb_image):
    delta1 = 210 #use this for calibration
    delta2 = 30 #Use this for calibration
    v_shift = -5
    h_shift = 15
    rgb = rgb_image
    rgb_crop_x = rgb[:, delta1+h_shift:1920-(delta1-h_shift)]
    resized_rgb = cv2.resize(rgb_crop_x, (512,424-delta2*2))
    print(f"shape first step {resized_rgb.shape}")
    
    rgb_scaled = resized_rgb#[delta2:424-delta2,:]

    empty = np.zeros((424,512,3),np.uint8)

    empty[delta2+v_shift:424-(delta2-v_shift),:] = rgb_scaled
    rgb_final = empty
    return rgb_final
    print(rgb_final.shape)



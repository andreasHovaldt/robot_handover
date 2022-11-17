import os 
import png 
import cv2 
import freenect2
import numpy as np

#load images into array 
def create_img_array(path):
    img_array = []
    with os.scandir(path) as images:
        for image in images:
            if image.name.endswith(".png"):
                #print(f"{path}/{image.name}")
                img=cv2.imread(f"{path}{image.name}")
                #cv2.imshow("video", img)
                height, width, layers = img.shape
                size = (width,height)
                img_array.append(img)
    return img_array

create_img_array("home/alfred/Desktop/hand_track_dataset")

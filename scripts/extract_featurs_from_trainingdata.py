import cv2 
import numpy as np 
import depth_video
import time 
import os 
import png 
import skimage.feature as skifeat #pip install scikit-image
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

#def train_kNN(hog_dataset):




data_folder_path = "Kinect/images/poses_data"

background_path = "Kinect/images/background1.png"

pngdata = png.Reader(background_path).read_flat()
background_raw = np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1))

#def conv2_8bit(img16):
#    scaler2_8b = 255/(np.max(img16)+1)
#    return np.array(img16*scaler2_8b, np.uint8)


#create static backgound 
static_backgound = depth_video.create_static_backgound(background_raw)
cropped_static_backgound = static_backgound[100:400,50:350]



prev_time = time.time()

pose_number = 0

dataset = []
#opens all the images in the dataset 
with os.scandir(data_folder_path) as poses:
    for pose in poses:  
        pose_number += 1  
        print(f"{pose.name} = {pose_number}")
        with os.scandir(os.path.join(data_folder_path, pose.name)) as img_types:
            for img_type in img_types:
                if img_type.name[0] == 'd':
                    with os.scandir(os.path.join(data_folder_path, pose.name ,img_type.name)) as img_paths:
                        for img_path in img_paths:
                            pngdata = png.Reader(os.path.join(data_folder_path, pose.name ,img_type.name, img_path.name)).read_flat()
                            depth_img = np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1))
                            #cv2.imshow("color", color_img) 
                            #cv2.waitKey(10)
                            #if human detected we extract features 
                            only_human = depth_video.only_human(static_backgound, depth_img)
                            if only_human[0]:
                                hog_features = depth_video.extract_HOG(only_human[1])
                                #print(hog_features)
                                data = hog_features
                                if pose_number == 3:
                                    data =np.r_[data, 1]
                                else:
                                    data =np.r_[data, pose_number]
                                #print(data)
                                #print(np.array(data).shape)
                                dataset.append(data)
                                cv2.waitKey(1)

np_dataset = np.array(dataset)



print(np_dataset.shape)  

print(np.sum(np_dataset))

        

np.savetxt("hog_pose_data.txt", np_dataset)

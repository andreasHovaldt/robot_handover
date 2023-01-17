#https://drive.google.com/file/d/1c0eOgwHd-Imz0kRCo7tC52QU1zzBLPZD/view?usp=sharing
import freenect2 as fn2
import numpy as np
import matplotlib.pyplot as plt 
import png
import os.path
import cv2

device = fn2.Device()
frames = {}

pcd_list = []

#pcd_generator = fn2.Registration(1,1)

writer_depth = png.Writer(512,424, bitdepth=16, greyscale=True)
writer_color = png.Writer(1920,1080, bitdepth=8, greyscale=False)


i = 0
images_d = {}
images_c = {}
with(device.running()):
    # For each received frame...
    color_exist = False
    depth_exist = False
    for type_, frame in device:
        # ...stop only when we get an IR frame
        
        if type_ is fn2.FrameType.Color:
            color_frame = frame
            color_array = color_frame.to_array()
            color_exist = True
            #print(color_array)
            

            #print("color frame")
        if type_ is fn2.FrameType.Depth:
            depth_image = frame
            depth_array = frame.to_array()
            depth_exist = True
            
        if (i % 30 == 0) and color_exist and depth_exist:
            print("saveing image")
            images_c[i]=np.array(color_array, np.uint8)
            cv2.imshow("color current", color_array)    
            images_d[i]=np.array(depth_array, np.uint16)

        
        cv2.waitKey(1)
        if i >= 10000:
            break   
        i+=1
#print(images_d[1])

for key in images_d:
    file_location = os.path.join("Kinect/images/depth",f"1{key}.png")
    with open(file_location, 'wb') as f:
        zgray2list = images_d[key].tolist()
        writer_depth.write(f, zgray2list)
for key in images_c:
    file_location = os.path.join("Kinect/images/color", f"{key}.png")
    #print(images_c[key])
    cv2.imwrite(file_location, images_c[key])
    #with open(file_location, 'wb') as f:
    #    color2list = images_c[key].tolist()
    #    writer_color.write(f, color2list)





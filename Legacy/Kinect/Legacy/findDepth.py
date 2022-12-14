import freenect2 as fn2
import numpy as np
import cv2
import PIL
import matplotlib.pyplot as plt 
import scipy.signal


device = fn2.Device()
frames = {}

pcd_list = []

#pcd_generator = fn2.Registration(1,1)

i = 0
images = {}
with device.running():
    # For each received frame...
    
    for type_, frame in device:
        # ...stop only when we get an IR frame
        if type_ is fn2.FrameType.Depth:
            depth_image = frame
            #depth_image /= depth_image.max()
            #depth_image = np.sqrt(depth_image)
            images["D"] = depth_image
            #cv2.imshow("IR Image", ir_image)
        if type_ is fn2.FrameType.Color:
            color_frame = frame
            images["C"]=color_frame
        if i >= 3:
            break
        i+=1
    #pcd_list.append(device.registration.apply(images["D"], images["C"]))

depth_array = device.registration.get_points_xyz_array(images["D"])
print(depth_array[250,250,:])



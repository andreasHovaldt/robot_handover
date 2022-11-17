import freenect2 as fn2
import numpy as np
import cv2
import PIL
import matplotlib.pyplot as plt 
import scipy.signal
import png

device = fn2.Device()
frames = {}

pcd_list = []

#pcd_generator = fn2.Registration(1,1)

writer_depth = png.Writer(512,424, bitdepth=16, greyscale=True)
writer_color = png.Writer(1920,1080, bitdepth=8, greyscale=False)


i = 0
images_d = {}
images_c = {}
with device.running():
    # For each received frame...
    
    for type_, frame in device:
        # ...stop only when we get an IR frame
        if type_ is fn2.FrameType.Color:
            color_frame = frame
            images_c["C"]=color_frame
        if type_ is fn2.FrameType.Depth:
            depth_image = frame
            #depth_image /= depth_image.max()
            #depth_image = np.sqrt(depth_image)
            #images_d["D"] = depth_image
            depth_array = frame.to_array()
            images_d[i]=np.array(depth_array, np.uint16)*7
            #cv2.imshow("IR Image", ir_image)
        if i >= 3:
            break
        i+=1
print(images_d[1])

for key in images_d:
    with open(f'foo_gray{key}.png', 'wb') as f:
        zgray2list = images_d[key].tolist()
        writer_depth.write(f, zgray2list)







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





color_map_float = np.array(plt.get_cmap("twilight").colors)




flat = depth_array.reshape(-1, depth_array.shape[-1])





mask = flat[:,1] != np.nan
flat = flat[~np.isnan(flat).any(axis=1)]
print(f"max z{np.max(flat[:,2])}")
print(f"len colar map{color_map_float.shape[0]}")
color_scaler = color_map_float.shape[0]/abs(np.min(flat[:,2]))
#print(color_scaler)
color_array = []#np.zeros_like(flat[:,2])
#print(color_array)
size_array=np.ones((flat[:,2].shape[0],1))*0.01
#print(flat)


for i,val in enumerate(flat[:,2]):
    #print(f"val{val}")
    #print(f"color map index{int(abs(val)*color_scaler)-1}")
    #print(f"color map at idex = {color_map_float[int(abs(val)*color_scaler)-1]}")
    color_array.append(color_map_float[int(abs(val)*color_scaler)-1])


#print(flat)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter3D(flat[:,0],flat[:,2],flat[:,1], c=color_array, s=size_array)

plt.show()
#ir_image = frame.to_array()
#ir_image /= ir_image.max()
#ir_image = np.sqrt(ir_image)

#cv2.imshow("IR Image", ir_image)
#cv2.waitKey()
#cv2.destroyAllWindows()






#with(device.running()):
#    pass
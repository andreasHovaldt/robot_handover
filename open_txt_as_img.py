import numpy as np 
import cv2 
import matplotlib.pyplot as plt
import math 
import scipy.signal


img = np.loadtxt("C:/Users/UNI/Downloads/depth_txt/10.txt")


def median_blur(img, k_size):
    ks = k_size
    idm = int(ks/2)
    out_img = np.zeros_like(img)
    for y in range(img.shape[0]-1):
        for x in range(img.shape[1]-1):
            try:
                out_img[y,x] = int(np.median(img[y-idm:y+idm,x-idm:x+idm]))
            except:
                print(np.median(img[y-idm:y+idm,x-idm:x+idm]))
    return out_img

#for i in range(2):
    #img = median_blur(img,5)

img = scipy.signal.medfilt(img,5)


img_color = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

color_map = np.array(plt.get_cmap("twilight").colors)*255
color_map_float = np.array(plt.get_cmap("twilight").colors)

print(np.max(img))

#img = np.array(((img - np.min(img)) / np.max(img)) *255, np.uint8)

print(len(color_map))

color_scaler = len(color_map) / np.max(img) 
data_scaler = 500/np.max(img)

img_xdata = []
img_ydata = []
img_zdata = []
img_cdata = []


fig = plt.figure()
ax = plt.axes(projection='3d')

for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        img_color[y,x,:] = color_map[int(color_scaler * img[y,x])-1]
        if  img[y,x] != 0:
            internal_x = -(x-256)*0.002246093750
            real_x = math.sin(math.atan(internal_x / 1))*img[y,x] #0.819152
            internal_y = -(y-256)*0.002246093750
            real_y = math.sin(math.atan(internal_y / 0.819152))*img[y,x]
            img_xdata.append(real_x)
            img_zdata.append(real_y)
            #print(img[y,x]*data_scaler)
            img_ydata.append(img[y,x])
            img_cdata.append(color_map_float[int(color_scaler * img[y,x])-1])
        
    print(y)
        
#print(f"x data shape {img_xdata.shape} \t y data shape {img_ydata.shape} \t z data shape {img_zdata.shape}")        
cv2.imshow("cool depth", img_color)
cv2.waitKey()

size = np.ones_like(img_xdata)*0.01

ax.scatter3D(img_xdata,img_ydata,img_zdata, c=img_cdata, s=size)




plt.show()

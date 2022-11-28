import numpy as np
import cv2 
import matplotlib.pyplot as plt 
import png 
import math 
import scipy.ndimage

def conv2_8bit(img16):
    scaler2_8b = 255/(np.max(img16)+1)
    return np.array(img16*scaler2_8b, np.uint8)


def create_psuedo_point_cloud(img16_non_crop):
    input_dimensions = img16_non_crop.shape
    result_array = np.zeros((input_dimensions[0],input_dimensions[1],3), np.int16)
    blob_location_mask = img16_non_crop > 1
    blob_locations = np.argwhere(img16_non_crop)
    for location in blob_locations:
        y = location[0]
        x = location[1]
        z = img16_non_crop[y,x]
        if z > 100:
            result_array[y,x,:] = [math.sin(math.atan((x-256)*0.0022460 / 0.82))*z,math.sin(math.atan((y-256)*0.0022460 / 0.82))*z,z]

    #for y in range(input_dimensions[0]):
    #    for x in range(input_dimensions[1]):
    #        result_array[y,x,:] = [math.sin(math.atan((x-256)*0.0022460 / 0.82))*img16_non_crop[y,x],math.sin(math.atan((y-256)*0.0022460 / 0.82))*img16_non_crop[y,x],img16_non_crop[y,x]]

    print(result_array)
    flat = result_array.reshape(-1, result_array.shape[-1])
    flat = flat[~np.all(flat == 0, axis=1)]
    #flat = np.ma.masked_equal(flat,0)
    
    return flat
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    size_array = np.ones_like(flat[:,0], np.float16)*0.01
    
    ax.scatter3D(flat[:,0],flat[:,2],-flat[:,1], s=size_array)

    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
def fast_median_noise_reduction(img16,dil_ksize, medfilt_ksize):
    result = np.zeros_like(img16)
    dil_img = cv2.dilate(conv2_8bit(img16), np.ones((dil_ksize,dil_ksize)))
    #cv2.imshow("dil img ", dil_img)
    mask4 = dil_img > 0
    result[mask4] = scipy.ndimage.median_filter(img16[mask4],medfilt_ksize)
    return result


pngdata = png.Reader(f"C:/Users/UNI/Desktop/hand_track_dataset/torso/257.png").read_flat()
img_torso = np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1))

img_torso = fast_median_noise_reduction(img_torso, 300, (7,7))

pngdata = png.Reader(f"C:/Users/UNI/Desktop/hand_track_dataset/only_human/257.png").read_flat()
img_human = np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1))

torso_pcd = create_psuedo_point_cloud(img_torso)
human_pcd = create_psuedo_point_cloud(img_human)


fig = plt.figure()
ax = plt.axes(projection='3d')
size_array = np.ones_like(human_pcd[:,0], np.float16)*0.01
ax.scatter3D(human_pcd[:,0],human_pcd[:,2],-human_pcd[:,1], s=size_array)

size_array = np.ones_like(torso_pcd[:,0], np.float16)*0.01
ax.scatter3D(torso_pcd[:,0],torso_pcd[:,2],-torso_pcd[:,1], s=size_array)

plt.show()
plt.pause(0.1)
plt.close()



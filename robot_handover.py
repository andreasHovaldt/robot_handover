import cv2
import numpy as np 


#alfred

def get_hsv_data(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]

glove_img = cv2.imread("cameraTest_renamed/Kinect V2/glove_colour.jpg")
img = cv2.imread("cameraTest_renamed/Kinect V2/4.jpg")

print(glove_img.shape)
glove_hsv = get_hsv_data(glove_img)
hsv_img = hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

print(glove_hsv)

hue_img = np.array(hsv_img[:,:,0])
sat_img = np.array(hsv_img[:,:,1])
v_img   = np.array(hsv_img[:,:,2])


hs = np.array([87.79605263157895, 179.17105263157896, 143.62828947368422])*1.2
ls = np.array([87.79605263157895, 179.17105263157896, 143.62828947368422])*0.8

mask = cv2.inRange(hsv_img,(ls[0],ls[1],ls[2]),(hs[0],hs[1],hs[2]))
print(mask)
imask = mask>0
glove = np.zeros_like(img, np.uint8)
glove[imask] = img[imask]
#imask = mask>0

kernel = np.ones((3,4), np.uint8)
glove = cv2.cvtColor(glove, cv2.COLOR_BGR2GRAY)
_,binary_glove = cv2.threshold(glove, 30, 255, cv2.THRESH_BINARY)

binary_glove = cv2.erode(binary_glove,kernel)
for i in range(4):
    binary_glove = cv2.dilate(binary_glove,kernel)

cv2.imshow("img",img)
cv2.imshow("glove_detect", binary_glove)



cv2.waitKey()
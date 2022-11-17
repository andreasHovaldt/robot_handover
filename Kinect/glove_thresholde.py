import cv2
import numpy as np 


def get_hsv_data(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return [np.average(hsv_img[:,:,0]),np.average(hsv_img[:,:,1]),np.average(hsv_img[:,:,2])]

glove_img = cv2.imread("Mats/cameraTest/Kinect V2/glove_colour.jpg")
img = cv2.imread("Mats/cameraTest/Kinect V2/1.jpg")

glove_hsv = get_hsv_data(glove_img)

hsv_img = hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


hs = np.array(glove_hsv)*1.2
ls = np.array(glove_hsv)*0.8

mask = cv2.inRange(hsv_img,(ls[0],ls[1],ls[2]),(hs[0],hs[1],hs[2]))

kernel=np.array([[0,1,1,0],[1,1,1,1],[1,1,1,1],[0,1,1,0]], np.uint8)

print(kernel.shape)

for i in range(1):
    glove = cv2.erode(mask ,kernel)
for i in range(3):
    glove = cv2.dilate(glove,kernel)

cv2.imshow("img",img)
cv2.imshow("glove_detect", glove)

cv2.waitKey()
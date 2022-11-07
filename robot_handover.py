import cv2
import numpy as np

#Andreas

img = cv2.imread("cameraTest_renamed/Kinect V2/4.jpg")

cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
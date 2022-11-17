import cv2
import numpy as np

img = cv2.imread("Mats/cameraTest/Kinect V2/5.jpg")
params = cv2.SimpleBlobDetector_Params()
imgBlue = img[:,:,2]

# Change thresholds
params.minThreshold = 0
params.maxThreshold = 255
 
# Filter by Area.
params.filterByArea = True
params.minArea = 500
params.maxArea = 5000


# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.4
params.maxCircularity = 0.7
 
# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.84
params.maxConvexity = 0.9
 
# Filter by Inertia #6
params.filterByInertia = False
params.minInertiaRatio = 0.1
params.maxInertiaRatio = 0.5


# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
  detector = cv2.SimpleBlobDetector(params)
else : 
  detector = cv2.SimpleBlobDetector_create(params)
 

'''
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
'''
# Detect blobs.
keypoints = detector.detect(img)

keypointsBlue = detector.detect(imgBlue)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
imBlue_with_keypoints = cv2.drawKeypoints(imgBlue, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#hsv_with_keypoints = cv2.drawKeypoints(HSV, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


# Show keypoints
#cv2.imshow("Keypoints", im_with_keypoints)

cv2.imshow("KeypointsBlue", imBlue_with_keypoints)
#cv2.imshow("Keypoints HSV", hsv_with_keypoints)
cv2.waitKey(0)
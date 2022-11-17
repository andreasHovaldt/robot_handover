import cv2
import numpy as np

img = cv2.imread("C:/Users/Tobia/Documents/GitHub/kingDominoOpenCV/King Domino dataset/Cropped and perspective corrected boards/66.jpg")#, cv2.IMREAD_GRAYSCALE)
params = cv2.SimpleBlobDetector_Params()



# Change thresholds
params.minThreshold = 0
params.maxThreshold = 255
 
# Filter by Area.
params.filterByArea = True
params.minArea = 70
params.maxArea = 800


# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.4
params.maxCircularity = 0.7
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.84
params.maxConvexity = 0.9
 
# Filter by Inertia #6
params.filterByInertia = True
params.minInertiaRatio = 0.1
params.maxInertiaRatio = 0.5
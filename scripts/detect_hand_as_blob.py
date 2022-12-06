import cv2
import numpy as np


def create_hand_detector():
  params = cv2.SimpleBlobDetector_Params() #Using Cv2 simple blob detector with params - Below are the parameters 
  #print(imgThresholded)

  #params.minThreshold = 0
  #params.maxThreshold = 255

  # Filter by Area.
  params.filterByArea = False
  params.minArea = 1000
  params.maxArea = 50000

  #Filter by color
  params.filterByColor = True
  params.blobColor = 255


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
  return(detector)
  

'''
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
'''



def gloveDetector(image,detector):
  #Detect blob
  k_points = detector.detect(image)
  #Draw blob
  image_k_points = 0#cv2.drawKeypoints(image, k_points, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  return k_points#, image_k_points
  






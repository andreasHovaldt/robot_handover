import cv2
import numpy as np
import glove_thresholde


img = cv2.imread("Mats/cameraTest/Kinect V2/5.jpg")
imgThresholded = (glove_thresholde.findGlove(img))
params = cv2.SimpleBlobDetector_Params()
#print(imgThresholded)

#params.minThreshold = 0
#params.maxThreshold = 255

# Filter by Area.
params.filterByArea = True
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
  
 

'''
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
'''



def gloveDetector(image):
  #Detect blob
  k_points = detector.detect(image)
  
  #Draw blob
  image_k_points = cv2.drawKeypoints(image, k_points, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   


  return k_points, image_k_points
  


# #------
# # Detect blobs.
# keypoints = detector.detect(imgThresholded)


# # Draw detected blobs as red circles.

# im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# imgThresholded_with_keypoints = cv2.drawKeypoints(imgThresholded, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# #---------


def main():
  
  # Generate keypoints and image w/ keypoints
  keypoints, imgThresholded_with_keypoints = gloveDetector(imgThresholded)
  
  # Show img
  cv2.imshow("KeypointsThresholded", imgThresholded_with_keypoints)


  pts = cv2.KeyPoint_convert(keypoints)

  print(pts.size/2) # Number of keypoints
  #print(keypoints[0].size)
  #Find coordinates

  #Loop to print location of all keypoints
  for i in range(int(pts.size/2)):
  
    print("Keypoint nr:", [i]," Position is: ", (keypoints[i].pt[0], keypoints[i].pt[1]))
  

  cv2.waitKey(0)

if __name__ == "__main__":
  main()
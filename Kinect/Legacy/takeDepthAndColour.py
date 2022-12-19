import cv2
import freenect2 as fn2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
device = fn2.Device()



with(device.running()):
    for type_, frame in device:
        if type_ is fn2.FrameType.Color:
            
            currentFrame = frame 
            currentFrame = currentFrame.to_array()
            
            color_image = currentFrame#[:,160:1760]
            
            cv2.imshow("Color", color_image)
        
        
        
        if type_ is fn2.FrameType.Depth:
            
            currentFrame = frame 
            currentFrame = currentFrame.to_array()
            
            depth_image = currentFrame#[30:394,:]
            
            cv2.imshow("Depth", depth_image)
            
        
        K = cv2.waitKey(1)
        if K == 113:
            cv2.imshow("Color", color_image)
            cv2.imshow("Depth", depth_image)
            break
    



cv2.waitKey()
cv2.destroyAllWindows()

# imgColor = plt.imshow(color_image)
# imgDepth = plt.imshow(depth_image)
# qqplt.show()



fig1 = plt.figure()
#ax1 = fig1.add_subplot(1, 2, 1)
imgplot1 = plt.imshow(color_image)
#ax1.set_title('Color')

fig2 = plt.figure()
#ax2 = fig2.add_subplot(1, 2, 2)
imgplot2 = plt.imshow(depth_image)
#ax2.set_title('Depth')

plt.show()

# imgColor = mpimg.imread(np.array(color_image))
# imgDepth = mpimg.imread(np.array(depth_image))


#imgplot = plt.imshow(imgColor)
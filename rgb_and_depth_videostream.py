import freenect2 as fn2
import numpy as np
import cv2

device = fn2.Device()
frames = {}

downscale_val = (960, 540)

with(device.running()):
    device.start()
    for type_, frame in device:
        if type_ is fn2.FrameType.Color:
            
            currentFrame = frame 
            currentFrame = currentFrame.to_array()
            currentFrame = currentFrame[:,:,0:3]
            currentFrame = cv2.resize(currentFrame,downscale_val,interpolation=cv2.INTER_LINEAR)
            
            cv2.imshow("RGB", currentFrame[:,200:760,:])
        
        if type_ is fn2.FrameType.Depth:
            
            currentFrame = frame
            currentFrame = currentFrame.to_array()
            currentFrame /= currentFrame.max()
            
            cv2.imshow("Depth", currentFrame)
        K = cv2.waitKey(1)
        if K == 113:
            break

cv2.destroyAllWindows()
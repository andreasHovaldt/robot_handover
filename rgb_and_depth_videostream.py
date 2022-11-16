import freenect2 as fn2
import numpy as np
import cv2

i = 0

device = fn2.Device()
frames = {}

downscale_val = (960, 540)

with(device.running()):
    device.start()
    for type_, frame in device:
        if type_ is fn2.FrameType.Color:
            
            currentFrame = frame 
            currentFrame = currentFrame.to_array()
        #     currentFrame = np.array(currentFrame, np.uint16)
        #     currentFrame.astype(np.uint16)
        #     currentFrame = currentFrame[:,:,0:3]
        #     currentFrame = cv2.resize(currentFrame,downscale_val,interpolation=cv2.INTER_LINEAR)
            
        #     cv2.imwrite(f'/home/andreas/Desktop/Video_save/{i}.jpg',currentFrame)
        #     i+=1
            
        #     cv2.imshow("RGB", currentFrame[:,200:760,:])
        
            if i % 10 == 0:
                print(i)
                #np.savetxt(f'/home/andreas/Desktop/Video_save/txt/{i}.txt',currentFrame)
                #print(currentFrame.max())
                cv2.imshow("Video", currentFrame)
            i += 1
        
        
        if type_ is fn2.FrameType.Depth:
            
            currentFrame = frame
            currentFrame = currentFrame.to_array()
            # currentFrame /= currentFrame.max()
            # if currentFrame[int(currentFrame.shape[0]/2),int(currentFrame.shape[1]/2)] > 1:
            #     print(currentFrame[int(currentFrame.shape[0]/2),int(currentFrame.shape[1]/2)])
            #     cv2.imwrite(f'/home/andreas/Desktop/Video_save/Color/{i}.jpg',currentFrame)
            #     for type_, frame in device:
            #         if type_ is fn2.FrameType.Color:
            #             frame = frame.to_array()
            #             cv2.imwrite(f'/home/andreas/Desktop/Video_save/Color/{i}.jpg',frame)
                
            #     i+=1
                
            
            
            # cv2.imwrite(f'/home/andreas/Desktop/Video_save/{i}.png',currentFrame)
            # i+=1
            # cv2.imshow("Depth", currentFrame)
            #cv2.imwrite(f'/home/andreas/Desktop/Video_save/{i}.png',currentFrame)
            
            # if i % 10 == 0:
            #     print(i)
            #     #np.savetxt(f'/home/andreas/Desktop/Video_save/txt/{i}.txt',currentFrame)
            #     #print(currentFrame.max())
            #     cv2.imshow("Video", currentFrame)
            # i += 1
            
            
            
        K = cv2.waitKey(1)
        if K == 113:
            break
        if i > 1000:
            #device.stop()
            break

cv2.destroyAllWindows()
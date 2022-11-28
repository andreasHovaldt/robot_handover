import freenect2 as fn2
import numpy as np
import cv2
import PIL

device = fn2.Device()
frames = {}


with device.running():
    # For each received frame...
    for type_, frame in device:
        # ...stop only when we get an IR frame
        if type_ is fn2.FrameType.Depth:
            ir_image = frame.to_array()
            ir_image /= ir_image.max()
            ir_image = np.sqrt(ir_image)
            cv2.imshow("IR Image", ir_image)
            K = cv2.waitKey(1)
            if K == 113:
                break


ir_image = frame.to_array()
ir_image /= ir_image.max()
ir_image = np.sqrt(ir_image)

cv2.imshow("IR Image", ir_image)
cv2.waitKey()
cv2.destroyAllWindows()






#with(device.running()):
#    pass
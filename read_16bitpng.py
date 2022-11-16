import png
import numpy as np
import cv2

pngdata = png.Reader("foo_gray3.png").read_flat()
img = np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1))

print(img)
print(img.dtype)
print(img.shape)

#display in cv2 
scalar = 255/np.max(img)

cv2img = np.array((img*scalar), np.uint8)
cv2.imshow("iojrsb" ,cv2img)
cv2.waitKey()


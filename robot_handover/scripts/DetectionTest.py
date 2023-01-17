import cv2
import numpy as np
from matplotlib import pyplot as plt



LayingGlove = cv2.imread('C:/Users/chris/Desktop/P3 after/GloveExtractLaying.png')
LayingHSV = cv2.cvtColor(LayingGlove,cv2.COLOR_BGR2HSV)

StandingGlove = cv2.imread('C:/Users/chris/Desktop/P3 after/GloveExtractStanding.png')
StandingHSV = cv2.cvtColor(StandingGlove,cv2.COLOR_BGR2HSV)

#3 following function fully isolates glove
def isolateGlove(glove):

    binary = cv2.inRange(glove[:,:,1],80,251)

    print(binary)
    cv2.imshow("H threshold", binary)
    return()

def maskGlove():
    mask = cv2.inRange(StandingHSV[:,:,1],80,251)
    result = cv2.bitwise_and(StandingGlove,StandingGlove, mask= mask)
    return(result)

    

    



     

# following function is meant to create a histogram of the HSV values
def createHistogram(hsvImage):
    
    #we find the min and max in order to later stretch the histogram
    min = np.min(hsvImage[:,:,0])
    max = np.max(hsvImage[:,:,0])
    print("max sat in standing is:"+str(max))
    print("min sat in standing is:"+str(min))

    #following is the formula for histogram stretching implemented
    Normalized = np.array((255/(max-min))*(hsvImage[:,:,0]-min),np.uint8)

    print("max normal in standing is:"+str(np.max(Normalized)))
    print("min normal in standing is:"+str(np.min(Normalized)))
    

    cv2.imshow('normal',Normalized)

    

    
    hist,bins = np.histogram(hsvImage[:,:,0].ravel(),256,[0,256])

    histH = cv2.calcHist(hsvImage,[0],None,[256],[0,255])
    HistS = cv2.calcHist(hsvImage,[1],None,[256],[0,255])
    plt.hist(hsvImage[:,:,0].ravel(),256,[0,256])
    
    plt.show()

    return()

# cv2.imshow("standingHSV",StandingHSV)
# cv2.imshow("LayingHSV", LayingHSV)


masked = maskGlove()

maskedHSV = cv2.cvtColor(masked,cv2.COLOR_BGR2HSV)
cv2.imshow("masked",maskedHSV[:,:,0])
cv2.imshow("standingHSVonly",StandingHSV)
cv2.imshow("standingHSVonlyH",StandingHSV[:,:,0])
# cv2.imshow("LayingHSVonly", LayingHSV[:,:,0])

isolateGlove(StandingHSV)
createHistogram(maskedHSV)
# createHistogram(LayingHSV)


cv2.waitKey()







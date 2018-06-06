# This python code uses MicroManager device drivers to control a camera. 
# Tested on Hamamatsu Orca Flash 4 camera, it acquires a sequence of images and 
# stores them in a folder. ROI will also be tested.
# Code implementation: David Sanchez

#code used to get an image sequence acquisition

#Adding micro manager to the sys path
import sys
import MMCorePy #load MicroManager for device control
import matplotlib.pyplot as plt
from pylab import *
import time
#import imageio
from scipy import misc
import cv2
#import skimage.io
#from skimage import exposure

def waitAcquisition(mmc):      
    while True:
        if mmc.isSequenceRunning():
            time.sleep(0.0001)
        else:
            break
            
def imgNormalization(arr):
    arr = arr.astype('float')
    minVal = arr.min()
    maxVal = arr.max()
    maxLim = 2**16
    if minVal != maxVal:
        arr -= minVal
        arr *= (maxLim/(maxVal - minVal))
    return arr.astype('uint16')

def main():
    sys.path.append("C:\\Program Files\\Micro-Manager-1.4")
    ion()
    
    #loading camera
    mmc = MMCorePy.CMMCore()
    mmc.getVersionInfo()
    mmc.loadDevice('Camera', 'DemoCamera', 'DCam')
    #Hamamatsu
    #mmc.loadDevice('Camera', 'HamamatsuHam', 'HamamatsuHam_DCAM')    

    mmc.initializeAllDevices()
    mmc.setCameraDevice('Camera')
    
    
    #All figures are closed
    plt.close("all")
    
    #Sigle image snapshot
    #mmc.setExposure(20) #ms
    mmc.snapImage()
    img = mmc.getImage() #this is numpy array, by the way
    plt.imshow(img, cmap='gray')
    plt.show()
    
    #Region of Interest
    x = 0
    y = 0
    xSize = 500
    ySize = 500
    mmc.setROI(x,y,xSize,ySize)
    start_time=time.time()
    #Image sequence acquisition
    numImages = 2
    intervalMs = 1
    mmc.clearCircularBuffer()
    mmc.startSequenceAcquisition(numImages,intervalMs,1)
    
    #print mmc.getRemainingImageCount()
    
    waitAcquisition(mmc)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    for x in range(numImages):
        #print mmc.getRemainingImageCount()
        img = mmc.popNextImage()
        filename = "C:\\Users\\MOTIV\\Documents\\Python\\image%d.tiff" % (x,)
        #filename = "C:\\Users\\Administrateur\\Documents\\David\\image%d.tiff" % (x,)
        #misc.imsave(filename, imgNormalization(img))
        cv2.imwrite(filename,img)
        #imageio.imwrite(filename, imgNormalization(img))
        figure()
        plt.imshow(img, cmap='gray')
        plt.show()
        #print imgNormalization(img).dtype
    
    mmc.reset()


if __name__ == "__main__": main()
    
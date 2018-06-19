# This python code uses MicroManager device drivers to control a camera. 
# Tested on Hamamatsu Orca Flash 4 camera, it acquires a sequence of images and 
# stores them in a folder. ROI will also be tested.
# Code implementation: David Sanchez

#code used to get an image sequence acquisition

#Importing necessary libraries
import sys
import MMCorePy #load MicroManager for device control
import matplotlib.pyplot as plt
from pylab import *
import time
from PIL import Image

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
    #ion()
    
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
    #plt.imshow(img, cmap='gray')
    #plt.show()
    
    #Region of Interest
    x = 0
    y = 0
    xSize = 512
    ySize = 512
    mmc.setROI(x,y,xSize,ySize)

    #Image sequence acquisition
    #mmc.setExposure(1)
    numImages = 50
    intervalMs = 1
    mmc.clearCircularBuffer()
    start_time = time.time()
    mmc.startSequenceAcquisition(numImages, intervalMs, 1)

    #waitAcquisition(mmc)
    imList = []
    flag = True
    while True:
        if mmc.getRemainingImageCount() > 0:
            img = mmc.popNextImage()
            #filename = "C:\\Users\\MOTIV\\Documents\\Python\\image%d.tiff" % (x,)
            filename = "sequence.tiff"
            #filename = "C:\\Users\\Administrateur\\Documents\\David\\image%d.tiff" % (x,)
            imList.append(Image.fromarray(img))
            imList[0].save(filename, compression="None", save_all=True,
                           append_images=imList[1:])
        elif not mmc.isSequenceRunning():
            if flag:
                print("Acquisition finished after %s seconds" % (time.time() - start_time))
                flag = False
            if len(imList) == numImages:
                print("File saved after %s seconds" % (time.time() - start_time))
                break

    print("Remaining Images: %d" % mmc.getRemainingImageCount())
    #plt.show()
    mmc.reset()


if __name__ == "__main__":
    main()
    

# This python code uses MicroManager device drivers to control a camera.
# Tested on Hamamatsu Orca Flash 4 camera, it acquires a sequence of images and
# stores them in a folder. ROI will also be tested.
# Code implementation: David Sanchez

# code used to get an image sequence acquisition

# Importing necessary libraries
import sys
import MMCorePy  # load MicroManager for device control
import matplotlib.pyplot as plt
from pylab import *
import time
from PIL import Image


class AcquisitionModel:

    def __init__(self):
        sys.path.append("C:\\Program Files\\Micro-Manager-1.4")
        # loading camera
        self.mmc = MMCorePy.CMMCore()
        self.mmc.getVersionInfo()
        self.mmc.loadDevice('Camera', 'DemoCamera', 'DCam')
        # Hamamatsu
        # self.mmc.loadDevice('Camera', 'HamamatsuHam', 'HamamatsuHam_DCAM'
        self.mmc.initializeAllDevices()
        self.mmc.setCameraDevice('Camera')
        self.x = 0
        self.y = 0
        self.xSize = int(self.mmc.getProperty('Camera', 'OnCameraCCDXSize'))
        self.ySize = int(self.mmc.getProperty('Camera', 'OnCameraCCDYSize'))
        self.expTime = 1
        self.numImages = 1
        self.intervalMs = 1

    def setROI(self, x, y, xSize, ySize):
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.mmc.setROI(x, y, xSize, ySize)

    def setExposureTime(self, expTime):
        self.expTime = expTime
        self.mmc.setExposure(self.expTime)

    def setNumImages(self, numImages):
        self.numImages = numImages

    def setIntervalMs(self, intervalMs):
        self.intervalMs = intervalMs

    def getXSize(self):
        return self.xSize

    def getYSize(self):
        return self.ySize

    def snapImage(self):
        self.mmc.snapImage()
        self.img = self.mmc.getImage()  # this is numpy array, by the way

    def getImage(self):
        return self.img

    def startSequenceAcquisition(self):
        # Image sequence acquisition
        start_time = time.time()
        self.mmc.clearCircularBuffer()
        self.mmc.startSequenceAcquisition(self.numImages, self.intervalMs, 1) # 1 is stopOnOverflow parameter

        print self.mmc.getRemainingImageCount()

        self.waitAcquisition()
        print("--- %s seconds ---" % (time.time() - start_time))
        imList = []
        print self.mmc.getRemainingImageCount()
        for x in range(self.numImages):
            # print mmc.getRemainingImageCount()
            img = self.mmc.popNextImage()
            # filename = "C:\\Users\\MOTIV\\Documents\\Python\\image%d.tiff" % (x,)
            filename = "sequence.tiff"
            # filename = "C:\\Users\\Administrateur\\Documents\\David\\image%d.tiff" % (x,)
            imList.append(Image.fromarray(img))
            imList[0].save(filename, compression="tiff_deflate", save_all=True,
                           append_images=imList[1:])
        print self.mmc.getRemainingImageCount()

    def resetCore(self):
        self.mmc.reset()

    def waitAcquisition(self):
        while True:
            if self.mmc.isSequenceRunning():
                time.sleep(0.0001)
            else:
                break

    def imgNormalization(self, arr):
        arr = arr.astype('float')
        minVal = arr.min()
        maxVal = arr.max()
        maxLim = 2 ** 16
        if minVal != maxVal:
            arr -= minVal
            arr *= (maxLim / (maxVal - minVal))
        return arr.astype('uint16')



if __name__ == "__main__":
    cameraModel = AcquisitionModel()
    print(cameraModel.mmc.getImageHeight())
    #cameraModel.setROI(0, 0, 200, 100)
    #print(cameraModel.mmc.getImageHeight())
    #print(cameraModel.mmc.getProperty('Camera', 'OnCameraCCDXSize'))
    #cameraModel.snapImage()
    numImages = 10
    intervalMs = 1
    exposureTime = 10
    cameraModel.setNumImages(numImages)
    cameraModel.setExposureTime(exposureTime)
    cameraModel.startSequenceAcquisition()
    cameraModel.resetCore()



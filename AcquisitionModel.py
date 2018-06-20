# This python code uses MicroManager device drivers to control a camera.
# Tested on Hamamatsu Orca Flash 4 camera, it acquires a sequence of images and
# stores them in a folder. ROI will also be tested.
# Code implementation: David Sanchez

# code used to get an image sequence acquisition

# Importing necessary libraries
import sys
import MMCorePy  # load MicroManager for device control
import matplotlib.pyplot as plt
import time
from PIL import Image


class AcquisitionModel:

    def __init__(self):
        sys.path.append("C:\\Program Files\\Micro-Manager-1.4")
        # loading camera
        self.mmc = MMCorePy.CMMCore()
        self.mmc.getVersionInfo()
        # self.mmc.loadDevice('Camera', 'DemoCamera', 'DCam')
        # Hamamatsu
        self.mmc.loadDevice('Camera', 'HamamatsuHam', 'HamamatsuHam_DCAM')
        self.mmc.initializeAllDevices()
        self.mmc.setCameraDevice('Camera')
        self.mmc.setCircularBufferMemoryFootprint(2048)  # Buffer siwe is set to 1Gb acquisitions with mqny frames
        self.x = 0
        self.y = 0
        self.xSize = int(self.mmc.getImageWidth())
        self.ySize = int(self.mmc.getImageHeight())
        self.width = self.xSize  # ROI width
        self.height = self.ySize  # ROI height
        self.expTime = 1
        self.numImages = 1
        self.intervalMs = 1
        self.successfulAcquisition = False
        self.filename = "sequence.tiff"
        self.numAcquisitions = 0

    def setROI(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mmc.setROI(x, y, width, height)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height

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

    def isAcquisitionDone(self):
        return self.successfulAcquisition

    def startSequenceAcquisition(self):
        # Image sequence acquisition
        # Camerq is reloaded in case there are 2 or more consecutive acquisitions
        if self.numAcquisitions > 0:
            self.reloadCamera()
            self.setROI(self.x, self.y, self.width, self.height)

        self.successfulAcquisition = False
        print("Acquiring %d Images. Exposure time: %d ms" % (self.numImages, self.expTime))
        self.mmc.waitForDevice('Camera')
        self.mmc.prepareSequenceAcquisition('Camera')
        # self.mmc.initializeDevice('Camera')
        # self.mmc.setCameraDevice('Camera')
        start_time = time.time()
        self.mmc.prepareSequenceAcquisition('Camera')
        self.mmc.startSequenceAcquisition(self.numImages, self.intervalMs, False)  # 1 is stopOnOverflow parameter

        # self.waitAcquisition()
        imList = []
        # filename = "C:\\Users\\MOTIV\\Documents\\Python\\image%d.tiff" % (x,)
        # filename = "C:\\Users\\Administrateur\\Documents\\David\\image%d.tiff" % (x,)
        while True:
            if self.mmc.getRemainingImageCount() > 0:
                img = self.mmc.popNextImage()
                imList.append(Image.fromarray(img))
            elif not self.mmc.isSequenceRunning():
                if not self.successfulAcquisition:
                    self.successfulAcquisition = True
                    print("Acquisition finished after %s seconds" % (time.time() - start_time))
                if len(imList) == self.numImages:
                    imList[0].save(self.filename, compression="None", save_all=True,
                                   append_images=imList[1:])
                    print("File saved after %s seconds" % (time.time() - start_time))
                    break

        print("Remaining Images: %d" % self.mmc.getRemainingImageCount())
        self.mmc.waitForDevice('Camera')  # The program waits until the device is done with all its tasks
        self.numAcquisitions += 1

    def reloadCamera(self):
        self.mmc.unloadDevice('Camera')
        self.mmc.loadDevice('Camera', 'HamamatsuHam', 'HamamatsuHam_DCAM')
        self.mmc.initializeDevice('Camera')
        self.mmc.setCameraDevice('Camera')

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
    numImages = 2
    exposureTime = 10
    # print(cameraModel.getXSize())
    cameraModel.setROI(0, 0, 100, 100)
    cameraModel.setNumImages(numImages)
    cameraModel.setExposureTime(exposureTime)
    cameraModel.startSequenceAcquisition()
    cameraModel.filename = "sequence2.tiff"
    cameraModel.startSequenceAcquisition()
    cameraModel.resetCore()
    # cameraModel.startSequenceAcquisition()
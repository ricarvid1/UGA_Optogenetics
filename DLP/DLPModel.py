# -*- coding: utf-8 -*-
from PatternWindow import PatternWindow
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import pycrafter4500_Irene as pycrafter4500
import time

class DLPModel:


    def __init__(self, XSize, YSize):
        self.irradiationPeriod = 2000
        self.pulseDuration = 1000
        self.numPeriods = 1
        self.RGB = [104, 135, 130] # Default values obtained in the manual
        self.XSize = XSize
        self.YSize = YSize
        self.distX = self.XSize / 2
        self.distY = self.YSize / 2
        self.vertices = np.zeros((1, 2))
        self.activationDone = False
        self.stopFlag = False
        # secondary window used to show the pattern
        self.patternScreen = PatternWindow(self.XSize, self.YSize)
        # window is placed on the secondary desktop screen to be projected
        pDesktop = QApplication.desktop()
        RectScreen1 = pDesktop.screenGeometry(1)
        self.patternScreen.move(RectScreen1.left(), RectScreen1.top())
        self.patternScreen.resize(RectScreen1.width(), RectScreen1.height())
        # background of window is set to black
        palette = self.patternScreen.palette()
        palette.setColor(self.patternScreen.backgroundRole(), Qt.black)
        self.patternScreen.setPalette(palette)
        # pattern is shown
        self.patternScreen.showMaximized()
        self.dlp=pycrafter4500.dmd()
        OK = self.dlp.checkstatus1()
        self.dlp.checkstatus2()
        self.dlp.setVideoMode()
        self.dlp.controlLED(self.RGB)
        self.dlp.enableLEDs([0, 0, 0])
        self.DMDPoints = np.array([[self.XSize / 2, self.XSize / 2, self.YSize / 4, self.YSize * 3 / 4],
                                   [self.YSize / 4, self.YSize * 3 / 4, self.YSize / 2, self.YSize / 2]])
        self.thetaCam = 0
        self.rotation = np.array([[1, 0], [0, 1]])
        self.shiftCam = np.array([[0], [0]])
        self.magX = 1
        self.magY = 1
        self.mag = np.array([[self.magX], [self.magY]])
        #rotation and shift introduced in order to compensate the optics inversion
        #given by an odd number of converging lenses
        self.rotationOptics = np.array([[-1, 0], [0, -1]])
        self.shiftOptics = np.array([[self.XSize], [self.YSize]])
        #shift introduced to take points to the origin and demagnify them
        self.shiftCentering = np.array([[self.distX], [self.distY]])
        
    def setIrradiationPeriod(self, irradiationPeriod):
        self.irradiationPeriod = irradiationPeriod
    
    def getIrradiationPeriod(self):
        return self.irradiationPeriod   
    
    def setPulseDuration(self, pulseDuration):
        self.pulseDuration = pulseDuration
    
    def getPulseDuration(self):
        return self.pulseDuration
    
    def setNumPeriods(self, numPeriods):
        self.numPeriods = numPeriods
    
    def getNumPeriods(self):
        return self.numPeriods
    
    def setRGB(self, red, green, blue):
        self.RGB = [red, green, blue]
    
    def getRGB(self):
        return self.RGB

    def setVertices(self, vertices):
        self.vertices = vertices
    
    def getVertices(self):
        return self.vertices
    
    def setStopFlag(self, stopFlag):
        self.stopFlag = stopFlag
    
    def getStopFlag(self):
        return self.stopFlag

    def setPattern(self):
        self.patternScreen.reset()
        self.adjustVertices()
        self.patternScreen.getAxis().fill(self.vertices[:, 0], self.vertices[:, 1], "w")
        self.patternScreen.getCanvas().draw_idle()
        self.dlp.controlLED([0, 100, 100])
        self.dlp.enableLEDs([0, 1, 1])

    def resetPattern(self):
        self.patternScreen.reset()
        self.vertices = np.zeros((1, 2))
        
    def resetSecondaryScreen(self):
        self.patternScreen.reset()
        self.dlp.enableLEDs([0, 0, 0])
        
    def setStandby(self):
        self.dlp.standby()
            
    def setPowerUp(self):
        self.dlp.wakeup()
        
    # displays the calibration pattern
    def showCalibrationPattern1(self):
        self.patternScreen.showCalibrationPattern1()
        self.dlp.enableLEDs([0, 1, 1])
        
    # displays the calibration pattern
    def showCalibrationPattern2(self):
        self.patternScreen.showCalibrationPattern2()
        self.dlp.enableLEDs([0, 1, 1])
        
    def getCalibrationParameters(self, calibrationPoints):
        cameraPoints = np.transpose(calibrationPoints)
        mCamera = (cameraPoints[1, 1] - cameraPoints[1, 0]) / (cameraPoints[0, 1] - cameraPoints[0, 0])
        self.thetaCam = np.arctan(mCamera)
        print self.thetaCam * 180 / np.pi
    
        self.thetaCam = -1 * self.thetaCam
    
        self.rotation = np.array([[np.cos(self.thetaCam), -np.sin(self.thetaCam)], [np.sin(self.thetaCam), np.cos(self.thetaCam)]])
        rotatedPoints = np.matmul(self.rotation, cameraPoints)
        
        self.magX = (rotatedPoints[0, 1] - rotatedPoints[0, 0]) / self.distX
        self.magY = (rotatedPoints[1, 3] - rotatedPoints[1, 2]) / self.distY
        self.mag = np.array([[self.magX], [self.magY]])
        print self.mag
        scaledPoints = rotatedPoints / self.mag
    
        shift = scaledPoints - self.DMDPoints
        self.shiftCam = np.array([[shift[0, 0]], [shift[1, 0]]])
        print self.shiftCam
        
        #shiftedPoints = rotatedPoints - self.shiftCam
        
    def adjustVertices(self):
        newVertices = np.transpose(self.vertices)
        newVertices = np.matmul(self.rotation, newVertices)
        newVertices = newVertices - self.shiftCentering
        newVertices = newVertices / self.mag
        newVertices = newVertices + self.shiftCentering
        newVertices = newVertices - self.shiftCam
        newVertices = np.matmul(self.rotationOptics, newVertices)
        newVertices = newVertices + self.shiftOptics
        print newVertices
        self.vertices = np.transpose(newVertices)
        
    def isActivationDone(self):
        return self.activationDone

    def startActivation(self):
        darkTime = self.irradiationPeriod - self.pulseDuration
        self.dlp.enableLEDs([0, 0, 0])
        self.dlp.controlLED(self.RGB)
        time.sleep(0.5)
        for i in range(self.numPeriods):
            if self.stopFlag:
                break
            self.dlp.enableLEDs([0, 1, 1])
            time.sleep(self.pulseDuration * 0.001)
            self.dlp.enableLEDs([0, 0, 0])
            #self.resetPattern()
            time.sleep(darkTime * 0.001)
        self.activationDone = True    
    
if __name__ == '__main__':
    DLPController = DLPModel(2048, 2048)
 
    vertices = np.array([[0, 0], [0, 0], [500, 500], [0, 500]])
    DLPController.setVertices(vertices)
    DLPController.setRGB(0, 0, 130)
    DLPController.setPattern()
    print 'you can start your acquisition'
#    DLPController.startActivation()
#    DLPController.showCalibrationPattern2()
    #gray_image = color.rgb2gray(mplimage)
    #plt.figure()
    #plt.imshow(gray_image, cmap='gray')

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
import pycrafter4500
import time

class DLPModel:


    def __init__(self, XSize, YSize):
        self.irradiationPeriod = 2000
        self.pulseDuration = 1000
        self.numPeriods = 1
        self.RGB = [104, 135, 130] # Default values obtained in the manual
        self.XSize = XSize
        self.YSize = YSize
        self.vertices = np.zeros((1, 2))
        self.activationDone = False
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
        #pycrafter4500.software_reset()
        pycrafter4500.video_mode()
        pycrafter4500.stop_display()
        
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

    def setPattern(self):
        self.patternScreen.getAxis().fill(self.vertices[1:, 0], self.vertices[1:, 1], "w")
        self.patternScreen.getCanvas().draw_idle()

    def resetPattern(self):
        self.patternScreen.reset()
        self.vertices = np.zeros((1, 2))
        
    def setStandby(self):
        pycrafter4500.power_down()
            
    def setPowerUp(self):
        pycrafter4500.power_up()
        
    def isActivationDone(self):
        return self.activationDone

    def startActivation(self):
        darkTime = self.irradiationPeriod - self.pulseDuration
        for i in range(self.numPeriods):
            pycrafter4500.start_display(self.RGB)
            time.sleep(self.pulseDuration * 0.001)
            pycrafter4500.stop_display()
            #self.resetPattern()
            time.sleep(darkTime * 0.001)
        self.activationDone = True    
    
if __name__ == '__main__':
    dlp = DLPModel(2048, 2048)
    '''
    vertices = np.array([[0, 0], [0, 0], [500, 500], [0, 500]])
    dlp.setVertices(vertices)
    dlp.setPattern()
    print 'you can start your acquisition'
    #screen.startActivation()
    '''
    dlp.patternScreen.plot()
    pycrafter4500.start_display([104, 135, 130])
    canvas = dlp.patternScreen.figure.canvas
    #mplimage = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(2048, 2048, 3)
    #gray_image = color.rgb2gray(mplimage)
    #plt.figure()
    #plt.imshow(gray_image, cmap='gray')

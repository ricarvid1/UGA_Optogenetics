import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


class PatternWindow(QWidget):
    def __init__(self, XSize, YSize):
        super(PatternWindow, self).__init__()
        # this new window has no frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # create an axis with equal aspect ratio and also on the given position
        self.ax = self.figure.add_axes([0, 0, 1, 1])
        # discards the old graph
        self.ax.clear()
        # axis are removed to show the pattern
        #self.ax.axis('off')
        # both face color and background (patch) are set to black
        self.ax.set_facecolor('k')
        self.figure.patch.set_color('k')
        self.setXSize(XSize)
        self.setYSize(YSize)
        self.background = np.zeros((self.XSize, self.YSize))
        self.ax.imshow(self.background, cmap='gray')
        self.createCalibrationPattern()
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        #hlayout = QHBoxLayout()
        #hlayout.addLayout(layout)
        self.setLayout(layout)


    def setXSize(self, XSize):
        self.XSize = XSize

    def setYSize(self, YSize):
        self.YSize = YSize

    def getXSize(self):
        return self.XSize

    def getYSize(self):
        return self.YSize

    def getFigure(self):
        return self.figure

    def getCanvas(self):
        return self.canvas

    def getAxis(self):
        return self.ax
    
    # Creates the calibration pattern
    def createCalibrationPattern(self):
        # A pattern in plotted
        # A circle is plotted
        xCenter = self.XSize / 2
        yCenter = self.YSize / 4
        radius = 3
        self.calibrationPattern1 = self.background[:, (self.YSize / 2):]
        #'''
        for i in range(self.XSize):
            for j in range(self.YSize / 2):
                d = np.sqrt((i - xCenter)**2 + (j - yCenter)**2)
                if d <= radius:
                    self.calibrationPattern1[i, j] = 1
        #'''
        self.calibrationPattern1 = np.tile(self.calibrationPattern1, 2)
        self.calibrationPattern2 = np.rot90(self.calibrationPattern1)

        
    # displays the calibration pattern
    def showCalibrationPattern1(self):
        # data (matrix) is displayed like an image
        self.ax.clear()
        self.ax.imshow(self.calibrationPattern1, cmap='gray')
        # refresh canvas
        self.canvas.draw_idle()
#        plt.figure()
#        plt.imshow(self.calibrationPattern1, cmap='gray')
        
    # displays the calibration pattern
    def showCalibrationPattern2(self):
        # data (matrix) is displayed like an image
        self.ax.clear()
        self.ax.imshow(self.calibrationPattern2, cmap='gray')
        # refresh canvas
        self.canvas.draw_idle()
#        plt.figure()
#        plt.imshow(self.calibrationPattern2, cmap='gray')

    # Generates a circle pattern and plots it on the window
    def plot(self):
        # A pattern in plotted
        # A circle is plotted
        xCenter = self.XSize / 2
        yCenter = self.YSize / 2
        radius = 3
        circle = self.background
        '''
        for i in range(self.XSize):
            for j in range(self.YSize):
                if i == xCenter and j == yCenter:
                    circle[i, j] = 1
        '''
        #'''
        for i in range(self.XSize):
            for j in range(self.YSize):
                d = np.sqrt((i - xCenter)**2 + (j - yCenter)**2)
                if d <= radius:
                    circle[i, j] = 1
        #'''
        # data (matrix) is displayed like an image
        self.ax.imshow(circle, cmap='gray')
        # refresh canvas
        self.canvas.draw_idle()
        #plt.figure()
        #plt.imshow(circle, cmap='gray')

    # Resets the pattern on the window to a black screen
    def reset(self):
        self.background = np.zeros((self.XSize, self.YSize))
        self.ax.clear()
        self.ax.imshow(self.background, cmap='gray')
        self.canvas.draw_idle()

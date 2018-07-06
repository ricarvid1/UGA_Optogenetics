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
        self.irradiation = 0
        self.irradiationPeriod = 2000
        self.pulseDuration = 1000
        self.intensity = 131
        self.XSize = XSize
        self.YSize = YSize
        self.vertices = np.zeros((1, 2))
        self.exposureDone = False
        self.numPeriods = 5
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


    def setVertices(self, vertices):
        self.vertices = vertices

    def setPattern(self):
        self.patternScreen.getAxis().fill(self.vertices[1:, 0], self.vertices[1:, 1], "w")
        self.patternScreen.getCanvas().draw_idle()

    def resetPattern(self):
        self.patternScreen.reset()
        self.vertices = np.zeros((1, 2))

    def startActivation(self):
        darkTime = self.irradiationPeriod - self.pulseDuration
        self.setPattern()
        for i in range(self.numPeriods):
            pycrafter4500.start_display([self.intensity, self.intensity, self.intensity])
            time.sleep(1)
            pycrafter4500.stop_display()
            self.resetPattern()
            time.sleep(1)
        self.exposureDone = True
        return self.exposureDone
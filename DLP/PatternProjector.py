import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

import random


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent

        # Just some button connected to `plot` method
        self.plot()
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        hlayout = QHBoxLayout()
        #hlayout.addStretch()
        hlayout.addLayout(layout)
        #hlayout.addStretch()
        self.setLayout(hlayout)

    def plot(self):
        ''' plot some random stuff '''
        #data = [random.random() for i in range(10)]
        xSize = 1024
        xCenter = xSize / 2
        ySize = 1024
        yCenter = ySize / 2
        radius = 256
        data = np.zeros((xSize, ySize))
        for i in range(xSize):
            for j in range(ySize):
                d = np.sqrt((i - xCenter)**2 + (j - yCenter)**2)
                if d < radius:
                    data[i, j] = 1

        # create an axis
        #ax = self.figure.add_subplot(111)
        ax = self.figure.add_axes([0., 0., 1., 1.], aspect='equal')

        # discards the old graph
        ax.clear()

        # plot data
        ax.imshow(data, cmap='gray')
        #ax.plot(data)
        ax.axis('off')
        ax.set_facecolor('k')
        self.figure.patch.set_color('k')
        print(ax.get_facecolor())
        '''
        fig = plt.figure()
        ax = plt.axes([0, 0, 1, 1])
        plt.imshow(data, interpolation="nearest")
        plt.axis("off")
        '''
        # refresh canvas
        self.canvas.draw_idle()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    pDesktop = QApplication.desktop()
    RectScreen1 = pDesktop.screenGeometry(1)
    main.move(RectScreen1.left(), RectScreen1.top())
    main.resize(RectScreen1.width(), RectScreen1.height())
    palette = main.palette()
    palette.setColor(main.backgroundRole(), Qt.black)
    main.setPalette(palette)

    main.showMaximized()

    win2 = Window()
    win2.setGeometry(100, 100, 100, 100)
    win2.setWindowTitle('Control test window')


    sys.exit(app.exec_())
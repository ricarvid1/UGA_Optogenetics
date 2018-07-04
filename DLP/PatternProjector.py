import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import PatternWindow

'''
class PatternWindow(QWidget):
    def __init__(self, parent=None):
        super(PatternWindow, self).__init__(parent)
        # this new window has no frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # create an axis with equal aspect ratio and also on the given position
        self.ax = self.figure.add_subplot(111)
        # discards the old graph
        self.ax.clear()
        # axis are removed to show the pattern
        self.ax.axis('off')
        # both face color and background (patch) are set to black
        self.ax.set_facecolor('k')
        self.figure.patch.set_color('k')
        xSize = 1024
        ySize = 1024
        data = np.ones((xSize, ySize))
        self.ax.imshow(data, cmap='gray')

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        hlayout = QHBoxLayout()
        hlayout.addLayout(layout)
        self.setLayout(hlayout)

    # Generates the desired pattern and plots it on the secondary window
    def plot(self):
        # A pattern in plotted
        # A circle is plotted
        xSize = 1024
        xCenter = xSize / 2
        ySize = 1024
        yCenter = ySize / 2
        radius = 256
        self.data = np.zeros((xSize, ySize))
        for i in range(xSize):
            for j in range(ySize):
                d = np.sqrt((i - xCenter)**2 + (j - yCenter)**2)
                if d < radius:
                    self.data[i, j] = 1

        # data (matrix) is displayed like an image
        self.ax.imshow(self.data, cmap='gray')
        # refresh canvas
        self.canvas.draw_idle()

    # Resets the pattern on the secondary window to a black screen
    def reset(self):
        xSize = 1024
        ySize = 1024
        radius = 256
        data = np.zeros((xSize, ySize))

        # plot data
        self.ax.imshow(data, cmap='gray')
        self.canvas.draw_idle()
'''
'''
class PatternCreator:

    def __init__(self):


    def onclick(self, event):
        if event.inaxes == self.ax_control:
            print('%s click: button=%d, x=%i, y=%i, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            coordinates = np.array([[event.xdata, event.ydata]])
            self.vertices = np.append(self.vertices, coordinates, axis=0)
            print self.vertices

    def fill(self):
        self.patternScreen.ax.fill(self.vertices[1:, 0], self.vertices[1:, 1], "w")
'''

# Controller window used for testing purposes
class smallWindow(QMainWindow):
    def __init__(self, parent=None):
        # init and geometry settings
        super(smallWindow, self).__init__(parent)
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Control test window')
        # controlling test buttons
        self.button = QPushButton("Set Pattern ")
        self.button.clicked.connect(self.plot)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset)

        self.btn_fill = QPushButton("Fill")
        self.btn_fill.clicked.connect(self.fill)
        # central widget is created
        self.center = QWidget()
        self.setCentralWidget(self.center)

        xSize = 1024
        ySize = 1024
        self.vertices = np.zeros((1, 2))
        data = np.ones((xSize, ySize))

        # secondary window used to show the pattern
        self.patternScreen = PatternWindow()
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

        fig_control = Figure()
        self.canvas = FigureCanvas(fig_control)
        self.ax_control = fig_control.add_subplot(1, 1, 1)

        self.ax_control.imshow(data, cmap='gray')
        self.canvas.draw_idle()

        cid = self.canvas.mpl_connect('button_press_event', self.onclick)

        # set layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.button)
        vbox.addWidget(self.btn_reset)
        vbox.addWidget(self.btn_fill)
        self.center.setLayout(vbox)

    def onclick(self, event):
        if event.inaxes == self.ax_control:
            print('%s click: button=%d, x=%i, y=%i, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            coordinates = np.array([[event.xdata, event.ydata]])
            self.vertices = np.append(self.vertices, coordinates, axis=0)
            print self.vertices

    def fill(self):
        self.patternScreen.ax.fill(self.vertices[1:, 0], self.vertices[1:, 1], "w")
        self.patternScreen.canvas.draw_idle()
        self.ax_control.fill(self.vertices[1:, 0], self.vertices[1:, 1], "w")
        self.canvas.draw_idle()

    def plot(self):
        self.patternScreen.plot()

    def reset(self):
        self.patternScreen.reset()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win2 = smallWindow()
    win2.show()
    sys.exit(app.exec_())

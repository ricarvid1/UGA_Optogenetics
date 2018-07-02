import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt



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
        self.ax = self.figure.add_axes([0., 0., 1., 1.], aspect='equal')
        # discards the old graph
        self.ax.clear()
        # axis are removed to show the pattern
        self.ax.axis('off')
        # both face color and background (patch) are set to black
        self.ax.set_facecolor('k')
        self.figure.patch.set_color('k')

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
        xCenter = xSize / 2
        ySize = 1024
        yCenter = ySize / 2
        radius = 256
        data = np.zeros((xSize, ySize))

        # plot data
        self.ax.imshow(data, cmap='gray')
        self.canvas.draw_idle()

# Controller window used for testing purposes
class smallWindow(QMainWindow):
    def __init__(self, parent=None):
        # init and geometry settings
        super(smallWindow, self).__init__(parent)
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('Control test window')
        # secondary window used to show the pattern
        self.pattern = PatternWindow()
        # window is placed on the secondary desktop screen to be projected
        pDesktop = QApplication.desktop()
        RectScreen1 = pDesktop.screenGeometry(1)
        self.pattern.move(RectScreen1.left(), RectScreen1.top())
        self.pattern.resize(RectScreen1.width(), RectScreen1.height())
        # background of window is set to black
        palette = self.pattern.palette()
        palette.setColor(self.main.backgroundRole(), Qt.black)
        self.pattern.setPalette(palette)
        # pattern is shown
        self.pattern.showMaximized()
        # controlling test buttons
        self.button = QPushButton("Set Pattern ")
        self.button.clicked.connect(self.plot)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset)
        # central widget is created
        self.center = QWidget()
        self.setCentralWidget(self.center)
        # set layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.btn_reset)
        self.center.setLayout(vbox)

    def plot(self):
        self.main.plot()

    def reset(self):
        self.main.reset()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win2 = smallWindow()
    win2.show()
    sys.exit(app.exec_())

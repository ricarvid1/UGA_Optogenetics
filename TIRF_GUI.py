import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from AcquisitionModel import AcquisitionModel
from DLP.PatternWindow import PatternWindow


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 200, 900, 650)
        self.setWindowTitle('TIRF Experiment Manager')
        self.setWindowIcon(QIcon('logo_LIPhy.png'))
        self.cameraModel = AcquisitionModel()
        self.home()

    def home(self):
        # central widget is created
        self.central = QWidget()
        self.setCentralWidget(self.central)
        # Left Section
        # Left boxes are added here
        vbox_main = QVBoxLayout()

        # Adding elements to the left main box
        vbox_main.addStretch()
        vbox_main.addWidget(self.setCamHome())
        vbox_main.addStretch()
        vbox_main.addWidget(self.setROIHome())
        vbox_main.addStretch()
        vbox_main.addWidget(self.setDMDHome())
        vbox_main.addStretch()

        # Right main Section
        #Main right VBox
        vbox_main_exp = QVBoxLayout()
        vbox_main_exp.addWidget(self.setGraphHome())
        vbox_main_exp.addStretch()
        vbox_main_exp.addWidget(self.setExpHome())

        # Secondary window
        self.setPatternWindow()

        #Main HBOX containing all subelements
        hbox_main = QHBoxLayout()
        hbox_main.addLayout(vbox_main)
        hbox_main.addStretch()
        hbox_main.addLayout(vbox_main_exp)
        self.central.setLayout(hbox_main)
        # Showing all the graphs
        self.show()

    def setCamHome(self):
        # Camera section is added using the grid option
        # Labels
        # lbl_cam = QLabel("Camera")
        lbl_cam_exp = QLabel("Exposure Time")
        lbl_cam_ms = QLabel("ms")
        lbl_cam_num = QLabel("Number of Im. ")
        # Edit lines
        self.exposureTime = 10
        self.edt_cam_exp = QLineEdit()
        self.edt_cam_exp.setValidator(QIntValidator())
        self.edt_cam_exp.setAlignment(Qt.AlignRight)
        self.edt_cam_exp.setMaxLength(4)
        self.edt_cam_exp.setText(str(self.exposureTime))
        self.numImages = 1
        self.edt_cam_num = QLineEdit()
        self.edt_cam_num.setValidator(QIntValidator())
        self.edt_cam_num.setAlignment(Qt.AlignRight)
        self.edt_cam_num.setMaxLength(4)
        self.edt_cam_num.setText(str(self.numImages))
        # Buttons
        self.btn_cam_snap = QPushButton("Capture Image")
        self.btn_cam_acq = QPushButton("Acquire")
        self.btn_cam_snap.clicked.connect(self.captureImage)
        self.btn_cam_acq.clicked.connect(self.startSequenceAcquisition)
        # grid
        grid_cam = QGridLayout()
        # grid_cam.addWidget(lbl_cam, 0, 0, 1, 1)
        grid_cam.addWidget(lbl_cam_exp, 1, 0, 1, 1)
        grid_cam.addWidget(self.edt_cam_exp, 1, 1, 1, 1)
        grid_cam.addWidget(lbl_cam_ms, 1, 2, 1, 1)
        grid_cam.addWidget(self.btn_cam_snap, 2, 0, 1, 2)
        grid_cam.addWidget(lbl_cam_num, 3, 0, 1, 1)
        grid_cam.addWidget(self.edt_cam_num, 3, 1, 1, 1)
        grid_cam.addWidget(self.btn_cam_acq, 4, 0, 1, 2)
        # GroupBox
        group_cam = QGroupBox("Camera")
        group_cam.setLayout(grid_cam)
        return group_cam

    def setROIHome(self):
        # Camera section is added using the grid option
        # Labels
        # lbl_cam = QLabel("Camera")
        lbl_roi_x = QLabel("X Coordinate")
        lbl_roi_y = QLabel("Y Coordinate")
        lbl_roi_width = QLabel("ROI Width")
        lbl_roi_height = QLabel("ROI Height")
        # Edit lines
        self.XSize = self.cameraModel.getXSize()    # Original size of camera's image (without ROI)
        self.YSize = self.cameraModel.getYSize()    # Original size of camera's image (without ROI)
        self.edt_roi_x = QLineEdit()
        self.edt_roi_x.setValidator(QIntValidator(0, self.XSize))
        self.edt_roi_x.setAlignment(Qt.AlignRight)
        self.edt_roi_x.setMaxLength(4)
        self.edt_roi_x.setText('0')
        self.edt_roi_y = QLineEdit()
        self.edt_roi_y.setValidator(QIntValidator(0, self.YSize))
        self.edt_roi_y.setAlignment(Qt.AlignRight)
        self.edt_roi_y.setMaxLength(4)
        self.edt_roi_y.setText('0')
        self.edt_roi_width = QLineEdit()
        self.edt_roi_width.setValidator(QIntValidator(0, self.XSize))
        self.edt_roi_width.setAlignment(Qt.AlignRight)
        self.edt_roi_width.setMaxLength(4)
        self.edt_roi_width.setText(str(self.XSize))
        self.edt_roi_height = QLineEdit()
        self.edt_roi_height.setValidator(QIntValidator(0, self.YSize))
        self.edt_roi_height.setAlignment(Qt.AlignRight)
        self.edt_roi_height.setMaxLength(4)
        self.edt_roi_height.setText(str(self.YSize))
        # Buttons
        self.btn_roi_set = QPushButton("Set Acquisition ROI")
        self.btn_roi_set.clicked.connect(self.setROIAcquisition)
        self.btn_roi_reset = QPushButton("Reset")
        self.btn_roi_reset.clicked.connect(self.resetROIAcquisition)
        # Form layout
        flo_roi = QFormLayout()
        flo_roi.addRow(lbl_roi_x, self.edt_roi_x)
        flo_roi.addRow(lbl_roi_y, self.edt_roi_y)
        flo_roi.addRow(lbl_roi_width, self.edt_roi_width)
        flo_roi.addRow(lbl_roi_height, self.edt_roi_height)
        # Vertical box
        vbox_roi = QVBoxLayout()
        vbox_roi.addLayout(flo_roi)
        vbox_roi.addWidget(self.btn_roi_set)
        vbox_roi.addWidget(self.btn_roi_reset)
        # GroupBox
        group_roi = QGroupBox("ROI")
        group_roi.setLayout(vbox_roi)
        return group_roi

    def setDMDHome(self):
        # DMD section is added using the form option
        # Labels
        # lbl_dmd = QLabel("DMD")
        lbl_dmd_irr = QLabel("Irradiation")
        lbl_dmd_iper = QLabel("Irradiation Period")
        lbl_dmd_pulse = QLabel("Pulse Duration")
        lbl_dmd_led = QLabel("LED Intensity")
        # Edit lines
        self.edt_dmd_irr = QLineEdit()
        self.edt_dmd_irr.setValidator(QIntValidator())
        self.edt_dmd_irr.setAlignment(Qt.AlignRight)
        self.edt_dmd_irr.setMaxLength(3)
        self.edt_dmd_irr.setText('0')
        self.edt_dmd_iper = QLineEdit()
        self.edt_dmd_iper.setValidator(QIntValidator())
        self.edt_dmd_iper.setAlignment(Qt.AlignRight)
        self.edt_dmd_iper.setMaxLength(3)
        self.edt_dmd_iper.setText('0')
        self.edt_dmd_pulse = QLineEdit()
        self.edt_dmd_pulse.setValidator(QIntValidator())
        self.edt_dmd_pulse.setAlignment(Qt.AlignRight)
        self.edt_dmd_pulse.setMaxLength(3)
        self.edt_dmd_pulse.setText('0')
        self.edt_dmd_led = QLineEdit()
        self.edt_dmd_led.setValidator(QIntValidator())
        self.edt_dmd_led.setAlignment(Qt.AlignRight)
        self.edt_dmd_led.setMaxLength(3)
        self.edt_dmd_led.setText('0')
        # Buttons
        self.btn_dmd_roi = QPushButton("Set Activation ROI")
        self.btn_dmd_roi.clicked.connect(self.fillPattern)
        self.btn_dmd_reset = QPushButton("Reset Activation ROI")
        self.btn_dmd_reset.clicked.connect(self.resetPattern)
        # Form layout
        flo_dmd = QFormLayout()
        flo_dmd.addRow(lbl_dmd_irr, self.edt_dmd_irr)
        flo_dmd.addRow(lbl_dmd_iper, self.edt_dmd_iper)
        flo_dmd.addRow(lbl_dmd_pulse, self.edt_dmd_pulse)
        flo_dmd.addRow(lbl_dmd_led, self.edt_dmd_led)
        # Vertical box
        vbox_dmd = QVBoxLayout()
        vbox_dmd.addWidget(self.btn_dmd_roi)
        vbox_dmd.addWidget(self.btn_dmd_reset)
        vbox_dmd.addLayout(flo_dmd)
        # GroupBox
        group_dmd = QGroupBox("DMD")
        group_dmd.setLayout(vbox_dmd)
        return group_dmd

    def setExpHome(self):
        # Optogenetic Experiment section
        # Labels
        # lbl_exp = QLabel("Optogenetic Experiment")
        lbl_exp_pre_seq = QLabel("Preactivation Sequence")
        lbl_exp_pre_num = QLabel("Nb. Im.")
        lbl_exp_pre_exp = QLabel("Exposure")
        lbl_exp_act = QLabel("Activation")
        lbl_exp_pos_seq = QLabel("Preactivation Sequence")
        lbl_exp_pos_num = QLabel("Nb. Im.")
        lbl_exp_pos_exp = QLabel("Exposure")
        # Checkboxes
        self.chck_exp_pre_seq = QCheckBox()
        self.chck_exp_pre_num = QCheckBox()
        self.chck_exp_pre_exp = QCheckBox()
        self.chck_exp_act = QCheckBox()
        self.chck_exp_pos_seq = QCheckBox()
        self.chck_exp_pos_num = QCheckBox()
        self.chck_exp_pos_exp = QCheckBox()
        # Buttons
        self.btn_exp_start = QPushButton("Launch")
        self.btn_exp_stop = QPushButton("Stop")
        # Hboxes EXP
        hbox_exp_pre = QHBoxLayout()
        hbox_exp_pos = QHBoxLayout()
        hbox_exp_act = QHBoxLayout()
        # Vboxes EXP
        vbox_exp = QVBoxLayout()
        # Setting horizontal boxes
        hbox_exp_pre.addWidget(lbl_exp_pre_seq)
        hbox_exp_pre.addWidget(self.chck_exp_pre_seq)
        hbox_exp_pre.addWidget(lbl_exp_pre_num)
        hbox_exp_pre.addWidget(self.chck_exp_pre_num)
        hbox_exp_pre.addWidget(lbl_exp_pre_exp)
        hbox_exp_pre.addWidget(self.chck_exp_pre_exp)

        hbox_exp_act.addWidget(lbl_exp_act)
        hbox_exp_act.addWidget(self.chck_exp_act)
        hbox_exp_act.addStretch()

        hbox_exp_pos.addWidget(lbl_exp_pos_seq)
        hbox_exp_pos.addWidget(self.chck_exp_pos_seq)
        hbox_exp_pos.addWidget(lbl_exp_pos_num)
        hbox_exp_pos.addWidget(self.chck_exp_pos_num)
        hbox_exp_pos.addWidget(lbl_exp_pos_exp)
        hbox_exp_pos.addWidget(self.chck_exp_pos_exp)
        # Setting vertical box
        vbox_exp.addStretch()
        # vbox_exp.addWidget(lbl_exp)
        vbox_exp.addWidget(self.btn_exp_start)
        vbox_exp.addWidget(self.btn_exp_stop)
        vbox_exp.addLayout(hbox_exp_pre)
        vbox_exp.addLayout(hbox_exp_act)
        vbox_exp.addLayout(hbox_exp_pos)
        # Groupbox
        group_exp = QGroupBox("Optogenetic Experiment")
        group_exp.setLayout(vbox_exp)
        return group_exp

    def setGraphHome(self):
        # Graph section to be located on top of the EXP section
        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.graph = FigureCanvas(fig)
        self.captureImage()
        # Setting event handling
        cid_dmd_region = self.graph.mpl_connect('button_press_event', self.onclick)
        # Navigation widget
        # it takes the Canvas widget and a parent
        toolbar = NavigationToolbar(self.graph, self)
        # Graph Vbox
        vbox_graph = QVBoxLayout()
        vbox_graph.addWidget(toolbar)
        vbox_graph.addWidget(self.graph)
        # Groupbox
        group_graph = QGroupBox("Image Display")
        group_graph.setLayout(vbox_graph)
        return group_graph

    def setPatternWindow(self):
        self.vertices = np.zeros((1, 2))

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

    def snapImage(self):
        self.cameraModel.snapImage()
        self.img = self.cameraModel.getImage()

    def displayImage(self):
        self.ax.clear()
        self.ax.imshow(self.img, cmap='gray')
        self.graph.draw_idle()

    # Captures an image with the desired exposure Time and displays it
    def captureImage(self):
        self.exposureTime = int(self.edt_cam_exp.text())
        self.cameraModel.setExposureTime(self.exposureTime)
        self.snapImage()
        self.displayImage()

    # Fills the selected area in the secondary window
    def fillPattern(self):
        self.patternScreen.getAxis().fill(self.vertices[1:, 0], self.vertices[1:, 1], "w")
        self.patternScreen.getCanvas().draw_idle()

    # Fills the selected area in the secondary window
    def resetPattern(self):
        self.vertices = np.zeros((1, 2))
        self.patternScreen.reset()
        self.captureImage()

    # Testing event handling
    def onclick(self, event):
        if event.inaxes == self.ax:
            coordinates = np.array([[event.xdata, event.ydata]])
            self.vertices = np.append(self.vertices, coordinates, axis=0)
            self.ax.scatter(self.vertices[1:, 0], self.vertices[1:, 1], color='red', marker='o')
            self.graph.draw_idle()

    # Interface Controller methods start here
    # Retrieves values from GUI and start the sequence acquisition
    def startSequenceAcquisition(self):
        self.exposureTime = int(self.edt_cam_exp.text())
        self.numImages = int(self.edt_cam_num.text())
        self.cameraModel.setExposureTime(self.exposureTime)
        self.cameraModel.setNumImages(self.numImages)
        self.cameraModel.startSequenceAcquisition()
        if self.cameraModel.isAcquisitionDone():
            self.successfulAcquisition()
        #self.cameraModel.resetCore()

    # Displays a pop-up indicating that the acquisition was successful
    def successfulAcquisition(self):
        choice = QMessageBox.information(self, 'Successful Acquisition',
                                         "Your file has been saved correctly",
                                         QMessageBox.Ok, QMessageBox.Ok)

    # Retrieves the values from GUI and sets a new ROI
    def setROIAcquisition(self):
        x = int(self.edt_roi_x.text())
        y = int(self.edt_roi_y.text())
        width = int(self.edt_roi_width.text())
        if (x + width) > self.XSize:
            width = self.XSize - x
            self.edt_roi_width.setText(str(width))
        height = int(self.edt_roi_height.text())
        if (y + height) > self.YSize:
            height = self.YSize - y
        self.edt_roi_height.setText(str(height))
        self.cameraModel.setROI(x, y, width, height)
        self.captureImage()

    # Retrieves the values from GUI and sets a new ROI
    def resetROIAcquisition(self):
        self.edt_roi_x.setText('0')
        self.cameraModel.setX(0)
        self.edt_roi_y.setText('0')
        self.cameraModel.setY(0)
        self.edt_roi_width.setText(str(self.XSize))
        self.cameraModel.setWidth(self.XSize)
        self.edt_roi_height.setText(str(self.YSize))
        self.cameraModel.setHeight(self.YSize)
        self.cameraModel.mmc.clearROI()
        self.captureImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


class window(QWidget):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(100, 200, 750, 550)
        self.setWindowTitle('TIRF')
        # self.setWindowIcon(QIcon('pic.png'))
        self.home()

    def home(self):

        # Left boxes are added here
        vbox_main = QVBoxLayout()

        # Camera section is added using the grid option
        # Labels
        #lbl_cam = QLabel("Camera")
        lbl_cam_exp = QLabel("Exposure Time")
        lbl_cam_ms = QLabel("ms")
        lbl_cam_num = QLabel("Number of Im. ")
        # Edit lines
        edt_cam_exp = QLineEdit()
        edt_cam_exp.setValidator(QIntValidator())
        edt_cam_exp.setAlignment(Qt.AlignRight)
        edt_cam_exp.setMaxLength(4)
        edt_cam_exp.resize(10, 50)
        edt_cam_num = QLineEdit()
        edt_cam_num.setValidator(QIntValidator())
        edt_cam_num.setAlignment(Qt.AlignRight)
        edt_cam_num.setMaxLength(4)
        # Buttons
        btn_cam_roi = QPushButton("Select ROI")
        btn_cam_acq = QPushButton("Acquire")
        # grid
        grid_cam = QGridLayout()
        #grid_cam.addWidget(lbl_cam, 0, 0, 1, 1)
        grid_cam.addWidget(lbl_cam_exp, 1, 0, 1, 1)
        grid_cam.addWidget(edt_cam_exp, 1, 1, 1, 1)
        grid_cam.addWidget(lbl_cam_ms, 1, 2, 1, 1)
        grid_cam.addWidget(btn_cam_roi, 2, 0, 1, 2)
        grid_cam.addWidget(lbl_cam_num, 3, 0, 1, 1)
        grid_cam.addWidget(edt_cam_num, 3, 1, 1, 1)
        grid_cam.addWidget(btn_cam_acq, 4, 0, 1, 2)
        # GroupBox
        group_cam = QGroupBox("Camera")
        group_cam.setLayout(grid_cam)

        # DMD section is added using the form option
        # Labels
        #lbl_dmd = QLabel("DMD")
        lbl_dmd_irr = QLabel("Irradiation")
        lbl_dmd_iper = QLabel("Irradiation Period")
        lbl_dmd_pulse = QLabel("Pulse Duration")
        lbl_dmd_led = QLabel("LED Intensity")
        # Edit lines
        edt_dmd_irr = QLineEdit()
        edt_dmd_irr.setValidator(QIntValidator())
        edt_dmd_irr.setAlignment(Qt.AlignRight)
        edt_dmd_irr.setMaxLength(3)
        edt_dmd_iper = QLineEdit()
        edt_dmd_iper.setValidator(QIntValidator())
        edt_dmd_iper.setAlignment(Qt.AlignRight)
        edt_dmd_iper.setMaxLength(3)
        edt_dmd_pulse = QLineEdit()
        edt_dmd_pulse.setValidator(QIntValidator())
        edt_dmd_pulse.setAlignment(Qt.AlignRight)
        edt_dmd_pulse.setMaxLength(3)
        edt_dmd_led = QLineEdit()
        edt_dmd_led.setValidator(QIntValidator())
        edt_dmd_led.setAlignment(Qt.AlignRight)
        edt_dmd_led.setMaxLength(3)
        # Buttons
        btn_dmd_roi = QPushButton("Set Activation ROI")
        # Form layout
        flo_dmd = QFormLayout()
        flo_dmd.addRow(lbl_dmd_irr, edt_dmd_irr)
        flo_dmd.addRow(lbl_dmd_iper, edt_dmd_iper)
        flo_dmd.addRow(lbl_dmd_pulse, edt_dmd_pulse)
        flo_dmd.addRow(lbl_dmd_led, edt_dmd_led)
        # Vertical box
        vbox_dmd = QVBoxLayout()
        vbox_dmd.addWidget(btn_dmd_roi)
        vbox_dmd.addLayout(flo_dmd)
        # GroupBox
        group_dmd = QGroupBox("DMD")
        group_dmd.setLayout(vbox_dmd)

        # Adding elements to the left main box
        vbox_main.addStretch()
        vbox_main.addWidget(group_cam)
        vbox_main.addStretch()
        vbox_main.addWidget(group_dmd)
        vbox_main.addStretch()

        # Right main box
        # Optogenetic Experiment section
        # Labels
        #lbl_exp = QLabel("Optogenetic Experiment")
        lbl_exp_pre_seq = QLabel("Preactivation Sequence")
        lbl_exp_pre_num = QLabel("Nb. Im.")
        lbl_exp_pre_exp = QLabel("Exposure")
        lbl_exp_act = QLabel("Activation")
        lbl_exp_pos_seq = QLabel("Preactivation Sequence")
        lbl_exp_pos_num = QLabel("Nb. Im.")
        lbl_exp_pos_exp = QLabel("Exposure")
        # Checkboxes
        chck_exp_pre_seq = QCheckBox()
        chck_exp_pre_num = QCheckBox()
        chck_exp_pre_exp = QCheckBox()
        chck_exp_act = QCheckBox()
        chck_exp_pos_seq = QCheckBox()
        chck_exp_pos_num = QCheckBox()
        chck_exp_pos_exp = QCheckBox()
        # Buttons
        btn_exp_start = QPushButton("Launch")
        btn_exp_stop = QPushButton("Stop")
        # Hboxes EXP
        hbox_exp_pre = QHBoxLayout()
        hbox_exp_pos = QHBoxLayout()
        hbox_exp_act = QHBoxLayout()
        # Vboxes EXP
        vbox_exp = QVBoxLayout()
        # Setting horizontal boxes
        hbox_exp_pre.addWidget(lbl_exp_pre_seq)
        hbox_exp_pre.addWidget(chck_exp_pre_seq)
        hbox_exp_pre.addWidget(lbl_exp_pre_num)
        hbox_exp_pre.addWidget(chck_exp_pre_num)
        hbox_exp_pre.addWidget(lbl_exp_pre_exp)
        hbox_exp_pre.addWidget(chck_exp_pre_exp)

        hbox_exp_act.addWidget(lbl_exp_act)
        hbox_exp_act.addWidget(chck_exp_act)
        hbox_exp_act.addStretch()

        hbox_exp_pos.addWidget(lbl_exp_pos_seq)
        hbox_exp_pos.addWidget(chck_exp_pos_seq)
        hbox_exp_pos.addWidget(lbl_exp_pos_num)
        hbox_exp_pos.addWidget(chck_exp_pos_num)
        hbox_exp_pos.addWidget(lbl_exp_pos_exp)
        hbox_exp_pos.addWidget(chck_exp_pos_exp)
        # Setting vertical box
        vbox_exp.addStretch()
        #vbox_exp.addWidget(lbl_exp)
        vbox_exp.addWidget(btn_exp_start)
        vbox_exp.addWidget(btn_exp_stop)
        vbox_exp.addLayout(hbox_exp_pre)
        vbox_exp.addLayout(hbox_exp_act)
        vbox_exp.addLayout(hbox_exp_pos)
        # Groupbox
        group_exp = QGroupBox("Optogenetic Experiment")
        group_exp.setLayout(vbox_exp)

        # Graph section to be located on top of the EXP section
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.clear()
        ax.plot(x, y, 'bo-')
        graph = FigureCanvas(fig)
        # Navigation widget
        # it takes the Canvas widget and a parent
        toolbar = NavigationToolbar(graph, self)
        # Graph Vbox
        vbox_graph = QVBoxLayout()
        vbox_graph.addWidget(toolbar)
        vbox_graph.addWidget(graph)
        # Groupbox
        group_graph = QGroupBox("Image Display")
        group_graph.setLayout(vbox_graph)
        #Main right VBox
        vbox_main_exp = QVBoxLayout()
        vbox_main_exp.addWidget(group_graph)
        vbox_main_exp.addStretch()
        vbox_main_exp.addWidget(group_exp)

        #Main HBOX containing all subelements
        hbox_main = QHBoxLayout()
        hbox_main.addLayout(vbox_main)
        hbox_main.addStretch()
        hbox_main.addLayout(vbox_main_exp)
        self.setLayout(hbox_main)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = np.linspace(1, 5, num=60, endpoint=True)
    y = np.sin(2 * np.pi * x)
    GUI = window()
    sys.exit(app.exec_())
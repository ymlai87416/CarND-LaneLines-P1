#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QDir, Qt, QUrl, QRegExp
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFileDialog, QMainWindow,
                             QTextEdit, QGridLayout, QApplication, QCheckBox, QGridLayout, QFormLayout,
                             QRadioButton, QTabWidget, QAction, QButtonGroup, QPushButton, QSlider, QStyle,
                             QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from app.app import Application
from app.app import (parseListTuple3, parseListOfPoint, formatListTuple)
import traceback

class ColorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.color_button_group = QButtonGroup()

        self.no_filter = QRadioButton('No color filtering', self)

        self.hsv_filter = QRadioButton('HSV color filtering', self)

        self.color_button_group.addButton(self.no_filter, 0)
        self.color_button_group.addButton(self.hsv_filter, 1)
        self.no_filter.toggled.connect(self.radio_button_click)
        self.hsv_filter.toggled.connect(self.radio_button_click)

        lbl_hsv_low = QLabel('HSV low threshold')
        self.txt_hsv_low = QLineEdit()
        self.txt_hsv_low.editingFinished.connect(self.txt_hsv_low_changed)
        lbl_hsv_high = QLabel('HSV high threshold')
        self.txt_hsv_high = QLineEdit()
        self.txt_hsv_high.editingFinished.connect(self.txt_hsv_high_changed)

        mainLayout = QFormLayout()
        mainLayout.addWidget(self.no_filter)
        mainLayout.addWidget(self.hsv_filter)
        mainLayout.addWidget(lbl_hsv_low)
        mainLayout.addWidget(self.txt_hsv_low)
        mainLayout.addWidget(lbl_hsv_high)
        mainLayout.addWidget(self.txt_hsv_high)

        self.setLayout(mainLayout)

    def propagateValue(self):
        setting = Application().setting
        if setting.color_filter == 'no':
            self.no_filter.setChecked(Qt.Checked)
            self.hsv_filter.setChecked(Qt.Unchecked)
        elif setting.color_filter == 'hsv':
            self.no_filter.setChecked(Qt.Unchecked)
            self.hsv_filter.setChecked(Qt.Checked)

        self.txt_hsv_low.setText(formatListTuple(setting.color_filter_hsv_low))
        self.txt_hsv_high.setText(formatListTuple(setting.color_filter_hsv_high))

    def radio_button_click(self):
        checkedId = self.color_button_group.checkedId()

        if(checkedId == 0):
            Application().setting.color_filter = 'no'
        else:
            Application().setting.color_filter = 'hsv'

    def txt_hsv_low_changed(self):
        try:
            Application().setting.color_filter_hsv_low = parseListTuple3(self.txt_hsv_low.text())
        except Exception as ex:
            pass

    def txt_hsv_high_changed(self):
        try:
            Application().setting.color_filter_hsv_high = parseListTuple3(self.txt_hsv_high.text())
        except Exception as ex:
            pass

class GrayScaleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QFormLayout()
        self.gray_button_group = QButtonGroup()

        self.gray_scale_filter = QRadioButton('Gray scale', self)
        self.yuv_filter = QRadioButton('YUV', self)

        self.gray_button_group.addButton(self.gray_scale_filter, 0)
        self.gray_button_group.addButton(self.yuv_filter, 1)
        self.gray_scale_filter.toggled.connect(self.radio_button_click)
        self.yuv_filter.toggled.connect(self.radio_button_click)

        mainLayout.addWidget(self.gray_scale_filter)
        mainLayout.addWidget(self.yuv_filter)

        self.setLayout(mainLayout)

    def propagateValue(self):
        setting = Application().setting

        if setting.gray_scale == 'gray':
            self.gray_scale_filter.setChecked(Qt.Checked)
            self.yuv_filter.setChecked(Qt.Unchecked)
        elif setting.gray_scale == 'yuv':
            self.gray_scale_filter.setChecked(Qt.Unchecked)
            self.yuv_filter.setChecked(Qt.Checked)

    def radio_button_click(self):
        checkedId = self.gray_button_group.checkedId()

        if (checkedId == 0):
            Application().setting.gray_scale = 'gray'
        else:
            Application().setting.gray_scale = 'yuv'

class Guassian(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QFormLayout()

        lbl_kernel = QLabel('Kernel size: ')
        self.txt_kernel = QLineEdit()
        self.txt_kernel.setValidator(QIntValidator())
        self.txt_kernel.editingFinished.connect(self.txt_kernel_editing_finished)

        mainLayout.addWidget(lbl_kernel)
        mainLayout.addWidget(self.txt_kernel)

        self.setLayout(mainLayout)

    def propagateValue(self):
        setting = Application().setting

        self.txt_kernel.setText(str(setting.guassian_kernel_size))

    def txt_kernel_editing_finished(self):
        Application().setting.guassian_kernel_size = int(self.txt_kernel.text())

class CannyTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QFormLayout()
        self.canny_button_group = QButtonGroup()

        self.canny_normal = QRadioButton('Canny', self)
        self.canny_ostu_filter = QRadioButton('Canny-ostu', self)

        self.canny_button_group.addButton(self.canny_normal, 0)
        self.canny_button_group.addButton(self.canny_ostu_filter, 1)
        self.canny_normal.toggled.connect(self.radio_button_click)
        self.canny_ostu_filter.toggled.connect(self.radio_button_click)

        lbl_canny_low = QLabel('Canny low threshold')
        self.txt_canny_low = QLineEdit()
        self.txt_canny_low.setValidator(QIntValidator())
        self.txt_canny_low.editingFinished.connect(self.txt_canny_low_editing_finish)

        lbl_canny_high = QLabel('Canny high threshold')
        self.txt_canny_high = QLineEdit()
        self.txt_canny_high.setValidator(QIntValidator())
        self.txt_canny_high.editingFinished.connect(self.txt_canny_high_editing_finish)

        lbl_canny_ostu = QLabel('Canny-ostu threshold')
        self.txt_canny_ostu = QLineEdit()
        self.txt_canny_ostu.setValidator(QDoubleValidator())
        self.txt_canny_ostu.editingFinished.connect(self.txt_canny_ostu_editing_finish)

        mainLayout.addWidget(self.canny_normal)
        mainLayout.addWidget(lbl_canny_low)
        mainLayout.addWidget(self.txt_canny_low)
        mainLayout.addWidget(lbl_canny_high)
        mainLayout.addWidget(self.txt_canny_high)
        mainLayout.addWidget(self.canny_ostu_filter)
        mainLayout.addWidget(lbl_canny_ostu)
        mainLayout.addWidget(self.txt_canny_ostu)

        self.setLayout(mainLayout)

    def propagateValue(self):
        setting = Application().setting

        if setting.canny == 'canny':
            self.canny_normal.setChecked(Qt.Checked)
            self.canny_ostu_filter.setChecked(Qt.Unchecked)
        elif setting.canny == 'canny-ostu':
            self.canny_normal.setChecked(Qt.Unchecked)
            self.canny_ostu_filter.setChecked(Qt.Checked)

        self.txt_canny_low.setText(str(setting.canny_low_threshold))
        self.txt_canny_low.setText(str(setting.canny_high_threshold))
        self.txt_canny_ostu.setText(str(setting.canny_ostu_threshold))

    def radio_button_click(self):
        checkedId = self.canny_button_group.checkedId()

        if (checkedId == 0):
            Application().setting.canny = 'canny'
        else:
            Application().setting.canny = 'canny-ostu'

    def txt_canny_low_editing_finish(self):
        Application().setting.canny_low_threshold = int(self.txt_canny_low.text())

    def txt_canny_high_editing_finish(self):
        Application().setting.canny_high_threshold = int(self.txt_canny_high.text())

    def txt_canny_ostu_editing_finish(self):
        Application().setting.canny_ostu_threshold = float(self.txt_canny_ostu.text())


class HoughTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QFormLayout()

        lbl_rho = QLabel("Rho: ")
        self.txt_rho = QLineEdit()
        self.txt_rho.setValidator(QIntValidator())
        self.txt_rho.editingFinished.connect(self.txt_rho_editing_finished)

        lbl_theta = QLabel("Theta: ")
        self.txt_theta = QLineEdit()
        self.txt_theta.setValidator(QIntValidator())
        self.txt_theta.editingFinished.connect(self.txt_theta_editing_finished)

        lbl_threshold = QLabel("Vote threshold: ")
        self.txt_threshold = QLineEdit()
        self.txt_threshold.setValidator(QIntValidator())
        self.txt_threshold.editingFinished.connect(self.txt_threshold_editing_finished)

        lbl_min_line_length = QLabel("Min line length: ")
        self.txt_min_line_length = QLineEdit()
        self.txt_min_line_length.setValidator(QIntValidator())
        self.txt_min_line_length.editingFinished.connect(self.txt_min_line_length_editing_finished)

        lbl_max_line_gap = QLabel("Max line gap: ")
        self.txt_max_line_gap = QLineEdit()
        self.txt_max_line_gap.setValidator(QIntValidator())
        self.txt_max_line_gap.editingFinished.connect(self.txt_max_line_gap_editing_finished)

        mainLayout.addWidget(lbl_rho)
        mainLayout.addWidget(self.txt_rho)
        mainLayout.addWidget(lbl_theta)
        mainLayout.addWidget(self.txt_theta)
        mainLayout.addWidget(lbl_threshold)
        mainLayout.addWidget(self.txt_threshold)
        mainLayout.addWidget(lbl_min_line_length)
        mainLayout.addWidget(self.txt_min_line_length)
        mainLayout.addWidget(lbl_max_line_gap)
        mainLayout.addWidget(self.txt_max_line_gap)

        self.setLayout(mainLayout)

    def propagateValue(self):
        setting = Application().setting

        self.txt_rho.setText(str(setting.hough_rho))
        self.txt_theta.setText(str(setting.hough_theta))
        self.txt_threshold.setText(str(setting.hough_vote_threshold))
        self.txt_min_line_length.setText(str(setting.hough_min_line_length))
        self.txt_max_line_gap.setText(str(setting.hough_max_line_gap))

    def txt_rho_editing_finished(self):
        Application().setting.canny_low_threshold = int(self.txt_rho.text())

    def txt_theta_editing_finished(self):
        Application().setting.canny_low_threshold = int(self.txt_theta.text())

    def txt_threshold_editing_finished(self):
        Application().setting.canny_low_threshold = int(self.txt_threshold.text())

    def txt_min_line_length_editing_finished(self):
        Application().setting.canny_low_threshold = int(self.txt_min_line_length.text())

    def txt_max_line_gap_editing_finished(self):
        Application().setting.canny_low_threshold = int(self.txt_max_line_gap.text())

class RegionOfInterestTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QFormLayout()

        lbl_region = QLabel("Region")
        self.txt_region = QLineEdit()

        mainLayout.addWidget(lbl_region)
        mainLayout.addWidget(self.txt_region)

        self.setLayout(mainLayout)

    def txt_max_line_gap_editing_finished(self):
        Application().setting.canny_low_threshold = parseListOfPoint(self.txt_region.text())

    def propagateValue(self):
        setting = Application().setting

        self.txt_region.setText(formatListTuple(setting.region_of_interest))

class DebugTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.final_output_group = QButtonGroup()
        mainLayout = QFormLayout()

        self.debug_normal = QRadioButton("Normal")
        self.debug_color_filter = QRadioButton("Color filtering")
        self.debug_gray_scale = QRadioButton("Gray scale")
        self.debug_guassian = QRadioButton("Gaussian")
        self.debug_canny = QRadioButton("Canny edge detection")
        self.debug_hough = QRadioButton("Hough line detection")
        self.debug_average = QRadioButton("Line averaging")

        self.final_output_group.addButton(self.debug_normal, 0)
        self.final_output_group.addButton(self.debug_color_filter, 1)
        self.final_output_group.addButton(self.debug_gray_scale, 2)
        self.final_output_group.addButton(self.debug_guassian, 3)
        self.final_output_group.addButton(self.debug_canny, 4)
        self.final_output_group.addButton(self.debug_hough, 5)
        self.final_output_group.addButton(self.debug_average, 6)

        self.debug_normal.toggled.connect(self.radio_button_click)
        self.debug_color_filter.toggled.connect(self.radio_button_click)
        self.debug_gray_scale.toggled.connect(self.radio_button_click)
        self.debug_guassian.toggled.connect(self.radio_button_click)
        self.debug_canny.toggled.connect(self.radio_button_click)
        self.debug_hough.toggled.connect(self.radio_button_click)
        self.debug_average.toggled.connect(self.radio_button_click)

        mainLayout.addWidget(self.debug_normal)
        mainLayout.addWidget(self.debug_color_filter)
        mainLayout.addWidget(self.debug_gray_scale)
        mainLayout.addWidget(self.debug_guassian)
        mainLayout.addWidget(self.debug_canny)
        mainLayout.addWidget(self.debug_hough)
        mainLayout.addWidget(self.debug_average)

        self.setLayout(mainLayout)

    def propagateValue(self):
        setting = Application().setting

        if setting.final_output == 'normal':
            self.debug_normal.setChecked(Qt.Checked)
            self.debug_color_filter.setChecked(Qt.Unchecked)
            self.debug_gray_scale.setChecked(Qt.Unchecked)
            self.debug_canny.setChecked(Qt.Unchecked)
            self.debug_hough.setChecked(Qt.Unchecked)
            self.debug_average.setChecked(Qt.Unchecked)
            self.debug_guassian.setChecked(Qt.Unchecked)
        elif setting.final_output == 'color_filter':
            self.debug_normal.setChecked(Qt.Unchecked)
            self.debug_color_filter.setChecked(Qt.Checked)
            self.debug_gray_scale.setChecked(Qt.Unchecked)
            self.debug_canny.setChecked(Qt.Unchecked)
            self.debug_hough.setChecked(Qt.Unchecked)
            self.debug_average.setChecked(Qt.Unchecked)
            self.debug_guassian.setChecked(Qt.Unchecked)
        elif setting.final_output == 'gray_scale':
            self.debug_normal.setChecked(Qt.Unchecked)
            self.debug_color_filter.setChecked(Qt.Unchecked)
            self.debug_gray_scale.setChecked(Qt.Checked)
            self.debug_canny.setChecked(Qt.Unchecked)
            self.debug_hough.setChecked(Qt.Unchecked)
            self.debug_average.setChecked(Qt.Unchecked)
            self.debug_guassian.setChecked(Qt.Unchecked)
        elif setting.final_output == 'canny':
            self.debug_normal.setChecked(Qt.Unchecked)
            self.debug_color_filter.setChecked(Qt.Unchecked)
            self.debug_gray_scale.setChecked(Qt.Unchecked)
            self.debug_canny.setChecked(Qt.Checked)
            self.debug_hough.setChecked(Qt.Unchecked)
            self.debug_average.setChecked(Qt.Unchecked)
            self.debug_guassian.setChecked(Qt.Unchecked)
        elif setting.final_output == 'hough':
            self.debug_normal.setChecked(Qt.Unchecked)
            self.debug_color_filter.setChecked(Qt.Unchecked)
            self.debug_gray_scale.setChecked(Qt.Unchecked)
            self.debug_canny.setChecked(Qt.Unchecked)
            self.debug_hough.setChecked(Qt.Checked)
            self.debug_average.setChecked(Qt.Unchecked)
            self.debug_guassian.setChecked(Qt.Unchecked)
        elif setting.final_output == 'average':
            self.debug_normal.setChecked(Qt.Unchecked)
            self.debug_color_filter.setChecked(Qt.Unchecked)
            self.debug_gray_scale.setChecked(Qt.Unchecked)
            self.debug_canny.setChecked(Qt.Unchecked)
            self.debug_hough.setChecked(Qt.Unchecked)
            self.debug_average.setChecked(Qt.Checked)
            self.debug_guassian.setChecked(Qt.Unchecked)
        elif setting.final_output == 'guassian':
            self.debug_normal.setChecked(Qt.Unchecked)
            self.debug_color_filter.setChecked(Qt.Unchecked)
            self.debug_gray_scale.setChecked(Qt.Unchecked)
            self.debug_canny.setChecked(Qt.Unchecked)
            self.debug_hough.setChecked(Qt.Unchecked)
            self.debug_average.setChecked(Qt.Unchecked)
            self.debug_guassian.setChecked(Qt.Checked)

    def radio_button_click(self):
        checkedId = self.final_output_group.checkedId()

        if checkedId == 0:
            Application().setting.final_output = 'normal'
        elif checkedId == 1:
            Application().setting.final_output = 'color_filter'
        elif checkedId == 2:
            Application().setting.final_output = 'gray_scale'
        elif checkedId == 3:
            Application().setting.final_output = 'guassian'
        elif checkedId == 4:
            Application().setting.final_output = 'canny'
        elif checkedId == 5:
            Application().setting.final_output = 'hough'
        elif checkedId == 6:
            Application().setting.final_output = 'average'


class MainWindow(QMainWindow):
    output_directory = "./output"

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.mediaPlayerLeft = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayerRight = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        videoWidgetLeft = QVideoWidget()
        videoWidgetLeft.setMinimumHeight(400)
        videoWidgetLeft.setMinimumWidth(400)
        videoWidgetRight = QVideoWidget()
        videoWidgetRight.setMinimumHeight(400)
        videoWidgetRight.setMinimumWidth(400)

        self.colorTab = ColorTab()
        self.colorTab.propagateValue()
        self.grayScaleTab = GrayScaleTab()
        self.grayScaleTab.propagateValue()
        self.guassianTab = Guassian()
        self.guassianTab.propagateValue()
        self.regionOfInterestTab = RegionOfInterestTab()
        self.regionOfInterestTab.propagateValue()
        self.cannyTab = CannyTab()
        self.cannyTab.propagateValue()
        self.houghTab = HoughTab()
        self.houghTab.propagateValue()
        self.debugTab = DebugTab()
        self.debugTab.propagateValue()

        tabWidget = QTabWidget()
        tabWidget.addTab(self.colorTab, "Color filtering")
        tabWidget.addTab(self.grayScaleTab, "Gray scale")
        tabWidget.addTab(self.guassianTab, "Gaussian")
        tabWidget.addTab(self.regionOfInterestTab, "Region of interest")
        tabWidget.addTab(self.cannyTab, "Canny edge detection")
        tabWidget.addTab(self.houghTab, "Hough line detection")
        tabWidget.addTab(self.debugTab, "Debug")

        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveConfig)
        self.exitButton = QPushButton("Exit", self)
        self.exitButton.clicked.connect(self.exitCall)


        self.initMenu()
        self.initStatusBar()

        mainLayout = QGridLayout()

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layoutLR = QHBoxLayout()
        layoutLR.addWidget(videoWidgetLeft)
        layoutLR.addWidget(videoWidgetRight)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.exitButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layoutLR)
        mainLayout.addLayout(controlLayout)
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(buttonLayout)
        wid.setLayout(mainLayout)

        self.mediaPlayerLeft.setVideoOutput(videoWidgetLeft)
        self.mediaPlayerLeft.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayerLeft.positionChanged.connect(self.positionChanged)
        self.mediaPlayerLeft.durationChanged.connect(self.durationChanged)
        self.mediaPlayerLeft.error.connect(self.handleError)

        self.mediaPlayerRight.setVideoOutput(videoWidgetRight)
        self.mediaPlayerRight.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayerRight.error.connect(self.handleError)

        self.resize(800, 800)
        self.setWindowTitle('Self driving car - Detecting lane line')
        self.statusBar().showMessage('Ready')

        self.show()

    def initMenu(self):
        # Create new action
        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open driving video')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

    def initStatusBar(self):
        self.statusBar().showMessage('Ready')

    def openFile(self):
        try:
            LeftFileName, _ = QFileDialog.getOpenFileName(self, "Open Left Movie",
                    QDir.homePath())

            if LeftFileName != '':
                self.mediaPlayerLeft.setMedia(
                        QMediaContent(QUrl.fromLocalFile(LeftFileName)))

                if False:
                    try:
                        self.statusBar().showMessage("Processing")
                        rightFilename = Application().processVideo(LeftFileName)
                        Application().logger.info("output file name is: "+rightFilename)
                        self.statusBar().showMessage("Ready")
                    except Exception as ex:
                        rightFilename = None
                        self.statusBar().showMessage("Error in processing video")
                        traceback.print_exc()
                        Application().logger.error("Error in processing video", exc_info=True)

                    if rightFilename != None:
                        self.mediaPlayerRight.setMedia(
                            QMediaContent(QUrl.fromLocalFile(rightFilename)))

                self.playButton.setEnabled(True)
            else:
                return
        except Exception as ex:
            print("Error when loading video")
            traceback.print_exc()
            Application().logger.error("Error when loading video", exc_info=True)

    def play(self):
        if (self.mediaPlayerLeft.state() == QMediaPlayer.PlayingState or self.mediaPlayerRight.state() == QMediaPlayer.PlayingState):
            self.mediaPlayerLeft.pause()
            self.mediaPlayerRight.pause()
        else:
            self.mediaPlayerLeft.play()
            self.mediaPlayerRight.play()

    def mediaStateChanged(self, state):
        if (
                self.mediaPlayerLeft.state() == QMediaPlayer.PlayingState or self.mediaPlayerRight.state() == QMediaPlayer.PlayingState):
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayerLeft.setPosition(position)
        self.mediaPlayerRight.setPosition(position)

    def handleError(self):
        #self.playButton.setEnabled(False)
        Application().logger.error("Error in media player (left)" + self.mediaPlayerLeft.errorString() + repr(self.mediaPlayerLeft.error()), exc_info=True)
        Application().logger.error("Error in media player (right)" + self.mediaPlayerRight.errorString() + repr(self.mediaPlayerRight.error()), exc_info=True)
        self.statusBar().showMessage("Error in media player")

    def saveConfig(self):
        try:
            Application().writeConfig()
        except Exception as ex:
            print("Error when saving config file.")
            traceback.print_exc()
            Application().logger.error("Error when saving config file.", exc_info=True)

    def exitCall(self):
        sys.exit(app.exec_())

if __name__ == '__main__':

    if False:
        import sys

        def my_except_hook(exctype, value, traceback_):
            file = open("application.log", "a")
            file.write("\n".join(traceback.format_exception(exctype, value, traceback_)))
            file.close()
            if exctype == KeyboardInterrupt:
                print('shit')
            else:
                sys.__excepthook__(exctype, value, traceback)
            sys.exit(-1)

        sys.excepthook = my_except_hook

    app = QApplication(sys.argv)
    core = Application()
    ex = MainWindow()
    sys.exit(app.exec_())

# PyQt5 Video player
#!/usr/bin/env python

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
        
        self.mediaPlayerLeft = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayerRight = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidgetLeft = QVideoWidget()
        videoWidgetRight = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layoutLR = QHBoxLayout()
        layoutLR.addWidget(videoWidgetLeft)
        layoutLR.addWidget(videoWidgetRight)

        layout = QVBoxLayout()
        layout.addLayout(layoutLR)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayerLeft.setVideoOutput(videoWidgetLeft)
        self.mediaPlayerLeft.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayerLeft.positionChanged.connect(self.positionChanged)
        self.mediaPlayerLeft.durationChanged.connect(self.durationChanged)
        self.mediaPlayerLeft.error.connect(self.handleError)

        self.mediaPlayerRight.setVideoOutput(videoWidgetRight)
        self.mediaPlayerRight.stateChanged.connect(self.mediaStateChanged)
        #self.mediaPlayerRight.positionChanged.connect(self.positionChanged)    use left as standard
        #self.mediaPlayerRight.durationChanged.connect(self.durationChanged)    use left as standard
        self.mediaPlayerRight.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Left Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayerLeft.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        else:
            return

        fileName, _ = QFileDialog.getOpenFileName(self, "Open Right Movie",
                                                  QDir.homePath())

        if fileName != '':
            self.mediaPlayerRight.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        else:
            return

    def exitCall(self):
        sys.exit(app.exec_())
        
    def play(self):
        if (self.mediaPlayerLeft.state() == QMediaPlayer.PlayingState or self.mediaPlayerRight.state() == QMediaPlayer.PlayingState):
            self.mediaPlayerLeft.pause()
            self.mediaPlayerRight.pause()
        else:
            self.mediaPlayerLeft.play()
            self.mediaPlayerRight.play()

    def mediaStateChanged(self, state):
        if (self.mediaPlayerLeft.state() == QMediaPlayer.PlayingState or self.mediaPlayerRight.state() == QMediaPlayer.PlayingState):
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
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())

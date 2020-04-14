from PyQt5 import  QtWidgets, uic
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt,QUrl

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Load  mainwindow.ui from Qt Designer
        uic.loadUi('ui/mainwindow.ui', self)
        #self.setupUi(self)
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.initMainWindow()
        self.show()

    def initMainWindow(self):
        #Create a mediaplayer object "mediaPlayer"
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)

        #Create videoWidget object
        videoWidget = QVideoWidget()

        #Open video button
        self.open = QAction('&Open Video', self)
        self.open.setStatusTip('Open Video')
        self.open.triggered.connect(self.openFile)
        self.menuFiles.addAction(self.open)

        #PlayButton

        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.playVideo)



        #Slider settings timeline
        self.videoTimeSlider.setRange(0,0)
        self.videoTimeSlider.sliderMoved.connect(self.setPosition)

        #Slider settings volume
        self.volume.setRange(0,100)
        self.volumeTextDisplay.setText("50%")
        self.volume.setValue(50)
        self.volume.sliderMoved.connect(self.volumeControl)
        self.mediaPlayer.setVolume(50)

        #videoWidget set
        self.videoPreviewLayout = QVBoxLayout()
        self.videoPreviewLayout.addWidget(videoWidget)

        self.vpfVideoPreview.setLayout(self.videoPreviewLayout)
        #Set output to the video
        self.mediaPlayer.setVideoOutput(videoWidget)

        #media player change state
        self.mediaPlayer.stateChanged.connect(self.mediaStateChange)
        self.mediaPlayer.positionChanged.connect(self.positionChange)
        self.mediaPlayer.durationChanged.connect(self.durationChange)


    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self,"OpenVideo")
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName[0])))
            self.playButton.setEnabled(True)

    def playVideo(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def mediaStateChange(self, ):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def convert(self,seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def positionChange(self,position):
        self.videoTimeSlider.setValue(position)
        x= round(position/1000)

        duration = position/1000
        self.videoTimeDisplay.setText(self.convert(duration))

    def durationChange(self,duration):
        self.videoTimeSlider.setRange(0,duration)

    def setPosition(self,position):
        self.mediaPlayer.setPosition(position)


    def volumeControl(self,volume):
        self.volume.setValue(volume)
        self.mediaPlayer.setVolume(volume)
        self.volumeTextDisplay.setText(str(volume) + "%")

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

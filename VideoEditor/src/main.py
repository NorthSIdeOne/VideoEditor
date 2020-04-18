from PyQt5 import  QtWidgets, uic
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent,QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt,QUrl,QAbstractListModel
import styleSheet
from PyQt5.QtCore import QAbstractListModel

class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()

import sys

class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()

        #Load  mainwindow.ui from Qt Designer
        uic.loadUi('../ui/mainwindow.ui', self)
        #Load all settings
        self.initMainWindow()
        #Show the main window
        self.show()

    def initMainWindow(self):
        """
            This function initialize all the buttons and all the setting for
            displaying and control the video.
        """
        self.index = -1
        self.curentFiles = {}
        self.curentIndex = self.index
        self.deleteButton.clicked.connect(self.RemoveVideo)
        self.addButton.clicked.connect(self.openFile)
        #Create a mediaplayer object to control the video
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(50)

        #Create videoWidget object for displaying the video
        videoWidget = QVideoWidget()

        #Create a playlist object for multiple videos
        self.playlist = QMediaPlaylist()
        self.mediaPlayer.setPlaylist(self.playlist)


        self.model = PlaylistModel(self.playlist)
        self.videoFiles.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.videoFiles.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)

        #videoWidget set
        self.videoPreviewLayout = QVBoxLayout()
        self.videoPreviewLayout.addWidget(videoWidget)
        self.vpfVideoPreview.setLayout(self.videoPreviewLayout)

        #Create Open Video button in taskbar
        self.open = QAction('&Open Video', self)
        self.open.setStatusTip('Open Video')
        self.open.triggered.connect(self.openFile)
        self.menuFiles.addAction(self.open)
        self.setAcceptDrops(True)
        #PlayButton
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.playVideo)
        #rewind Button

        #next Button

        #Slider settings timeline
        self.videoTimeSlider.setRange(0,0)
        self.videoTimeSlider.sliderMoved.connect(self.setPosition)

        #Slider settings volume
        self.volume.setRange(0,100)
        self.volumeTextDisplay.setText("50%")
        self.volume.setValue(50)
        self.volume.sliderMoved.connect(self.volumeControl)

        #media player change state
        self.mediaPlayer.stateChanged.connect(self.mediaStateChange)
        self.mediaPlayer.positionChanged.connect(self.positionChange)
        self.mediaPlayer.durationChanged.connect(self.durationChange)

        #Set output to the video
        self.mediaPlayer.setVideoOutput(videoWidget)


    def openFile(self):
        """
            Function for opening a video file from
            taskbar.
        """
        fileName = QFileDialog.getOpenFileName(self,"OpenVideo")
        #Checks if fileName is a valid file
        if fileName[0] != '':
            #Set to mediaPlayer object the file(video)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName[0])))
            self.index = self.index + 1
            print("Index = " + str(self.index))
            self.curentFiles[self.index] = fileName[0]
            print(self.curentFiles)
            #Enable the play button after the video was set
            self.playButton.setEnabled(True)
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(fileName[0])))
            self.model.layoutChanged.emit()

    def playVideo(self):
        """"
            Function for controling the video Play/Pause
        """
        #Checks the state of the video.If the video is playing it will be paused.
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            #If the video is paused it will be playing
            self.mediaPlayer.play()


    def mediaStateChange(self, ):
        """
            This function is changing the icon of the playButton.
            If the video is going from playing to "pause",the icon
            will change to pause icon.Otherwise the playingButton
            will change to "play" icon
        """

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(QIcon("../resources/icons/1262942-multimedia/png/002-pause.png"))
        else:
            self.playButton.setIcon(QIcon("../resources/icons/1262942-multimedia/png/025-play.png"))



    def convert(self,seconds):
        """
            Function for converting duration of the video(seconds)
            into Hour/minute/seconds and returning that format.
        """

        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def positionChange(self,position):
        """
            This function is activatet when the video is
            changing the time.When that happens is updating
            the Time slider the new position and the time label.
        """
        self.videoTimeSlider.setValue(position)
        #Convert position into seconds
        duration = position/1000
        self.videoTimeDisplay.setText(self.convert(duration))

    def durationChange(self,duration):
        """
            This function update the range of the time splider
            when the video position is changing.
        """
        self.videoTimeSlider.setRange(0,duration)

    def setPosition(self,position):
        """
            Sets the video time based on time slider.
            When the user is changing the time slider
            to a specific time,the video position is updated.
        """
        self.mediaPlayer.setPosition(position)


    def volumeControl(self,volume):
        """
            This function is used for changing the volume of the video
            and update the volume label.Also,is used to change the color
            of the slider based on the volume.If is < 50 is green, <50 && < 75 yellow
            and red for 74 >
        """
        self.volume.setValue(volume)
        self.mediaPlayer.setVolume(volume)
        self.volumeTextDisplay.setText(str(volume) + "%")
        if(volume <=50):
            #green
            self.volume.setStyleSheet(styleSheet.volumeStageOne)
        elif(volume > 50 and volume <=75 ):
            #yellow
            self.volume.setStyleSheet(styleSheet.volumeStageTwo)
        else:
            #red
            self.volume.setStyleSheet(styleSheet.volumeStageThree)


        #If the volume is zero the icon of the volume is changed
        if(volume == 0):
            self.volumeIcon.setIcon(QIcon("../resources/icons/1262942-multimedia/png/mute.png"))
        else:
            self.volumeIcon.setIcon(QIcon("../resources/icons/1262942-multimedia/png/speaker.png"))



    def closeEvent(self, event):
        """
            Popup a dialog when the user is trying to close the main app.
        """
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()
    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[i])))
        self.curentIndex = i
        print(i)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.videoFiles.setCurrentIndex(ix)


    def RemoveVideo(self):
        if(self.curentIndex != -1):
            self.playlist.removeMedia(self.curentIndex)
            self.index=self.index - 1
            if(self.index > -1):
                del self.curentFiles[self.curentIndex]
                self.SortFilesIndex()
                print(self.curentFiles)
            else:
                self.playButton.setEnabled(False)
                self.videoTimeSlider.setValue(0)



    def SortFilesIndex(self):
        newIndex = 0
        newCurentFiles = {}
        for key in self.curentFiles:
            newCurentFiles[newIndex] = self.curentFiles[key]
            newIndex+=1
        self.curentFiles =  newCurentFiles.copy()





app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

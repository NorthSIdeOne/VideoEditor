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
import FoldersConfig as ProjectFolders
import sys
from qtimeline import QTimeLine

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

        #Total number of curent media opened
        self.totalIndex = -1
        #Dictionary for index and path for the media
        self.curentFiles = {}
        #Index that indicates the curent media selected
        self.curentIndex = self.totalIndex
        #Media play speed
        self.speed = 1
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
        #back 15 seconds Button
        self.skipbackButton.clicked.connect(self.skipbackFunction)
        #skip 15 seconds forward Button
        self.skipforwardButton.clicked.connect(self.skipforwadFunction)

        #fastorForward button
        self.fastForward.clicked.connect(self.fastForwardFunction)

        #rewind button
        self.rewind.clicked.connect(self.rewindFunction)

        #Speed label
        self.speedLabel.setText("1.0x")
        #Add video button
        self.addButton.clicked.connect(self.openFile)

        #Remove video button

        self.deleteButton.clicked.connect(self.RemoveVideo)

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

        qtimeline = QTimeLine(360,1)
        self.test = QVBoxLayout()
        self.test.addWidget(qtimeline)
        qtimeline2 = QTimeLine(360,1)
        self.test.addWidget(qtimeline2)
        self.sfTimeLineFrame.setLayout(self.test)
        self.concatenateComboBox =  QtWidgets.QComboBox(self)

        self.entry = QtGui.QStandardItemModel()
        self.concatenateList.setModel(self.entry)
        self.concatenateList.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item
        self.concatenateVideoList.removeItem(0)

        for text in ["Itemname1", "Itemname2", "Itemname3", "Itemname4"]:
            it = QtGui.QStandardItem(text)
            self.entry.appendRow(it)
        self.itemOld = QtGui.QStandardItem("text")


    def on_clicked(self, index):
        item = self.entry.itemFromIndex(index)

        #self.entry.clearItemData(index)
        self.entry.sort(0)
        print(item.index().row())

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
            #Update total number of curent media opened
            self.totalIndex = self.totalIndex + 1
            #Update the curentFiles dict which holds the path for the opened videos
            self.curentFiles[self.totalIndex] = fileName[0]

            #Enable the play button after the video was set
            self.playButton.setEnabled(True)
            #Add media to the playlist
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(fileName[0])))

            #Add item to the list for avalabile videos for concatenate
            self.concatenateVideoList.addItem(fileName[0].split('/')[-1])
            print(self.concatenateVideoList.currentIndex())
            #A new media was added so we sent a signal to updated List view
            self.model.layoutChanged.emit()

    def playVideo(self):
        """"
            Function for controling the video Play/Pause
        """
        #Checks the state of the video.If the video is playing it will be paused.
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            #Pause the video
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
            #Change playButton icon into "Pause icon"
            self.playButton.setIcon(QIcon("../resources/icons/GUI_Icons/002-pause.png"))
        else:
            #Change playButton icon into "Play icon"
            self.playButton.setIcon(QIcon("../resources/icons/GUI_Icons/play.png"))



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
        print(self.mediaPlayer.position)

    def skipforwadFunction(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 15000)
    def skipbackFunction(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() -15000)
    def rewindFunction(self):
        if(self.speed - 0.1 >=0.1):
            self.speed-=0.1
        self.mediaPlayer.setPlaybackRate(self.speed)
        self.speedLabel.setText(str(round(self.speed, 2))+"x")

    def fastForwardFunction(self):
        if(self.speed + 0.1 <=2.1):
            self.speed+=0.1
        self.mediaPlayer.setPlaybackRate(self.speed)
        self.speedLabel.setText(str(round(self.speed, 2))+"x")

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
            self.volumeIcon.setIcon(QIcon("../resources/icons/GUI_Icons/mute.png"))
        else:
            self.volumeIcon.setIcon(QIcon("../resources/icons/GUI_Icons/speaker.png"))





    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)
        self.curentIndex = i
        self.speed = 1
        self.mediaPlayer.setPlaybackRate(self.speed)
        self.speedLabel.setText(str(self.speed)+"x")
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[self.curentIndex])))


    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            print("playlist_position_changed")
            self.videoFiles.setCurrentIndex(ix)


    def RemoveVideo(self):
        """
            This function is connected to the remove button on Project files.
            It removes the file from List view and curentFiles dictionary.It also
            changethe mediaPlayer output based on what media was left.If the is media
            left the video output will be the firs mediaFile from the list.If the List view
            have no media left,the video output will be an video of 1 seconds with black background
            to clear the screen.

        """
        if(self.totalIndex != -1):
            if(self.curentIndex != -1):
                try:
                    #Delete media from index "curentIndex"
                    self.playlist.removeMedia(self.curentIndex)
                    try:
                        #Delete the file name from index "curentIndex" from curentFiles
                        del self.curentFiles[self.curentIndex]
                        #Decrement the total number of videos opened
                        self.totalIndex=self.totalIndex - 1
                        #Update index of every video from curentFiles
                        self.SortFilesIndex()



                        if(self.totalIndex == -1):
                            try:
                                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
                                #Block the play button
                                self.playButton.setEnabled(False)
                                #Reset the time slider
                                self.videoTimeSlider.setValue(0)
                                #Reset the time slider
                                self.videoTimeSlider.setRange(0,0)
                            except:
                                print("The black video couldn't be loaded")
                        else:
                           try:
                               self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[0])))
                           except:
                               print("The mediaPlayer couldn't be updated")

                    except:
                        print("The value from index "+str(self.curentIndex) + " could not be deleted form curentFiles")
                except:
                    print("Media cannot be deleted from playlist")
        else:
            #Block the play button
            self.playButton.setEnabled(False)
            #Reset the time slider
            self.videoTimeSlider.setValue(0)
            #Reset the time slider
            self.videoTimeSlider.setRange(0,0)



    def SortFilesIndex(self):
        """
            This function sort the curentFiles dictionary.
            When an element is deleted from curentFiles the function
            sort the index of the curentFiles ascending.
        """
        newIndex = 0
        newCurentFiles = {}
        #loop through the curentFiles and update the index
        for key in self.curentFiles:
            newCurentFiles[newIndex] = self.curentFiles[key]
            newIndex+=1

        #curentFiles files is updated to the new dictionary of files
        self.curentFiles =  newCurentFiles.copy()



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

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

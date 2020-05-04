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
from VideoEditing import Panel
from Multithreading import Worker
import mimetypes
import numpy as np
import cv2

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
        #delete all temp files
        self.deleteAllTemp()

        """<Objects>"""
        #Object for controling all edit functions
        self.edit = Panel()
        """</Objects>"""

        """--------------------<Global variables>----------------------------"""
        #Thread manager variable
        self.threadmanager = True
        #Audio file holder
        self.audioFile = ''
        #frame time variable
        self.frameTime = ''
        #frame file path
        self.frameFilePath = ''
        #Total number of curent media opened
        self.totalIndex = -1
        #Dictionary for index and path for the media
        self.curentFiles = {}
        #Index that indicates the curent media selected
        self.curentIndex = self.totalIndex
        #Curent index of Concatenate ListView
        self.curentIndexOfConcatenateList = -1
        #Dictionary with all video path for concatenate
        self.concatenateVideos ={}
        #Total number of videos added to the concatenate list view
        self.totalNrOfVideosConcat = -1
        #Media play speed
        self.speed = 1

        """-------------------</Global variables>----------------------------"""

        """----------------<Media player settings>---------------------------"""
        #Create a mediaplayer object to control the video
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(50)


        #Create a playlist object for multiple videos
        self.playlist = QMediaPlaylist()
        self.mediaPlayer.setPlaylist(self.playlist)


        self.model = PlaylistModel(self.playlist)
        self.videoFiles.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.videoFiles.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)

        #Create videoWidget object for displaying the video
        videoWidget = QVideoWidget()
        #videoWidget set
        self.videoPreviewLayout = QVBoxLayout()
        self.videoPreviewLayout.addWidget(videoWidget)
        self.vpfVideoPreview.setLayout(self.videoPreviewLayout)
        """----------------</Media player settings>--------------------------"""


        """-----------------<Buttons&Labels settings>-------------------------"""
        #Create Open Video button in taskbar
        self.open = QAction('&Open Video', self)
        self.open.setStatusTip('Open Video')
        self.menuFiles.addAction(self.open)
        self.setAcceptDrops(True)

        #PlayButton
        self.playButton.setEnabled(False)
        #Speed label
        self.speedLabel.setText("1.0x")
        #Slider settings timeline
        self.videoTimeSlider.setRange(0,0)
        #Slider settings volume
        self.volume.setRange(0,100)
        self.volume.setValue(50)
        self.volumeTextDisplay.setText("50%")
        #Cut lock buttons
        self.lockButtonStart.setCheckable(True)
        self.lockButtonFinish.setCheckable(True)
        #Cut text editor settings
        self.cutStart.setReadOnly(True)
        self.cutFinish.setReadOnly(True)
        self.cutStart.setText("0:00:00")
        self.cutFinish.setText("0:00:00")
        #Resolution Image settings
        self.resolutionIcon.setPixmap(QPixmap("../resources/icons/GUI_Icons/720.png"))

        """-----------------</Buttons&Labels settings>-------------------------"""


        """-----------------<Buttons connections>------------------------------"""

        """           -----------<Player buttons>---------                    """
        #Play button
        self.playButton.clicked.connect(self.playVideo)

        #back 15 seconds Button
        self.skipbackButton.clicked.connect(self.skipbackFunction)
        #skip 15 seconds forward Button
        self.skipforwardButton.clicked.connect(self.skipforwadFunction)

        #fastorForward button
        self.fastForward.clicked.connect(self.fastForwardFunction)
        #rewind button
        self.rewind.clicked.connect(self.rewindFunction)

        #Add video button
        self.addButton.clicked.connect(self.openFile)
        #Remove video button
        self.deleteButton.clicked.connect(self.RemoveVideo)
        #save video
        self.saveVideo.clicked.connect(self.saveVideoFunction)
        #Time slider
        self.videoTimeSlider.sliderMoved.connect(self.setPosition)

        #Volume slider
        self.volume.sliderMoved.connect(self.volumeControl)

        #media player change state
        self.mediaPlayer.stateChanged.connect(self.mediaStateChange)
        self.mediaPlayer.positionChanged.connect(self.positionChange)
        self.mediaPlayer.durationChanged.connect(self.durationChange)
        """         -----------</Player buttons>---------                   """
        #Open file
        self.open.triggered.connect(self.openFile)

        """         -------------<Edit  Buttons>-----------------           """


        """<Concatenate>"""
        #Create a model for Concatenate Lisview
        self.concatenateModel = QtGui.QStandardItemModel()
        #Set the model to the Concatenate List view
        self.concatenateList.setModel(self.concatenateModel)
        #Concatenate list of videos
        self.concatenateList.clicked[QtCore.QModelIndex].connect(self.setConcatenateIndex)
        #Add button to concatenate list
        self.addConcatenate.clicked.connect(self.addVideoToConcatenate)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item
        self.removeConcatenate.clicked.connect(self.removeVideoToConcatenate)
        #Concatenate Button
        self.concatenateButton.clicked.connect(self.concatenateThreadFunction)
        """</Concatenate>"""


        """<Cut>"""
        #Lock cut filed1
        self.lockButtonStart.clicked.connect(self.lockButtonChangeIconStart)
        #Lock cut filed2
        self.lockButtonFinish.clicked.connect(self.lockButtonChangeIconFinish)
        #Cut button
        self.cutButton.clicked.connect(self.cutThreadFunction)
        """</Cut>"""

        """<Resolution>"""
        #Resoluiton ComboBox for selecting the desired resolution
        self.ResolutionsList.currentIndexChanged.connect(self.changeResolutionDisplay)
        #Change resolution button
        self.changeResolution.clicked.connect(self. changeResolutionThread)
        """</Resoluton>"""


        """<Mirror>"""
        #Mirror button
        self.mirroringButton.clicked.connect(self.mirrorThread)
        """</Mirror>"""

        """<Audio replace>"""

        self.openAudioFile.clicked.connect(self.openAudio)
        self.removeAudioFile.clicked.connect(self.removeAudioFileFunction)
        self.audioModeSelect.currentIndexChanged.connect(self.changeAudioBackground)
        self.AddAudio.clicked.connect(self.SoundReplaceThread)
        """</Audio replace>"""

        """<GetFrame>"""

        self.getFrameButton.clicked.connect(self.GetFrameFunction)
        #self.saveFrameButton.setShortcut("Ctrl+S")
        self.saveFrameButton.setStatusTip('Save File')
        self.saveFrameButton.clicked.connect(self.saveFrame)
        """"</GetFrame>"""

        """<AddSubtitles>"""

        self.loadSubtitles.clicked.connect(self.loadSubtitlesFunction)
        self.cleanButton.clicked.connect(self.removeSubtitlesFunction)
        self.addSubtitle.clicked.connect(self.addSubtitlesThread)
        """</AddSubtitles>"""

        """         -------------</Edit  Buttons>-----------------            """
        """         -------------<Shortcut Buttons>---------------            """

        self.soundShortcut.clicked.connect(self.soundShortcutKey)
        self.getFrameShortcut.clicked.connect(self.getFrameShortcutKey)
        self.cutShortcut.clicked.connect(self.cutShortcutKey)
        self.concatShortcut.clicked.connect(self.concatShortcutKey)
        self.mirrorShortcut.clicked.connect(self.mirrorShortcutKey)

        """         -------------</Shortcut Buttons>---------------            """
        """-----------------</Buttons connections>----------------------------"""



        """-------------------<Threads for editing>--------------------------"""

        self.pool = QThreadPool()

        """-------------------</Threads for editing>--------------------------"""


        """<Experimental>"""
        qtimeline = QTimeLine(360,1)
        self.test = QVBoxLayout()
        qtimeline2 = QTimeLine(360,1)
        self.test.addWidget(qtimeline)
        self.test.addWidget(qtimeline2)


        self.sfTimeLineFrame.setLayout(self.test)
        #self.editMenu.setCurrentIndex(5)
        """</Experimental>"""

        #Set output to the video
        self.mediaPlayer.setVideoOutput(videoWidget)



    """ ------------------<Concatenate functions>---------------------------"""
    def setConcatenateIndex(self, index):
            """
                Set the curent index of the selected
                item from concatenate list view (self.concatenateList)
            """
            #Get the item from the model of index "index"
            item = self.concatenateModel.itemFromIndex(index)
            #Get the "item " row index
            self.curentIndexOfConcatenateList = item.index().row()
            print(self.concatenateVideos)

    def addVideoToConcatenate(self):
            """
                Add from 'concatenateVideoList'
                a video to 'concatenateList'
            """

            try:
                #Add the current video selected from the ComboBox to the concatenate list view
                item = QtGui.QStandardItem(self.curentFiles[self.concatenateVideoList.currentIndex()].split('/')[-1])
                self.concatenateModel.appendRow(item)
                self.totalNrOfVideosConcat+=1
                self.concatenateVideos[self.totalNrOfVideosConcat] = self.curentFiles[self.concatenateVideoList.currentIndex()]

            except:
                print("No video")
                QMessageBox.about(self, "No video", "Please add a video!       ")
                print(self.concatenateVideoList.currentIndex())


    def removeVideoToConcatenate(self):
            """
                Remove video from concatenation list.
            """
            try:
                self.concatenateModel.removeRow(self.curentIndexOfConcatenateList)
                del self.concatenateVideos[self.curentIndexOfConcatenateList]
                self.totalNrOfVideosConcat-=1
                self.SortFilesIndexConcat()

            except:
                QMessageBox.about(self, "No video", "No video to remove or not selected!     ")
                print("Error when removing video from list")



    def concatenate(self):
            """
                This function is used for concatenate multiple videos
                from the list.
            """
            if(self.curentIndex == -1 and self.totalIndex != -1):
                self.curentIndex = 0
            try:
                videosToConcatenate = []

                #I'm adding the main video
                videosToConcatenate.append(self.curentFiles[self.curentIndex])

                #Add the path to all videos to be concatenated
                for key in self.concatenateVideos:
                     videosToConcatenate.append(self.concatenateVideos[key])

                #Save the current index befor concatenation because
                #during the concatenation the user could change the curent video
                #so it would affect curentFiles
                indexOfRootVideo = self.curentIndex
                print(videosToConcatenate)
                #Call concatenate function and save the url of the modified video
                self.curentFiles[indexOfRootVideo] =self.edit.concat(videosToConcatenate)

                #Update the media with the edited video
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[indexOfRootVideo])))

                #Clear concatenate list view
                self.concatenateModel.removeRows( 0, self.concatenateModel.rowCount())
                #Clear the dict that holds all the data for concatenation
                self.concatenateVideos.clear()
                #Reste the number of videos to be concatenated
                self.totalNrOfVideosConcat = -1

            except:
                print("A problem occured during concatenation process.Check 'concatenate' function")


    def SortFilesIndexConcat(self):
            """
                This function sort the curentFiles dictionary.
                When an element is deleted from curentFiles the function
                sort the index of the curentFiles ascending.
            """
            newIndex = 0
            newCurentFiles = {}
            #loop through the curentFiles and update the index
            for key in self.concatenateVideos:
                newCurentFiles[newIndex] = self.concatenateVideos[key]
                newIndex+=1

            #curentFiles files is updated to the new dictionary of files
            self.concatenateVideos =  newCurentFiles.copy()




    """-------------------</Concatenate functions>--------------------------"""


    """-----------------------<Cut functions>--------------------------------"""

    def lockButtonChangeIconStart(self):
            """
                Function for changing the icon
                when the button is pressed.
            """
            if(self.lockButtonStart.isChecked() == True):
                self.lockButtonStart.setIcon(QIcon("../resources/icons/GUI_Icons/icons8-lock-80.png"))
            else:
                self.lockButtonStart.setIcon(QIcon("../resources/icons/GUI_Icons/icons8-padlock-80.png"))

    def lockButtonChangeIconFinish(self):
            """
                Function for changing the icon
                when the button is pressed.
            """

            if(self.lockButtonFinish.isChecked() == True):
                self.lockButtonFinish.setIcon(QIcon("../resources/icons/GUI_Icons/icons8-lock-80.png"))
            else:
                self.lockButtonFinish.setIcon(QIcon("../resources/icons/GUI_Icons/icons8-padlock-80.png"))

    def restCutButtons(self):
            """
                This function is used to reset
                all the value for cut section.
            """
            self.cutStart.setText("0:00:00")
            self.cutFinish.setText("0:00:00")
            if(self.lockButtonStart.isChecked() == True):
                self.lockButtonStart.toggle()
            if(self.lockButtonFinish.isChecked() == True):
                self.lockButtonFinish.toggle()
            self.lockButtonChangeIconStart()
            self.lockButtonChangeIconFinish()

    def cutFunction(self):
            """
                Function used for cut a video from
                'start' to 'finish' and replace in the
                'curentFiles'(dictionary that holds all opend video)
                the curent video path with the path provided by the
                'edit.cut'
            """
            try:

                #if both buttons are pressed the the function can be called
                if(self.lockButtonStart.isChecked() == True and self.lockButtonFinish.isChecked() == True):
                        try:
                            #save the current index before cut because user can change the 'curentIndex' during execution
                            indexOfRootVideo = self.curentIndex

                            #call the cut function and the result path is saved in currentFiles
                            self.curentFiles[indexOfRootVideo] = self.edit.cut([self.curentFiles[indexOfRootVideo]], [self.cutStart.toPlainText(),self.cutFinish.toPlainText()])
                            #Set the new video
                            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
                            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[indexOfRootVideo])))
                            #Reset all values for cut function

                        except:
                            print("Problem in  at self.edit.cut or mediaPlayer")
            except:
                print("Problem in cutFunction function")





    """-----------------------</Cut functions>-------------------------------"""

    """-----------------------<Mirror functions>-----------------------------"""

    def mirrorVideo(self):
        if(self.curentIndex == -1 and self.totalIndex != -1):
            self.curentIndex = 0
        try:
            indexOfRootVideo = self.curentIndex
            result = ''
            result = self.edit.video_mirroring([self.curentFiles[indexOfRootVideo]])
            if(result != ''):
                self.curentFiles[indexOfRootVideo] =result
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[indexOfRootVideo])))
        except:
            print("Problem in change mirror function")

    """-----------------------</Mirror functions>-----------------------------"""


    """-----------------------<Resoluton functions>-----------------------------"""

    def changeResolutionF(self):
        """
            Function for changing the video resolution.
        """
        if(self.curentIndex == -1 and self.totalIndex != -1):
            self.curentIndex = 0
        currentResolution = self.ResolutionsList.currentText()[0:len(self.ResolutionsList.currentText())-1]
        try:
            indexOfRootVideo = self.curentIndex
            self.curentFiles[indexOfRootVideo] = self.edit.video_resize([self.curentFiles[indexOfRootVideo]],currentResolution)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[indexOfRootVideo])))
        except:
            print("Problem in change resolution")



    def changeResolutionDisplay(self):
        """
            Usef for changing image in resolution section
            when the user select a resolution.
        """
        resolutionsIconList = ["../resources/icons/GUI_Icons/720.png","../resources/icons/GUI_Icons/540.png","../resources/icons/GUI_Icons/360.png","../resources/icons/GUI_Icons/240.png","../resources/icons/GUI_Icons/144.png"]
        if(self.ResolutionsList.currentIndex() == 0):
            self.resolutionIcon.setPixmap(QPixmap(resolutionsIconList[0]))
        elif(self.ResolutionsList.currentIndex() == 1):
            self.resolutionIcon.setPixmap(QPixmap(resolutionsIconList[1]))
        elif(self.ResolutionsList.currentIndex() == 2):
            self.resolutionIcon.setPixmap(QPixmap(resolutionsIconList[2]))
        elif(self.ResolutionsList.currentIndex() == 3):
            self.resolutionIcon.setPixmap(QPixmap(resolutionsIconList[3]))
        elif(self.ResolutionsList.currentIndex() == 4):
            self.resolutionIcon.setPixmap(QPixmap(resolutionsIconList[4]))

    """-----------------------</Resoluton functions>--------------------------"""


    """-----------------------<Sound Repalce functions>--------------------------"""

    def openAudio(self):
        try:
            fileName = QFileDialog.getOpenFileName(self,"Open Audio")
            mimetypes.init()
            mimestart = mimetypes.guess_type(fileName[0])[0]

            if mimestart != None:
                mimestart = mimestart.split('/')[0]
                if mimestart == 'audio':
                    print("Audio file detected")
                    self.audioFile = fileName[0]
                    self.audioFileCheck.setIcon(QIcon("../resources/icons/GUI_Icons/check.png"))
                else:
                    QMessageBox.about(self, "Audio", "This is not an audio file.Please load an audio file..")
                    print("Non audio file detected")
            else:
                QMessageBox.about(self, "Audio", "This file format is not accepted.")
                print("Not accepted file")
        except:
            QMessageBox.about(self, "Audio", "Changing sound track failed.")
            print("Problem in open audio function")

    def removeAudioFileFunction(self):
        self.audioFile = ''
        self.audioFileCheck.setIcon(QIcon("../resources/icons/GUI_Icons/ezgif-7-e04c11fb7018.png"))

    def changeAudioBackground(self):
        if(self.audioModeSelect.currentIndex() == 0):
            self.aduioModeImage.setPixmap(QPixmap("../resources/img/soundAdd.png"))
        elif(self.audioModeSelect.currentIndex() == 1):
            self.aduioModeImage.setPixmap(QPixmap("../resources/img/soundReplace.png"))

    def SoundReplaceFunction(self):
        if(self.curentIndex == -1 and self.totalIndex != -1):
            self.curentIndex = 0
        audioMode = self.audioModeSelect.currentText()
        print(audioMode)
        try:
            if(self.audioFile != ''):
                if(self.totalIndex != -1):
                    indexOfRootVideo = self.curentIndex
                    self.curentFiles[indexOfRootVideo] = self.edit.soundReplace([self.curentFiles[indexOfRootVideo]],self.audioFile,audioMode)
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[indexOfRootVideo])))
                else:

                    print("No video uploaded")
            else:

                print("No aduio file uploaded")
        except:

            print("Problem in SoundReplaceFunction")

    """-----------------------</Sound Repalce functions>-------------------------"""

    """-----------------------<GetFrame functions>-------------------------"""
    def GetFrameFunction(self):
        if(self.curentIndex == -1 and self.totalIndex != -1):
            self.curentIndex = 0
        try:
            if(self.totalIndex != -1 and self.frameTime != ''):
                indexOfRootVideo = self.curentIndex
                print(self.frameTime)
                self.frameFilePath = ''
                self.frameFilePath = self.edit.getFrame([self.curentFiles[indexOfRootVideo]],self.frameTime)
                self.extractedFrame.setPixmap(QPixmap(self.frameFilePath))
            else:
                print("No video uploaded or frameTime is empty")

        except:
            print("Problem in GetFrameFunction")

    def saveFrame(self):
        try:
            fileName = QFileDialog.getSaveFileName(self, 'Save File',"img.jpg", '*.jpg')
            img = cv2.imread(self.frameFilePath)
            cv2.imwrite(fileName[0],img)
        except:
            QMessageBox.about(self, "Save image", "Problem during saving image.")
            print("Problem during saving image")
    """-----------------------</GetFrame functions>-------------------------"""

    """-----------------------<Add Subtitles functions>-----------------------"""

    def loadSubtitlesFunction(self):
        try:
            fileName = QFileDialog.getOpenFileName(self,"Open Subtitles")
            if(fileName[0].split('.')[-1] == "srt"):
                self.subtitlesFile = fileName[0]
                self.subtitlesCheck.setIcon(QIcon("../resources/icons/GUI_Icons/check.png"))
            else:
                QMessageBox.about(self, "Subtitles", "Couldn't load subtitles.Please use file with .srt extension.")

        except:
            print("Problem in load Subtitles function")

    def removeSubtitlesFunction(self):
        self.subtitlesFile = ''
        self.subtitlesCheck.setIcon(QIcon("../resources/icons/GUI_Icons/ezgif-7-e04c11fb7018.png"))


    def addSubtitlesFunction(self):
        if(self.curentIndex == -1 and self.totalIndex != -1):
            self.curentIndex = 0
        try:
            if(self.subtitlesFile != ''):
                if(self.totalIndex != -1):
                    indexOfRootVideo = self.curentIndex
                    self.curentFiles[indexOfRootVideo] = self.edit.addSubtitles([self.curentFiles[indexOfRootVideo]],self.subtitlesFile)
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("../resources/videos/blackvideo.mp4")))
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[indexOfRootVideo])))
                else:
                    print("No video uploaded")
            else:
                print("No subtitles file uploaded")
        except:
            print("Problem in addSubtitlesFunction")


    """-----------------------</Add Subtitles functions>----------------------"""

    """--------------------------<File functions>----------------------------"""
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
            self.curentIndex = self.totalIndex
            #Update the curentFiles dict which holds the path for the opened videos
            self.curentFiles[self.totalIndex] = fileName[0]

            if(self.totalIndex == 0):
                self.curentIndex = 0
            #Enable the play button after the video was set
            self.playButton.setEnabled(True)
            #Add media to the playlist
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(fileName[0])))

            #Add item to the list for avalabile videos for concatenate
            self.concatenateVideoList.addItem(fileName[0].split('/')[-1])

            #A new media was added so we sent a signal to updated List view
            self.model.layoutChanged.emit()



    """------------------------</File functions>----------------------------"""


    """------------------<Media player functions>---------------------------"""

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
            This function is activated when the video is
            changing the time.When that happens is updating
            the Time slider the new position and the time label.
        """
        self.videoTimeSlider.setValue(position)

        #Convert position into seconds
        duration = position/1000
        self.frameTime = int(duration)
        self.videoTimeDisplay.setText(self.convert(duration))
        if(self.lockButtonStart.isChecked() == False):
            self.cutStart.setText(self.convert(duration))
        if(self.lockButtonFinish.isChecked() == False):
            self.cutFinish.setText(self.convert(duration))


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
        try:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.curentFiles[self.curentIndex])))
            #Reset cut text and icon
            self.restCutButtons()
        except:
            print("Error in  playlist_selection_changed function.Media player couldn't be updated")





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

                    #Delete video from concatenate ComboBox
                    self.concatenateVideoList.removeItem(self.curentIndex)

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

    def saveVideoFunction(self):
        try:
            import shutil
            extension = self.curentFiles[self.curentIndex].split('.')[-1]
            extension = "*." + extension
            fileName = QFileDialog.getSaveFileName(self, 'Save video',"video_name", extension)
            shutil.move(self.curentFiles[self.curentIndex], fileName[0])
            print("Save video Done")
        except:
            QMessageBox.about(self, "Save video", "Error during the video saving.")
            print("Error during the video saving")

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




    def soundShortcutKey(self):
        self.editMenu.setCurrentIndex(4)
    def getFrameShortcutKey(self):
        self.editMenu.setCurrentIndex(5)
    def cutShortcutKey(self):
        self.editMenu.setCurrentIndex(1)
    def concatShortcutKey(self):
        self.editMenu.setCurrentIndex(0)
    def mirrorShortcutKey(self):
        self.editMenu.setCurrentIndex(3)


        """------------------</Media player functions>-----------------------"""

        """----------------------<Thread functions>--------------------------"""

    """---<Concatenate>---"""
    def concatenateThreadFunction(self):
            #If is true that means that no thread is running and can start a thread
            if(self.threadmanager == True):
                try:
                    #If is false that means that a thread is already executing
                    self.threadmanager = False
                    worker = Worker(self.concatenate)
                    #When the thread is done threadmanager will be True
                    worker.signals.finished.connect(self.ReleaseThread)
                    self.pool.start(worker)
                except:
                    print("Problem with concatenate thread")
            else:
                print("A thread is already running")

    """---</Concatenate>---"""

    """---<Cut>---"""
    def cutThreadFunction(self):
           if(self.threadmanager == True):
               try:
                   self.threadmanager = False
                   worker = Worker(self.cutFunction)
                   worker.signals.finished.connect(self.restCutButtons)
                   worker.signals.finished.connect(self.ReleaseThread)
                   self.pool.start(worker)
               except:
                   print("Problem with cut thread")
           else:
               print("A thread is already running")

    """---</Cut>---"""

    """---<Resolution>---"""
    def changeResolutionThread(self):
        if(self.threadmanager == True):
           try:
               self.threadmanager = False
               worker = Worker(self.changeResolutionF)
               worker.signals.finished.connect(self.ReleaseThread)
               self.pool.start(worker)
           except:
               print("Problem with resolution thread")
        else:
            print("A thread is already running")

    """---</Resolution>---"""

    """---<Mirror>---"""

    def mirrorThread(self):
        if(self.threadmanager == True):
           try:
               self.threadmanager = False
               worker = Worker(self.mirrorVideo)
               worker.signals.finished.connect(self.ReleaseThread)
               self.pool.start(worker)
           except:
               print("Problem with mirror thread")
        else:
           print("A thread is already running")

    """---</Mirror>---"""

    """---<SoundReplace>---"""
    def SoundReplaceThread(self):
        if(self.threadmanager == True):
           try:
               self.threadmanager = False
               worker = Worker(self.SoundReplaceFunction)
               worker.signals.finished.connect(self.ReleaseThread)
               worker.signals.finished.connect(self.removeAudioFileFunction)
               self.pool.start(worker)
           except:
               print("Problem with SoundReplace thread")
        else:
           print("A thread is already running")

    """---</SoundReplace>---"""
    def ReleaseThread(self):
            self.threadmanager = True
            print(self.curentFiles)


    """---<GetFrame>---"""

    def GetFrameThread(self):
        if(self.threadmanager == True):
           try:
               self.threadmanager = False
               worker = Worker(self.GetFrameFunction)
               worker.signals.finished.connect(self.ReleaseThread)
               self.pool.start(worker)
           except:
               print("Problem with getFrame thread")
        else:
           print("A thread is already running")


    """---</GetFrame>---"""

    """---<AddSubtitles>---"""

    def addSubtitlesThread(self):
        if(self.threadmanager == True):
           try:
               self.threadmanager = False
               worker = Worker(self.addSubtitlesFunction)
               worker.signals.finished.connect(self.ReleaseThread)
               worker.signals.finished.connect(self.removeSubtitlesFunction)
               self.pool.start(worker)
           except:
               print("Problem with add subtitles thread")
        else:
           print("A thread is already running")


    """---</AddSubtitles>--"""

    """---------------------</Thread functions>--------------------------"""


    def deleteAllTemp(self):
        import os, shutil
        folder = ProjectFolders.tmpDir
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    def closeEvent(self, event):
            """
                Popup a dialog when the user is trying to close the main app.
            """
            reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
    				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                if(self.threadmanager == True):
                   try:
                       self.threadmanager = False
                       worker = Worker(self.deleteAllTemp)
                       worker.signals.finished.connect(self.ReleaseThread)
                       self.pool.start(worker)
                   except:
                       print("Problem with getFrame thread")
                else:
                   print("A thread is already running")

                event.accept()
                print('Window closed')
            else:
                event.ignore()


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

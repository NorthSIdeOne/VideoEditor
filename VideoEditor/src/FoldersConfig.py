import os


absFilePath = os.path.abspath(__file__)
#Files directory :\src
fileDir = os.path.dirname(os.path.abspath(__file__))
#Parent directory: \VideoEditor
parentDir = os.path.dirname(fileDir)
#resources directory:\VideoEditor\resources
resourcesDir = parentDir+r"\resources"
#Videos directory:\VideoEditor\resources\videos
videosDir = resourcesDir+"\\videos\\"



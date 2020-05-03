from PyQt5.QtCore import *
import time
import traceback, sys


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    '''
    finished = pyqtSignal()


class Worker(QRunnable):
    def __init__(self,fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        self.fn()
        self.signals.finished.emit()

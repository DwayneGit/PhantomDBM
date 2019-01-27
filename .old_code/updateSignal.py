from PyQt5.QtCore import QObject, pyqtSignal

class updateBoard(QObject):
    ''' Represents a punching bag; when you punch it, it
        emits a signal that indicates that it was punched. '''
    update = pyqtSignal(str)
 
    def __init__(self):
        QObject.__init__(self)
 
    def updateSignal(self, msg):
        ''' Punch the bag '''
        print(msg)
        self.update.emit(msg)
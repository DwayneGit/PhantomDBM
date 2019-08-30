from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import centerWindow

from . import PhtmTitleBar

class PhtmFileDialog(QDialog):
    def __init__(self, parent, title, fileMode=None, nameFilter=None, options=None, acceptMode=QFileDialog.AcceptOpen):
        super().__init__(parent) # set screen size (left, top, width, height

        # if not isinstance(centralDialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.windowTitle = title

        self.parent = parent

        self.oldPos = self.pos()
        self.acceptMode = acceptMode

        self.titleBar = PhtmTitleBar(self)
        self.titleBar.generateTitleBar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.titleBar)

        self.selectedFiles = None
        self.saveName = None
        
        self.__fileDialog = QFileDialog()
        self.__fileDialog.setOptions(options)
        self.__fileDialog.setFileMode(fileMode)
        self.__fileDialog.setNameFilter(nameFilter)
        self.__fileDialog.setAcceptMode(self.acceptMode)

        self.__fileDialog.fileSelected.connect(self.fileSelected)
        self.__fileDialog.rejected.connect(self.reject)

        self.__layout.addWidget(self.__fileDialog)

        self.setLayout(self.__layout)
        self.messageSelection = None

        # self.setGeometry(geometry)
        # self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setWindowTitle(self.windowTitle)

    def urlSelected(self, result):
            self.accept()

    def fileSelected(self, selectedFile):
        self.selectedFiles = self.__fileDialog.selectedFiles()
        if self.acceptMode == QFileDialog.AcceptSave:
            self.saveName = self.__fileDialog.selectedUrls()[0].path()
        self.accept()

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.titleBar.windowTitle

    def getLayout(self):
        return self.__layout

    def getMessageBox(self):
        return self.__fileDialog
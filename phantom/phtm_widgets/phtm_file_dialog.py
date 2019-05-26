from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import center_window

from . import PhtmTitleBar

class PhtmFileDialog(QDialog):
    def __init__(self, parent, title, file_mode=None, name_filter=None, options=None, accept_mode=QFileDialog.AcceptOpen):
        super().__init__(parent) # set screen size (left, top, width, height

        # if not isinstance(central_dialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.window_title = title

        self.parent = parent

        self.oldPos = self.pos()
        self.accept_mode = accept_mode

        self.title_bar = PhtmTitleBar(self)
        self.title_bar.generate_title_bar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.title_bar)

        self.selectedFiles = None
        self.save_name = None
        
        self.__file_dialog = QFileDialog()
        self.__file_dialog.setOptions(options)
        self.__file_dialog.setFileMode(file_mode)
        self.__file_dialog.setNameFilter(name_filter)
        self.__file_dialog.setAcceptMode(self.accept_mode)

        self.__file_dialog.fileSelected.connect(self.file_selected)
        self.__file_dialog.rejected.connect(self.reject)

        self.__layout.addWidget(self.__file_dialog)

        self.setLayout(self.__layout)
        self.msg_selection = None

        # self.setGeometry(geometry)
        # self.move(center_window(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.set_window_title(self.window_title)

    def url_selected(self, result):
            self.accept()

    def file_selected(self, selected_file):
        self.selectedFiles = self.__file_dialog.selectedFiles()
        if self.accept_mode == QFileDialog.AcceptSave:
            self.save_name = self.__file_dialog.selectedUrls()[0].path()
        self.accept()

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.title_bar.window_title

    def get_layout(self):
        return self.__layout

    def get_message_box(self):
        return self.__file_dialog
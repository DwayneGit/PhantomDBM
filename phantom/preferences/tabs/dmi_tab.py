from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QSize

from phantom.utility import text_style
from phantom.file_stuff import file_ctrl as f_ctrl
from phantom.phtm_widgets import PhtmPushButton
from phantom.phtm_widgets import PhtmPlainTextEdit

class dmi_tab(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.mw = main_window
        dmiVBox = QVBoxLayout()

        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()

        self.__dmi_editor = PhtmPlainTextEdit()
        self.__dmi_instr = self.mw.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]

        load_dmi_btn = PhtmPushButton("Open Instruction Doc")

        self.__curr_dmi = PhtmPlainTextEdit()
        self.__curr_dmi.setFixedSize(QSize(175, 31))
        self.__curr_dmi.setReadOnly(True)

        load_widget_layout.addWidget(load_dmi_btn)
        load_widget_layout.addWidget(self.__curr_dmi)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        self.__dmi_editor.setSizePolicy(spBottm)

        load_dmi_btn.clicked.connect(lambda: self.__load_dmi_instr(self.__curr_dmi, self.__dmi_editor))

        if self.__dmi_instr["instr"]:
            self.__dmi_editor.setPlainText(self.__dmi_instr["instr"])
            self.__curr_dmi.setPlainText(self.__dmi_instr["name"])
            
        dmiVBox.addWidget(load_widget)
        dmiVBox.addWidget(self.__dmi_editor)
        dmiVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(dmiVBox)

    def __load_dmi_instr(self, dmi, editor):
        name, file_path = f_ctrl.load_instructions()
        if file_path:
            dmi.setPlainText(name)
            instr = text_style.read_text(file_path)
            editor.setPlainText(instr)
            self.__dmi_instr["instr"] = instr
            self.__dmi_instr["name"] = name

    def save_dmi(self):
        self.__dmi_instr['instr'] = self.__dmi_editor.toPlainText()

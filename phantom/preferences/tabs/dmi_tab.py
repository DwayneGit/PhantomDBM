from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QSize

from phantom.utility import textStyle
from phantom.file_stuff import file_ctrl as f_ctrl
from phantom.phtmWidgets import PhtmPushButton
from phantom.phtmWidgets import PhtmPlainTextEdit

class dmi_tab(QWidget):
    def __init__(self, cluster):
        super().__init__()

        self.__cluster = cluster
        dmiVBox = QVBoxLayout()

        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()

        self.__dmi_editor = PhtmPlainTextEdit()
        self.__dmi_instr = self.__cluster.getPhmScripts()["__dmi_instr__"]

        load_dmi_btn = PhtmPushButton("Open Instruction Doc")

        self.__currDmi = PhtmPlainTextEdit()
        self.__currDmi.setFixedSize(QSize(175, 31))
        self.__currDmi.setReadOnly(True)

        load_widget_layout.addWidget(load_dmi_btn)
        load_widget_layout.addWidget(self.__currDmi)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        self.__dmi_editor.setSizePolicy(spBottm)

        load_dmi_btn.clicked.connect(lambda: self.__load_dmi_instr(self.__currDmi, self.__dmi_editor))

        if self.__dmi_instr["instr"]:
            self.__dmi_editor.setPlainText(self.__dmi_instr["instr"])
            self.__currDmi.setPlainText(self.__dmi_instr["name"])
            
        dmiVBox.addWidget(load_widget)
        dmiVBox.addWidget(self.__dmi_editor)
        dmiVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(dmiVBox)

    def __load_dmi_instr(self, dmi, editor):
        name, filePath = f_ctrl.loadInstructions()
        if filePath:
            dmi.setPlainText(name)
            instr = textStyle.readText(filePath)
            editor.setPlainText(instr)
            self.__dmi_instr["instr"] = instr
            self.__dmi_instr["name"] = name

    def save_dmi(self):
        self.__dmi_instr['instr'] = self.__dmi_editor.toPlainText()

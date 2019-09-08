from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QSize

from Phantom.Utility import TextStyle
from Phantom.file_stuff import FileHandler
from Phantom.PhtmWidgets import PhtmPushButton
from Phantom.PhtmWidgets import PhtmPlainTextEdit

class DmiTab(QWidget):
    def __init__(self, cluster):
        super().__init__()

        self.__cluster = cluster
        dmiVBox = QVBoxLayout()

        loadWidget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        loadWidget.setSizePolicy(spTop)
        loadWidgetLayout = QHBoxLayout()

        self.__dmiEditor = PhtmPlainTextEdit()
        self.__dmiInstr = self.__cluster.getPhmScripts()["__dmi_instr__"]

        loadDmiButton = PhtmPushButton("Open Instruction Doc")

        self.__currDmi = PhtmPlainTextEdit()
        self.__currDmi.setFixedSize(QSize(175, 31))
        self.__currDmi.setReadOnly(True)

        loadWidgetLayout.addWidget(loadDmiButton)
        loadWidgetLayout.addWidget(self.__currDmi)
        loadWidgetLayout.setContentsMargins(0, 0, 0, 0)

        loadWidget.setLayout(loadWidgetLayout)

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        self.__dmiEditor.setSizePolicy(spBottm)

        loadDmiButton.clicked.connect(lambda: self.__load_dmi_instr(self.__currDmi, self.__dmiEditor))

        if self.__dmiInstr["instr"]:
            self.__dmiEditor.setPlainText(self.__dmiInstr["instr"])
            self.__currDmi.setPlainText(self.__dmiInstr["name"])
            
        dmiVBox.addWidget(loadWidget)
        dmiVBox.addWidget(self.__dmiEditor)
        dmiVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(dmiVBox)

    def __load_dmi_instr(self, dmi, editor):
        name, filePath = FileHandler.loadInstructions()
        if filePath:
            dmi.setPlainText(name)
            instr = TextStyle.readText(filePath)
            editor.setPlainText(instr)
            self.__dmiInstr["instr"] = instr
            self.__dmiInstr["name"] = name

    def saveDmi(self):
        self.__dmiInstr['instr'] = self.__dmiEditor.toPlainText()

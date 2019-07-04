from PyQt5.QtWidgets import QWidget, QFormLayout, QHBoxLayout, QRadioButton, QLabel, QButtonGroup, QLineEdit

from phantom.phtm_widgets import PhtmComboBox
from phantom.phtm_widgets import PhtmPushButton

from phantom.database import DatabaseHandler

from phantom.application_settings import settings

class database_tab(QWidget):
    def __init__(self, instancesPrefDict):
        super().__init__()
        
        self.instancesPrefDict = instancesPrefDict

        self.__colList = self.__getListOfCollections()

        self.__dbForm = QFormLayout()

        dbW = QWidget()
        dbHBox = QHBoxLayout()
        self.__dbBtnGroup = QButtonGroup()

        mgButton = QRadioButton("MongoDB")
        otherButton = QRadioButton("Other")

        # if self.instancesPrefDict['db'] == 'mongodb':
        mgButton.setChecked(True)

        # elif self.instancesPrefDict['db'] == 'other':
        #     otherButton.setChecked(True)

        self.__dbBtnGroup.addButton(mgButton)
        self.__dbBtnGroup.addButton(otherButton)
        self.__dbBtnGroup.buttonReleased.connect(lambda x: self.__changeDb(self.__dbBtnGroup.checkedButton().text().lower()))

        dbHBox.addWidget(mgButton)
        dbHBox.addWidget(otherButton)

        dbLabel = QLabel("Database: ")
        dbW.setLayout(dbHBox)

        colLabel = QLabel("Collection: ")
        self.__colEditBtn = PhtmComboBox()

        self.__colEditBtn.addItems(self.__colList)
        index = self.__colEditBtn.findText(self.instancesPrefDict.get_collection_name())
        self.__colEditBtn.setCurrentIndex(index)

        self.__colEditBtn.currentTextChanged.connect(lambda a: self.__changeColl(self.__colEditBtn.currentText()))

        #------------------------------ database name --------------------------------

        dbNameLabel = QLabel("Database Name: ")
        dbNameBox = PhtmComboBox()
        dbNameBox.addItems(DatabaseHandler.getDatabaseList(self.instancesPrefDict.get_host_name(), self.instancesPrefDict.get_port_number()))

        index = dbNameBox.findText(self.instancesPrefDict.get_database_name())
        dbNameBox.setCurrentIndex(index)

        self.__dbChanged(dbNameBox.currentText())

        dbNameBox.currentTextChanged.connect(lambda x : self.__dbChanged(dbNameBox.currentText()))

        #------------------------------ Host Name --------------------------------

        hostLabel = QLabel("Host: ")
        hostBox = QLineEdit()
        hostBox.setText(str(self.instancesPrefDict.get_host_name()))
        hostBox.textChanged.connect(lambda a : self.__changeHost(hostBox.text()))

        #------------------------------ Port Number --------------------------------

        portNumLabel = QLabel("Port Number: ")
        portNumBox = QLineEdit()
        portNumBox.setText(str(self.instancesPrefDict.get_port_number()))
        portNumBox.textChanged.connect(lambda a : self.__changePort(portNumBox.text()))

        #------------------------------ database name --------------------------------

        # tbSizeLabel = QLabel("Table Size: ")
        # tbSizeBox = QLineEdit()
        # tbSizeBox.setText(str(self.instancesPrefDict['mongodb']['tableSize']))
        # tbSizeBox.textChanged.connect(lambda a : self.__changeTbSize(int(tbSizeBox.text())))

        #------------------------------ reload settings --------------------------------

        reloadBtn = PhtmPushButton('Reload')
        reloadBtn.clicked.connect(self.__reloadSettings)

        #---------------------------------- add widgets to form

        self.__dbForm.addRow(dbLabel, dbW)
        self.__dbForm.addRow(dbNameLabel, dbNameBox)
        self.__dbForm.addRow(hostLabel, hostBox)
        self.__dbForm.addRow(portNumLabel, portNumBox)
        # self.__dbForm.addRow(tbSizeLabel, tbSizeBox)
        self.__dbForm.addRow(colLabel, self.__colEditBtn)
        self.__dbForm.addWidget(reloadBtn)

        self.setLayout(self.__dbForm)

    def get_db_form(self):
        return self.__dbForm

    def __changeHost(self, host):
        self.instancesPrefDict.set_host_name(host)

    def __changePort(self, port):
        self.instancesPrefDict.set_port_number(port)

    # def __changeTbSize(self, port):
    #     self.instancesPrefDict['mongodb']['tableSize'] = port

    #----------------------- database engine ---------------------
    def __changeDb(self, engine):
        settings.__LOG__.logInfo(engine)

    #------------------------------ current collection --------------------------------
    def __changeColl(self, coll):
        if not coll:
            return

        self.instancesPrefDict.set_collection_name(coll)

        index = self.__colEditBtn.findText(self.instancesPrefDict.get_collection_name())
        self.__colEditBtn.setCurrentIndex(index)

    def __getListOfCollections(self):
        if not self.instancesPrefDict.get_database_name() or self.instancesPrefDict.get_database_name() == "":
            return []

        return DatabaseHandler.getCollectionList(self.instancesPrefDict.get_host_name(), int(self.instancesPrefDict.get_port_number()),
                                                 self.instancesPrefDict.get_database_name())

    def __reloadSettings(self):
        print(self.instancesPrefDict)

    def editCollections(self):
        print("Open Edit Collections Window")

    def __dbChanged(self, name):
        
        self.instancesPrefDict.set_database_name(name)
        self.__colList = self.__getListOfCollections()
        
        self.__colEditBtn.disconnect()

        self.__colEditBtn.clear()

        self.__colEditBtn.addItems(self.__colList)

        index = self.__colEditBtn.findText(self.instancesPrefDict.get_collection_name())
        self.__colEditBtn.setCurrentIndex(index)

        self.__colEditBtn.currentTextChanged.connect(lambda a: self.__changeColl(self.__colEditBtn.currentText()))

    def save(self):

        settings.__DATABASE__.set_database_name(self.instancesPrefDict.get_database_name())
        settings.__DATABASE__.set_collection_name(self.instancesPrefDict.get_collection_name())
        settings.__DATABASE__.set_host_name(self.instancesPrefDict.get_host_name())
        settings.__DATABASE__.set_port_number(int(self.instancesPrefDict.get_port_number()))
        
        # prefs['mongodb']['tableSize'] = int(self.__dbForm.itemAt(9).widget().text())


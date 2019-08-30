from PyQt5.QtWidgets import QWidget, QFormLayout, QHBoxLayout, QRadioButton, QLabel, QButtonGroup, QLineEdit

from phantom.phtmWidgets import PhtmComboBox
from phantom.phtmWidgets import PhtmPushButton

from phantom.database import DatabaseHandler

from phantom.applicationSettings import settings

class DatabaseTab(QWidget):
    def __init__(self, instancesPrefDict):
        super().__init__()
        
        self.instancesPrefDict = instancesPrefDict

        self.__colList = self.__getListOfCollections()

        self.__databaseForm = QFormLayout()

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
        index = self.__colEditBtn.findText(self.instancesPrefDict.getCollectionName())
        self.__colEditBtn.setCurrentIndex(index)

        self.__colEditBtn.currentTextChanged.connect(lambda a: self.__changeColl(self.__colEditBtn.currentText()))

        #------------------------------ database name --------------------------------

        dbNameLabel = QLabel("Database Name: ")
        dbNameBox = PhtmComboBox()
        dbNameBox.addItems(DatabaseHandler.getDatabaseList(self.instancesPrefDict.getHostName(), self.instancesPrefDict.getPortNumber()))

        index = dbNameBox.findText(self.instancesPrefDict.getDatabaseName())
        dbNameBox.setCurrentIndex(index)

        self.__dbChanged(dbNameBox.currentText())

        dbNameBox.currentTextChanged.connect(lambda x : self.__dbChanged(dbNameBox.currentText()))

        #------------------------------ Host Name --------------------------------

        hostLabel = QLabel("Host: ")
        hostBox = QLineEdit()
        hostBox.setText(str(self.instancesPrefDict.getHostName()))
        hostBox.textChanged.connect(lambda a : self.__changeHost(hostBox.text()))

        #------------------------------ Port Number --------------------------------

        portNumLabel = QLabel("Port Number: ")
        portNumBox = QLineEdit()
        portNumBox.setText(str(self.instancesPrefDict.getPortNumber()))
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

        self.__databaseForm.addRow(dbLabel, dbW)
        self.__databaseForm.addRow(dbNameLabel, dbNameBox)
        self.__databaseForm.addRow(hostLabel, hostBox)
        self.__databaseForm.addRow(portNumLabel, portNumBox)
        # self.__databaseForm.addRow(tbSizeLabel, tbSizeBox)
        self.__databaseForm.addRow(colLabel, self.__colEditBtn)
        self.__databaseForm.addWidget(reloadBtn)

        self.setLayout(self.__databaseForm)

    def getDatabaseForm(self):
        return self.__databaseForm

    def __changeHost(self, host):
        self.instancesPrefDict.setHostName(host)

    def __changePort(self, port):
        self.instancesPrefDict.setPortNumber(port)

    # def __changeTbSize(self, port):
    #     self.instancesPrefDict['mongodb']['tableSize'] = port

    #----------------------- database engine ---------------------
    def __changeDb(self, engine):
        settings.__LOG__.logInfo(engine)

    #------------------------------ current collection --------------------------------
    def __changeColl(self, coll):
        if not coll:
            return

        self.instancesPrefDict.setCollectionName(coll)

        index = self.__colEditBtn.findText(self.instancesPrefDict.getCollectionName())
        self.__colEditBtn.setCurrentIndex(index)

    def __getListOfCollections(self):
        if not self.instancesPrefDict.getDatabaseName() or self.instancesPrefDict.getDatabaseName() == "":
            return []

        return DatabaseHandler.getCollectionList(self.instancesPrefDict.getHostName(), int(self.instancesPrefDict.getPortNumber()),
                                                 self.instancesPrefDict.getDatabaseName())

    def __reloadSettings(self):
        print(self.instancesPrefDict)

    def editCollections(self):
        print("Open Edit Collections Window")

    def __dbChanged(self, name):
        
        self.instancesPrefDict.setDatabaseName(name)
        self.__colList = self.__getListOfCollections()
        
        self.__colEditBtn.disconnect()

        self.__colEditBtn.clear()

        self.__colEditBtn.addItems(self.__colList)

        index = self.__colEditBtn.findText(self.instancesPrefDict.getCollectionName())
        self.__colEditBtn.setCurrentIndex(index)

        self.__colEditBtn.currentTextChanged.connect(lambda a: self.__changeColl(self.__colEditBtn.currentText()))

    def save(self):

        settings.__DATABASE__.setDatabaseName(self.instancesPrefDict.getDatabaseName())
        settings.__DATABASE__.setCollectionName(self.instancesPrefDict.getCollectionName())
        settings.__DATABASE__.setHostName(self.instancesPrefDict.getHostName())
        settings.__DATABASE__.setPortNumber(int(self.instancesPrefDict.getPortNumber()))
        
        # prefs['mongodb']['tableSize'] = int(self.__databaseForm.itemAt(9).widget().text())


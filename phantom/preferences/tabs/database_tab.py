from PyQt5.QtWidgets import QWidget, QFormLayout, QHBoxLayout, QRadioButton, QLabel, QButtonGroup, QLineEdit

from phantom.phtm_widgets import PhtmComboBox
from phantom.phtm_widgets import PhtmPushButton

from phantom.database import database_handler

from phantom.application_settings import settings

class database_tab(QWidget):
    def __init__(self, prefs, instancesPrefDict):
        super().__init__()
        self.prefs = prefs
        self.instancesPrefDict = instancesPrefDict

        self.__colList = self.__getListOfCollections()

        self.__dbForm = QFormLayout()

        dbW = QWidget()
        dbHBox = QHBoxLayout()
        self.__dbBtnGroup = QButtonGroup()

        mgButton = QRadioButton("MongoDB")
        sqlButton = QRadioButton("SQL")

        if self.instancesPrefDict['db'] == 'mongodb':
            mgButton.setChecked(True)

        elif self.instancesPrefDict['db'] == 'sql':
            sqlButton.setChecked(True)

        self.__dbBtnGroup.addButton(mgButton)
        self.__dbBtnGroup.addButton(sqlButton)
        self.__dbBtnGroup.buttonReleased.connect(lambda x: self.__changeDb(self.__dbBtnGroup.checkedButton().text().lower()))

        dbHBox.addWidget(mgButton)
        dbHBox.addWidget(sqlButton)

        dbLabel = QLabel("Database: ")
        dbW.setLayout(dbHBox)

        self.__clrFlag = False

        colLabel = QLabel("Collection: ")
        self.__colEditBtn = PhtmComboBox()

        self.__colEditBtn.addItems(self.__colList)
        index = self.__colEditBtn.findText(self.prefs['mongodb']['collection'])
        self.__colEditBtn.setCurrentIndex(index)

        self.__colEditBtn.currentTextChanged.connect(lambda a : self.__changeColl(self.__colEditBtn.currentText()))

        #------------------------------ database name --------------------------------

        dbNameLabel = QLabel("Database Name: ")
        dbNameBox = PhtmComboBox()
        dbNameBox.addItems(database_handler.getDatabaseList(self.prefs['mongodb']['host'],self.prefs['mongodb']['port']))

        index = dbNameBox.findText(self.prefs['mongodb']['dbname'])
        dbNameBox.setCurrentIndex(index)

        self.__dbChanged(dbNameBox.currentText())

        dbNameBox.currentTextChanged.connect(lambda x : self.__dbChanged(dbNameBox.currentText()))

        #------------------------------ Host Name --------------------------------

        hostLabel = QLabel("Host: ")
        hostBox = QLineEdit()
        hostBox.setText(str(self.instancesPrefDict['mongodb']['host']))
        hostBox.textChanged.connect(lambda a : self.__changeHost(hostBox.text()))

        #------------------------------ Port Number --------------------------------

        portNumLabel = QLabel("Port Number: ")
        portNumBox = QLineEdit()
        portNumBox.setText(str(self.instancesPrefDict['mongodb']['port']))
        portNumBox.textChanged.connect(lambda a : self.__changePort(portNumBox.text()))

        #------------------------------ database name --------------------------------

        tbSizeLabel = QLabel("Table Size: ")
        tbSizeBox = QLineEdit()
        tbSizeBox.setText(str(self.instancesPrefDict['mongodb']['tableSize']))
        tbSizeBox.textChanged.connect(lambda a : self.__changeTbSize(int(tbSizeBox.text())))

        #------------------------------ reload settings --------------------------------

        reloadBtn = PhtmPushButton('Reload')
        reloadBtn.clicked.connect(self.__reloadSettings)

        #---------------------------------- add widgets to form

        self.__dbForm.addRow(dbLabel, dbW)
        self.__dbForm.addRow(dbNameLabel, dbNameBox)
        self.__dbForm.addRow(hostLabel, hostBox)
        self.__dbForm.addRow(portNumLabel, portNumBox)
        self.__dbForm.addRow(tbSizeLabel, tbSizeBox)
        self.__dbForm.addRow(colLabel, self.__colEditBtn)
        self.__dbForm.addWidget(reloadBtn)

        self.setLayout(self.__dbForm)

    def get_db_form(self):
        return self.__dbForm

    def __changeHost(self, host):
        self.instancesPrefDict['mongodb']['host']=host

    def __changePort(self, port):
        self.instancesPrefDict['mongodb']['port'] = port 

    def __changeTbSize(self,port):
        self.instancesPrefDict['mongodb']['tableSize'] = port 

    #----------------------- database engine ---------------------
    def __changeDb(self, engine):
        self.instancesPrefDict['db']=engine

    #------------------------------ current collection --------------------------------
    def __changeColl(self, coll):
        if coll == "" or coll==None:
            return
        elif self.__clrFlag == True:
            self.__clrFlag = False
            return

        self.instancesPrefDict['mongodb']['collection'] = coll

        index = self.__colEditBtn.findText(self.prefs['mongodb']['collection'])
        self.__colEditBtn.setCurrentIndex(index)

    def __getListOfCollections(self):
        if not self.prefs['mongodb']['dbname'] or self.prefs['mongodb']['dbname']=="":
            return []

        return database_handler.getCollectionList(self.prefs['mongodb']['host'], self.prefs['mongodb']['port'], self.prefs['mongodb']['dbname'])

    def __reloadSettings(self):
        print(self.instancesPrefDict)

    def editCollections(self):
        print("Open Edit Collections Window")

    def __dbChanged(self, name):

        self.instancesPrefDict['mongodb']['dbname']=name
        self.__colList = self.__getListOfCollections()

        self.__clrFlag = True
        self.__colEditBtn.clear()

        self.__colEditBtn.addItems(self.__colList)

        index = self.__colEditBtn.findText(self.prefs['mongodb']['collection'])
        self.__colEditBtn.setCurrentIndex(index)

    def save(self, prefs):
        if prefs['db'] == "mongodb":
            prefs['mongodb']['dbname'] = self.__dbForm.itemAt(3).widget().currentText()
            prefs['mongodb']['collection'] = self.__dbForm.itemAt(11).widget().currentText()
            prefs['mongodb']['host'] = self.__dbForm.itemAt(5).widget().text()
            prefs['mongodb']['port'] = int(self.__dbForm.itemAt(7).widget().text())
            prefs['mongodb']['tableSize'] = int(self.__dbForm.itemAt(9).widget().text())

        elif prefs['db'] == "sql":
            pass

        return prefs

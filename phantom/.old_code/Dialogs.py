from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from Center import center
from collections import OrderedDict
from DatabaseHandler import DatabaseHandler
from Preferences import Preferences

class addCollectionDialog(QDialog):
    def __init__ (self, dbData, parent = None):
        super(addCollectionDialog, self).__init__(parent)

        self.dbData = dbData
        #print(self.dbData)

        self.setWindowTitle("Add Collection")
        self.setWindowModality(Qt.ApplicationModal)

        createButton = QPushButton("Create Collection")
        createButton.clicked.connect(self.createCollection(self))

        vBox = QVBoxLayout()
        self.fLayout = QFormLayout()

        l2 = QLabel("Collection Name:")
        add1 = QLineEdit()

        addButton = QPushButton("Add Key")
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        
        addButton.clicked.connect(self.getKeyName)

        self.fLayout.addRow(l2, add1)
        self.fLayout.addRow(addButton, cancelButton)

        wid = QWidget()
        wid.setLayout(self.fLayout)

        vBox.addWidget(wid)
        vBox.addWidget(createButton)

        self.setLayout(vBox)

    '''
    getKeyName(self):
    creates a dialog box which prompts user for
    the name of the field to be added to collection
    then calls add key. window closes when key is added or canceled
    '''
    @pyqtSlot()
    def getKeyName(self):
        getNameDialog = QDialog()

        self.keyLine = QLineEdit()

        addB = QPushButton("Add", self)
        addB.clicked.connect(self.addKey(getNameDialog))
        
        cancelB = QPushButton("Cancel")
        cancelB.clicked.connect(getNameDialog.reject)

        instruct = QLabel("Enter the name of the key to add to collection: ")

        vBox = QVBoxLayout()
        formL = QFormLayout()

        formL.addRow(addB,cancelB)

        widget = QWidget()
        widget.setLayout(formL)

        vBox.addWidget(instruct)
        vBox.addWidget(self.keyLine)
        vBox.addWidget(widget)

        getNameDialog.setLayout(vBox)

        getNameDialog.exec_()
        return 0

    '''
    addKey(self, dialog):
    gets the name from the dialog box and adds it 
    to the form layout in the add collection dialog box
    with radio button options
    '''
    @pyqtSlot()
    def addKey(self, dialog): #a function must be returned to connect
        def forButtonConnect(): #create a function to return so the button is able to connect with the main function
            label = QLabel(self.keyLine.text())

            buttonBox = QHBoxLayout()
            buttonWidget = QWidget()

            lstRButton = QCheckBox("Lst")
            strRButton = QCheckBox("Str")
            numRButton = QCheckBox("Num")
            boolRButton = QCheckBox("Bool")

            buttonBox.addWidget(lstRButton)
            buttonBox.addWidget(strRButton)
            buttonBox.addWidget(numRButton)
            buttonBox.addWidget(boolRButton)

            buttonWidget.setLayout(buttonBox)

            self.fLayout.insertRow(int(self.fLayout.count()/2-1),label, buttonWidget)
            dialog.close()
            
        return forButtonConnect

    '''
    createCollection:
    creates and ordered dictionary that is a model of the new colletion
    fields are added to collection with with name given by user
    and the option of bool, num or str.closeare selected str is set by default
    '''
    @pyqtSlot()
    def createCollection(self, dialog):
        def forButtonConnect():
            #print(self.fLayout.count())

            self.modelDict = OrderedDict()

            self.collectionName = self.fLayout.itemAt(1).widget().text()
            self.modelDict['_id'] = "__Model__" #id named model so it is easily avioded when managing database

            for i in range( 4, self.fLayout.count(),2):
                key = self.fLayout.itemAt(i).widget().text()
                isList = False
                #print(key)
                rButtonLay = self.fLayout.itemAt(i+1).widget().layout()
                self.modelDict[key] = ""
                for i in range(rButtonLay.count()):
                    if rButtonLay.itemAt(i).widget().isChecked():
                        if rButtonLay.itemAt(i).widget().text() == "Lst":
                            isList = True
                        else:
                            self.modelDict[key] += rButtonLay.itemAt(i).widget().text()

                if isList:
                    self.modelDict[key] = "[" + self.modelDict[key] + "]"

                if self.modelDict[key] == "":
                    self.modelDict[key] = "Str"

            #print(self.modelDict)

            dbHandler = DatabaseHandler(self.dbData)
            dbHandler.createCollection(self.collectionName, self.modelDict)

            dialog.accept()

        return forButtonConnect


class PreferencesDialog(QDialog):
    def __init__(self, prefs, user, parent = None):
        super(PreferencesDialog, self).__init__(parent)
        '''
        Initialize the window
        '''
        self.prefs = prefs
        self.prefDict = prefs.prefDict
        self.user = user
        self.svd = False
        self.initUI()
        
    
    def initUI(self):
        #Window initial size

        self.setGeometry(10,10,350, 475)

        #Window title
        self.setWindowTitle("Preferences")
        self.setWindowModality(Qt.ApplicationModal)

        vBox = QVBoxLayout()

        tabW = QTabWidget(self)
        tabW.setTabPosition(QTabWidget.North)

        tabW.addTab(self.databaseTab(),"Database")
        tabW.addTab(self.webTab(),"Web")
        tabW.addTab(self.userTab(),"User")
        tabW.addTab(self.themeTab(),"Theme")

        vBox.addWidget(tabW)
        vBox.addWidget(self.buttons())

        self.setLayout(vBox)

        self.move(center(self))

    def buttons(self):
        btnWidget = QWidget()
        btnLayout = QHBoxLayout()

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.savePreferences)
        
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(self.submitPreferences)
        
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelPreferences)

        btnLayout.addWidget(saveButton)
        btnLayout.addWidget(submitButton)
        btnLayout.addWidget(cancelButton)

        btnWidget.setLayout(btnLayout)
        return btnWidget

    def savePreferences(self):
        print("Saving Preferences ...")
        self.svd = True

    def submitPreferences(self):
        self.savePreferences()
        self.accept()

    def cancelPreferences(self):
        if self.svd == True:
            print("closeing with true")
            self.reject() #if canceled with out previously being saved
        else:
            self.accept()

    def databaseTab(self):

        dbPrefWidget = QWidget()
        form = QFormLayout()

        dbW = QWidget()
        dbHBox = QHBoxLayout()
        mgButton = QRadioButton("MongoDB")
        sqlButton = QRadioButton("MySQL")

        if self.prefDict['db'] == 'mongodb':
            mgButton.setChecked(True)

        elif self.prefDict['db'] == 'mysql':
            sqlButton.setChecked(True)

        dbHBox.addWidget(mgButton)
        dbHBox.addWidget(sqlButton)

        dbLabel = QLabel("Database: ")
        dbW.setLayout(dbHBox)
        form.addRow(dbLabel, dbW)

        dbNameLabel = QLabel("Database Name: ")
        dbNameBox = QLineEdit()
        dbNameBox.setText(str(self.prefDict['mongodb']['dbname']))
        form.addRow(dbNameLabel, dbNameBox)
        
        hostLabel = QLabel("Host: ")
        hostBox = QLineEdit()
        hostBox.setText(str(self.prefDict['mongodb']['host']))
        form.addRow(hostLabel, hostBox)
        
        portNumLabel = QLabel("PortNumber: ")
        portNumBox = QLineEdit()
        portNumBox.setText(str(self.prefDict['mongodb']['port']))
        form.addRow(portNumLabel, portNumBox)
        
        tbSizeLabel = QLabel("Table Size: ")
        tbSizeBox = QLineEdit()
        tbSizeBox.setText(str(self.prefDict['mongodb']['tableSize']))
        form.addRow(tbSizeLabel, tbSizeBox)

        colEditBtn = QPushButton("Edit Collections")
        colEditBtn.clicked.connect(self.editCollections)
        form.addWidget(colEditBtn)

        dbPrefWidget.setLayout(form)
        
        return dbPrefWidget

    def editCollections(self):
        print("Open Edit Collections Window")

    def webTab(self):
        webPrefWidget = QWidget()

        return webPrefWidget

    def userTab(self):
        usrPrefWidget = QWidget()
        form = QFormLayout()

        accessLabel = QLabel("Access Level: ")
        access = QLabel(self.user.access)
        form.addRow(accessLabel, access)
        
        userLabel = QLabel("Username: ")
        username = QLabel(self.user.username)
        form.addRow(userLabel, username)
        
        passwordLabel = QLabel("Password: ")
        password = QLabel(''.join([char*len(self.user.password) for char in '*']))
        form.addRow(passwordLabel, password)
        
        password = QPushButton("Change Password")
        form.addWidget(password)
        mngAccessBtn = QPushButton("Manage Access Levels")
        mngAccessBtn.clicked.connect(self.mngAccess)
        form.addWidget(mngAccessBtn)
        manageDbs = QPushButton("Manage Database Access")
        manageDbs.clicked.connect(self.mngUsers)
        form.addWidget(manageDbs)

        usrPrefWidget.setLayout(form)
        return usrPrefWidget

    def mngAccess(self):
        if self.user.access.lower() == "admin":
            db = self.prefDict['mongodb']['dbname']
            mngAcessDialog = QDialog()

            form = QFormLayout()

            usrLabel = QLabel("Users: ")
            usrDropMenu = QComboBox()
            acsDropMenu = QComboBox()
            users = User.getUserList(self.prefDict['mongodb']['dbname'])
            #print(users)
            def getAccesses():
                acsDropMenu.clear()
                for acs in ["Admin","ReadWrite","Monitor"]:
                    if "all" in users[usrDropMenu.currentText()]["database"].keys():
                        if not acs == users[usrDropMenu.currentText()]["database"]["all"]:
                            acsDropMenu.addItem(acs)
                    elif not acs == users[usrDropMenu.currentText()]["database"][db]:
                        acsDropMenu.addItem(acs)

            usrDropMenu.addItems(users.keys())
            usrDropMenu.currentIndexChanged.connect(getAccesses)
            form.addRow(usrLabel, usrDropMenu)

            acsLabel = QLabel("Access: ")
            getAccesses()
            form.addRow(acsLabel, acsDropMenu)

            submitBtn = QPushButton("Submit")
            submitBtn.clicked.connect(mngAcessDialog.accept)

            cancelBtn = QPushButton("Cancel")
            cancelBtn.clicked.connect(mngAcessDialog.reject)
            form.addRow(submitBtn, cancelBtn)

            mngAcessDialog.setLayout(form)

            mngAcessDialog.exec_()

    def mngUsers(self):
        if self.user.access.lower() == "admin":
            db = self.prefDict['mongodb']['dbname']
            mngUsersDialog = QDialog()

            form = QFormLayout()

            usrLabel = QLabel("Users: ")
            usrDropMenu = QComboBox()
            acsDropMenu = QComboBox()
            users = User.getUserList()
            usersdb = User.getUserList(self.prefDict['mongodb']['dbname'])
            #print(users)
            def getUsers():
                ret = []
                for acs in users.keys():
                    if ("all" not in users[acs]["database"].keys() and self.user.db not in users[acs]["database"].keys()):
                        if not acs == self.user.username:
                            ret.append(acs)
                return ret

            adminLabel = QLabel("Admin: ")
            adminNameLabel = QLabel(self.user.username)
            form.addRow(adminLabel, adminNameLabel)

            usr = getUsers()
            if len(usr) <= 0:
                return

            usrDropMenu.addItems(usr)
            form.addRow(usrLabel, usrDropMenu)

            acsLabel = QLabel("Access: ")
            acsDropMenu.addItems(["Admin","ReadWrite","Monitor"])
            form.addRow(acsLabel, acsDropMenu)

            submitBtn = QPushButton("Add")
            submitBtn.clicked.connect(mngUsersDialog.accept)

            cancelBtn = QPushButton("Cancel")
            cancelBtn.clicked.connect(mngUsersDialog.reject)
            form.addRow(submitBtn, cancelBtn)

            mngUsersDialog.setLayout(form)

            mngUsersDialog.exec_()

    def newPassword(self):
        return True

    def themeTab(self):
        thmPrefWidget = QWidget()

        return thmPrefWidget

    def loadPreferences(self):
        return 0
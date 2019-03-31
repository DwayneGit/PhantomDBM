from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

from Center import center_window
from Preferences import *
from DBConnection import *

from phtm_widgets.phtm_push_button import phtm_push_button
from phtm_widgets.phtm_combo_box import phtm_combo_box
from phtm_widgets.phtm_tab_widget import phtm_tab_widget

class preference_body(QDialog):
    def __init__(self, user, log, parent):
        super(preference_body, self).__init__()
        '''
        Initialize the window
        '''
        
        self.prefDict = parent.parent.dbData
        print(self.prefDict)
        self.user = user
        self.svd = False
        self.log = log
        self.parent = parent
        
        self.loadPreferences()

        self.initUI()

    def loadPreferences(self):
        self.prefs = Preferences('config', self.log, prefDict = DefaultGeneralConfig.prefDict) # name of preference file minus json
        self.prefs.loadConfig()
        self.prefDict = self.prefs.prefDict
        self.instancesPrefDict = self.prefDict
           
        self.colList = self.getListOfCollections()

    def getWindowTitle(self):
        return self.parent.getWindowTitle()

    def set_window_title(self, text):
        self.parent.set_window_title(text)

    def getListOfCollections(self):
        
        if not self.prefDict['mongodb']['dbname'] or self.prefDict['mongodb']['dbname']=="":
            return []

        return DatabaseHandler.getCollectionList(self.prefDict['mongodb']['host'], self.prefDict['mongodb']['port'], self.prefDict['mongodb']['dbname'])


    def initUI(self):
        #Window initial size

        #Window title

        vBox = QVBoxLayout()

        tabW = phtm_tab_widget(self)
        tabW.setTabPosition(QTabWidget.North)

        tabW.addTab(self.databaseTab(),"Database")
        tabW.addTab(self.apiTab(),"API")
        tabW.addTab(self.userTab(),"User")
        tabW.addTab(self.themeTab(),"Theme")

        vBox.addWidget(tabW)
        vBox.addWidget(self.buttons())

        self.setLayout(vBox)

    def buttons(self):
        btnWidget = QWidget()
        btnLayout = QHBoxLayout()

        saveButton = phtm_push_button("Save")
        saveButton.clicked.connect(self.savePreferences)
        
        submitButton = phtm_push_button("Submit")
        submitButton.clicked.connect(self.submitPreferences)
        
        cancelButton = phtm_push_button("Cancel")
        cancelButton.clicked.connect(self.cancelPreferences)

        btnLayout.addWidget(saveButton)
        btnLayout.addWidget(submitButton)
        btnLayout.addWidget(cancelButton)

        btnWidget.setLayout(btnLayout)
        return btnWidget

    def savePreferences(self):
        print("Saving Preferences ...")
        self.saveDbTab()
        self.svd = True

    def saveDbTab(self):
        # self.prefDict['db'] = self.dbBtnGroup.checkedButton().text().lower()
        # print(self.dbBtnGroup.checkedButton().text().lower())
        if self.prefDict['db'] == "mongodb":
            self.prefDict['mongodb']['dbname'] = self.dbForm.itemAt(3).widget().currentText()
            print(self.prefDict['mongodb']['dbname'])

            self.prefDict['mongodb']['collection'] = self.dbForm.itemAt(11).widget().currentText()
            print(self.prefDict['mongodb']['collection'])

            self.prefDict['mongodb']['host'] = self.dbForm.itemAt(5).widget().text()
            print(self.prefDict['mongodb']['host'])

            self.prefDict['mongodb']['port'] = int(self.dbForm.itemAt(7).widget().text())
            print(self.prefDict['mongodb']['port'])

            self.prefDict['mongodb']['tableSize'] = int(self.dbForm.itemAt(9).widget().text())
            print(self.prefDict['mongodb']['tableSize'])



        elif self.prefDict['db'] == "sql":
            pass

        self.prefs.saveConfig()
        
        # items = (self.dbForm.itemAt(i) for i in range(self.dbForm.count())) 
        # for w in range(3, 12, 2):
        #     widget = self.dbForm.itemAt(w).widget()
        #     if isinstance(widget, phtm_combo_box):
        #         # print(widget.currentIndex())
        #         print(widget.currentText())
        #     else:
        #         print(widget.text())



        # pass

    def submitPreferences(self):
        self.savePreferences()
        self.parent.accept()

    def cancelPreferences(self):
        if self.svd == False:
            print("closeing with false")
            self.parent.reject() #if canceled with out previously being saved
        else:
            self.parent.accept()

    def databaseTab(self):

        dbPrefWidget = QWidget()
        self.dbForm = QFormLayout()
        #----------------------- database engine ---------------------
        def changeDb(engine):
            self.instancesPrefDict['db']=engine

        dbW = QWidget()
        dbHBox = QHBoxLayout()
        self.dbBtnGroup = QButtonGroup()

        mgButton = QRadioButton("MongoDB")
        sqlButton = QRadioButton("SQL")

        if self.instancesPrefDict['db'] == 'mongodb':
            mgButton.setChecked(True)

        elif self.instancesPrefDict['db'] == 'sql':
            sqlButton.setChecked(True)

        self.dbBtnGroup.addButton(mgButton)
        self.dbBtnGroup.addButton(sqlButton)
        self.dbBtnGroup.buttonReleased.connect(lambda x: changeDb(self.dbBtnGroup.checkedButton().text().lower()))

        dbHBox.addWidget(mgButton)
        dbHBox.addWidget(sqlButton)

        dbLabel = QLabel("Database: ")
        dbW.setLayout(dbHBox)


        #------------------------------ current collection --------------------------------
        def changeColl(coll):
            if coll == "" or coll==None:
                return
            elif self.clrFlag == True:
                self.clrFlag = False
                return
            
            self.instancesPrefDict['mongodb']['collection'] = coll

            index = colEditBtn.findText(self.prefDict['mongodb']['collection'])
            colEditBtn.setCurrentIndex(index)

        def dbChanged(name):

            self.instancesPrefDict['mongodb']['dbname']=name
            self.colList = self.getListOfCollections()

            self.clrFlag = True
            colEditBtn.clear()

            colEditBtn.addItems(self.colList)

            index = colEditBtn.findText(self.prefDict['mongodb']['collection'])
            colEditBtn.setCurrentIndex(index)
            
        self.clrFlag = False

        colLabel = QLabel("Collection: ")
        colEditBtn = phtm_combo_box()

        colEditBtn.addItems(self.colList)
        index = colEditBtn.findText(self.prefDict['mongodb']['collection'])
        colEditBtn.setCurrentIndex(index)

        colEditBtn.currentTextChanged.connect(lambda a : changeColl(colEditBtn.currentText()))

        #------------------------------ database name --------------------------------
       
        dbNameLabel = QLabel("Database Name: ")
        dbNameBox = phtm_combo_box()
        dbNameBox.addItems(DatabaseHandler.getDatabaseList(self.prefs.prefDict['mongodb']['host'],self.prefs.prefDict['mongodb']['port']))
        
        index = dbNameBox.findText(self.prefDict['mongodb']['dbname'])
        dbNameBox.setCurrentIndex(index)

        dbChanged(dbNameBox.currentText())

        dbNameBox.currentTextChanged.connect(lambda x : dbChanged(dbNameBox.currentText()))

        #------------------------------ Host Name --------------------------------
        def changeHost(host):
            self.instancesPrefDict['mongodb']['host']=host

        hostLabel = QLabel("Host: ")
        hostBox = QLineEdit()
        hostBox.setText(str(self.instancesPrefDict['mongodb']['host']))
        hostBox.textChanged.connect(lambda a : changeHost(hostBox.text()))
        
        #------------------------------ Port Number --------------------------------
        def changePort(port):
            self.instancesPrefDict['mongodb']['port'] = port 

        portNumLabel = QLabel("Port Number: ")
        portNumBox = QLineEdit()
        portNumBox.setText(str(self.instancesPrefDict['mongodb']['port']))
        portNumBox.textChanged.connect(lambda a : changePort(portNumBox.text()))

        #------------------------------ database name --------------------------------
        def changeTbSize(port):
            self.instancesPrefDict['mongodb']['tableSize'] = port 
        
        tbSizeLabel = QLabel("Table Size: ")
        tbSizeBox = QLineEdit()
        tbSizeBox.setText(str(self.instancesPrefDict['mongodb']['tableSize']))
        tbSizeBox.textChanged.connect(lambda a : changeTbSize(int(tbSizeBox.text())))

        #------------------------------ reload settings --------------------------------

        reloadBtn = phtm_push_button('Reload')
        reloadBtn.clicked.connect(self.reloadSettings)

        #---------------------------------- add widgets to form

        self.dbForm.addRow(dbLabel, dbW)
        self.dbForm.addRow(dbNameLabel, dbNameBox)
        self.dbForm.addRow(hostLabel, hostBox)
        self.dbForm.addRow(portNumLabel, portNumBox)
        self.dbForm.addRow(tbSizeLabel, tbSizeBox)
        self.dbForm.addRow(colLabel, colEditBtn)
        self.dbForm.addWidget(reloadBtn)

        dbPrefWidget.setLayout(self.dbForm)     

        return dbPrefWidget

    def reloadSettings(self):
        print(self.instancesPrefDict)

    def editCollections(self):
        print("Open Edit Collections Window")

    def apiTab(self):
        apiPrefWidget = QWidget()

        return apiPrefWidget

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
        
        password = phtm_push_button("Change Password")
        form.addWidget(password)
        mngAccessBtn = phtm_push_button("Manage Access Levels")
        mngAccessBtn.clicked.connect(self.mngAccess)
        form.addWidget(mngAccessBtn)
        manageDbs = phtm_push_button("Manage Database Access")
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
            usrDropMenu = phtm_combo_box()
            acsDropMenu = phtm_combo_box()
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

            submitBtn = phtm_push_button("Submit")
            submitBtn.clicked.connect(mngAcessDialog.accept)

            cancelBtn = phtm_push_button("Cancel")
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
            usrDropMenu = phtm_combo_box()
            acsDropMenu = phtm_combo_box()
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

            submitBtn = phtm_push_button("Add")
            submitBtn.clicked.connect(mngUsersDialog.accept)

            cancelBtn = phtm_push_button("Cancel")
            cancelBtn.clicked.connect(mngUsersDialog.reject)
            form.addRow(submitBtn, cancelBtn)

            mngUsersDialog.setLayout(form)

            mngUsersDialog.exec_()

    def newPassword(self):
        return True

    def themeTab(self):
        thmPrefWidget = QWidget()

        return thmPrefWidget
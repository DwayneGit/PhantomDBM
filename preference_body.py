from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

from Center import center_window
from Preferences import *
from database.DBConnection import *

import file_ctrl as f_ctrl
import text_style as text_style

from phtm_widgets.phtm_push_button import phtm_push_button
from phtm_widgets.phtm_combo_box import phtm_combo_box
from phtm_widgets.phtm_tab_widget import phtm_tab_widget
from phtm_widgets.phtm_plain_text_edit import phtm_plain_text_edit

class preference_body(QDialog):
    def __init__(self, user, log, parent):
        super(preference_body, self).__init__()
        '''
        Initialize the window
        '''
        
        # self.prefDict = parent.parent.dbData
        # print(self.prefDict)
        self.user = user
        self.svd = False
        self.log = log
        self.parent = parent
        
        self.prefs = self.parent.parent.get_editor_widget().get_cluster().get_settings()
        self.dmi_instr = self.parent.parent.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]

        self.instancesPrefDict = self.prefs
        self.colList = self.getListOfCollections()


        self.initUI()

    def getWindowTitle(self):
        return self.parent.getWindowTitle()

    def set_window_title(self, text):
        self.parent.set_window_title(text)

    def getListOfCollections(self):
        
        if not self.prefs['mongodb']['dbname'] or self.prefs['mongodb']['dbname']=="":
            return []

        return database_handler.getCollectionList(self.prefs['mongodb']['host'], self.prefs['mongodb']['port'], self.prefs['mongodb']['dbname'])


    def initUI(self):
        #Window initial size

        #Window title

        vBox = QVBoxLayout()

        self.tabW = phtm_tab_widget(self)
        self.tabW.setTabPosition(QTabWidget.North)

        self.tabW.addTab(self.databaseTab(), "Database")
        self.tabW.addTab(self.dmiTab(), "DMI")
        # self.tabW.addTab(self.userTab(), "User")
        self.tabW.addTab(self.themeTab(), "Theme")

        vBox.addWidget(self.tabW)
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
        # print("Saving Preferences ...")
        self.saveDbTab()
        self.svd = True

    def saveDbTab(self):
        # self.prefs['db'] = self.dbBtnGroup.checkedButton().text().lower()
        # print(self.dbBtnGroup.checkedButton().text().lower())
        if self.prefs['db'] == "mongodb":
            self.prefs['mongodb']['dbname'] = self.dbForm.itemAt(3).widget().currentText()
            # print(self.prefs['mongodb']['dbname'])

            self.prefs['mongodb']['collection'] = self.dbForm.itemAt(11).widget().currentText()
            # print(self.prefs['mongodb']['collection'])

            self.prefs['mongodb']['host'] = self.dbForm.itemAt(5).widget().text()
            # print(self.prefs['mongodb']['host'])

            self.prefs['mongodb']['port'] = int(self.dbForm.itemAt(7).widget().text())
            # print(self.prefs['mongodb']['port'])

            self.prefs['mongodb']['tableSize'] = int(self.dbForm.itemAt(9).widget().text())
            # print(self.prefs['mongodb']['tableSize'])

        elif self.prefs['db'] == "sql":
            pass

        # print(self.dmi_instr["filepath"])

        self.parent.parent.get_editor_widget().get_cluster().save_settings(self.prefs)
        self.parent.prefs = self.prefs 
        
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
            # print("closeing with false")
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

            index = colEditBtn.findText(self.prefs['mongodb']['collection'])
            colEditBtn.setCurrentIndex(index)

        def dbChanged(name):

            self.instancesPrefDict['mongodb']['dbname']=name
            self.colList = self.getListOfCollections()

            self.clrFlag = True
            colEditBtn.clear()

            colEditBtn.addItems(self.colList)

            index = colEditBtn.findText(self.prefs['mongodb']['collection'])
            colEditBtn.setCurrentIndex(index)
            
        self.clrFlag = False

        colLabel = QLabel("Collection: ")
        colEditBtn = phtm_combo_box()

        colEditBtn.addItems(self.colList)
        index = colEditBtn.findText(self.prefs['mongodb']['collection'])
        colEditBtn.setCurrentIndex(index)

        colEditBtn.currentTextChanged.connect(lambda a : changeColl(colEditBtn.currentText()))

        #------------------------------ database name --------------------------------
       
        dbNameLabel = QLabel("Database Name: ")
        dbNameBox = phtm_combo_box()
        dbNameBox.addItems(database_handler.getDatabaseList(self.prefs['mongodb']['host'],self.prefs['mongodb']['port']))
        
        index = dbNameBox.findText(self.prefs['mongodb']['dbname'])
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

    def dmiTab(self):

        def __load_dmi_instr(dmi, editor):
            name, file_path = f_ctrl.load_instructions()
            dmi.setPlainText(name)
            if file_path:
                instr = text_style.read_text(file_path)
                editor.setPlainText(instr)
                self.dmi_instr["instr"] = instr
                self.dmi_instr["name"] = name
            # print(self.dmi_instr["filepath"])

        dmiPrefWidget = QWidget()
        dmiVBox = QVBoxLayout()

        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()
        # load_widget_layout.setSpacing(2)

        load_dmi_btn = phtm_push_button("Open Instruction Doc")

        self.curr_dmi = phtm_plain_text_edit()
        self.curr_dmi.setFixedSize(QSize(175,31))
        self.curr_dmi.setReadOnly(True)
        
        load_widget_layout.addWidget(load_dmi_btn)
        load_widget_layout.addWidget(self.curr_dmi)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        dmi_editor = phtm_plain_text_edit()
        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        dmi_editor.setSizePolicy(spBottm)
        
        load_dmi_btn.clicked.connect(lambda: __load_dmi_instr(self.curr_dmi, dmi_editor))

        if self.dmi_instr["instr"]:
            dmi_editor.setPlainText(self.dmi_instr["instr"])
            self.curr_dmi.setPlainText(self.dmi_instr["name"])
            

        dmiVBox.addWidget(load_widget)
        dmiVBox.addWidget(dmi_editor)
        dmiVBox.setContentsMargins(0, 0, 0, 0)

        dmiPrefWidget.setLayout(dmiVBox)
            
        return dmiPrefWidget

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
            db = self.prefs['mongodb']['dbname']
            mngAcessDialog = QDialog()

            form = QFormLayout()

            usrLabel = QLabel("Users: ")
            usrDropMenu = phtm_combo_box()
            acsDropMenu = phtm_combo_box()
            users = User.getUserList(self.prefs['mongodb']['dbname'])
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
            db = self.prefs['mongodb']['dbname']
            mngUsersDialog = QDialog()

            form = QFormLayout()

            usrLabel = QLabel("Users: ")
            usrDropMenu = phtm_combo_box()
            acsDropMenu = phtm_combo_box()
            users = User.getUserList()
            usersdb = User.getUserList(self.prefs['mongodb']['dbname'])
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
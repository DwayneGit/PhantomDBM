from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

from phantom.phtm_widgets import PhtmPushButton
from phantom.phtm_widgets import PhtmComboBox

from phantom.users import Users

class user_tab(QWidget):
    def __init__(self):
        super().__init__()
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

        password = PhtmPushButton("Change Password")
        form.addWidget(password)
        mngAccessBtn = PhtmPushButton("Manage Access Levels")
        mngAccessBtn.clicked.connect(self.__mngAccess)
        form.addWidget(mngAccessBtn)
        manageDbs = PhtmPushButton("Manage Database Access")
        manageDbs.clicked.connect(self.__mngUsers)
        form.addWidget(manageDbs)

        self.setLayout(form)

    def __mngAccess(self):
        if self.user.access.lower() == "admin":
            db = self.prefs['mongodb']['dbname']
            mngAcessDialog = QDialog()

            form = QFormLayout()

            usrLabel = QLabel("Users: ")
            usrDropMenu = PhtmComboBox()
            acsDropMenu = PhtmComboBox()
            users = Users.getUserList(self.prefs['mongodb']['dbname'])
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

            submitBtn = PhtmPushButton("Submit")
            submitBtn.clicked.connect(mngAcessDialog.accept)

            cancelBtn = PhtmPushButton("Cancel")
            cancelBtn.clicked.connect(mngAcessDialog.reject)
            form.addRow(submitBtn, cancelBtn)

            mngAcessDialog.setLayout(form)

            mngAcessDialog.exec_()

    def __mngUsers(self):
        if self.user.access.lower() == "admin":
            db = self.prefs['mongodb']['dbname']
            mngUsersDialog = QDialog()

            form = QFormLayout()

            usrLabel = QLabel("Users: ")
            usrDropMenu = PhtmComboBox()
            acsDropMenu = PhtmComboBox()
            users = Users.getUserList()
            usersdb = Users.getUserList(self.prefs['mongodb']['dbname'])
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

            submitBtn = PhtmPushButton("Add")
            submitBtn.clicked.connect(mngUsersDialog.accept)

            cancelBtn = PhtmPushButton("Cancel")
            cancelBtn.clicked.connect(mngUsersDialog.reject)
            form.addRow(submitBtn, cancelBtn)

            mngUsersDialog.setLayout(form)

            mngUsersDialog.exec_()

    def __newPassword(self):
        return True

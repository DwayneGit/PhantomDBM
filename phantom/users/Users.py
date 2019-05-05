import json
import os.path

from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFormLayout, QWidget, QVBoxLayout, QComboBox

from phantom.utility import center_window

from phantom.phtm_widgets import PhtmPushButton

class User:
    __usrFile = "users.json"
    @staticmethod
    def createUser(usr):
        usrs = User.getUserList()
        if not usr.username in usrs.keys():
            usrs.update(usr.toDict())
            User.__updateUsers(usrs)
            return True
        else:
            print("User already exists...")
            return False

    @staticmethod
    def removeUser(usr):
        usrs = User.getUserList()
        if usr in usrs:
            usrs.remove(usr)
            User.__updateUsers(usrs)
            return True
        else:
            return False

    @staticmethod
    def getUserList(db=None):
        usrs = User.__loadUsers()
        if db:
            dbUsrs = {}
            for usr in usrs.keys():
                if (db in usrs[usr]["database"].keys()) or ("all" in usrs[usr]["database"].keys()):
                    dbUsrs[usr] = usrs[usr]
            return dbUsrs

        return usrs

    @staticmethod
    def __initUserList():
        usrs = {
            "admin" : {
                "password" : "admin",
                "database" : {"all":"admin"}
            }
        }

        User.__updateUsers(usrs)
        return usrs

    @staticmethod
    def __loadUsers():
        usrList = {}
        if (os.path.isfile(User.__usrFile) and
            os.stat(User.__usrFile).st_size != 0): #check if file exists and is not empty
            with open(User.__usrFile) as json_data_file:
                usrList = json.load(json_data_file)
                return usrList

        else:
            return User.__initUserList()

    @staticmethod
    def __updateUsers(usrs):
        with open(User.__usrFile, 'w') as outfile:
            json.dump(usrs, outfile, indent=4, sort_keys=True)# save to file indent=4 & sort_keys=True make the file pretty

    def __init__(self, username, password, db=None):
        self.username = username
        self.password = password
        self.access = ""
        self.db = db

    def login(self):
        usrs = User.getUserList()
        if self.username in usrs.keys():
            if usrs[self.username]["password"] == self.password:
                if "all" in usrs[self.username]["database"].keys():
                    self.access = usrs[self.username]["database"]["all"]
                elif self.db in usrs[self.username]["database"].keys():
                    self.access = usrs[self.username]["database"][self.db]
                else:
                    print("You dont have access to this database ...")
                    return False
                print("Login Successful ...")
                return True
        print("Invalid Username or Password")
        return False

    def changeAccess(self, username, db, access):
        if not self.access.lower() == "admin" or access.lower() not in ["admin", "readWrite", "monitor"]:
            return False

        usrs = User.getUserList()
        if username in usrs.keys():
            print("User exists...")
            if db in usrs[username]["database"].keys():
                if not usrs[username]["database"][db] == access:
                    usrs[username]["database"][db] = access
                else:
                    print("User already has access " + self.access)
            else:
                usrs[username]["database"][db] = access

        User.__updateUsers(usrs)
        return True

    def toDict(self):
        userDict = {
            self.username : {
                "password" : self.password,
                "database" : {}
            }
        }
        return userDict

class loginScreen(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.initUI()

    def initUI(self):
        vBox = QVBoxLayout()
        formLay = QFormLayout()

        self.userBox = QLineEdit()
        userLabel = QLabel("Username")

        self.passwordBox = QLineEdit()
        self.passwordBox.setEchoMode(QLineEdit.Password)
        passwordLabel = QLabel("Password")

        self.dbDropdown = QComboBox()
        # self.dbDropdown.addItems(DatabaseHandler.getDatabaseList('localhost',27017))

        submitBtn = PhtmPushButton("Submit")
        submitBtn.clicked.connect(self.login)

        cancelBtn = PhtmPushButton("Cancel")
        cancelBtn.clicked.connect(self.parent.reject)

        formLay.addRow(userLabel, self.userBox)
        formLay.addRow(passwordLabel, self.passwordBox)
        formLay.addWidget(self.dbDropdown)
        formLay.addRow(submitBtn, cancelBtn)

        formWidget = QWidget()
        formWidget.setLayout(formLay)

        vBox.addWidget(formWidget)

        self.setLayout(vBox)

        self.show()

    def login(self):
        self.user = User(self.userBox.text(), self.passwordBox.text(), self.dbDropdown.currentText())
        # if self.user.login():
        self.parent.accept()

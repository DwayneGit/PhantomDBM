import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from Center import center
from MenuBar import initMenuBar
from Preferences import *
from DatabaseHandler import *
import bson
from bson import ObjectId
import pprint
from collections import OrderedDict
from Dialogs import *
from getType import getType

from numpy import ndarray

class DataTable(QHBoxLayout):

    def __init__(self, database):
        super().__init__()
        self.db = database
        self.dataTable = Table(self.db)
        # Add box layout, add table to box layout and add box layout to widget
        self.addWidget(self.dataTable)

class Table(QTreeView):
    def __init__(self, database):
        super().__init__()
        self.db = database

        model = MyTableModel(self.db)
        self.setRootIsDecorated(False)

        #Remove the option to expand (right arrow/ double click) prevent crash
        self.setItemsExpandable(False)

        #disble all predefined options for editing table
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setModel(model)

        self.alternatingRowColors()
        
        self.currSelectedData = None

        self.clicked.connect(self.click)
        #self.doubleClicked.connect(self.doubleClick)

    def getIndexData(self, row = False):
        if len(self.selectedIndexes()) < 1:
            return
        #print(self.selectedIndexes())
        item = self.selectedIndexes()[0]

#        print(item)
#        print(item.model().rowCount(item))
#        print(item.model().columnCount(item))
        if not row:
            return item
            
        dct = OrderedDict()
        for col in range(self.model().columnCount(item)):
            dct[self.model().headers[col]] = (self.model().itemData(self.model().index(item.row(),col))[2])

        return dct, item

    def removeRow(self):
        dct, item = self.getIndexData(True)

        lst=list(dct.items())

        self.setRowHidden(item.row(),item.parent(),True)
        print({"_id":ObjectId(lst[0][1])})
        self.db.removeDoc({"_id":ObjectId(lst[0][1])})

    def editCell(self):
        #dct = self.getIndexData();
        #self.setCurrentIndex(dct)
        self.edit(self.currentIndex())
        #print(dct)


    def click(self, index):
        if len(self.selectedIndexes()) < 1:
            return

        item = self.selectedIndexes()[0]
#        print(item)
#        print(item.model().rowCount(item))
#        print(item.model().columnCount(item))
        dct = OrderedDict()
        for col in range(self.model().columnCount(item)): # get data from table and store in a ordered dictinary
            dct[self.model().headers[col]] = (self.model().itemData(self.model().index(item.row(),col))[2])
        
        lst=list(dct.items()) #put data into a list
        self.currSelectedData = dct.items()

        #print("")
        #print(self.currSelectedData)

    def contextMenuEvent(self, event):
    
        menu = QMenu(self)

        deleteAction = menu.addAction("Delete")
        editAction = menu.addAction("Edit")
        quitAction = menu.addAction("Quit")

        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.close()
        elif action == deleteAction:
            self.removeRow()
        elif action == editAction:
            self.editCell()

    #def doubleClick(self, index):
    #    print("")

        
class MyTableModel(QAbstractItemModel):
    def __init__(self, db, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.db = db
        self.docs = db.mDbDocs
        self.mkTableList()
        

    #retunr number of rows that should be in the table
    def rowCount(self, parent):
        return len(self.list)

    #retunr number of columns that should be in the table
    def columnCount(self, parent):
        return len(self.list[0])
    
    def flags(self, index):
        if not index.row() == 0 or not self.db.model:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.NoItemFlags
    '''
        index changes for each cell in table start at o 0,0,
        if role == QDisplayRole returns the vale that should be in a particular cell

    '''
    def data(self, index, role):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            value = self.getPrettyString(self.list[row][column])
            return value

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.getPrettyString(self.list[row][column])
            return value

    #for cell edited in table
    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()

            #print(value)
            change = self.getUnprettyString(value)
            #print(change )
            #print(dict(zip(self.headers, self.list[row][:])))
            #create dictionary from using the updated row and the headers
            #using dict(zip(l1,l2)) and use to updated in database
            
            #print({self.headers[0]:self.lis for doc in docs.find({"_id":"__Model__"}):
            #print({self.headers[column]:self.list[row][column]})
            print(self.getPrettyString(self.list[row][column]))

            if not(value == self.getPrettyString(self.list[row][column])):
                okay = self.db.updateDoc({self.headers[0]:self.list[row][0]},{self.headers[column]:change})
                if okay == 1:
                    self.list[row][column] = change
                    self.dataChanged.emit(index, index)

            return True
        return False

    #may need to edit
    def parent(self, child):
        return QModelIndex()

    def index(self,  row,  column, parent = QModelIndex()):
        return self.createIndex(row, column )

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:

                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "not implemented"
            else:
                return "item %d" % section

    def mkTableList(self):        
        self.headers = []  
        self.list = []

        if self.docs: #get names of columns in table from keys in database
            for key in self.docs[0]:
                #print(key)
                self.headers.append(key)

            for i in range(len(self.docs)):
                temp = []
                for val in self.docs[i].values():
                    temp.append(val)
                self.list.append(temp)
    
    '''
    getType:
    converts the user inputed data in to the appropriate data
    type to be stored in the database
    
    def getType(self, torf):
        if not isinstance(torf, str):
            return torf

        elif torf.lower() == "true":
            return True

        elif torf.lower() == "false":
            return False

        try:
            return int(torf)
        except:
            pass

        try:
            return float(torf)
        except:
            pass 

        return torf
    '''

    def getUnprettyString(self, value):
        if not isinstance(value,str):
            return value

        if value[0] == "[":
            #using regex get find all that match patterns of being in single quotes
            #or a number with no quotes. returns in tuple 
            dataList = re.findall(r"(\d+(?:,\d+)?)|(?:\'(.*?)\')", value[1:-1])
            
            #detuple results
            dataList = [''.join(t) for t in dataList]

            #print(dataList)
            filtList = []
            for i in range(len(dataList)):
                if dataList[i] not in ['\'','','[',']']:
                    #get data type from results
                    filtList.append(getType(dataList[i]))

            return filtList 

        else:
            t = re.findall(r"'.*'|[\\\w\d\s]+",value)
            print(t)
            tpe = getType(t[0])
            if isinstance(tpe, str):
                return tpe
            return tpe

    def getPrettyString(self, value):
        if value == None:
            return "None"
           
        if isinstance( value, bson.objectid.ObjectId):
            return str(value)
            
        if isinstance(value ,list):
            temp = ""
            for i in range(len(value)):
                if not i == 0:
                    if isinstance( getType( str(value[i]) ), str):
                        if not value[i] == "None":
                            temp += (", " + "\'" +str(value[i]) + "\'")
                        else: temp += value[i]
                    else: temp += (", "  +str(value[i]) )
                else:
                    if isinstance( getType( str(value[i]) ), str):
                        if not value[i] == "None":
                            temp += ("[" + "\'" +str(value[i])+ "\'")
                        else: temp += "[" + value[i]
                    else: temp += ("[" + str(value[i]))
            return temp + "]" 

        elif isinstance(value, str):
            value = '\'' + value + '\''
        
        return value

            


'''
class MyTableModel(QAbstractTableModel):
    def __init__(self, list, headers = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.list = list
        self.headers = headers

    #retunr number of rows that should be in the table
    def rowCount(self, parent):
        return len(self.list)

    #retunr number of columns that should be in the table
    def columnCount(self, parent):
        return len(self.list[0])
    
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    
    #    index changes for each cell in table start at o 0,0,
    #    if role == QDisplayRole returns the vale that should be in a particular cell

    def data(self, index, role):
        if role == Qt.EditRole:
            row = index.row()self.ids, 
            column = index.column()
            return self.list[row][column]

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.list[row][column]
            return value

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.list[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "not implemented"
            else:
                return "item %d" % section
'''
        
class MainLayout(QWidget):

    def __init__(self, database ):
        super().__init__()
        self.hbox = QHBoxLayout()
        self.split = QSplitter(Qt.Horizontal)
        self.db = database

        self.srchData = None
        self.srchSet = False

        self.table = self.createTableFrame(DataTable(self.db))
        self.form = self.createFormFrame()

        self.split.addWidget(self.table)
        self.split.addWidget(self.form)

        #self.split.setCollapsible(1,False) # set just the middle non collapsible
        self.split.setChildrenCollapsible(False) #set all collapsible
        self.split.setStretchFactor(0,1)
        self.split.setStretchFactor(1,0)
        self.split.setStretchFactor(2,0)

        self.showAddEntry = False
        self.fromWeb = False

        self.hbox.addWidget(self.split)
        self.setUpTabToolBar()
        self.setLayout(self.hbox)

    def setUpTabToolBar(self):
        self.collectionBar = QToolBar(self)
        self.collectionBar.setOrientation(Qt.Vertical)

        addForm = QAction(QIcon("plus.png"),"Add entry",self)
        addForm.triggered.connect(self.toggleAddEntry)
        self.collectionBar.addAction(addForm)

        colForm = QAction(QIcon("column.png"),"Add field to docs in database",self)
        
        self.collectionBar.addAction(colForm)

        srch = QAction(QIcon("search.png"),"Internet LookUp",self) #opens searchs menu even if saved search
        srch.triggered.connect(self.searchCollection)
        self.collectionBar.addAction(srch)

        lookUp = QAction(QIcon("internetset.png"),"Internet LookUp",self) #auto loads saved searches opens menu if no saved search
        lookUp.triggered.connect(self.openScrapper)
        self.collectionBar.addAction(lookUp)

        lookUpToo = QAction(QIcon("star.png"),"Internet LookUp",self) #opens searchs menu even if saved search
        lookUpToo.triggered.connect(self.justOpenScrapper)
        self.collectionBar.addAction(lookUpToo)

        searchCol = QAction(QIcon("internet.png"),"Search Collection",self)
        searchCol.triggered.connect(self.scrapSearch)
        self.collectionBar.addAction(searchCol)

        reloadTable = QAction(QIcon("reload.png"),"Search Collection",self)
        reloadTable.triggered.connect(self.updateTable)
        self.collectionBar.addAction(reloadTable)

        self.hbox.addWidget(self.collectionBar)

    def searchCollection(self):
        srchForDialog = QDialog()
        vBox = QVBoxLayout()
        fLay = QFormLayout() 
            

        labels = []
        boxes = []
        for i in range(len(self.keys)): # create labels and buttons for each column in table
            labels.append( QLabel(srchForDialog) )
            labels[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)       
            labels[i].setText(self.keys[i])
        
            boxes.append(QLineEdit(srchForDialog))
            boxes[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)      
            boxes[i].resize(200, 32)

            fLay.addRow(labels[i],boxes[i])

        fWidget = QWidget()
        fWidget.setLayout(fLay)

        b1 = QPushButton("Search", srchForDialog)
        b1.clicked.connect(srchForDialog.accept)  

        b2 = QPushButton("Cancel", srchForDialog)
        b2.clicked.connect(srchForDialog.reject) 

        vBox.addWidget(fWidget)
        vBox.addWidget(b1)
        vBox.addWidget(b2)

        srchForDialog.setLayout(vBox)
        srchForDialog.show()

        if srchForDialog.exec_():
            srchDict = {}
            for i in range(len(self.keys)):
                if (labels[i].text() == '_id') and (boxes[i].text() == ""):
                    continue
                if not boxes[i].text() == "":
                    if len(self.splitString(boxes[i].text())) > 1:
                        srchDict[abels[i].text()] = self.splitString(getType(boxes[i].text()))
                    else:
                        srchDict[labels[i].text()] = getType(boxes[i].text())
                
            okay = self.db.findDoc(srchDict)
            if okay:
                self.updateTable(True)
            else:
                self.db.reload
    

    def toggleAddEntry(self, tog = False):
        if not self.showAddEntry or tog: 
            self.fFrame.show()
            self.showAddEntry = True
        else: 
            self.fFrame.hide()
            self.showAddEntry = False

    def justOpenScrapper(self):
        self.openScrapper(True)

   
    def createButtonFrame(self):
        bLayout = QFormLayout()
        
        b1 = QPushButton("@", self)
        b1.setFixedSize(30,30)
        
        bLayout.addWidget(b1)
        
        bFrame = QFrame(self)
        bFrame.setFrameShape(QFrame.StyledPanel)
        bFrame.setLayout(bLayout) 
        
        return bFrame
        
    def createTableFrame(self, dataTable ):
        
        tLayout = dataTable
        
        tFrame = QFrame(self)
        tFrame.setFrameShape(QFrame.StyledPanel)
        tFrame.setLayout(tLayout)
        
        return tFrame
        
        
    def createFormFrame(self):
        vLayout = QVBoxLayout()
        fLayout = QFormLayout()
              
        self.keys = []
        if self.db.mDbDocs: #get names of columns in table from keys in database
            for key in self.db.mDbDocs[0]:
                #print(key)
                self.keys.append(key)

        self.labels = []
        self.boxes = []
        for i in range(len(self.keys)): # create labels and buttons for each column in table
            self.labels.append( QLabel(self) )
            self.labels[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)       
            self.labels[i].setText(self.keys[i])
        
            self.boxes.append(QLineEdit(self))
            self.boxes[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)      
            self.boxes[i].resize(200, 32)

            fLayout.addRow(self.labels[i],self.boxes[i])

        self.b1 = QPushButton("New Entry", self)
        self.b1.setFixedSize(100,30)
        self.b1.clicked.connect(self.newEntry)  

        self.b2 = QPushButton("Clear", self)
        self.b2.setFixedSize(100,30)
        self.b2.clicked.connect(self.clearEntry)  

        fWidget = QWidget()
        fWidget.setLayout(fLayout)
        
        vLayout.addWidget(fWidget)
        
        btnFLayout = QFormLayout()

        btnFLayout.addRow(self.b1,self.b2)

        btnFWidget = QWidget()
        btnFWidget.setLayout(btnFLayout)
        
        vLayout.addWidget(btnFWidget)
        
        self.fFrame = QFrame(self)
        self.fFrame.setFrameShape(QFrame.StyledPanel)
        self.fFrame.setLayout(vLayout)
        self.fFrame.hide()
        
        return self.fFrame

    '''
    newEntry:
    gets data from text fields and adds them to an ordered dictionary
    and calls update table to insert them into the table
    '''
    def newEntry(self):
        newEntryDict = OrderedDict()
        for i in range(len(self.keys)):
            if (self.labels[i].text() == '_id') and (self.boxes[i].text() == ""):
                continue
            entries = self.splitString(self.boxes[i].text())
            if len(entries) > 1:
                newEntryDict[self.labels[i].text()] = []
                for en in entries:
                    newEntryDict[self.labels[i].text()].append(getType(en))
                    
            else:
                newEntryDict[self.labels[i].text()] = getType(self.boxes[i].text())
        
        okay = self.db.insertDoc(newEntryDict) 
        print(okay)

        if okay:
            self.clearEntry()

            if self.fromWeb:
                self.toggleAddEntry()
                self.fromWeb = False

            self.updateTable()
            #print(newEntryDict)

    def clearEntry(self):
        for i in range(len(self.boxes)):
            self.boxes[i].setText("")

        if self.fromWeb:
            self.toggleAddEntry()
            self.fromWeb = False


    def splitString(self, splstr):
        return re.split(r",\s|,|;\s|;", splstr)
        
    
    '''
    getType:
    converts the user inputed data in to the appropriate data
    type to be stored in the database
    
    def getType(self, torf):
        print(torf)
        if not isinstance(torf, str):
            return torf

        try:
            return int(torf)
        except:
            pass

        try:
            return float(torf)
        except:
            pass

        if torf.lower() == "true":
            return True

        elif torf.lower() == "false":
            return False

        elif torf == "":
            return None

        else: 
            return torf
    '''


    '''
    updateTable:
    updates reloads the table to show the newly inserted data
    '''
    def updateTable(self, find = False):
        if not find:
            self.db.reload()

        self.table = self.createTableFrame(DataTable(self.db))
        
        old = self.split.widget(0)
        old.deleteLater()

        self.split.insertWidget(0,self.table)
 
        #self.split.setCollapsible(1,False) # set just the middle non collapsible
        self.split.setChildrenCollapsible(False) #set all collapsible
        self.split.setStretchFactor(0,1)
        self.split.setStretchFactor(1,0)

        self.show()
            
        

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.showMessage("Hello")
        
        
                
class Manager(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 840
        self.height = 480

        self.prefs = Preferences('config', DefaultGeneralConfig.prefDict) # name of preference file minus json
        self.prefs.loadConfig()

        self.dbData = self.prefs.prefDict['mongodb']
        #load data from database
        #self.db = DatabaseHandler(self.dbData['collections'], self.dbData['dbname'], self.dbData['host'], self.dbData['port'], tableSize, pageNum) # move to loop and give individual collections
        #print(self.db.mDbDocs)

        # login = loginScreen()
        # if login.exec_():
        #     self.user = login.user
        #     self.initUI()
        #     self.move(center(self))
        # else:
        #     self.reject()
        
    def initUI(self):    
        '''
        initiates application UI
		'''   
        self.setWindowTitle('DBManager')  
        self.setGeometry(self.left,self.top,self.width, self.height) # set screen size (left, top, width, height
         
        self.setStatusBar(StatusBar())
        '''
        self.db = DatabaseHandler(self.dbData, pageNum)
        for i in range(len(self.db.mDbCollections)):
            x =[]
            if not(self.db.mDbDocs[i]):
                x=[]
            else:
                for key in self.db.mDbDocs[i][0]:
                    #print(key)
                    x.append(key)
            self.tabWidget.addTab(MainLayout(x), self.db.mDbCollections[i])
        '''

        self.setUpToolBar()

        self.setTabs()

        initMenuBar(self, 1)
 
        self.show()
        
    def setUpToolBar(self):

        tb = QToolBar(self)
        self.addToolBar(tb)
        
        tbopen = QAction(QIcon("internet.png"),"open",self)
        tb.addAction(tbopen)
        
        tbsettings = QAction(QIcon("settings.png"),"open",self)
        tbsettings.triggered.connect(self.showPref)
        tb.addAction(tbsettings)

        addCol = QAction(QIcon("collect.png"),"Add Collection",self)
        addCol.triggered.connect(self.addCollect) #fall function without parentheses to open dialog window
        tb.addAction(addCol)

        dropCol = QAction(QIcon("rcollect.png"),"Drop Collection",self)
        dropCol.triggered.connect(self.dropCollect) #fall function without parentheses to open dialog window
        tb.addAction(dropCol)

    def setTabs(self):
        '''
        Create TABS for each collection
        '''
        self.collectionNames = DatabaseHandler.getCollectionList(self.dbData)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.setObjectName('tabWidget')

        pageNum = 0
        
        print(self.collectionNames)

        for i in range(len(self.collectionNames)):
            #print(type(self.db.mDbDocs[i]))
            self.db = DatabaseHandler(self.dbData, self.collectionNames[i], pageNum)
            if not(self.db.mDbDocs): #if collection is empty skip it
                continue
            self.tabWidget.addTab(MainLayout(self.db), self.db.mDbCollection)

        self.setCentralWidget(self.tabWidget)

    def dropCollect(self):

        collection, drop = QInputDialog.getItem(self, "Drop Collection", 
            "Collections:", self.collectionNames, 0, False)
			
        if drop and collection:
            buttonReply = QMessageBox.question(self, 'PyQt5 message',
                "Are you sure you want to delete " + collection + "?"+ " \nAll unsaved data will be lost", 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.db.dropCollection(collection)
                self.setTabs()
            else:
                self.dropCollect()

    def addCollect(self, checked = 1):
        if checked==None: return
        dialog = addCollectionDialog(self.dbData)
        if dialog.exec_():
            # print("Hello Tabs")
            self.setTabs()

    def showPref(self):
        p = PreferencesDialog(self.prefs, self.user)
        p.exec_()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle("plastique")
    manager = Manager()    
    sys.exit(app.exec_())

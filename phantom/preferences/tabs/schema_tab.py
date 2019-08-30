import json
import os
import regex

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QMessageBox, QVBoxLayout, QSizePolicy, QMenu, QAction

from phantom.phtmWidgets import PhtmComboBox, PhtmPushButton, PhtmPlainTextEdit, PhtmMessageBox, PhtmInputDialog

from phantom.preferences.defaultSettings import defaultSchemaTemplate

from phantom.utility import textStyle, validateJsonScript

from phantom.applicationSettings import settings

class SchemaTab(QWidget):
    def __init__(self, schema):
        super().__init__()

        self.__schema = schema
        # self.__ref_schemas = ref_schemas
        self.__schemaEditor = PhtmPlainTextEdit()
        self.__schemaEditor.showLineNumbers()
        # self.__schemaEditor.setPlainText("// Schemas use the keywords found in mongoengine.\n// For Details go to https://www.blahblahblah.com.")

        schemaVBox = QVBoxLayout()

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)

        self.__schemaEditor.setSizePolicy(spBottm)
        schemaVBox.addWidget(self.__schemaEditor)
        schemaVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(schemaVBox)


        self.__collection = settings.__DATABASE__.getCollectionName()
        self.children = []

        self.__currItem = "main"
        self.__currItemChanged = False

        if not self.__collection:
            self.__schemaEditor.setReadOnly(True)
            return

        self.db = settings.__DATABASE__.getDatabaseName()
        if schema.getScript() == "{}":
            self.schema = defaultSchemaTemplate(self.__collection)
        else:
            self.schema = schema.getScript()
        self.__schemaEditor.appendPlainText(self.schema)

        # if self.__schema.getScript():
        #     self.__schemaEditor.appendPlainText(self.__schema.getScript())
            # self.schemaBox.setPlainText(self.schema)

        # self.schemaBox = PhtmComboBox()
        # self.schemaBox.setFixedSize(QSize(175, 31))
        # self.schemaBox.addItem(self.__currItem)

        # self.schemaBox.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.schemaBox.customContextMenuRequested.connect(lambda p: self.on_schemaBox_customContextMenuRequested(p))

        # self.__load_reference_schemas()

        self.__schemaEditor.textChanged.connect(self.__schemaChanged)
        # self.schemaBox.currentIndexChanged.connect(lambda i: self.__editSchema(self.__currItem, self.schemaBox.itemText(i)))

        # schemaVBox.addWidget(self.btn_row_1())
        # schemaVBox.addWidget(self.btn_row_2())


    # def on_schemaBox_customContextMenuRequested(self, pos):
    #     menu = QMenu(self)

    #     index = self.schemaBox.view().indexAt(pos)

    #     renameAction = QAction("Rename", self)
    #     renameAction.triggered.connect(lambda x: self.__renameScript(1))

    #     deleteAction = QAction("Delete", self)
    #     deleteAction.triggered.connect(lambda x: self.__deleteScript(1))

    #     menu.addAction(renameAction)
    #     menu.addAction(deleteAction)

    #     menu.popup(self.schemaBox.view().mapToGlobal(pos))

    # def __renameScript(self, x):
    #     pass

    # def __deleteScript(self, x):
    #     pass

    # def btn_row_1(self):
    #     loadWidget = QWidget()
    #     spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    #     spTop.setVerticalStretch(1)
    #     loadWidget.setSizePolicy(spTop)
    #     loadWidgetLayout = QHBoxLayout()

    #     import_ref_schema_btn = PhtmPushButton("Import Reference Schema")
    #     import_primary_schema_btn = PhtmPushButton("Import Primary Schema")

    #     loadWidgetLayout.addWidget(import_primary_schema_btn)
    #     loadWidgetLayout.addWidget(import_ref_schema_btn)
    #     loadWidgetLayout.setContentsMargins(0, 0, 0, 0)

    #     loadWidget.setLayout(loadWidgetLayout)

    #     import_ref_schema_btn.clicked.connect(lambda: self.__import_ref_schema(self.schemaBox))
    #     import_primary_schema_btn.clicked.connect(self.__import_primary_schema)

    #     return loadWidget

    # def btn_row_2(self):
    #     loadWidget = QWidget()
    #     spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    #     spTop.setVerticalStretch(1)
    #     loadWidget.setSizePolicy(spTop)
    #     loadWidgetLayout = QHBoxLayout()

    #     new_ref_btn = PhtmPushButton("Add Child Schema")

    #     loadWidgetLayout.addWidget(self.schemaBox)
    #     loadWidgetLayout.addWidget(new_ref_btn)
    #     loadWidgetLayout.setContentsMargins(0, 0, 0, 0)

    #     loadWidget.setLayout(loadWidgetLayout)

    #     new_ref_btn.clicked.connect(self.__new_ref_script)

    #     return loadWidget

    def __schemaChanged(self):
        self.__currItemChanged = True

    def saveSchemas(self):
        return self.__saveSchema(self.__currItem)

    def __saveSchema(self, schema):
        self.__schema.setScript(self.__schemaEditor.toPlainText())
        if self.__currItemChanged:
            self.__currItemChanged = False
            self.generateMongooseSchema(self.__schemaEditor.toPlainText())

        return True

    def __editSchema(self, curr, schema):
        if curr == schema:
            return

        if self.__currItemChanged:
            errorMessage = PhtmMessageBox(self, 'Save Changes', "Do you want to save changes made to this schema?",
                                     [QMessageBox.Yes, QMessageBox.No])
            if errorMessage.exec_():
                if errorMessage.messageSelection == QMessageBox.Yes:
                    if not self.__saveSchema(curr):
                        self.schemaBox.setCurrentIndex(self.schemaBox.setCurrentIndex(self.__indexOfChild(schema)))
                        return

        if schema == "main":
            self.__schemaEditor.setPlainText(self.__schema.getScript())

        self.__currItem = schema
        self.__currItemChanged = False

    def generateMongooseSchema(self, schemas, schema_addr="./phantom/database/js/src/schemas/"):
        # print(os.getcwd())
        col_key = "__" + self.__collection

        collectionDirectory = schema_addr + self.db + "_" + self.__collection + "/"
        if not os.path.exists(collectionDirectory):
            os.makedirs(collectionDirectory)

        fp = open(collectionDirectory + self.__collection +".js", "w+")
        fp.write('const mongoose = require("mongoose")\n\n')
        fp.write("var " + self.__collection + "Schema = new mongoose.Schema(")

        schm = self.__getObject(schemas, col_key, "__schema")[0]
        if schm:
            fp.write(schm + ", " + self.__getObject(schemas, col_key, "__options")[0] + ")\n\n")
        else:
            fp.write(self.__getObject(schemas, col_key) + ")\n\n" )
        fp.write("module.exports = mongoose.model(\""+ self.__collection + 'Model' +"\", " + self.__collection + "Schema" +")")
        fp.close()

        if schemas.find("__children"):
            self.children = (self.__getKeys(collectionDirectory, self.__getObject(schemas, "__children")[0]))
            print(self.children)
                
    def __getKeys(self, collectionDirectory, jsonData, start=0, keyList=[]):
        key = regex.search("[^\[\]{}\s:\",]+", jsonData[start:])

        if not key: 
            return keyList

        data, index = self.__getObject(jsonData, key.group(0))
        keyList.append(key.group(0))

        fp2 = open(collectionDirectory + key.group(0) + ".js", "w+")
        fp2.write('const mongoose = require("mongoose")\n')
        fp2.write('const ' + self.__collection + 'Model = require("./'+ self.__collection +'")\n')

        fp2.write("\nmodule.exports = " + self.__collection + "Model.discriminator('" + key.group(0) + "',")
        fp2.write("\n\tnew mongoose.Schema(")
        chld = self.__getObject(data, '__schema')[0]
        if chld:
            fp2.write(chld + ", " + self.__getObject(data, '__options')[0] + "))\n")
        else:
            fp2.write(self.__getObject(data)[0] + "))\n")

        fp2.close()
        if start < len(jsonData):
            return self.__getKeys(collectionDirectory, jsonData, index, keyList)

    def __getObject(self, jsonData, *keydata):
        index = 0
        for val in keydata:
            index = jsonData.find(val, index)
            if index == -1:
                return "", 0
        index = jsonData.find("{", index)
        return self.__bracketParse(jsonData, index)
        
    def __bracketParse(self, strg, start):
        out = ""
        bracket = 0
        i = 0
        for i in range(start, len(strg)):
            if strg[i] == "{":
                bracket += 1
            elif strg[i] == "}":
                bracket -= 1
            elif bracket <= 0:
                break
            out += strg[i]

        return out, i
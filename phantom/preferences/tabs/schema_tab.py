import json
import os
import regex

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QMessageBox, QVBoxLayout, QSizePolicy, QMenu, QAction

from phantom.phtm_widgets import PhtmComboBox, PhtmPushButton, PhtmPlainTextEdit, PhtmMessageBox, PhtmInputDialog

from phantom.preferences.default_settings import default_schema_template

from phantom.utility import text_style, validate_json_script

from phantom.application_settings import settings
from phantom.database.createSchema import generate_mongoose_schema

class schema_tab(QWidget):
    def __init__(self, schema, db, collection):
        super().__init__()

        self.__schema = schema
        # self.__ref_schemas = ref_schemas
        self.__schema_editor = PhtmPlainTextEdit()
        # self.__schema_editor.setPlainText("// Schemas use the keywords found in mongoengine.\n// For Details go to https://www.blahblahblah.com.")

        schemaVBox = QVBoxLayout()

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)

        self.__schema_editor.setSizePolicy(spBottm)
        schemaVBox.addWidget(self.__schema_editor)
        schemaVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(schemaVBox)

        self.__collection = collection

        self.__curr_item = "main"
        self.__curr_item_changed = False

        if not self.__collection:
            self.__schema_editor.setReadOnly(True)
            return

        self.db = db
        if schema.get_script() == "{}":
            self.schema = default_schema_template(self.__collection)
        else:
            self.schema = schema.get_script()
        self.__schema_editor.appendPlainText(self.schema)

        # if self.__schema.get_script():
        #     self.__schema_editor.appendPlainText(self.__schema.get_script())
            # self.schema_box.setPlainText(self.schema)

        # self.schema_box = PhtmComboBox()
        # self.schema_box.setFixedSize(QSize(175, 31))
        # self.schema_box.addItem(self.__curr_item)

        # self.schema_box.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.schema_box.customContextMenuRequested.connect(lambda p: self.on_schemaBox_customContextMenuRequested(p))

        # self.__load_reference_schemas()

        # self.__schema_editor.textChanged.connect(self.__schema_changed)
        # self.schema_box.currentIndexChanged.connect(lambda i: self.__edit_schema(self.__curr_item, self.schema_box.itemText(i)))

        # schemaVBox.addWidget(self.btn_row_1())
        # schemaVBox.addWidget(self.btn_row_2())


    # def on_schemaBox_customContextMenuRequested(self, pos):
    #     menu = QMenu(self)

    #     index = self.schema_box.view().indexAt(pos)

    #     renameAction = QAction("Rename", self)
    #     renameAction.triggered.connect(lambda x: self.__rename_script(1))

    #     deleteAction = QAction("Delete", self)
    #     deleteAction.triggered.connect(lambda x: self.__delete_script(1))

    #     menu.addAction(renameAction)
    #     menu.addAction(deleteAction)

    #     menu.popup(self.schema_box.view().mapToGlobal(pos))

    # def __rename_script(self, x):
    #     pass

    # def __delete_script(self, x):
    #     pass

    # def btn_row_1(self):
    #     load_widget = QWidget()
    #     spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    #     spTop.setVerticalStretch(1)
    #     load_widget.setSizePolicy(spTop)
    #     load_widget_layout = QHBoxLayout()

    #     import_ref_schema_btn = PhtmPushButton("Import Reference Schema")
    #     import_primary_schema_btn = PhtmPushButton("Import Primary Schema")

    #     load_widget_layout.addWidget(import_primary_schema_btn)
    #     load_widget_layout.addWidget(import_ref_schema_btn)
    #     load_widget_layout.setContentsMargins(0, 0, 0, 0)

    #     load_widget.setLayout(load_widget_layout)

    #     import_ref_schema_btn.clicked.connect(lambda: self.__import_ref_schema(self.schema_box))
    #     import_primary_schema_btn.clicked.connect(self.__import_primary_schema)

    #     return load_widget

    # def btn_row_2(self):
    #     load_widget = QWidget()
    #     spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    #     spTop.setVerticalStretch(1)
    #     load_widget.setSizePolicy(spTop)
    #     load_widget_layout = QHBoxLayout()

    #     new_ref_btn = PhtmPushButton("Add Child Schema")

    #     load_widget_layout.addWidget(self.schema_box)
    #     load_widget_layout.addWidget(new_ref_btn)
    #     load_widget_layout.setContentsMargins(0, 0, 0, 0)

    #     load_widget.setLayout(load_widget_layout)

    #     new_ref_btn.clicked.connect(self.__new_ref_script)

    #     return load_widget

    # def __schema_changed(self):
    #     self.__curr_item_changed = True

    # def __new_ref_script(self):
    #     if not self.__save_schema(self.__curr_item):
    #         return False
    #     input_name = PhtmInputDialog(self, "Enter Schema Name", "Name: ", QLineEdit.Normal, "")
    #     if input_name.exec_():
    #         if input_name.selected_value:
    #             self.__ref_schemas[input_name.selected_value] = ""
    #             self.__schema_editor.clear()
    #             self.__curr_item = input_name.selected_value

    #             self.schema_box.addItem(input_name.selected_value)
    #             self.schema_box.setCurrentIndex(self.schema_box.count()-1)
    #         else:
    #             err_msg = PhtmMessageBox(None, "Enter Name", "Please enter the name of the collection the schema represents.")
    #             err_msg.exec_()

    def save_schemas(self):
        return self.__save_schema(self.__curr_item)

    # def __load_reference_schemas(self):
    #     for schema in self.__ref_schemas:
    #         self.schema_box.addItem(schema)

    def __save_schema(self, schema):
        # try:
        #     validate_json_script(self, self.__schema_editor.toPlainText())
        # except (ValueError, json.decoder.JSONDecodeError) as err:
        #     settings.__LOG__.logError("SCHEMA_ERR:" + str(err))
        #     err_msg = PhtmMessageBox(self, "Invalid JSON Error",
        #                              "Invalid JSON Format\n" + str(err))
        #     err_msg.exec_()
        #     return False

        self.__schema.set_script(self.__schema_editor.toPlainText())
        if self.__curr_item_changed:
            self.__curr_item_changed = False
            self.generate_mongoose_schema(self.__schema_editor.toPlainText())
        # else:
        #     self.__ref_schemas[schema] = self.__schema_editor.toPlainText()
        #     generate_mongoose_schema(self.__schema_editor.toPlainText(), schema)

        return True

    def __edit_schema(self, curr, schema):
        if curr == schema:
            return

        if self.__curr_item_changed:
            err_msg = PhtmMessageBox(self, 'Save Changes', "Do you want to save changes made to this schema?",
                                     [QMessageBox.Yes, QMessageBox.No])
            if err_msg.exec_():
                if err_msg.msg_selection == QMessageBox.Yes:
                    if not self.__save_schema(curr):
                        self.schema_box.setCurrentIndex(self.schema_box.setCurrentIndex(self.__index_of_child(schema)))
                        return

        if schema == "main":
            self.__schema_editor.setPlainText(self.__schema.get_script())
        # else:
        #     self.__schema_editor.setPlainText(self.__ref_schemas[schema])

        self.__curr_item = schema
        self.__curr_item_changed = False

    def generate_mongoose_schema(self, schemas, schema_addr="./phantom/database/js/src/schemas/"):
        # print(os.getcwd())
        col_key = "__" + self.__collection

        collection_dir = schema_addr + self.db + "_" + self.__collection + "/"
        if not os.path.exists(collection_dir):
            os.makedirs(collection_dir)

        fp = open(collection_dir + self.__collection +"Schema.js", "w+")
        fp.write('const mongoose = require("mongoose")\n')
        fp.write("var " + self.__collection + "Schema = new mongoose.Schema(")
        fp.write(self.__get_object(schemas, col_key, "__schema")[0] + ", " + self.__get_object(schemas, col_key, "__options")[0] + ")\n\n")
        fp.write("module.exports = mongoose.model(\""+ self.__collection + 'Model' +"\"," + self.__collection + "Schema" +")")
        fp.close()

        if schemas.find("__children"):
            fp2 = open(collection_dir + self.__collection + "ChildSchemas.js", "w+")
            fp2.write('const mongoose = require("mongoose")\n')
            fp2.write('const ' + self.__collection + 'Model = require("./'+ self.__collection +'Schema")\n')

            self.__get_keys(fp2, self.__get_object(schemas, "__children")[0])

            fp2.close()
                
    def __get_keys(self, fp, json_data, start=0):
        key = regex.search("[^\[\]{}\s:\",]+", json_data[start:])
        if not key: return
        data, index = self.__get_object(json_data, key.group(0))
        print(data)

        fp.write("module.exports." + key.group(0) + " = new " + self.__collection + "Model.discriminator('" + key.group(0) + "',")
        fp.write("\n\tnew mongoose.Schema(")
        fp.write(self.__get_object(data, '__schema')[0] + ", " + self.__get_object(data, '__options')[0] + "))\n\n")
            
        if start < len(json_data):
            self.__get_keys(fp, json_data, index)

    def __get_object(self, json_data, *keydata):
        index = 0
        for val in keydata:
            index = json_data.find(val, index)
            if index == -1:
                return "", 0
        index = json_data.find("{", index)
        return self.__bracket_parse(json_data, index)
        
    def __bracket_parse(self, strg, start):
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

    # def __import_ref_schema(self, schemaBox):
    #     file_path = f_ctrl.load_script()[1]
    #     if file_path:
    #         input_name = PhtmInputDialog(self, "Enter Schema Name", "Name: ", QLineEdit.Normal, "")
    #         if input_name.exec_():
    #             if input_name.selected_value:
    #                 self.__ref_schemas[input_name.selected_value] = ""
    #                 self.__schema_editor.clear()
    #                 self.__curr_item = input_name.selected_value

    #                 self.schema_box.addItem(input_name.selected_value)
    #                 self.schema_box.setCurrentIndex(self.schema_box.count()-1)
    #             else:
    #                 err_msg = PhtmMessageBox(None, "Enter Name", "Please enter the name of the collection the schema represents.")
    #                 err_msg.exec_()

    # def __import_primary_schema(self):
    #     file_path = f_ctrl.load_script()[1]
    #     if file_path:
    #         schema = text_style.read_text(file_path)
    #         self.__schema_editor.setPlainText(schema)
    #         self.__schema.set_script(schema)
    #         self.__curr_item = "main"
    
    # def __index_of_child(self, child):
    #     for i in range(self.schema_box.count()):
    #         if self.schema_box.childAt(i) == child:
    #             return i
    #     return None
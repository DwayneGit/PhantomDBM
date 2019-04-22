from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

from phtm_widgets.phtm_combo_box import phtm_combo_box
from phtm_widgets.phtm_push_button import phtm_push_button
from phtm_widgets.phtm_plain_text_edit import phtm_plain_text_edit

import file_ctrl as f_ctrl
import text_style

class schema_tab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

        self.__schema = self.mw.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"]
        self.__ref_schemas = self.mw.get_editor_widget().get_cluster().get_phm_scripts()["__reference_schemas__"]
        self.__schema_editor = phtm_plain_text_edit()
        self.__schema_editor.setPlainText("Schemas use the keywords found in mongoengine.\nFor Details go to https://www.blahblahblah.com.")

        self.__curr_item = "Main"
        self.__curr_item_changed = False
        schemaVBox = QVBoxLayout()

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        self.__schema_editor.setSizePolicy(spBottm)

        if self.__schema.get_script():
            self.__schema_editor.setPlainText(self.__schema.get_script())
            # schema_box.setPlainText(self.schema)

        schema_box = phtm_combo_box()
        schema_box.setFixedSize(QSize(175, 31))
        schema_box.addItem(self.__curr_item)

        schema_box.setContextMenuPolicy(Qt.CustomContextMenu)
        schema_box.customContextMenuRequested.connect(lambda p: self.on_treeWidget_customContextMenuRequested(p, schema_box))

        self.__load_reference_schemas(schema_box)

        self.__schema_editor.textChanged.connect(self.__schema_changed)
        schema_box.currentIndexChanged.connect(lambda i : self.__edit_schema(self.__curr_item, schema_box.itemText(i)))

        schemaVBox.addWidget(self.btn_row_1(schema_box))
        schemaVBox.addWidget(self.btn_row_2(schema_box))
        schemaVBox.addWidget(self.__schema_editor)
        schemaVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(schemaVBox)


    def on_treeWidget_customContextMenuRequested(self, pos, schema_box):
        # item = self.__script_tree.itemAt(pos)
        # self.__script_tree.itemClicked.emit(item, 0)
        # print(str(self.__script_tree.indexOfTopLevelItem(item)))
        # if item:
        menu=QMenu(self)

        index = schema_box.view().indexAt(pos)
        item = schema_box.model().data(index, Qt.DisplayRole)

        # print(item)
        
        renameAction = QAction("Rename", self)
        renameAction.triggered.connect(lambda x: self.__rename_script(1))

        deleteAction = QAction("Delete", self)
        deleteAction.triggered.connect(lambda x: self.__delete_script(1))

        menu.addAction(renameAction)
        menu.addAction(deleteAction)
            
        menu.popup(schema_box.view().mapToGlobal(pos))

    def __rename_script(self, x):
        pass

    def __delete_script(self, x):
        pass

    def btn_row_1(self, schema_box):
        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()
        # load_widget_layout.setSpacing(2)

        import_ref_schema_btn = phtm_push_button("Import Reference Schema")
        import_primary_schema_btn = phtm_push_button("Import Primary Schema")

        load_widget_layout.addWidget(import_primary_schema_btn)
        load_widget_layout.addWidget(import_ref_schema_btn)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        # self.curr_schema.setReadOnly(True)
        import_ref_schema_btn.clicked.connect(lambda: self.__import_ref_schema(schema_box))
        import_primary_schema_btn.clicked.connect(self.__import_primary_schema)

        return load_widget

    def btn_row_2(self, schema_box):
        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()
        # load_widget_layout.setSpacing(2)

        new_ref_btn = phtm_push_button("Add Reference Schema")

        load_widget_layout.addWidget(schema_box)
        load_widget_layout.addWidget(new_ref_btn)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        new_ref_btn.clicked.connect(lambda: self.__new_ref_script(schema_box))

        return load_widget

    def __schema_changed(self):
        self.__curr_item_changed = True

    def __new_ref_script(self, schema_box):
        self.__save_schema(self.__curr_item)
        name, ok = QInputDialog.getText(self, "Enter Schema Name", "Name: ", QLineEdit.Normal, "")
        if ok and name:
            self.__ref_schemas[name] = ""
            self.__schema_editor.clear()
            self.__curr_item = name

            schema_box.addItem(name)
            schema_box.setCurrentIndex(schema_box.count()-1)
        else:
            print("Please enter the name of the collection the schema represents.")

    def save_schemas(self):
        self.__save_schema(self.__curr_item)
        
    def __load_reference_schemas(self, schemaBox):
        for schema in self.__ref_schemas:
            schemaBox.addItem(schema)

    def __save_schema(self, schema):
        if schema == "Main":
            self.__schema.set_script(self.__schema_editor.toPlainText())
        else:
            self.__ref_schemas[schema] = self.__schema_editor.toPlainText()

    def __edit_schema(self, curr, schema):
        if curr == schema:
            return
        # print(curr + " " + schema)
        if self.__curr_item_changed:
            reply = QMessageBox.question(self, 'Save Changes', "Do you want to save chnages made to this schema?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.__save_schema(curr)

        if schema == "Main":
            self.__schema_editor.setPlainText(self.__schema.get_script())
        else:
            # print(self.__ref_schemas[schema])
            self.__schema_editor.setPlainText(self.__ref_schemas[schema])

        self.__curr_item = schema
        self.__curr_item_changed = False
        # print(curr)

    def __import_ref_schema(self, schemaBox):
        file_path = f_ctrl.load_script(self.mw)[1]
        if file_path:
            name, ok = QInputDialog.getText(self, "Enter Schema Name", "Name: ", QLineEdit.Normal, "")
            if ok and name:
                schema = text_style.read_text(file_path)
                self.__ref_schemas[name] = schema
                
                schemaBox.addItem(name)
                schemaBox.setCurrentIndex(schemaBox.count()-1)
                self.__curr_item = name
            else:
                print("Please enter the name of the collection the schema represents.")

        # print(self.schema_instr["filepath"])

    def __import_primary_schema(self):
        file_path = f_ctrl.load_script(self.mw)[1]
        if file_path:
            schema = text_style.read_text(file_path)
            self.__schema_editor.setPlainText(schema)
            self.__schema.set_script(schema)
            self.__curr_item = "Main"

        # print(self.schema_instr["filepath"])
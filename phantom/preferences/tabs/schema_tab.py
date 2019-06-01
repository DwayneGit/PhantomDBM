import json

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QMessageBox, QVBoxLayout, QSizePolicy, QMenu, QAction

from phantom.phtm_widgets import PhtmComboBox, PhtmPushButton, PhtmPlainTextEdit, PhtmMessageBox, PhtmInputDialog

from phantom.file_stuff import file_ctrl as f_ctrl
from phantom.utility import text_style, validate_json_script

from phantom.application_settings import settings

class schema_tab(QWidget):
    def __init__(self, schema, ref_schemas):
        super().__init__()

        self.__schema = schema
        self.__ref_schemas = ref_schemas
        self.__schema_editor = PhtmPlainTextEdit()
        self.__schema_editor.setPlainText("Schemas use the keywords found in mongoengine.\nFor Details go to https://www.blahblahblah.com.")

        self.__curr_item = "Main"
        self.__curr_item_changed = False
        schemaVBox = QVBoxLayout()

        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        self.__schema_editor.setSizePolicy(spBottm)

        if self.__schema.get_script():
            self.__schema_editor.setPlainText(self.__schema.get_script())
            # self.schema_box.setPlainText(self.schema)

        self.schema_box = PhtmComboBox()
        self.schema_box.setFixedSize(QSize(175, 31))
        self.schema_box.addItem(self.__curr_item)

        self.schema_box.setContextMenuPolicy(Qt.CustomContextMenu)
        self.schema_box.customContextMenuRequested.connect(lambda p: self.on_schemaBox_customContextMenuRequested(p))

        self.__load_reference_schemas()

        self.__schema_editor.textChanged.connect(self.__schema_changed)
        self.schema_box.currentIndexChanged.connect(lambda i: self.__edit_schema(self.__curr_item, self.schema_box.itemText(i)))

        schemaVBox.addWidget(self.btn_row_1())
        schemaVBox.addWidget(self.btn_row_2())
        schemaVBox.addWidget(self.__schema_editor)
        schemaVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(schemaVBox)


    def on_schemaBox_customContextMenuRequested(self, pos):
        menu = QMenu(self)

        index = self.schema_box.view().indexAt(pos)

        renameAction = QAction("Rename", self)
        renameAction.triggered.connect(lambda x: self.__rename_script(1))

        deleteAction = QAction("Delete", self)
        deleteAction.triggered.connect(lambda x: self.__delete_script(1))

        menu.addAction(renameAction)
        menu.addAction(deleteAction)

        menu.popup(self.schema_box.view().mapToGlobal(pos))

    def __rename_script(self, x):
        pass

    def __delete_script(self, x):
        pass

    def btn_row_1(self):
        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()

        import_ref_schema_btn = PhtmPushButton("Import Reference Schema")
        import_primary_schema_btn = PhtmPushButton("Import Primary Schema")

        load_widget_layout.addWidget(import_primary_schema_btn)
        load_widget_layout.addWidget(import_ref_schema_btn)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        import_ref_schema_btn.clicked.connect(lambda: self.__import_ref_schema(self.schema_box))
        import_primary_schema_btn.clicked.connect(self.__import_primary_schema)

        return load_widget

    def btn_row_2(self):
        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()

        new_ref_btn = PhtmPushButton("Add Reference Schema")

        load_widget_layout.addWidget(self.schema_box)
        load_widget_layout.addWidget(new_ref_btn)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        new_ref_btn.clicked.connect(self.__new_ref_script)

        return load_widget

    def __schema_changed(self):
        self.__curr_item_changed = True

    def __new_ref_script(self):
        if not self.__save_schema(self.__curr_item):
            return False
        input_name = PhtmInputDialog(self, "Enter Schema Name", "Name: ", QLineEdit.Normal, "")
        if input_name.exec_():
            if input_name.selected_value:
                self.__ref_schemas[input_name.selected_value] = ""
                self.__schema_editor.clear()
                self.__curr_item = input_name.selected_value

                self.schema_box.addItem(input_name.selected_value)
                self.schema_box.setCurrentIndex(self.schema_box.count()-1)
            else:
                err_msg = PhtmMessageBox(None, "Enter Name", "Please enter the name of the collection the schema represents.")
                err_msg.exec_()

    def save_schemas(self):
        return self.__save_schema(self.__curr_item)

    def __load_reference_schemas(self):
        for schema in self.__ref_schemas:
            self.schema_box.addItem(schema)

    def __save_schema(self, schema):
        try:
            validate_json_script(self, self.__schema_editor.toPlainText())
        except (ValueError, json.decoder.JSONDecodeError) as err:
            settings.__LOG__.logError("SCHEMA_ERR:" + str(err))
            err_msg = PhtmMessageBox(self, "Invalid JSON Error",
                                     "Invalid JSON Format\n" + str(err))
            err_msg.exec_()
            return False

        if schema == "Main":
            self.__schema.set_script(self.__schema_editor.toPlainText())
        else:
            self.__ref_schemas[schema] = self.__schema_editor.toPlainText()

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

        if schema == "Main":
            self.__schema_editor.setPlainText(self.__schema.get_script())
        else:
            self.__schema_editor.setPlainText(self.__ref_schemas[schema])

        self.__curr_item = schema
        self.__curr_item_changed = False

    def __import_ref_schema(self, schemaBox):
        file_path = f_ctrl.load_script()[1]
        if file_path:
            input_name = PhtmInputDialog(self, "Enter Schema Name", "Name: ", QLineEdit.Normal, "")
            if input_name.exec_():
                if input_name.selected_value:
                    self.__ref_schemas[input_name.selected_value] = ""
                    self.__schema_editor.clear()
                    self.__curr_item = input_name.selected_value

                    self.schema_box.addItem(input_name.selected_value)
                    self.schema_box.setCurrentIndex(self.schema_box.count()-1)
                else:
                    err_msg = PhtmMessageBox(None, "Enter Name", "Please enter the name of the collection the schema represents.")
                    err_msg.exec_()

    def __import_primary_schema(self):
        file_path = f_ctrl.load_script()[1]
        if file_path:
            schema = text_style.read_text(file_path)
            self.__schema_editor.setPlainText(schema)
            self.__schema.set_script(schema)
            self.__curr_item = "Main"
    
    def __index_of_child(self, child):
        for i in range(self.schema_box.count()):
            if self.schema_box.childAt(i) == child:
                return i
        return None
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

        schemaVBox = QVBoxLayout()
        
        spBottm = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spBottm.setVerticalStretch(10)
        self.__schema_editor.setSizePolicy(spBottm)

        if self.__schema.get_script():
            self.__schema_editor.setPlainText(self.__schema.get_script())
            # ref_schemas_box.setPlainText(self.schema)

        ref_schemas_box.currentIndexChanged.connect(lambda i : self.__edit_schema(self.__curr_item, ref_schemas_box.itemText(i)))
            
        schemaVBox.addWidget(self.btn_row1)
        schemaVBox.addWidget(ref_schemas_box)
        schemaVBox.addWidget(self.__schema_editor)
        schemaVBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(schemaVBox)

    def btn_row1(self):
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

        ref_schemas_box = phtm_combo_box()
        ref_schemas_box.setFixedSize(QSize(175,31))
        ref_schemas_box.addItem("Main")
        self.__curr_item = "Main"
        # self.curr_schema.setReadOnly(True)
        self.__load_reference_schemas(ref_schemas_box)
        
        import_ref_schema_btn.clicked.connect(lambda: self.__import_ref_schema(self.__curr_item, ref_schemas_box))
        import_primary_schema_btn.clicked.connect(lambda: self.__import_primary_schema(self.__curr_item))

        return load_widget

    def btn_row1(self):
        load_widget = QWidget()
        spTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spTop.setVerticalStretch(1)
        load_widget.setSizePolicy(spTop)
        load_widget_layout = QHBoxLayout()
        # load_widget_layout.setSpacing(2)

        import_ref_schema_btn = phtm_push_button("Import Reference Schema")
        new_ref_btn = phtm_push_button("Add Reference Schema")
        
        load_widget_layout.addWidget(import_primary_schema_btn)
        load_widget_layout.addWidget(new_ref_btn)
        load_widget_layout.setContentsMargins(0, 0, 0, 0)

        load_widget.setLayout(load_widget_layout)

        ref_schemas_box = phtm_combo_box()
        ref_schemas_box.setFixedSize(QSize(175,31))
        ref_schemas_box.addItem("Main")
        self.__curr_item = "Main"
        # self.curr_schema.setReadOnly(True)
        self.__load_reference_schemas(ref_schemas_box)

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
        self.__save_schema(curr)
        # print(curr)
        if schema == "Main":
            self.__schema_editor.setPlainText(self.__schema.get_script())
        else:
            self.__schema_editor.setPlainText(self.__ref_schemas[schema])
        curr = schema
        # print(curr)

    def __import_ref_schema(self, curr, schemaBox):
        file_path = f_ctrl.load_script(self.parent.parent)[1]
        if file_path:
            name, ok = QInputDialog.getText(self,"Enter Schema Name","Name: ", QLineEdit.Normal, "")
            if ok and name:
                schema = text_style.read_text(file_path)
                self.__ref_schemas[name] = schema
                
                schemaBox.addItem(name)
                schemaBox.setCurrentIndex(schemaBox.count()-1)
                curr = name
            else:
                print("Please enter the name of the collection the schema represents.")

        # print(self.schema_instr["filepath"])

    def __import_primary_schema(self, curr):
        file_path = f_ctrl.load_script(self.parent.parent)[1]
        if file_path:
            schema = text_style.read_text(file_path)
            self.__schema_editor.setPlainText(schema)
            self.__schema.set_script(schema)
            curr = "Main"

        # print(self.schema_instr["filepath"])
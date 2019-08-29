import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QMessageBox

from phantom.utility import validate_json_script

from phantom.phtm_widgets import PhtmPlainTextEdit, PhtmMessageBox

from phantom.application_settings import settings

class PhtmTabWidget(QTabWidget):
    clearTabsRequested = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setMovable(True)
        self.setTabsClosable(True)
        self.hide()

        self.default_tab_count = 1
        self.tab_data = {}
        self.script_set = {}
        self.tabCloseRequested.connect(self.close_tab)

    def tab_by_text(self, text):
        tab_index_found = -1
        for i in range(self.count()):
            if text == self.tabText(i):
                tab_index_found = i
                self.setCurrentIndex(i)
                break
        return tab_index_found

    def save_editor(self, index):
        if not self.widget(index).is_changed:
            return

        save_msg = "The current script is not saved. Do you want to save?"
        msg_box = PhtmMessageBox(self, "Save", save_msg, [QMessageBox.Yes, QMessageBox.Cancel])
        if msg_box.exec_():
            if msg_box.msg_selection == QMessageBox.Cancel:
                return False
            elif msg_box.msg_selection == QMessageBox.Yes:
                if self.widget(index).save_script():
                    self.is_saved(self.tabText(index), index)
                    return False

        return True

    def close_tab(self, index):
        if self.widget(index).is_changed:
            if not self.save_editor(index):
                return

        self.removeTab(index)
        if self.count() < 1:
            self.hide()

    def clear(self):
        for index in range(self.count()):
            self.tabCloseRequested.emit(0)

    def add_editor(self, script=None):
        if script:
            editor = _PhtmEditor(script)
            editor.showLineNumbers()

            index = self.addTab(editor, editor.title)

            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.is_saved(title, self.currentIndex()))

        else:
            editor = _PhtmEditor()
            index = self.addTab(editor, "")
            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.is_saved(title, self.currentIndex()))

        self.setCurrentIndex(index)
        return index

    def is_saved(self, title, index):
        self.widget(index).is_changed = False
        self.setTabText(index, title)

        self.widget(index).get_tree_item().setText(0, title)

    def isChanged(self, index):
        if not self.widget(index).is_changed and self.tabText(index):
            self.widget(index).is_changed = True
            self.setTabText(index, "* " + self.tabText(index))

            self.widget(index).get_tree_item().setText(0, self.tabText(index))

    def get_index(self, editor):
        return self.indexOf(editor)

    def get_tab_text(self, index):
        if self.tabText(index)[0:2] == "* ":
            return self.tabText(index)[2:]
        else: return self.tabText(index)

class _PhtmEditor(PhtmPlainTextEdit):

    saved = pyqtSignal(str)

    def __init__(self, script=None):
        super(_PhtmEditor, self).__init__()

        self.file_path = None
        self.is_changed = False
        self.tree_item = None

        self.__curr_script = script
        self.title = self.__curr_script.get_title()
        self.setPlainText(self.__curr_script.get_script())

    def set_curr_script(self, script):
        self.__curr_script = script
        self.title = self.__curr_script.get_title()
        self.setPlainText(self.__curr_script.get_script())
        self.is_changed = False

    def get_curr_script(self):
        return self.__curr_script

    def save_script(self, user="Daru"):
        try:
            validate_json_script(self, self.toPlainText())
        except Exception as err:
            error_msg = PhtmMessageBox(self, "Validation Error", "Invalid JSON:\n" + str(err))
            error_msg.exec_()
            return False

        self.__curr_script.set_script(self.toPlainText())
        self.__curr_script.set_modified_by(user)
        self.__curr_script.update_date_time_modified()

        self.is_changed = False

        self.saved.emit(self.__curr_script.get_title())
        return True

    def get_tree_item(self):
        return self.tree_item

    def set_tree_item(self, item):
        self.tree_item = item
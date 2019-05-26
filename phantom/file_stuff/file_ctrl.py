__all__ = [
    'load_phm',
    'save_phm',
    'tmpScript',
    'export_phm',
    'load_script',
    'save_script',
    'export_script',
    'tmpScriptCleaner',
    'load_instructions'
]

import json
import os

from time import gmtime, strftime

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from phantom.utility import cleanTmpScripts

from phantom.phtm_widgets import PhtmMessageBox

def load_instructions():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("XML files (*.xml)")
    filenames = []

    if dlg.exec_():
        filenames = dlg.selectedFiles()

        filename_w_ext = os.path.basename(filenames[0])
        filename = os.path.splitext(filename_w_ext)[0]

        return filename, filenames[0]
    return "", None

def load_script():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("JSON files (*.json)")
    filenames = []

    if dlg.exec_():
        filenames = dlg.selectedFiles()

        filename_w_ext = os.path.basename(filenames[0])
        filename = os.path.splitext(filename_w_ext)[0]

        return filename, filenames[0]
    return False, False

def load_phm(main_window):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("Cluster files (*.phm)")
    filenames = []

    if dlg.exec_():
        filenames = dlg.selectedFiles()

        filename_w_ext = os.path.basename(filenames[0])
        filename = os.path.splitext(filename_w_ext)[0]

        main_window.updateWindowTitle(filename)
        main_window.get_editor_widget().clear_tabs()
        main_window.get_editor_widget().load_cluster(filenames[0], filename)

        main_window.load_settings()
        main_window.reload_curr_dmi()
        main_window.reloadDbNames()

        return True
    return False



def save_script(editor, editor_widget):
    f_path = editor_widget.get_cluster().get_file_path()
    if not f_path:
        f_path = export_phm(editor_widget)
        if f_path:
            editor_widget.get_cluster().set_file_path(f_path)
        else: return False

    if not editor.save_script():
        return False
    save_phm(editor_widget, f_path)

    return True

def save_phm(editor_widget, file_path=None):
    if not file_path:
        file_path = editor_widget.get_cluster().get_file_path()
        if not file_path:
            err_msg = PhtmMessageBox(None, "Save PHM", "Cluster file not saved. would you like to save?",
                                        [QMessageBox.Yes, QMessageBox.Cancel])
            if err_msg.exec_():
                if err_msg.msg_selection == QMessageBox.Yes:
                    file_path = export_phm(editor_widget)
                    if not file_path:
                        return False
                else: return False

    editor_widget.save_phm(file_path)
    
    return True



def export_script(curr_script):
    if not curr_script:
        return
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON files (*.json)")
    if file_name:
        if file_name[-5:] != ".json":
            file_name = file_name + ".json"
        with open(file_name, "w") as write_file:
            write_file.write(eval(json.dumps(curr_script.toPlainText(), indent=4)))

def export_phm(editor_widget):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Cluster files (*.phm)")
    if file_path:
        save_phm(editor_widget, file_path)
        return file_path
    return False

def tmpScript(main_window, curr_tab, temp = None):
    file_name = "tmp/script_"+ strftime("%w%d%m%y_%H%M%S", gmtime()) +".json"

    tmpfilePath = file_name

    with open(tmpfilePath, 'w') as outfile:
        outfile.write(eval(json.dumps(curr_tab.toPlainText(), indent=4)))

    return tmpfilePath

def tmpScriptCleaner(main_window):
    main_window.cleanScripts = cleanTmpScripts(0) # for now deletes all previous temp files on startup
    main_window.cleanScripts.start()

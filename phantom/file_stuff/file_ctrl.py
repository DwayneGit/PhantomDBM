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

from PyQt5.QtWidgets import QFileDialog

from phantom.utility import cleanTmpScripts

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
    raise Exception("Error loading cluster file")

def save_script(editor, editor_widget):
    fp = editor_widget.get_cluster().get_file_path()
    if not fp:
        print("Cluster file not saved. would you liket to save?")
        x = export_phm(editor_widget)
        if x: 
            editor_widget.get_cluster().set_file_path(x)
        else: return False

    # main_window.statusBar().showMessage("Saving File ...")

    editor.save_script()
    save_phm(editor_widget, fp)
    editor.is_changed = False 

    return True

def export_script(curr_script):
    if not curr_script:
        return
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON files (*.json)")
    if fileName:
        with open(fileName, "w") as write_file:
            write_file.write(eval(json.dumps(curr_script, indent=4)))

def export_phm(editor_widget):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Cluster files (*.phm)")
    if file_path:
        save_phm(editor_widget, file_path)
        return file_path
    return False

def save_phm(editor_widget, file_path=None):
    if not file_path:
        file_path = editor_widget.get_cluster().get_file_path()
        if not file_path:
            print("Cluster file not saved. would you liket to save?")
            file_path = export_phm(editor_widget)
            if not file_path:
                return

    editor_widget.save_phm(file_path)

def tmpScript(main_window, curr_tab, temp = None):
    fileName = "tmp/script_"+ strftime("%w%d%m%y_%H%M%S", gmtime()) +".json"

    tmpfilePath = fileName

    with open(tmpfilePath, 'w') as outfile:
        outfile.write(eval(json.dumps(curr_tab.toPlainText(), indent=4)))

    return tmpfilePath

def tmpScriptCleaner(main_window):
    main_window.cleanScripts = cleanTmpScripts(main_window.log, 0) # for now deletes all previous temp files on startup
    main_window.cleanScripts.start()

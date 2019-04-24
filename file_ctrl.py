import json
import re
import os

from PyQt5.QtWidgets import QFileDialog

from cleanTmpScript import cleanTmpScripts
from phtm_editor import phtm_editor

from file.json_script import json_script

import text_style as text_style

from time import gmtime, strftime
    
def putfile(main_window, curr_tab):
    fname = QFileDialog.getOpenFileName(main_window, 'Open file', 
        'c:\\',"Image files (*.jpg *.gif *.png)")

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
        # print(main_window.file_path)
        # main_window.editWindowTitle()

        # new_script = main_window.get_editor_widget().add_script(text_style.read_text(filenames[0]), filename, "Dwayne W")[0]

        # new_editor= phtm_editor()
        # new_editor.clear()
        # new_editor=text_style.translate_text(filenames[0],new_editor)
        # new_editor.set_file_path(file_path)

        # main_window.get_editor_widget().get_editor_tabs().add_editor(new_script)
    return filename, filenames[0]

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

        # print(filename_w_ext)

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
    fileName, _ = QFileDialog.getSaveFileName(0, "Save File", "", "JSON files (*.json)")
    if fileName:
        print(fileName)
        with open(fileName, "w") as write_file:
            write_file.write(eval(json.dumps(curr_script, indent=4)))

def export_phm(editor_widget):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getSaveFileName(0, "Save File", "", "Cluster files (*.phm)")
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

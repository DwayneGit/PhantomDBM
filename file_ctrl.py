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
        # print(filenames)
        filename, file_ext = os.path.splitext(filename_w_ext)
        return filename, filenames[0]
    return "", None

def load_script(main_window):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("JSON files (*.json)")
    filenames = []
    
    if dlg.exec_():
        filenames = dlg.selectedFiles()

        filename_w_ext = os.path.basename(filenames[0])
        filename, file_extension = os.path.splitext(filename_w_ext)
        # print(main_window.file_path)
        # main_window.editWindowTitle()

        new_script = main_window.get_editor_widget().add_script(text_style.read_text(filenames[0]), filename, "Dwayne W")

        # new_editor= phtm_editor()
        # new_editor.clear()
        # new_editor=text_style.translate_text(filenames[0],new_editor)
        # new_editor.set_file_path(file_path)

        main_window.get_editor_widget().get_editor_tabs().add_editor(new_script)

def load_phm(main_window):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("Cluster files (*.phm)")
    filenames = []
    
    if dlg.exec_():
        filenames = dlg.selectedFiles()

        filename_w_ext = os.path.basename(filenames[0])
        filename, file_extension = os.path.splitext(filename_w_ext)
        # print(main_window.file_path)
        main_window.updateWindowTitle(filename)
        main_window.get_editor_widget().clear_tabs()
        main_window.get_editor_widget().load_cluster(filename_w_ext)

        main_window.load_settings()
        main_window.reload_curr_dmi()
        main_window.reloadDbNames()

        # print(filename_w_ext)

def save_script(main_window, editor):
    
    file_path = main_window.get_editor_widget().get_cluster().get_file_path()
    tabs = main_window.get_editor_widget().get_editor_tabs()
    curr_tab = tabs.currentWidget()

    if not file_path:
        print("Cluster file not saved. would you liket to save?")
        main_window.get_editor_widget().get_cluster().set_file_path(export_phm(main_window))

    main_window.statusBar().showMessage("Saving File ...")
    # pprint.pprint(re.sub('\'|\n', '', main_window.fileContents.toPlainText()))
    # with open(curr_tab.file_path, 'w') as outfile:
    #     outfile.write(eval(json.dumps(curr_tab.toPlainText(), indent=4)))
    
    editor.save_script()
    save_phm(main_window)
    # if file_path:
    #     main_window.get_editor_widget().get_editor_tabs()(curr_tab.title)
    # else:
    #     main_window.editor_tabs.setTabTitle(main_window.currTitle)

    editor.is_changed = False 

def export_script(main_window):
    file_path = main_window.get_editor_widget().get_cluster().get_file_path()
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(main_window, "Save File", "", "JSON files (*.json)")
    if fileName:
        file_path = fileName
        save_script(main_window, main_window.get_editor_widget().get_editor_tabs().currentWidget())

def export_phm(main_window):
    file_path = main_window.get_editor_widget().get_cluster().get_file_path()
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(main_window, "Save File", "", "Cluster files (*.phm)")
    if fileName:
        file_path = fileName
        main_window.get_editor_widget().get_cluster().save(fileName)
        return fileName

def save_phm(main_window):
    
    file_path = main_window.get_editor_widget().get_cluster().get_file_path()
    phm_handler = main_window.get_editor_widget().get_cluster()

    if not file_path:
        print("Cluster file not saved. would you liket to save?")
        export_phm(main_window)
        return

    main_window.statusBar().showMessage("Saving PHM ...")
    for i in range(main_window.get_editor_widget().get_editor_tabs().count()):
        # print(i)
        if main_window.get_editor_widget().get_editor_tabs().widget(i).is_changed:
        #     print(main_window.get_editor_widget().get_editor_tabs().widget(i).get_curr_script().get_title())
            main_window.get_editor_widget().get_editor_tabs().widget(i).save_script()  
    phm_handler.save()

def tmpScript(main_window, curr_tab, temp = None):
    
    fileName = "tmp/script_"+ strftime("%w%d%m%y_%H%M%S", gmtime()) +".json"
        
    tmpfilePath = fileName

    with open(tmpfilePath, 'w') as outfile:
        outfile.write(eval(json.dumps(curr_tab.toPlainText(), indent=4)))
    
    return tmpfilePath

def tmpScriptCleaner(main_window):

    main_window.cleanScripts = cleanTmpScripts(main_window.log, 0) # for now deletes all previous temp files on startup
    main_window.cleanScripts.start()

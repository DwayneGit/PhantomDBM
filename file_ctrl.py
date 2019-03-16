import json
import re

from PyQt5.QtWidgets import QFileDialog

from cleanTmpScript import cleanTmpScripts
from phtm_editor import phtm_editor

import text_style as text_style

from time import gmtime, strftime
    
def putfile(main_window, curr_tab):
    fname = QFileDialog.getOpenFileName(main_window, 'Open file', 
        'c:\\',"Image files (*.jpg *.gif *.png)")
    
def getfile(main_window, curr_tab):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("JSON files (*.json)")
    filenames = []
    
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        file_path = filenames[0] # save file path
        # print(main_window.file_path)
        # main_window.editWindowTitle()

        new_editor= phtm_editor()
        new_editor.clear()
        new_editor=text_style.translate_text(filenames[0],new_editor)
        new_editor.set_file_path(file_path)

        main_window.editor_tabs.add_editor(new_editor)

def saveScript(main_window, curr_tab):
        
    if not curr_tab.file_path:
        exportScript(main_window, curr_tab)
        return

    main_window.statusBar().showMessage("Saving File ...")
    # pprint.pprint(re.sub('\'|\n', '', main_window.fileContents.toPlainText()))
    with open(curr_tab.file_path, 'w') as outfile:
        outfile.write(eval(json.dumps(curr_tab.toPlainText(), indent=4)))
    
    if curr_tab.file_path:
        main_window.editor_tabs.editTabTitle(curr_tab.title)
    # else:
    #     main_window.editor_tabs.setTabTitle(main_window.currTitle)

    curr_tab.is_changed = False 

def exportScript(main_window, curr_tab):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(main_window, "Save File", "", "JSON files (*.json)")
    if fileName:
        curr_tab.file_path = fileName
        saveScript(main_window, curr_tab)

def tmpScript(main_window, curr_tab, temp = None):
    
    fileName = "tmp/script_"+ strftime("%w%d%m%y_%H%M%S", gmtime()) +".json"
        
    tmpfilePath = fileName

    with open(tmpfilePath, 'w') as outfile:
        outfile.write(eval(json.dumps(curr_tab.toPlainText(), indent=4)))
    
    return tmpfilePath

def tmpScriptCleaner(main_window):

    main_window.cleanScripts = cleanTmpScripts(main_window.log, 0) # for now deletes all previous temp files on startup
    main_window.cleanScripts.start()

import json

from PyQt5.QtWidgets import QFileDialog

from cleanTmpScript import cleanTmpScripts

from time import gmtime, strftime
    
def putfile(main_window):
    fname = QFileDialog.getOpenFileName(main_window, 'Open file', 
        'c:\\',"Image files (*.jpg *.gif *.png)")
    
def getfile(main_window):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("JSON files (*.json)")
    filenames = []
    
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        main_window.filePath = filenames[0] # save file path
        print(main_window.filePath)
        main_window.editWindowTitle()
        f = open(filenames[0], 'r')
        
    with f:
        main_window.fileContents.blockSignals(True)
        data = f.read()
        main_window.fileContents.setText(data)
        main_window.changed = False
        main_window.fileContents.blockSignals(False)

def saveScript(main_window):
    if not main_window.filePath:
        exportScript(main_window)
        return
    main_window.statusBar().showMessage("Saving File ...")
    # pprint.pprint(re.sub('\'|\n', '', main_window.fileContents.toPlainText()))
    with open(main_window.filePath, 'w') as outfile:
        outfile.write(eval(json.dumps(main_window.fileContents.toPlainText(), indent=4)))
    if main_window.filePath:
        main_window.editWindowTitle()
    else:
        main_window.setWindowTitle(main_window.currTitle)

    main_window.changed = False 

def exportScript(main_window):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(main_window,"Save File","","JSON files (*.json)")
    if fileName:
        main_window.filePath = fileName
        saveScript(main_window)

def tmpScript(main_window, temp = None):
    
    fileName = "tmp/script_"+ strftime("%w%d%m%y_%H%M%S", gmtime()) +".json"
        
    tmpfilePath = fileName

    with open(tmpfilePath, 'w') as outfile:
        outfile.write(eval(json.dumps(main_window.fileContents.toPlainText(), indent=4)))
    
    return tmpfilePath

def tmpScriptCleaner(main_window):

    main_window.cleanScripts = cleanTmpScripts(main_window.log, 0) # for now deletes all previous temp files on startup
    main_window.cleanScripts.start()

import json
import os

from time import gmtime, strftime

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from phantom.utility import cleanTmpScripts

from phantom.phtm_widgets import PhtmMessageBox, PhtmFileDialog

def load_instructions():
    dlg = PhtmFileDialog(None, "Open", QFileDialog.AnyFile, "XML files (*.xml)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
    filenames = []

    if dlg.exec_():
        filenames = dlg.selectedFiles

        filename_w_ext = os.path.basename(filenames[0])
        filename = os.path.splitext(filename_w_ext)[0]

        return filename, filenames[0]
    return "", None

def load_script():
    dlg = PhtmFileDialog(None, "Open", QFileDialog.AnyFile, "JSON files (*.json)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
    filenames = []

    if dlg.exec_():
        filenames = dlg.selectedFiles

        filename_w_ext = os.path.basename(filenames[0])
        filename = os.path.splitext(filename_w_ext)[0]
        
        return filename, filenames[0]
    return False, False

def load_phm(main_window, file_path=None):
    
    def load(path):
        filename_w_ext = os.path.basename(path)
        filename = os.path.splitext(filename_w_ext)[0]

        main_window.updateWindowTitle(filename)
        main_window.get_editor_widget().clear_tabs()
        main_window.get_editor_widget().load_cluster(path, filename)

        main_window.adjustForCurrentFile(path)
        main_window.load_settings()
        main_window.reload_curr_dmi()
        main_window.reloadDbNames()

    if not file_path:
        dlg = PhtmFileDialog(main_window, "Open", QFileDialog.AnyFile, "Cluster files (*.phm)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
        filenames = []

        if dlg.exec_():
            try:
                filenames = dlg.selectedFiles
                load(filenames[0])
                return True
            except Exception as err:
                print(str(err))
    else:
        try:
            load(file_path)
            return True
        except Exception as err:
            print(str(err))

    return False

def save_script(editor, editor_widget, adjustForCurrentFile):
    f_path = editor_widget.get_cluster().get_file_path()
    if not f_path:
        f_path = export_phm(editor_widget, adjustForCurrentFile)
        if f_path:
            editor_widget.get_cluster().set_file_path(f_path)
        else: return False

    if not editor.save_script():
        return False
    save_phm(editor_widget, adjustForCurrentFile, f_path)

    return True

def save_phm(editor_widget, adjustForCurrentFile, file_path=None):
    
    if not file_path:
        file_path = editor_widget.get_cluster().get_file_path()
        if not file_path:
            err_msg = PhtmMessageBox(None, "Save PHM", "Cluster file not saved. would you like to save?",
                                        [QMessageBox.Yes, QMessageBox.Cancel])
            if err_msg.exec_():
                if err_msg.msg_selection == QMessageBox.Yes:
                    file_path = export_phm(editor_widget, adjustForCurrentFile)
                    if not file_path:
                        return False
                else: return False
                    
    adjustForCurrentFile(file_path if file_path[-4:] == ".phm" else file_path+".phm")
    editor_widget.save_phm(file_path)
    
    return True

def export_script(curr_script):
    if not curr_script:
        return
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dlg = PhtmFileDialog(None, "Save File", QFileDialog.AnyFile, "JSON files (*.json)", options=options, accept_mode=QFileDialog.AcceptSave)
    if dlg.exec_():
        if dlg.save_name:
            if dlg.save_name[-5:] != ".json":
                dlg.save_name = dlg.save_name + ".json"
            with open(dlg.save_name, "w") as write_file:
                write_file.write(eval(json.dumps(curr_script.toPlainText(), indent=4)))

def export_phm(editor_widget, adjustForCurrentFile):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dlg = PhtmFileDialog(None, "Save Cluster", QFileDialog.AnyFile, "Cluster files (*.phm)", options=options, accept_mode=QFileDialog.AcceptSave)
    if dlg.exec_():
        if dlg.save_name:
            # print(dlg.save_name)
            save_phm(editor_widget, adjustForCurrentFile, dlg.save_name)
            return dlg.save_name
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

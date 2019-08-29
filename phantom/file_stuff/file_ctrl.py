import json
import os

from time import gmtime, strftime

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from phantom.phtm_widgets import PhtmMessageBox, PhtmFileDialog

from phantom.application_settings import settings
class FileHandler():
    def __init__(self, parent):
        self.parent = parent
        self.adjustSignal = None

    def set_adjust_signal(self, signal):
        self.adjustSignal = signal

    def load_instructions(self):
        dlg = PhtmFileDialog(None, "Open", QFileDialog.AnyFile, "XML files (*.xml)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles

            filename_w_ext = os.path.basename(filenames[0])
            filename = os.path.splitext(filename_w_ext)[0]

            return filename, filenames[0]
        return "", None

    def load_script(self):
        dlg = PhtmFileDialog(None, "Open", QFileDialog.AnyFile, "JSON files (*.json)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles

            filename_w_ext = os.path.basename(filenames[0])
            filename = os.path.splitext(filename_w_ext)[0]

            return filename, filenames[0]
        return False, False

    def load_phm(self, file_path=None):

        def load(path):
            if not os.path.exists(path):
                raise Exception("PathError: No such file or directory: '" + path + "'")

            filename_w_ext = os.path.basename(path)
            filename = os.path.splitext(filename_w_ext)[0]

            self.parent.updateWindowTitle(filename)
            self.parent.get_editor_widget().clear_tabs()
            self.parent.get_editor_widget().load_cluster(path, filename)

            self.parent.get_menubar().get_adjust_signal().emit(path)
            self.parent.reload_curr_dmi()
            self.parent.reloadDbNames()

        if not file_path:
            dlg = PhtmFileDialog(self.parent, "Open", QFileDialog.AnyFile, "Cluster files (*.phm)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
            filenames = []

            if dlg.exec_():
                try:
                    filenames = dlg.selectedFiles
                    load(filenames[0])
                    return True
                except Exception as err:
                    settings.__LOG__.logError("LDERR: " + str(err))

        else:
            try:
                load(file_path)
                return True
            except Exception as err:
                settings.__LOG__.logError("LDERR: " + str(err))

        return False

    def save_phm(self, file_path=None):
        try:
            cluster = self.parent.get_editor_widget().get_cluster()
            file_path = cluster.get_file_path()
            if not file_path:
                save_msg = PhtmMessageBox(None, "Save PHM", "Cluster file not saved. would you like to save?",
                                            [QMessageBox.Yes, QMessageBox.Cancel])
                if save_msg.exec_():
                    if save_msg.msg_selection == QMessageBox.Yes:
                        file_path = self.export_phm(self.parent.get_editor_widget())
                        if not file_path:
                            return False
                        
                        if cluster.get_phm().get_name() == "New Cluster":
                            cluster.get_phm().set_name(os.path.basename(file_path)[:-4])

                    else: return False
                        
            self.adjustSignal.emit(file_path if file_path[-4:] == ".phm" else file_path+".phm")
            self.parent.get_editor_widget().save_phm(file_path)
            
            return True

        except Exception as err:
            print("Error Here " + str(err))
            return False

    def export_script(self):
        curr_script = self.parent.get_editor_widget().get_editor_tabs().currentWidget()
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

    def export_phm(self, editor_widget):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dlg = PhtmFileDialog(None, "Save Cluster", QFileDialog.AnyFile, "Cluster files (*.phm)", options=options, accept_mode=QFileDialog.AcceptSave)
        if dlg.exec_():
            if dlg.save_name:
                return dlg.save_name
        return False

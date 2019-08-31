import json
import os

from time import gmtime, strftime

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

from Phantom.PhtmWidgets import PhtmMessageBox, PhtmFileDialog

from Phantom.ApplicationSettings import Settings
class FileHandler(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.adjustSignal = None
        self.reloadDmiSignal = parent.reloadDmiSignal
        self.windowTitleSignal = parent.windowTitleSignal
        self.reloadDatabaseSignal = parent.reloadDatabaseSignal
        
        self.__menuBar = None

    def setEditorWidget(self, editorWidget):
        self.__editorWidget = editorWidget

    def setMenuBar(self, menuBar):
        self.__menuBar = menuBar

    def setAdjustSignal(self, signal):
        self.adjustSignal = signal

    def loadInstructions(self):
        dialog = PhtmFileDialog(None, "Open", QFileDialog.AnyFile, "XML files (*.xml)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
        filenames = []

        if dialog.exec_():
            filenames = dialog.selectedFiles

            filenameWithExtension = os.path.basename(filenames[0])
            filename = os.path.splitext(filenameWithExtension)[0]

            return filename, filenames[0]
        return "", None

    def loadScript(self):
        dialog = PhtmFileDialog(None, "Open", QFileDialog.AnyFile, "JSON files (*.json)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
        filenames = []

        if dialog.exec_():
            filenames = dialog.selectedFiles

            filenameWithExtension = os.path.basename(filenames[0])
            filename = os.path.splitext(filenameWithExtension)[0]

            return filename, filenames[0]
        return False, False

    def loadPhm(self, filePath=None):

        def load(path):
            if not os.path.exists(path):
                raise Exception("PathError: No such file or directory: '" + path + "'")

            filenameWithExtension = os.path.basename(path)
            filename = os.path.splitext(filenameWithExtension)[0]

            self.__editorWidget.clearTabs()
            self.__editorWidget.loadCluster(path, filename)

            self.__menuBar.getAdjustSignal().emit(path)
            self.reloadDmiSignal.emit()
            self.reloadDatabaseSignal.emit()
            self.windowTitleSignal.emit(filename)

        if not filePath:
            dialog = PhtmFileDialog(self, "Open", QFileDialog.AnyFile, "Cluster files (*.phm)", options=QFileDialog.DontUseNativeDialog|QFileDialog.DontUseCustomDirectoryIcons)
            filenames = []

            if dialog.exec_():
                try:
                    filenames = dialog.selectedFiles
                    load(filenames[0])
                    return True
                except Exception as err:
                    Settings.__LOG__.logError("LDERR: " + str(err))

        else:
            try:
                load(filePath)
                return True
            except Exception as err:
                Settings.__LOG__.logError("LDERR: " + str(err))

        return False

    def savePhm(self, filePath=None):
        try:
            cluster = self.__editorWidget.getCluster()
            filePath = cluster.getFilePath()
            if not filePath:
                saveMessage = PhtmMessageBox(None, "Save PHM", "Cluster file not saved. would you like to save?",
                                            [QMessageBox.Yes, QMessageBox.Cancel])
                if saveMessage.exec_():
                    if saveMessage.messageSelection == QMessageBox.Yes:
                        filePath = self.exportPhm(self.__editorWidget)
                        if not filePath:
                            return False
                        
                        if cluster.getPhm().getName() == "New Cluster":
                            cluster.getPhm().setName(os.path.basename(filePath)[:-4])

                    else: return False
                        
            self.adjustSignal.emit(filePath if filePath[-4:] == ".phm" else filePath+".phm")
            self.__editorWidget.savePhm(filePath)
            
            return True

        except Exception as err:
            Settings.__LOG__.logError("SAVE_ERR: " + str(err))
            return False

    def exportScript(self):
        try:
            currScript = self.__editorWidget.getEditorTabs().currentWidget()
        except:
            return

        if not currScript:
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = PhtmFileDialog(None, "Save File", QFileDialog.AnyFile, "JSON files (*.json)", options=options, acceptMode=QFileDialog.AcceptSave)
        if dialog.exec_():
            if dialog.saveName:
                if dialog.saveName[-5:] != ".json":
                    dialog.saveName = dialog.saveName + ".json"
                with open(dialog.saveName, "w") as writeFile:
                    writeFile.write(eval(json.dumps(currScript.toPlainText(), indent=4)))

    def exportPhm(self, editorWidget):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = PhtmFileDialog(None, "Save Cluster", QFileDialog.AnyFile, "Cluster files (*.phm)", options=options, acceptMode=QFileDialog.AcceptSave)
        if dialog.exec_():
            if dialog.saveName:
                return dialog.saveName
        return False

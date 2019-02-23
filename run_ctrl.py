from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from upload_thread import upload_thread

from DBConnection import DatabaseHandler
import file_ctrl as f_ctrl

'''
runScript:
run script to load files into the database
'''
def runScript(main_window, run_counter, completed_run_counter):
    # make sure file is not deleted before saving
    file_path = main_window.filePath

    if main_window.changed:
        save_msg = "Changes made have not been saved.\nWould you like to save before running this script?"
        reply = QMessageBox.question(main_window, 'Message', 
                        save_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            if file_path:
                f_ctrl.saveScript(main_window)
            else:
                f_ctrl.exportScript(main_window)
        elif reply == QMessageBox.Cancel:
            return   
        elif reply == QMessageBox.No:
            file_path = f_ctrl.tmpScript(main_window)

    if file_path is None:
        main_window.appendToBoard("Nothing To Run. Please make changes to the default script or load your own script to run. ")
        return

    main_window.setRunState(True)
    run_counter += 1

    main_window.log.logInfo("Checking Database Connection...")

    db_handler = DatabaseHandler(main_window.dbData, main_window.log)
    if db_handler.serverStatus():

        main_window.log.logInfo("Connected to Database. " + main_window.dbData['dbname'] + " collection " + main_window.dbData['collection'])
        print(main_window.dbData)
        main_window.upld_thrd = upload_thread(file_path, db_handler, main_window.log) # instanciate the Q object
        thread = QThread(main_window) # create a thread

        try:
            main_window.upld_thrd.moveToThread(thread) # send object to its own thread
        except:
            main_window.appendToBoard("error moving to thread")


        main_window.upld_thrd.update.connect(main_window.appendToBoard) # link signals to functions
        main_window.upld_thrd.done.connect(lambda msg: threadDone(main_window, completed_run_counter, msg))

        thread.started.connect(main_window.upld_thrd.addToDatabase) # connect function to be started in thread
        thread.start()

    else:
        main_window.appendToBoard("Failed to Connect to Database")
        main_window.setRunState(False)
        return

def stopRun(main_window):
    if main_window.isRunning:
        main_window.upld_thrd.setStopFlag()
        main_window.setIsRunning(False)

def pauseRun(main_window):
    if main_window.isRunning:
        main_window.setRunBtnIcon(QIcon("icons/play_pause.png"))
        main_window.setIsRunning(False)
    else:
        main_window.setRunBtnIcon(QIcon("icons/pause.png"))
        main_window.setIsRunning(True)

    main_window.upld_thrd.togglePauseFlag()


@pyqtSlot(str)
def threadDone(main_window, completed_run_counter, msg):
    main_window.appendToBoard(msg)
    completed_run_counter += 1
    main_window.setRunState(False)

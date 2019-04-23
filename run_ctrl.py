from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

import json

from upload_thread import upload_thread

from collections import OrderedDict
from itertools import islice

from database.DBConnection import database_handler
import file_ctrl as f_ctrl

'''
run_cript:
run script to load files into the database
'''
def run_script(**kwargs):
    # make sure file is not deleted before saving
    if kwargs["curr_tab"].is_changed:
        save_msg = "Changes made will be saved,\nAre you Sure you want to run this script?"
        reply = QMessageBox.question(self, 'Message', 
                        save_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            f_ctrl.save_script(kwargs["curr_tab"], kwargs["editor_widget"]))
        elif reply == QMessageBox.Cancel:
            return   
        elif reply == QMessageBox.No:
            return

    kwargs["main_toolbar"].setRunState(True)
    run_counter += 1
    kwargs["log"].logInfo("Checking Database Connection...")

    try:
        db_handler = database_handler(kwargs["dbData"], kwargs["log"])
        json.loads(kwargs["phm_scripts"]["__schema__"].get_script())
        db_handler.set_schema(kwargs["phm_scripts"]["__schema__"].get_script(), kwargs["phm_scripts"]["__reference_schemas__"])

    except (Exception, KeyError, AttributeError, json.decoder.JSONDecodeError) as err:
        kwargs["log"].logError(err)
        kwargs["main_toolbar"].setRunState(False)
        return False

    kwargs["log"].logInfo("Connected to Database. " + kwargs["dbData"]['dbname'] + " collection " + kwargs["dbData"]['collection'])
    
    self.upld_thrd = upload_thread(kwargs["curr_tab"].get_curr_script().get_script(), db_handler, kwarg["log"], kwargs["phm_scripts"]["__dmi_instr__"]["instr"]) # instanciate the Q object
    thread = QThread(self) # create a thread

    try:
        self.upld_thrd.moveToThread(thread) # send object to its own thread
    except:
        kwargs["log"].logError("error moving to thread")
        kwargs["main_toolbar"].setRunState(False)
        return False

    self.upld_thrd.start.connect(main_window.set_progress_max)
    self.upld_thrd.update.connect(main_window.update_progress) # link signals to functions
    self.upld_thrd.done.connect(lambda nm: script_done(main_window, nm))
    self.upld_thrd.thrd_done.connect(lambda msg: thread_done(main_window, completed_run_counter, msg))

    thread.started.connect(main_window.upld_thrd.addToDatabase) # connect function to be started in thread
    thread.start()

def run_all_scripts(main_window):
    # make sure file is not deleted before saving
    # curr_tab = main_window.get_editor_widget().get_editor_tabs().currentWidget()
    # file_path = curr_tab.file_path

    # if curr_tab.is_changed:
    #     save_msg = "Are you Sure you want to run this script?"
    #     reply = QMessageBox.question(main_window, 'Message', 
    #                     save_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

    #     if reply == QMessageBox.Yes:
    #         f_ctrl.save_script(main_window)
    #     elif reply == QMessageBox.Cancel:
    #         return   
    #     elif reply == QMessageBox.No:
    #         return

    # if file_path is None:
    #     main_window.appendToBoard("Nothing To Run. Please make changes to the default script or load your own script to run. ")
    #     return

    scripts = main_window.get_editor_widget().get_cluster().get_phm_scripts()

    main_window.get_main_toolbar().setRunState(True)

    main_window.log.logInfo("Checking Database Connection...")

    db_handler = database_handler(main_window.dbData, main_window.log)
    if not db_handler.connected:
        print("Unable to connect to database")
        return False

    try:
        json.loads(main_window.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"])
        db_handler.set_schema(main_window.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"].get_script(), main_window.get_editor_widget().get_cluster().get_phm_scripts()["__reference_schemas__"])
    except KeyError as err:
        print(err)
        main_window.get_main_toolbar().setRunState(False)
        return
    except AttributeError as err:
        print("Invalid schema for main collection")
        main_window.get_main_toolbar().setRunState(False)
        return

    if db_handler.serverStatus():

        main_window.log.logInfo("Connected to Database. " + main_window.dbData['dbname'] + " collection " + main_window.dbData['collection'])
        print("run all")
        # print(main_window.dbData)
        main_window.upld_thrd = upload_thread(scripts, db_handler, main_window.log) # instanciate the Q object
        thread = QThread(main_window) # create a thread

        try:
            main_window.upld_thrd.moveToThread(thread) # send object to its own thread
        except:
            main_window.appendToBoard("error moving to thread")

        main_window.upld_thrd.start.connect(main_window.set_progress_max)
        main_window.upld_thrd.update.connect(main_window.update_progress) # link signals to functions
        main_window.upld_thrd.done.connect(lambda nm: script_done(main_window, nm))
        main_window.upld_thrd.thrd_done.connect(lambda msg: thread_done(main_window, 0, msg))

        thread.started.connect(main_window.upld_thrd.addToDatabase) # connect function to be started in thread
        thread.start()

    else:
        main_window.appendToBoard("Failed to Connect to Database")
        main_window.get_main_toolbar().setRunState(False)
        return

def run_plus_below(main_window, index):
    # make sure file is not deleted before saving
    # curr_tab = main_window.get_editor_widget().get_editor_tabs().currentWidget()
    # file_path = curr_tab.file_path

    # if curr_tab.is_changed:
    #     save_msg = "Are you Sure you want to run this script?"
    #     reply = QMessageBox.question(main_window, 'Message', 
    #                     save_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

    #     if reply == QMessageBox.Yes:
    #         f_ctrl.save_script(main_window)
    #     elif reply == QMessageBox.Cancel:
    #         return   
    #     elif reply == QMessageBox.No:
    #         return

    # if file_path is None:
    #     main_window.appendToBoard("Nothing To Run. Please make changes to the default script or load your own script to run. ")
    #     return

    scripts = main_window.get_editor_widget().get_cluster().get_phm_scripts()

    main_window.get_main_toolbar().setRunState(True)

    main_window.log.logInfo("Checking Database Connection...")

    db_handler = database_handler(main_window.dbData, main_window.log)
    if not db_handler.connected:
        print("Unable to connect to database")
        return False

    try:
        json.loads(main_window.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"])
        db_handler.set_schema(main_window.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"].get_script(), main_window.get_editor_widget().get_cluster().get_phm_scripts()["__reference_schemas__"])
    except KeyError as err:
        print(err)
        main_window.get_main_toolbar().setRunState(False)
        return
    except AttributeError as err:
        print("Invalid schema for main collection")
        main_window.get_main_toolbar().setRunState(False)
        return

    if db_handler.serverStatus():

        main_window.log.logInfo("Connected to Database. " + main_window.dbData['dbname'] + " collection " + main_window.dbData['collection'])
        print(main_window.dbData)
        main_window.upld_thrd = upload_thread(OrderedDict(islice(scripts.items(), index, len(scripts))), db_handler, main_window.log) # instanciate the Q object
        thread = QThread(main_window) # create a thread

        try:
            main_window.upld_thrd.moveToThread(thread) # send object to its own thread
        except:
            main_window.appendToBoard("error moving to thread")

        main_window.upld_thrd.start.connect(main_window.set_progress_max)
        main_window.upld_thrd.update.connect(main_window.update_progress) # link signals to functions
        main_window.upld_thrd.done.connect(lambda nm: script_done(main_window, nm))
        main_window.upld_thrd.thrd_done.connect(lambda msg: thread_done(main_window, 0, msg))

        thread.started.connect(main_window.upld_thrd.addToDatabase) # connect function to be started in thread
        thread.start()

    else:
        main_window.appendToBoard("Failed to Connect to Database")
        main_window.get_main_toolbar().setRunState(False)
        return

def stopRun(main_window):
    if main_window.isRunning:
        main_window.upld_thrd.setStopFlag()
        main_window.get_main_toolbar().setIsRunning(False)

def pauseRun(main_window):
    if main_window.isRunning:
        main_window.get_main_toolbar().setRunBtnIcon(QIcon("icons/play_pause.png"))
        main_window.get_main_toolbar().setIsRunning(False)
    else:
        main_window.get_main_toolbar().setRunBtnIcon(QIcon("icons/pause.png"))
        main_window.get_main_toolbar().setIsRunning(True)

    main_window.upld_thrd.togglePauseFlag()


@pyqtSlot(str)
def thread_done(main_window, completed_run_counter, msg):
    main_window.appendToBoard(msg)
    completed_run_counter += 1
    main_window.get_main_toolbar().setRunState(False)
    script_done(main_window, "Upload")

def script_done(main_window, name):
    main_window.statusBar().showMessage(name + " Complete")
    main_window.progressBar.setValue(0)


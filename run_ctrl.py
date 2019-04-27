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
class run_ctrl():
    def __init__(self, parent=None):
        self.parent = parent
        self.__upld_thrd = None

    def __run_script(self, script_s):
        self.parent.get_main_toolbar().setRunState(True)
        self.parent.runs += 1
        self.parent.log.logInfo("Checking Database Connection...")

        try:
            db_handler = database_handler(self.parent.dbData, self.parent.log)
            # json.loads(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"].get_script())
            db_handler.set_schema(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"].get_script(), self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__reference_schemas__"])

        except (Exception, KeyError, AttributeError, json.decoder.JSONDecodeError) as err:
            self.parent.log.logError(err)
            self.parent.get_main_toolbar().setRunState(False)
            return False

        self.parent.log.logInfo("Connected to Database. " + self.parent.dbData['dbname'] + " collection " + self.parent.dbData['collection'])
        
        self.__upld_thrd = upload_thread(script_s, db_handler, self.parent.log, self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["instr"]) # instanciate the Q object

        thread = QThread(self.parent) # create a thread
        
        try:
            self.__upld_thrd.moveToThread(thread) # send object to its own thread
        except:
            self.parent.log.logError("error moving to thread")
            self.parent.get_main_toolbar().setRunState(False)
            return False

        self.__upld_thrd.start.connect(self.set_progress_max)
        self.__upld_thrd.update.connect(self.update_progress) # link signals to functions
        self.__upld_thrd.done.connect(self.script_done)
        self.__upld_thrd.thrd_done.connect(lambda msg:self.thread_done(thread, msg))

        thread.started.connect(self.__upld_thrd.addToDatabase) # connect function to be started in thread
        thread.start()

    def run(self, opt=0, index=None):
        if opt == 0:
            f_ctrl.save_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget(), self.parent.get_editor_widget())
            script_s = self.parent.get_editor_widget().get_editor_tabs().currentWidget().get_curr_script().get_script()
        elif opt == 1:
            script_s = self.parent.get_editor_widget().get_cluster().get_phm_scripts()
        elif opt == 2:
            s = self.parent.get_editor_widget().get_cluster().get_phm_scripts()
            script_s = OrderedDict(islice(s.items(), index, len(s)))

        self.parent.r_ctrl.__run_script(script_s)

    def stopRun(self, run_state):
        if run_state:
            self.__upld_thrd.setStopFlag()
            return False

    def pauseRun(self, main_toolbar, run_state):
        self.__upld_thrd.togglePauseFlag()
        if run_state:
            main_toolbar.setRunBtnIcon(QIcon("icons/play_pause.png"))
            return False
        main_toolbar.setRunBtnIcon(QIcon("icons/pause.png"))
        return True

    def thread_done(self, thread, msg):
        self.parent.appendToBoard(msg)
        self.parent.completed_run_counter += 1
        self.parent.get_main_toolbar().setRunState(False)
        self.script_done("Upload")
        thread.exit(1)

    def script_done(self, name):
        self.parent.statusBar().showMessage(name + " Complete")
        self.parent.progressBar.setValue(0)

    def set_progress_max(self, mx):
        self.parent.progressBar.setMaximum(mx)

    def update_progress(self, status):
        self.parent.progressBar.setValue(self.parent.progressBar.value()+1)
        self.parent.statusBar().showMessage(status)
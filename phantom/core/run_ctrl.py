import json

from collections import OrderedDict
from itertools import islice

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread

from phantom.database import DatabaseHandler, upload_thread, mongoose_thread

from phantom.file_stuff import file_ctrl as f_ctrl

from phantom.application_settings import settings

'''
run_cript:
run script to load files into the database
'''
class run_ctrl():
    def __init__(self, parent=None):
        self.parent = parent
        self.__upld_thrd = None
        self.__mongoose_thrd = None

    def __run_script(self, script_s):
        self.parent.get_main_toolbar().setRunState(True)
        self.parent.runs += 1
        settings.__LOG__.logInfo("Checking Database Connection...")

        try:
            db_handler = DatabaseHandler(self.parent.dbData)
            # json.loads(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"].get_script())
            # db_handler.set_schema(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__reference_schemas__"])

        except (Exception, KeyError, AttributeError, json.decoder.JSONDecodeError) as err:
            settings.__LOG__.logError("RUN_ERR:" + str(err))
            self.parent.get_main_toolbar().setRunState(False)
            return False

        settings.__LOG__.logInfo("Connected to Database. " + self.parent.dbData['dbname'] + " collection " + self.parent.dbData['collection'])
        self.parent.appendToBoard("Connected to Database. " + self.parent.dbData['dbname'] + " collection " + self.parent.dbData['collection'])

        self.__mongoose_thrd = mongoose_thread(db_handler) # instanciate the Q object
        self.__upld_thrd = upload_thread(script_s, db_handler, self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["instr"]) # instanciate the Q object

        thread1 = QThread(self.parent) # create a thread
        thread2 = QThread(self.parent)

        try:
            self.__mongoose_thrd.moveToThread(thread2)
            self.__upld_thrd.moveToThread(thread1) # send object to its own thread
        except Exception as err:
            settings.__LOG__.logError("RUN_ERR: error moving to thread")
            self.parent.get_main_toolbar().setRunState(False)
            return False

        self.__upld_thrd.start.connect(self.set_progress_max)
        self.__upld_thrd.update_s.connect(self.update_status) # link signals to functions
        self.__upld_thrd.update_b.connect(self.update_board) # link signals to functions
        self.__upld_thrd.done.connect(self.script_done)
        self.__upld_thrd.thrd_done.connect(lambda msg:self.thread_done(thread1, msg))
        
        thread1.started.connect(self.__upld_thrd.addToDatabase) # connect function to be started in thread
        thread2.started.connect(self.__mongoose_thrd.run)

        thread2.start()
        thread1.start()

    def run(self, opt=0, index=None):
        if opt == 0:
            f_ctrl.save_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget(), self.parent.get_editor_widget())
            script_s = self.parent.get_editor_widget().get_editor_tabs().currentWidget().get_curr_script().get_script()

        elif opt == 1:
            script_s = self.parent.get_editor_widget().get_cluster().get_phm_scripts()

        elif opt == 2:
            clust = self.parent.get_editor_widget().get_cluster().get_phm_scripts()
            script_s = OrderedDict(islice(clust.items(), index, len(clust)))

        self.__run_script(script_s)

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

    def update_status(self, status):
        self.parent.progressBar.setValue(self.parent.progressBar.value()+1)
        self.parent.statusBar().showMessage(status)

    def update_board(self, status):
        self.parent.appendToBoard(status)

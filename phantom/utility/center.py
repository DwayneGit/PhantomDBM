from PyQt5.QtWidgets import QApplication

def center_window(Obj):
    '''
    place window at the center of the screen
    '''
    frameGm = Obj.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    centerPoint = QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    return frameGm.topLeft()

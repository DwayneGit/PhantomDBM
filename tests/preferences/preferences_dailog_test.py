from pytestqt import qtbot

from PyQt5.QtCore import QRect

from phantom.phtmWidgets.phtm_dialog import PhtmDialog
from phantom.preferences import PreferenceBody as body

def test_PreferenceBody():

    p = PhtmDialog("Preferences", QRect(10, 10, 450, 500), self)
    p.setCentralDialog(body(None, p))
    p.getCentralDialog().tabW.setCurrentIndex(0)

    p.show()
from pytestqt import qtbot

from PyQt5.QtCore import QRect

from phantom.phtm_widgets.phtm_dialog import PhtmDialog
from phantom.preferences import preference_body as body

def test_preference_body():

    p = PhtmDialog("Preferences", QRect(10, 10, 450, 500), self)
    p.set_central_dialog(body(None, p))
    p.get_central_dialog().tabW.setCurrentIndex(0)

    p.show()
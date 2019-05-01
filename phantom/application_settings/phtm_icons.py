import os

class PhtmIcons():
    def __init__(self, ui_icons):
        self.ui_icons = ui_icons
        self.get_icons()
        self.get_window_icons()

    def get_icons(self):
        self.app_icon = ("icons/" + self.ui_icons + "/phantom.png")
        self.play = ("icons/" + self.ui_icons +"/play.png")
        self.pause = ("icons/" + self.ui_icons +"/pause.png")
        self.save = ("icons/" + self.ui_icons +"/save.png")
        self.stop = ("icons/" + self.ui_icons +"/stop.png")
        self.edit = ("icons/" + self.ui_icons +"/edit.png")
        self.sync = ("icons/" + self.ui_icons +"/sync.png")
        self.info = ("icons/" + self.ui_icons +"/info.png")
        self.close = ("icons/" + self.ui_icons +"/close.png")
        self.add = ("icons/" + self.ui_icons +"/add.png")
        self.settings = ("icons/" + self.ui_icons +"/settings.png")
        self.load_file = ("icons/" + self.ui_icons +"/load-file.png")
        self.import_file = ("icons/" + self.ui_icons +"/import_file.png")
        self.export = ("icons/" + self.ui_icons +"/export.png")

    def get_window_icons(self):
        self.maximize = ("icons/window_icons/icons8-maximize-window-48.png")
        self.minimze = ("icons/window_icons/icons8-minimize-window-48.png")
        self.restore = ("icons/window_icons/icons8-restore-window-100.png")
        self.close = ("icons/window_icons/icons8-close-window-96.png")

import os

class PhtmIcons():
    def __init__(self, ui_icons, path="icons/"):
        self.ui_icons = ui_icons
        self.app_icon = (path +'phantom.png')
        self.get_icons(path)
        self.get_window_icons(path)

    def get_icons(self, path):
        self.play = (path+self.ui_icons +"/play.png")
        self.save = (path+self.ui_icons +"/save.png")
        self.stop = (path+self.ui_icons +"/stop.png")
        self.edit = (path+self.ui_icons +"/edit.png")
        self.wifi = (path+self.ui_icons +"/wifi.png")
        self.reload = (path+self.ui_icons +"/reload-512.png")
        self.settings = (path+self.ui_icons +"/settings.png")
        self.load_file = (path+self.ui_icons +"/load-file.png")
        self.import_file = (path+self.ui_icons +"/import-file.png")
        self.export_file = (path+self.ui_icons +"/export-file.png")

    def get_window_icons(self, path):
        self.maximize = (path+"window_icons/icons8-maximize-window-48.png")
        self.minimze = (path+"window_icons/icons8-minimize-window-48.png")
        self.restore = (path+"window_icons/icons8-restore-window-100.png")
        self.close = (path+"window_icons/icons8-close-window-96.png")

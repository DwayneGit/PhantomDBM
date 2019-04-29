import os

class PhtmIcons():
    def __init__(self, path="icons/"):

        self.app_icon = (path +'phantom.png')
        self.get_icons(path)
        self.get_window_icons(path)

    def get_icons(self, path):
        self.play = (path+"std_white/play.png")
        self.save = (path+"std_white/save.png")
        self.stop = (path+"std_white/stop.png")
        self.edit = (path+"std_white/edit.png")
        self.wifi = (path+"std_white/wifi.png")
        self.reload = (path+"std_white/reload-512.png")
        self.settings = (path+"std_white/settings.png")
        self.load_file = (path+"std_white/load-file.png")
        self.import_file = (path+"std_white/import-file.png")
        self.export_file = (path+"std_white/export-file.png")

    def get_window_icons(self, path):
        self.maximize = (path+"window_icons/icons8-maximize-window-48.png")
        self.minimze = (path+"window_icons/icons8-minimize-window-48.png")
        self.restore = (path+"window_icons/icons8-restore-window-100.png")
        self.close = (path+"window_icons/icons8-close-window-96.png")

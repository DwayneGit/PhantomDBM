class PhtmIcons():
    def __init__(self, path="icons/standard_white/"):
        self.get_icons(path)

    def get_icons(self, path):
        self.play = path+"play.png"
        self.save = path+"save.png"
        self.stop = path+"stop.png"
        self.edit = path+"edit.png"
        self.wifi = path+"wifi.png"
        self.reload = "icons/reload-512.png"
        self.settings = path+"settings.png"
        self.load_file = path+"load-file.png"
        self.import_file = path+"import-file.png"
        self.export_file = path+"export-file.png"

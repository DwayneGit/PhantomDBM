class PhtmIcons():
    def __init__(self, iconSet=None):
        self.iconSet = None
        self.setIconSet(iconSet)
        if self.iconSet:
            self.setIcons()

    def setIconSet(self, iconSet):
        self.iconSet = "icons/" + iconSet
        self.setIcons()

    def setIcons(self):
        self.appIcon = self.iconSet + "/phantom.png"
        self.play = self.iconSet + "/play.png"
        self.pause = self.iconSet + "/pause.png"
        self.save = self.iconSet + "/save.png"
        self.stop = self.iconSet + "/stop.png"
        self.edit = self.iconSet + "/edit.png"
        self.sync = self.iconSet + "/sync.png"
        self.info = self.iconSet + "/info.png"
        self.warning = self.iconSet + "/warning.png"
        self.close = self.iconSet + "/close.png"
        self.add = self.iconSet + "/add.png"
        self.settings = self.iconSet + "/settings.png"
        self.loadFile = self.iconSet + "/load-file.png"
        self.importFile = self.iconSet + "/import_file.png"
        self.export = self.iconSet + "/export.png"
        self.closeTab = self.iconSet + "/close.png"

        self.whiteDot = "icons/white.png"
        self.maximize = "icons/window_icons/icons8-maximize-window-48.png"
        self.minimze = "icons/window_icons/icons8-minimize-window-48.png"
        self.restore = "icons/window_icons/icons8-restore-window-100.png"
        self.close = "icons/window_icons/icons8-close-window-96.png"

    def getPlay(self):
        return self.play

    def getPause(self):
        return self.pause

    def getSave(self):
        return self.save

    def getAppIcon(self):
        return self.appIcon

    def getStop(self):
        return self.stop

    def getEdit(self):
        return self.edit

    def getSync(self):
        return self.sync

    def getWarning(self):
        return self.warning

    def getInfo(self):
        return self.info

    def getClose(self):
        return self.close

    def getCloseTab(self):
        return self.closeTab

    def getAdd(self):
        return self.add

    def getSettings(self):
        return self.settings

    def getLoadFile(self):
        return self.loadFile

    def getImportFile(self):
        return self.importFile

    def getExport(self):
        return self.export

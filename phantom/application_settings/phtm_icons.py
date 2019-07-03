class PhtmIcons():
    def __init__(self, icon_set=None):
        self.icon_set = icon_set
        if self.icon_set:
            self.set_icons()

    def set_icons_set(self, icon_set):
        self.icon_set = icon_set
        self.set_icons()

    def set_icons(self):
        self.app_icon = "icons/" + self.icon_set + "/phantom.png"
        self.play = "icons/" + self.icon_set +"/play.png"
        self.pause = "icons/" + self.icon_set +"/pause.png"
        self.save = "icons/" + self.icon_set +"/save.png"
        self.stop = "icons/" + self.icon_set +"/stop.png"
        self.edit = "icons/" + self.icon_set +"/edit.png"
        self.sync = "icons/" + self.icon_set +"/sync.png"
        self.info = "icons/" + self.icon_set +"/info.png"
        self.warning = "icons/" + self.icon_set +"/warning.png"
        self.close = "icons/" + self.icon_set +"/close.png"
        self.add = "icons/" + self.icon_set +"/add.png"
        self.settings = "icons/" + self.icon_set +"/settings.png"
        self.load_file = "icons/" + self.icon_set +"/load-file.png"
        self.import_file = "icons/" + self.icon_set +"/import_file.png"
        self.export = "icons/" + self.icon_set +"/export.png"
        self.close_tab = "icons/" + self.icon_set + "/close.png"

        self.white_dot = "icons/white.png"
        self.maximize = "icons/window_icons/icons8-maximize-window-48.png"
        self.minimze = "icons/window_icons/icons8-minimize-window-48.png"
        self.restore = "icons/window_icons/icons8-restore-window-100.png"
        self.close = "icons/window_icons/icons8-close-window-96.png"

    def get_play(self):
        return self.play

    def get_pause(self):
        return self.pause

    def get_save(self):
        return self.save

    def get_app_icon(self):
        return self.app_icon

    def get_stop(self):
        return self.stop

    def get_edit(self):
        return self.edit

    def get_sync(self):
        return self.sync

    def get_warning(self):
        return self.warning

    def get_info(self):
        return self.info

    def get_close(self):
        return self.close

    def get_close_tab(self):
        return self.close_tab

    def get_add(self):
        return self.add

    def get_settings(self):
        return self.settings

    def get_load_file(self):
        return self.load_file

    def get_import_file(self):
        return self.import_file

    def get_export(self):
        return self.export

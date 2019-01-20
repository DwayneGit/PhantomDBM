def save_design_inputs(self):

        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Design", os.path.join(str(self.folder), "untitled.osi"),
                                                  "Input Files(*.osi)")

        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return

        # yaml.dump(self.uiObj,out_file,allow_unicode=True, default_flow_style=False)
        json.dump(self.uiObj, out_file)

        out_file.close()

        pass 
import json

from PyQt5.QtWidgets import QMessageBox

def validate_json_script(parent, json_str):
    try:
        return json.loads(json_str)
    except json.decoder.JSONDecodeError as err:
        QMessageBox.warning(parent, "Invalid Json Error",
                            "Invalid Json Format\n" + str(err))
        raise

import fileinput
import regex
from PyQt5.QtWidgets import QPlainTextEdit

def translate_text(xfile, text_edit=None):
    if not text_edit:
        text_edit = QPlainTextEdit()
    else:
        text_edit.clear()
        
    with fileinput.input(files=(xfile)) as f:
        for line in f:
            line = regex.sub("(?<=:\s*)(\"\w+\")", add_style_to_text, line)
            line = regex.sub("\"\w+\"(?=\s*:)", add_style_to_text_col, line)
            line = regex.sub("(?<!\<span)\s", "&nbsp;", line)
            text_edit.appendHtml(line) #regex.sub("\n", "", line)

            # print(line)
        # print(text)
    return text_edit
    
def add_style_to_text_col(matchobj):
    # print(matchobj.group(0) + "2")
    cpy = "<span style=\"color:#8a08e0;\">"
    cpy += matchobj.group(0)
    cpy += "</span>"
    return cpy
    
def add_style_to_text(matchobj):
    # print(matchobj.group(0) + "1")
    cpy = "<span style=\"color:#128712;\">"
    cpy += matchobj.group(0)
    cpy += "</span>"
    return cpy

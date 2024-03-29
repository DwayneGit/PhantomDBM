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
            text_edit.appendHtml(line)

    return text_edit

def readText(xfile):
    if not xfile:
        raise Exception("File does not exist")
        
    with fileinput.input(files=(xfile)) as f:
        script = ""
        for line in f:
            script += line

    return script

def read_string(xString):
    script = ""
    for line in xString.splitlines():
        script += line

    return script

def add_style_to_text_col(matchobj):
    cpy = "<span style=\"color:#8a08e0;\">"
    cpy += matchobj.group(0)
    cpy += "</span>"
    return cpy

def add_style_to_text(matchobj):
    cpy = "<span style=\"color:#128712;\">"
    cpy += matchobj.group(0)
    cpy += "</span>"
    return cpy

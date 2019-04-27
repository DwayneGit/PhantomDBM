import sys
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
from utility.center import center_window

class FileDialogDemo(QDialog):
   def __init__(self):
      super().__init__()
		
      layout = QVBoxLayout()
      self.btn = QPushButton("QFileDialog static method demo")
      self.btn.clicked.connect(self.getfile)
		
      layout.addWidget(self.btn)
      self.le = QLabel("Hello")
		
      layout.addWidget(self.le)
      self.btn1 = QPushButton("QFileDialog object")
      self.btn1.clicked.connect(self.getfiles)
      layout.addWidget(self.btn1)
		
      self.contents = QTextEdit()
      layout.addWidget(self.contents)
      self.setLayout(layout)
      self.set_window_title("File Dialog demo")

      self.setGeometry(10,10,400, 550) 
      self.move(center_window(self))
		
   def getfile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif *.png)")
      self.le.setPixmap(QPixmap(fname))
		
   def getfiles(self):
      dlg = QFileDialog()
      dlg.setFileMode(QFileDialog.AnyFile)
      dlg.setNameFilter("JSON files (*.js *.json)")
      filenames = []
		
      if dlg.exec_():
         filenames = dlg.selectedFiles()
         f = open(filenames[0], 'r')
			
         with f:
            data = f.read()
            self.contents.setText(data)
            
def readJSON(file):
    
    json=open(file)

    data = json.load(json)  


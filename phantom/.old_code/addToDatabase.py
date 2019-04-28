import os
import sys
import subprocess
import json
import time
    
def addToDatabase(b, filePath):

    b.appendPlainText("Checking Database Connection...")
    dbHandler = DatabaseHandler(self.dbData)

    

    os.close(r)
    w = os.fdopen(w,'w')
    w.write("Running JSON Script...")
    # sys.stdout.flush()

    with open(filePath) as infile:
        data = json.load(infile)
        for i in range(len(data)):
            dbHandler.insertDoc(data[i])
            w.write("Sending Objects to Database... %d/%d" %(i+1,len(data)))
            print(1)
            time.sleep(1)
            

argList = str(sys.argv)
addToDatabase()
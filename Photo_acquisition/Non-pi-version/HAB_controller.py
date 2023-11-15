from datetime import datetime
import time
import csv

DATE = datetime.utcnow()
#checks to see if the current setting of the camera are within time
try:
    settings_file = open('Camera_settings.csv','r')
    settings = csv.reader(settings_file,delimiter = ',')

    for line in settings:
        file_date = datetime.fromisoformat(line[0])
        break
    print("File_date",str(file_date))
    current_settings = True
    settings_file.close()
except:
    current_settings = False

#changes settings if more time has past
if not current_settings:
    input("press enter to start getting camera settings:")

    exec(open("ExposureAndGain.py").read())

    input("press enter to start capturing pictures")

    
#starts taking pitcures
exec(open("ContAcquisition.py").read())

#ContAcquisition.py
from simple_pyspin import Camera
from PIL import Image
import os
import time
import simple_pyspin
import numpy as np
from datetime import date
import PySpin

import serial
import csv

import HAB_classes


#gain and exposure time for the cameras
#These will be overridden by the Camera_settings.csv file, but are here in case it does not exist
#the settings for the camera have not been saved
serial_numbs = ["58","72","73"]
gain = [0,0,0]
exposure_time = [3503,3503,3503] #microseconds

cams = HAB_classes.CAMERAS()





#entering the time between taking images (seconds)
#if the gps pps is availible then only int will be used
imageInterval = "1"

starttime = time.time()



cams.init_cams()
print("init_time:",time.time()-starttime)


# Make a directory to save some images
# It is set up such that a new folder with the date/flight# is created
#first the gps is used to see if it can find the current date
time.sleep(0.1)


#makes a new directory with the flight number (just += 1 from the previous)
cams.DIR_Flights(gps.output_dir)
gps.output_dir = cams.output_dir
output_dir = cams.output_dir
gps.make_csv()
cams.DIR_cams()




#create log file
LOG = open(output_dir+"/Log.csv",'w')
write_log = csv.writer(LOG)
write_log.writerow(['TIME','Frame','LOG'])
LOG.close()


starttime = time.time()
#m shows the frame number
m = 0


cams.start()
start = True
while True:
    #breaks if the button is pressed
    if GPIO.input(31):
        LOG = open(output_dir+"/Log.csv",'a')
        write_log = csv.writer(LOG)
        write_log.writerow([round((time.time() - starttime),3),m,"Button pressed-loop exited"])
        LOG.close()
        break
    
    # disconnects and reconnects  all cameras if a new camera is detected
    TIME = np.round(time.time()-starttime,3)
    if cams.New_connection:
        print("reconnect")
        cams.Reconnect(TIME,m)
    m = m+1
        
    #this controls the timing of the pictures being taken, if the pps is available
    #(which is the case when the gps has a fix) then it used the pps from the gps for
    #timing, otherwise the pi's internal clock is used
    gps.frame_timing(imageInterval,starttime,m)
    TIME = np.round(time.time()-starttime,3)    
    imgs = []
    #time from beginning
    print(TIME)
    #detects new camera
    cams.Detect_cameras(TIME,m)
    #takes pictures
    cams.take_and_save(TIME,m)
        
    #gets data from gps
    gps.save_data(m)
    


#shutdown camera,GPIO pins, and the auto run feature
cams.cleanup()
GPIO.cleanup()
os.system("sudo systemctl stop HAB")
LOG = open(output_dir+"/Log.csv",'a')
write_log = csv.writer(LOG)
write_log.writerow([round((time.time() - starttime),3),m,"DONE"])
LOG.close()
print("DONE!")

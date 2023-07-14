#ContAcquisition.py
import HAB_functions
from simple_pyspin import Camera
from PIL import Image
import os
import time
import simple_pyspin
import numpy as np
from datetime import date
import PySpin
import adafruit_gps
import serial
import csv
import RPi.GPIO as GPIO
import HAB_classes


#gain and exposure time for the cameras
#These will be overridden by the Camera_settings.csv file, but are here in case it does not exist
#the settings for the camera have not been saved
serial_numbs = ["58","72","73"]
gain = [0,0,0]
exposure_time = [3503,3503,3503] #microseconds

cams = HAB_classes.CAMERAS()

gps = HAB_classes.GPS()


#initializes the button and LED
GPIO.setup(31,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(40,GPIO.OUT)
GPIO.output(40,GPIO.HIGH)




#entering the time between taking images (seconds)
#if the gps pps is availible then only int will be used
imageInterval = "1"

starttime = time.time()



cams.init_cams()
print("init_time:",time.time()-starttime)


# Make a directory to save some images
# It is set up such that a new folder with the date/flight# is created
#first the gps is used to see if it can find the current date
time.sleep(5)
print("past gps")
gps.get_dir()

#makes a new directory with the flight number (just += 1 from the previous)
cams.DIR_Flights(output_dir)
gps.output_dir = cams.output_dir
cams.DIR_cams()




#create log file
LOG = open(output_dir+"/Log.csv",'w')
write_log = csv.writer(LOG)
write_log.writerow(['TIME','Frame','LOG'])
LOG.close()


starttime = time.time()
#M shows the frame number, trys and good are here to disconnect the camera if
#it misses 2 frames
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
    if cams.New_connection:
        cams.Reconnect()
    m = m+1
        
    #this controls the timing of the pictures being taken, if the pps is available
    #(which is the case when the gps has a fix) then it used the pps from the gps for
    #timing, otherwise the pi's internal clock is used

    gps.frame_timming(imageInterval)
        
    imgs = []
    TIME = np.round(time.time()-starttime,3)#time from beginning
    print(TIME)
    #detects new camera
    cams.Detect_cameras()
    #takes pictures
    cams.take_and_save(m,TIME)
        
    #gets data from gps
    gps.update()
    GPS_data = HAB_functions.GPS(gps)
    GPS_data = GPS_data+tuple([str(m)])
    file = open(output_dir+"/GPS_DATA.csv",'a')
    write = csv.writer(file)
    write.writerow(GPS_data)
    file.close()
    


#shutdown camera,GPIO pins, and the auto run feature
cams.close()
GPIO.cleanup()
os.system("sudo systemctl stop HAB")
LOG = open(output_dir+"/Log.csv",'a')
write_log = csv.writer(LOG)
write_log.writerow([round((time.time() - starttime),3),m,"DONE"])
LOG.close()
print("DONE!")

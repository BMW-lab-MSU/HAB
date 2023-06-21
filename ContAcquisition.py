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
import logging



#gain and exposure time for the cameras
#These will be overridden by the Camera_settings.csv file, but are here in case it does not exist
#the settings for the camera have not been saved
serial_numbs = ["58","72","73"]
gain = [0,0,0]
exposure_time = [3503,3503,3503] #microseconds

#searches camera settings with the file
settings_file = open('Camera_settings.csv','r')
settings = csv.reader(settings_file,delimiter = ',')
for line in settings:
    for i in range(len(serial_numbs)):
        if line[0][-2:] == serial_numbs[i]:
            gain[i] = float(line[1])
            if float(line[2])>=100:
                exposure_time[i] = float(line[2])
settings_file.close()


#initializes the pps pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

#initializes the button and LED
GPIO.setup(31,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(40,GPIO.OUT)
GPIO.output(40,GPIO.HIGH)

#GPS initialization
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=None)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # Turn off everything:
gps.send_command(b'PMTK220,1000')


#entering the time between taking images (seconds)
#if the gps pps is availible then only int will be used
imageInterval = "1"

starttime = time.time()
#initialize the cameras and set settings
[cams,CamNames] = HAB_functions.find_cameras()

#This stops the cameras to ensure the settigns can be changed
for cam in cams:
    cam.stop()
    cam.close()

[cams,CamNames] = HAB_functions.find_cameras()
#initializes the cameras with the desired settings
for i in range(len(cams)):
    print(CamNames[i][-2:])
    for j in range(len(serial_numbs)):
        if serial_numbs[j] == CamNames[i][-2:]:
            print("init")
            HAB_functions.Initialize_camera(cams[i],gain[j],exposure_time[j])
print("init_time:",time.time()-starttime)


# Make a directory to save some images
# It is set up such that a new folder with the date/flight# is created
#first the gps is used to see if it can find the current date
time.sleep(5)
print("past gps")
gps.update()
if gps.has_fix:
    gps.timestamp_utc
    time.sleep(2)
    gps.update()
    if gps.has_fix:
        Date = gps.timestamp_utc
        Date = Date[:-3]
        DATE = "-".join([str(i).zfill(2) for i in Date])
        DATE = DATE[:-9]
        output_dir = DATE
else:
    output_dir = str(date.today())
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#makes a new directory with the flight number (just += 1 from the previous)
flights = os.listdir(output_dir)
flight_numb = str(len(flights)+1)
output_dir = output_dir+"/Flight_"+flight_numb
os.makedirs(output_dir)
for camera in CamNames:
    if not os.path.exists(output_dir+"/"+camera):
        os.makedirs(output_dir+"/"+camera)

#makes GPS data file
file = open(output_dir+"/GPS_DATA.csv",'w')
write = csv.writer(file)
write.writerow(["Latitude","Longitude","Altitude[m]","UTC","Frame"])
file.close()

#create log file
LOG = open(output_dir+"/Log.txt",'w')
write_log = csv.writer(LOG)


starttime = time.time()
#M shows the frame number, trys and good are here to disconnect the camera if
#it misses 2 frames
m = 0
trys = 0
goods = 0
for cam in cams:
    cam.start()
New_connection = False

while True:
    #breaks if the button is pressed
    if GPIO.input(31):
        write_log.writerow(["Button pressed-loop exited"])
        break
    # disconnects and reconnects  all cameras if a new camera is detected
    if New_connection:
        for cam in cams:
            cam.stop()
            cam.close()
        cams = []
        CamNames = []
        [cams,CamNames] = HAB_functions.find_cameras()
        for i in range(len(cams)):
            print(CamNames[i][-2:])
            for j in range(len(serial_numbs)):
                if serial_numbs[j] == CamNames[i][-2:]:
                    print("init")
                    HAB_functions.Initialize_camera(cams[i],gain[j],exposure_time[j])

        for camera in CamNames:
            if not os.path.exists(output_dir+"/"+camera):
                os.makedirs(output_dir+"/"+camera)
        write_log.writerow(["Reconnected..."])
        for cam in cams:
            cam.start()
        New_connection = False
    m = m+1
        
    #this controls the timing of the pictures being taken, if the pps is available
    #(which is the case when the gps has a fix) then it used the pps from the gps for
    #timing, otherwise the pi's internal clock is used

    gps.update()
    time_since_last_frame = 0
    if gps.has_fix:
        while time_since_last_frame < int(imageInterval):
            gps.update()
            if not gps.has_fix:
                time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))
                break
            HAB_functions.wait_for_edge_gps(7,gps)
            time_since_last_frame += 1
            print("GPS:",m)
    else:
        time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
        print("CLOCK",m)
        
    imgs = []
    TIME = np.round(time.time()-starttime,3)#time from beginning
    
    #detects new camera
    if len(simple_pyspin.list_cameras())>len(cams):
        New_connection = True
        write_log.writerow(["Will try to reconnect..."])
    if goods == 5:
        trys = 0
    i = 0
    while i < (len(cams)):
        try:
            imgs.append(cams[i].get_array()) # Each image is a numpy array!
            goods +=1
        except:
            goods = 0
            if trys >=2:
                write_log.writerow(["camera "+CamNames[i]+" disconnected..."])
                
                cams = np.delete(cams,i,0)
                CamNames.pop(i)
                trys = 0
                i-=1
            else:
                imgs.append(None)
                write_log.writerow(["img skipped"])
                trys +=1
        i+=1
    
    #gets data from gps
    gps.update()
    GPS_data = HAB_functions.GPS(gps)
    GPS_data = GPS_data+tuple([str(m)])
    file = open(output_dir+"/GPS_DATA.csv",'a')
    write = csv.writer(file)
    write.writerow(GPS_data)
    file.close()
    
    #saving the images as numpy arrays
    for i in range(len(cams)):
        
        filename = "F"+str(m).zfill(5)+"-T"+str(TIME)+"-G"+str(cams[i].Gain)+"-E"+str(cams[i].ExposureTime)
        filename = filename.replace(".","_",3)
        
        #makes sure the image exists
        if type(imgs[i]) != type(None):
            np.save(output_dir+"/"+CamNames[i]+"/"+filename,imgs[i])
        else:
            print("not saved")


#shutdown camera,GPIO pins, and the auto run feature
for cam in cams:
    cam.stop()
    cam.close()
GPIO.cleanup()
os.system("sudo systemctl stop HAB")
LOG.close()
print("DONE!")

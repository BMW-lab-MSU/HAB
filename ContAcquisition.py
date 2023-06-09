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

#gain and exposure time for the cameras
serial_numbs = ["58","72","73"]
gain = [0,0,0]
exposure_time = [3503,3503,3503] #microseconds


#initializes the pps pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)


#GPS initialization
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=None)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # Turn off everything:
gps.send_command(b'PMTK220,1000')


#entering the time between taking images (seconds)
imageInterval = "1"

starttime = time.time()
#initialize the cameras and set settings
[cams,CamNames] = HAB_functions.find_cameras()

for cam in cams:
    cam.stop()
    cam.close()

[cams,CamNames] = HAB_functions.find_cameras()
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
time.sleep(5)
gps.update()
if gps.has_fix:
    Date = gps.timestamp_utc
    Date = Date[:-3]
    DATE = "-".join([str(i) for i in Date])
    DATE = DATE[:-9]
    output_dir = DATE
else:
    output_dir = str(date.today())
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
flights = os.listdir(output_dir)
flight_numb = str(len(flights)+1)
output_dir = output_dir+"/Flight_"+flight_numb
os.makedirs(output_dir)
for camera in CamNames:
    if not os.path.exists(output_dir+"/"+camera):
        os.makedirs(output_dir+"/"+camera)

file = open(output_dir+"/GPS_DATA.csv",'w')
file.close()

starttime = time.time()
m = 0
trys = 0
goods = 0
for cam in cams:
    cam.start()
New_connection = False

while True:
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
        print("Reconnected...")
        for cam in cams:
            cam.start()
        New_connection = False
    m = m+1
        
    #print(m,"(tn)")
    time_since_last_frame = 0
    if gps.has_fix:
        while time_since_last_frame < int(imageInterval):
            HAB_functions.wait_for_edge(7)
            time_since_last_frame += 1
            print("GPS:",m)
    else:
        time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
        #print(time.time()-starttime)
    
    imgs = []
    TIME = np.round(time.time()-starttime,3)
    #print("Before images are taken:",np.round(time.time()-starttime,3))
    
    if len(simple_pyspin.list_cameras())>len(cams):
        New_connection = True
        print("Will try to reconnect...")
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
                print("camera "+CamNames[i]+" disconnected...")
                
                cams = np.delete(cams,i,0)
                CamNames.pop(i)
                trys = 0
                i-=1
            else:
                imgs.append(None)
                print("img skipped")
                trys +=1
        i+=1
        #print(imgs[0].shape, imgs[0].dtype)
        #print("Saving images to: %s" % output_dir)
    
    #put gps here
    gps.update()
    GPS_data = HAB_functions.GPS(gps)
    file = open(output_dir+"/GPS_DATA.csv",'a')
    write = csv.writer(file)
    write.writerow(GPS_data)
    file.close()
    #print("After images are taken:",np.round(time.time()-starttime,3))
    for i in range(len(cams)):
        
        filename = "T"+str(TIME)+"-G"+str(cams[i].Gain)+"-E"+str(cams[i].ExposureTime)
        filename = filename.replace(".","_",3)
        
        #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
        if type(imgs[i]) != type(None):
            np.save(output_dir+"/"+CamNames[i]+"/"+filename,imgs[i])
        else:
            print("not saved")

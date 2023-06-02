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


#GPS initialization
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # Turn off everything:
gps.send_command(b'PMTK220,1000')



#Entering the exposure time desired in ms
exposureTime = "10003"



#entering the time between taking images (seconds)
imageInterval = "1"


#initialize the cameras and set settings
starttime = time.time()
[cams,CamNames] = HAB_functions.find_cameras()
for cam in cams:
    cam.stop()
    cam.close()

[cams,CamNames] = HAB_functions.find_cameras()
for cam in cams:
    HAB_functions.Initialize_camera(cam)
print("init_time:",time.time()-starttime)


# Make a directory to save some images
# It is set up such that a new folder with the date/flight# is created
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
            try:
                cam.stop()
                cam.close()
            except:
                pass
        cams = []
        CamNames = []
        [cams,CamNames] = HAB_functions.find_cameras()
        for cam in cams:
            HAB_functions.Initialize_camera(cam)
        for camera in CamNames:
            if not os.path.exists(output_dir+"/"+camera):
                os.makedirs(output_dir+"/"+camera)
        print("Reconnected...")
    m = m+1
    if New_connection:
        print("boot")
        New_connection = False
        for cam in cams:
            cam.start()
    print(m,"(tn)")
    time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
    print(time.time()-starttime)
    
    imgs = []
    TIME = np.round(time.time()-starttime,3)
    #print("Before images are taken:",np.round(time.time()-starttime,3))
    if len(simple_pyspin.list_cameras())>len(cams):
        New_connection = True
        print("Will try to reconnect...")
    if goods == 15:
        trys = 0
    for cam in cams:
        try:
            imgs.append(cam.get_array()) # Each image is a numpy array!
            goods +=1
        except:
            goods = 0
            if trys >=2:
                print("camera disconnected...")
                index = np.where(cams == cam)[0][0]
                cams = np.delete(cams,index,0)
                CamNames.pop(index)
                trys = 0
            else:
                imgs.append(None)
                print("img skipped")
                trys +=1
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

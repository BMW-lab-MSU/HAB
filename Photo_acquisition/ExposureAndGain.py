#To get avg exposure time and gain
from simple_pyspin import Camera
from PIL import Image
import os
import time
import simple_pyspin
import numpy as np
from datetime import datetime
import PySpin
import csv
import RPi.GPIO as GPIO

#sets up button
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

#This function searches for all cameras and outputs [cameras, names]
def find_cameras():
    cams = []
    Names = []
    for i in range(len(simple_pyspin.list_cameras())):
        cams = np.append(cams,Camera(i))
        Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
    return(cams,Names)

#similar to the function in HAB_functions, except the auto gain and exposure are set to cont
def initialize_camera(cam):
    cam.stop()
    cam.init()

    # To change the frame rate, we need to enable manual control
    cam.AcquisitionFrameRateEnable = True
    cam.AcquisitionFrameRate = 1

    cam.AcquisitionMode = 'Continuous'


    cam.GainAuto = 'Continuous'

    cam.ExposureAuto = 'Continuous'

    cam.GammaEnable = False

    cam.BlackLevelClampingEnable = False

    #this controles if gain or exposure gets changed first
    #it is set to off to ensure that they will both change
    cam.AutoExposureTargetGreyValueAuto = 'Off'

    #cam.AutoExposureMeteringMode = 'Average'

    cam.AutoExposureControlLoopDamping = 0.2

    cam.ChunkModeActive = False
    try:
        cam.PixelFormat = "Mono16"
    except:
        pass

imageInterval = "1"
#gets current time so that it can check when the last time the exposure and gain was updated
DATE = str(datetime.utcnow())

[cams,CamNames] = find_cameras()
for cam in cams:
    cam.stop()
    cam.close()

[cams,CamNames] = find_cameras()
for cam in cams:
    initialize_camera(cam)
starttime = time.time()
m = 0
trys = 0
goods = 0
#ET = exposure time
#its of size 3 because we are using 3 cameras
ET = [0,0,0]
Gain = [0,0,0]
for cam in cams:
    cam.start()
New_connection = False

while True:
    #stops if the button is pressed
    if GPIO.input(31):
        break
    #connects new camera if detected
    if New_connection:
        for cam in cams:
            try:
                cam.stop()
                cam.close()
            except:
                pass
        cams = []
        CamNames = []
        [cams,CamNames] = find_cameras()
        for cam in cams:
            initialize_camera(cam)
        print("Reconnected...")
    m = m+1
    if New_connection:
        New_connection = False
        for cam in cams:
            cam.start()
    time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second

    TIME = np.round(time.time()-starttime,3)
    
    if len(simple_pyspin.list_cameras())>len(cams):
        New_connection = True
        print("Will try to reconnect...")
    if goods == 15:
        trys = 0
    print()
    print()
    print()
    for i in range(len(cams)):
        try:
            #gets the averages
            cams[i].GainAuto = 'Continuous'
            cams[i].ExposureAuto = 'Continuous'
            Gain[i] = (Gain[i]*(m-1)/m)+(cams[i].Gain/m)
            ET[i] = (ET[i]*(m-1)/m)+(cams[i].ExposureTime/m)
            print(CamNames[i]+" Avgs:")
            print("    Gain avg:"+str(Gain[i]))
            print("    Gain:", cams[i].Gain)
            print("    Exposure Time:"+str(ET[i]))
            print("    Exposure Time:", cams[i].ExposureTime)
            goods +=1
        except:
            goods = 0
            if trys >=2:
                print("camera disconnected...")
                index = i
                cams = np.delete(cams,index,0)
                CamNames.pop(index)
                trys = 0
            else:
                imgs.append(None)
                print("img skipped")
                trys +=1

#opens file, and saves the current time
file = open('Camera_settings.csv','w')
write = csv.writer(file)
write.writerow([DATE])
write.writerow(["Name","Gain","Exposure"])

#saves camera settings
for i in range(len(CamNames)):
    Camera_settings = [CamNames[i],str(Gain[i]),str(ET[i])]
    write.writerow(Camera_settings)

file.close()

for cam in cams:
    cam.stop()
    cam.close()


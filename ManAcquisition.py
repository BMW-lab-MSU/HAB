#ManAcquisition.py
#this script is for calibration purposes and will make a file labeled with the date and CAL
from simple_pyspin import Camera
from PIL import Image
import os
import time
import simple_pyspin
import numpy as np
from datetime import date
import PySpin
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

#Entering the exposure time desired
exposureTime = "15000"
#important because the calibrations are done with specific filters
color = "671nm"
cal_or_dark = "dark"
expected_cameras = 1

#enering the time between taking images
imageInterval = "1"

#this keeps searching for the camera and will not continue if its not there

def find_cameras(expected_length):
    cams = []
    Names = []
    if len(simple_pyspin.list_cameras()) != expected_length:
        print("did not find all cameras, searching...")
        time.sleep(0.5)
        find_cameras(expected_length)
    else:
        for i in range(len(simple_pyspin.list_cameras())):
            cams = np.append(Camera(i),cams)
            Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
        return(cams,Names)

def Initialize_camera(cam):
    cam.init()
    cam.stop()
    cam.AcquisitionFrameRateEnable = True
    cam.AcquisitionFrameRate = 1

    cam.AcquisitionMode = 'Continuous'

    # To control the exposure settings, we need to turn off auto
    cam.GainAuto = 'Off'
    # Set the gain to 0.
    gain = min(0, cam.get_info('Gain')['max'])
    #print("Setting gain to %.1f dB" % gain)
    print(gain)
    cam.Gain = gain
    cam.ExposureAuto = 'Off'
    cam.ExposureTime = int(exposureTime) # microseconds

    cam.GammaEnable = False

    cam.BlackLevelClampingEnable = False

    cam.AutoExposureTargetGreyValueAuto = 'Off'

    cam.AutoExposureControlLoopDamping = 0.2

    cam.ChunkModeActive = False

    cam.PixelFormat = "Mono16"

    


#initialize the cameras and set settings
starttime = time.time()
[cams,CamNames] = find_cameras(expected_cameras)
for cam in cams:
    Initialize_camera(cam)
print("init_time:",time.time()-starttime)


# Make a directory to save some images
# It is set up such that a new folder with the date_CAL/flight# is created
output_dir = str(date.today())+"-CAL"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_dir = output_dir+"/"+color
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

flights = os.listdir(output_dir)
flight_numb = str(len(flights)+1)
output_dir = output_dir+"/"+cal_or_dark+"_"+flight_numb
os.makedirs(output_dir)
for camera in CamNames:
    if not os.path.exists(output_dir+"/"+camera):
        os.makedirs(output_dir+"/"+camera)


starttime = time.time()
m = 0
for cam in cams:
    cam.start()
New_connection = False
Degree = 0
pic_numb = 0
#This code is similar to what is in cont aquisition, except it takes 5 pictures in a
#row and then waits for an input for the next set of images
#it is also important to note that this code is currently set up for degrees
#which represent the angle of the polarizer, but that can be easily changed
while True:
    if New_connection:
        for cam in cams:
            try:
                cam.stop()
                cam.close()
            except:
                print()
        [cams,CamNames] = find_cameras(expected_cameras)
        for cam in cams:
            Initialize_camera(cam)
        print("Reconnected...")
    m = m+1
    print("tick number: ",m)
    #time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
    
    if pic_numb >=5:
        Degree +=15
        print()
        input("current degree:"+str(Degree))
        
        pic_numb=0
    
    print(time.time()-starttime)
    if New_connection:
        New_connection = False
        for cam in cams:
            cam.start()
    imgs = []
    TIME = np.round(time.time()-starttime,3)
    print("Before images are taken:",np.round(time.time()-starttime,3))
    for cam in cams:
        try:
            
            
            imgs.append(cam.get_array()) # Each image is a numpy array!
        except:
            print("Camera disconnected...")
            if(len(simple_pyspin.list_cameras()) == expected_cameras):
               New_connection=True
               print("will try to reconnect...")
            else:
                print("Unable to reconnect")
            imgs.append(None)
        #print(imgs[0].shape, imgs[0].dtype)
        #print("Saving images to: %s" % output_dir)

    
    print("After images are taken:",np.round(time.time()-starttime,3))
    pic_numb+=1
    for i in range(len(cams)):
        
        filename = "G"+str(cams[i].Gain)+"-E"+str(cams[i].ExposureTime)+"-T"+str(TIME)+"-img"+str(pic_numb)
        if cal_or_dark == "cal":
            filename= "-Degree"+str(Degree).zfill(3)+filename
        
        #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
        if type(imgs[i]) != type(None):
            print("min:",np.amin(imgs[i]))
            print("max:",np.amax(imgs[i]))
            np.save(output_dir+"/"+CamNames[i]+"/"+filename,imgs[i])
            
        else:
            print("not saved")
    
    

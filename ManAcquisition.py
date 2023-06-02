#ContAcquisition.py

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
color = "671nm"
expected_cameras = 1

#enering the time between taking images
imageInterval = "1"

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
    #print("camera pixel format is", cam.PixelFormat)

    # To change the frame rate, we need to enable manual control
    cam.AcquisitionFrameRateEnable = True
    cam.AcquisitionFrameRate = 1

    cam.AcquisitionMode = 'Continuous'

    # To control the exposure settings, we need to turn off auto
    cam.GainAuto = 'Off'
    # Set the gain to 20 dB or the maximum of the camera.
    gain = min(0, cam.get_info('Gain')['max'])
    #print("Setting gain to %.1f dB" % gain)
    print(gain)
    cam.Gain = gain
    cam.ExposureAuto = 'Off'
    cam.ExposureTime = int(exposureTime) # microseconds

    #print("Exposure Time: ", cam.ExposureTime)     

    #cam.BalanceWhiteAuto = 'Off'

    #cam.SharpeningAuto = False

    cam.GammaEnable = False

    cam.BlackLevelClampingEnable = False

    #cam.SaturationEnable = False

    #cam.AasRoiEnable = False

    cam.AutoExposureTargetGreyValueAuto = 'Off'

    #cam.AutoExposureMeteringMode = 'Average'

    cam.AutoExposureControlLoopDamping = 0.2

    #cam.AutoExposureControlPriority = 'Gain'

    cam.ChunkModeActive = False

    cam.PixelFormat = "Mono16"

    

#get all cameras connected to the pi




#initialize the cameras and set settings
starttime = time.time()
[cams,CamNames] = find_cameras(expected_cameras)
for cam in cams:
    Initialize_camera(cam)
print("init_time:",time.time()-starttime)


# Make a directory to save some images
# It is set up such that a new folder with the date/flight# is created
output_dir = str(date.today())+"_CAL"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
flights = os.listdir(output_dir)
flight_numb = str(len(flights)+1)
output_dir = output_dir+"/cal_"+color+"_"+flight_numb
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
    #put gps here
    pic_numb+=1
    print("After images are taken:",np.round(time.time()-starttime,3))
    for i in range(len(cams)):
        
        filename = "G"+str(cams[i].Gain)+"-E"+str(cams[i].ExposureTime)+"-T"+str(TIME)+"-img_"+str(pic_numb)+"-"
        filename = filename.replace(".","_",3)
        filename= filename+"_Dark"
        #filename= filename+"Degree_"+str(Degree)
        
        #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
        if type(imgs[i]) != type(None):
            print("min:",np.amin(imgs[i]))
            print("max:",np.amax(imgs[i]))
            np.save(output_dir+"/"+CamNames[i]+"/"+filename,imgs[i])
        else:
            print("not saved")
    

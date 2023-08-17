"""
Created on Jun 25 2023

@author: Flint Morgan
"""
#ManAcquisition.py
#this script is for calibration purposes and will make a file labeled with the date and CAL

from simple_pyspin import Camera
import time
import simple_pyspin
import numpy as np
import PySpin
import os
import pandas as pd
#Entering the exposure time desired



def find_cameras():
    cams = []
    Names = []
    for i in range(len(simple_pyspin.list_cameras())):
        cams = np.append(cams,Camera(i))
        Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
    return(cams,Names)

def Initialize_camera(cam,gain,exposureTime):
    #The camera can't be running while the settings are being changed, hence the
    #cam.stop
    cam.stop()
    cam.init()

    # To change the frame rate, we need to enable manual control
    cam.AcquisitionFrameRateEnable = True
    cam.AcquisitionFrameRate = 1

    if cam.AcquisitionMode != 'Continuous':
        cam.AcquisitionMode = 'Continuous'

    # To control the exposure settings, we need to turn off auto
    cam.GainAuto = "Off"
    cam.Gain = gain
    cam.ExposureAuto = 'Off'
    cam.ExposureTime = exposureTime # microseconds
  

    #cam.BalanceWhiteAuto = 'Off' # not on grayscale cameras

    #cam.SharpeningAuto = False
    if cam.GammaEnable:
        cam.GammaEnable = False
    if cam.BlackLevelClampingEnable:
        cam.BlackLevelClampingEnable = False

    #cam.SaturationEnable = False

    #cam.AasRoiEnable = False
    if cam.AutoExposureTargetGreyValueAuto != 'Off':
        cam.AutoExposureTargetGreyValueAuto = 'Off'

    #cam.AutoExposureMeteringMode = 'Average'
    if cam.AutoExposureControlLoopDamping != 0.2:
        cam.AutoExposureControlLoopDamping = 0.2

    #cam.AutoExposureControlPriority = 'Gain'
    if cam.ChunkModeActive:
        cam.ChunkModeActive = False
    # once this is changed once it cant be changed agian while the camera has power
    #the try statement is to prevent a crash in the event it has already been set
    try:
        cam.PixelFormat = "Mono16"
    except:
        pass

def man(gain,exposureTime):
    imageInterval = "1"
    #initialize the cameras and set settings
    starttime = time.time()
    [cams,CamNames] = find_cameras()
    
    
    #This stops the cameras to ensure the settigns can be changed
    for cam in cams:
        cam.stop()
        cam.close()
    #initialize the cameras and set settings
    [cams,CamNames] = find_cameras()   
    for cam in cams:
        Initialize_camera(cam,gain,exposureTime)
    print("init_time:",time.time()-starttime)
    
    
    # Make a directory to save some images
    # It is set up such that a new folder with the date_CAL/flight# is created
    
    
    
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
    input("start:")
    I90avg = 0
    I45avg = 0
    I0avg  = 0
    I135avg= 0
    while True:
        if New_connection:
            for cam in cams:
                try:
                    cam.stop()
                    cam.close()
                except:
                    print()
            [cams,CamNames] = find_cameras()
            for cam in cams:
                Initialize_camera(cam)
            print("Reconnected...")
        m = m+1
        time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
        
        if pic_numb >=5:
            Degree +=15
            print("I90:",I90avg)
            print("I45:",I45avg)
            print("I0:",I0avg)
            print("I135:",I135avg)
            radiometric = input("\nGet next values (stop or q to stop):").lower()
            I90avg = 0
            I45avg = 0
            I0avg  = 0
            I135avg= 0
            if radiometric == "stop" or "q" in radiometric.lower():
                break
            
            pic_numb=0
        
        if New_connection:
            New_connection = False
            for cam in cams:
                cam.start()
        imgs = []
        TIME = np.round(time.time()-starttime,3)
        for cam in cams:
            cam.stop()
            cam.start()
            try:
                
                
                imgs.append(cam.get_array()) # Each image is a numpy array!
            except:
                print("Camera disconnected...")
                if(len(simple_pyspin.list_cameras()) > len(cams)):
                   New_connection=True
                   print("will try to reconnect...")
                else:
                    print("Unable to reconnect")
                imgs.append(None)
            #print(imgs[0].shape, imgs[0].dtype)
            #print("Saving images to: %s" % output_dir)
    
        
        pic_numb+=1
        for i in range(len(cams)):
    
            #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
            if type(imgs[i]) != type(None):
                raw = imgs[i]
                I90 = np.mean(raw.astype(float)[::2,::2])
                I45 = np.mean(raw.astype(float)[::2,1::2])
                I0  = np.mean(raw.astype(float)[1::2,1::2])
                I135= np.mean(raw.astype(float)[1::2,::2])
                I90avg += (I90*0.2)
                I45avg += (I45*0.2)
                I0avg  += (I0*0.2)
                I135avg+= (I135*0.2)
                
                
            else:
                print("Img not taken")
        
    for cam in cams:
        cam.stop()
        cam.close()

[cams,CamNames] = find_cameras()
camName = int(CamNames[0])
#This stops the cameras to ensure the settigns can be changed
for cam in cams:
    cam.stop()
    cam.close()
Month_dir = "Z:Flathead-Aug-2023/"
Month_output= "Z:Flathead-Aug-2023-Cal/"
for day in os.listdir(Month_dir):
    for time_dir in os.listdir(Month_dir+day):
        print(Month_dir+day+"/"+time_dir)
        for file in os.listdir(Month_dir+day+"/"+time_dir):
            if file == "Camera_settings.csv":
                print("\n\n\n\n")
                settings = pd.read_csv(Month_dir+day+"/"+time_dir+"/"+file,skiprows=1)
                gain = settings['Gain'][settings['Name']==camName].tolist()[0]
                exposure = settings['Exposure'][settings['Name']==camName].tolist()[0]
                output_dir=Month_output+day+"/"+time_dir+"/"
                print(settings)
                print(gain,exposure)
                man(gain,exposure)
                print(output_dir)
                print()
                #polarization_cal(exposure,gain,output_dir)
#enering the time between taking images


#this keeps searching for the camera and will not continue if its not there



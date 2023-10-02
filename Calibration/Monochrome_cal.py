#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 15:06:53 2023

@author: Flint Morgan
"""

import Monochromator_class
import Cal_functions
from simple_pyspin import Camera
import os
import time
import simple_pyspin
import numpy as np
import pandas as pd
from datetime import date
import PySpin

#Blue 440 nm 58
#Red 660/671 nm 73
#green 550nm 72

#Entering the exposure time desired

#gain = 10.721805051364594
#exposureTime = 14407.615384615385
#important because the calibrations are done with specific filters


def Monochrome_cal(exposureTime,gain,output_dir, wavelengths):
    print("connecting to monochromator...")
    Possible_cameras = ["22027758","22027772","22027773"]
    colors = ["440nm","550nm","660nm"]
    MC = Monochromator_class.monochromator()
    #enering the time between taking images
    print("conected")
    imageInterval = "1"
    #initialize the cameras and set settings
    starttime = time.time()
    [cams,CamNames] = Cal_functions.find_cameras()
    
    
    #This stops the cameras to ensure the settigns can be changed
    for cam in cams:
        cam.stop()
        cam.close()
    #initialize the cameras and set settings
    cams = []
    CamNames = []
    [cams,CamNames] = Cal_functions.find_cameras()   
    for cam in cams:
        Cal_functions.Initialize_camera(cam,gain,exposureTime)
    for name in CamNames:
        for i in range(len(Possible_cameras)):
            if name == Possible_cameras[i]:
                color = colors[i]
    print("init_time:",time.time()-starttime)
    CamNames[0] = color+"-"+CamNames[0]+"-E"+str(exposureTime)+"-G"+str(gain)
    CamNames[0] = CamNames[0].replace(".", "_")
    
    # Make a directory to save some images
    # It is set up such that a new folder with the date_CAL/flight# is created


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for camera in CamNames:
        if not os.path.exists(output_dir+"/"+camera):
            os.makedirs(output_dir+"/"+camera)
    
    
    starttime = time.time()
    m = 0
    for cam in cams:
        cam.start()
    
    index = 0
    pic_numb = 0
    MC.Set_wavelength(wavelengths[0])
    time.sleep(2)
    #This code is similar to what is in cont aquisition, except it takes 5 pictures in a
    #row and then waits for an input for the next set of images
    #it is also important to note that this code is currently set up for degrees
    #which represent the angle of the polarizer, but that can be easily changed
    crash = False
    time.sleep(1)
    cams[0].ExposureAuto = 'Continuous'
    time.sleep(2)
    exposureTime = (cams[0].ExposureTime)
    cams[0].ExposureAuto = 'Off'
    cams[0].ExposureTime = exposureTime
    while True:
        m = m+1
        print("tick number: ",m)
        
        
        time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
    
        
        if pic_numb >=5:
            index +=1
            print()
            if index > len(wavelengths)-1:
                break
            time.sleep(1)
            MC.Set_wavelength(wavelengths[index])
            time.sleep(2)
            
            print("\nWavelengthto be taken:"+str(wavelengths[index]))
            print("Wavelength of rotation stage:", MC.cur_nm)
            
            cams[0].ExposureAuto = 'Continuous'
            time.sleep(2)
            exposureTime = (cams[0].ExposureTime)
            cams[0].ExposureAuto = 'Off'
            cams[0].ExposureTime = exposureTime

            
            
            pic_numb=0
        
        print(time.time()-starttime)
    
        imgs = []
        TIME = np.round(time.time()-starttime,3)
        
        #takes pictures
        for cam in cams:
            cam.stop()
            cam.start()
            time.sleep(0.1)
            try:
                imgs.append(cam.get_array()) # Each image is a numpy array!
            except:
                print("image skipped stopping program")
                crash = True
                break
            #print(imgs[0].shape, imgs[0].dtype)
            #print("Saving images to: %s" % output_dir)
    
        
        print("After images are taken:",np.round(time.time()-starttime,3))
        pic_numb+=1
        for i in range(len(cams)):
            
            filename = "Img"+str(pic_numb)+"-E"+str(cams[i].ExposureTime)+"-T"+str(TIME)+"-G"+str(cams[i].Gain)
            filename=filename.replace(".","_")
            filename= "MCWavelength"+str(wavelengths[index]).zfill(3)+"-"+filename
            filename = color+"-"+"MonoChromeCal"+"-"+filename
            
            #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
            if type(imgs[i]) != type(None):
                print("min:",np.amin(imgs[i]))
                print("max:",np.amax(imgs[i]))
                print("mean:",np.mean(imgs[i]))
                np.save(output_dir+"/"+CamNames[i]+"/"+filename,imgs[i])
                
            else:
                print("not saved")
    if not crash:  
        Cal_functions.send_text("Pol Cal done", "Calibration of "+CamNames[0]+" complete.")  
        for cam in cams:
            cam.stop()
            cam.close()
        MC.close()
        Cal_functions.polarization_cal_check(output_dir+"/"+camera)
    else: 
        Cal_functions.send_text("Crash", "The program crashed at",wavelengths[index]) 


#ensure only one camera is connected to the computer at a time
[cams,CamNames] = Cal_functions.find_cameras()
camName = int(CamNames[0])
#This stops the cameras to ensure the settigns can be changed
for cam in cams:
    cam.stop()
    cam.close()
Month_dir = "Z:Flathead-Aug-2023/"
Month_output= "Z:Flathead-Aug-2023-MonoCal/"
day = "2023-08-14"

for time_dir in os.listdir(Month_dir+day):
    print(Month_dir+day+"/"+time_dir)
    for file in os.listdir(Month_dir+day+"/"+time_dir):
        if file == "Camera_settings.csv":
            settings = pd.read_csv(Month_dir+day+"/"+time_dir+"/"+file,skiprows=1)
            gain = settings['Gain'][settings['Name']==camName].tolist()[0]
            exposure = settings['Exposure'][settings['Name']==camName].tolist()[0]
            output_dir=Month_output+day+"/"+time_dir+"/"
            print(settings)
            print(gain,exposure)
            print(output_dir)
            print()
            Monochrome_cal(exposure,gain,output_dir)
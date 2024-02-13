#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:52:52 2023

@author: Flint Morgan
"""
import smtplib, ssl
import simple_pyspin
from simple_pyspin import Camera
import os
import time
import simple_pyspin
import numpy as np
from datetime import date
import PySpin
import matplotlib.pyplot as plt


#This is a relatively quick check after the polarization data is taken to see if the data taken is correct
#The result should be four equally offset sin functions
def polarization_cal_check(DIR):
    deg_pol = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    angles = [0,-15,-30,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330,-345,-360]
    photos = np.zeros([2048,2448,len(deg_pol)])
    to_remove="PolCalGETImgDegr_nm"
    fig = plt.figure()
    colors = ["green","blue","yellow","red","orange"]
    #gets and plots the average value of each quadrent of the superpixel and arranges them in order
    for image_file in os.listdir(DIR):
        if "polcal" in image_file.lower():
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
    
            image_np = np.load(DIR+"/"+image_file)
            raw = image_np
            I90 = np.mean(raw.astype(float)[::2,::2])
            I45 = np.mean(raw.astype(float)[::2,1::2])
            I0  = np.mean(raw.astype(float)[1::2,1::2])
            I135= np.mean(raw.astype(float)[1::2,::2])
            #plots each point
            plt.subplot(2,2,1)
            plt.scatter(info[1],I90,c=colors[int(info[2]-1)])
            plt.title("(0,0)")
            plt.subplot(2,2,2)
            plt.scatter(info[1],I45,c=colors[int(info[2]-1)])
            plt.title("(0,1)")
            plt.subplot(2,2,3)
            plt.scatter(info[1],I135,c=colors[int(info[2]-1)])
            plt.title("(1,0)")
            plt.subplot(2,2,4)
            plt.scatter(info[1],I0,c=colors[int(info[2]-1)])
            plt.title("(1,1)")
            #print(image_file,int(info[0]/15),"\n")
            photos[:,:,int(info[1]/15)]=photos[:,:,int(info[1]/15)]+(0.2*image_np)
    
    
    fig.tight_layout()
    plt.show()
    

#finds cameras pluged in and returns them with a name
def find_cameras():
    cams = []
    Names = []
    for i in range(len(simple_pyspin.list_cameras())):
        cams = np.append(cams,Camera(i))
        Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
    return(cams,Names)

#Creates the appropriate dir
def New_cameras(cams,output_dir,gain,exposureTime):
    for cam in cams:
        cam.stop()
        cam.close()
    cams = []
    CamNames = []
    [cams,CamNames] = find_cameras()
    for cam in cams:
        Initialize_camera(cam,gain,exposureTime)

    for camera in CamNames:
        if not os.path.exists(output_dir+"/"+camera):
            os.makedirs(output_dir+"/"+camera)

    for cam in cams:
        cam.start()
    return(cams,CamNames)

#initializes camera with desired gain and exposure
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

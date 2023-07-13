import simple_pyspin
import time
import numpy as np
from simple_pyspin import Camera
import PySpin
import adafruit_gps
import serial
import RPi.GPIO as GPIO

#This function searches for all cameras and outputs [cameras, names]
def find_cameras():
    cams = []
    Names = []
    for i in range(len(simple_pyspin.list_cameras())):
        cams = np.append(cams,Camera(i))
        Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
    return(cams,Names)


#This function initializes the cameras to have the desired parameters
#sometimes in re-initialization the cameras can already have the proper settings
#saved, hence the if statements
#there are many commented out sections, this is because they are not writable with
#the cameras we have, but may prove useful in the future
def Initialize_camera(cam,gain,exposureTime):
    #The camera can't be running while the settings are being changed, hence the
    #cam.stop
    cam.stop()
    cam.init()

    #if cam.FileAccessBuffer:
    #    cam.FileAccessBuffer = False
    if cam.FileAccessLength != 0:
        cam.FileAccessLength = 0
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

#waits for gpio pin to be high
def wait_for_edge(pin):
    while True:
        time.sleep(0.05)
        if GPIO.input(pin):
            break
#same as previous, but also checks if the gps has a fix so that it doesnt wait for an edge that will never come
def wait_for_edge_gps(pin,gps):
    while True:
        gps.update()
        time.sleep(0.05)
        if GPIO.input(pin) or not gps.has_fix:
            break
#gets GPS data
def GPS(gps):
    if gps.has_fix:
        Lat = str(gps.latitude)
        Long = str(gps.longitude)
        Height = str(gps.altitude_m)
        TIME = gps.timestamp_utc
        TIME = TIME[:-3]
        Time = "-".join([str(i) for i in TIME])
        return(Lat,Long,Height,Time)
    else:
        return("NaN","NaN","NaN","NaN")

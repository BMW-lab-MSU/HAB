import simple_pyspin
import time
import numpy as np
from simple_pyspin import Camera
import PySpin
import adafruit_gps
import serial

#This function searches for all cameras and outputs [cameras, names] and takes an input of the expected length
def find_cameras():
    cams = []
    Names = []
    for i in range(len(simple_pyspin.list_cameras())):
        cams = np.append(cams,Camera(i))
        Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
    return(cams,Names)


#This function initializes the cameras to have the desired parameters
def Initialize_camera(cam,gain,exposureTime):
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

    #print("Exposure Time: ", cam.ExposureTime)     

    #cam.BalanceWhiteAuto = 'Off'

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
        cam.ChunkModeActive = Falses
    try:
        cam.PixelFormat = "Mono16"
    except:
        pass


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

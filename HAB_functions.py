import simple_pyspin
import time
import numpy as np
from simple_pyspin import Camera
import PySpin
import adafruit_gps
import serial

#This function searches for all cameras and outputs [cameras, names] and takes an input of the expected length
def find_cameras(expected_length):
    cams = []
    Names = []
    if len(simple_pyspin.list_cameras()) != expected_length:
        print("did not find all cameras, searching...")
        time.sleep(0.5)
        [cams,Names]=find_cameras(expected_length)
        return(cams,Names)
    else:
        for i in range(len(simple_pyspin.list_cameras())):
            cams = np.append(Camera(i),cams)
            Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
        return(cams,Names)


#This function initializes the cameras to have the desired parameters
def Initialize_camera(cam):
    cam.stop()
    #cam.close()
    cam.init()
    #print("camera pixel format is", cam.PixelFormat)

    # To change the frame rate, we need to enable manual control
    cam.AcquisitionFrameRateEnable = True
    cam.AcquisitionFrameRate = 1

    cam.AcquisitionMode = 'Continuous'

    # To control the exposure settings, we need to turn off auto
    cam.GainAuto = 'Continuous'
    # Set the gain to 20 dB or the maximum of the camera.
    #gain = min(0, cam.get_info('Gain')['max'])
    #print("Setting gain to %.1f dB" % gain)
    #cam.Gain = gain
    cam.ExposureAuto = 'Continuous'
    #cam.ExposureTime = int(exposureTime) # microseconds

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

    cam.AutoExposureControlPriority = 'Gain'

    cam.ChunkModeActive = False



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

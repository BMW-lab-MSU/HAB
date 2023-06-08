#To get avg exposure time and gain
import HAB_functions
from simple_pyspin import Camera
from PIL import Image
import os
import time
import simple_pyspin
import numpy as np
from datetime import date
import PySpin

def initialize_camera(cam):
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
    try:
        cam.PixelFormat = "Mono16"
    except:
        pass

imageInterval = "1"

[cams,CamNames] = HAB_functions.find_cameras()
for cam in cams:
    cam.stop()
    cam.close()

[cams,CamNames] = HAB_functions.find_cameras()
for cam in cams:
    initialize_camera(cam)
starttime = time.time()
m = 0
trys = 0
goods = 0
ET = [0,0,0]
Gain = [0,0,0]
for cam in cams:
    cam.start()
New_connection = False
input("Press enter to start averaging")

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
            cams[i].GainAuto = 'Continuous'
            cams[i].ExposureAuto = 'Continuous'
            #cams[i].stop
            Gain[i] = (Gain[i]*(m-1)/m)+(cams[i].Gain/m)
            ET[i] = (ET[i]*(m-1)/m)+(cams[i].ExposureTime/m)
            print(CamNames[i]+" Avgs:")
            print("    Gain avg:"+str(Gain[i]))
            print("    Gain:", cams[i].Gain)
            print("    Exposure Time:"+str(ET[i]))
            print("    Exposure Time:", cams[i].ExposureTime)
            #cams[i].start()
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




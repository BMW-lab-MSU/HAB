#ManAcquisition.py
#this script is for calibration purposes and will make a file labeled with the date and CAL

from simple_pyspin import Camera
import time
import simple_pyspin
import numpy as np
import PySpin

#Entering the exposure time desired
gain = 12.460766915206191
exposureTime = 14316.244444444443


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




#enering the time between taking images
imageInterval = "1"

#this keeps searching for the camera and will not continue if its not there



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
    print("tick number: ",m)
    time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
    
    if pic_numb >=5:
        Degree +=15
        print()
        radiometric = input("\nGet next values (stop or q to stop):"+str(Degree)).lower()
        if radiometric == "stop" or "q" in radiometric.lower():
            break
        
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

    
    print("After images are taken:",np.round(time.time()-starttime,3))
    pic_numb+=1
    for i in range(len(cams)):

        #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
        if type(imgs[i]) != type(None):
            raw = imgs[i]
            I90 = raw.astype(float)[::2,::2]
            I45 = raw.astype(float)[::2,1::2]
            I0  = raw.astype(float)[1::2,1::2]
            I135= raw.astype(float)[1::2,::2]
            print("min:",np.amin(imgs[i]))
            print("max:",np.amax(imgs[i]))
            print("mean:",np.mean(imgs[i]))
            print("I90:",np.mean(I90))
            print("I45:",np.mean(I45))
            print("I0:",np.mean(I0))
            print("I135:",np.mean(I135))
            
        else:
            print("Img not taken")
    
for cam in cams:
    cam.stop()
    cam.close()

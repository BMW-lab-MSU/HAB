#ManAcquisition.py
#this script is for calibration purposes and will make a file labeled with the date and CAL
import HAB_functions
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
gain = 0
exposureTime = 4000
#important because the calibrations are done with specific filters
color = "58"
cal_or_dark = "cal"

#enering the time between taking images
imageInterval = "1"

#this keeps searching for the camera and will not continue if its not there



#initialize the cameras and set settings
starttime = time.time()
[cams,CamNames] = HAB_functions.find_cameras()
for cam in cams:
    HAB_functions.Initialize_camera(cam,gain,exposureTime)
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
radiometric = input("start at 0 Degree")
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
    time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
    
    if pic_numb >=5:
        Degree +=15
        print()
        radiometric = input("\nDegree to be taken:"+str(Degree)).lower()
        if radiometric == "stop":
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
        
        filename = "Img"+str(pic_numb)+"-E"+str(cams[i].ExposureTime)+"-T"+str(TIME)+"-G"+str(cams[i].Gain)
        filename=filename.replace(".","_")
        if cal_or_dark == "cal":
            filename= "Degree"+str(Degree).zfill(3)+"-"+filename
        elif cal_or_dark == "radiometric":
            filename = "current(ua)"+radiometric+"-"+filename
        
        #Image.fromarray(imgs[i]).save(os.path.join(output_dir+"/"+CamNames[i]+"/"+filename)) #Files named based on m
        if type(imgs[i]) != type(None):
            print("min:",np.amin(imgs[i]))
            print("max:",np.amax(imgs[i]))
            print("mean:",np.mean(imgs[i]))
            np.save(output_dir+"/"+CamNames[i]+"/"+filename,imgs[i])
            
        else:
            print("not saved")
    
    

"""
Created on Jul 24 2023

@author: Flint Morgan
"""

import simple_pyspin
import numpy as np
from simple_pyspin import Camera
import PySpin
import os
import csv



"""
class CAMERAS
    functions:
        find_cameras():
            finds all cameras connected and gets the camera obj and names
        init_cam_internal(cam = simple_pyspin cam obj,gain,exposureTime):
            turns off all auto settings and sets gain and exposure time to what is input. 
        DIR_Flights(self,top_folder):
            makes flight folder in top_folder
        DIR_cams():
            makes camera folders
        init_cams():
            inits cams and calls init_cam_internal with the correct gain and exposure time
        start():
            starts taking photos
        Reconnect(self,TIME = time passed since first frame,frame_num = frame number):
            reconnects the cameras (used if one drops out and then is detected again, or if a new camera is detected)
        Detect_cameras(self,TIME = time passed since first frame,frame_num = frame number):
            Detects if new cameras are connected
        take_and_save(self,TIME = time passed since first frame,frame_num = frame number):
            takes and saves pictures to the folder created in the DIR functions
        close():
            properly closes cameras
            
    variables:
        cams = simple_pyspin camera objects
        CamNames = serial number of the cams
        serial_numbs = serial numbres of the cameras
        gain = gain for each of the cameras
        exposure_time = exposure time of each of the cameras
        file_endings = endings of each of the files by camera (not a file extention but a way to tell the files apart)
        trys = times the camera has failed to take a picture
        goods = times in a row the camera has taken a picture
        output_dir = where images are saved
        New_connection = bool describing if a new connection has been found
        
"""

class CAMERAS:
    
    #finds all cameras connected and gets the camera object and the names
    def find_cameras(self):
        cams = []
        Names = []
        for i in range(len(simple_pyspin.list_cameras())):
            cams = np.append(cams,Camera(i))
            Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
        self.cams = cams
        self.CamNames = Names


    #gets the names and objects of the cameras and gets what thier settings should be from a settings file
    def __init__(self,serial_numbs=["58","72","73"],file_endings=["440nm","550nm","660nm"], gain=[0,0,0], exposure_time=[25000,25000,25000]):
        self.serial_numbs = serial_numbs;self.gain = gain;self.exposure_time=exposure_time;self.file_endings=file_endings
        settings_file = open('Camera_settings.csv','r')
        settings = csv.reader(settings_file,delimiter = ',')
        for line in settings:
            for i in range(len(serial_numbs)):
                if line[0] == "220277"+serial_numbs[i]:
                    self.gain[i] = float(line[1])
                    if float(line[2])>=100:
                        self.exposure_time[i] = float(line[2])
        settings_file.close()
        self.find_cameras()
        for cam in self.cams:
            cam.stop()
            cam.close()
        self.find_cameras()
        self.trys = 0
        self.goods = 0

    #sets the settings of the cameras
    def init_cam_internal(self,cam,gain,exposureTime):
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
        if cam.PixelFormat != "Mono16":
            cam.PixelFormat = "Mono16"
            
    def DIR_Flights(self,top_folder):
        flights = os.listdir(top_folder)
        flight_numb = str(len(flights)+1)
        output_dir = top_folder+"/Flight_"+flight_numb
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def DIR_cams(self):
        for camera in self.CamNames:
            if not os.path.exists(self.output_dir+"/"+camera):
                os.makedirs(self.output_dir+"/"+camera)
            
    def init_cams(self):
        for i in range(len(self.cams)):
            print(self.CamNames[i][-2:])
            for j in range(len(self.serial_numbs)):
                if self.serial_numbs[j] == self.CamNames[i][-2:]:
                    print("init")
                    self.init_cam_internal(self.cams[i],self.gain[j],self.exposure_time[j])

    def start(self):
        for cam in self.cams:
            cam.stop()
            cam.start()
            try:
                cam.get_array()
            except:
                pass
        self.New_connection = False

    def Reconnect(self,TIME,frame_num):
        for cam in self.cams:
            cam.stop()
            cam.close()
        self.find_cameras()
        self.init_cams()
        self.DIR_cams()
        LOG = open(self.output_dir+"/Log.csv",'a')
        write_log = csv.writer(LOG)
        write_log.writerow([round((TIME),3),frame_num,"Reconnected..."])
        LOG.close()
        self.start()
        self.New_connection = False

    def Detect_cameras(self,TIME,frame_num):
        if len(simple_pyspin.list_cameras())>len(self.cams):
            self.New_connection = True
            LOG = open(self.output_dir+"/Log.csv",'a')
            write_log = csv.writer(LOG)
            write_log.writerow([round((TIME),3),frame_num,"Will try to reconnect..."])
            LOG.close()
        if self.goods == 5:
            self.trys = 0

    def take_and_save(self,TIME,frame_num):
        i =0
        imgs=[]
        while i < (len(self.cams)):
            current_img = "text"
            try:
                current_img = self.cams[i].get_array()
            except:
                pass
            
            if type(current_img) != type("text"):
                imgs.append(current_img) # Each image is a numpy array!
                self.goods +=1
            else:
                self.goods = 0
                if self.trys >=2:
                    LOG = open(self.output_dir+"/Log.csv",'a')
                    write_log = csv.writer(LOG)
                    write_log.writerow([round((TIME),3),frame_num,"camera "+self.CamNames[i]+" disconnected..."])
                    LOG.close()
                    self.cams = np.delete(self.cams,i,0)
                    self.CamNames.pop(i)
                    self.trys = 0
                    i-=1
                else:
                    imgs.append(None)
                    LOG = open(self.output_dir+"/Log.csv",'a')
                    write_log = csv.writer(LOG)
                    write_log.writerow([round((TIME),3),frame_num,"img skipped"])
                    LOG.close()
                    self.trys +=1
            i+=1
        
        #saving the images as numpy arrays
        for i in range(len(self.cams)):
            for j in range(len(self.serial_numbs)):
                    if "220277"+self.serial_numbs[j] == self.CamNames[i]:
                        file_ending = self.file_endings[j]
            filename = "F"+str(frame_num).zfill(5)+"-T"+str(TIME)+"-G"+str(self.cams[i].Gain)+"-E"+str(self.cams[i].ExposureTime)+"-"+file_ending
            filename = filename.replace(".","_",3)
            
            #makes sure the image exists
            if type(imgs[i]) != type(None):
                np.save(self.output_dir+"/"+self.CamNames[i]+"/"+filename,imgs[i])
            else:
                print("not saved")

    def close(self):
        for cam in self.cams:
            cam.stop()
            cam.close()
    
    def cleanup(self):
        self.close()
        os.system('mv Camera_settings.csv '+self.output_dir+"/")

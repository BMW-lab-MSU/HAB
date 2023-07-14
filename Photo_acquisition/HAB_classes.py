import simple_pyspin
import time
import numpy as np
from simple_pyspin import Camera
import PySpin
import os
import csv
import adafruit_gps
import RPi.GPIO as GPIO

class GPS:
    def __init__(self):
        #initializes the pps pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

        #GPS initialization
        uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=None)
        self.gps = adafruit_gps.GPS(uart, debug=False)
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # Turn off everything:
        self.gps.send_command(b'PMTK220,1000')

        #makes GPS data file
        file = open(output_dir+"/GPS_DATA.csv",'w')
        write = csv.writer(file)
        write.writerow(["Latitude","Longitude","Altitude[m]","UTC","Frame"])
        file.close()
        
    def get_dir(self):
        self.gps.update()
        if self.gps.has_fix:
            self.gps.timestamp_utc
            time.sleep(2)
            self.gps.update()
            if self.gps.has_fix:
                Date = self.gps.timestamp_utc
                Date = Date[:-3]
                DATE = "-".join([str(i).zfill(2) for i in Date])
                DATE = DATE[:-9]
                self.output_dir = DATE
        else:
            self.output_dir = str(date.today())
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def frame_timming(self,imageInterval):
        self.gps.update()

        time_since_last_frame = 0
        if self.gps.has_fix:
            while time_since_last_frame < int(imageInterval):
                self.gps.update()
                if not self.gps.has_fix:
                    break
                HAB_functions.wait_for_edge_gps(7,gps)
                time_since_last_frame += 1
                print("GPS:",m)




class CAMERAS:
    def find_cameras(self):
        cams = []
        Names = []
        for i in range(len(simple_pyspin.list_cameras())):
            cams = np.append(cams,Camera(i))
            Names.append(PySpin.CStringPtr(Camera(i).cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber')).GetValue())
        self.cams = cams
        self.CamNames = Names
    
    def __init__(self,serial_numbs=["58","72","73"],wavelengths=["440nm","550nm","671nm"], gain=[0,0,0], exposure_time=[25000,25000,25000],imageInterval="1"):
        self.serial_numbs = serial_numbs;self.gain = gain;self.exposure_time=exposure_time;self.wavelengths=wavelengths
        settings_file = open('Camera_settings.csv','r')
        settings = csv.reader(settings_file,delimiter = ',')
        for line in settings:
            for i in range(len(serial_numbs)):
                if line[0][-2:] == serial_numbs[i]:
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
        try:
            cam.PixelFormat = "Mono16"
        except:
            pass

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
            cam.get_array()
        self.New_connection = False

    def Reconnect(self):
        for cam in self.cams:
            cam.stop()
            cam.close()
        self.find_cameras()
        self.init_cams()
        self.DIR_cams()
        LOG = open(self.output_dir+"/Log.csv",'a')
        write_log = csv.writer(LOG)
        write_log.writerow([round((time.time() - starttime),3),m,"Reconnected..."])
        LOG.close()
        self.start()
        self.New_connection = False

    def Detect_cameras(self):
        if len(simple_pyspin.list_cameras())>len(self.cams):
            self.New_connection = True
            LOG = open(self.output_dir+"/Log.csv",'a')
            write_log = csv.writer(LOG)
            write_log.writerow([round((time.time() - starttime),3),m,"Will try to reconnect..."])
            LOG.close()
        if self.goods == 5:
            self.trys = 0

    def take_and_save(self,m,TIME):
        i =0
        imgs=[]
        while i < (len(self.cams)):
            current_img = "text"
            try:
                for j in range(100):
                    current_img = self.cams[j].get_array()
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
                    write_log.writerow([round((time.time() - starttime),3),m,"camera "+CamNames[i]+" disconnected..."])
                    LOG.close()
                    self.cams = np.delete(self.cams,i,0)
                    self.CamNames.pop(i)
                    self.trys = 0
                    i-=1
                else:
                    self.imgs.append(None)
                    LOG = open(self.output_dir+"/Log.csv",'a')
                    write_log = csv.writer(LOG)
                    write_log.writerow([round((time.time() - starttime),3),m,"img skipped"])
                    LOG.close()
                    self.trys +=1
            i+=1

        #saving the images as numpy arrays
        for i in range(len(self.cams)):
            for i in range(len(self.cams)):
                print(self.CamNames[i][-2:])
                for j in range(len(self.serial_numbs)):
                    if self.serial_numbs[j] == self.CamNames[i][-2:]:
                        print("init")
                        wave = self.wavelengths[j]
            filename = "F"+str(m).zfill(5)+"-T"+str(TIME)+"-G"+str(self.cams[i].Gain)+"-E"+str(self.cams[i].ExposureTime)+"-"+wave
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

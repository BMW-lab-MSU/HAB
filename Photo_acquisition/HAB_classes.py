import simple_pyspin
import time
import numpy as np
from simple_pyspin import Camera
import PySpin
import os
import csv
import adafruit_gps
import RPi.GPIO as GPIO
import serial
from datetime import date



"""
class GPS
    functions:
        make_csv():
            makes cvs that holds gps data
        get_dir():
            gets and makes dir based on current day
        wait_for_edge_gps(pin=pps pin):
            waits for the pps (pulse per second) pin to show high
        frame_timing(imageInterval=time between frames,starttime= when to base timing from,frame_num= frame #):
            waits for an imageInterval amount of time
        data():
            gets gps data in a way easy to save to a csv
        save_data(frame_num=frame #):
            gets and saves gps data to the csv that make_csv makes

    variables:
        gps=reference to the GPS object from adafruit_gps
        output_dir=place where GPC_DATA.csv is saved      
"""


class GPS:
    #initializes the GPS
    def __init__(self):
        #initializes the pps pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

        #GPS initialization
        uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=None)
        self.gps = adafruit_gps.GPS(uart, debug=False)
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # Turn off everything:
        self.gps.send_command(b'PMTK220,1000')

    #makes the csv that holds the gps data
    def make_csv(self):
        #makes GPS data file
        file = open(self.output_dir+"/GPS_DATA.csv",'w')
        write = csv.writer(file)
        write.writerow(["Latitude","Longitude","Altitude[m]","UTC","Frame"])
        file.close()

    #gets the day from either the gps or system  
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
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    #waits for the pps on the gps and will break if there is no fix
    def wait_for_edge_gps(self,pin):
        while True:
            self.gps.update()
            time.sleep(0.05)
            if GPIO.input(pin) or not self.gps.has_fix:
                break

    #will wait a number of seconds = imageInterval
    #starttime is needed if there is no gps fix so the system clock can be used
    #frame_num is used to print the frame#
    def frame_timing(self,imageInterval,starttime,frame_num):
        self.gps.update()

        time_since_last_frame = 0
        if self.gps.has_fix:
            while time_since_last_frame < int(imageInterval):
                self.gps.update()
                if not self.gps.has_fix:
                    time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))
                    print("CLOCK",frame_num)
                    break
                self.wait_for_edge_gps(7,self.gps)
                time_since_last_frame += 1
                print("GPS:",frame_num)
        else:
            time.sleep(int(imageInterval) - ((time.time() - starttime) % int(imageInterval)))#ticks every 1 second
            print("CLOCK",frame_num)

    #gets the gps data to save
    def data(self):
        if self.gps.has_fix:
            Lat = str(self.gps.latitude)
            Long = str(self.gps.longitude)
            Height = str(self.gps.altitude_m)
            TIME = gps.timestamp_utc
            TIME = TIME[:-3]
            Time = "-".join([str(i) for i in TIME])
            return(Lat,Long,Height,Time)
        else:
            return("NaN","NaN","NaN","NaN")

    #saves gps data with frame information        
    def save_data(self,frame_num):
        self.gps.update()
        GPS_data = self.data()
        GPS_data = GPS_data+tuple([str(frame_num)])
        file = open(self.output_dir+"/GPS_DATA.csv",'a')
        write = csv.writer(file)
        write.writerow(GPS_data)
        file.close()


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
    def __init__(self,serial_numbs=["58","72","73"],file_endings=["440nm","550nm","671nm"], gain=[0,0,0], exposure_time=[25000,25000,25000]):
        self.serial_numbs = serial_numbs;self.gain = gain;self.exposure_time=exposure_time;self.file_endings=file_endings
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
            for i in range(len(self.cams)):
                for j in range(len(self.serial_numbs)):
                    if self.serial_numbs[j] == self.CamNames[i][-2:]:
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

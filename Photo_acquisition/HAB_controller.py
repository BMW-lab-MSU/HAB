from datetime import datetime
import RPi.GPIO as GPIO
import time
import csv

#without this sleep an error is thrown about not having access to the GPIO pins
#which is also done at start up
time.sleep(30)
#if the current time is this much greater than the previous then the settings will be redone
redo_settings_time = 1800 #seconds

#sets GPIO of button and LEDs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
GPIO.output(38,GPIO.LOW)
GPIO.output(40,GPIO.LOW)

#similar to the waitfor edge in HAB_functions, except it also flashes an LED
def wait_for_edge(pin, LED):
    while True:
        time.sleep(0.25)
        GPIO.output(LED,GPIO.LOW)
        if GPIO.input(pin):
            GPIO.output(LED,GPIO.HIGH)
            break
        time.sleep(0.25)
        GPIO.output(LED,GPIO.HIGH)
        if GPIO.input(pin):
            break

DATE = datetime.utcnow()
#checks to see if the current setting of the camera are within time
try:
    settings_file = open('Camera_settings.csv','r')
    settings = csv.reader(settings_file,delimiter = ',')
    current_settings = False
    for line in settings:
        file_date = datetime.fromisoformat(line[0])
        break
    print("File_date",str(file_date))
    print("delta_time",abs((file_date-DATE).total_seconds()))
    if abs((file_date-DATE).total_seconds())<redo_settings_time:
        current_settings = True
    settings_file.close()
except:
    current_settings = False

#changes settings if more time has past
if not current_settings:
    print("press button to start getting camera settings:")
    wait_for_edge(31,38)
    
    exec(open("ExposureAndGain.py").read())
    GPIO.output(38,GPIO.LOW)
    time.sleep(1)
    print("press button to start capturing pictures")
    wait_for_edge(31,40)
    
GPIO.cleanup()
#starts taking pitcures
exec(open("ContAcquisition.py").read())

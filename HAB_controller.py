from datetime import date
import RPi.GPIO as GPIO
import time
import csv

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
GPIO.output(38,GPIO.LOW)
GPIO.output(40,GPIO.LOW)

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

DATE = str(date.today())
try:
    settings_file = open('Camera_settings.csv','r')
    settings = csv.reader(settings_file,delimiter = ',')
    current_settings = False
    for line in settings:
        if DATE == line[0]:
            current_settings = True
    settings_file.close()
except:
    current_settings = False
if not current_settings:
    print("press button to start getting camera settings:")
    wait_for_edge(31,38)
    
    exec(open("ExposureAndGain.py").read())
    GPIO.output(38,GPIO.LOW)
    time.sleep(1)
    print("press button to start capturing pictures")
    wait_for_edge(31,40)
    
GPIO.cleanup()
exec(open("ContAcquisition.py").read())

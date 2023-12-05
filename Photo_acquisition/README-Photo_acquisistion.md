# HAB README
Last updated Jul 17 2023

The files are as follows:

***MAKE SURE TO CHANGE THE GPIO PERMISSIONS OF THE PI OR RUN THE PROGRAM AS ROOT***

***MAKE SURE TO DOWNLOAD THE CAMERA PYTHON PACKAGE FROM THE FLIR WEBSITE***

## Photo_aquisition

### HAB_controller.py

1. Checks to see if the camera settings exists

2. If not it waits for a button input (white LED flashes) else it skips to step 6
	
3. It will reset the auto gain and exposure settings by running ExposureAndGain.py (steady yellow)
	
4. This will run until the button is pressed again, averaging the auto exposure and gain.
	
5. Indicates the frame aquisition is ready by blue LED flashing
	
6. runs contAcquisition.py

7. When the button is pressed again it stops contAcquisition.py and moves the camera settings file to the flight that was just complete
	
In our current set up this has a systemd file that causes the file to be run on startup

### contAcquisition.py

- Takes and saves a picture a second along with saving gps data
	
- uses the pps of the gps for timing if availible (this tends to be slower than the onboard clock of the pi)

### HAB_classes.py

- Contains the classes used in contAcquisition.py. The GPS class and the CAMERAS class
	
### ExposureAndGain.py

- Averages the auto gain and exposure while running and saves it in the Camera_settigns.csv for use in contAcquisition.py
	
### Camera_settings.csv

- Holds the camera settings, and is overridden by ExposureAndGain.py
	

## Other notes:

- There is a possibility that your GPS will have a different divice address use the comand "dmesg | grep tty" and there will not be many options

- There is a python environment set up for the pi as of Aug 24 2023 it is a text file that shows you what to install and what version of python to install. You should be able to do pip install HAB_pi.txt but it is untested

- With the patch antenna on the gps it appears like it looses a signal when cameras are pluged in but this does not appear to be the case when an external antenna is used. 


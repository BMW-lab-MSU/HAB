# HAB README
Last updated Jun 14 2023
The files are as follows:
MAKE SURE TO CHANGE THE GPIO PERMISSIONS OF THE PI OR RUN THE PROGRAM AS ROOT

HAB_controller.py-
	1)Checks to see if the camera settings file is older than 30 min 
	2)If so it waits for a button input (yellow LED flashes)
	3)It will reset the auto gain and exposure settings by running ExposureAndGain.py (steady yellow)
	4)This will run until the button is pressed again, then it goes to the next step
	5)Indicates the frame aquisition is ready by blue LED flashing
	6)runs contAcquisition.py
In our current set up this has a systemd file that causes the file to be run on startup

HAB_functions.py-
	Contains the functions used in contAcquisition.py
	The functions are also used elsewhere, but there are also independent functions in other scripts because it is inefficeint to load the entire script when it is not needed

contAcquisition.py-
	Takes and saves a picture a second along with saving gps data
	uses the pps of the gps for timing if availible

ExposureAndGain.py-
	Averages the auto gain and exposure while running and saves it in the Camera_settigns.csv for use in contAcquisition.py
	
ImgView.py-
	Changes all numpy arrays in a directory to png for easy viewing (makes a new dir for the pngs)

ManAcquisition.py-
	Takes 5 images a piece when enter is pressed, used for calibration purposes

Camera_settings.csv-
	Holds the camera settings, and is overridden by ExposureAndGain.py

README.md-
	Describes the set up

Other notes:
There is a possibility that your GPS will have a different divice address use the comand "dmesg | grep tty" and there will not be many options

There is no python environment set up so good luck

With the patch antenna on the gps it appears like it looses a signal when cameras are pluged in but this does not appear to be the case when an external camera is used. 


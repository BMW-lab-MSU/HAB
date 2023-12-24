# HAB README
Last updated Dec 05 2023

The folders are as follows:


## Photo_aquisition

Contains the scripts that the pi runs to take photos, and a readme describing how to use it and things to look out for.

## Data_processing
	
### ImgView.py

- Changes all numpy arrays in a directory to png for easy viewing (makes a new dir for the pngs)

- Make a .mp4 to watch the photos

### GPS_to_map.py

- Puts the GPS data on an interactible map
	

## Calibration

### ManAcquisition.py

- Takes 5 images a piece when enter is pressed, used for calibration purposes

### npy_to_mat.py

- Converts the numpy calibration files to what Erica has

### polarization_cal.py

- Automates the polarization calibration and will send me a text when done

### pol_controler.py

- contains class that controles the polarization rotation stage

### Rad_cal.py

- similar to ManAcquisition.py except changed to have same file structure as polarization_cal.py and to allow for the current of the integrating sphere to be input into the file name

	





Each .h5 file has the following quantities:
'440nm_AoP'
'440nm_DoLP'
'440nm_S0'
'440nm_S1'
'440nm_S2'
'550nm_AoP'
'550nm_DoLP'
'550nm_S0'
'550nm_S1'
'550nm_S2'
'660nm_AoP'
'660nm_DoLP'
'660nm_S0'
'660nm_S1'
'660nm_S2'
'Drone_alt'
'Drone_lat'
'Drone_lon'
'Pixel_bearing'
'Pixel_view'
'Pixel_lat'
'Pixel_lon'
'Sin_Az' - this is a typo and will be fixed for the final data set, but I caught it as the data was uploading, its sun azmuth angle
'Sun_alt' -sun altitude angle
'UTC'

AoP is the angle of polarization, DoLP is the degree of linear polarization, S0,S1, and S2 are the linear stokes parameters. The angles are shown in the attatched pdf

The data is separated by day, and flight. 
Things of note:
In July we did not start the drone as far back into the shore, and so the first collection site is not in as many images. 
For the 2023-08-14/16-29 flight a wire was loose and potentially obscured some of the images. However, on inspection the obstruction was not found.
2023-08-16 was smokey and as such the light was more diffuse than what is ideal.

site_location.csv holds the cite location for each of the days

The script Radius_sorter.py is still in development, but right now it returns how many frames are within a given radius of the site locations.

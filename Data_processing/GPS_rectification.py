#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:31:32 2023

@author: flint
"""
import pandas as pd
import numpy as np
import math
from pysolar.solar import get_azimuth,get_altitude
import datetime as dt
import os
import Processing_functions as PF

def GPS_pixelwise(lat,lon,bearing,h,viewing_ang=45,pixel_width = 1224,pixel_hight = 1024, delta_pix_ang = 0.0153655):
    Bearing_angle_change = (np.arange(pixel_width)*delta_pix_ang)
    viewing_angle_change = (np.arange(pixel_hight)*delta_pix_ang)
    bottom_left_pix = 


def GPS_correction(CurGPS,NxtGPS,Altitude,lakeAlt = 882.0):
    CurGPS_np = np.array(CurGPS)
    Magnitude= Altitude-lakeAlt
    
    lat1 = math.radians(CurGPS[0])
    lat2 = math.radians(NxtGPS[0])
    diffLong = math.radians(NxtGPS[1] - CurGPS[1])
    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)* math.cos(lat2) * math.cos(diffLong))
    initial_bearing = math.atan2(x, y)
    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    cb = np.deg2rad(compass_bearing)
    unit_vec = np.array([np.cos(cb),np.sin(cb)])
    vec = unit_vec*Magnitude
    vec /=  111111.0
    vec[1] /= np.cos(np.deg2rad(NxtGPS[0]))
    point = vec+CurGPS_np

    return(point[0],point[1],compass_bearing)
    
    


def Image_loc_aund_ang(directory,h=1000, GPS_direction=165,tol = 10):
    df = pd.read_csv(directory+"GPS_DATA.csv")
    
    LakeSurfaceAltitude_m = 882
    Lat_pic = []
    Lon_pic = []
    Bearing = []
    for i in range(len(df["Frame"])-1):
        CurGPS = [df["Latitude"][i],df["Longitude"][i]]
    
        DroneAltitude_m = df["Altitude[m]"][i]
        
        NxtGPS = [df["Latitude"][i+1],df["Longitude"][i+1]]
        
        [lat,lon, direction] = GPS_correction(CurGPS, NxtGPS, DroneAltitude_m)
        Lat_pic.append(lat)
        Lon_pic.append(lon)
        Bearing.append(direction)
    
    Lat_pic.append("")
    Lon_pic.append("")
    Bearing.append(Bearing[-1])
    
    df["Image_Latitude"] = Lat_pic
    df["Image_Longitude"] = Lon_pic
    df["Bearing"] = Bearing
    
    
        
    
    date = []
    for time in df["UTC"]:
        if type(0.0) != type(time):
            TIME = [int(i) for i in time.split("-")]
            date.append(dt.datetime(TIME[0],TIME[1],TIME[2],TIME[3],TIME[4],TIME[5],tzinfo=dt.timezone.utc))
        else: date.append(date[-1])
    azimuth = []
    altitude = []
    for i in range(len(date)):
        altitude.append(get_altitude(df["Latitude"][i],df["Longitude"][i],date[i]))
        azimuth.append(get_azimuth(df["Latitude"][i],df["Longitude"][i],date[i]))
        
    df["Sun_Altitude"] = altitude
    df["Sun_Azimuth"] = azimuth
    
    cond = (((df["Altitude[m]"].shift()>h) & ((GPS_direction-tol)<=df["Bearing"].shift()) & (df["Bearing"].shift()<=(GPS_direction+tol)))&(df["Bearing"] != 180.0))
    df_trunk = df[(((df["Altitude[m]"]>h) & (((GPS_direction-tol)<=df["Bearing"]) & (df["Bearing"]<=(GPS_direction+tol))|(cond)) & (df["Bearing"] != 180.0)))]
    df_trunk.to_csv(directory+"GPS_DATA_USEABLE.csv")
    
    To_get_rid = df["Frame"][(((df["Altitude[m]"]<h) | (((GPS_direction-tol)>=df["Bearing"]) | (df["Bearing"]>=(GPS_direction+tol)))) & (~ cond))]
    PF.Remove_frames(directory, To_get_rid)

months = ["/mnt/2TB/HAB/Flathead-July-2023/","/mnt/2TB/HAB/Flathead-Aug-2023/"]
for month in months:
    for day in os.listdir(month):
        day_dir = month+day
        for time in os.listdir(day_dir):
            if not ".csv" in time:
                time_dir = day_dir+"/"+time+"/"
                print(time_dir)
                Image_loc_aund_ang(time_dir)
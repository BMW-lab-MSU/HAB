#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:31:32 2023

@author: flint
"""
import pandas as pd
import numpy as np
import math

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
    print(initial_bearing,compass_bearing)
    cb = np.deg2rad(compass_bearing)
    unit_vec = np.array([np.cos(cb),np.sin(cb)])
    vec = unit_vec*Magnitude
    vec /=  111111.0
    vec[1] /= np.cos(np.deg2rad(NxtGPS[0]))
    point = vec+CurGPS_np

    return(point)
    
    

directory = "/home/flint/Downloads/"
df = pd.read_csv(directory+"GPS_DATA.csv")

LakeSurfaceAltitude_m = 882
Frame = df.values[0,4]

CurLat = df.values[Frame-1,0]
CurLon = df.values[Frame-1,1]
DroneAltitude_m = df.values[Frame-1,2]

NxtLat = df.values[Frame,0]
NxtLon = df.values[Frame,1]
NxtDroneAltitude_m = df.values[Frame,2]

v = GPS_correction([np.float128(CurLat),np.float128(CurLon)], [np.float128(NxtLat),np.float128(NxtLon)],DroneAltitude_m)
print(v)
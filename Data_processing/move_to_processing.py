#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:19:10 2023

@author: Flint Morgan
"""
import pandas as pd
#import Processing_functions as PF
from pysolar.solar import *

import datetime as dt
import numpy as np
directory = "/mnt/data/HAB/Flathead-July-2023/2023-07-26/Flight_1/"
df = pd.read_csv(directory+"GPS_DATA.csv")

def frames_above_height(DIR,h):
    df = pd.read_csv(DIR+"GPS_DATA.csv")

    frames_int = df["Frame"][df["Altitude[m]"]>h]
    frames = []
    for frame in frames_int:
        frames.append("F"+str(frame).zfill(5))
    return(frames)

"""
frames = frames_above_height(directory, 950)
for frame in frames:
    PF.false_color(directory, frame)
"""
date = []
for time in df["UTC"]:
    TIME = [int(i) for i in time.split("-")]
    date.append(dt.datetime(TIME[0],TIME[1],TIME[2],TIME[3],TIME[4],TIME[5],tzinfo=dt.timezone.utc))

azimuth = []
altitude = []
for i in range(len(date)):
    
    altitude.append(get_altitude(df["Latitude"][i],df["Longitude"][i],date[i]))
    azimuth.append(get_azimuth(df["Latitude"][i],df["Longitude"][i],date[i]))
    
df["Sun_Altitude"] = altitude
df["Sun_Azimuth"] = azimuth
print(df)

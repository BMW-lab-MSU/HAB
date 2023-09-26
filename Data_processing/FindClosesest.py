#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 17:56:29 2023

@author: flint
"""
import Processing_functions as PF
import os
import pandas as pd
import numpy as np
#lon then lat
mv_loc = "/mnt/2TB/HAB/site_locations/"
collection_sites= np.array([[-114.032577194112,47.8756916988456],[-114.031543701051,47.8735539519776],[-114.030510289423,47.8714161969059]])

def closest(directory,add_to):
    df = pd.read_csv(directory+"GPS_DATA_USEABLE.csv")
    save_dir = mv_loc+add_to
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    closest_frame = [0,0,0]
    for j in range(len(collection_sites)):
        min_dist = 100
        for i in range(len(df["Frame"])):
            
            CurGPS = np.array([df["Image_Longitude"][i],df["Image_Latitude"][i]])
            dist = np.linalg.norm(collection_sites[j]- CurGPS)
            if dist < min_dist:
                min_dist = dist
                closest_frame[j] = "F"+str(int(df["Frame"][i])).zfill(5)
    print(closest_frame)
    for frame in closest_frame:
        #PF.false_color_DoLP(directory,frame,add_to)
        os.system("cp "+directory+"22027758-Calibrated/"+frame+"* "+save_dir )
        os.system("cp "+directory+"22027772-Calibrated/"+frame+"* "+save_dir )
        os.system("cp "+directory+"22027773-Calibrated/"+frame+"* "+save_dir )
        
        


months = ["/mnt/2TB/HAB/Flathead-July-2023/","/mnt/2TB/HAB/Flathead-Aug-2023/"]

for month in months:
    for day in os.listdir(month):
        day_dir = month+day
        for time in os.listdir(day_dir):
            if not ".csv" in time:
                time_dir = day_dir+"/"+time+"/"
                print(time_dir)
                closest(time_dir,day+"/"+time+"/")
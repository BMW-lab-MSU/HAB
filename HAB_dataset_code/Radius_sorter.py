#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:34:12 2023

@author: flint
"""

import h5py
import numpy as np
import pandas as pd
import geopy.distance
import os
import multiprocessing as MP

def distance(lat1,lon1,lat2,lon2):
    GPS1 = [lat1,lon1]
    GPS2 = [lat2,lon2]
    return(geopy.distance.great_circle(GPS1, GPS2).m)

vdistance = np.vectorize(distance)

def Site_finder(DIR):
    sites = [0,0,0]
    for frame in os.listdir(DIR):
        if ".h5" in frame:
            f = h5py.File(DIR+frame,"r")       
            #horizontal_middle = int(f["Pixel_lat"][()].shape[1]/2)
            Plat = f["Pixel_lat"][()][::12,::12]
            Plon = f["Pixel_lon"][()][::12,::12]
            
            for i in range(len(df["Site_lat"])):
                dist = vdistance(Plat,Plon,df["Site_lat"][i],df["Site_lon"][i])
                if np.min(dist) <= radius:
                    sites[i] +=1
                    break
    print(sites)
    return(sites)
    

radius = 0.1
Month = "/mnt/2TB/HAB/HAB_Dataset/"
df = pd.read_csv("site_location.csv")
DIRs = [x[0]+"/" for x in os.walk(Month) if x[0].count("/") == os.getcwd().count("/")+2]
total = np.array([0,0,0])

with MP.Pool(MP.cpu_count()) as p:
    total = p.map(Site_finder,DIRs)
"""
for DIR in DIRs:
    temp = np.array(Site_finder(DIR,10))
    total = total + temp
"""
print("Totals:")
print(np.sum(total,0))
print(np.sum(total))
print(np.sum(total) * 190/1024)
    
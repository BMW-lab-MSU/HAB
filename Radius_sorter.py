#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:34:12 2023

@author: flint
"""
import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd
import geopy.distance
import os
import multiprocessing as MP
import pandas as pd


radius = 10


CA_1m_h5_Aug = h5py.File("CA_1m_aug.h5","r")
CA_1m_h5_july = h5py.File("CA_1m_july.h5","r")
df = pd.read_csv("Chl_sites.csv")
Chl_Aug = df[df["Depth"] == 1]["Chl"]
Chl_Aug = Chl_Aug.to_numpy()
wv = CA_1m_h5_Aug["Wavelength[nm]"][()]

CA_440_Aug = [CA_1m_h5_Aug["Station_1"][()][wv ==439.3][0],CA_1m_h5_Aug["Station_2"][()][wv ==439.3][0]]
CA_550_Aug = [CA_1m_h5_Aug["Station_1"][()][wv ==549.7][0],CA_1m_h5_Aug["Station_2"][()][wv ==549.7][0]]
CA_660_Aug = [CA_1m_h5_Aug["Station_1"][()][wv ==661.1][0],CA_1m_h5_Aug["Station_2"][()][wv ==661.1][0]]

CA_440_july = [CA_1m_h5_july["Station_1"][()][wv ==439.3][0],CA_1m_h5_july["Station_2"][()][wv ==439.3][0],CA_1m_h5_july["Station_3"][()][wv ==439.3][0]]
CA_550_july = [CA_1m_h5_july["Station_1"][()][wv ==549.7][0],CA_1m_h5_july["Station_2"][()][wv ==549.7][0],CA_1m_h5_july["Station_3"][()][wv ==549.7][0]]
CA_660_july = [CA_1m_h5_july["Station_1"][()][wv ==661.1][0],CA_1m_h5_july["Station_2"][()][wv ==661.1][0],CA_1m_h5_july["Station_3"][()][wv ==661.1][0]]

df = pd.read_csv("site_location.csv")

def distance(lat1,lon1,lat2,lon2,radius):
    GPS1 = [lat1,lon1]
    GPS2 = [lat2,lon2]
    return(geopy.distance.great_circle(GPS1, GPS2).m <= radius)

vdistance = np.vectorize(distance)

def pixel_return(frame):
    f = h5py.File(frame,"r")       
    #horizontal_middle = int(f["Pixel_lat"][()].shape[1]/2)
    Plat = f["Pixel_lat"][()][:]
    Plon = f["Pixel_lon"][()][:]
    for i in sites:
        dist = vdistance(Plat,Plon,df["Site_lat"][i],df["Site_lon"][i],radius)
        if np.max(dist):
            temp = []
            for key in keys:
                
                if "nm" in key or "Pixel" in key:
                    temp.append(f[key][()][dist])
                else:
                    temp2 = f[key][()]
                    temp.append(np.resize(temp2, len(dist[dist])))
            temp.append(i*np.ones(len(temp[0]))) 
            x = np.vstack(temp).T              
            return(x)
            break

def Site_finder(DIR):
    global keys  
    global sites
    if "8" in DIR:
        sites = range(2)
    else:
        sites = range(3)
    
    
    frames = [x for x in os.listdir(DIR) if ".h5" in x]
    frames = [DIR+frame for frame in frames]
    f = h5py.File(frames[0],"r") 
    keys = [key for key in f.keys() if key not in ['Drone_alt', 'Drone_lat', 'Drone_lon','Pixel_lon', 'Pixel_lat', 'UTC']]
    cols = keys+["Site"]
    cols = [x.replace("440nm","Blue").replace("550nm","Green").replace("660nm","Red") for x in cols]
    
    with MP.Pool(MP.cpu_count()-2) as p:
        x_ = p.map(pixel_return,frames)         
    X = [x for x in x_ if np.size(x) >2 ]
    X = pd.DataFrame(np.vstack(X),columns=cols)
    Y = X["Site"]
    X = X.drop(labels = ["Site"],axis = 1)
    
    
    C_over_A_440 = [CA_440_july[int(x)] for x in Y]
    C_over_A_550 = [CA_550_july[int(x)] for x in Y]
    C_over_A_660 = [CA_660_july[int(x)] for x in Y]
    
    if "8" in DIR:
        Chl = [Chl_Aug[int(x)] for x in Y]
        return(X,C_over_A_440,C_over_A_550,C_over_A_660,Chl)
    else:
        return(X,C_over_A_440,C_over_A_550,C_over_A_660)
    

    





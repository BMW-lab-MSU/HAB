#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:42:52 2023

@author: flint morgan
"""
import pandas as pd
import numpy as np
import math
from pysolar.solar import get_azimuth,get_altitude
import datetime as dt
import os
import glob
import h5py

def viewing_pixelwise(bearing,viewing_ang=45,pixel_width = 1224,pixel_hight = 1024, delta_pix_ang = 0.0153655):
    Bearing_angle_change = (np.arange(pixel_width)*delta_pix_ang)
    viewing_angle_change = (np.arange(pixel_hight)*delta_pix_ang)
    #bottom left starts at [-1,0] [vertical, horizontal] the vertical is flipped
    bottom_left_pix_viewing =  [bearing-(((pixel_width/2)-0.5)*delta_pix_ang),viewing_ang -(((pixel_hight/2)-0.5)*delta_pix_ang)]
    Bearing = np.tile((Bearing_angle_change+bottom_left_pix_viewing[0]),(pixel_hight,1))
    Viewing = viewing_angle_change+bottom_left_pix_viewing[1]
    
    
    VIEW = np.zeros([pixel_hight,pixel_width])
    for v in range(len(Viewing)):VIEW[v,:] = Viewing[v]
    
    #return(np.dstack((Bearing,VIEW)))
    return(Bearing,VIEW)
    #return({Bearing:"Bearing",VIEW:"View"})
B,V = viewing_pixelwise(165)

def GPS_correction(CurGPS,NxtGPS,Altitude,lakeAlt = 882.0):
    CurGPS_np = np.array(CurGPS)
    NxtGPS_np = np.array(NxtGPS)
    Height = np.array(Altitude)[0]-lakeAlt
    
    
    lat1 = math.radians(CurGPS[0])
    lat2 = math.radians(NxtGPS[0])
    diffLong = math.radians(NxtGPS_np[1][0] - CurGPS_np[1][0])
    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)* math.cos(lat2) * math.cos(diffLong))
    initial_bearing = math.atan2(x, y)
    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    Pixel_bearing, Pixel_viewing = viewing_pixelwise(compass_bearing)
    PB = np.deg2rad(Pixel_bearing)
    unit_vecs = np.array([np.cos(PB),np.sin(PB)])
    PV = np.deg2rad(Pixel_viewing)
    Magnitude= Height/np.tan(PV)
    Pixel_vec = unit_vecs*Magnitude
    Pixel_vec /=  111111.0
    Pixel_vec[1] /= np.cos(np.deg2rad(NxtGPS_np[0]))
    Pixel_point = [Pixel_vec[0]+CurGPS_np[0],Pixel_vec[1]+CurGPS_np[1]]

    return(Pixel_point[0],Pixel_point[1],Pixel_bearing,Pixel_viewing)
    
    


def Viewing_and_gps(directory, Frame):
    df = pd.read_csv(directory+"GPS_DATA.csv")

    i= df.index[df["Frame"]==Frame]
    CurGPS = [df["Latitude"][i],df["Longitude"][i]]

    DroneAltitude_m = df["Altitude[m]"][i]
    
    NxtGPS = [df["Latitude"][i+1],df["Longitude"][i+1]]
    
    lat,lon, Pix_bearing, Pix_view = GPS_correction(CurGPS, NxtGPS, DroneAltitude_m)
    return(lat,lon,Pix_bearing,Pix_view)


def Camera_pol(directory, camera, Frame):
    file_name = glob.glob(directory+camera+"-Calibrated/F00"+str(Frame)+"*")[0]
    data = np.load(file_name)
    AoP =0.5*np.arctan2(data["S2"],data["S1"])* 180/np.pi
    
    return(data["S0"],data["S1"],data["S2"],data["DoLP"],AoP)
        
        
def to_h5(Time_DIR,save_dir):
    df = pd.read_csv(Time_DIR+"GPS_DATA_USEABLE.csv")
    for frame in df["Frame"]:
        i= df.index[df["Frame"]==frame]
        Frame_name = save_dir+str(i[0]+1).zfill(4)+".h5"
        hf = h5py.File(Frame_name,"a")
        
        
        lat,lon,Pix_bearing,Pix_view = Viewing_and_gps(Time_DIR, frame)
        hf.create_dataset("Pixel_lat",data=lat)
        hf.create_dataset("Pixel_lon",data=lon)
        hf.create_dataset("Pixel_bearing",data=Pix_bearing)
        hf.create_dataset("Pixel_view",data=Pix_view)
        
        Sun_alt = df["Sun_Altitude"][i]
        hf.create_dataset("Sun_alt",data=Sun_alt)
        Sun_Azm = df["Sun_Azimuth"][i]
        hf.create_dataset("Sin_Az",data=Sun_Azm)
        
        Drone_lat = df["Latitude"][i]
        hf.create_dataset("Drone_lat",data=Drone_lat)
        Drone_lon = df["Longitude"][i]
        hf.create_dataset("Drone_lon",data=Drone_lon)
        Drone_alt = df["Altitude[m]"][i]
        hf.create_dataset("Drone_alt",data=Drone_alt)
        Time = np.array(df["UTC"][i])
        hf.create_dataset("UTC",data=Time[0])
        
        Blue_S0, Blue_S1, Blue_S2, Blue_DoLP, Blue_AoP = Camera_pol(Time_DIR,"22027758",frame)
        hf.create_dataset("440nm_S0",data=Blue_S0)
        hf.create_dataset("440nm_S1",data=Blue_S1)
        hf.create_dataset("440nm_S2",data=Blue_S2)
        hf.create_dataset("440nm_DoLP",data=Blue_DoLP)
        hf.create_dataset("440nm_AoP",data=Blue_AoP)
        Green_S0, Green_S1, Green_S2, Green_DoLP, Green_AoP = Camera_pol(Time_DIR,"22027772",frame)
        hf.create_dataset("550nm_S0",data=Green_S0)
        hf.create_dataset("550nm_S1",data=Green_S1)
        hf.create_dataset("550nm_S2",data=Green_S2)
        hf.create_dataset("550nm_DoLP",data=Green_DoLP)
        hf.create_dataset("550nm_AoP",data=Green_AoP)
        Red_S0, Red_S1, Red_S2, Red_DoLP, Red_AoP = Camera_pol(Time_DIR,"22027773",frame)
        hf.create_dataset("660nm_S0",data=Red_S0)
        hf.create_dataset("660nm_S1",data=Red_S1)
        hf.create_dataset("660nm_S2",data=Red_S2)
        hf.create_dataset("660nm_DoLP",data=Red_DoLP)
        hf.create_dataset("660nm_AoP",data=Red_AoP)
        
        
        
        
        hf.close()
        
    


months = ["/mnt/2TB/HAB/Flathead-July-2023/","/mnt/2TB/HAB/Flathead-Aug-2023/"]
for month in months:
    for day in os.listdir(month):
        day_dir = month+day
        for time in os.listdir(day_dir):
            if not ".csv" in time:
                time_dir = day_dir+"/"+time+"/"
                print(time_dir)
                save_dir = "/mnt/2TB/HAB/HAB_Dataset/"+day+"/"+time+"/"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                print(save_dir)
                to_h5(time_dir,save_dir)


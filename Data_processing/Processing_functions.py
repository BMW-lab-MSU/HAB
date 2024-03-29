#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 16:05:03 2023

@author: Flint Morgan
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import scipy.io


def raw_to_stokes_vec(raw):
    I90 = raw.astype(float)[::2,::2]
    I45 = raw.astype(float)[::2,1::2]
    I0  = raw.astype(float)[1::2,1::2]
    I135= raw.astype(float)[1::2,::2]
    #print("raw:",np.min(raw),np.max(raw))
    S0 = 0.5*(I90+I45+I0+I135)
    #print("S0:",np.min(S0),np.max(S0))
    S1 = I0 - I90
    #print("S1:",np.min(S1),np.max(S1))
    S2 = I45 - I135
    return(S0, S1, S2)

def raw_to_stokes_mono(raw):
    I90 = raw.astype(float)[::2,::2]
    I45 = raw.astype(float)[::2,1::2]
    I0  = raw.astype(float)[1::2,1::2]
    I135= raw.astype(float)[1::2,::2]
    #print("raw:",np.min(raw),np.max(raw))
    S0 = 0.5*(I90+I45+I0+I135)
    #print("S0:",np.min(S0),np.max(S0))
    S1 = I0 - I90
    #print("S1:",np.min(S1),np.max(S1))
    S2 = I45 - I135
    #print("S2:",np.min(S2),np.max(S2))
    DoLP = np.sqrt((S1**2)+(S2**2))/S0
    #print("DoLP:",np.min(DoLP),np.max(DoLP))
    AoP =0.5*np.arctan2(S2,S1)* 180/np.pi
    #print("AoP:",np.min(AoP),np.max(AoP))
    
    return(I90, I45, I0, I135, S0, S1, S2, DoLP, AoP)


def false_color_DoLP(DIR,frame,add_to):
    cams=["22027758-Calibrated","22027772-Calibrated","22027773-Calibrated"]
    print(DIR)
    for cameras in os.listdir(DIR):
        if cameras in cams:
            for image_file in os.listdir(DIR+"/"+cameras):
                if frame in image_file:
                    plt.figure()
                    
                    image_np = np.load(DIR+"/"+cameras+"/"+image_file)
                    S0, S1, S2, DoLP = [image_np["S0"],image_np["S1"],image_np["S2"],image_np["DoLP"]]
                    
                    plt.subplot(2,2,4)
                    plt.pcolormesh(DoLP,cmap=plt.cm.turbo,vmin=0, vmax=1)
                    plt.gca().invert_yaxis()
                    plt.colorbar()
                    plt.title(image_file[-10:-4].replace("n"," n")+" DoLP Frame:"+str(frame))
                    plt.tight_layout()
                    
                    
                    plt.subplot(2,2,1)
                    plt.pcolormesh(S0,vmin=0, vmax=2*np.mean(S0))
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-10:-4].replace("n"," n")+" S0 Frame:"+str(frame))
                    plt.tight_layout()

                    
                    plt.subplot(2,2,2)
                    plt.pcolormesh(S1,vmin=0, vmax=2*np.mean(S1))
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-10:-4].replace("n"," n")+" S1 Frame:"+str(frame))
                    plt.tight_layout()

                    
                    plt.subplot(2,2,3)
                    plt.pcolormesh(S2,vmin = 2*np.mean(S2), vmax=0)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-10:-4].replace("n"," n")+ " S2 Frame:"+str(frame))
                    plt.tight_layout()
                    plt.suptitle(cameras+"/"+add_to)
                    plt.tight_layout()
                    plt.show()
                        
                        
                        
        
        print("done")

def false_color(DIR,frame):
    cams=["22027758","22027772","22027773"]
    P = [[42.5,-340.0,1049.5,-1161.5],[68.0,-655.5,2472.0,-3293.0],[34.5,-213.5,553.0,-542]]
    print(DIR)
    for cameras in os.listdir(DIR):
        if cameras in cams:
            index = cams.index(cameras)
            p = P[index]
            for image_file in os.listdir(DIR+"/"+cameras):
                if frame in image_file:
                    plt.figure(figsize=(12,5.5))
                    image_np = np.load(DIR+"/"+cameras+"/"+image_file)
                    I90, I45, I0, I135, S0, S1, S2, DoLP, AoP = raw_to_stokes_mono(image_np)
                    
                    plt.subplot(2,3,4)
                    plt.pcolormesh(DoLP,cmap=plt.cm.turbo,vmin=0, vmax=1)
                    plt.gca().invert_yaxis()
                    plt.colorbar()
                    plt.title(image_file[-9:-4].replace("n"," n")+" DoLP Frame:"+str(frame))
                    plt.tight_layout()
                    
                    plt.subplot(2,3,5)
                    plt.pcolormesh(AoP,cmap=plt.cm.hsv,vmin=-90, vmax=90)
                    plt.gca().invert_yaxis()
                    plt.colorbar()
                    plt.title(image_file[-9:-4].replace("n"," n")+" AoP Frame:"+str(frame))
                    plt.tight_layout()
                    
                    plt.subplot(2,3,1)
                    plt.pcolormesh(S0,vmin=0, vmax=2*np.mean(S0))
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4].replace("n"," n")+" S0 Frame:"+str(frame))
                    plt.tight_layout()

                    
                    plt.subplot(2,3,2)
                    plt.pcolormesh(S1,vmin=0, vmax=2*np.mean(S1))
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4].replace("n"," n")+" S1 Frame:"+str(frame))
                    plt.tight_layout()

                    
                    plt.subplot(2,3,3)
                    plt.pcolormesh(S2,vmin = 2*np.mean(S2), vmax=0)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4].replace("n"," n")+ " S2 Frame:"+str(frame))
                    plt.tight_layout()

                    """
                    c_over_a = p[3]*(DoLP**3)+p[2]*(DoLP**2)+p[1]*(DoLP)+p[0]
                    print("c/a:",np.min(c_over_a),np.max(c_over_a))
                    print("mean:",np.mean(c_over_a))
                    plt.subplot(2,3,6)
                    if 2*np.mean(c_over_a)<0:
                        plt.pcolormesh(c_over_a,vmin=2*np.mean(c_over_a),vmax=10)
                    else:
                        plt.pcolormesh(c_over_a,vmax=2*np.mean(c_over_a),vmin=-10)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4].replace("n"," n")+ " c/a Frame:"+str(frame))
                    plt.tight_layout()
                    """
                    plt.show()
                    
                    
                    
    
    print("done")
    

def frames_above_height(DIR,h):
    df = pd.read_csv(DIR+"GPS_DATA.csv")

    frames_int = df["Frame"][df["Altitude[m]"]>h]
    frames = []
    for frame in frames_int:
        frames.append("F"+str(frame).zfill(5))
    return(frames)   


def Remove_frames(DIR,to_remove):
    rmv_frames = []
    for frame in to_remove:
        rmv_frames.append("F"+str(int(frame)).zfill(5))
    for rmv_frame in rmv_frames:
        os.system("rm "+DIR+"22027758/"+rmv_frame+"*")
        os.system("rm "+DIR+"22027772/"+rmv_frame+"*")
        os.system("rm "+DIR+"22027773/"+rmv_frame+"*")
        os.system("rm "+DIR+"22027758-Calibrated/"+rmv_frame+"*")
        os.system("rm "+DIR+"22027772-Calibrated/"+rmv_frame+"*")
        os.system("rm "+DIR+"22027773-Calibrated/"+rmv_frame+"*")
    
      


def GPS_to_map(directory, style = 0,h=1000, GPS_direction=165,tol = 10):
    df = pd.read_csv(directory+"GPS_DATA_New.csv")
    cond = (((df["Altitude[m]"].shift()>h) & ((GPS_direction-tol)<=df["Bearing"].shift()) & (df["Bearing"].shift()<=(GPS_direction+tol)))&(df["Bearing"] != 180.0))
    df_trunk = df[(((df["Altitude[m]"]>h) & (((GPS_direction-tol)<=df["Bearing"]) & (df["Bearing"]<=(GPS_direction+tol))|(cond)) & (df["Bearing"] != 180.0)))]
    types = ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor']
    
    
    
    color_scale = [(0, 'blue'), (1,'orange')]
    
    fig = px.scatter_mapbox(df_trunk, 
                            lat="Latitude", 
                            lon="Longitude", 
                            hover_name="UTC", 
                            hover_data=["UTC", "Frame", "Bearing"],
                            color="Altitude[m]",
                            color_continuous_scale=color_scale,
                            
                            zoom=15, 
                            height=800,
                            width=800)
    #px.scatter_mapbox(lat= [-114.032577194112,-114.031543701051,-114.030510289423],lon=[47.8756916988456,47.8735539519776,47.8714161969059])
    fig.update_layout(mapbox_style=types[style])
    
    fig.show()
    plot(fig)


def Frame_to_Mat(DIR,frame):
    cams=["22027758","22027772","22027773"]
    
    for cameras in os.listdir(DIR):
        if cameras in cams:
            for image_file in os.listdir(DIR+"/"+cameras):
                if frame in image_file:
                    print(DIR+"/"+cameras+"/"+image_file)
                    image_np = np.load(DIR+"/"+cameras+"/"+image_file)
                    print("past")
                    mat_dir = DIR+"/"+image_file[:-4]+".mat"
                    scipy.io.savemat(mat_dir, {"image":image_np})
"""
#440-713
numbs = np.arange(440,721,20)
frames = []
for num in numbs:
    frames.append("F00"+str(num))

for frame in frames:
    print("\nFrame: "+frame)
    false_color("Z:2023-07-24\Flight_1", frame)
#s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027758", frame)
#s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027772", frame)
#DoLP=s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027773", frame)
"""
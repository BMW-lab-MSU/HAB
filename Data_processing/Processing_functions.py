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

def raw_to_stokes_mono(raw):
    I90 = raw.astype(float)[::2,::2]
    I45 = raw.astype(float)[::2,1::2]
    I0  = raw.astype(float)[1::2,1::2]
    I135= raw.astype(float)[1::2,::2]
    print("raw:",np.min(raw),np.max(raw))
    S0 = 0.5*(I90+I45+I0+I135)
    print("S0:",np.min(S0),np.max(S0))
    S1 = I0 - I90
    print("S1:",np.min(S1),np.max(S1))
    S2 = I45 - I135
    print("S2:",np.min(S2),np.max(S2))
    DoLP = np.sqrt((S1**2)+(S2**2))/S0
    print("DoLP:",np.min(DoLP),np.max(DoLP))
    AoP =0.5*np.arctan2(S2,S1)* 180/np.pi
    print("AoP:",np.min(AoP),np.max(AoP))
    
    return(I90, I45, I0, I135, S0, S1, S2, DoLP, AoP)

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
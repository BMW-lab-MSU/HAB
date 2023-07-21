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
    AoP =0.5*np.arctan2(S2,S1)* 180/np.pi
    
    return(I90, I45, I0, I135, S0, S1, S2, DoLP, AoP)

def false_color(DIR,frame):
    cams=["22027758","22027772","22027773"]
    
    for cameras in os.listdir(DIR):
        if cameras in cams:
            for image_file in os.listdir(DIR+"/"+cameras):
                if frame in image_file:
                    plt.figure(figsize=(12,5.5))
                    image_np = np.load(DIR+"/"+cameras+"/"+image_file)
                    I90, I45, I0, I135, S0, S1, S2, DoLP, AoP = raw_to_stokes_mono(image_np)
                    
                    plt.subplot(2,3,4)
                    plt.pcolor(DoLP,cmap=plt.cm.turbo,vmin=0, vmax=1)
                    plt.gca().invert_yaxis()
                    plt.colorbar()
                    plt.title(image_file[-9:-4].replace("n"," n")+" DoLP Frame:"+str(frame))
                    plt.tight_layout()
                    
                    plt.subplot(2,3,5)
                    plt.pcolor(AoP,cmap=plt.cm.hsv,vmin=-90, vmax=90)
                    plt.gca().invert_yaxis()
                    plt.colorbar()
                    plt.title(image_file[-9:-4].replace("n"," n")+" AoP Frame:"+str(frame))
                    plt.tight_layout()
                    
                    plt.subplot(2,3,1)
                    plt.pcolor(S0,vmin=0, vmax=2*np.mean(S0))
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4].replace("n"," n")+" S0 Frame:"+str(frame))
                    plt.tight_layout()

                    
                    plt.subplot(2,3,2)
                    plt.pcolor(S1,vmin=0, vmax=2*np.mean(S1))
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4].replace("n"," n")+" S1 Frame:"+str(frame))
                    plt.tight_layout()

                    
                    plt.subplot(2,3,3)
                    plt.pcolor(S2,vmin = 2*np.mean(S2), vmax=0)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4]+ " S2 Frame:"+str(frame))
                    plt.tight_layout()
                    plt.show()
                    
    
    print("done")
    

    
#f99 flight 5
#f276 flight 1
frame = "F00005"
false_color("/media/flint/Elements/HAB/2023-07-21/Flight_1", frame)
#s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027758", frame)
#s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027772", frame)
#DoLP=s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027773", frame)
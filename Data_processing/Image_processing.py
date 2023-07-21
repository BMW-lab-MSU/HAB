#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 16:49:06 2023

@author: Flint Morgan
"""
import Processing_functions
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors

def false_color_DoLP(DIR,frame):
    cams=["22027758","22027772","22027773"]
    
    for cameras in os.listdir(DIR):
        if cameras in cams:
            for image_file in os.listdir(DIR+"/"+cameras):
                if frame in image_file:
                    plt.figure()
                    image_np = np.load(DIR+"/"+cameras+"/"+image_file)
                    I90, I45, I0, I135, S0, S1, S2, DoLP, AoP = Processing_functions.raw_to_stokes_mono(image_np)
                    DoLP[np.isnan(DoLP)] =0
                    DoLP[DoLP == np.inf] =1
                    DoLP[DoLP >= 1] = 1
                    plt.pcolor(DoLP,cmap=plt.cm.RdBu)
                    plt.colorbar()
                    
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4]+" DoLP Frame:"+str(frame))
                    plt.tight_layout()
                    plt.show()
                    
                    plt.figure()
                    plt.pcolor(S0,cmap=plt.cm.RdBu)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4]+" S0 Frame:"+str(frame))
                    plt.tight_layout()
                    plt.show()
                    
                    plt.figure()
                    plt.pcolor(S1,cmap=plt.cm.RdBu)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4]+" S1 Frame:"+str(frame))
                    plt.tight_layout()
                    plt.show()
                    
                    plt.figure()
                    plt.pcolor(S2,cmap=plt.cm.RdBu)
                    plt.colorbar()
                    plt.gca().invert_yaxis()
                    plt.title(image_file[-9:-4]+ " S2 Frame:"+str(frame))
                    plt.tight_layout()
                    plt.show()
    
    print("done")
    
def s0_s1_s2(Cam_dir,frame):
    plt.figure()
    for image_file in os.listdir(Cam_dir):
        if frame in image_file:
            image_np = np.load(Cam_dir+"/"+image_file)
            I90, I45, I0, I135, S0, S1, S2, DoLP, AoP = Processing_functions.raw_to_stokes_mono(image_np)
            
            plt.figure()
            plt.pcolor(S0)
            plt.gca().invert_yaxis()
            plt.title(image_file[-9:-4]+" S0 Frame:"+str(frame))
            plt.tight_layout()
            plt.show()
            
            plt.figure()
            plt.pcolor(S1)
            plt.gca().invert_yaxis()
            plt.title(image_file[-9:-4]+" S1 Frame:"+str(frame))
            plt.tight_layout()
            plt.show()
            
            plt.figure()
            plt.pcolor(S2)
            plt.gca().invert_yaxis()
            plt.title(image_file[-9:-4]+ " S2 Frame:"+str(frame))
            plt.tight_layout()
            plt.show()
            
            return(DoLP)
    print("done")
    
#f99 flight 5
#f276 flight 1
frame = "F00276"
false_color_DoLP("/media/flint/Elements/HAB/2023-07-19/Flight_1", frame)
#s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027758", frame)
#s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027772", frame)
#DoLP=s0_s1_s2("/media/flint/Elements/HAB/2023-07-19/Flight_1/22027773", frame)

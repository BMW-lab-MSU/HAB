#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 10:18:55 2023

@author: flint
"""
import os
import scipy.io
import Processing_functions as PF
import numpy as np
from multiprocessing import Pool

def Pol_cal_application(Image_dir):
    try:
        Img_split = Image_dir.split("/")
        image_name = Img_split[-1]
        wv = image_name.split("-")[-1][:-4]
        new_dir = "/".join(Img_split[:5])+"-Cal/"+"/".join(Img_split[5:-2])+"/"
        new_dir = new_dir.replace("Flight2","Flight1")
        dirr = os.listdir(new_dir)
        #print(wv,dirr)
        cal_dir = new_dir+[s for s in dirr if wv in s and "Pol_M_INV" in s][0]
        mat = scipy.io.loadmat(cal_dir)
        M_sys_inv = mat["M_sys_inv"]
        
        image_np = np.load(Image_dir)
        S0, S1, S2 = PF.raw_to_stokes_vec(image_np)
        
        
        S0_corr = M_sys_inv[:,:,0,0]*S0+M_sys_inv[:,:,0,1]*S1+M_sys_inv[:,:,0,2]*S2
        S1_corr = M_sys_inv[:,:,1,0]*S0+M_sys_inv[:,:,1,1]*S1+M_sys_inv[:,:,1,2]*S2
        S2_corr = M_sys_inv[:,:,2,0]*S0+M_sys_inv[:,:,2,1]*S1+M_sys_inv[:,:,2,2]*S2
        DoLP_corr = np.sqrt((S1_corr**2)+(S2_corr**2))/S0_corr
        
        out_dir = "/".join(Image_dir.split("/")[:-1])+"-Calibrated/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        save_dir = out_dir+Image_dir.split("/")[-1][:-4]+"-Calibrated-stokes.npz"
        
        np.savez(save_dir,S0 = S0_corr,S1 = S1_corr,S2 = S2_corr,DoLP = DoLP_corr)
    except:
        print("Not saved:"+Image_dir)
        pass


def Rad_cal_app(Image_dir):
    try:
        Img_split = Image_dir.split("/")
        image_name = Img_split[-1]
        wv = image_name.split("-")[-1][:-4]
        new_dir = "/".join(Img_split[:5])+"-Cal/"+"/".join(Img_split[5:-2])+"/"
        new_dir = new_dir.replace("Flight2","Flight1")
        dirr = os.listdir(new_dir)
        #print(wv,dirr)
        cal_dir = new_dir+[s for s in dirr if wv in s and "Pol_M_INV" in s][0]
        mat = scipy.io.loadmat(cal_dir)
        M_sys_inv = mat["M_sys_inv"]
        
        image_np = np.load(Image_dir)
        S0, S1, S2 = PF.raw_to_stokes_vec(image_np)
        
        S0_corr = M_sys_inv[:,:,0,0]*S0+M_sys_inv[:,:,0,1]*S1+M_sys_inv[:,:,0,2]*S2
        S1_corr = M_sys_inv[:,:,1,0]*S0+M_sys_inv[:,:,1,1]*S1+M_sys_inv[:,:,1,2]*S2
        S2_corr = M_sys_inv[:,:,2,0]*S0+M_sys_inv[:,:,2,1]*S1+M_sys_inv[:,:,2,2]*S2
        DoLP_corr = np.sqrt((S1_corr**2)+(S2_corr**2))/S0_corr
        
        out_dir = "/".join(Image_dir.split("/")[:-1])+"-Calibrated/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        save_dir = out_dir+Image_dir.split("/")[-1][:-4]+"-Calibrated-stokes.npz"
        
        np.savez(save_dir,S0 = S0_corr,S1 = S1_corr,S2 = S2_corr,DoLP = DoLP_corr)
    except:
        print("Not saved:"+Image_dir)
        pass


image_list= ["/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/10-58/22027772/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/10-58/22027773/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/11-16/22027758/","/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/11-16/22027772/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/11-16/22027773/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/16-29/22027758/","/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/16-29/22027772/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/16-29/22027773/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/16-40/22027758/","/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/16-40/22027772/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-14/16-40/22027773/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-16/10-42/22027758/","/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-16/10-42/22027772/",
             "/mnt/2TB/HAB/Flathead-Aug-2023/2023-08-16/10-42/22027773/",]

"""
for Image in image_list:
    print(Image)
    Images = [Image+x for x in os.listdir(Image)]
    
    
    with Pool(6) as p:
        p.map(Pol_cal_application,Images)
"""

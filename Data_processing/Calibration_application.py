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
import time

def rad_app(img, eq):
    m = eq[:,:,0]
    m[m==0]= m.mean()
    b = eq[:,:,1]
    corrected = (img-b)/m
    return(corrected)

def get_avg_dark(DIR):
    dark = np.zeros([2048,2448])
    for image_file in os.listdir(DIR):
        if "dark" in image_file.lower():
            image_np = np.load(DIR+"/"+image_file)
            dark = dark+image_np/5
    return(dark)

def Pol_cal_application(Image_dir):
    try:
        Img_split = Image_dir.split("/")
        image_name = Img_split[-1]
        wv = image_name.split("-")[-1][:-4]
        new_dir = "/".join(Img_split[:5])+"-Cal/"+"/".join(Img_split[5:-2])+"/"
        new_dir = new_dir.replace("Flight2","Flight1")
        dirr = os.listdir(new_dir)
        #print(wv,dirr)
        Pol_cal_dir = new_dir+[s for s in dirr if wv in s and "Pol_M_INV" in s][0]
        Rad_cal_dir = new_dir+[s for s in dirr if wv in s and "-RAD.npy" in s][0]
        Dark_dir = new_dir+[s for s in dirr if wv in s and not "." in s][0]
        
        dark = get_avg_dark(Dark_dir)
        rad_eq = np.load(Rad_cal_dir)
        mat = scipy.io.loadmat(Pol_cal_dir)
        M_sys_inv = mat["M_sys_inv"]
        
        image_np = np.load(Image_dir)
        image_np = image_np - dark
        image_np = rad_app(image_np,rad_eq)
        S0, S1, S2 = PF.raw_to_stokes_vec(image_np)
        
        
        S0_corr = M_sys_inv[:,:,0,0]*S0+M_sys_inv[:,:,0,1]*S1+M_sys_inv[:,:,0,2]*S2
        S1_corr = M_sys_inv[:,:,1,0]*S0+M_sys_inv[:,:,1,1]*S1+M_sys_inv[:,:,1,2]*S2
        S2_corr = M_sys_inv[:,:,2,0]*S0+M_sys_inv[:,:,2,1]*S1+M_sys_inv[:,:,2,2]*S2
        
        out_dir = "/".join(Image_dir.split("/")[:-1])+"-Calibrated/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        save_dir = out_dir+Image_dir.split("/")[-1][:-4]+"-Calibrated-stokes.npz"
        
        np.savez(save_dir,S0 = S0_corr,S1 = S1_corr,S2 = S2_corr)
    except:
        print("Not saved:"+Image_dir)
        pass

"""
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
"""

Month = "/mnt/2TB/HAB/Flathead-July-2023/"

image_list = [x[0] for x in os.walk(Month) if "220277" in x[0] and not "Calibrated" in x[0]]
start = time.time()

for Image in image_list:
    print(Image)
    Images = [Image+"/"+x for x in os.listdir(Image)]
    """
    for img in Images:
        Pol_cal_application(img)
    """
    with Pool(10) as p:
        p.map(Pol_cal_application,Images)
    

end = time.time()

print(end-start)
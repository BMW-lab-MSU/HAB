#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:48:03 2023

@author: flint
"""
import numpy as np
import os
from scipy import stats
import multiprocessing as MP
import time

def get_current_scale(camera,det_cur=6.3207e-4): 
    #these are chosen beecaues they are the 3db points of the filters
    if int(camera) == 22027758:
        lower = 436
        upper = 445
    elif int(camera) == 22027772:
        lower = 545
        upper = 553
    elif int(camera) == 22027773:
        lower = 657
        upper = 666
    else:
        print("INVALID OPTION")
        return()
    
    calFile = "/home/flint/Desktop/HAB/calibration/calibration_file.csv"
    cal = np.loadtxt(calFile,delimiter=",")
    cal[:,0] = cal[:,0]*1000
    cal[:,1] = cal[:,1]/1000
    cal = cal[:][lower<=cal[:,0]]
    cal = cal[:][upper>=cal[:,0]]
    int_rad = np.trapz(cal[:,0],cal[:,1])
    cur_scl = int_rad/det_cur
    return(cur_scl)



def rad_eq(photos,lum):
    equations = np.zeros((np.shape(photos[0])[0],np.shape(photos[0])[1],2))
    for row_idx in range(len(photos[0])):
        for col_idx in range(len(photos[0,0])):
            y = photos[:,row_idx,col_idx]
            slope, intercept, r_value, p_value, std_err = stats.linregress(lum,y)
            equations[row_idx,col_idx]=[slope,intercept]
    return(equations)



def rad_app(img, eq):
    corrected = np.zeros(np.shape(img))
    for row_idx in range(len(img)):
        for col_idx in range(len(img[0])):
            y = img[row_idx,col_idx]
            m,b = eq[row_idx,col_idx]
            corrected[row_idx,col_idx]=(y-b)/m
    return(corrected)


def get_avg_dark(DIR):

    dark = np.zeros([2048,2448])
    for image_file in os.listdir(DIR):
        if "dark" in image_file.lower():
            image_np = np.load(DIR+"/"+image_file)
            dark = dark+image_np/5
    return(dark)
    
    

def rad_cal(DIR):
    camera_name = DIR.split("/")[-1][6:14]
    dark = get_avg_dark(DIR)
    #photos = np.empty([2048,2448,len(deg_pol)])
    to_remove="nPolCalGETIimgDegr_Rdut"
    numb_pol = 0
    currents = []
    for image_file in os.listdir(DIR):
        if "radcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            #print(info)
            image_np = np.load(DIR+"/"+image_file)
            if not info[1] in currents and not np.mean(image_np.astype(float))>60000:
                currents.append(info[1])

    currents.sort()
    photos = np.zeros([len(currents),2048,2448])
    
    for image_file in os.listdir(DIR):
        if "radcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            #print(info)
            image_np = np.load(DIR+"/"+image_file)
            image_np = image_np-dark
            
            if info[1] in currents:
                idx = currents.index(info[1])
            
                if not np.mean(image_np.astype(float))>60000:
                    photos[idx] = photos[idx]+(image_np/5)
                else:
                    photos=np.delete(photos,idx)
                    currents.pop(idx)
                    print("didnt work")

    #plt.scatter(currents, img_avg)
    CURRENTS = (np.array(currents)*1E-6)
    
    lum = CURRENTS*get_current_scale(camera_name)
    equation = rad_eq(photos, lum)
    np.save(DIR+"-RAD.npy",equation)

start = time.time()


Month = "/mnt/data/HAB/Flathead-Aug-2023-Cal/"

DIRs = [x[0] for x in os.walk(Month) if "nm" in x[0]]
with MP.Pool(MP.cpu_count()-2) as p:
    p.map(rad_cal,DIRs)

"""
DIR = DIRs[0]
for folder in os.listdir(DIRs):
    rad_cal(folder)
"""
end = time.time()

print(end-start)
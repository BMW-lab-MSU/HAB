#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:48:03 2023

@author: flint
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm





def rad_cal_check(DIR):
    print(DIR)
    plt.figure()
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
    print(currents)
    img_avg = np.zeros(len(currents))
    photos = np.zeros([2048,2448,len(currents)])
    
    for image_file in os.listdir(DIR):
        if "radcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            #print(info)
            image_np = np.load(DIR+"/"+image_file)
            
            if info[1] in currents:
                idx = currents.index(info[1])
            
                if not np.mean(image_np.astype(float))>60000:
                    img_avg[idx] = img_avg[idx]+np.mean(image_np.astype(float))/5
                    photos[idx] = photos[idx]+(image_np/5)
                else:
                    img_avg= np.delete(img_avg,idx)
                    photos=np.delete(photos,idx)
                    currents.pop(idx)
                    print("didnt work")

    #plt.scatter(currents, img_avg)
    x = (np.array(currents)*1E-6)
    y=img_avg
    coef = np.polyfit(x,y,1)
    poly1d_fn = np.poly1d(coef) 
    # poly1d_fn is now a function which takes in x and returns an estimate for y
    corr_matrix = np.corrcoef(img_avg, poly1d_fn(x))
    corr = corr_matrix[0,1]
    R_sq = corr**2
    plt.plot(x,y, 'yo', x, poly1d_fn(x), '--k')
    plt.title(str(R_sq))
    plt.show()
    
    print("r^2:",R_sq)
    return(R_sq)


DIR = "/mnt/data/HAB/Flathead-Aug-2023-Cal/2023-08-16/10-42/"
R_sq = []
for folder in os.listdir(DIR):
    if not "." in folder:
        R_sq.append(rad_cal_check(DIR+folder))
print(min(R_sq))
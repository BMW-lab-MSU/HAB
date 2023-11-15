#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:07:36 2023

@author: flint
"""
import numpy as np
from sklearn.linear_model import LinearRegression as LR
from scipy import stats

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


x = [1,2,3]
temp = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])

temp2 = temp*15
temp3 = temp*29

print(np.shape(np.array([temp,temp2,temp3])))
equations = (rad_eq(np.array([temp,temp2,temp3]),x))

print(np.shape(equations))
print(rad_app(temp, equations))

def get_current_scale(camera,det_cur=6.3207e-4):
    
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

print(get_current_scale(22027758))
print(get_current_scale(22027772))
print(get_current_scale(22027773))


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
    m = eq[:,:,0]
    m[m==0]= m.mean()
    b = eq[:,:,1]
    corrected = (img-b)/m
    return(corrected)


x = [1,2,3]
temp = np.array([[0,2,3,4],[5,6,7,8],[9,10,11,12]])

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


from multiprocessing import Process

def f(name,a):
    print('hello', name,a)


p = Process(target=f, args=('bob',10))
p.start()
p.join()

from math import sin, cos, sqrt, atan2, radians

# Approximate radius of earth in km
R = 6373.0

lat1 = radians(47.8759184875073)
lon1 = radians(-114.03288242073337)
lat2 = radians(47.875858218942696)
lon2 = radians(-114.03277982624206)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result: ", distance)
print("Should be: ", 10.01 ,"m")

import geopy.distance

coords_1 = (47.8759184875073, -114.03288242073337)
coords_2 = (47.875858218942696, -114.03277982624206)

print(geopy.distance.great_circle(coords_1, coords_2).m)

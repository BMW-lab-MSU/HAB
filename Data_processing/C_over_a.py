#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 13:29:54 2023

@author: flint
"""
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

dict = {"Time/Frame":[],"Color":[],"c/a avg":[]}
df = pd.DataFrame(dict)
def c_over_a(DIR):
    global df
    cams=["440","550","660"]
    P = [[41.0,-296.0,808.0,-783.0],[69.0,-602.0,2037.0,-2407.0],[34.0,-184.0,414.0,-350.0]]
    for time in os.listdir(DIR):
        for Image in os.listdir(DIR+"/"+time):
            if cams[0] in Image:
                index = 0
            elif cams[1] in Image:
                index = 1
            elif cams[2] in Image:
                index = 2
    
            p = P[index]
    
            image_npz = np.load(DIR+"/"+time+"/"+Image)
            DoLP = image_npz["DoLP"]
            c_over_a = p[3]*(DoLP**3)+p[2]*(DoLP**2)+p[1]*(DoLP)+p[0]
            c_over_a[c_over_a < 0] = np.nan
            to_save = DIR+"/"+time+"/"+Image.split("-")[0]
            to_save = to_save.replace("/mnt/2TB/HAB/site_locations/2023-","")
            df.loc[len(df.index)] = [to_save,cams[index], np.nanmean(c_over_a)] 
            if 2<np.nanmean(c_over_a)<7:
                plt.figure()
                plt.pcolormesh(c_over_a,cmap=plt.cm.turbo,vmin=2, vmax=10)
                plt.gca().invert_yaxis()
                plt.colorbar()
                plt.title(to_save+": "+cams[index]+" nm (average value = " + str(np.round(np.nanmean(c_over_a),2))+")")
                plt.tight_layout()

                    
                    
months = ["/mnt/2TB/HAB/site_locations/"]
for month in months:
    for day in os.listdir(month):
        day_dir = month+day
        if "8" in day:
            c_over_a(day_dir)

print(df.sort_values("Time/Frame"))
print(np.average(df["c/a avg"]))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:50:22 2024

@author: flint
"""
import Radius_sorter as RS
import pandas as pd
import numpy as np
import os


Month = "/mnt/2TB/HAB/HAB_Dataset/"

DIRs_aug = [x[0]+"/" for x in os.walk(Month) if x[0].count("/") == os.getcwd().count("/")+2 and "8" in x[0]]
DIRs_july = [x[0]+"/" for x in os.walk(Month) if x[0].count("/") == os.getcwd().count("/")+2 and not "8" in x[0]]
for day in DIRs_july:
    save = day[len(Month):-1].replace("/","-")
    print(save)
    save_dir = "10m_radius/"+save
    X,C_over_A_440,C_over_A_550,C_over_A_660 = RS.Site_finder(day)
    save_df = X.assign(C_over_A_440 = C_over_A_440,C_over_A_550 = C_over_A_550,C_over_A_660 = C_over_A_660)
    save_df.to_csv(save_dir, index = False)
for day in DIRs_aug:
    save = day[len(Month):-1].replace("/","-")
    print(save)
    save_dir = "10m_radius/"+save
    X,C_over_A_440,C_over_A_550,C_over_A_660,Chl = RS.Site_finder(day)
    save_df = X.assign(C_over_A_440 = C_over_A_440,C_over_A_550 = C_over_A_550,C_over_A_660 = C_over_A_660,Chl = Chl)
    save_df.to_csv(save_dir, index = False)


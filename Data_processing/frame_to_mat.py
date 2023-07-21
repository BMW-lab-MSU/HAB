#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:12:39 2023

@author: flint
"""

import scipy.io
import numpy as np
import os
from multiprocessing import Pool


def false_color_DoLP(DIR,frame):
    cams=["22027758","22027772","22027773"]
    
    for cameras in os.listdir(DIR):
        if cameras in cams:
            for image_file in os.listdir(DIR+"/"+cameras):
                if frame in image_file:
                    print(DIR+"/"+cameras+"/"+image_file)
                    image_np = np.load(DIR+"/"+cameras+"/"+image_file)
                    print("past")
                    mat_dir = DIR+"/"+image_file[:-4]+".mat"
                    scipy.io.savemat(mat_dir, {"image":image_np})
#converts all np images in a folder to mat and creates a dir for them
frame = "F00099"
false_color_DoLP("/media/flint/Elements/HAB/2023-07-19/Flight_5", frame)
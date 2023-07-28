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

from multiprocessing import Pool

directory = "/mnt/data/HAB/Flathead-July-2023/2023-07-25/Flight_2/"

frames = Processing_functions.frames_above_height(directory, 950)
frames = frames[::10]

for frame in frames:
    Processing_functions.false_color(directory,frame)

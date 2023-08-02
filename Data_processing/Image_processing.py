#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 16:49:06 2023

@author: Flint Morgan
"""
import Processing_functions as PF


directory = "/mnt/data/HAB/Flathead-July-2023/2023-07-25/Flight_2/"

frames = PF.frames_above_height(directory, 950)
frames = frames[::20]

for frame in frames:
    PF.false_color(directory,frame)

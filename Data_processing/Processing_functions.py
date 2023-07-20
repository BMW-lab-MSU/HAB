#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 16:05:03 2023

@author: Flint Morgan
"""
import numpy as np

def raw_to_stokes_mono(raw):
    I90 = raw[::2,::2]
    I45 = raw[::2,1::2]
    I0  = raw[1::2,::2]
    I135= raw[1::2,1::2]
    
    S0 = 0.5*(I90+I45+I0+I135)
    S1 = I0 - I90
    S2 = I45 - I135
    
    DoLP = np.sqrt((S1**2)+(S2**2))/S0
    AoP =0.5* np.arctan2(S2,S1)* 180/np.pi
    
    return(I90, I45, I0, I135, S0, S1, S2, DoLP, AoP)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:12:39 2023

@author: flint
"""

import Processing_functions as PF



frame = "F00460"
directory = "/mnt/data/HAB/Flathead-July-2023/2023-07-24/Flight_1"
PF.Frame_to_Mat(directory, frame)
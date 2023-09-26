#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:33:19 2023

@author: flint
"""

import numpy as np
import pyOSOAA
from pyOSOAA.osoaahelpers import RunWavelengths
import matplotlib.pyplot as plt

s = pyOSOAA.OSOAA()
view = 0
wavelengths = np.array([440,550,665])/1000
s.view.phi = 40
s.view.vza = 90
s.ang.thetas = 40



# Sea bottom configuration
s.sea.depth = 0.05
s.sea.bottype = 1
s.sea.botalb = 0
# Sea particles configuration
s.phyto.chl = 0
s.sed.csed = 0
s.det.abs440 = 0
s.ys.abs440 = 0
# Sea surface configuration
s.sea.wind = 5

# Configure view level below the surface
s.view.level = 3
rhowg = RunWavelengths(s, wavelengths, view)/np.cos(np.pi*s.ang.thetas/180.0)
# Configure view level below the surface
s.view.level = 4
rhowl = RunWavelengths(s, wavelengths, view)/np.cos(np.pi*s.ang.thetas/180.0)

# Small optical thickness
s.ap.SetMot(0.0005)
s.aer.aotref = 0.00001
# View level
s.view.level = 4
rhog = RunWavelengths(s, wavelengths, view)/np.cos(np.pi*s.ang.thetas/180.0)


# Small optical thickness
s.ap.SetPressure(1013.25)
# Set view level at TOA
s.view.level = 1
rhor = RunWavelengths(s, wavelengths, view)/np.cos(np.pi*s.ang.thetas/180.0)

print("wavelengths:",wavelengths*1e3)
print("rhowg:",rhowg)
print("rhowl:",rhowl)
print("rhog:",rhog)
print("rhor:",rhor)



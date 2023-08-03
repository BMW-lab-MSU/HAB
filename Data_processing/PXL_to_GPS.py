"""
Created on Wed Jul 27 9:40:30 2023

Move to Processing_functions When Done

@author: Wyatt Weller
"""
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
# intersection function
def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=1e-6):
    """
    p0, p1: Define the line.
    p_co, p_no: define the plane:
        p_co Is a point on the plane (plane coordinate).
        p_no Is a normal vector defining the plane direction;
             (does not need to be normalized).

    Return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        # The factor of the point between p0 -> p1 (0 - 1)
        # if 'fac' is between (0 - 1) the point intersects with the segment.
        # Otherwise:
        #  < 0.0: behind p0.
        #  > 1.0: infront of p1.
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(p_no, w) / dot
        u = mul_v3_fl(u, fac)
        return add_v3v3(p0, u)

    # The segment is parallel to plane.
    return None

# ----------------------
# generic math functions

def add_v3v3(v0, v1):
    return (
        v0[0] + v1[0],
        v0[1] + v1[1],
        v0[2] + v1[2],
    )


def sub_v3v3(v0, v1):
    return (
        v0[0] - v1[0],
        v0[1] - v1[1],
        v0[2] - v1[2],
    )


def dot_v3v3(v0, v1):
    return (
        (v0[0] * v1[0]) +
        (v0[1] * v1[1]) +
        (v0[2] * v1[2])
    )


def len_squared_v3(v0):
    return dot_v3v3(v0, v0)


def mul_v3_fl(v0, f):
    return (
        v0[0] * f,
        v0[1] * f,
        v0[2] * f,
    )

def PXL_to_GPS(CurGPS, NxtGPS):
    CurGPS[2] = CurGPS[2] * 1/(111111) #Convert Altitude from m to degrees
    NxtGPS[2] = NxtGPS[2] * 1/(111111)
    
    YCoord = NxtGPS[0] - CurGPS[0]
    XCoord = NxtGPS[1] - CurGPS[1]
    
    ro = 1
    phi = np.pi/4
    theta = np.sin(YCoord) * np.arccos((XCoord)/(np.sqrt((XCoord)**2 + (YCoord)**2)))#np.arctan((NxtGPS[0] - CurGPS[0]) / (NxtGPS[1] - CurGPS[1]))
    print(180*theta/np.pi)
    
    y = CurGPS[1] + ro * np.sin(phi) * np.cos(theta)
    x = CurGPS[0] + ro * np.sin(phi) * np.sin(theta)
            
    z = CurGPS[2] - ro * np.cos(phi)
    
    print([x,y,z])
    
    v = isect_line_plane_v3(CurGPS, [x,y,z], [0,0,0], [0,0,1])
    print(v)
    return None

directory = "C:/Users/wyatt/OneDrive/Documents/GitHub/HAB/Data_processing/"
df = pd.read_csv(directory+"GPS_DATA.csv")

LakeSurfaceAltitude_m = 882
Frame = df.values[0,4]

CurLat = df.values[Frame-1,0]
CurLon = df.values[Frame-1,1]
DroneAltitude_m = df.values[Frame-1,2]

NxtLat = df.values[Frame,0]
NxtLon = df.values[Frame,1]
NxtDroneAltitude_m = df.values[Frame,2]

PXL_to_GPS([CurLat,CurLon,DroneAltitude_m - LakeSurfaceAltitude_m], [NxtLat,NxtLon,NxtDroneAltitude_m - LakeSurfaceAltitude_m])
# The altitude of the Next GPS Coordinate doesn't affect calculation for current
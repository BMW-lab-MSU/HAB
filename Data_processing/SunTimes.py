#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:23:06 2023

@author: flint
"""



    
    
from pysolar.solar import get_azimuth,get_altitude
import datetime as dt

def time_of_sun_ang(altitude,GPS,day):
    epsilon = 9999
    i=0
    while True:
        i+=1
        date = day+dt.timedelta(minutes=i)
        alt = get_altitude(GPS[0],GPS[1],date)
        if abs(alt-altitude)<epsilon:
            epsilon = abs(alt-altitude)
            Time = date-dt.timedelta(hours=6)
        elif alt>0:
            break
    return(Time,alt)

print(time_of_sun_ang(90-30,[47.87619429062692, -114.03204548226243],dt.datetime(2023,8,16,12,tzinfo=dt.timezone.utc)))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:19:19 2023

@author: Flint Morgan
"""
import serial
from time import sleep

class rot_stage:
    #waits for the roation to stop
    def Wait_for_stop(self):
        moving = "0"
        while float(moving) != 1:
            self.port.write('1MD?\r\n')#read Motion Done
            sleep(0.5)
            moving = self.port.read()
            sleep(1)
    #init newport rot stage
    def __init__(self,rot_stage_comport):

        self.port= serial.Serial(port = rot_stage_comport,baudrate=19200,bytesize=8,stopbits=1)#settings
        self.port.isOpen()#opens port
        self.port.write('1MO\r\n')#axis 1 Motor On    
        self.port.write('1OR\r\n')#search for home
        self.Wait_for_stop()
        self.port.write('1TB\r\n')#read error
        print(self.port.read())
        self.port.write('1VA30\r\n')#sets velocity of roation stage to 30 deg/s instead of the default 40
        self.port.write('1TP?\r\n')#read actual postion
        self.degree = self.port.read()
    #sets the rotation stage to a degree then waits for it to get there
    def Degree(self,degree):
        self.port.write("1PA"+str(degree)+"\r\n")
        self.Wait_for_stop()

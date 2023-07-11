#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:19:19 2023

@author: Flint Morgan
"""
import serial.tools.list_ports as port_list
import serial
from time import sleep

class rotation_stage:
    #gets the angle and ensures that it is stable for 3 queries
    def get_current_degree(self):
        prev_ang2 = 998
        prev_ang = 999
        while True:
            self.port.write('1TP?\r\n'.encode())
            sleep(0.1)
            angle = self.port.readline().decode()
            try:
                angle = float(angle)
                if prev_ang == angle and prev_ang2 == prev_ang:
                    return(angle)
                else:
                    prev_ang2=prev_ang
                    prev_ang = angle
            except:
                pass
    #waits for the roation to stop
    def Wait_for_stop(self):
        moving = "0"
        while moving != 1:
            self.port.write('1MD?\r\n'.encode())#read Motion Done
            sleep(0.5)
            moving = self.port.readline()
            try:
                moving = float(moving)
            except:
                pass
            sleep(0.5)
            
    #init newport rot stage
    def __init__(self):
        ports = list(port_list.comports())
        for p in ports:
            if "Prolific USB-to-Serial" in str(p):
                rot_stage_comport=p.name

        self.port= serial.Serial(port = rot_stage_comport,baudrate=19200,bytesize=8,stopbits=1)#settings
        self.port.isOpen()#opens port
        self.port.write('1MO\r\n'.encode())#axis 1 Motor On    
        self.port.write('1OR\r\n'.encode())#search for home
        self.Wait_for_stop()
        #self.port.write('1TB\r\n'.encode())#read error
        #print(self.port.read())
        self.port.write('1VA15\r\n'.encode())#sets velocity of roation stage to 30 deg/s instead of the default 40
        self.cur_degree = self.get_current_degree()
    #sets the rotation stage to a degree then waits for it to get there

            
    def Set_Degree(self,degree):
        to_encode = "1PA"+str(degree)+'\r\n'#sets absolute angle
        self.port.write(to_encode.encode())
        self.Wait_for_stop()
        self.cur_degree = self.get_current_degree()
        
    def close(self):
        self.port.close()


    

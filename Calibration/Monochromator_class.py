#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 12:42:51 2023

@author: Flint Morgan
"""

import serial.tools.list_ports as port_list
import serial
from time import sleep
import numpy as np


class monochromator:
    #sets which grating is active, the input must be an int
    def Set_Grating(self, Grating: int):
        to_encode = str(Grating)+" GRATING"
        self.port.write(to_encode.encode())#tells the system to change gratings
        while True:
            self.port.write("?grating")#queries which grating is currently active
            current_grating = self.port.readline()
            if str(Grating) == str(current_grating):
                break
            else:
                sleep(1)
    #gets the wavelength after it has stoped moving for three queries in a row
    def get_current_nm(self):
        prev_nm2 = 0
        prev_nm = 1
        while True:
            self.port.write('?NM'.encode()) #gets current wavelength (has a precision of 1 decimal place ex 250.0)
            sleep(0.1)
            nm = self.port.readline().decode()
            try:
                nm = float(nm)
                if prev_nm == nm and prev_nm2 == prev_nm:
                    return(nm)
                else:
                    prev_nm2=prev_nm
                    prev_nm = nm
            except:
                pass
            
    #init Monochromator 
    def __init__(self,COM_port:str = "COM3", scan_speed:float = 100.0):
        scan_speed = str(np.round(float(scan_speed),1)) # converts scan speed to what is useable for the com port
        ports = list(port_list.comports())
        #finds com port listed
        for p in ports:
            if COM_port in str(p):
                MC_comport=p.name

        self.port= serial.Serial(port = MC_comport,baudrate=9600,bytesize=8,stopbits=1,newline="\r",timeout = 1.0)#settings
        self.port.isOpen()#opens port
        input("Power cycle the monochromator now. Press enter once you see Acton message")# I am not yet convinced this is needed
        
        print("Installed Gratings:")#shows installed gratins
        sleep(0.1)
        self.port.write('?GRATINGS'.encode())#reads gratings
        print(self.port.readlines())
        
        print("\nSelected Turret:")#shows which turret is selected
        sleep(0.1)
        self.port.write("?TURRET".encode())
        print(self.port.readlines())
        
        to_encode = scan_speed+" NM/MIN"
        self.port.write(to_encode.encode())#sets scan speed to 100 mn/min by default, but will set it to whatever scan speed is
        self.Set_Grating(1)# moves grating to position 1
        self.cur_nm = self.get_current_nm()


            
    def Set_wavelength(self,nm):
        nm = str(np.round(float(nm),1))
        to_encode = str(nm)+" <GOTO>"#goes to wavelength (Note the example in the manual has a different sentax ex "250.0 GOTO")
        self.port.write(to_encode.encode())
        self.cur_nm = self.Wait_for_wavelength()
        

    #closes port properly
    def close(self):
        self.port.close()
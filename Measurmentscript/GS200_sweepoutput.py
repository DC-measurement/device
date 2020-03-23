# -*- coding: utf-8 -*-
"""
Created on 2019/09/08
@author: Rui
"""

import Labber
import numpy as np
import time
import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt
# path -----
import sys
from pathlib import Path
p = Path.cwd()
sys.path.append(str(p.parent))
# Instruments you use ------
import Instrumentdriver.GS200 as gs


####################################################
#  IP addresses of instruments
GS200_address = 'TCPIP0::192.168.2.13::inst0::INSTR'

# GS200--- open instance
GS200 = gs.GS200(GS200_address)

# configurate sweeps:
mode= "CURR" #can be "VOLT" or "CURR"
rampflag=0  # 1: do slow ramp between two setpoint; 0: not do
goToinitial=0  # 1：go to initial setpoint after sweep; 0: not back

# set sweep range
Out_start =0E-6
Out_step = 0.001E-6
Out_stop = -0.2E-6
ramp_step= 0.0001E-6   #(protective slow ramp between two major steps)
Out_point = round(abs((Out_stop-Out_start))/Out_step)+1



if goToinitial==1:    # creat sweep back list  
   vOutback=np.linspace(Out_stop, Out_start, Out_point)

####################################################
###### for Labber data structure ######
vOut = np.linspace(Out_start, Out_stop, Out_point)   # this command is not usefull here because we do not save data

#######################################


j=0
for j in tqdm(range(Out_point)):
    
    if rampflag==0:
        level = vOut[j]
        GS200.LevelSet(level, OUTPUT=1, mode=mode)
        time.sleep(0.02)
    else:
        if j==0:
            GS200.LevelSet(vOut[j], OUTPUT=1, mode=mode)
            time.sleep(0.02)
        else:
            #vRamp=np.arange(vCurr[j-1], vCurr[j], ramp_step)
            Ramp_point = round(abs((vOut[j]-vOut[j-1]))/ramp_step)+1
            vRamp = np.linspace(vOut[j-1], vOut[j], Ramp_point)
            #print(vRamp)
            jdx=0
            for jdx in range(len(vRamp)):
                GS200.LevelSet(vRamp[jdx], OUTPUT=1, mode=mode)
                time.sleep(0.02)


    
###########sweep back to initial if need#############    
if goToinitial==1:
   i=0
   for i in tqdm(range(len(vOutback))):
       
       if rampflag==0:
        levelback = vOutback[i]
        GS200.LevelSet(levelback, OUTPUT=1, mode=mode)
        time.sleep(0.02)
       else:
            if i==0:
                GS200.LevelSet(vOutback[i], OUTPUT=1, mode=mode)
                time.sleep(0.02)
            else:
                Ramp_point = round(abs((vOutback[i]-vOutback[i-1]))/ramp_step)+1
                vRamp = np.linspace(vOutback[i-1], vOutback[i], Ramp_point)
                jdx=0
                for jdx in range(len(vRamp)):
                    GS200.LevelSet(vRamp[jdx], OUTPUT=1, mode=mode)
                    time.sleep(0.02)

   
#GS200.LevelSet(0, 0, mode=mode)
#GS200.close()
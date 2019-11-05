# -*- coding: utf-8 -*-
"""
Created on 2019/11/01
@author: Rui Wang
"""

import Labber
import numpy as np
import time
import datetime
import timeit
#from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
# path -----
import sys
from pathlib import Path
p = Path.cwd()
sys.path.append(str(p.parent))
# Instruments you use ------
import Instrumentdriver.GS200 as gs
import Instrumentdriver.Keysight34470 as K34470


####################################################
#  IP addresses of instruments
Tpath="C:\shareRuilaptop"
Tfilename="I__f5000-13000MHz_P0mdB_B0mT_ATT30db-AB30UM-IF50_D4-20-2018_003_Var1_39_Var2_0-22-04-2018-12-05-07_ascii.dat"
Tfiledirect=Tpath+Tfilename


GS200_ip = 'TCPIP0::192.168.2.12::inst0::INSTR'
K34470_ip= 'TCPIP0::192.168.2.31::inst0::INSTR'

# open input and output instance
GS200 = gs.GS200(GS200_ip)
DMM=K34470.Keysight34470(K34470_ip)


################################################

##### configurate out sweeps: (can sweep either V or I) of GS200
outmode= "CURR" #can be "VOLT" or "CURR"
outunit= "A"
rampflag=0  # 1: do slow ramp between two setpoint; 0: not do

##### configurate measurment mode: can be V or I of K34470
inmode="VOLT"
inunit= "V"

### indicate preamplifier gain ###
Gvolt=100.0  # for voltage amplifier NF SA410fs

##### set output setpoint (in this program we do the bipolar measure)#############

Iout=1e-6
####################################################




############ Labber Logger Tags ##################
name = 'RWang'
tag = ['DCmeasuretest']  # list
project = 'IVVI /RwithT'

comment = ''
datetime0 = datetime.datetime.now()
stamp = '{0:%H%M%S}'.format(datetime0)
filename1 = 'IVVI-DoublesweepfromZero' + stamp



fig = plt.figure(figsize=[16,12])
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
#######################################


j=0
Timelist=[]
Tlist=[]
Vmeas=[]
Ibias=[]
Rcal=[]
######## define just script test indicator ###########
idx=20
#####################################################
time0=timeit.default_timer()


#####################################################

while idx>=0:
    deltatime=float(timeit.default_timer()-time0)/60
    Timelist.append(deltatime)
    ######## read temperature datapoint #############
    Trecord = np.array(pd.read_csv(Tfiledirect, delim_whitespace=True,header=None))
    time.sleep(0.02)
    Tdata=Trecord[-1][-1]
    Tlist.append(Tdata)
    
    # output current or volt (bipolar)
    GS200.LevelSet(Iout, OUTPUT=1, mode=outmode)
    time.sleep(0.02)
    Vdata1=float(DMM.measure(mode=inmode))
    time.sleep(0.02)
    GS200.LevelSet(-1*Iout, OUTPUT=1, mode=outmode)
    time.sleep(0.02)
    Vdata2=float(DMM.measure(mode=inmode))
    time.sleep(0.02)
    
    Ibias.append(Iout)
    Vmeas.append((Vdata1-Vdata2)/(2*Gvolt))
    Rcal.append((Vdata1-Vdata2)/(2*Gvolt*Iout))
    
    idx-=1
        
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    
    ax1.set_title('Temp vs. Time')
    ax1.set_xlabel('Time Elapse (min)')
    ax1.set_ylabel('Temperature (K)')
    ax2.set_title('Ibias vs. Time')
    ax2.set_xlabel('Time Elapse (min)')
    ax2.set_ylabel('Ibias (A)')
    ax3.set_title('Vmeas vs. Time')
    ax3.set_xlabel('Time Elapse (min)')
    ax3.set_ylabel('Vmeas (V)')
    ax4.set_title('Rcal vs. Time')
    ax4.set_xlabel('Time Elapse (min)')
    ax4.set_ylabel('Rcal (ohm)')
    
    ax1.plot(np.array(Timelist),np.array(Tlist) , marker='.')
    ax2.plot(np.array(Timelist),np.array(Ibias) , marker='.')
    ax3.plot(np.array(Timelist),np.array(Vmeas), marker='.')
    ax4.plot(np.array(Timelist), np.array(Rcal), marker='.')
    
    plt.pause(0.001)
    
plt.close('all')
#GS200.LevelSet(0, 0, mode=mode)
DMM.close()
GS200.close()


# define step channels
Step = [dict(name='Time Elapse', unit='min', values=Timelist)]
Log1 = [dict(name='Temperature', unit='K', vector=False),
        dict(name='Ibias', unit='A', vector=False),
        dict(name='Vmeas', unit='V', vector=False),
        dict(name='Rcal', unit='ohm', vector=False)]
f1 = Labber.createLogFile_ForData(filename1, Log1, Step)

f1.setUser(name)
f1.setProject(project)
f1.setTags(tag)

#addcomment = comment+', readsource={}dBm, Drivesource={}dBm, fq={}GHz, amp_I_read={}, amp_I_drive={}, Tpi={}ns'.format(LOpowerRead, Qubit_MW_power, (Qubit_MW_freq)/1e9, amp_I, amp_I_drv, Tpi)
f1.setComment(comment)
f1.addEntry({'Temperature': np.array(Tlist), 'Ibias': np.array(Ibias), 
             'Vmeas': np.array(Vmeas), 'Rcal': np.array(Rcal) })


    


   

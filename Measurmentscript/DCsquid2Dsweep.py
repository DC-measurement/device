# -*- coding: utf-8 -*-
"""
Created on 2019/11/01
@author: Rui Wang
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
import Instrumentdriver.Keysight34470 as K34470


####################################################
#  IP addresses of instruments
GS200_ip1 = 'TCPIP0::192.168.2.12::inst0::INSTR'  # I bias 
GS200_ip2 = 'USB0::0x0B21::0x0039::91S200133::0::INSTR'   # I gate(USB) 
K34470_ip= 'TCPIP0::192.168.2.31::inst0::INSTR'

# open input and output instance
GS200bias = gs.GS200(GS200_ip1)
GS200gate = gs.GS200(GS200_ip2)
DMM=K34470.Keysight34470(K34470_ip)

##### configurate out sweeps for bias: (can sweep either V or I) of GS200
outmode= "CURR" #can be "VOLT" or "CURR"
outunit= "A"
rampflag=0  # 1: do slow ramp between two setpoint; 0: not do

##### configurate measurment mode for bias: can be V or I of K34470
inmode="VOLT"
inunit= "V"

### indicate preamplifier gain ###
Gvolt=100.0  # for voltage amplifier NF SA410fs

##### set output sweep range for bias  (always start from zero and comback to zero and save all data)
Out_min_bias =-1E-6
Out_step_bias = 0.1E-6
Out_max_bias = 1E-6
#Out_point = round(abs((Out_stop-Out_start))/Out_step)+1

##### set output sweep range for gate (always start from zero and comback to zero and save all data)
Out_min_gate =-2E-6
Out_step_gate = 0.2E-6
Out_max_gate = 2E-6
Out_point_gate = round(abs((Out_max_gate-Out_min_gate))/Out_step_gate)+1
outmodegate="CURR"
#Out_point = round(abs((Out_stop-Out_start))/Out_step)+1

ramp_step= 0.001E-6   #(protective slow ramp between two major steps for both bias and gate)
####################################################
###### for Labber data structure ######
#make out put list
vOutbias=np.r_[np.arange(0, Out_min_bias, -Out_step_bias), np.arange(Out_min_bias, Out_max_bias, Out_step_bias), 
           np.arange (Out_max_bias, 0, -Out_step_bias)]

vOutgate=np.linspace(Out_min_gate, Out_max_gate, Out_point_gate)

############ Labber Logger Tags ##################
name = 'RWang'
tag = ['DCmeasuretest']  # list
project = 'IVVI /2DSQUID'

comment = ''
datetime0 = datetime.datetime.now()
stamp = '{0:%H%M%S}'.format(datetime0)
filename1 = 'IVVI-DoublesweepfromZero' + stamp

# define step channels
Step = [dict(name='point', unit='', values=vOutbias), dict(name='Igate', unit='A', values=vOutgate)]
Log1 = [dict(name=outmode, unit=outunit, vector=False),
        dict(name=inmode, unit=inunit, vector=False)]
f1 = Labber.createLogFile_ForData(filename1, Log1, Step)

f1.setUser(name)
f1.setProject(project)
f1.setTags(tag)

#addcomment = comment+', readsource={}dBm, Drivesource={}dBm, fq={}GHz, amp_I_read={}, amp_I_drive={}, Tpi={}ns'.format(LOpowerRead, Qubit_MW_power, (Qubit_MW_freq)/1e9, amp_I, amp_I_drv, Tpi)
f1.setComment(comment)

fig = plt.figure(figsize=[12,12])
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
#######################################

i=0
j=0
Vout=[]
Ibias=[]
for i in tqdm(range(len(vOutgate))):
    # output gate current with or w/o slow ramp
    if rampflag==0:
        levelgate = vOutgate[i]
        GS200gate.LevelSet(levelgate, OUTPUT=1, mode=outmodegate)
        time.sleep(0.02)
    else:
        if i==0:
            GS200gate.LevelSet(vOutgate[i], OUTPUT=1, mode=outmodegate)
            time.sleep(0.02)
        else:
            #vRamp=np.arange(vCurr[j-1], vCurr[j], ramp_step)
            Ramp_pointgate = round(abs((vOutgate[i]-vOutgate[i-1]))/ramp_step)+1
            vRampgate = np.linspace(vOutgate[i-1], vOutgate[i], Ramp_pointgate)
            #print(vRamp)
            idx=0
            for idx in range(len(vRampgate)):
                GS200gate.LevelSet(vRampgate[idx], OUTPUT=1, mode=outmodegate)
                time.sleep(0.02)
    
    Vout=[]
    Ibias=[]                
    for j in tqdm(range(len(vOutbias))):
    
        # output current or volt with or w/o slow ramp
        if rampflag==0:
            level = vOutbias[j]
            GS200bias.LevelSet(level, OUTPUT=1, mode=outmode)
            time.sleep(0.02)
        else:
            if j==0:
                GS200bias.LevelSet(vOutbias[j], OUTPUT=1, mode=outmode)
                time.sleep(0.02)
            else:
                #vRamp=np.arange(vCurr[j-1], vCurr[j], ramp_step)
                Ramp_point = round(abs((vOutbias[j]-vOutbias[j-1]))/ramp_step)+1
                vRamp = np.linspace(vOutbias[j-1], vOutbias[j], Ramp_point)
                #print(vRamp)
                jdx=0
                for jdx in range(len(vRamp)):
                    GS200bias.LevelSet(vRamp[jdx], OUTPUT=1, mode=outmode)
                    time.sleep(0.02)
        # volt from amplifier
        Ibias.append(vOutbias[j])
        Meas = float(DMM.measure(mode=inmode))/Gvolt
        Vout.append(Meas)
        time.sleep(0.02)
        
        ax1.cla()
        ax2.cla()
        ax3.cla()
        
        ax1.set_title(outmode+'={}'.format(vOutbias[j])+outunit+',Igate={}'.format(vOutgate[i]))
        ax1.set_xlabel('datapoint')
        ax1.set_ylabel(outmode+'['+outunit+']')
        ax2.set_title(outmode+'={}'.format(vOutbias[j])+outunit+',Igate={}'.format(vOutgate[i]))
        ax2.set_xlabel('datapoint')
        ax2.set_ylabel(inmode+'['+inunit+']')
        ax3.set_title(inmode+ 'vs.'+ outmode+',Igate={}'.format(vOutgate[i]))
        ax3.set_xlabel(outmode+'['+outunit+']')
        ax3.set_ylabel(inmode+'['+inunit+']')
        
        ax1.plot(np.array(Ibias) , marker='.')
        ax2.plot(np.array(Vout), marker='.')
        ax3.plot(np.array(Ibias), np.array(Vout), marker='.')
        
        plt.pause(0.001)
    f1.addEntry({outmode: np.array(Ibias),inmode: np.array(Vout)})

plt.close('all')

   
#GS200.LevelSet(0, 0, mode=mode)
DMM.close()
GS200bias.close()
GS200gate.close()
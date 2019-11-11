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

GS200_ip = 'TCPIP0::192.168.2.12::inst0::INSTR'

K34470_ip= 'TCPIP0::192.168.2.31::inst0::INSTR'



# open input and output instance

GS200 = gs.GS200(GS200_ip)

DMM=K34470.Keysight34470(K34470_ip)



##### configurate out sweeps: (can sweep either V or I) of GS200

outmode= "CURR" #can be "VOLT" or "CURR"

outunit= "A"

rampflag=0  # 1: do slow ramp between two setpoint; 0: not do



##### configurate measurment mode: can be V or I of K34470

inmode="VOLT"

inunit= "V"



### indicate preamplifier gain ###

Gvolt=100.0  # for voltage amplifier NF SA410fs



##### set output sweep range  (always start from zero and comback to zero and save all data)

Out_min =-1E-6

Out_step = 0.1E-6

Out_max = 1E-6

ramp_step= 0.001E-6   #(protective slow ramp between two major steps)

#Out_point = round(abs((Out_stop-Out_start))/Out_step)+1



####################################################

###### for Labber data structure ######

#make out put list

vOut=np.r_[np.arange(0, Out_min, -Out_step), np.arange(Out_min, Out_max, Out_step), 

           np.arange (Out_max, 0, -Out_step)]







############ Labber Logger Tags ##################

name = 'RWang'

tag = ['DCmeasuretest']  # list

project = 'IVVI'



comment = ''

datetime0 = datetime.datetime.now()

stamp = '{0:%H%M%S}'.format(datetime0)

filename1 = 'IVVI-DoublesweepfromZero' + stamp



# define step channels

Step = [dict(name='point', unit='', values=vOut)]

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





j=0

Vout=[]

Ibias=[]

for j in tqdm(range(len(vOut))):



    # output current or volt

    if rampflag==0:

        level = vOut[j]

        GS200.LevelSet(level, OUTPUT=1, mode=outmode)

        time.sleep(0.02)

    else:

        if j==0:

            GS200.LevelSet(vOut[j], OUTPUT=1, mode=outmode)

            time.sleep(0.02)

        else:

            #vRamp=np.arange(vCurr[j-1], vCurr[j], ramp_step)

            Ramp_point = round(abs((vOut[j]-vOut[j-1]))/ramp_step)+1

            vRamp = np.linspace(vOut[j-1], vOut[j], Ramp_point)

            #print(vRamp)

            jdx=0

            for jdx in range(len(vRamp)):

                GS200.LevelSet(vRamp[jdx], OUTPUT=1, mode=outmode)

                time.sleep(0.02)

    # volt from amplifier

    Ibias.append(vOut[j])

    Meas = float(DMM.measure(mode=inmode))/Gvolt

    Vout.append(Meas)

    time.sleep(0.02)

    

    ax1.cla()

    ax2.cla()

    ax3.cla()

    

    ax1.set_title(outmode+'={}'.format(vOut[j])+outunit)

    ax1.set_xlabel('datapoint')

    ax1.set_ylabel(outmode+'['+outunit+']')

    ax2.set_title(outmode+'={}'.format(vOut[j])+outunit)

    ax2.set_xlabel('datapoint')

    ax2.set_ylabel(inmode+'['+inunit+']')

    ax3.set_title(inmode+ 'vs.'+ outmode)

    ax3.set_xlabel(outmode+'['+outunit+']')

    ax3.set_ylabel(inmode+'['+inunit+']')

    

    ax1.plot(np.array(Ibias) , marker='.')

    ax2.plot(np.array(Vout), marker='.')

    ax3.plot(np.array(Ibias), np.array(Vout), marker='.')

    

    plt.pause(0.001)

    

plt.close('all')

f1.addEntry({outmode: np.array(Ibias),inmode: np.array(Vout)})





    





   

#GS200.LevelSet(0, 0, mode=mode)

DMM.close()

GS200.close()
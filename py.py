# -*- coding: utf-8 -*-

"""
Created on Fri Nov  1 14:36:55 2019

@author: steve

"""

import time
import datetime
import timeit
import numpy as np
import pandas as pd


Tpath="C:\\shareRuilaptop"+"\\"

Tfilename="I__f5000-13000MHz_P0mdB_B0mT_ATT30db-AB30UM-IF50_D4-20-2018_003_Var1_39_Var2_0-22-04-2018-12-05-07_ascii.dat"

Tfiledirect=Tpath+Tfilename

idx=20

b=[]

while idx>=0:

    x = np.array(pd.read_csv(Tfiledirect, delim_whitespace=True,header=None))

    a=x[-1][-1]

    b.append(a)

    idx-=1

print("process end!")

#datetime0=datetime.datetime.now()

#timestart=timeit.default_timer()

#time.sleep(100)

#deltatime=timeit.default_timer()-timestart
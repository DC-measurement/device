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


datanow=datetime.date.today().strftime('%y-%m-%d')
Tpath="R:\\"+datanow+"\\"
Tfilename="CH6 T "+datanow+".log"
Tfiledirect=Tpath+Tfilename



idx=20
b=[]
while idx>=0:
    x = np.array(pd.read_csv(Tfiledirect, delim_whitespace=False,header=None))
    a=x[-1][-1]
    b.append(a)
    idx-=1
    
    
print("process end!")




#datetime0=datetime.datetime.now()
#timestart=timeit.default_timer()
#time.sleep(100)
#deltatime=timeit.default_timer()-timestart

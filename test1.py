import visa
import pandas as  pd
import numpy as np
import random
import datetime
import matplotlib.pyplot as plt

rm =visa.ResourceManager()
rm.list_resources()
instr=rm.open_resource('USB0::0x2A8D::0x0201::MY57700883::0::INSTR')


ms_A=[]
ms_V=[]
ms_R=[]

for i in range(10):
    I=float(instr.query("MEAS:CURR:DC? 100 mA"))
    V=float(instr.query("MEAS:VOLT:DC?"))
    R=float(instr.query("MEAS:RES?"))
    ms_A.append(I)
    ms_V.append(V)
    ms_R.append(R)
 
me_time= datetime.datetime.today()
print(me_time)
print("-----------------------------------")
print("電流")
print(ms_A)
print("電圧")
print(ms_V)
print("抵抗")
print(ms_R)

#散布図
x=ms_A
y=ms_V
plt.scatter(x,y)
plt.title("IvsV")
plt.xlabel("I[mA]")
plt.ylabel("V[mV]")
plt.show()



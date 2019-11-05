"""
Created on 2019/10/04
@author : Shu

"""

import visa
import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
import time


#GS200 current set 
def current_set(chassis: str, current: float, output: int):

    """





    Parameters

    ----------

    chassis : str

        'n0' or 'n1'



    current : float

        Unit is [A].



    output : int

        0 = OFF

        1 = ON



    Returns

    -------

    

    """

    if chassis == 'n0':

        GS200_address = 'USB0::0x0B21::0x0039::91S200133::0::INSTR'

    elif chassis == 'n1':

        GS200_address = 'TCPIP0::192.168.2.9::inst0::INSTR'

    

    rm = visa.ResourceManager()

    inst = rm.open_resource(GS200_address)



    if output == 1:

        a = max([math.ceil(abs(current*1320)), 1])

        vol_limit = min([a, 10])



        inst.write(':SOUR:PROT:VOLT {}'.format(vol_limit))



        if abs(current) <= 1e-3:

            inst.write(':SOUR:RANG 1E-3')

        elif abs(current) > 1e-3 and abs(current) <= 10e-3:

            inst.write(':SOUR:RANG 10E-3')

        else:

            inst.write(':SOUR:RANG 100E-3')

        

        inst.write(':SOUR:LEV {}'.format(current))

        time.sleep(0.03)

        inst.write(':OUTP ON')

    else:

        inst.write(':OUTP OFF')

    

    return inst.close()


#measur with digital multimeter 
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

# measurement result and time
print(me_time)
print("-----------------------------------")
print("Current")
print(ms_A)
print("Voltage")
print(ms_V)
print("Resistanse")
print(ms_R)

#Scattter plot
x=ms_A
y=ms_V
plt.scatter(x,y)
plt.title("IvsV")
plt.xlabel("I[mA]")
plt.ylabel("V[mV]")
plt.show()

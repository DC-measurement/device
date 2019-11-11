#%%

# import visa

from mpl_toolkits.mplot3d import Axes3D

import pandas as pd

import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
import time

import matplotlib.pyplot as plt

# x = [1,2,3,4,5,6]
# y = [2,5,4,6,8,7]
# plt.plot(x,y)



import numpy as np
import pandas as pd
from numpy.random import randn
np.random.seed()

import matplotlib.pyplot as plt

#measur with digital multimeter 

# rm =visa.ResourceManager()

# rm.list_resources()

# instr=rm.open_resource('USB0::0x2A8D::0x0201::MY57700883::0::INSTR')


ms_A=[]

ms_V=[]

ms_R=[]

me_time= datetime.datetime.today()



# measurement result and time

# print(me_time)

# print("-----------------------------------")


# for i in range(10):

#     I=float(instr.query("MEAS:CURR:DC? 100 mA"))

#     V=float(instr.query("MEAS:VOLT:DC? 100 mV"))

#     R=float(instr.query("MEAS:RES?"))

for i in range(10):
    
#     ms_A.append(I)
#     ms_V.append(V)
#     ms_R.append(R)
    
    
    ms_A = np.random.randn(1)

    ms_V = np.random.randn(1)

    ms_R = np.random.randn(1)

#     ms_A.append(I)
#     ms_V.append(V)
#     ms_R.append(R)
 

# me_time= datetime.datetime.today()


print(me_time)

m = ['Current', 'Voltage', 'Resistanse']

print(m)

print("-----------------------------------")


for i in range(10):

    x = ms_A

    y = ms_V

    z = ms_R
    
    u = [x, y , z]
    
    print(u)






    
# print("Current")

# print(ms_A)

# print("Voltage")

# print(ms_V)

# print("Resistanse")

# print(ms_R)


#Scattter plot

def func1(ms_A, ms_V):
    return ms_V / ms_A

ms_A = np.arange(-1.0, 1.0, 0.1)
ms_V = np.arange(-1.0, 1.0, 0.1)

X, Y = np.meshgrid(ms_A, ms_V)
Z = func1(X, Y)

fig = plt.figure()
ax = Axes3D(fig)

# plt.title("IvsVvsR")

ax.set_xlabel("current [mA]")
ax.set_ylabel("volt [mV]")
ax.set_zlabel("resistence [Ω]")

ax.plot_wireframe(X, Y, Z)
plt.show()

# tree.insert(write(ms_A), write(ms_V),write(ms_R))

# for i in range(10):
    
#     arrA.append(I)
#     arrV.append(V)
#     arrR.append(R)

# plt.scatter(x,y)

# ms_A=[]

# ms_V=[]

# ms_R=[]


# for i in range(10):
    
#     ms_A.append(I)
#     ms_V.append(V)
#     ms_R.append(R)
    
    
#     ms_A = np.random.randn(10)

#     ms_V = np.random.randn(10)

#     ms_R = np.random.randn(10)
    
dfV = pd.DataFrame(ms_V)

dfV.columns = ['V']

dfA = pd.DataFrame(ms_A)

dfA.columns = ['A']

dfR = pd.DataFrame(ms_R)

dfR.columns = ['R']

df = dfV.join([dfA,dfR])

df


df.describe()


print(df['V'].max())

print(df['V'].idxmax())


plt.figure()

plt.title('random_test')

plt.xlabel('$Current$ [A]')

plt.ylabel('$Voltage$ [V]')

plt.grid()

plt.scatter(df['A'],df['V'] ,label='File : array')

plt.legend()

filename = "output.png"
plt.savefig(filename)

df = pd.DataFrame(index='1 2 3 4 5 6 7 8 9 10'.split(),columns='crr vol res'.split())
# df = pd.DataFrame(print(ms_A,ms_V,ms_R),index='1 2 3 4 5 6 7 8 9 10'.split(),columns='crr vol res'.split())
# df = pd.DataFrame(randn(5,4),['a', 'b', 'c', 'd', 'e'], ['w', 'x', 'y', 'z'])

df[['crr', 'vol','res']]



# plt.xlabel("I[mA]")

# plt.ylabel("V[mV]")

# plt.ylabel("R[Ω]")

# plt.show()

#%%

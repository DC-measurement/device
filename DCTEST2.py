import paho.mqtt.publish as publish
from time import sleep
import visa

ID = "USB0::0x2A8D::0x0201::MY57700883::0::INSTR"
r = visa.ResourceManager()
instr = r.get_instrument(ID)

instr.write("SENSe:VOLTage:DC:RANGe{<range>|MIN|}:mV 0.3")
instr.write("CONF:VOLT:DC 10,0.003")
instr.write("TRIG:COUN 10")
instr.write("TRIG:COUN MIN;:SAMP:COUN MIN")
instr.write("CURR:DC:mA 0.1")
instr.write("OUTPUT:STAT ON")
instr.write(DISP:TEXT "WAITING...")


topicV = "34470A/DC/volt"
topicC = "34470A/DC/current"

print('-----------')

for V in range(10):

    volts = float(instr.query("MEAS:VOLT:DC? "))
    currents = float(instr.query("MEAS:CURR:DC? "))
    print(volts, "V")
    print(currents, "A")
    msg = [{'topic':topicV, 'payload':str(volts)}, ( topicC, str(currents), 0, False)]

    if V == 10:
        break


f = open('DCresult.txt', 'w')

f.write('volts, \n')
f.write('currents \n')

f.close()

print('-----------')



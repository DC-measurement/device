-# -*- coding: utf-8 -*-

"""
20191031
Created:RuiWang
Not full function of keisight34470

"""
import visa
import math
import time
import sys

class Keysight34470():

    #### This class implements the GS200 ####

    def __init__(self, ip, options={}):

        rm = visa.ResourceManager()

        self.inst = rm.open_resource(ip)

    def measure(self, mode="VOLT"): #mode = "CURR", "VOLT", "RES"

        self.inst.write("SENS:{}:DC:RANG:AUTO ON".format(mode)) # select mode and define auto range

        self.inst.write("SENS:{}:NPLC 1".format (mode))

        self.inst.write("MEAS:{}:DC?".format(mode))

        time.sleep(0.02)

        return self.inst.read()

    def close(self):

        self.inst.close()

    def reset(self):

        self.inst.write('*RST')

"""

"""

if __name__ == '__main__':

    ip = 'TCPIP0::192.168.2.31::inst0::INSTR'

    K34470 = Keysight34470(ip)

    K34470.reset()

    time.sleep(0.02)

    MeasV=K34470.measure(mode="VOLT")

    K34470.close()

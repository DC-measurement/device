# -*- coding: utf-8 -*-
"""
Created on 2019/03/04
@author: Sho

Modified: RuiWang 2019/09/09  add mode, reset function, maixaml protection limit
"""

import visa
import math
import time
import sys

class GS200():
    #### This class implements the GS200 ####
    def __init__(self, ip, options={}):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(ip)


    def currentSet(self, current=0, OUTPUT=0):
        """
        Parameters
        current : float, Unit is [A];
        output : int 0 = OFF;1 = ON
        Returns
        -------
        """
        self.inst.write("SOUR:FUNC {}".format("CURR"))
        if OUTPUT == 1:

            vol_limit = 30
            self.inst.write(':SOUR:PROT:VOLT {}'.format(vol_limit))

            if abs(current) <= 1e-3:
                self.inst.write(':SOUR:RANG 1E-3')
            elif abs(current) > 1e-3 and abs(current) <= 10e-3:
                self.inst.write(':SOUR:RANG 10E-3')
            else:
                self.inst.write(':SOUR:RANG 100E-3')
        
            self.inst.write(':SOUR:LEV {}'.format(current))

            time.sleep(0.02)

            self.inst.write(':OUTP ON')
        else:
            self.inst.write(':OUTP OFF')

    def voltageSet(self, voltage=0, OUTPUT=0):
        """
        Parameters
        ----------
        voltage : float Unit is [V]; 
        output : int   0 = OFF;1 = ON
        Returns
        -------
        """
        self.inst.write("SOUR:FUNC {}".format("VOLT"))
        if OUTPUT == 1:
            cur_limit = 200E-3  # set a protective current
            self.inst.write(':SOUR:PROT:CURR {}'.format(cur_limit))
            # output voltage in auto range
            self.inst.write(':SOUR:LEV:AUTO {}'.format(voltage))
            time.sleep(0.02)
            self.inst.write(':OUTP ON')
        else:
            self.inst.write(':OUTP OFF')
    
    def LevelSet(self, level=0, OUTPUT=0, mode="CURR"):  # mode="CURR" or "VOLT"
         """
        Parameters
        ----------
        voltage : float Unit is [V]; current : float, Unit is [A];
        output : int   0 = OFF;1 = ON
        Returns
        -------
        """
         if mode == "VOLT":
             self.inst.write("SOUR:FUNC {}".format("VOLT"))
             cur_limit = 200E-3  # set a protective current
             self.inst.write(':SOUR:PROT:CURR {}'.format(cur_limit))
         else:
             self.inst.write("SOUR:FUNC {}".format("CURR"))
             vol_limit = 30
             self.inst.write(':SOUR:PROT:VOLT {}'.format(vol_limit))

         if OUTPUT == 1:        
              # output level in auto range
              self.inst.write(':SOUR:LEV:AUTO {}'.format(level))
              time.sleep(0.02)
              self.inst.write(':OUTP ON')
         else:
              self.inst.write(':OUTP OFF')  


    def close(self):
        self.inst.close()

    def reset(self):
        self.inst.write('*RST')

"""
    
"""

    
if __name__ == '__main__':
    #ip = 'TCPIP0::192.168.2.12::inst0::INSTR'
    ip='USB0::0x0B21::0x0039::91S200133::0::INSTR'   #GS200 n0
    #ip='USB0::0x0B21::0x0039::91V111744::0::INSTR'
    GS200 = GS200(ip)
    GS200.reset()
    time.sleep(0.02)
    GS200.LevelSet(level=1e-3, OUTPUT=1, mode="VOLT")
    #GS200.voltageSet(voltage=0, OUTPUT=0)
    GS200.close()


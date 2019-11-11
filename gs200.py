# -*- coding: utf-8 -*-

"""
Created on 2018/12/10
@author: Sho

"""
import visa
import math
import time

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

        time.sleep(0.02)

        inst.write(':OUTP ON')

    else:

        inst.write(':OUTP OFF')

    

    return inst.close()
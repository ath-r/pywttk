# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 16:20:45 2023

@author: nicec
"""

import numpy as np

def bandlimit(FFT, last):
    
    for i in range(last + 1, FFT.size - 1):
            FFT[i] = 0
            
    return FFT

def calc(FFT, order = -1):
    for i in range(1, FFT.size):
        x = FFT[i]
        y = (i * 1j * np.pi) ** order
        z = 2
        
        FFT[i] = x * y
        
    return FFT

def rotate(FFT, angle):
    power = angle / (np.pi / 2)
    
    for i in range(1, FFT.size):
        FFT[i] *= 1j ** (power * i)
        
    return FFT

def rotate_phases(FFT, angle):
    power = angle / (np.pi / 2)
    
    FFT *= 1j ** power
    
    return FFT

def set_phases(FFT, phase):
    power = phase / (np.pi / 2)
    
    FFT = np.abs(FFT).astype(np.complex128) * (1j ** power)
    
    return FFT

def shift(FFT, shiftvalue):
    
    shiftint = int(shiftvalue)
    shiftint2 = shiftint + 1
    shiftfrac = shiftvalue - shiftint
    shiftfracreverse = (1 - shiftfrac)
    
    output = np.zeros(FFT.size, dtype = np.complex128)
    output[0] = FFT[0]
    
    for i in range(shiftint, len(output)):
        if ((i % shiftint) == 0):
            output[i] = FFT[int(i / shiftint)] * shiftfracreverse
        if ((i % shiftint2) == 0):
            output[i] += FFT[int(i / shiftint2)] * shiftfrac
            
    return output
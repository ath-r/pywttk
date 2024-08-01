# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:15:45 2023

@author: nicec
"""

import numpy as np

def fft_size(a):
    if type(a) is int:
        return a // 2 + 1
    elif type(a) is np.ndarray:
        return len(a) // 2 + 1

def ifft_size(a):
    if type(a) is int:
        return (a - 1) * 2
    elif type(a) is np.ndarray:
        return (len(a) - 1) * 2

def fft_from_np(data):    
    size = fft_size(data)
    
    FFT = np.copy(np.resize(data, size))
    return FFT

def fft(table):
    size = fft_size(table)
        
    FFT = np.fft.fft(table, table.size)
    
    FFT = fft_from_np(FFT)
    FFT = np.resize(FFT, size)
    return FFT

def ifft(data):
    size = ifft_size(data.size)
    
    IFFT = np.fft.ifft(data, size).astype(np.float64)
    IFFT *= 2 # normalize lack of negative frequencies
    return IFFT

def fft_norm(current_size, new_size):
    return new_size / current_size

def fft_resize(data, new_size):
    if new_size > data.size:
        output = np.hstack([data, np.zeros(new_size - data.size, dtype = np.complex128)])
    else:
        output = np.copy(np.resize(data, new_size))
        
    output *= fft_norm(data.size, new_size)
    
    return output
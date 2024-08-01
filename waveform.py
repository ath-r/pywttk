# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:50:50 2023

@author: nicec
"""
import numpy as np

import wttk.fft as fft
import wttk.freqdomain as fd
import wttk.maths as maths

def saw(size, ifft = True):
    
    fftsize = fft.fft_size(size)
    FFT = np.empty(fftsize, dtype = np.complex128)
    
    for i in range(1, FFT.size):
        FFT[i] = (1 / i  * 1j / np.pi) * size
        
    if (ifft == True):
        return fft.ifft(FFT)
    else:
        return FFT
    
def square(size, ifft = True):
    FFT = saw(size, ifft = False)
    
    for i in range(1, FFT.size):
        if i % 2 == 0:
            FFT[i] = 0
    FFT *= 2
            
    if (ifft == True):
        return fft.ifft(FFT)
    else:
        return FFT

def pulse(size, r = 0.5, norm = True, ifft = True):
    
   fftsize = fft.fft_size(size)
   FFT = np.empty(fftsize, dtype = np.complex128)
    
   if (norm == True):
       FFT[0] = (2 * r - 1) * size * 0.5
   else:
       FFT[0] = 0
    
   for i in range(1, FFT.size):
       slope = 2 / (np.pi * i)
       sin = np.sin(i * r * np.pi)
    
       FFT[i] = (slope * sin) * size
    
   if (ifft == True):
       return fft.ifft(FFT)
   else:
        return FFT
    
def triangle(size, ifft = True):
   FFT = square(size, ifft = False)
   fd.calc(FFT, -1)
   FFT *= 2
    
   if (ifft == True):
       return fft.ifft(FFT)
   else:
        return FFT
    
def parabola(size, ifft = True):
   FFT = square(size, ifft = False)
   fd.calc(FFT, -2)
   FFT *= 8
    
   if (ifft == True):
       return fft.ifft(FFT)
   else:
        return FFT
    
def prime(size, slope = 1, ifft = True):
    
    fftsize = fft.fft_size(size)
    FFT = np.zeros(fftsize, dtype = np.complex128)
    
    indices = maths.primes(FFT.size - 1)
    for i in indices:
        FFT[i] = 1 / (i ** slope) * 1j * size
    
    if (ifft == True):
        return fft.ifft(FFT)
    else:
        return FFT
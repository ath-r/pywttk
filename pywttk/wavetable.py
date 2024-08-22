# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:33:13 2023

@author: nicec
"""

import numpy as np
import pywttk.fft as fft
import pywttk.readwrite as rw
import pywttk.maths as maths

def is_time(data):
    if type(data) is np.ndarray:
        if data.dtype == np.float64:
            return True
    return False

def is_freq(data):
    if type(data) is np.ndarray:
        if data.dtype == np.complex128:
            return True
    return False

def is_wt(wt):
    return type(wt) is Wavetable

class Wavetable:    
    
    def __init__(self, data):
        
        if type(data) is np.ndarray:
            self.set(data)
        
        elif type(data) is Wavetable:
            self.set(data._table_time)
        
        elif type(data) is str:
            self.set(rw.read_wav(data))
        
        elif type(data) is int:
            size = data
            self._table_time = np.zeros(size, dtype = np.float64)
            self._table_freq = np.zeros(fft.fft_size(size), dtype = np.complex128)
        
        else: 
            raise Exception("Wavetable__init__: no size or data supplied.")
        
    def size_time(self):
        return self._table_time.size
    
    def size_freq(self):
        return self._table_freq.size
        
    def set(self, data):
        if is_time(data):
            self._table_time = np.copy(data)
            self._table_freq = fft.fft(data)
            
        elif is_freq(data):
            self._table_freq = np.copy(data)
            self._table_time = fft.ifft(data)
            
        else:
            data_type = data.__class__.__name__
            
            ndarray_type = "";
            if type(data) is np.ndarray:
                ndarray_type = np.typename(data.dtype.char)
            
            raise Exception("""Wavetable.set: Unsupported type of data: {} {}
Use numpy.ndarray of numpy.float64 for time domain data.
Use numpy.ndarray of numpy.complex128 for frequency domain data.""".format(ndarray_type, data_type))
            
    def get_time(self):
        return np.copy(self._table_time)
    
    def get_freq(self):
        return np.copy(self._table_freq)
    
    def get_freq_plot(self, normalize = True, threshold = -100):
        plot = maths.v2db(np.abs(self._table_freq))
        plot[0] = -120
        if normalize: plot -= np.max(plot)
        plot = np.maximum(plot, threshold)
        plot[0] = 0
        return plot
    
##########################################
#Operation wrappers
##########################################
    
def _check(wt):
    if not is_wt(wt):
        raise Exception("Can't perform wavetable operation because wt is not a valid wavetable!")

def _set_or_copy(wt, data, copy = False):
    if copy:
        return Wavetable(data)
    else:
        wt.set(data)
        return wt
    
def wtop(func):
    def inner(*args, **kwargs):
        _check(args[0])
        data = func(*args, **kwargs)
        return _set_or_copy(args[0], data, kwargs.get('copy', False))
    return inner

##########################################
#Frequency domain operations
##########################################

import pywttk.freqdomain as fd

@wtop
def resize(wt, new_size, copy = False):
    data = wt.get_freq()
    return fft.fft_resize(data, fft.fft_size(new_size))

@wtop
def bandlimit(wt, overtones, copy = False):    
    data = wt.get_freq()
    return fd.bandlimit(data, overtones)

@wtop
def calc(wt, order = -1, copy = False):
    data = wt.get_freq()
    return fd.calc(data, order)

@wtop
def rotate(wt, angle, copy = False):
    data = wt.get_freq()
    return fd.rotate(data, angle)

@wtop
def rotate_phases(wt, angle, copy = False):
    data = wt.get_freq()
    return fd.rotate_phases(data, angle)

@wtop
def set_phases(wt, phase = np.pi / 2, copy = False):
    data = wt.get_freq()
    return fd.set_phases(data, phase)

##########################################
#Time domain operations
##########################################

import pywttk.timedomain as td

@wtop
def normalize_amplitude(wt, copy = False):
    data = wt.get_time()
    return td.normalize_amplitude(data)

@wtop
def normalize_dc(wt, copy = False):
    data = wt.get_time()
    return td.normalize_dc(data)

@wtop
def normalize_centered(wt, copy = False):
    data = wt.get_time()
    return td.normalize_centered(data)

@wtop
def normalize_fit(wt, copy = False):
    data = wt.get_time()
    return td.normalize_fit(data)

@wtop
def normalize_dc_fit(wt, copy = False):
    data = wt.get_time()
    return td.normalize_dc_fit(data)

##########################################
#Waveform synthesis
##########################################

import pywttk.waveform as wf

def saw(size = 2048):
    wavetable = Wavetable(wf.saw(size, ifft = False))
    normalize_fit(wavetable)
    return wavetable

def square(size = 2048):
    wavetable = Wavetable(wf.square(size, ifft = False))
    normalize_fit(wavetable)
    return wavetable

def pulse(size = 2048, r = 0.5):
    wavetable = Wavetable(wf.pulse(size, r, ifft = False))
    rotate(wavetable, r * np.pi)
    normalize_fit(wavetable)
    return wavetable

def triangle(size = 2048, r = 0.5):
    wavetable = Wavetable(wf.pulse(size, r, ifft = False))
    calc(wavetable, -1)
    rotate(wavetable, np.pi)
    normalize_fit(wavetable)
    return wavetable

def parabola(size = 2048, r = 0.5):
    wavetable = Wavetable(wf.pulse(size, -r, ifft = False))
    calc(wavetable, -2)
    rotate(wavetable, np.pi / 2)
    normalize_fit(wavetable)
    return wavetable
    
def prime(size = 2048, slope = 1):
    wavetable = Wavetable(wf.prime(size, slope, ifft = False))
    normalize_fit(wavetable)
    return wavetable
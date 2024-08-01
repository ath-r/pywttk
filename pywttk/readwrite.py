# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 22:58:22 2023

@author: nicec
"""

import soundfile as sf
import numpy as np

def read_wav(filename):
    info = sf.info(filename)
    data, samplerate = sf.read(filename)
    #data is dtype = np.float64 by default
    
    if info.format == "WAV":
        if info.subtype == "PCM_U8":
            pass #data /= 2 ** 8
        elif info.subtype == "PCM16":
            pass #data /= 2 ** 15
        elif info.subtype == "PCM_24":
            pass #data /= 2 ** 23
        elif info.subtype == "PCM_32":
            pass #data /= 2 ** 31
        elif info.subtype == "FLOAT":
            pass
        elif info.subtype == "DOUBLE":
            pass
        else:
            raise Exception("readwrite.read_file: can't read subtype {} of format WAV".format(info.subtype))
    elif info.format  == "FLAC":
        if info.subtype == "PCM_S8":
            data /= 2 ** 7
        if info.subtype == "PCM_16":
            data /= 2 ** 15
        if info.subtype == "PCM_24":
            data /= 2 ** 23
    else:
        raise Exception("readwrite.read_file: format {} is not supported.".format(info.format))
            
    return data
        
def write_wav(filename, data, samplerate = 48000):
    if data.dtype == np.float32:
        subtype = "FLOAT"
    elif data.dtype == np.float64:
        subtype = "FLOAT"
    elif data.dtype == np.int32:
        subtype = "PCM_32"
    elif data.dtype == np.int16:
        subtype = "PCM_16"
    sf.write(filename, data, samplerate, subtype)
    
def from_reaktor(filename, dtype = np.float32):
    f = open(filename)
    table = np.array([line.rstrip('\n') for line in f], dtype)
    f.close()
    
    return table

def to_cheader(signature, data, form = "f"):
    
    form = "%" + form + ",\n"
    
    out = signature
    out += '[] = {\n'

    for x in data:
        out += form % x
        
    out = out[:-2]

    out += "\n};"
    
    return out
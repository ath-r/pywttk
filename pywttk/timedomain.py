# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 18:33:41 2023

@author: nicec
"""

import numpy as np

def normalize_amplitude(table):
    divider = np.absolute(table).max()
    
    if divider == 0:
        return table
    else:    
        return table / divider

def normalize_dc(table):
    mean = np.mean(table)
    return [x - mean for x in table]

def normalize_centered(table):
    tmax = np.max(table)
    tmin = np.min(table)
    return [x - (tmax + tmin) / 2 for x in table]

def normalize_fit(table):
    return normalize_amplitude(normalize_centered(table))


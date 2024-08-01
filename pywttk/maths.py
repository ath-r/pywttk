# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:49:36 2023

@author: nicec
"""

import numpy as np

def primes(max_n):
    numbers = np.arange(3, max_n + 1, 2)
    half = (max_n) // 2
    initial = 4

    for step in range(3, max_n + 1, 2):
        for i in range(initial, half, step):
            numbers[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            numbers = numbers[numbers != np.array(0)]
            numbers = np.insert(numbers, 0, [1, 2])
            return numbers
        
def f2p(f):
    return 69 + 12 * np.log2(f / 440)

def p2f(p):
    return 2 ** ((p - 69) / 12) * 440

def v2db(v):
    return 20 * np.log10(v)

def db2v(db):
    return 10 ** (db / 20)

def r2db(v1, v2):
    return 10 * np.log10(v1 / v2)

def db2r(db):
    return 10 ** (db / 10)
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:32:01 2023

@author: nate


bad implementations of math stuff

"""

import cmath
#import math

def bad_dft(in_arr):
    
    N = len(in_arr)
    
    out_arr = [];
    
    #for each frequency 2pi*1/N, 2pi*2/N, ..., 2pi*N/N
    for f in range(N) :
        
        csum = complex(0,0)
        #for each term
        for n in range(N):
            
            #cumulate in_arr[n] * e^(-2*i*pi*f*n/N)
            csum = csum + in_arr[n] * cmath.exp(complex(0,-2)*cmath.pi*f*n/N)
        
        out_arr.append(csum)
    return out_arr


def bad_idft(in_arr):
    
    N = len(in_arr)
    
    out_arr = [];
    for f in range(N):
    
        csum = complex(0,0)
        
        for n in range (N):
            csum= csum + in_arr[n] * cmath.exp( complex(0,2)*n*f*cmath.pi/N )
            
        csum = csum/N
        
        out_arr.append(csum)
    return out_arr
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:32:01 2023

@author: nate


bad implementations of math stuff

"""

import cmath
import math

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
    
def sort_by_mag(in_arr):
    
    N = len(in_arr)
    
    if N <= 1 :
        return in_arr
    
    #check first, middle, last and find middle
    threshold = 0
    magf = abs(in_arr[0])
    magm = abs(in_arr[ round(N/2) ])
    magl = abs(in_arr[N-1])

    #ugly because we don't want to sort within a sort...
    if magf < magm and magf > magl:
        threshold = magf
    elif magf > magm and magf < magl:
        threshold = magf
    elif magm < magf and magm > magl:
        threshold = magm
    elif magm > magf and magm < magl:
        threshold = magm
    else:
        threshold = magl
        
    sub_arr_lower = []
    sub_arr_higher = []
    
    #check if array is already sorted...
    is_sorted = True
    sorted_last_m = magf
    
    #make 2 sub arrays, less than eq the threshold and greater than
    for n in range(N):
        
        magn = abs(in_arr[n])
        
        #add to sub lists
        if magn <= threshold :
            sub_arr_lower.append(in_arr[n])
        else:
            sub_arr_higher.append(in_arr[n])
            
        
        #check if list is sorted
        if is_sorted == True :
            if magn < sorted_last_m:
                is_sorted = False
            else :
                sorted_last_m = magn

    if is_sorted == True :
        return in_arr
    
    sorted_low = sort_by_mag(sub_arr_lower)
    sorted_high = sort_by_mag(sub_arr_higher)
    
    sorted_low.extend(sorted_high)
    return sorted_low
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
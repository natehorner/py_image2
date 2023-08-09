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


#insertion sort - better because the numbers can be so granular
def isort_by_mag(in_arr):
    N= len(in_arr)
    
    for i in range(N):
        val = in_arr[i]
        val_mag = abs(in_arr[i])
        j = i-1
        while j>=0 and abs(in_arr[j]) < val_mag :
            in_arr[j+1] = in_arr[j]
            j-=1
        in_arr[j+1] = val
        
        if i%10000 == 0 :
            print("insertion sort " + str(100*i/N) + "%")
                  
    return in_arr
            

def sort_by_mag(in_arr):
    
    N = len(in_arr)
    print("Starting sort_by_mag size " + str(N))    
    if N <= 1 :
        return in_arr
    
    threshold = (abs(in_arr[0]) + abs(in_arr[N-1]) )/2

    print(str(abs(in_arr[0])) +","+str(abs(in_arr[N-1]))+" : " + str(threshold))    
    sub_arr_lower = []
    sub_arr_higher = []
    
    #check if array is already sorted...
    is_sorted = True
    sorted_last_m = abs(in_arr[0])
    
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
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
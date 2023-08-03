# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 17:39:40 2023

@author: Nate
"""

import math
from PIL import Image

#only works with RGB pictures!
colors = 3

#average filter - averages each pixel with surrounding pixels, in
#                 size_sqrt*size_sqrt square filter frame
def im_avg_filter(im_in, size_sqrt) :
    
    width,height = im_in.size
    im_out = Image.new(mode="RGB",size=(width,height))
    
    kernel = []
    for i in range(size_sqrt) :
        row = []
        for j in range(size_sqrt):
            row.append(1/(size_sqrt*size_sqrt))
        kernel.append(row)
        
    for x in range(width) :
        for y in range(height) :
            
            #output pixel
            outpixel = [0,0,0]
            
            for i in range(size_sqrt) :
                for j in range(size_sqrt) : 
                    thisx = x + i - math.floor(size_sqrt/2)
                    thisy = y + j - math.floor(size_sqrt/2)
                    
                    if thisx < 0:
                        thisx = 0
                    if thisy < 0:
                        thisy = 0
                    if thisx >= width:
                        thisx = width-1
                    if thisy >= height:
                        thisy = height-1
                        
                    inpixels = im_in.getpixel((thisx,thisy))
                
                    #compute this pixels contribution to output and add
                    for color in range(colors) :
                        outpixel[color] += kernel[i][j]*inpixels[color]
                        
            #do final rounding and bounding
            for color in range(colors) :                  
                outpixel[color] = round(outpixel[color])

                    
                if outpixel[color] > 255 :
                    outpixel[color] = 255
                if outpixel[color] < 0:
                    outpixel[color] = 0

            #put pixel in the output image
            im_out.putpixel( (x,y), tuple(outpixel) )
            
            #progress print - big images and large frames take a while...
            if ((y+height*x)%100000) == 0 :
                print("Finished " + str(round((100.0*(y+height*x))/(width*height),2)) + " percent") 
    
    return im_out

def im_edge_detect(im_in) :
    
    width,height = im_in.size
    im_out = Image.new(mode="RGB",size=(width,height))
    
    kernel_sqrt = 3
    kernel = [ [1, 0, -1], [2, 0, -2], [1, 0, -1] ]

    for x in range(width) :
        for y in range(height) :
            
            #output pixel
            outpixel = [0,0,0]
            
            #output transpose
            outpixel_t = [0,0,0]
            
            for i in range(kernel_sqrt) :
                for j in range(kernel_sqrt) : 
                    thisx = x + i - math.floor(kernel_sqrt/2)
                    thisy = y + j - math.floor(kernel_sqrt/2)
                    
                    if thisx < 0:
                        thisx = 0
                    if thisy < 0:
                        thisy = 0
                    if thisx >= width:
                        thisx = width-1
                    if thisy >= height:
                        thisy = height-1
                        
                    inpixels = im_in.getpixel((thisx,thisy))
                
                    #compute this pixels contribution to output and add
                    for color in range(colors) :
                        outpixel[color] += kernel[i][j]*inpixels[color]
                        outpixel_t[color] += kernel[j][i]*inpixels[color]

            #do final rounding and bounding
            for color in range(colors) :
                outpixel[color] = math.sqrt( pow(outpixel[color],2) + pow(outpixel_t[color],2) )
                outpixel[color] = round(outpixel[color])
                
                if outpixel[color] > 255 :
                    outpixel[color] = 255
                if outpixel[color] < 0:
                    outpixel[color] = 0

            #put pixel in the output image
            im_out.putpixel( (x,y), tuple(outpixel) )
            
            #progress print - big images take a while...
            if ((y+height*x)%200000) == 0 :
                print("Finished " + str(round((100.0*(y+height*x))/(width*height),2)) + " percent") 
    
    return im_out

"""
SImplify the color pallet

normal range is 0-255 per red/green/blue - restrict to granularity (g)

    0, (g), 2(g), 3(g), etc 

steps only - rounded to nearest for each pixel and color

higher granularity is simpler picture - big numbers don't work (>64 gets dark)
"""
def im_simplify_colors(im_in, granularity):
    if granularity < 2 :
        print("Using minimum granularity of 2!")
        granularity = 2
    if granularity > 255 :
        print("Using maximum granularity of 255")
        granularity = 255
    
    width,height = im_in.size
    im_out = Image.new(mode="RGB",size=(width,height))
    for x in range(width) :
        for y in range(height) :
            
            #output pixel
            outpixel = [0,0,0]
            
            inpixels = im_in.getpixel((x,y))
            for color in range(colors) :
                 
                outpixel[color] = inpixels[color] 
                if outpixel[color]%granularity != 0 :
                    outpixel[color] -= inpixels[color]%granularity
                
                if outpixel[color] > 255 :
                    outpixel[color] = 255
                if outpixel[color] < 0:
                    outpixel[color] = 0
 
            #put pixel in the output image
            im_out.putpixel( (x,y), tuple(outpixel) )
                
            #progress print - big images take a while...
            if ((y+height*x)%200000) == 0 :
                print("Finished " + str(round((100.0*(y+height*x))/(width*height),2)) + " percent") 

    return im_out
 
    
def im_photo_negative(im_in):
    width,height = im_in.size
    im_out = Image.new(mode="RGB",size=(width,height))
    
    for x in range(width) :
        for y in range(height) :
            
            #output pixel
            outpixel = [0,0,0]
    
            inpixels = im_in.getpixel((x,y))
            for color in range(colors) :
                outpixel[color] = 255 - inpixels[color]
 
            #put pixel in the output image
            im_out.putpixel( (x,y), tuple(outpixel) )
                 
            #progress print - big images take a while...
            if ((y+height*x)%200000) == 0 :
                print("Finished " + str(round((100.0*(y+height*x))/(width*height),2)) + " percent") 

    return im_out
           
 
    
 
    
 
    
 
    
 
    
 
                
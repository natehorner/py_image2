# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 17:39:40 2023

@author: Nate
"""

import math
from PIL import Image
import bad_math
import cmath

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

def im_edge_detect(im_in, inverse) :
    
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

                if inverse == True :
                    outpixel[color] = 255 - outpixel[color]
                    
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
           
"""
subtract edge detection from image to add dark outlines

hope it works!
"""
def im_outline(im_in):
    
    width,height = im_in.size
    im_out = Image.new(mode="RGB",size=(width,height))
    
    kernel_sqrt = 3
    kernel = [ [1, 0, -1], [2, 0, -2], [1, 0, -1] ]

    for x in range(width) :
        for y in range(height) :
            
            #outline pixel
            outpixel = [0,0,0]
            
            #outline transpose
            outpixel_t = [0,0,0]
            
            #final pixel
            fpixel = [0,0,0]
            
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

            for color in range(colors) :
                outpixel[color] = math.sqrt( pow(outpixel[color],2) + pow(outpixel_t[color],2) )
                outpixel[color] = round(outpixel[color])
                
                if outpixel[color] < 0:
                    outpixel[color] = 0
            
                #outpixel is the outline negative.  COpy input and subtract negative
                fpixel[color] = inpixels[color] - outpixel[color]
                
                if fpixel[color] < 0:
                    fpixel[color] = 0            
                if fpixel[color] > 255 :
                    fpixel[color] = 255
                
            
            #put pixel in the output image
            im_out.putpixel( (x,y), tuple(fpixel) )
            
            #progress print - big images take a while...
            if ((y+height*x)%200000) == 0 :
                print("Finished " + str(round((100.0*(y+height*x))/(width*height),2)) + " percent") 
    
    return im_out 
    
 
def im_diff(im1, im2, negative_out_mode) :
    width,height = im1.size
    im_out = Image.new(mode="RGB",size=(width,height))
 
    #check size matches
    width2,height2 = im2.size
    if width != width2 or height != height2 :
        print("im_diff error: both images must be same dimensions")
        return
     
    for x in range(width):
        for y in range(height):
            p1 = im1.getpixel((x,y))
            p2 = im2.getpixel((x,y))
             
            outp = []
            
            for color in range( len(p1) ):
                outp.append( abs(p1[color] - p2[color]))
                
                if(outp[color] > 255):
                    outp[color] = 255;
                if(negative_out_mode) :
                    outp[color] = 255 - outp[color]
                    
            im_out.putpixel( (x,y), tuple(outp) )
    
    return im_out

def im_sum(im1,im2):
    width,height = im1.size
    im_out = Image.new(mode="RGB",size=(width,height))
 
    #check size matches
    width2,height2 = im2.size
    if width != width2 or height != height2 :
        print("im_sum error: both images must be same dimensions")
        return
     
    for x in range(width):
        for y in range(height):
            p1 = im1.getpixel((x,y))
            p2 = im2.getpixel((x,y))
             
            outp = []
            
            for color in range( len(p1) ):
                outp.append( p1[color] + p2[color])
                
                if(outp[color] > 255):
                    outp[color] = 255;
                    
            im_out.putpixel( (x,y), tuple(outp) )
    
    return im_out

                 
#minimum value between two images per pixel per color 
def im_min(im1,im2):
    width,height = im1.size
    im_out = Image.new(mode="RGB",size=(width,height))
 
    #check size matches
    width2,height2 = im2.size
    if width != width2 or height != height2 :
        print("im_min error: both images must be same dimensions")
        return
     
    for x in range(width):
        for y in range(height):
            p1 = im1.getpixel((x,y))
            p2 = im2.getpixel((x,y))
             
            outp = []
            
            for color in range( len(p1) ):
                if p1[color] < p2[color] :
                    outp.append( p1[color])
                else :
                    outp.append(p2[color])
                
                    
            im_out.putpixel( (x,y), tuple(outp) )
    
    return im_out


def im_to_3d_arr(im_in) :
    
    width,height = im_in.size
    arr_out = [];
    
    for i in range(width):
        arr_2d_out = []
        for j in range(height):
            arr_1d_out = []
            
            inpixel = im_in.getpixel((i,j))
            
            for color in range(colors):
                arr_1d_out.append( complex(inpixel[color],0) )
            
            arr_2d_out.append(arr_1d_out)
        arr_out.append(arr_2d_out)

    return arr_out;

#return complex arry back to image - mode = true returns only real
#mode = false gives absolute magnitude per value
def carr_to_im(arr_in, concat_mode) :
    
    width = len(arr_in)
    height = len(arr_in[0])
    
    im_out = Image.new(mode="RGB",size=(width,height))
 
    for i in range(width):
        for j in range(height):
            
            outp = []
            
            for color in range(colors):
                val = 0;
                ival = complex(arr_in[i][j][color])
                if concat_mode == True :
                    val = round(ival.real)
                else:
                    val = round( cmath.magnitude(ival) )
                    
                if val > 255:
                    val = 255
                elif val < 0 :
                    val = 0
                
                outp.append(val)
            im_out.putpixel((i,j),tuple(outp))
            
    return im_out


#transform either X or Y direction
def transform_2d_arr_1d(arr_in,row_mode,inverse_mode):
       
    width = len(arr_in)
    height = len(arr_in[0])
    
    arr_out = [];
    for i in range(width):
        arr_2d_out = []
        for j in range(height):
            arr_1d_out = []
            for color in range(colors):
                arr_1d_out.append( complex(0,0) )
            
            arr_2d_out.append(arr_1d_out)
        arr_out.append(arr_2d_out)
            

    outer_size = 0
    inner_size = 0
    
    if row_mode :
        outer_size = height
        inner_size = width
    else :
        outer_size = width
        inner_size = height
    
    for i in range(outer_size):

        for color in range(colors) :
        
            in_arr = []
            for j in range(inner_size):
                inval = 0;
                if row_mode :
                    inval = arr_in[j][i][color]
                else :
                    inval = arr_in[i][j][color]
                    
                in_arr.append(inval)                
            
            freq_arr = 0
            if inverse_mode == True :
                freq_arr = bad_math.bad_idft(in_arr)
            else :          
                freq_arr = bad_math.bad_dft(in_arr)
            
            for j in range(inner_size):
                if row_mode :
                    arr_out[j][i][color] = freq_arr[j]
                else :
                    arr_out[i][j] = freq_arr[j]

    return arr_out
                    

#zero out all values under pct percentile (pct is floating point 0-1)
def cull_3d_arry(arr_in, pct):
    arr_1d = []
    
    for i in range(len(arr_in)):
        for j in range(len(arr_in[1])):
            for color in range(colors):
                arr_1d.append(arr_in[i][j][color])
                    
#    s_arr_wd = bad_math.sort_by_mag(arr_1d)
    s_arr_wd = arr_1d.sort()
    
    t_index = pct * len(arr_1d)
    if t_index >= len(arr_1d):
        t_index = len(arr_1d) - 1;
    elif t_index <= 0:
        t_index = 0
        
    threshold = cmath.magnitude(s_arr_wd[t_index])
    
    arr_3d_out = []
    
    for i in range(len(arr_in)):
        arr_2d_out = []
        for j in range(len(arr_in[1])):
            arr_1d_out = []
            for color in range(colors):
                outval = 0
                inval = arr_in[i][j][color]
                if cmath.magnitude(inval) < threshold :
                    outval = complex(0,0)
                else :
                    outval = arr_in[i][j][color]
                arr_1d_out.append(outval)
            arr_2d_out.append(arr_1d_out)
        arr_3d_out.append(arr_2d_out)
    return arr_3d_out
    


                
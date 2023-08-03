# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 17:40:47 2023

@author: Nate
"""

from PIL import Image
import image_effects

"""
open the file -     any jpg, png or other files in same directory 
                    as this script should work
                    
                    DOES NOT SUPPORT BLACK AND WHITE IMAGES RIGHT NOW!
                    (or multi layered - expects 3 values per pixel)
"""
#im_in = Image.open("images/checkerboard2.png")
#im_in = Image.open("images/cold.jpg")
im_in = Image.open("images/bird.jpg")


#do stuff
#im_out = image_effects.im_avg_filter(im_in, 4)
#im_out = image_effects.im_avg_filter(im_in, 9)

#im_out = image_effects.im_edge_detect(im_in)

#im_out = image_effects.im_simplify_colors(im_in,63)

im_out = image_effects.im_photo_negative(im_in)

im_out.show()
im_in.show()
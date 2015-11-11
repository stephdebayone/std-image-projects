# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:33:42 2015

@author: Stephane
"""

import cv2 
import os.path

from  os.path import join as join 

from PIL import Image 
import pylab  
from matplotlib import pyplot as plt 
import numpy as np 

def display(image):
    pylab.imshow(image)
    pylab.show() 
        
    

VIDEO_DIR =  'D:\\dev\\std-image-projects\\video\\videosfl'

DATA_DIR =  os.path.join(VIDEO_DIR , '2015-11-08T19-39-40.907000' ) 

JPEG_DIR = os.path.join( DATA_DIR , "jpeg" ) 

RECT_DIR = os.path.join(DATA_DIR,"rect") 
img = cv2.imread(join(JPEG_DIR,"44.jpg"))

# display(img) 

rgb = cv2.split(img) 


histo = cv2.calcHist([img],[1] , None  , [256] , [0,256])


color = ('b','g','r')
mask = np.zeros(img.shape[:2], np.uint8) 
rect = (100,200,150, 250)
mask[rect[0]:rect[2],rect[1]:rect[3]] = 255 

for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],mask,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])

plt.show()

print img[100,100][0]
print img[100,100][1]
print img[100,100][2]
print "=" * 30 
imgarr = np.array(img)

print type(img) 
print type(imgarr)

print imgarr[100,100][0]
print imgarr[100,100][1]
print imgarr[100,100][2]

print "=" * 30 

h,v , nbChannels = img.shape[:3] 
print h 
print v 

print "=" * 30 

diff = False 
for i in range(0,h):
    for j in range(0,v):
        for c in range(0,nbChannels):
            if img[i,j][c] != imgarr[i,j][c]:
                print "Difference sur [%d,%d%d]" % (i,j,c) 
                diff = True 
if ( not diff):
    print "Pas de différence" 
    
hhistr,  whistr = histr.shape    

for i in range(0,hhistr):
    for j in range(0,whistr):
            print histr[i,j] ,     

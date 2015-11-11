# -*- coding: utf-8 -*-
"""
Created on Sun Nov 08 13:39:27 2015

@author: Stephane
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
from ProcessImage import ProcessImage


class DisplayImage(ProcessImage):

    def __init__(self,fileName,s1,s2):
        super(DisplayImage, self).__init__(fileName)
        self.s1 = s1
        self.s2 = s2 
        
        
    def processFrame(self, frame):
        subFrame = frame[30:frame.shape[0], 0:frame.shape[1]]
        subFrame = cv2.blur(subFrame,(5,5)) 
        #subFrame  = frame 
        #imgray = cv2.cvtColor(subFrame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(subFrame,45,255,cv2.THRESH_BINARY)
        img = cv2.Canny(thresh,self.s1,self.s2)
        image, contours, hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            print "=>" , contour
            x,y,w,h = cv2.boundingRect(contour)  
            subFrame = cv2.rectangle(subFrame,(x,y),(x+w,y+h),(0,255,0),1)
        return subFrame    
        


def usage():
    print sys.argv[0]  , "<IMAGE> <SEUIL1> <SEUIL2>"
    print "teste Canny avec les seuils donnés en paramétre"
    

    
def testCanny(fileName, s1,s2):
    pi = DisplayImage(fileName,s1,s2)
    pi.process() 
   
      
def main():
    try:
        fileName  = sys.argv[1] 
        s1 = sys.argv[2] 
        s2 = sys.argv[3] 
        print fileName
    except:
        usage() 
        return 
    testCanny(fileName,float(s1),float(s2))    

main() 
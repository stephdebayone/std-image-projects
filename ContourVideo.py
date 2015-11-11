#! /cygdrive/d/Anaconda/python.exe 
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 11:04:40 2015

@author: Stephane
"""


import cv2
import sys
import os
import os.path
from ProcessVideo import ProcessVideo
import shutil
from Config import Config



class ContourVideo(ProcessVideo): 
    
    BEGIN_Y = 30 
    HEADER  = "topx,topy,w,h,id\n" 
    
    def __init__(self,dirName,fileName,config):
        super(ContourVideo, self).__init__(fileName)
        self.dirName = dirName
        self.config = config
        self.f = open(config.DATA_DOUBLONS_CSV , "w+")
        self.f.write(ContourVideo.HEADER)
        self.dirJpeg = config.JPEG_DIR
        self.dirJpegWithRect = config.RECT_DIR
        os.makedirs(self.dirJpeg)
        os.makedirs(self.dirJpegWithRect)
        
    def processFrame(self, frame):
        jpegName = self.config.getImageFile(self.numFrame+1)
        jpegNameWithRect = self.config.getRectImageFile(self.numFrame+1)
        cv2.imwrite(jpegName,frame)
        subFrame = frame[ContourVideo.BEGIN_Y:frame.shape[0], 0:frame.shape[1]]
        subFrame = cv2.blur(subFrame,(5,5)) 
        #subFrame  = frame 
        imgray = cv2.cvtColor(subFrame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,31,255,cv2.THRESH_BINARY)
        img = cv2.Canny(thresh,100,200)
        image, contours, hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            #print "=>" , contour#
            x,y,w,h = cv2.boundingRect(contour)            
            self.f.write( "%d,%d,%d,%d,%d\n" % (x,y+ContourVideo.BEGIN_Y,w,h,self.numFrame+1)) 
            subFrame = cv2.rectangle(frame,(x,y+ContourVideo.BEGIN_Y),(x+w,y+h+ContourVideo.BEGIN_Y),(0,255,0),1)
        cv2.imwrite(jpegNameWithRect, subFrame)
        return frame
    
    def display(self,frame):
        #cv2.imshow(self.window,frame)
        return 
        
    def filterUnique(self):
        self.f.close() 
        self.f = open(self.config.DATA_DOUBLONS_CSV , "r+")
        self.f2 = open(self.config.DATA_CSV , "w")
        self.f2.write(ContourVideo.HEADER)
        lines = self.f.readlines()  
        # suppression de l'entête 
        lines = lines[1:]
        d = {} 
        #suppression des doublons 
        for line in lines: 
            d[line] = True 
        d2= {}
        # classement par l'ID Image 
        for line in d.keys():
            tab = line.split(",")
            idImage = float(tab[4]) 
            if d2.has_key(idImage):
                d2[idImage].append(line)
            else:
                d2[idImage] = [line]
        for k in sorted(d2.keys()):
            for line in d2[k]:
                self.f2.write(line)
        self.f.close()
        self.f2.close()
    
    def end(self):
        self.filterUnique()
        return 
  
def usage():
    print "ContourVideo.py <VIDEO FILE>" 
    print "Crée un répertoire <REP> et extrait les images de la video dans un répertoire <REP>/jpeg " 
    print "Crée des images avec les rectangles identifiés et les met dans un répertoire <REP>/rect "
    print "Crée un fichier data.csv avec les rectangles identifiés pour chaque image " 

      
def main():
    try:
        fileName  = sys.argv[1] 
    except:
        usage() 
        return 
    config  = Config() 
    dirName = config.DATA_DIR 
    
    if os.path.isfile(fileName):
        if os.path.isdir(dirName):
            shutil.rmtree(dirName)
            os.makedirs(dirName)
        else:
            os.makedirs(dirName)
        print fileName 
        print os.path.join(dirName ,fileName)
        shutil.copyfile(fileName,os.path.join(dirName ,os.path.basename(fileName)))
        dc = ContourVideo(dirName, fileName,config)
        dc.process() 
        print "Data created in " , config.DATA_DIR
    else:
        print "Can't find file " + fileName 

main() 
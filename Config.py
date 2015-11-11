# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 12:16:00 2015

@author: Stephane
"""
import os.path
import datetime 


class Config(object):
    
    def __init__(self, rep = None):
        if rep == None:
            self.DATA_DIR = os.path.join(os.getcwd() , 
                                         datetime.datetime.today().isoformat().replace(":","-").replace('T','-') )
        else:
            self.DATA_DIR = rep 

        self.JPEG_DIR = os.path.join( self.DATA_DIR , "jpeg" ) 
        
        self.RECT_DIR = os.path.join(self.DATA_DIR,"rect") 
     
        self.DATA_DOUBLONS_CSV = os.path.join(self.DATA_DIR,"data.csv") 
        
        self.DATA_CSV = os.path.join(self.DATA_DIR,"data_unique.csv") 

    def getImageFile(self,idImage):
        fileName = "%s.jpg" % (idImage) 
        return os.path.join(self.JPEG_DIR,fileName)

    def getRectImageFile(self,idImage):
        fileName = "%s_rect.jpg" % (idImage) 
        return os.path.join(self.RECT_DIR,fileName)
        
    def getCsvDataFile(self):
        return self.DATA_CSV
        
    
    VIDEO_DIR =  'D:\\dev\\std-image-projects\\video\\videosfl'
    
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 12:15:51 2015

@author: Stephane
"""

from Config import Config 
import geometry 
import sys
import pandas 
import numpy as np 
import cv2 


COLORS = ('b','g','r')

def getRectInData(idImage,data):
    rects = [] 
    nbRects = len(data.at[idImage,'topx'])
    for row in range(0,nbRects):
        r = geometry.Rect(data.at[idImage,'topx'][row],
                           data.at[idImage,'topy'][row], 
                           data.at[idImage,'w'][row],
                           data.at[idImage,'h'][row])
       # print r 
        rects.append(r)
    return rects         


def getRects(config,idImage1,idImage2):
    if not hasattr(getRects, "df"):
        datafile = config.getCsvDataFile() 
    getRects.df = pandas.read_csv(datafile,index_col=4, header=0 )
    rectImage1 = getRectInData(idImage1,getRects.df)
    rectImage2 = getRectInData(idImage2,getRects.df)
    return rectImage1, rectImage2     

def computeHistogramme(image,rect):

    # compute mask 
    mask = np.zeros(image.shape[:2], np.uint8) 
    mask[rect.l_top.x:rect.r_top.x,rect.l_top.y:rect.l_bot.y] = 255 
    rect.histogramme = {} 
    for i,color in enumerate(COLORS):
        rect.histogramme[color] = cv2.calcHist([image],[i],mask,[256],[0,256])
    return 
    

def computePreferedRect(rect, lstRect):
    distance = float('inf') 
    preferedRect = None 
    for paramRect in lstRect:
        # la distance est la moyenne des distances pour chaque histogramme 
        d = 0 
        for i,color in enumerate(COLORS):
            d += cv2.compareHist(rect.histogramme[color],paramRect.histogramme[color],cv2.HISTCMP_BHATTACHARYYA)
        d = d / 3 
        if d < distance:
            preferedRect = paramRect 
            distance = d 
    return preferedRect 

def usage():
    print sys.argv[0] + "<REP> <idImage> <idImage2>" 
    print "Tente de correler les rectangles identifiés dans les images dont l'id est donnée en paramétre" 
    print "Le script utilise le fichier data_unique.csv trouvé dans <REP>" 
    print "Les images sont trouvées dans <REP>/jpeg" 
    sys.exit() 

def parseCommandLine():
    try:
        dirName = sys.argv[1] 
        jpg1 = int(sys.argv[2])
        jpg2 = int(sys.argv[3])
    except Exception as e:
        print e
        usage() 
    return dirName, jpg1,jpg2 



def main():
    dirName , jpg1, jpg2 = parseCommandLine() 
    config  = Config(dirName)
    lstRectImage1 , lstRectImage2  = getRects(config,jpg1,jpg2)
    image1 = cv2.imread(config.getImageFile(jpg1))
    image2 = cv2.imread(config.getImageFile(jpg2)) 
    for rect in lstRectImage1: 
        computeHistogramme(image1,rect)
    for rect in lstRectImage2: 
        computeHistogramme(image2,rect)
    for rect in lstRectImage1:
        print rect 
        print computePreferedRect(rect, lstRectImage2) 
        print "=" * 60 
        
        
        
    


main() 
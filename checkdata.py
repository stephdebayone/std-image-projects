# -*- coding: utf-8 -*-
"""
Created on Sun Nov 08 11:24:08 2015

@author: Stephane
"""
import sys 
import geometry

def usage():
    print sys.argv[0] + " csv file "  
    print "Détermine pour chaque image si il y a des triangles qui se chevauchent ...  "


def filterUnique(lines):
    d = {} 
    for line in lines: 
        d[line] = True 
    return d.keys() 
      
def read(fileName):
    reader = open(fileName) 
    lines = reader.readlines() 
    lines = filterUnique(lines)
    rectangles = {} 
    for line in lines:
        line = line[:-1]
        rect = line.split(",")
        topX = float(rect[0])
        topY = float(rect[1])
        w  = float(rect[2]) 
        h = float(rect[3])
        r = geometry.Rect(topX,topY,w,h) 
        idImage = float(rect[4]) 
        if rectangles.has_key(idImage):
            rectangles[idImage].append(r) 
        else:
            rectangles[idImage] = [r] 
    return rectangles 
        
        
def overlap(fileName):
    rectangles = read(fileName)
    for idImage, rectsInImage in sorted(rectangles.iteritems()):
        rect0 = rectsInImage[0]
        print "Image N°= " , idImage 
        for rect in rectsInImage:
            index = rectsInImage.index(rect) +1 
            for rect1 in rectsInImage[index:]:
                if rect1.overlaps_with(rect):
                    print "\t ==> chevauchement !"   
                    print rect1
                    print 
                    print rect 
            

      
def main():
    try:
        fileName  = sys.argv[1] 
    except Exception as e:
        print e
        usage() 
        return 
    
    overlap(fileName)
    

main() 
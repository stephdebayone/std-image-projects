#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 08 18:09:13 2015

@author: Stephane
"""


"""This is a small script to demonstrate using Tk to show PIL Image objects.
The advantage of this over using Image.show() is that it will reuse the
same window, so you can show multiple images without opening a new
window for each image.

This will simply go through each file in the current directory and
try to display it. If the file is not an image then it will be skipped.
Click on the image display window to go to the next image.

Noah Spurrier 2007
"""

import os
import Tkinter
import Image, ImageTk

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.



import os
import os.path

class ProcessImage(object): 
    clicked = False 
    def __init__(self, filename): 
        self.root = Tkinter.Tk()
        self.root.bind("<Button>", button_click_exit_mainloop)
        self.root.geometry('+%d+%d' % (100,100))
        self.filename = filename 
        self.clicked = False 
        self.prepareDisplay(filename)

    def prepareDisplay(self,fileName): 
        pass
        
    def process(self):
        image1 = Image.open(self.filename)
        self.root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(self.root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        self.root.title(self.filename)
        self.root.mainloop()
        self.finish() 
        
    def processFrame(self, frame):
        raise Exception ("To be defined !!!!!!!!!!!!!!!!!" )

    def finish(self):
        pass


def test():
    dirlist = os.listdir('.')
    for f in dirlist:
        try:
            pi = ProcessImage(f)
            pi.process() 
        except Exception as e:
            # This is used to skip anything not an image.
            # Image.open will generate an exception if it cannot open a file.
            # Warning, this will hide other errors as well.
            print e 


if __name__ == '__main__':
    test() 


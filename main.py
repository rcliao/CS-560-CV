#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from Tkinter import Tk, Frame, Menu, Label, BOTH
from tkFileDialog import askopenfilename, asksaveasfilename
from tkSimpleDialog import askstring

from PIL import Image, ImageTk


class MenuFrame(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("CS 560 Homework")
        self.pack(fill=BOTH, expand=1)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        self.label = Label(self.parent)
        
        # File Menu
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Load", command=self.onLoad)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        # Homework 1 Menu
        hw1Menu = Menu(menubar)
        hw1Menu.add_command(label="Gray Scale", command=self.onGray)
        hw1Menu.add_command(label="Resize Image", command=self.onResize)
        hw1Menu.add_command(label="Connect Component", command=self.onConnectedComponent)

        morphologicalMenu = Menu(fileMenu)
        morphologicalMenu.add_command(label="Threshold", command=self.onThreshold)
        morphologicalMenu.add_command(label="Erode", command=self.onErode)
        morphologicalMenu.add_command(label="Dilate", command=self.onDilate)
        morphologicalMenu.add_command(label="Open", command=self.onOpen)
        morphologicalMenu.add_command(label="Close", command=self.onClose)

        hw1Menu.add_cascade(label='Morphological Operations', menu=morphologicalMenu, underline=0)

        hw1Menu.add_command(label="Smooth", command=self.onSmooth)
        hw1Menu.add_command(label="Blur", command=self.onBlur)
        hw1Menu.add_command(label="Equalize the Histogram", command=self.onEqualizeHist)
        hw1Menu.add_command(label="Otsu's method")
        menubar.add_cascade(label="Homework 1", menu=hw1Menu)

    def displayAndUpdate(self):
        self.gray_img = Image.fromarray(self.cv_img)
        self.gray_img_tk = ImageTk.PhotoImage(image=self.gray_img)

        self.parent.geometry("%dx%d+%d+%d" % (self.gray_img_tk.width(), self.gray_img_tk.height(), 100, 100) )
        
        self.label = Label(self.parent, image=self.gray_img_tk)
        self.label.pack()
        self.label.place(x=0, y=0)
        self.parent.update()
        
    """ Quit program """
    def onExit(self):
        self.quit()

    """ Load the Image and show it on the GUI """
    def onLoad(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

        self.cv_img = cv2.imread(filename, 1)

        self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)

        self.displayAndUpdate()

    """ Save the Image into harddisk """
    def onSave(self):
        filename = asksaveasfilename() # show an "Save" dialog box and return the path to the selected file

        cv2.imwrite(filename, self.cv_img)

    """ Conver the image to gray scale and change the image to gray """
    def onGray(self):
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)
        
        self.displayAndUpdate()

    """ Resize the image according to user input """
    def onResize(self):
        ratio = askstring("Ratio", "Enter a Ratio (0 - 1) to resize the image")
        self.cv_img = cv2.resize(self.cv_img, None, fx=float(ratio), fy=float(ratio))

        self.displayAndUpdate()

    """ Erode the image """
    def onErode(self):

        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)
        th3,self.cv_img = cv2.threshold(self.cv_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.cv_img = cv2.erode(self.cv_img,kernel,iterations = 1)
        
        self.displayAndUpdate()

    """ Dilate the image """
    def onDilate(self):

        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)
        th3,self.cv_img = cv2.threshold(self.cv_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.cv_img = cv2.dilate(self.cv_img,kernel,iterations = 1)
        
        self.displayAndUpdate()

    """ Open the image """
    def onOpen(self):

        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)
        th3,self.cv_img = cv2.threshold(self.cv_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.cv_img = cv2.morphologyEx(self.cv_img, cv2.MORPH_OPEN,kernel)
        
        self.displayAndUpdate()

    """ Close the image """
    def onClose(self):

        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)
        th3,self.cv_img = cv2.threshold(self.cv_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.cv_img = cv2.morphologyEx(self.cv_img, cv2.MORPH_CLOSE, kernel)
        
        self.displayAndUpdate()

    """ Thresholding image """
    def onThreshold(self):

        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)

        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)
        th3,self.cv_img = cv2.threshold(self.cv_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        self.displayAndUpdate()

    """ Smooth the image """
    def onSmooth(self):
        kernel = np.ones((5,5),np.float32)/25
        self.cv_img = cv2.filter2D(self.cv_img,-1,kernel)

        self.displayAndUpdate()

    """ Blur the image """
    def onBlur(self):
        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)

        self.displayAndUpdate()

    """ Equalize the histogram """
    def onEqualizeHist(self):
        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)

        self.cv_img = cv2.equalizeHist(self.cv_img)

        self.displayAndUpdate()

    def onConnectedComponent(self):
        # change image to gray scale if not in gray scale mode
        if len(self.cv_img.shape) == 3:
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)
        self.cv_img = cv2.GaussianBlur(self.cv_img,(5,5),0)
        th3,self.cv_img = cv2.threshold(self.cv_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        self.contours, hierarchy = cv2.findContours(self.cv_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

        self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_GRAY2RGB)

        cv2.drawContours(self.cv_img, self.contours, -1, (255,0,0), 5)

        self.displayAndUpdate()




def main():
  
    root = Tk()
    root.geometry("550x550+300+300")
    app = MenuFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

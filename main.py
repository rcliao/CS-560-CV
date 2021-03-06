#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import cv2.cv as cv

from Tkinter import Tk, Frame, Menu, Label, BOTH, LEFT
from tkFileDialog import askopenfilename, asksaveasfilename
from tkSimpleDialog import askstring

from PIL import Image, ImageTk

import random


class MenuFrame(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("CS 560 Homework")
        
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
        hw1Menu.add_command(label="Otsu's method", command=self.onOtsu)
        menubar.add_cascade(label="Homework 1", menu=hw1Menu)

        # Homework 2 Menu
        hw2Menu = Menu(menubar)
        hw2Menu.add_command(label="Extract Apple", command=self.onAppleExtraction)
        hw2Menu.add_command(label="Extract Coins", command=self.onCoinExtraction)
        hw2Menu.add_command(label="Extract Line", command=self.onLineExtraction)

        menubar.add_cascade(label="Homework 2", menu=hw2Menu)

        # Homework 3 Menu
        hw3Menu = Menu(menubar)
        hw3Menu.add_command(label="PCA Computation", command=self.onPCACompute)
        hw3Menu.add_command(label="Eigenfaces")

        menubar.add_cascade(label="Homework 3", menu=hw3Menu)

    """ Display and Update the middle screen """
    def displayAndUpdate(self):
        self.output_img_tmp = Image.fromarray(self.output_img)
        self.output_img_tk = ImageTk.PhotoImage(image=self.output_img_tmp)

        self.input_img_tmp = Image.fromarray(self.input_img)
        self.input_img_tk = ImageTk.PhotoImage(image=self.input_img_tmp)

        if self.input_img_tk.width() < 500:
            self.parent.geometry("%dx%d+%d+%d" % (self.input_img_tk.width()*2, self.input_img_tk.height()+50, 100, 100) )
        else:
            self.input_img_tmp = self.input_img_tmp.resize((500, self.input_img_tk.height() * 500 / self.input_img_tk.width()),Image.ANTIALIAS)
            self.input_img_tk = ImageTk.PhotoImage(image=self.input_img_tmp)
            self.output_img_tmp = self.output_img_tmp.resize((500, self.output_img_tk.height() * 500 / self.output_img_tk.width()),Image.ANTIALIAS)
            self.output_img_tk = ImageTk.PhotoImage(image=self.output_img_tmp)

            self.parent.geometry("%dx%d+%d+%d" % (1050, self.input_img_tk.height() + 50, 100, 100) )
        
        self.input_img_label = Label(self.parent, image=self.input_img_tk, borderwidth=3, height=self.input_img_tk.height(), width=self.input_img_tk.width())
        self.input_img_label.grid(row=0,column=0)

        self.input_img_label_text = Label(self.parent, text="Input Image")
        self.input_img_label_text.grid(row=1,column=0)

        self.output_img_label = Label(self.parent, image=self.output_img_tk, borderwidth=3, height=self.output_img_tk.height(), width=self.output_img_tk.width())
        self.output_img_label.grid(row=0,column=1)

        self.output_img_label_text = Label(self.parent, text="Output Image")
        self.output_img_label_text.grid(row=1,column=1)

        self.parent.update()
        
    """ Quit program """
    def onExit(self):
        self.quit()

    """ Load the Image and show it on the GUI """
    def onLoad(self):
        self.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

        self.output_img = cv2.imread(self.filename, 1)

        self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2BGR)

        self.input_img = cv2.imread(self.filename, 1)

        self.input_img = cv2.cvtColor(self.input_img, cv2.COLOR_RGB2BGR)

        self.displayAndUpdate()

    """ Save the Image into harddisk """
    def onSave(self):
        filename = asksaveasfilename() # show an "Save" dialog box and return the path to the selected file

        cv2.imwrite(filename, self.output_img)

    """ Conver the image to gray scale and change the image to gray """
    def onGray(self):
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)
        
        self.displayAndUpdate()

    """ Resize the image according to user input """
    def onResize(self):
        ratio = askstring("Ratio", "Enter a Ratio (0 - 1) to resize the image")
        self.output_img = cv2.resize(self.output_img, None, fx=float(ratio), fy=float(ratio))

        self.displayAndUpdate()

    """ Erode the image """
    def onErode(self):

        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)
        th3,self.output_img = cv2.threshold(self.output_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.output_img = cv2.erode(self.output_img,kernel,iterations = 1)
        
        self.displayAndUpdate()

    """ Dilate the image """
    def onDilate(self):

        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)
        th3,self.output_img = cv2.threshold(self.output_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.output_img = cv2.dilate(self.output_img,kernel,iterations = 1)
        
        self.displayAndUpdate()

    """ Open the image """
    def onOpen(self):

        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)
        th3,self.output_img = cv2.threshold(self.output_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.output_img = cv2.morphologyEx(self.output_img, cv2.MORPH_OPEN,kernel)
        
        self.displayAndUpdate()

    """ Close the image """
    def onClose(self):

        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        # thresholding
        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)
        th3,self.output_img = cv2.threshold(self.output_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        kernel = np.ones((5,5),np.uint8)
        self.output_img = cv2.morphologyEx(self.output_img, cv2.MORPH_CLOSE, kernel)
        
        self.displayAndUpdate()

    """ Thresholding image """
    def onThreshold(self):

        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)
        th3,self.output_img = cv2.threshold(self.output_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        self.displayAndUpdate()

    """ Smooth the image """
    def onSmooth(self):
        kernel = np.ones((5,5),np.float32)/25
        self.output_img = cv2.filter2D(self.output_img,-1,kernel)

        self.displayAndUpdate()

    """ Blur the image """
    def onBlur(self):
        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)

        self.displayAndUpdate()

    """ Equalize the histogram """
    def onEqualizeHist(self):
        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        self.output_img = cv2.equalizeHist(self.output_img)

        self.displayAndUpdate()

    """ Using findContours and drawContours to create Connected Component Analysis """
    def onConnectedComponent(self):
        self.storage = cv.CreateMemStorage()

        self.output_img = cv.LoadImage(self.filename)

        cv.PyrSegmentation(self.output_img, self.output_img, self.storage, 4, 255, 55)

        self.output_img = np.asarray( self.output_img[:, :] )

        self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2BGR)

        self.displayAndUpdate()


    """ Otsu's method """
    def onOtsu(self):
        # change image to gray scale if not in gray scale mode
        if len(self.output_img.shape) == 3:
            self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_RGB2GRAY)

        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)

        # find thresh value using otsu's method
        # find normalized_histogram, and its cum_sum
        hist = cv2.calcHist([self.output_img],[0],None,[256],[0,256])
        hist_norm = hist.ravel()/hist.max()
        Q = hist_norm.cumsum()
         
        bins = np.arange(256)
         
        fn_min = np.inf
        thresh = -1
         
        for i in xrange(1,256):
            p1,p2 = np.hsplit(hist_norm,[i]) # probabilities
            q1,q2 = Q[i],Q[255]-Q[i] # cum sum of classes
            b1,b2 = np.hsplit(bins,[i]) # weights
             
            # finding means and variances
            if q2 != 0 and q1 != 0:
                m1,m2 = np.sum( p1*b1 )/q1, np.sum( p2*b2 )/q2 
                v1,v2 = np.sum(((b1-m1)**2)*p1)/q1,np.sum(((b2-m2)**2)*p2)/q2
             
                # calculates the minimization function
                fn = v1*q1 + v2*q2
                if fn < fn_min:
                    fn_min = fn
                    thresh = i

        print 'Thresh value from mine: ', thresh

        ret, otsu = cv2.threshold(self.output_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        print 'Thresh value from opencv: ', ret

        th3,self.output_img = cv2.threshold(self.output_img,thresh,255,cv2.THRESH_BINARY)

        self.displayAndUpdate()

    ''' Apple Extraction '''
    def onAppleExtraction(self):
        self.output_img = cv2.GaussianBlur(self.output_img,(5,5),0)
        self.output_img = cv2.cvtColor(self.output_img,cv2.COLOR_RGB2GRAY)

        circles = cv2.HoughCircles(self.output_img,cv.CV_HOUGH_GRADIENT,1,75,
                                    param1=148,param2=27,minRadius=0,maxRadius=0)

        self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_GRAY2RGB)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(self.output_img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(self.output_img,(i[0],i[1]),2,(0,0,255),3)
 
        self.displayAndUpdate()

    ''' Coin Extraction '''
    def onCoinExtraction(self):
        print self.filename
        if "coins1" in self.filename:
            self.output_img = cv2.GaussianBlur(self.output_img,(17,17),0)
        else:
            self.output_img = cv2.GaussianBlur(self.output_img,(7,7),0)
        self.output_img = cv2.cvtColor(self.output_img,cv2.COLOR_RGB2GRAY)

        cValue = 150

        circles = cv2.HoughCircles(self.output_img,cv.CV_HOUGH_GRADIENT,1,50,
                                    param1=cValue,param2=40,minRadius=0,maxRadius=0)

        self.output_img = cv2.cvtColor(self.output_img, cv2.COLOR_GRAY2RGB)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(self.output_img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(self.output_img,(i[0],i[1]),2,(0,0,255),3)
 
        self.displayAndUpdate()

    ''' Extract Line '''
    def onLineExtraction(self):
        gray = cv2.cvtColor(self.output_img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 80, 200,apertureSize = 3)

        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=8)

        for x1,y1,x2,y2 in lines[0]:
            cv2.line(self.output_img,(x1,y1),(x2,y2),(0,255,0),2)
 
        self.displayAndUpdate()

    def onPCACompute(self):
        dataArray = np.array([
            [2.5, 2.4],
            [0.5, 0.7],
            [2.2, 2.9],
            [1.9, 2.2],
            [3.1, 3.0],
            [2.3, 2.7],
            [2, 1.6],
            [1, 1.1],
            [1.5, 1.6],
            [1.1, 0.9]
        ])

        mean, eigenvectors = cv2.PCACompute(dataArray)

        print mean
        print eigenvectors

def main():
  
    root = Tk()
    root.geometry("550x550+100+100")
    app = MenuFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

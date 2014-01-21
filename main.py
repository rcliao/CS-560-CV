#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from Tkinter import Tk, Frame, Menu, Label, BOTH
from tkFileDialog import askopenfilename, asksaveasfilename

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
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Load", command=self.onLoad)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        hw1Menu = Menu(menubar)
        hw1Menu.add_command(label="Gray Scale", command=self.onGray)
        hw1Menu.add_command(label="Resize Image")
        hw1Menu.add_command(label="Connect Component")
        hw1Menu.add_command(label="Erode/Dilate/Open/Close")
        hw1Menu.add_command(label="Smooth")
        hw1Menu.add_command(label="Blur")
        hw1Menu.add_command(label="Equalize the Histogram")
        hw1Menu.add_command(label="Otsu's method")
        menubar.add_cascade(label="Homework 1", menu=hw1Menu)
        

    def onExit(self):
        self.quit()

    """ Load the Image and show it on the GUI """
    def onLoad(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

        self.cv_img = cv2.imread(filename, 1)
        self.img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)

        self.gray_img = Image.fromarray(self.img)
        self.gray_img_tk = ImageTk.PhotoImage(image=self.gray_img)
        
        self.label = Label(self.parent, image=self.gray_img_tk)
        self.label.pack()
        self.label.place(x=0, y=0)
        self.parent.update()

    """ Save the Image into harddisk """
    def onSave(self):
        filename = asksaveasfilename() # show an "Save" dialog box and return the path to the selected file

        cv2.imwrite(filename, self.img)

    def onGray(self):
        self.img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2GRAY)
        self.gray_img = Image.fromarray(self.img)
        self.gray_img_tk = ImageTk.PhotoImage(image=self.gray_img)
        
        self.label = Label(self.parent, image=self.gray_img_tk)
        self.label.pack()
        self.label.place(x=0, y=0)
        self.parent.update()


def main():
  
    root = Tk()
    root.geometry("550x550+300+300")
    app = MenuFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

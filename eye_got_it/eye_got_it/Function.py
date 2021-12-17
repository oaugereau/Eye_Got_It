#import python Module
import sys, os, time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *
import Config

#from matplotlib import pyplot as plt

def defineStyle(widget,police,fontSize,fontType,colorFont,colorText,colorselect):

    widget.setStyleSheet("color: " + str(colorText) +";"
                        "background-color: " + str(colorFont) +";"
                        "font: "+ str(fontType) +" " + str(fontSize)+ "px " + str(police) + ";"
                        "selection-color: "+ str(colorselect) +";")
"""
def changeFontSize(widget,police,fontSize,fontType,colorFont,colorText,colorselect):
    widget.setStyleSheet("font: "+ str(fontType) +" " + str(fontSize)+ "px " + str(police) + ";")
"""
def UpdateComboBox(comboBox,tab):
    comboBox.clear()
    comboBox.addItems(tab)
    comboBox.hide()
    comboBox.setCurrentIndex(-1)
    comboBox.show()
        
def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

#get time in milli seconde
def current_milli_time():
    return round(time.time() * 1000)



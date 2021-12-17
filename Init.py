#import python Module
import sys, os

    
def CheckLib():
    #check if python module required
    restart=False
    
    #check python version
    if (sys.version_info < (3, 0)):
        sys.exit("You must install python 3")
    
    #check if PyQt5 is installed
    try:
        import PyQt5
    except ImportError:
        restart=True
        print("PyQt5 not installed : => pip install PyQt5")
            

    #check if configparser is installed   
    try:
        import configparser
    except ImportError:
        restart=True
        print("configparser not installed : => pip install configparser")

    #check if logging are installed 
    try:
        import logging
    except ImportError:
        restart=True
        print("logging not installed : => pip install logging")

    #check if pyaudio are installed 
    try:
        import pyaudio
    except ImportError:
        restart=True
        print("pyaudio not installed : => pip install pyaudio if problem to install it try pip install pipwin then pipwin install pyaudio")


    #check if wave are installed 
    try:
        import wave
    except ImportError:
        restart=True
        print("wave not installed : => pip install wave")

     #check if numpy are installed 
    try:
        import numpy
    except ImportError:
        restart=True
        print("numpy not installed : => pip install numpy")

    #check if sklearn are installed 
    try:
        import sklearn
    except ImportError:
        restart=True
        print("scikit-learn not installed : => pip install scikit-learn")

    #check if opencv are installed 
    try:
        import cv2
    except ImportError:
        restart=True
        print("opencv not installed : => pip install opencv-python")

    #check if pygrabber are installed 
    try:
        import pygrabber
    except ImportError:
        restart=True
        print("pygrabber not installed : => pip install pygrabber")

        
    if restart:
        sys.exit("please install them")
    else:
        sys.exit("All requirement are good")

if __name__=="__main__":
    CheckLib()


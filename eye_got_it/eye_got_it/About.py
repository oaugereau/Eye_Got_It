#about.py => credit
#contain one class About that contain the name of authors and logo credit

#import python Module
import sys, os
from PyQt5 import QtCore, QtWidgets, QtGui
#import others Modules
import Function, Config

#Eye Got It credit display
class About(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        #windows config        
        self.setWindowTitle('About Eye Got It')
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=250
        self.height=250
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        self.title = QtWidgets.QLabel("Created by :",self)
        self.title.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.title, 0,0)

        self.creator1 = QtWidgets.QLabel("Nougier Axel  : a7nougie@enib.fr",self)
        self.creator1.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(18)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.creator1, 1,0)

        self.creator2 = QtWidgets.QLabel("Menard Victor : v7menard@enib.fr",self)
        self.creator2.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(18)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.creator2, 2,0)

        self.creator3 = QtWidgets.QLabel("Mohamed EL BAHA",self)
        self.creator3.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(18)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.creator3, 3,0)
        if os.path.isfile(os.path.join(Config.PATH_IMAGE,"enib.jpg")):
            with open(str(os.path.join(Config.PATH_IMAGE,"enib.jpg")),'r') as UseFile:
                pixmap = QtGui.QPixmap(str(os.path.join(Config.PATH_IMAGE,"enib.jpg")))
                self.enib = QtWidgets.QLabel(self)                                                                                                                 
                self.enib.setPixmap(pixmap)  
                self.grid.addWidget(self.enib, 4,0)          

        self.icon = QtWidgets.QLabel("Eye Got It icon created by Denny Hurkmans.\nThis icon is licensed as Creative Commons CCBY",self)
        self.icon.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(12)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.icon, 5,0)

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 6,0)
        self.back.clicked.connect(self.close)


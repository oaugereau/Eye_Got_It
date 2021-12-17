#import python Module
import sys, os, shutil, webbrowser,cv2
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
#import others Modules
import Function, Welcome, Config, ConfigFileManagement, Audio, EyeTracker, Video

class Parameters(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.option_set_text=[]
        self.option_set_switch_button=[]
        self.newTheme ="" 

        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Parameters')
        self.width=1100
        self.height=600
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.setMinimumSize(self.width, self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint |   QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowTitleHint)

        #User GroupBox
        self.userGroupBox = QtWidgets.QGroupBox("User Files Name")
        self.userGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.userLayout = QtWidgets.QFormLayout()

        self.mcqAnswer = QtWidgets.QLabel("MCQ answer",self)
        self.mcqAnswer.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.mcqAnswerEdit=QtWidgets.QLineEdit(str(Config.mcqAnswer),self)#self.mcqAnswerEdit=QtWidgets.QLineEdit(str(Config.mcqAnswer.split(',')[0]),self)
        self.mcqAnswerEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.mcqAnswerEdit.textChanged.connect(lambda:self.defaultEdit(self.mcqAnswerEdit))
        self.userLayout.addRow(self.mcqAnswer, self.mcqAnswerEdit)

        self.textPosition = QtWidgets.QLabel("Text Position",self)
        self.textPosition.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.textPositionEdit=QtWidgets.QLineEdit(str(Config.textPosition),self)#self.textPositionEdit=QtWidgets.QLineEdit(str(Config.textPosition.split(',')[0]),self)
        self.textPositionEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.textPositionEdit.textChanged.connect(lambda:self.defaultEdit(self.textPositionEdit))
        self.userLayout.addRow(self.textPosition, self.textPositionEdit)

        self.textPart = QtWidgets.QLabel("Text Part",self)
        self.textPart.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.textPartEdit=QtWidgets.QLineEdit(str(Config.textPart),self) #self.textPartEdit=QtWidgets.QLineEdit(str(Config.textPart.split(',')[0]),self)
        self.textPartEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.textPartEdit.textChanged.connect(lambda:self.defaultEdit(self.textPartEdit))
        self.userLayout.addRow(self.textPart, self.textPartEdit)
        
        self.userGroupBox.setLayout(self.userLayout)

        self.grid.addWidget(self.userGroupBox,0,0)

        #Sound GroupBox
        self.soundGroupBox = QtWidgets.QGroupBox("Sound")
        self.soundGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.soundLayout = QtWidgets.QFormLayout()

        self.rate = QtWidgets.QLabel("Rate",self)
        self.rate.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.rateEdit=QtWidgets.QLineEdit(str(Config.rate),self)
        self.rateEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
                        
        self.rateEdit.textChanged.connect(lambda:self.IntEdit(self.rateEdit))
        self.soundLayout.addRow(self.rate, self.rateEdit)

        self.channels = QtWidgets.QLabel("Channels",self)
        self.channels.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.channels, 2,20)

        self.channelsEdit=QtWidgets.QLineEdit(str(Config.channels),self)
        self.channelsEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.channelsEdit.textChanged.connect(lambda:self.IntEdit(self.channelsEdit))
        self.soundLayout.addRow(self.channels, self.channelsEdit)

        self.chunk = QtWidgets.QLabel("Chunk",self)
        self.chunk.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.chunkEdit=QtWidgets.QLineEdit(str(Config.chunk),self)
        self.chunkEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.chunkEdit.textChanged.connect(lambda:self.IntEdit(self.chunkEdit))
        self.soundLayout.addRow(self.chunk, self.chunkEdit)

        self.soundOut = QtWidgets.QLabel("Sound output name",self)
        self.soundOut.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.soundOutEdit=QtWidgets.QLineEdit(str(Config.soundOut),self)#self.soundOutEdit=QtWidgets.QLineEdit(str(Config.soundOut.split(',')[0]),self)
        self.soundOutEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.soundOutEdit.textChanged.connect(lambda:self.defaultEdit(self.soundOutEdit))
        self.soundLayout.addRow(self.soundOut, self.soundOutEdit)

        self.soundGroupBox.setLayout(self.soundLayout)

        self.grid.addWidget(self.soundGroupBox,0,1)
        
        #Screenshot GroupBox
        self.screenshotGroupBox = QtWidgets.QGroupBox("Screenshot")
        self.screenshotGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.screenshotLayout = QtWidgets.QFormLayout()
        self.screenshotName = QtWidgets.QLabel("Screenshot Name",self)
        self.screenshotName.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.screenshotNameEdit=QtWidgets.QLineEdit(str(Config.screenshotName),self)
        self.screenshotNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.screenshotNameEdit.textChanged.connect(lambda:self.defaultEdit(self.screenshotNameEdit))
        self.screenshotLayout.addRow(self.screenshotName, self.screenshotNameEdit)

        self.screenshotGroupBox.setLayout(self.screenshotLayout)

        self.grid.addWidget(self.screenshotGroupBox,1,0)
        
        #Eye Tracker Data GroupBox
        self.eyeTrackerDataGroupBox = QtWidgets.QGroupBox("Eye Tracker Data")
        self.eyeTrackerDataGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.eyeTrackerDataLayout = QtWidgets.QFormLayout()

        self.eyeTrackerData = QtWidgets.QLabel("Eye Tracker Eyes :",self)
        self.eyeTrackerData.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.eyeTrackerDataEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerData),self) 
        self.eyeTrackerDataEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.eyeTrackerDataEdit.textChanged.connect(lambda:self.defaultEdit(self.eyeTrackerDataEdit))
        self.eyeTrackerDataLayout.addRow(self.eyeTrackerData, self.eyeTrackerDataEdit)

        self.eyeTrackerHeadData = QtWidgets.QLabel("Eye Tracker Head:",self)
        self.eyeTrackerHeadData.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.eyeTrackerHeadDataEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerHeadData),self) 
        self.eyeTrackerHeadDataEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.eyeTrackerHeadDataEdit.textChanged.connect(lambda:self.defaultEdit(self.eyeTrackerHeadDataEdit))
        self.eyeTrackerDataLayout.addRow(self.eyeTrackerHeadData, self.eyeTrackerHeadDataEdit)

        self.eyeTrackerDataGroupBox.setLayout(self.eyeTrackerDataLayout)

        self.grid.addWidget(self.eyeTrackerDataGroupBox,1,1)

        #Video GroupBox
        self.videoGroupBox = QtWidgets.QGroupBox("Video")
        self.videoGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.videoLayout = QtWidgets.QFormLayout()
        self.video = QtWidgets.QLabel("Video save :",self)
        self.video.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.videoEdit=QtWidgets.QLineEdit(str(Config.videoOut),self) 
        self.videoEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.videoEdit.textChanged.connect(lambda:self.defaultEdit(self.videoEdit))
        self.videoLayout.addRow(self.video, self.videoEdit)

        self.actionUnits = QtWidgets.QPushButton('Action Units', self)
        self.actionUnits.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.actionUnits.clicked.connect(self.actionUnits_click)
        self.videoLayout.addRow(None,self.actionUnits)
        #self.actionUnits.hide()
        self.videoGroupBox.setLayout(self.videoLayout)

        self.grid.addWidget(self.videoGroupBox,2,1)
        
        #Theme GroupBox
        self.themeGroupBox = QtWidgets.QGroupBox("Theme")
        self.themeGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.themeLayout = QtWidgets.QHBoxLayout()
        
        self.dark= QtWidgets.QRadioButton('Dark')
        self.dark.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.themeLayout.addWidget(self.dark)
        self.dark.toggled.connect(self.btnstate)
            
        self.normal= QtWidgets.QRadioButton('Normal')
        self.normal.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.themeLayout.addWidget(self.normal)
        self.normal.toggled.connect(self.btnstate)
        
        self.btngroup = QtWidgets.QButtonGroup()
        self.btngroup.addButton(self.dark)
        self.btngroup.addButton(self.normal)
               
        if Config.THEME == "Dark":
            self.dark.setChecked(True)
        elif Config.THEME == "Normal" :
            self.normal.setChecked(True)
        self.themeGroupBox.setLayout(self.themeLayout)

        self.grid.addWidget(self.themeGroupBox,2,0)

        #Report GroupBox
        self.reportGroupBox = QtWidgets.QGroupBox("Report")
        self.reportGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.reportLayout = QtWidgets.QFormLayout()

        self.glissades = QtWidgets.QLabel("Glissade :",self)
        self.glissades.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.glissadesEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerGlissades),self) 
        self.glissadesEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.glissadesEdit.textChanged.connect(lambda:self.defaultEdit(self.glissadesEdit))
        self.reportLayout.addRow(self.glissades, self.glissadesEdit)

        self.saccades = QtWidgets.QLabel("Saccades :",self)
        self.saccades.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.saccadesEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerSaccades),self) 
        self.saccadesEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.saccadesEdit.textChanged.connect(lambda:self.defaultEdit(self.saccadesEdit))
        self.reportLayout.addRow(self.saccades, self.saccadesEdit)

        self.fixations = QtWidgets.QLabel("Fixations :",self)
        self.fixations.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.fixationsEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerFixations),self) 
        self.fixationsEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.fixationsEdit.textChanged.connect(lambda:self.defaultEdit(self.fixationsEdit))
        self.reportLayout.addRow(self.fixations, self.fixationsEdit)

        self.velocityGazes = QtWidgets.QLabel("VelocityGazes :",self)
        self.velocityGazes.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.velocityGazesEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerVelocityGazes),self) 
        self.velocityGazesEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.velocityGazesEdit.textChanged.connect(lambda:self.defaultEdit(self.velocityGazesEdit))
        self.reportLayout.addRow(self.velocityGazes, self.velocityGazesEdit)

        self.eyeTrackerScreenshot = QtWidgets.QLabel("Eye Tracker screenshot :",self)
        self.eyeTrackerScreenshot.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.eyeTrackerScreenshotEdit=QtWidgets.QLineEdit(str(Config.eyeTrackerScreenshot),self) 
        self.eyeTrackerScreenshotEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.eyeTrackerScreenshotEdit.textChanged.connect(lambda:self.defaultEdit(self.eyeTrackerScreenshotEdit))
        self.reportLayout.addRow(self.eyeTrackerScreenshot, self.eyeTrackerScreenshotEdit)

        self.wordScreenshot = QtWidgets.QLabel("Word Screenshot :",self)
        self.wordScreenshot.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.wordScreenshotEdit=QtWidgets.QLineEdit(str(Config.wordScreenshot),self) 
        self.wordScreenshotEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.wordScreenshotEdit.textChanged.connect(lambda:self.defaultEdit(self.wordScreenshotEdit))
        self.reportLayout.addRow(self.wordScreenshot, self.wordScreenshotEdit)


        self.reportGroupBox.setLayout(self.reportLayout)

        self.grid.addWidget(self.reportGroupBox,0,2,3,1)

        # Test GroupBox
        if Config.audioTest or Config.videoTest or Config.eyeTrackerTest:

            self.testGroupBox = QtWidgets.QGroupBox("Test Section")
            self.testGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")
            self.testLayout = QtWidgets.QHBoxLayout()

            if Config.audioTest :
                self.soundTest = QtWidgets.QPushButton('Sound Test', self)
                self.soundTest.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";"+"}")
                self.soundTest.clicked.connect(self.sound_click)
                self.testLayout.addWidget(self.soundTest)

            if Config.videoTest:
                self.videoTest = QtWidgets.QPushButton('Video Test', self)
                self.videoTest.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";"+"}")
                self.videoTest.clicked.connect(self.videoTest_click)
                self.testLayout.addWidget(self.videoTest)

            if Config.eyeTrackerTest:
                self.eyeTrackerTest = QtWidgets.QPushButton('Eye Tracker Test', self)
                self.eyeTrackerTest.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";"+"}")
                self.eyeTrackerTest.clicked.connect(self.eyeTrackerTest_click)
                self.testLayout.addWidget(self.eyeTrackerTest)

            self.testGroupBox.setLayout(self.testLayout)

            self.grid.addWidget(self.testGroupBox,3,0,1,3)

        #Button
        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 5,0)
        self.back.clicked.connect(self.close)

        self.save = QtWidgets.QPushButton('Save', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.save, 5,1)
        self.save.clicked.connect(self.saveConfig)
        
        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 5,2)
        self.help.clicked.connect(self.help_click)
        self.help.setEnabled(True) 

        self.btngroupSave = QtWidgets.QButtonGroup()
        self.btngroupSave.addButton(self.save)

        self.closeEvent = self.closeEvent
        self.closeCondition = True

        
        

    def defaultEdit(self,defaultEdit):

        if defaultEdit.text() == '':
            defaultEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        else :
            if defaultEdit.text() != '':
                defaultEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

    #check if parameter is integer                        
    def IntEdit(self,widget):
        if not Function.is_integer(widget.text()) and widget.text() != '':
            widget.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")
        else:
            widget.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        if widget.text() == '':
            widget.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")
    def actionUnits_click(self):
        self.actionUnitsWindows = Video.ActionUnits()
        self.actionUnitsWindows.show()
    #sound test                        
    def sound_click(self):
        self.askQuit=False
        self.soundWindows = Audio.AudioTestDisplay()
        self.soundWindows.show()   



    #video test
    def videoTest_click(self):
        self.askQuit=False
        
        if hasattr(self, "videoTestView"):
            #self.videoTestView.stop()
            try:
                cv2.destroyAllWindows()
            except:
                pass
        
        self.videoTestView = Video.videoTestWindows()
        
        """
        message=QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Question)
        message.setText("Press ECHAP to close video view")
        message.setWindowTitle("Video Test")
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message=message.exec_()
        """
        self.videoTestView.show()
        
        

    def eyeTrackerTest_click(self):
        self.askQuit=False
        self.eyeTrackerTest = EyeTracker.EyeTrackerTest()
        self.eyeTrackerTest.show()
        

    #theme state
    def btnstate(self):
        rbtn = self.sender()
        if rbtn.isChecked() == True:            
            self.newTheme=rbtn.text()

    #save parameter
    def saveConfig(self):

        configChanged = False

        if self.newTheme != Config.THEME:
            if self.newTheme == "Dark":
                Config.configParser.SetParameters(None,"theme","Dark")
            elif self.newTheme == "Normal":
                Config.configParser.SetParameters(None,"theme","Normal")

            configChanged = True

        if int(self.rateEdit.text()) != Config.rate:
            Config.configParser.SetParameters("SOUND","rate",self.rateEdit.text())
            configChanged = True
        
        if int(self.channelsEdit.text()) != Config.channels:
            Config.configParser.SetParameters("SOUND","channels",self.channelsEdit.text())
            configChanged = True

        if int(self.chunkEdit.text()) != Config.chunk :
            Config.configParser.SetParameters("SOUND","chunk",self.chunkEdit.text())
            configChanged = True

        if self.soundOutEdit.text() != Config.soundOut:
            Config.configParser.SetParameters("SOUND","sound_out",self.soundOutEdit.text())
            configChanged = True

        if self.screenshotNameEdit.text() != Config.screenshotName:
            Config.configParser.SetParameters("SYSTEM","screenshot_name",self.screenshotNameEdit.text())
            configChanged = True
        
        if self.mcqAnswerEdit.text() != Config.mcqAnswer:
            Config.configParser.SetParameters("USER","mcq_answer",self.mcqAnswerEdit.text())
            configChanged = True
        
        if self.textPositionEdit.text() != Config.textPosition :
            Config.configParser.SetParameters("USER","text_position",self.textPositionEdit.text())
            configChanged = True
        
        if self.textPartEdit.text() != Config.textPart:
            Config.configParser.SetParameters("USER","text_part",self.textPartEdit.text())
            configChanged = True
        
        if self.eyeTrackerDataEdit.text() != Config.eyeTrackerData:
            Config.configParser.SetParameters("EYETRACKER","eye_tracker_data",self.eyeTrackerDataEdit.text())
            configChanged = True

        if self.eyeTrackerHeadDataEdit.text() != Config.eyeTrackerHeadData:
            Config.configParser.SetParameters("EYETRACKER","eye_tracker_head_data",self.eyeTrackerHeadDataEdit.text())
            configChanged = True

        if self.videoEdit.text() != Config.videoOut:
            Config.configParser.SetParameters("VIDEO","video_out",self.videoEdit.text())
            configChanged = True


        if self.glissadesEdit.text() != Config.eyeTrackerGlissades:
            Config.configParser.SetParameters("REPORT","eyeTracker_Glissades",self.glissadesEdit.text())
            configChanged = True

        if self.saccadesEdit.text() != Config.eyeTrackerSaccades:
            Config.configParser.SetParameters("REPORT","eyeTracker_Saccades",self.saccadesEdit.text())
            configChanged = True

        if self.fixationsEdit.text() != Config.eyeTrackerFixations:
            Config.configParser.SetParameters("REPORT","eyeTracker_Fixations",self.fixationsEdit.text())
            configChanged = True

        if self.velocityGazesEdit.text() != Config.eyeTrackerVelocityGazes:
            Config.configParser.SetParameters("REPORT","eyeTracker_VelocityGazes",self.velocityGazesEdit.text())
            configChanged = True

        if self.eyeTrackerScreenshotEdit.text() != Config.eyeTrackerScreenshot:
            Config.configParser.SetParameters("REPORT","eyeTracker_Screenshot",self.eyeTrackerScreenshotEdit.text())
            configChanged = True

        if self.wordScreenshotEdit.text() != Config.wordScreenshot:
            Config.configParser.SetParameters("REPORT","word_Screenshot",self.wordScreenshotEdit.text())
            configChanged = True

            

        Config.CONFIG_IMPORTED=False

        if  configChanged :
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Parameters saved")
            message.setWindowTitle("Parameters")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_()
            self.close()
        
            self.welcome = Welcome.Welcome()
            self.welcome.show()

        else :
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Parameters not saved because you didn't change parameters")
            message.setWindowTitle("Parameters")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_()
    
    
    def closeEvent(self, event):
         
        if self.closeCondition :
            print ("quit")
            if hasattr(self, "helpWindows"):
                self.helpWindows.close()
            if hasattr(self, "eyeTrackerWindows"):
                self.eyeTrackerWindows.close()
            if hasattr(self, "soundWindows"):
                self.soundWindows.close()
            if hasattr(self, "videoTestView"):
                try:
                    cv2.destroyAllWindows()
                except:
                    pass
                #self.videoTestView.stop()
            self.welcome = Welcome.Welcome()
            self.welcome.show()
        
        
    #help click
    def help_click(self):
        if Config.documentationHTML:
            helpHtml()
        else:
            self.helpWindows = Help()
            self.helpWindows.show()
 
def helpHtml():
    webbrowser.open_new_tab('file://'+str(Config.documentationParameters))
    
#help windows
class Help(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Help Windows')
        self.width=600
        self.height=200
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.Label = QtWidgets.QLabel("Here you can change the name of outputFile for audio, video , MCQ, eyeTracker ...\n\nYou can adjust the audio parameters also\n\nYou can test the Audio, Video or EyeTracker if you want\n")
        self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.Label,0,0)
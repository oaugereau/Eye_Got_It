#Simulation.py => config ans make a simulation. Select word not understand and answer to MCQ
#SimulationConfig class => config the simulation
#SimulationWindows => make simulation
#SelectWord => select words not understood
#Help => help windows for config simulation

import pyaudio
import wave
#import python Module
import sys, os, csv, time, shutil, threading, subprocess, random, webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui
import Config, Function, Audio, User, Mcq, Welcome, EyeTracker, ConfigFileManagement, Video, TextAdaptation
import audioop
import numpy as np
format = pyaudio.paInt16
from shutil import copyfile

#config the simulation
class SimulationConfig(QtWidgets.QWidget):

    def __init__(self,window):
        QtWidgets.QWidget.__init__(self)


        self.window=window
        self.askQuit=True


        #random simulation init
        self.randomSimulation = False
        self.randomLanguageSelect = False
        self.randomLevelSelect = False
   
        Config.userListCreate()#create user list
        Config.databaseListCreate()#create database list

        #windows config
        self.setWindowTitle("Simulation Init")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=1000
        self.height=600
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        #self.setMinimumSize(self.width, self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.grid.setColumnMinimumWidth(0,self.width/2)
        self.grid.setColumnMinimumWidth(1,self.width/2)
        self.grid.setRowMinimumHeight(0,self.height/3)
        self.grid.setRowMinimumHeight(1,self.height/3)
        self.grid.setRowMinimumHeight(2,self.height/3)

        #widgets

        #simulationGroupbox
        self.simulationGroupbox = QtWidgets.QGroupBox("Recording Configuration")
        self.simulationGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.simulationLayout = QtWidgets.QFormLayout()

        self.user = QtWidgets.QLabel("User",self)
        self.user.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.user, 3,0)

        #user section
        self.userEdit = QtWidgets.QComboBox(self)
        self.userEdit.addItems(Config.UsersList)
        self.userEdit.setCurrentIndex(-1)
        self.userEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.simulationLayout.addRow(self.user,self.userEdit)

        self.adduser = QtWidgets.QPushButton('Add User', self)
        self.adduser.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.adduser.clicked.connect(self.addUserFunction)
        self.simulationLayout.addRow(None,self.adduser)

        #database section
        self.database = QtWidgets.QLabel("Choose database",self)
        self.database.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.databaseEdit = QtWidgets.QComboBox(self)
        self.databaseEdit.addItems(Config.DatabaseList)
        self.databaseEdit.setCurrentIndex(-1)
        self.databaseEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.databaseEdit.currentIndexChanged[int].connect(self.on_currentIndexChangedDatabaseEdit)
        self.simulationLayout.addRow(self.database,self.databaseEdit)

        self.simulationGroupbox.setLayout(self.simulationLayout)

        self.grid.addWidget(self.simulationGroupbox,0,0)

        #Eye Tracker section
        #eyeTrackerGroupbox
        self.eyeTrackerGroupbox = QtWidgets.QGroupBox("Eye Tracker Configuration")
        self.eyeTrackerGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.eyetrackerLayout = QtWidgets.QFormLayout()

        self.allowEyeTracker = QtWidgets.QCheckBox("Allow")
        self.allowEyeTracker.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.allowEyeTracker, 2,2)
        self.allowEyeTracker.stateChanged.connect(self.checkBoxChangedActionAllowEyeTracker)
        self.allowEyeTracker.setChecked(False)
        self.eyetrackerLayout.addWidget(self.allowEyeTracker)

        self.eyeTrackerLabel = QtWidgets.QLabel("Input",self)
        self.eyeTrackerLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.eyeTrackerLabel, 2,0)

        self.eyeTrackerEdit = QtWidgets.QComboBox(self)
        self.eyeTrackerEdit.addItems(Config.eyeTrackerList)
        self.eyeTrackerEdit.setCurrentIndex(-1)
        self.eyeTrackerEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.eyeTrackerEdit, 2,1)
        self.eyeTrackerEdit.currentIndexChanged[int].connect(self.on_currentIndexChangedEyeTrackerEdit)
        self.eyeTrackerEdit.setEnabled(False)
        self.eyetrackerLayout.addRow(self.eyeTrackerLabel,self.eyeTrackerEdit)

        self.eyeTrackerCalibration = QtWidgets.QPushButton('Eye Tracker Test', self)
        self.eyeTrackerCalibration.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.eyetrackerLayout.addRow(None,self.eyeTrackerCalibration)
        self.eyeTrackerCalibration.clicked.connect(self.eyeTrackerTest_click)
        self.eyeTrackerCalibration.setEnabled(False)

        self.eyeTrackerGroupbox.setLayout(self.eyetrackerLayout)

        self.grid.addWidget(self.eyeTrackerGroupbox,0,1)

        #audio section
        #audioGroupbox
        self.audioGroupBox = QtWidgets.QGroupBox("Audio Configuration")
        self.audioGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.audioLayout = QtWidgets.QFormLayout()

        self.allowAudio = QtWidgets.QCheckBox("Allow")
        self.allowAudio.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.allowAudio, 0,2)
        self.allowAudio.stateChanged.connect(self.checkBoxChangedActionAllowAudio)
        self.allowAudio.setChecked(False)
        self.audioLayout.addWidget(self.allowAudio)

        self.inputText = QtWidgets.QLabel("Input :",self)
        self.inputText.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.inputText, 0,0)
        

        self.input = QtWidgets.QComboBox(self)
        self.input.addItems([])
        self.input.setCurrentIndex(-1)
        self.input.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.input, 0,1)
        self.input.currentIndexChanged[int].connect(self.on_currentIndexChangedInput)
        self.input.setEnabled(False)
        #self.inputSelect=False
        self.audioLayout.addRow(self.inputText,self.input)


        self.audioTest = QtWidgets.QPushButton('Audio Test', self)
        self.audioTest.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.audioLayout.addRow(None,self.audioTest)
        self.audioTest.clicked.connect(self.audioTest_click)
        self.audioTest.setEnabled(False)

        self.audioGroupBox.setLayout(self.audioLayout)

        self.grid.addWidget(self.audioGroupBox,1,0)

        #video section
        #videoGroupbox
        self.videoGroupBox = QtWidgets.QGroupBox("Video Configuration")
        self.videoGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.videoLayout = QtWidgets.QFormLayout()

        self.allowVideo = QtWidgets.QCheckBox("Allow")
        self.allowVideo.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.allowVideo, 1,2)
        self.allowVideo.stateChanged.connect(self.checkBoxChangedActionAllowVideo)
        self.allowVideo.setChecked(False)
        self.videoLayout.addWidget(self.allowVideo)

        self.videoText = QtWidgets.QLabel("Input",self)
        self.videoText.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.videoText, 1,0)

        self.videoEdit = QtWidgets.QComboBox(self)
        self.videoEdit.addItems([])
        self.videoEdit.setCurrentIndex(-1)
        self.videoEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.videoEdit, 1,1)
        self.videoEdit.currentIndexChanged[int].connect(self.on_currentIndexChangedVideoEdit)
        #self.videoEditSelect=False
        self.videoEdit.setEnabled(False)
        self.videoLayout.addRow(self.videoText,self.videoEdit)

        self.videoTest = QtWidgets.QPushButton('Video Test', self)
        self.videoTest.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.videoLayout.addRow(None,self.videoTest)
        self.videoTest.clicked.connect(self.videoTest_click)
        self.videoTest.setEnabled(False)
        self.videoGroupBox.setLayout(self.videoLayout)

        self.grid.addWidget(self.videoGroupBox,2,0)


        #random simulation section
        #randomGroupbox
        self.randomGroupbox = QtWidgets.QGroupBox("Random Text Selection")
        self.randomGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.randomLayout = QtWidgets.QFormLayout()

        self.randomCheck = QtWidgets.QCheckBox("Enable")
        self.randomCheck.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.randomLayout.addWidget(self.randomCheck)
        self.randomCheck.stateChanged.connect(self.checkBoxChangedActionRandomSimulation)
        self.randomCheck.setChecked(False)
        self.randomCheck.setEnabled(False)
        self.randomCheck.show()

        defaultNumberText = 2
        self.text = QtWidgets.QLabel(str(defaultNumberText),self)
        self.text.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.randomLayout.addWidget(self.text)
        self.text.hide()

        self.numberText = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.numberText.setTickPosition(QtWidgets.QSlider.TicksAbove)
        #self.numberText.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.numberText.setMinimum(1)
        self.numberText.setMaximum(10)
        self.numberText.setSingleStep(1)
        self.numberText.setTickInterval(1)
        self.numberText.setValue(defaultNumberText)
        self.randomLayout.addWidget(self.numberText)
        self.numberText.valueChanged.connect(lambda:self.text.setText(str(self.numberText.value())))
        self.numberText.hide()

        #languageGroupbox
        self.languageGroupbox = QtWidgets.QGroupBox("Language")
        self.languageGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.languageLayout = QtWidgets.QFormLayout()

        self.randomLanguage = QtWidgets.QCheckBox("Random Language")
        self.randomLanguage.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.languageLayout.addWidget(self.randomLanguage)
        self.randomLanguage.stateChanged.connect(self.checkBoxChangedActionRandomLanguage)
        self.randomLanguage.setChecked(False)
        #self.randomLanguage.hide()

        self.language = QtWidgets.QLabel("Language",self)
        self.language.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.randomLayout.addWidget(self.language, 2,0)
        #self.language.hide()

        
        self.languageSelect = QtWidgets.QComboBox(self)
        self.languageSelect.addItems([])
        self.languageSelect.setCurrentIndex(-1)
        self.languageSelect.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.randomLayout.addWidget(self.languageSelect, 2,1)
        #self.languageSelect.hide()
        self.languageLayout.addRow(self.language,self.languageSelect)

        self.languageGroupbox.setLayout(self.languageLayout)

        self.randomLayout.addWidget(self.languageGroupbox)
        self.languageGroupbox.hide()

        #levelGroupbox
        self.levelGroupbox = QtWidgets.QGroupBox("Level")
        self.levelGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.levelLayout = QtWidgets.QFormLayout()

        self.randomLevel = QtWidgets.QCheckBox("Random Level")
        self.randomLevel.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.randomLayout.addWidget(self.randomLevel, 3,2)
        self.randomLevel.stateChanged.connect(self.checkBoxChangedActionRandomLevel)
        self.randomLevel.setChecked(False)
        #self.randomLevel.hide()
        self.levelLayout.addWidget(self.randomLevel)

        self.level = QtWidgets.QLabel("Level",self)
        self.level.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.level.addWidget(self.level, 3,0)
        #self.level.hide()
        
        self.levelSelect = QtWidgets.QComboBox(self)
        self.levelSelect.addItems([])
        self.levelSelect.setCurrentIndex(-1)
        self.levelSelect.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.randomLayout.addWidget(self.levelSelect, 3,1)
        #self.levelSelect.hide()
        self.levelLayout.addRow(self.level,self.levelSelect)

        self.levelGroupbox.setLayout(self.levelLayout)

        self.randomLayout.addWidget(self.levelGroupbox)
        self.levelGroupbox.hide()

        self.randomGroupbox.setLayout(self.randomLayout)

        self.grid.addWidget(self.randomGroupbox,1,1,2,1)

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 3,0)
        self.back.clicked.connect(self.close)

        #validate config section
        self.ok = QtWidgets.QPushButton('OK', self)
        self.ok.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.ok, 3,1)
        self.ok.clicked.connect(self.ok_click)
        self.ok.setEnabled(True)


        #help section
        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 4,0)
        self.help.clicked.connect(self.help_click)
        self.help.setEnabled(True) 



    def addUserFunction(self):
        self.newUser = User.UserManagement("",True)
        self.newUser.finished.connect(self.refreshUserList)
        self.newUser.show()

    def refreshUserList(self):
        Config.userListCreate()
        self.userEdit.clear()
        self.userEdit.addItems(Config.UsersList)
        self.userEdit.setCurrentIndex(-1)
        #Function.UpdateComboBox(self.userEdit, Config.UsersList)


    #allow audio
    def checkBoxChangedActionAllowAudio(self, state):
        #audio get input
        Audio.getListAudioInput()#self.sound.getListAudioInput()

        if (QtCore.Qt.Checked == state):
            #self.inputSelect = False
            self.input.clear()
            self.input.addItems([])
            self.input.addItems(Config.audioInput)
            self.input.setCurrentIndex(-1)
            self.input.setEnabled(True)
            #print("Audio Selected.")
        else:
            #self.inputSelect = False
            self.input.clear()
            self.input.addItems([])
            self.input.setCurrentIndex(-1)
            self.input.setEnabled(False)
            #print("Audio Not Selected.")

    #audio select input
    def on_currentIndexChangedInput(self, index):
        
        if self.input.currentText() != "":

            self.audioTest.setEnabled(True)
                    

        else:
            #self.inputSelect=False
            self.audioTest.setEnabled(False)


    #allow video
    def checkBoxChangedActionAllowVideo(self, state):
        Video.getListVideoInput()
        if (QtCore.Qt.Checked == state):
            #self.videoEditSelect=False
            self.videoEdit.clear()
            self.videoEdit.addItems(Config.videoInput)
            self.videoEdit.setCurrentIndex(-1)
            self.videoEdit.setEnabled(True)
            #print("Video Selected.")
        else:
            #self.videoEditSelect=False
            self.videoEdit.clear()
            self.videoEdit.addItems([])
            self.videoEdit.setCurrentIndex(-1)
            self.videoEdit.setEnabled(False)
            #print("Video Not Selected.")

    def on_currentIndexChangedVideoEdit(self,index):
        if self.videoEdit.currentText() != "":
            #self.videoEditSelect = True
            self.videoTest.setEnabled(True)

        else:
            #self.videoEditSelect=False
            self.videoTest.setEnabled(False)

    #allow random simulation
    def checkBoxChangedActionRandomSimulation(self, state):
        if (QtCore.Qt.Checked == state) :
            #self.randomCheck.setText("Disable")
            if self.databaseEdit.currentText() !="":
                if Config.database.languageExist :
                    self.languageGroupbox.show()
                    #self.language.show()
                    #self.languageSelect.show()
                    #self.randomLanguage.show()

                if  Config.database.levelExist :
                    self.levelGroupbox.show()
                    #self.level.show()
                    #self.levelSelect.show()
                    #self.randomLevel.show()

                self.text.show()
                self.numberText.show()
                self.randomSimulation = True
                #print("random simulation enabled.")
        else: 
            #self.randomCheck.setText("Enable")          
            if self.databaseEdit.currentText() !=""   :
                self.text.hide()
                self.numberText.hide()
                self.languageGroupbox.hide()
                #self.language.hide()
                #self.languageSelect.hide()
                #self.randomLanguage.hide()
                self.levelGroupbox.hide()
                #self.level.hide()
                #self.levelSelect.hide()
                #self.randomLevel.hide()
                self.randomSimulation = False
                #print("random simulation disabled.")

    #random simulation choose language or random language
    def checkBoxChangedActionRandomLanguage(self, state):
        if (QtCore.Qt.Checked == state):
            self.randomLanguageSelect = True
            self.languageSelect.setCurrentIndex(-1)
            self.languageSelect.setEnabled(False)
            #print("random language enabled.")
        else:
            self.randomLanguageSelect = True
            self.languageSelect.setCurrentIndex(-1)
            self.languageSelect.setEnabled(True)
            #print("random language disabled.")

    #random simulation choose level or random level
    def checkBoxChangedActionRandomLevel(self, state):
        if (QtCore.Qt.Checked == state):
            self.randomLevelSelect = True
            self.levelSelect.setCurrentIndex(-1)
            self.levelSelect.setEnabled(False)
            #print("random level enabled.")
        else:
            self.randomLevelSelect = True
            self.levelSelect.setCurrentIndex(-1)
            self.levelSelect.setEnabled(True)
            #print("random level disabled.")

    #allow Eye Tracker
    def checkBoxChangedActionAllowEyeTracker(self, state):
        if (QtCore.Qt.Checked == state):
            self.eyeTrackerEdit.setCurrentIndex(-1)
            self.eyeTrackerEdit.setEnabled(True)
            #print("EyeTracker Selected.")
        else:
            self.eyeTrackerEdit.setCurrentIndex(-1)
            self.eyeTrackerEdit.setEnabled(False)            
            #print("EyeTracker Not Selected.")

    def on_currentIndexChangedEyeTrackerEdit(self,index):
        if self.eyeTrackerEdit.currentText() != "":
            self.eyeTrackerCalibration.setEnabled(True)

        else:
            self.eyeTrackerCalibration.setEnabled(False)

    #choose database
    def on_currentIndexChangedDatabaseEdit(self,index):
        if self.databaseEdit.currentText() != "":
            Config.CreateDatabase(self.databaseEdit.currentText())
            #self.randomCheck.show()
            self.randomCheck.setEnabled(True)

            Function.UpdateComboBox(self.languageSelect,Config.database.get(str("Language")))
            Function.UpdateComboBox(self.levelSelect,Config.database.get(str("Level")))

            if Config.database.languageExist and self.randomSimulation:
                self.languageGroupbox.show()
                #self.language.show()
                #self.languageSelect.show()
                #self.randomLanguage.show()
            else :
                self.languageGroupbox.hide()
                #self.language.hide()
                #self.languageSelect.hide()
                #self.randomLanguage.hide()

            if  Config.database.levelExist and self.randomSimulation:
                self.levelGroupbox.show()
                #self.level.show()
                #self.levelSelect.show()
                #self.randomLevel.show()
            else :
                self.levelGroupbox.hide()
                #self.level.hide()
                #self.levelSelect.hide()
                #self.randomLevel.hide()


        
    def audioTest_click(self):
        self.soundWindows = Audio.AudioTestDisplay(self.input.currentText())
        self.soundWindows.show()

    def videoTest_click(self):
        """
        if hasattr(self, "videoTestView"):
            self.videoTestView.stop()
        """
        self.videoTestView = Video.ThreadVideoTest(Config.videoInput.index(self.videoEdit.currentText()))      
        
        self.videoTestView.start()

    def eyeTrackerTest_click(self):
        self.eyeTrackerTest = EyeTracker.TestCalibrationWindows()
        self.eyeTrackerTest.show()
    #validate config
    def ok_click(self):
        if (self.userEdit.currentText() != "" and self.databaseEdit.currentText() != "" ) and ( (self.input.currentText() != "" or not self.allowAudio.isChecked()) and (self.videoEdit.currentText() != "" or not self.allowVideo.isChecked()) and (self.eyeTrackerEdit.currentText() != "" or not self.allowEyeTracker.isChecked())):
            
            Config.eyeTrackerSdkPro = True if (self.eyeTrackerEdit.currentText() == Config.eyeTrackerList[0]) else False
            videoIndex = Config.videoInput.index(self.videoEdit.currentText()) if (self.allowVideo.isChecked() and self.videoEdit.currentText() != "") else ""
            audioIndex = Config.audioInput.index(self.input.currentText()) if (self.allowAudio.isChecked() and self.input.currentText() != "") else ""

            if Config.database.languageExist and self.languageSelect.currentText() =="":
                self.randomLanguageSelect = True

            if Config.database.levelExist and self.levelSelect.currentText() =="":
                self.randomLevelSelect = True

            
            self.askQuit=False
            reply=QtWidgets.QMessageBox()
            reply.setIcon(QtWidgets.QMessageBox.Information)
            
            reply.setText("How to use simulation mod :\n"
                          "-Use Key 'Q' or 'A' to go to the previous page\n"
                          "-Use Key 'D' or 'E' to go to the next Pages\n"
                          "-Press the 'start recording' button to start the recording\n"
                          "-Press enter or click on the 'stop recording' button to stop the recording\n")
            
            reply.setWindowTitle("Simulation mod")
            reply.setStandardButtons(QtWidgets.QMessageBox.Ok)
            reply=reply.exec_()

            self.close()

            self.simul = SimulationWindows(self.userEdit.currentText(),audioIndex,videoIndex,self.window,self.allowAudio.isChecked(),self.allowVideo.isChecked(),self.allowEyeTracker.isChecked(),self.randomSimulation,self.randomLanguageSelect,self.randomLevelSelect,self.numberText.value(),self.languageSelect.currentText(),self.levelSelect.currentText())#SimulationWindows(self.userEdit.currentText(),self.sound.index,self.window)
        
            self.simul.show()
    
    #close windows
    def closeEvent(self, event):
        if self.askQuit:
            self.window.show()
        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

    #help
    def help_click(self):
        if Config.documentationHTML:
            helpHtml()
        else:
            self.helpWindows = Help()
            self.helpWindows.show()

def helpHtml():
    webbrowser.open_new_tab('file://'+str(Config.documentationSimulation))
    
#help windows for config simulation
class Help(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Help Windows')
        self.width=1366
        self.height=400
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        self.Label = QtWidgets.QLabel("-Allow your different devices to record by clicking on the checkbox\n\n"
                                      "-Select the audio and video recording device in the list\n\n"
                                      "-Select the user(data will be stored in this user file)\n\n"
                                      "-Select from wich database you want your text selection\n\n"
                                      "-You can check 'Random text selection'\nand it will generate a list of randomly selected text\n\n"
                                      "-Click on 'OK' to start the recording")
        self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.Label,0,0,2,1)

        try:
            with open(str(os.path.join(Config.PATH_IMAGE,"random_selection_example.jpg")),'r') as UseFile:
                pixmap = QtGui.QPixmap(str(os.path.join(Config.PATH_IMAGE,"random_selection_example.jpg")))
                self.example = QtWidgets.QLabel(self)                                                                                                                 
                self.example.setPixmap(pixmap)  
                self.grid.addWidget(self.example, 1,1) 
        except:
            #file no exist or no file chosen
            #self.MessageBox("Image error",str(location + " not found"),"warning","","","")
            pass
        
        self.exampleLabel = QtWidgets.QLabel("in the example below the list will contain 4 text in english with a random level")
        self.exampleLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.exampleLabel,0,1)


#make simulation Widgets in absolutes coordinates
class SimulationWindows(QtWidgets.QWidget):

    def __init__(self,userName,index,video,window,allowAudio,allowVideo, allowEyeTracker,randomSimulation,randomLanguageSelect,randomLevelSelect,numberText,languageSelect,levelSelect):
        QtWidgets.QWidget.__init__(self)
        self.textListSimul = []
        self.textSelectedSimul=""
        self.randomSimulation = randomSimulation 
        self.randomLanguageSelect = randomLanguageSelect
        self.randomLevelSelect = randomLevelSelect
        self.numberText = numberText
        self.languageSelect = languageSelect
        self.levelSelect = levelSelect
        self.userName=userName
        self.index=index

        #user agreement
        self.allowAudio = allowAudio
        self.videoIndex = video
        self.allowVideo = allowVideo
        self.allowEyeTracker = allowEyeTracker

        #random mode text selection
        titleTemp = []
        if self.randomSimulation:
            i=0
            error = 0
            while i < self.numberText:

                if Config.database.languageExist:
                    if self.randomLanguageSelect:
                        language = str(Config.database.get(str("Language"))[random.randint(0,len(Config.database.get(str("Language")))-1)])
                    else :
                        language = self.languageSelect
                    
                if Config.database.levelExist:
                    if self.randomLevelSelect:
                        level = str(Config.database.get(str("Level"))[random.randint(0,len(Config.database.get(str("Level")))-1)])
                    else :
                        level = self.levelSelect
                    
                try:
                    if Config.database.languageExist and Config.database.levelExist :
                        text = Config.database.get((str(language + "_" + level)))[random.randint(0,len(Config.database.get(str(language + "_" + level)))-1)]
                    if Config.database.languageExist and not Config.database.levelExist :
                        #print("language")
                        text = Config.database.get((str(language)))[random.randint(0,len(Config.database.get(str(language)))-1)]
                    if not Config.database.languageExist and Config.database.levelExist :
                        #print("level")
                        text = Config.database.get((str(level)))[random.randint(0,len(Config.database.get(str(level)))-1)]
                    if not Config.database.languageExist and not Config.database.levelExist :
                        #print("text")
                        text = Config.database.get((str("Text")))[random.randint(0,len(Config.database.get(str("Text")))-1)]
                    
                    if text not in titleTemp:
                        titleTemp.append(text)
                        self.textListSimul.append(text)
                        i+=1
                
                    else :
                        error += 1
                except:
                    error += 1

                if error > 100 :
                    break

        self.currentText=""
        self.recording=False # simulation not started
        self.textDisplay = False #text not display
        self.word_tab=[]
        self.page_tab=[]
        self.timePage=[]
        self.page=0 #display first page
        self.rect=QtCore.QRect()#only used in debug mode
        self.window=window
        
        #windows config
        self.setWindowTitle("Simulation")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setGeometry(Config.SCREEN_WIDTH/2-Config.SCREEN_WIDTH_SIMULATION/2,Config.SCREEN_HEIGHT/2-Config.SCREEN_HEIGHT_SIMULATION/2,Config.SCREEN_WIDTH_SIMULATION,Config.SCREEN_HEIGHT_SIMULATION)
        self.setFixedSize(Config.SCREEN_WIDTH_SIMULATION,Config.SCREEN_HEIGHT_SIMULATION)

        #widgets => absolute coordinate 
        self.start = QtWidgets.QPushButton('start recording', self)
        self.start.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: green" +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.start.setGeometry(0, 0, 200, 30)
        self.start.clicked.connect(self.start_click)
        self.start.setEnabled(False)

        self.stop = QtWidgets.QPushButton('stop recording', self)
        self.stop.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color:  " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.stop.setGeometry(200, 0, 200, 30)
        self.stop.clicked.connect(lambda:self.endSimulation(True))
        self.stop.setEnabled(False)

        self.calibrate = QtWidgets.QPushButton('Eye Tracker Test Calibration', self)
        self.calibrate.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.calibrate.setGeometry(400, 0, 300, 30)
        self.calibrate.clicked.connect(self.eyeTrackerTest_click)
        self.calibrate.setEnabled(True)
        if not self.allowEyeTracker :
            self.calibrate.hide()

        self.userLabel = QtWidgets.QLabel(str("User : " + self.userName),self)
        self.userLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.userLabel.setGeometry(710,0, 490, 30)

        self.recordingDisplay = QtWidgets.QLabel("Recording",self)
        self.recordingDisplay.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str("red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.recordingDisplay.setGeometry(1200,0, 100, 30)
        self.recordingDisplay.hide()

        self.choiceLabel = QtWidgets.QLabel(self)
        self.choiceLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                    "background-color: " + str(Config.colorFont) +";"
                    "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                    "selection-color: "+ str("") +";" + "}")
        self.choiceLabel.setGeometry(0,30, 500, 30)

        if not self.randomSimulation:
            
            if Config.database.languageExist:
                language = Config.database.get("Language")

                self.languageList = QtWidgets.QComboBox(self)
                self.languageList.addItems(language)
                self.languageList.setCurrentIndex(-1)
                self.languageList.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
                self.languageList.setGeometry(500, 30, 200, 30)
                self.languageList.activated.connect(self.language_select)
                self.languageList.setEnabled(True)

            if Config.database.levelExist:
                level = []
                if Config.database.levelExist and not Config.database.languageExist:
                    level = Config.database.get("Level")

                self.levelList = QtWidgets.QComboBox(self)
                self.levelList.addItems(level)
                self.levelList.setCurrentIndex(-1)
                self.levelList.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
                self.levelList.setGeometry(700, 30, 200, 30)
                self.levelList.activated.connect(self.level_select)
                if Config.database.levelExist and not Config.database.languageExist:
                    self.levelList.setEnabled(True)
                else:
                    self.levelList.setEnabled(False)
            
            if Config.database.languageExist and not Config.database.levelExist :
                self.choiceLabel.setText("choose Language and the text :")

            if not Config.database.languageExist and Config.database.levelExist :
                self.choiceLabel.setText("choose the difficulty level and the text :")

            if Config.database.languageExist and Config.database.levelExist :
                self.choiceLabel.setText("choose Language, the difficulty level and the text :")
        else :
            self.choiceLabel.setText("choose text :")

        if not randomSimulation and not Config.database.levelExist and not Config.database.languageExist:
            self.textListSimul = Config.database.get("Text")
            self.choiceLabel.setText("choose text :")

        self.textList = QtWidgets.QComboBox(self)
        self.textList.addItems(self.textListSimul)#(["3d-indoormap.en.0.txt"])
        self.textList.setCurrentIndex(-1)
        self.textList.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.textList.setGeometry(900, 30, 300, 30)
        self.textList.activated.connect(lambda:self.select.setEnabled(True))

        if not self.randomSimulation and (Config.database.levelExist or Config.database.languageExist):
            
            self.textList.setEnabled(False)
        else :
            self.textList.setEnabled(True)

        self.textLabel = QtWidgets.QTextEdit("",self)
        self.textLabel.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSizeText)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.textLabel.setGeometry(0, 60, Config.SCREEN_WIDTH_SIMULATION, Config.SCREEN_HEIGHT_SIMULATION-60)
        self.textLabel.setReadOnly(True)
        self.textLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.select = QtWidgets.QPushButton('select', self)
        self.select.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.select.setGeometry(1200, 30, 100, 30)
        self.select.clicked.connect(lambda:self.select_click(self.textList.currentText()))
        self.select.setEnabled(False)

        self.displayPage = QtWidgets.QLabel(self)
        self.displayPage.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.displayPage.setGeometry(1050,0, 150, 30)
        self.displayPage.hide()

        self.sessionTime= str(Config.currentDate() + Config.currentTime())
        Config.SAVE_DATA_MAIN_FOLDER=str(os.path.join(Config.UsersFolder,self.userName,str(Config.currentDate() + Config.currentTime()) ))
        self.popup = popupStartSimulation()

    def eyeTrackerTest_click(self):
        self.eyeTrackerTest = EyeTracker.TestCalibrationWindows()
        self.eyeTrackerTest.show()
    def language_select(self):

        if Config.database.levelExist :
            level_contents=Config.database.get("Level")#Config.database.get(str(self.languageList.currentText() + "_level"))
            Function.UpdateComboBox(self.levelList,level_contents)
            Function.UpdateComboBox(self.textList,[])
            self.levelList.setEnabled(True)
        else :
            text_contents=Config.database.get(self.languageList.currentText())#Config.database.get(str(self.languageList.currentText() + "_level"))
            Function.UpdateComboBox(self.textList,text_contents)
            self.textList.setEnabled(True)

    def level_select(self):
        if Config.database.languageExist:
            text_contents=Config.database.get(str(self.languageList.currentText() + "_" + self.levelList.currentText()))
            Function.UpdateComboBox(self.textList,text_contents)
            self.textList.setEnabled(True)

        else :
            text_contents=Config.database.get(str(self.levelList.currentText()))
            Function.UpdateComboBox(self.textList,text_contents)
            self.textList.setEnabled(True)

    def select_click(self,text):
        Config.TXT_IMPORT=os.path.join(Config.DatabaseFolder,Config.databaseName,Config.database.folder,self.textList.currentText())
  
        with open(str(Config.TXT_IMPORT), 'r',encoding='utf-8',errors='ignore') as f:
            self.currentText=f.read()
            self.textLabel.setText(self.currentText)
            f.close()
        
        metrics=self.textLabel.fontMetrics()
        text=self.textLabel.toPlainText()
        width=self.textLabel.width()
        height=self.textLabel.height()
        self.word_tab,self.page_tab=TextAdaptation.textAdaptation(metrics,text,width,height)
        self.page=0
        self.textLabel.setText(self.page_tab[self.page])
        self.displayPage.show()
        self.displayPage.setText(str( "Page " + str(self.page + 1) + " / " + str(len(self.page_tab))))
        self.start.setEnabled(True) 
        self.sliderEdit=True
        self.textDisplay=True
        if self.randomSimulation:
            self.textSelectedSimul = self.textList.currentText()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return and self.recording: 
            #print("enter pressed")
            self.endSimulation(True)
        
        if (event.key() == QtCore.Qt.Key_F4 or event.key() == QtCore.Qt.Key_D or event.key() == QtCore.Qt.Key_E)and self.textDisplay:
            self.nextPage()

        if (event.key() == QtCore.Qt.Key_F3 or event.key() == QtCore.Qt.Key_Q or event.key() == QtCore.Qt.Key_A) and self.textDisplay and not self.recording:
            self.previousPage()

        if Config.DEBUG:#display word coordinayes : only in debug
            if event.key() == QtCore.Qt.Key_F1:
                self.textLabel.hide() 
            if event.key() == QtCore.Qt.Key_F2:
                self.textLabel.show()
        
        event.accept()

    #display next page
    def nextPage(self):
        if self.page < len(self.page_tab)-1:
            if self.recording:
                self.timePage.append(Function.current_milli_time() )
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.winId())
                screenshot.save(os.path.join(Config.SAVE_DATA_FOLDER,str(Config.screenshotName +"_"+str(self.page)+ "."+Config.screenshotExtension)), str(Config.screenshotExtension))
                self.page+=1
                self.textLabel.setText(self.page_tab[self.page])
                self.displayPage.setText(str( "Page " + str(self.page + 1) + " / " + str(len(self.page_tab))))

            else:    
                self.page+=1
                self.textLabel.setText(self.page_tab[self.page])
                self.displayPage.setText(str( "Page " + str(self.page + 1) + " / " + str(len(self.page_tab))))
           
        #print("right pressed")

    #display previous page (not allow when start the simulation)
    def previousPage(self):
        if self.page > 0:
            self.page-=1
            self.textLabel.setText(self.page_tab[self.page])
            self.displayPage.setText(str( "Page " + str(self.page + 1) + " / " + str(len(self.page_tab))))
        #print("left pressed")

    #start the simulation
    def start_click(self):
        self.hide()
        self.popup.show()
        self.textLabel.setText("")
        self.timePage=[]
        self.recording=True
        self.select.setEnabled(False)
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        self.calibrate.setEnabled(False)
        if not self.randomSimulation:
            if Config.database.languageExist:
                self.languageList.setEnabled(False)
                Function.UpdateComboBox(self.languageList,Config.database.get("Language"))
            if Config.database.levelExist:
                self.levelList.setEnabled(False)
                if Config.database.languageExist:
                    Function.UpdateComboBox(self.levelList,[])
                else:
                    Function.UpdateComboBox(self.levelList,Config.database.get("Level"))

        self.textList.setEnabled(False)
        
        if not self.randomSimulation and (Config.database.levelExist and Config.database.languageExist):
            Function.UpdateComboBox(self.textList,[])

        elif not self.randomSimulation and (Config.database.levelExist and not Config.database.languageExist):
            Function.UpdateComboBox(self.textList,[])

        elif not self.randomSimulation and (not Config.database.levelExist and Config.database.languageExist):
            Function.UpdateComboBox(self.textList,[])
        
        elif not self.randomSimulation and (not Config.database.levelExist and Config.database.languageExist):
            Function.UpdateComboBox(self.textList,[])
        
        elif not self.randomSimulation and (not Config.database.levelExist and not Config.database.languageExist):
            Function.UpdateComboBox(self.textList,Config.database.get("Text"))

        Config.SAVE_DATA_FOLDER=str(os.path.join(Config.UsersFolder,self.userName,str(Config.SAVE_DATA_MAIN_FOLDER),str(Config.currentDate() + Config.currentTime()) ))
        
        if not os.path.isdir(Config.SAVE_DATA_MAIN_FOLDER):
            os.makedirs(Config.SAVE_DATA_MAIN_FOLDER)

        if not os.path.isdir(Config.SAVE_DATA_FOLDER):
            os.makedirs(Config.SAVE_DATA_FOLDER)
        """
        try :
            os.makedirs(os.path.join(Config.UsersFolder,self.userName,str(Config.SAVE_DATA_MAIN_FOLDER)))
        except:
            pass

        try:
            os.makedirs(Config.SAVE_DATA_FOLDER)
        except:
            pass
        """
       
        self.recordingDisplay.show()
        
        if self.allowEyeTracker:
            saveCSV = os.path.join(Config.SAVE_DATA_FOLDER,str(Config.eyeTrackerData+"."+(Config.eyeTrackerDataFile)))
            saveCSV = str('"' + saveCSV + '"')
            saveCSV2 = os.path.join(Config.SAVE_DATA_FOLDER,str(Config.eyeTrackerHeadData+"."+(Config.eyeTrackerDataFile)))
            saveCSV2 = str('"' + saveCSV2 + '"')
            self.eyeTrackerThread=EyeTracker.EyeTrackerRecordThread(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT,saveCSV,saveCSV2)
            self.eyeTrackerThread.start()
        
        if self.allowVideo:
            self.videoThread = Video.ThreadVideoRecord(self.videoIndex,640,480,os.path.join(Config.SAVE_DATA_FOLDER,Config.videoOut))
            self.videoThread.start()
        if self.allowAudio:
            self.audioThread = Audio.ThreadAudioRecord(os.path.join(Config.SAVE_DATA_FOLDER,str(Config.soundOut)),self.index)
            self.audioThread.start()

        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(5000,loop.quit)
        loop.exec_()
        print("start simulation")
        self.timeStart=Function.current_milli_time() 
        if self.allowVideo:
            self.videoThread.startRecord()
        
        if self.allowAudio:
            self.audioThread.startRecord()
        self.popup.hide()  
        self.show()   
            
        self.timePage.append(self.timeStart)
        self.page=0
        self.textLabel.setText(self.page_tab[self.page])
        self.displayPage.show()
        self.displayPage.setText(str( "Page " + str(self.page + 1) + " / " + str(len(self.page_tab))))

    #stop Simulation
    def endSimulation(self,condition):
        print("end simulation")
        timeStop=Function.current_milli_time()
        #####################################
        #
        #
        # Added text file to simulation folder
        #
        #
        ######################################

        shutil.copyfile(os.path.join(Config.TXT_IMPORT), os.path.join(Config.SAVE_DATA_FOLDER, "file.txt"))

        #####################################
        #
        #
        # Added text file to simulation folder
        #
        #
        ######################################

        self.timePage.append(Function.current_milli_time())
        if self.allowVideo:
            self.videoThread.stopRecord()
        if self.allowAudio:   
            self.audioThread.close() 
        if self.allowEyeTracker:
            self.eyeTrackerThread.stop()
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())#screen.grabWindow(QtWidgets.QApplication.desktop().winId(), 0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        screenshot.save(os.path.join(Config.SAVE_DATA_FOLDER,str(Config.screenshotName +"_"+str(self.page)+ "."+Config.screenshotExtension)), str(Config.screenshotExtension))
        self.displayPage.hide()

        if not self.randomSimulation:
            if Config.database.languageExist:
                self.languageList.setEnabled(True)
            if Config.database.levelExist and Config.database.languageExist:
                self.levelList.setEnabled(False)
            if Config.database.levelExist :
                self.levelList.setEnabled(True)
        
        if not self.randomSimulation and (Config.database.levelExist or Config.database.languageExist):
            self.textList.setEnabled(False)
        else :
            self.textList.setEnabled(True)
        self.select.setEnabled(False)
        self.start.setEnabled(False)
        self.stop.setEnabled(False)
        self.calibrate.setEnabled(True)
        self.recording=False
        self.textDisplay = False

        self.recordingDisplay.hide()

        if self.randomSimulation:
            self.textListSimul.pop(self.textListSimul.index(self.textSelectedSimul))
            Function.UpdateComboBox(self.textList,self.textListSimul)
    
        self.textLabel.setText("")
        configSimulation = ConfigFileManagement.ConfigFileWrite()
        configSimulation.Add_Section("Time")
        configSimulation.Add_Section("System")
        configSimulation.Add_Section("Text")
        configSimulation.Add_Section("User")
        configSimulation.SetParameters("Time","time",','.join(map(str, self.timePage)))
        configSimulation.SetParameters("Time","audio",Config.audioUNIXStart)
        configSimulation.SetParameters("Time","video",Config.videoUNIXStart)
        configSimulation.SetParameters("System","screen_width",Config.SCREEN_WIDTH)
        configSimulation.SetParameters("System","screen_height",Config.SCREEN_HEIGHT)
        configSimulation.SetParameters("System","x0",int(Config.SCREEN_WIDTH/2-Config.SCREEN_WIDTH_SIMULATION/2))
        configSimulation.SetParameters("System","y0",int(Config.SCREEN_HEIGHT/2-Config.SCREEN_HEIGHT_SIMULATION/2))
        if self.allowEyeTracker:
            configSimulation.SetParameters("System","eyeTracker",str(Config.eyeTrackerList[0] if Config.eyeTrackerSdkPro else Config.eyeTrackerList[1]))
        else :
            configSimulation.SetParameters("System","eyeTracker","")
        configSimulation.SetParameters("System","rate",Config.rate)
        configSimulation.SetParameters("System","channels",Config.channels)
        configSimulation.SetParameters("System","chunk",Config.chunk)
        configSimulation.SetParameters("System","sound_out",Config.soundOut)
        configSimulation.SetParameters("System","videoOut",Config.videoOut)
        configSimulation.SetParameters("System","mcq_answer",Config.mcqAnswer)
        configSimulation.SetParameters("System","text_position",Config.textPosition)
        configSimulation.SetParameters("System","text_part",Config.textPart)
        configSimulation.SetParameters("System","eye_tracker_head_data",Config.eyeTrackerHeadData)
        configSimulation.SetParameters("System","eye_tracker_data",Config.eyeTrackerData)
        configSimulation.SetParameters("System","screenshot_name",Config.screenshotName)
        
        configSimulation.SetParameters("System","eyeTrackerGlissades",Config.eyeTrackerGlissades)
        configSimulation.SetParameters("System","eyeTrackerSaccades",Config.eyeTrackerSaccades)
        configSimulation.SetParameters("System","eyeTrackerFixations",Config.eyeTrackerFixations)
        configSimulation.SetParameters("System","eyeTrackerVelocityGazes",Config.eyeTrackerVelocityGazes)
        configSimulation.SetParameters("System","eyeTrackerScreenshot",Config.eyeTrackerScreenshot)
        configSimulation.SetParameters("System","wordScreenshot",Config.wordScreenshot)
        
        configSimulation.SetParameters("Text","title",os.path.split(Config.TXT_IMPORT)[1])
        configSimulation.SetParameters("Text","page",self.page+1)
        configSimulation.SetParameters("User","audio",self.allowAudio)
        configSimulation.SetParameters("User","video",self.allowVideo)
        configSimulation.SetParameters("User","eyeTracker",self.allowEyeTracker)
        configSimulation.CreateFile(os.path.join(Config.SAVE_DATA_FOLDER,'config.ini'))

        textName=os.path.split(Config.TXT_IMPORT)[1]
        textPositionCsv=str(Config.textPosition +".csv")#str('textPosition.csv')
        with open(str(os.path.join(Config.SAVE_DATA_FOLDER,textPositionCsv)), 'w', newline='') as csvfile:
            textPosition = csv.writer(csvfile,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            textPosition.writerow([textName])
            textPosition.writerow(["word","x","y","width","height","page"])
            for i in range(0,len(self.word_tab)):
                try:
                    textPosition.writerow([self.word_tab[i][0],self.word_tab[i][1],self.word_tab[i][2],self.word_tab[i][3],self.word_tab[i][4],self.word_tab[i][5]])
                except:
                    pass 
            csvfile.close()

        if condition :
            if self.randomSimulation and len(self.textListSimul)==0:
                self.close()
            
            self.save_windows=SelectWord(self.currentText,self.userName)#self.currentText
            self.save_windows.show()

    #auto replace the windows in center of the screen and default windows size
    def moveEvent(self, event):
        self.setGeometry(Config.SCREEN_WIDTH/2-Config.SCREEN_WIDTH_SIMULATION/2,Config.SCREEN_HEIGHT/2-Config.SCREEN_HEIGHT_SIMULATION/2,Config.SCREEN_WIDTH_SIMULATION,Config.SCREEN_HEIGHT_SIMULATION)

    #close windows
    def closeEvent(self, event):
        if self.recording:
            reply=QtWidgets.QMessageBox()
            reply.setIcon(QtWidgets.QMessageBox.Question)
            reply.setText("Are you sure you want to exit the simulation ?")
            reply.setWindowTitle("Quit Simulation")
            reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            reply=reply.exec_()
            if reply == QtWidgets.QMessageBox.Yes:
                self.endSimulation(False)
                self.window.show()
                event.accept()
            else:
                event.ignore()
        else :
            self.window.show()
            
    def back_click(self):
        self.close()
   
    #display word position in debug mode (check keyPressEvent function for keyboard )
    def paintEvent(self, event): # event de type QPaintEvent
        if Config.DEBUG:
            painter = QtGui.QPainter(self) # recupere le QPainter du widget
            painter.setPen(QtGui.QColor(168, 34, 3))
            for i in range (0,len(self.word_tab)):
                if self.word_tab[i][5]==self.page:
                    self.rect=QtCore.QRect(self.word_tab[i][1],self.word_tab[i][2],self.word_tab[i][3],self.word_tab[i][4])
                painter.drawRect(self.rect) # dessiner un rectangle noir

#popupStartSimulation       
class popupStartSimulation(QtWidgets.QWidget):
    def __init__(self):
            QtWidgets.QWidget.__init__(self)  

            #windows config
            self.setStyleSheet("background-color:"+ str(Config.background)+";")
            self.setWindowTitle('Initialisation')
            self.width=300
            self.height=300
            self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

            self.grid=QtWidgets.QGridLayout()
            self.setLayout(self.grid)

            #widgets
            self.Label = QtWidgets.QLabel("Start Simulation\nPlease wait\n",self)
            self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";" + "}")
            self.grid.addWidget(self.Label,0,0)

            self.adjustSize()

#select words not understood       
class SelectWord(QtWidgets.QWidget):
    
    def __init__(self,currentText,user):
        QtWidgets.QWidget.__init__(self)
        self.textPart=[]
        self.userName=user

        #windows config 
        self.setWindowTitle("SaveData")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=1500
        self.height=700
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.showMaximized()
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        self.instructionLabel = QtWidgets.QLabel("select a part of the text you didn't understand and click on add",self)
        self.instructionLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.instructionLabel,0,0)
        
        self.textSelected = QtWidgets.QTextEdit(self)
        self.textSelected.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSizeText)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.textSelected,1,0,1,3)
        self.textSelected.setReadOnly(True)
        self.textSelected.setText(currentText)
        
        self.add = QtWidgets.QPushButton('Add Word', self)
        self.add.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.add,0,1)
        self.add.clicked.connect(self.add_click)

        self.remove = QtWidgets.QPushButton('Remove Word', self)
        self.remove.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.remove,0,2)
        self.remove.clicked.connect(self.delete_click)

        self.save = QtWidgets.QPushButton('Save', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.save,2,0)
        self.save.clicked.connect(self.save_click)

    #add word
    def add_click(self):
        cursor = self.textSelected.textCursor()
        fmt = QtGui.QTextCharFormat()
        
        if (cursor.hasSelection()):
            t=cursor.selectedText()
            t = t.replace('\u2029',' ')
            t = t.replace('\ufeff','')
            
            if t not in self.textPart:
                self.textPart.append(t)
                fmt.setBackground(QtCore.Qt.yellow)
                cursor.setCharFormat(fmt)
            #else:
            #    fmt.setBackground(QtCore.Qt.red)
            #    cursor.setCharFormat(fmt)

    def delete_click(self):
        cursor = self.textSelected.textCursor()
        fmt = QtGui.QTextCharFormat()
        
        if (cursor.hasSelection()):
            t=cursor.selectedText()
            t = t.replace('\u2029',' ')
            t = t.replace('\ufeff','')
            
            if t in self.textPart:
                del self.textPart[self.textPart.index(t)]
                fmt.setBackground(QtCore.Qt.white)
                cursor.setCharFormat(fmt)
            #else:
            #    fmt.setBackground(QtCore.Qt.red)
            #    cursor.setCharFormat(fmt)
        
        #print(self.textPart)

    #save words 1
    def save_click(self):
        
        if self.textPart == []:
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("No words have been selected do you want to continue anyway? ")
            message.setWindowTitle("Save word selected")
            message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            message=message.exec_()
            if message == QtWidgets.QMessageBox.Yes:
                self.saveWord(False)
        else :
            self.saveWord(True)

    #save word 2
    def saveWord(self,condition):
        #textName=os.path.split(Config.TXT_IMPORT)[1]
        textName=os.path.split(Config.TXT_IMPORT)[1]
        textName=os.path.splitext(Config.TXT_IMPORT)[0]
        mcq=str(textName+'.csv')
        mcq=os.path.join(os.path.split(Config.TXT_IMPORT)[0],mcq)
        if condition:
            textPartFile=str(Config.textPart+".txt")#str('textPart.txt') 
            txtfile=open(str(os.path.join(Config.SAVE_DATA_FOLDER,textPartFile)), 'w', newline='') 
            txtfile.writelines(str(textName + os.linesep))
            for i in self.textPart:
                try:
                    txtfile.writelines(str(str(i) + os.linesep))
                except:
                    pass
            txtfile.close()
        if os.path.isfile(mcq):
            reply=QtWidgets.QMessageBox()
            reply.setIcon(QtWidgets.QMessageBox.Question)
            reply.setText("Do you want to answer question about the text ?")
            reply.setWindowTitle("Mcq")
            reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            reply=reply.exec_()
            if reply == QtWidgets.QMessageBox.Yes:
                self.mcq = Mcq.Mcq(self.userName,mcq)
                self.mcq.show()
                self.mcq.finishedMcq.connect(self.close)
                self.save.setEnabled(False)
                self.add.setEnabled(False)
            else:
                self.close()
        else:
            self.close()
        


#report.py => data processing and generate report
#ReportDisplay class => 
#CreateReport def => get all simulation parameters
#ReportProcess => reprt process
#CopieFile def => copy file in report folder
#ReportWord class => display word coordinates and save them
#Help class => help windows

#import python Module
import sys, os, csv, time, shutil, threading, subprocess, webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.Qt import *
import Config, Function, Audio, User, Mcq, Welcome, EyeTracker, ConfigFileManagement, Video,VelocityInDeg, Buscher, Nystrom, MachineLearning
import cv2, datetime
import EVSGeneration
import csv

reportConfig = ""#all simulation parameters see CreateReport class

#Main report windows
class ReportDisplay(QtWidgets.QWidget):
    
    ############################################################################################################
    #
    #
    # 
    ## WIDGETS
    #
    #
    #
    ############################################################################################################

    def __init__(self,windows):
        QtWidgets.QWidget.__init__(self)
        
        self.windows=windows
        self.windows.hide()
        self.algorithm=[]
        Config.userListCreate()

        #windows config
        self.setWindowTitle("Report Init")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=1000
        self.height=300
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets

        #reportGroupbox
        self.reportGroupBox = QtWidgets.QGroupBox("Configuration")
        self.reportGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.reportLayout = QtWidgets.QFormLayout()

        self.user = QtWidgets.QLabel("User",self)
        self.user.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.user, 0,0)

        self.userEdit = QtWidgets.QComboBox(self)
        self.userEdit.addItems(Config.UsersList)
        self.userEdit.setCurrentIndex(-1)
        self.userEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.userEdit, 0,1)
        self.reportLayout.addRow(self.user, self.userEdit)
        self.userEdit.activated.connect(self.activatedUserEdit)

        self.simulationMain = QtWidgets.QLabel("Session",self)
        self.simulationMain.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.simulationMainEdit = QtWidgets.QComboBox(self)
        self.simulationMainEdit.addItems([])
        self.simulationMainEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.simulationMainEdit, 1,1)
        self.simulationMainEdit.activated.connect(self.activatedSimulationMainEdit)
        self.reportLayout.addRow(self.simulationMain, self.simulationMainEdit)

        self.simulation = QtWidgets.QLabel("Recording",self)
        self.simulation.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.simulation, 1,0)

        self.simulationEdit = QtWidgets.QComboBox(self)
        self.simulationEdit.addItems([])
        self.simulationEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.reportLayout.addRow(self.simulation, self.simulationEdit)

        self.allSimulation = QtWidgets.QCheckBox("Process All Records")
        self.allSimulation.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.allSimulation.setChecked(False)
        self.reportLayout.addRow(None,self.allSimulation)
        self.allSimulation.setEnabled(False) 
        self.allSimulation.stateChanged.connect(self.checkBoxChangedActionAllSimulation)


        #choose Eye tracker algorithm (default Buscher)
        if not Config.onlyBuscher :
            self.algoLabel = QtWidgets.QLabel("Choose algorithm",self)
            self.algoLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";" + "}")
            #self.grid.addWidget(self.algoLabel, 3,0)

            self.algo = QtWidgets.QComboBox(self)
            self.algo.addItems(Config.eyeTrackerAlgorithm)
            self.algo.setCurrentIndex(-1)
            self.algo.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";" + "}")
            #self.grid.addWidget(self.algo, 3,1)
            self.algo.currentIndexChanged[int].connect(self.on_currentIndexAlgo)
            self.reportLayout.addRow(self.algoLabel,self.algo)

            self.allAlgorithm = QtWidgets.QCheckBox("All Algorithm")
            self.allAlgorithm.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";" + "}")
            self.allAlgorithm.setChecked(False)
            self.reportLayout.addRow(None,self.allAlgorithm)
            #self.eyeTracker.setEnabled(False) 
            self.allAlgorithm.stateChanged.connect(self.checkBoxChangedActionAllAlgorithm)

        else :
            self.algorithm=["buscher"]
        self.reportGroupBox.setLayout(self.reportLayout)

        self.grid.addWidget(self.reportGroupBox,0,0)


        #dataGroupbox
        self.dataGroupbox = QtWidgets.QGroupBox("Data Processing")
        self.dataGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.dataLayout = QtWidgets.QFormLayout()


        self.audio = QtWidgets.QCheckBox("Audio")
        self.audio.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.audio.setChecked(True)
        self.audio.clicked.connect(self.checkBoxChangedEyeTracker)
        self.dataLayout.addRow(self.audio)
        self.audio.setEnabled(True)
        #self.audio.hide() 


        self.eyeTracker = QtWidgets.QCheckBox("Eye Tracker")
        self.eyeTracker.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.eyeTracker.clicked.connect(self.checkBoxChangedEyeTracker)
        self.dataLayout.addRow(self.eyeTracker)
        self.eyeTracker.setChecked(False)

        self.video = QtWidgets.QCheckBox("Video")
        self.video.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.video.setChecked(True)
        self.dataLayout.addRow(self.video)
        #self.video.setEnabled(False) 

        self.actionUnit = QtWidgets.QCheckBox("Detect Action Unit in Video")
        self.actionUnit.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.actionUnit.setChecked(False)
        #self.dataLayout.addWidget(self.actionUnit)

        self.checkActionUnit = QtWidgets.QPushButton("Check Action Units")
        self.checkActionUnit.setStyleSheet("QPushButton" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        self.checkActionUnit.setEnabled(True)
        self.checkActionUnit.clicked.connect(self.checkActionUnit_click)
        self.dataLayout.addRow(self.actionUnit,self.checkActionUnit)

        self.dataGroupbox.setLayout(self.dataLayout)

        self.grid.addWidget(self.dataGroupbox,0,1)

        #extraGroupbox
        self.extraGroupbox = QtWidgets.QGroupBox("Post processing")
        self.extraGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.extraLayout = QtWidgets.QFormLayout()

        ############################################################################################################
        ## EVS variation Widget
        ############################################################################################################
         
        self.evs = QtWidgets.QCheckBox("EVS Generation")
        self.evs.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.extraLayout.addRow(self.evs)
        self.evs.setEnabled(False)

        ############################################################################################################
        ## EVS variation Widget
        ############################################################################################################
         
        #choose machine learning model
        self.modelCheck = QtWidgets.QCheckBox("Machine Learning")
        self.modelCheck.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.modelCheck.setChecked(False)
        self.modelCheck.setEnabled(True)
        self.modelCheck.stateChanged.connect(self.checkBoxChangedActionModel)
        

        self.model = QtWidgets.QComboBox(self)
        model_contents=os.listdir(os.path.join(os.getcwd(),"model"))
        model_contents.remove('modelConfig.ini')
        self.model_list = [s.replace(".joblib", "") for s in model_contents]
        self.model.addItems(self.model_list)
        self.model.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.model.setCurrentIndex(-1)
        self.extraLayout.addRow(self.modelCheck,self.model)
        self.model.setEnabled(False) 

        self.allMachineLearning = QtWidgets.QCheckBox("All Machine Learning")
        self.allMachineLearning.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.allMachineLearning.setChecked(False)
        self.extraLayout.addRow(None,self.allMachineLearning)
        self.allMachineLearning.setEnabled(False) 
        self.allMachineLearning.stateChanged.connect(self.checkBoxChangedActionAllMachineLearning)

        self.extraGroupbox.setLayout(self.extraLayout)

        self.grid.addWidget(self.extraGroupbox,1,0)
    
        #optionGroupbox
        self.optionGroupbox = QtWidgets.QGroupBox("Extra options")
        self.optionGroupbox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.optionLayout = QtWidgets.QFormLayout()

        self.openFolder = QtWidgets.QCheckBox("Open the folder at the end ")
        self.openFolder.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.openFolder, 3,0)
        #self.openFolder.stateChanged.connect(self.checkBoxChangedActionOpenFolder)
        self.openFolder.setChecked(True)
        self.optionLayout.addWidget(self.openFolder)

        self.optionGroupbox.setLayout(self.optionLayout)

        self.grid.addWidget(self.optionGroupbox,1,1)

        self.Report = QtWidgets.QPushButton('Generate Report', self)
        self.Report.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.Report, 4,1)
        self.Report.clicked.connect(self.Report_click)
        #self.Report.setEnabled(False) 

        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 5,0)
        self.help.clicked.connect(self.help_click)
        self.help.setEnabled(True) 

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 4,0)
        self.back.clicked.connect(self.close)

        
        self.deleteBefore = QtWidgets.QCheckBox("Delete before report generation")
        self.deleteBefore.setStyleSheet("QCheckBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.deleteBefore.setChecked(False)
        self.grid.addWidget(self.deleteBefore, 5,1)
        self.deleteBefore.setEnabled(True)
        
    ############################################################################################################
    #
    #
    # 
    ## WIDGETS
    #
    #
    #
    ############################################################################################################
    

    ############################################################################################################
    #
    #
    # 
    ## STATE MANAGEMENT
    #
    #
    #
    ############################################################################################################

    #choose user    
    def activatedUserEdit(self, index):
        if self.userEdit.currentText() != "":
            self.userEditSelect = True
            directory_contents=os.listdir(os.path.join(Config.UsersFolder,self.userEdit.currentText()))

            SimulList=[]
            for elem in directory_contents:
                if len(elem.split('.'))==1 :
                    SimulList.append(elem)
            SimulList.sort()
            SimulList.reverse()
            Function.UpdateComboBox(self.simulationMainEdit, SimulList)
            Function.UpdateComboBox(self.simulationEdit, [])
    
    def activatedSimulationMainEdit(self, index):
        if self.simulationMainEdit.currentText() != "":
            directory_contents=os.listdir(os.path.join(Config.UsersFolder,self.userEdit.currentText(),self.simulationMainEdit.currentText()))

            SimulList=[]
            for elem in directory_contents:
                if len(elem.split('.'))==1 :
                    SimulList.append(elem)
            SimulList.sort()
            SimulList.reverse()
            Function.UpdateComboBox(self.simulationEdit, SimulList)
            self.allSimulation.setEnabled(True)


    def checkBoxChangedActionAllSimulation(self, state):
        if (QtCore.Qt.Checked == state):
            self.simulationEdit.setCurrentIndex(-1)
            self.simulationEdit.setEnabled(False)
            
        else:
            self.simulationEdit.setEnabled(True)

    def checkBoxChangedActionAllAlgorithm(self,state)   :
        if (QtCore.Qt.Checked == state):
            self.algo.setCurrentIndex(-1)
            self.algo.setEnabled(False)
            self.algorithm=Config.eyeTrackerAlgorithm
             
        else:
            self.algo.setEnabled(True)  
            self.algorithm=[]  

    ############################################################################################################
    ## EVS CHECKBOX STATE MANAGEMENT
    ############################################################################################################
        
    def checkBoxChangedEyeTracker(self):
        if self.eyeTracker.isChecked() and self.audio.isChecked(): 
            self.evs.setEnabled(True)
        else :
            self.evs.setEnabled(False)
            self.evs.setChecked(False)

    ############################################################################################################
    ## EVS CHECKBOX STATE MANAGEMENT
    ############################################################################################################

    def on_currentIndexAlgo(self):
        if self.algo.currentText() != "":
            #self.Report.setEnabled(True)
            self.algorithm=[self.algo.currentText()]

    def checkBoxChangedActionModel(self, state):
        if (QtCore.Qt.Checked == state):
            self.model.setEnabled(True)
            self.allMachineLearning.setEnabled(True)
        else :
            self.model.setCurrentIndex(-1)
            self.model.setEnabled(False)
            self.allMachineLearning.setEnabled(False)

    def checkBoxChangedActionAllMachineLearning(self, state):
        if (QtCore.Qt.Checked == state):
            self.model.setCurrentIndex(-1)
            self.model.setEnabled(False)
        else :
            self.model.setEnabled(True)
        

    def checkActionUnit_click(self):
        self.actionUnitsWindows = Video.ActionUnits()
        self.actionUnitsWindows.show()

    def checkReport(self):
        algorithmCondition = Config.onlyBuscher or (self.algo.currentText() != "" or self.allAlgorithm.isChecked())
        userCondition = (self.userEdit.currentText() != "" and self.simulationMainEdit.currentText() != "" and (self.simulationEdit.currentText() != "" or self.allSimulation.isChecked() ))
        eyeTrackerCondition = ( not self.eyeTracker.isChecked() or (self.eyeTracker.isChecked() and algorithmCondition ))
        machineLearning = (not self.modelCheck.isChecked() or (self.modelCheck.isChecked() and (self.model.currentText() != "" or self.allMachineLearning.isChecked()) and algorithmCondition))

        if userCondition and eyeTrackerCondition and machineLearning :
            return True
        else :
            if not userCondition and eyeTrackerCondition and machineLearning:
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("User parameters not full completed"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()
            elif userCondition and not eyeTrackerCondition and machineLearning:
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("Eye Tracker parameters not full completed"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()

            elif userCondition and eyeTrackerCondition and not machineLearning:
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("Machine Learning parameters not full completed"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()

            elif not userCondition and not eyeTrackerCondition and machineLearning:
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("User and Eye Tracker parameters not full completed"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()

            elif not userCondition and eyeTrackerCondition and not machineLearning:
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("User and Machine Learning parameters not full completed"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()

            elif userCondition and not eyeTrackerCondition and not machineLearning:
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("Eye Tracker and Machine Learning parameters not full completed"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()

            else :
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("Report not correct"))
                message.setWindowTitle("Report Generation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()
            return False

    ############################################################################################################
    #
    #
    # 
    ## STATE MANAGEMENT
    #
    #
    #
    ############################################################################################################

    ############################################################################################################
    #
    #
    # 
    ## START REPORT PROCESS 
    #
    #
    #
    ############################################################################################################

    #start report
    def Report_click(self):
        condition = self.checkReport()
        if condition:
            notFileOpen=True
            self.reportConfig=[]

            SimulList=[]
            if self.allSimulation.isChecked() :
                directory_contents=os.listdir(os.path.join(Config.UsersFolder,self.userEdit.currentText(),self.simulationMainEdit.currentText()))
                for elem in directory_contents:
                    if len(elem.split('.'))==1 :
                        SimulList.append(elem)
                SimulList.sort()
                SimulList.reverse()
                i=0
                a = len(SimulList)
            else :
                SimulList.append(self.simulationEdit.currentText())


            for elem in SimulList:
                self.reportConfig.append(CreateReport(os.path.join(Config.UsersFolder,self.userEdit.currentText(),self.simulationMainEdit.currentText(),elem),self.userEdit.currentText(),os.path.join(Config.ReportFolder,str(self.userEdit.currentText() + "_" + self.simulationMainEdit.currentText()),elem),self.algorithm))
            fileOpen=[]
            for i in range(0,len(self.reportConfig)):    
                            
                self.reportConfig[i].openFolder = self.openFolder.isChecked()
                self.reportConfig[i].reportMainName=os.path.join(Config.ReportFolder,str(self.userEdit.currentText() + "_" + self.simulationMainEdit.currentText()))

                if not os.path.isdir(os.path.join(Config.ReportFolder)): 
                        os.makedirs(os.path.join(Config.ReportFolder))

                try:
                    if  os.path.isdir(self.reportConfig[i].reportName):
                        os.rename(self.reportConfig[i].reportName,self.reportConfig[i].reportName)

                except:
                    fileOpen.append(str(self.reportConfig[i].reportName))
                    notFileOpen = False

            if notFileOpen and len(fileOpen) == 0 : 
                for i in range(0,len(self.reportConfig)):
                    if self.deleteBefore.isChecked() :
                        if  os.path.isdir(self.reportConfig[i].reportName):
                            shutil.rmtree(self.reportConfig[i].reportName)
                            print(str(self.reportConfig[i].reportName) + " already exit => it was deleted")
                            os.makedirs(self.reportConfig[i].reportName)
                    
                    if  not os.path.isdir(self.reportConfig[i].reportName):
                        os.makedirs(self.reportConfig[i].reportName)
                    
                    self.reportConfig[i].eyeTrackerChecked = self.eyeTracker.isChecked()
                    self.reportConfig[i].audioChecked = self.audio.isChecked()

                    ############################################################################################################
                    ## FETCH EVS CHECKBOX STATE AND ADD IT TO REPORT CONFIG
                    ############################################################################################################

                    self.reportConfig[i].evsChecked = self.evs.isChecked()

                    ############################################################################################################
                    ## FETCH EVS CHECKBOX STATE AND ADD IT TO REPORT CONFIG
                    ############################################################################################################

                    if self.modelCheck.isChecked() and self.model.currentText() != "" and not self.allMachineLearning.isChecked():
                        self.reportConfig[i].modelCheck=True
                        self.reportConfig[i].model=[self.model.currentText()]

                    elif self.modelCheck.isChecked() and self.allMachineLearning.isChecked():
                        self.reportConfig[i].modelCheck=True
                        self.reportConfig[i].model=self.model_list

                    else :
                        self.reportConfig[i].modelCheck=False

                    if self.eyeTracker.isChecked():           
                        self.reportConfig[i].timeStartEye = ""
                        self.reportConfig[i].timeStartHead = ""
                        
                    self.reportConfig[i].videoChecked = self.video.isChecked()
                    self.reportConfig[i].actionUnit=self.actionUnit.isChecked()
                    CopieFile(self.reportConfig[i])
                self.hide()
                self.process = ReportProcess(self,self.reportConfig)
                
                self.process.show()
            
            else:
                print("pb detected")
                informativeText = ("File or folder open in " + os.linesep)
                for elem in fileOpen:
                    informativeText+=(str(elem) + os.linesep)
            
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText(str("Report Creation Error" + os.linesep))
                message.setInformativeText(informativeText)
                message.setDetailedText(str("Please close all file in folder or close folder" ))
                message.setWindowTitle("Report Creation Error")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                #width=900
                #height=500
                #message.setGeometry(Config.SCREEN_WIDTH/2-width/2,Config.SCREEN_HEIGHT/2-height/2,width,height)
                message=message.exec_()

    ############################################################################################################
    #
    #
    # 
    ## START REPORT PROCESS  
    #
    #
    #
    ############################################################################################################



    ############################################################################################################
    #
    #
    # 
    ## HELP WINDOW STATE MANAGEMENT
    #
    #
    #
    ############################################################################################################

    #close windows
    def closeEvent(self, event):
        if hasattr(self, "helpWindows"):
            self.helpWindows.close()
        self.windows.show()

    #help
    def help_click(self):
        if Config.documentationHTML:
            helpHtml()
        else:
            self.helpWindows = Help()
            self.helpWindows.show()

    ############################################################################################################
    #
    #
    # 
    ## HELP WINDOW STATE MANAGEMENT
    #
    #
    #
    ############################################################################################################

 ############################################################################################################
 #
 #
 #
 ## INITIALIZE SIMULATION PARAMETERS
 #
 #
 #
 ############################################################################################################
#analyze the generated report
class AnalyzeReport():
    def __init__(self,reportFolder):
        self.reportFolder = reportFolder
        self.textPosition = os.path.join(self.reportFolder, "textPosition.csv")

        self.fixationsFolder = os.path.join(self.reportFolder, "buscher")
        self.eyesPosition = os.path.join(self.fixationsFolder, "fixations_0.csv")
        self.validPrct = 0
        self.validPrctWord = 0
        #recup des emplacements dossier

    def readTextPosition(self):
        text = open(self.textPosition, 'r')
        self.words = list(csv.reader(text))
        text.close()

    def readEyesPosition(self, algo):

        self.fixations = []
        self.fixationsFolder = os.path.join(self.reportFolder, str(algo))
        self.eyesPosition = os.path.join(self.fixationsFolder, "fixations_0.csv")

        if os.path.isfile(self.eyesPosition):
            fixations = open(self.eyesPosition, 'r')
            self.fixations = list(csv.reader(fixations))
            fixations.close()  
        
    def comparePos(self):
        #compraison en x
        nb_valid = 0
        if len(self.fixations) != 0:
            total_fix = len(self.fixations) - 1

            #fixations dans les mots
            for fix in self.fixations[1:]:
                x = float(fix[0])
                y = float(fix[1])
                for row in self.words[2:]:
                    nb_page = int(row[5])
                    wordXPos = float(row[1])
                    wordWidth = float(row[3])
                    if(nb_page == 0):
                        if( (x < wordXPos + wordWidth) and (x > wordXPos) ):
                            wordYPos = float(row[2])
                            wordHeigth = float(row[4])
                            if( (y < (wordYPos + wordHeigth)) and (y > wordYPos)):
                                nb_valid = nb_valid + 1

            self.validPrct = 100*(nb_valid/total_fix)
            #print(nb_valid,"/",total_fix)
            #print(self.validPrct)

            #mots avec au moins une fixation
            nb_word = 0
            nb_valid_word = 0
            for row in self.words[2:]:
                nb_page = int(row[5])
                wordXPos = float(row[1])
                wordWidth = float(row[3])
                wordYPos = float(row[2])
                wordHeigth = float(row[4])
                if(nb_page == 0):
                    nb_word = nb_word + 1
                    for fix in self.fixations[1:]:
                        x = float(fix[0])
                        y = float(fix[1])
                        if( (x < wordXPos + wordWidth) and (x > wordXPos) ):
                            if( (y < wordYPos + wordHeigth) and (y > wordYPos )):
                                nb_valid_word = nb_valid_word + 1
                                break
            self.validPrctWord = 100*(nb_valid_word/nb_word)
            #print(str(nb_valid_word),"/",str(nb_word))

#get all simulation parameters    
class CreateReport():
    def __init__(self,simulFolder,user,reportName,algorithm):
        self.simulFolder = simulFolder
        self.configSimul = ConfigFileManagement.ConfigFileRead(os.path.join(self.simulFolder,"config.ini"))
        self.screenWidth = int(self.configSimul.GetParameters('System', 'screen_width'))
        self.screenHeight = int(self.configSimul.GetParameters('System', 'screen_height'))
        self.x0 = int(self.configSimul.GetParameters('System', 'x0'))
        self.y0 = int(self.configSimul.GetParameters('System', 'y0'))
        self.eyeTracker = str(self.configSimul.GetParameters('System', 'eyeTracker'))
        self.txt = str(self.configSimul.GetParameters('Text', 'title'))
        self.pageMax = int(self.configSimul.GetParameters('Text', 'page'))
        self.timeSimul = str(self.configSimul.GetParameters('Time', 'time')).split(',')
        self.audio = str(self.configSimul.GetParameters('Time', 'audio'))
        self.video = str(self.configSimul.GetParameters('Time', 'video'))

        self.rate = int(self.configSimul.GetParameters('System', 'rate'))
        self.channels = int(self.configSimul.GetParameters('System', 'channels'))
        self.chunk = int(self.configSimul.GetParameters('System', 'chunk'))
        self.soundOut = str(self.configSimul.GetParameters('System', 'sound_out'))
        self.videoOut = str(self.configSimul.GetParameters('System', 'videoOut'))
        self.mcqAnswer = str(self.configSimul.GetParameters('System', 'mcq_answer'))
        self.textPosition = str(self.configSimul.GetParameters('System', 'text_position'))
        self.textPart = str(self.configSimul.GetParameters('System', 'text_part'))
        self.eyeTrackerHeadData = str(self.configSimul.GetParameters('System', 'eye_tracker_head_data'))
        self.eyeTrackerData = str(self.configSimul.GetParameters('System', 'eye_tracker_data'))
        self.screenshotName = str(self.configSimul.GetParameters('System', 'screenshot_name'))

        self.eyeTrackerGlissades = str(self.configSimul.GetParameters('System', 'eyeTrackerGlissades'))
        self.eyeTrackerSaccades = str(self.configSimul.GetParameters('System', 'eyeTrackerSaccades'))
        self.eyeTrackerFixations = str(self.configSimul.GetParameters('System', 'eyeTrackerFixations'))
        self.eyeTrackerVelocityGazes = str(self.configSimul.GetParameters('System', 'eyeTrackerVelocityGazes'))
        self.eyeTrackerScreenshot = str(self.configSimul.GetParameters('System', 'eyeTrackerScreenshot'))
        self.wordScreenshot = str(self.configSimul.GetParameters('System', 'wordScreenshot'))

        
        self.allowAudio = str(self.configSimul.GetParameters('User', 'audio'))
        self.allowAudio = True if self.allowAudio=="True" else False
        self.audioChecked = False
        self.allowVideo = str(self.configSimul.GetParameters('User', 'video'))
        self.allowVideo = True if self.allowVideo=="True" else False
        self.videoChecked = False
        self.allowEyeTracker = str(self.configSimul.GetParameters('User', 'eyeTracker'))
        self.allowEyeTracker = True if self.allowEyeTracker=="True" else False
        self.eyeTrackerChecked = False
        self.user = user
        self.reportMainName=""
        self.reportName= reportName
        self.timeStartEye=""
        self.timeStartHead=""
        self.algorithm=algorithm
        self.headPositionValidity=False
        self.videoProcess = False
        self.opencv = True
        self.timeVideo = ""
        self.videoWidth = ""
        self.videoHeight = ""
        self.videoFPS = ""
        self.numberFrame = ""
        self.timeDuring = ""
        self.numberFace = ""
        self.numberEyes = ""
        self.openFolder = False

        ############################################################################################################
        ## EVS VARIABLES
        ############################################################################################################

        self.evsChecked = False
        self.evs= ""
        

        ############################################################################################################
        ## EVS VARIABLES
        ############################################################################################################
        
        self.modelCheck = False
        self.model = ""
        self.createPageCSV = ""
        self.deleteBefore = ""
        self.actionUnit=False
 ############################################################################################################
 #
 #
 #
 ## INITIALIZE SIMULATION PARAMETERS
 #
 #
 #
 ############################################################################################################







 ############################################################################################################
 #
 #
 #
 ## GENERATING REPORT
 #
 #
 #
 ############################################################################################################

#report Generation
class ReportProcess(QtWidgets.QWidget):
    ############################################################################################################
    #
    ## GENERATING REPORT : MAIN WINDOW LAYOUT 
    #
    ############################################################################################################

    def __init__(self,windows,reportConfig):
        QtWidgets.QWidget.__init__(self)
        self.reportConfig=reportConfig
        self.windows = windows
        self.windows.hide()
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Report Generation')
        self.width=400
        self.height=500
        self.setGeometry(0,0,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid) 

        self.title = QtWidgets.QLabel("",self)
        self.title.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.title, 0,0)

        self.text = QtWidgets.QTextEdit(self)
        self.text.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.text, 1,0)
        self.text.setReadOnly(True)

        self.end = QtWidgets.QPushButton('Done', self)
        self.end.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.end, 2,0)
        self.end.clicked.connect(self.close)
        #self.end.setEnabled(False) 
        self.end.hide()
        self.finished = False
        self.process()
    ############################################################################################################
    #
    ## GENERATING REPORT : MAIN WINDOW LAYOUT 
    #
    ############################################################################################################

    ############################################################################################################
    #
    ## GENERATING REPORT : CREATING MAIN FILES 
    #
    ############################################################################################################

    #start report
    def process(self):
        #check if generate word position necessary
        tempWord = []
        for reportConfig in self.reportConfig:
            wordText = 0
            for (root,dirs,files) in os.walk(reportConfig.reportName, topdown=True):
                for file in files:
                    if str(str(reportConfig.wordScreenshot) + "_") in file:
                        wordText+=1
            if wordText < reportConfig.pageMax:
                tempWord.append(reportConfig)
        wordGeneration = False

        #generate word position
        if len(tempWord)>0:
            wordGeneration = True
            self.reportWordWindows = ReportWord(tempWord)
            self.reportWordWindows.processing.connect(self.text.append)

        #eyetracker process
        if self.reportConfig[0].eyeTrackerChecked:
            if wordGeneration :
                self.reportWordWindows.finished.connect(self.createPageProcess)
            else :
                self.createPageProcess()

        #MachineLearning
        elif self.reportConfig[0].modelCheck==True and len(self.reportConfig[0].model) >0 :
            if wordGeneration :
                self.reportWordWindows.finished.connect(lambda:self.machineLearningPredictThread(self.reportConfig))
            else:
                self.machineLearningPredictThread(self.reportConfig)

        #video process
        elif self.reportConfig[0].videoChecked :
            if wordGeneration :
                self.reportWordWindows.finished.connect(self.videoProcess) 
            else:
                self.videoProcess()

        #actionUnit
        elif self.reportConfig[0].actionUnit :
            if wordGeneration :
                self.reportWordWindows.finished.connect(self.actionUnit) 
            else :
                self.actionUnit()
    
        ############################################################################################################
        ## CHECKING IF EVS CHECKBOX IS CHECKED
        ############################################################################################################

        elif self.reportConfig[0].evsChecked :
            if wordGeneration :
                self.reportWordWindows.finished.connect(self.generateEVS) 
            else :
                self.generateEVS(self.reportConfig)
                
        ############################################################################################################
        ## CHECKING IF EVS CHECKBOX IS CHECKED
        ############################################################################################################
        
        
        #ADD AUDIO PROCESS HERE
       
        #report TXT
        else:
            if wordGeneration :
                self.reportWordWindows.finished.connect(self.ReportTxt) 
            else:
                self.ReportTxt()
    
    ############################################################################################################
    #
    ## GENERATING REPORT : CREATING MAIN FILES 
    #
    ############################################################################################################

    #eyetracker create page generation    
    def createPageProcess(self):

        if self.reportConfig[0].eyeTrackerChecked:
            self.createPage = EyeTracker.CreatePage(self.reportConfig)
            self.createPage.finished.connect(self.eyeTrackerProcess)
            self.createPage.processing.connect(self.text.append)
            self.createPage.start()

        else :
            self.eyeTrackerProcess()

    #eyetracker generation    
    def eyeTrackerProcess(self):
        tempReportConfig=[]
        tempMachineLearning=[]

        self.reportConfig = self.createPage.reportConfigProcess

        for i in range(0,len(self.reportConfig)):
            if self.reportConfig[i].createPageCSV:
                tempReportConfig.append(self.reportConfig[i])


        for i in range(0,len(tempReportConfig)):
            if tempReportConfig[i].modelCheck:
                tempMachineLearning.append(tempReportConfig[i])

        if len(tempReportConfig)>0:

            self.eyeTrackerTraceWindows = EyeTracker.EyeTrackerTrace(tempReportConfig)
            self.eyeTrackerTraceWindows.processing.connect(self.text.append)

            self.eyeTrackerTraceWindows.finished.connect(lambda:self.machineLearningPredictThread(tempMachineLearning))

        else :
            self.machineLearningPredictThread(self.reportConfig)
        

    #machine learning generation
    def machineLearningPredictThread(self,reportConfig):

        if len(reportConfig) > 0 and reportConfig[0].modelCheck:
            self.machineLearning = MachineLearning.MachineLearningProcess(reportConfig)
            self.machineLearning.processing.connect(self.text.append)
            self.machineLearning.finished.connect(self.videoProcess)
            self.machineLearning.start()

        else :
           self.videoProcess()

    #video generation
    def videoProcess(self):

        for i in range(0,len(self.reportConfig)) :
            if self.reportConfig[i].allowVideo and os.path.isfile(os.path.join(Config.ReportFolder,self.reportConfig[i].reportName,str(self.reportConfig[i].videoOut + ".avi"))):
                if os.path.isfile(os.path.join(Config.ReportFolder,self.reportConfig[i].reportName,str(self.reportConfig[i].videoOut + ".avi"))):
                    cap = cv2.VideoCapture(os.path.join(Config.ReportFolder,self.reportConfig[i].reportName,str(self.reportConfig[i].videoOut + ".avi")))
                    self.reportConfig[i].numberFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.reportConfig[i].duration = float(self.reportConfig[i].numberFrame / cap.get(cv2.CAP_PROP_FPS))
                    self.reportConfig[i].timeVideo = datetime.timedelta(seconds=(self.reportConfig[i].duration))
                    self.reportConfig[i].videoWidth = int(cap.get(3))
                    self.reportConfig[i].videoHeight = int(cap.get(4))
                    self.reportConfig[i].videoFPS = cap.get(cv2.CAP_PROP_FPS)
                    cap.release() 

        tempReportConfig = []
        for i in range(0,len(self.reportConfig)):
            
            if self.reportConfig[i].allowVideo and self.reportConfig[i].videoChecked and os.path.isfile(os.path.join(Config.ReportFolder,self.reportConfig[i].reportName,str(self.reportConfig[i].videoOut + ".avi"))):
                self.reportConfig[i].videoProcess = True
                tempReportConfig.append(self.reportConfig[i])

        if len(tempReportConfig) > 0:
            if os.path.isfile(os.path.join(os.getcwd(),"openFace","FeatureExtraction.exe")):
                for i in range(0,len(self.reportConfig)):
                    self.reportConfig[i].opencv = False
                
                self.thread=Video.ThreadVideoProcessingOpenFace(tempReportConfig)

                #self.text.append("Start video process")
                self.thread.processing.connect(self.text.append)#insertPlainText
                self.thread.finished.connect(self.actionUnit)
                self.thread.start()

            else:
                #self.text.append("Start video process")
                self.thread = Video.ThreadVideoProcessingOpencv(tempReportConfig)
                self.thread.processing.connect(self.text.append)
                self.thread.finished.connect(self.ReportTxt)
                #self.thread.remainTime.connect(self.remain.setText)
                #self.thread.timeStart.connect(self.timeStart.setText)
                self.thread.start()

        else : 
            self.actionUnit()

    #action unit generation
    def actionUnit(self):

        tempReportConfig=[]

        for i in range(0,len(self.reportConfig)):
            if self.reportConfig[i].allowVideo and os.path.isfile(os.path.join(Config.ReportFolder,self.reportConfig[i].reportName,"video_processed","video.csv")) and self.reportConfig[i].actionUnit:
                tempReportConfig.append(self.reportConfig[i])

        if len(tempReportConfig) >= 1:
            self.actionUnitsThread = Video.CheckActionUnits(tempReportConfig)
            self.actionUnitsThread.processing.connect(self.text.append)#insertPlainText
            self.actionUnitsThread.finished.connect(self.generateEVS)
            self.actionUnitsThread.start()
            
        else : 
            self.generateEVS(self.reportConfig)
    
    ############################################################################################################
    ## CHECKING IF EVS CHECKBOX IS CHECKED
    ############################################################################################################

    def generateEVS(self, reportConfig):
       if len(self.reportConfig) > 0 and self.reportConfig[0].evsChecked :
           self.evsProcess = EVSGeneration.EVS(reportConfig)
           self.evsProcess.processing.connect(self.text.append)
           self.evsProcess.finished.connect(self.ReportTxt)
           self.evsProcess.start()
       else:
           self.ReportTxt()

    ############################################################################################################
    ## CHECKING IF EVS CHECKBOX IS CHECKED
    ############################################################################################################

    #AUDIO PROCESS FUNCTION        
    #def audioProcess(self):

    #generate txt report
    def ReportTxt(self):

        for current in range(0,len(self.reportConfig)):
            
            userConfig = User.User()
            userConfig.Import(self.reportConfig[current].user)

            with open(str(os.path.join(self.reportConfig[current].reportName,"Report.txt")), 'w',encoding='utf-8',errors='ignore',newline='') as f:
                f.writelines(str("Report : "+ os.path.split(self.reportConfig[current].simulFolder)[1]+ os.linesep))
                f.write(str(os.linesep))
                f.write(str("Screen Resolution :") + os.linesep)
                f.write(str("   Screen width : "+str(self.reportConfig[current].screenWidth)+os.linesep))
                f.write(str("   Screen heigth : "+str(self.reportConfig[current].screenHeight)+os.linesep))
                f.write(str(os.linesep))
                f.writelines(str("Offset coordinate :" ) + os.linesep)
                f.write(str("   x0 : "+str(self.reportConfig[current].x0)+os.linesep))
                f.write(str("   y0 : "+str(self.reportConfig[current].y0)+os.linesep))
                f.write(str(os.linesep))
                f.write(str("User : " + os.linesep))
                f.write(str("   Name : " + userConfig.get("Last_name") + " " + userConfig.get("First_name")) + os.linesep)
                f.write(str("   Birthday : " + userConfig.get("Birthday")) + os.linesep)
                f.write(str("   Genre : " + userConfig.get("Genre")) + os.linesep)
                f.write(str("   Level : " + userConfig.get("Level")) + os.linesep)
                f.write(str("   Toeic : " + userConfig.get("Toeic")) + os.linesep)
                f.write(str("   Country : " + userConfig.get("Country")) + os.linesep)
                f.write(str(os.linesep))

                f.writelines(str("User Data : " +  os.linesep))
                f.writelines(str("   Audio : " + str(self.reportConfig[current].allowAudio) + os.linesep))
                f.writelines(str("   Video : " + str(self.reportConfig[current].allowVideo) + os.linesep))
                f.writelines(str("   EyeTracker : " + str(self.reportConfig[current].allowEyeTracker) + os.linesep))
                f.write(str(os.linesep))

                f.writelines(str("Text : " +  os.linesep))
                f.writelines(str("   Title : " + str(self.reportConfig[current].txt) + os.linesep))
                f.writelines(str("   Page Read : " + str(self.reportConfig[current].pageMax) + os.linesep))
                f.write(str(os.linesep))

                f.writelines(str("Time Read : " +  os.linesep))
                for i in range(1,len(self.reportConfig[current].timeSimul)):
                    f.writelines(str("   Page " + str(i-1)+" : "+ str((int(self.reportConfig[current].timeSimul[i]) - int(self.reportConfig[current].timeSimul[i-1])) )+ os.linesep))
                f.write(str(os.linesep))

            
                f.writelines(str("UNIX Time : " +  os.linesep))
                f.writelines(str("   Start : "+ str(self.reportConfig[current].timeSimul[0])+ os.linesep))
                for i in range(1,len(self.reportConfig[current].timeSimul)-1):
                    f.writelines(str("   Page " + str(i-1)+" : "+ str(self.reportConfig[current].timeSimul[i] )+ os.linesep))
                f.writelines(str("   Stop : "+ self.reportConfig[current].timeSimul[len(self.reportConfig[current].timeSimul)-1]+ os.linesep))
                f.write(str(os.linesep))

                if self.reportConfig[current].allowAudio or self.reportConfig[current].allowVideo:
                    f.write(str(os.linesep))
                    f.writelines(str("UNIX Time Start " +  os.linesep))
                    if self.reportConfig[current].allowAudio:
                        f.writelines(str("   Start Audio : "+ str(self.reportConfig[current].audio)+ os.linesep))
                    if self.reportConfig[current].allowVideo:
                        f.writelines(str("   Start Video : "+ str(self.reportConfig[current].video)+ os.linesep))
                
                
                if self.reportConfig[current].timeStartEye != "" and self.reportConfig[current].allowEyeTracker:
                    f.writelines(str("   Start Eye Tracker Eye : "+ str(self.reportConfig[current].timeStartEye)+ os.linesep))
                
                if self.reportConfig[current].timeStartHead != "" and self.reportConfig[current].allowEyeTracker:
                    f.writelines(str("   Start Eye Tracker Head: "+ str(self.reportConfig[current].timeStartHead)+ os.linesep))

                ############################################################################################################
                ## WRITE AVERAGE EVS
                ############################################################################################################

                if self.reportConfig[current].evsChecked and self.reportConfig[current].allowAudio  :
                    f.write(str(os.linesep))
                    f.writelines(str("Eye-voice variation Generated" + os.linesep))
                    # TODO: write average evs 
                    f.write(str(os.linesep))
                
                ############################################################################################################
                ## WRITE AVERAGE EVS
                ############################################################################################################

                if self.reportConfig[current].allowVideo  :
                    f.write(str(os.linesep))
                    f.writelines(str("Video : " + os.linesep))
                    f.write("   Time video : " + str(self.reportConfig[current].timeVideo) + os.linesep)
                    f.write("   Size video : " + str(self.reportConfig[current].videoWidth) + "x" + str(self.reportConfig[current].videoHeight) + os.linesep)
                    f.write("   FPS : " + str(self.reportConfig[current].videoFPS) + os.linesep)
                    f.write("   Total Frame : " + str(self.reportConfig[current].numberFrame) + os.linesep)
                    f.write(str(os.linesep))
                    """
                    if self.reportConfig[current].videoProcess:
                        if self.reportConfig[current].opencv :
                            f.write("   Time processing during : " + str(self.reportConfig[current].timeDuring) + os.linesep)
                            f.write("   Face detected : " + str(self.reportConfig[current].numberFace) + os.linesep)
                            f.write("   Eyes detected : " + str(self.reportConfig[current].numberEyes) + os.linesep)
                            f.write(str(os.linesep))
                            f.writelines(str("   Video processed with Opencv" + os.linesep))
                            f.write(str(os.linesep))
                        if not self.reportConfig[current].opencv :
                            f.write(str(os.linesep))
                            f.writelines(str("   Video processed with OpenFace" + os.linesep))
                            f.write(str(os.linesep))
                
                    else :
                        f.write(str(os.linesep))
                        f.writelines(str("  Video not process by user" + os.linesep))
                        f.write(str(os.linesep))
                    """
                """
                if self.reportConfig[current].headPositionValidity :
                    f.writelines(str("VelocityGazes.csv was not created because eyeTrackerHead.csv was invalid" + os.linesep))
                    f.write(str(os.linesep))
                """
                if os.path.isfile(os.path.join(self.reportConfig[current].simulFolder,str(self.reportConfig[current].textPart+".txt"))):
                    f.writelines(str("Words not understood : " + (os.linesep)))
                    f.write(str(os.linesep))
                    word=[]
                    with open(str(os.path.join(self.reportConfig[current].simulFolder,str(self.reportConfig[current].textPart+".txt"))), 'r',encoding='utf-8',errors='ignore',newline='') as textPart:
                        for elem in textPart.readlines():
                            word.append(elem)
                        textPart.close()
                    word.pop(0)
                    for elem in word :
                        f.writelines("  " + str(elem))
                    f.write(str(os.linesep))

                #####
                if self.reportConfig[current].modelCheck:
                    for algo in self.reportConfig[current].algorithm:
                        for machineLearning in self.reportConfig[current].model:
                            if os.path.isdir(os.path.join(self.reportConfig[current].reportName,algo,machineLearning)):
                                with open(str(os.path.join(self.reportConfig[current].reportName,algo,machineLearning,"machineLearningReport.txt")), 'w',encoding='utf-8',errors='ignore',newline='') as wordsPredicted:
                                    if os.path.isfile(os.path.join(self.reportConfig[current].reportName,algo,machineLearning,"dataFramePredict.csv")):
                                        wordsPredicted.writelines(str("Words predicted not understood by the machine learning : " + (os.linesep)))
                                        wordsPredicted.write(str(os.linesep))
                                        word=[]
                                        with open(os.path.join(self.reportConfig[current].reportName,algo,machineLearning,"dataFramePredict.csv"),'r', newline='') as csvfile:
                                        #with open(str(os.path.join(root,str(self.reportConfig[current].textPosition) + ".csv")),'r', newline='') as csvfile:
                                            dataFramePredict = csv.reader(csvfile, delimiter=',')
                                            wordData = [line for line in dataFramePredict]
                                        for i in range (1,len(wordData)):
                                            if wordData[i][-1]=='1':
                                                wordsPredicted.writelines("  " + str(wordData[i][1]) + " , page: " + str(wordData[i][6]) + ", index csv: " + str(i))
                                                wordsPredicted.write(str(os.linesep))
                                        wordsPredicted.write(str(os.linesep))
                                wordsPredicted.close()

                if os.path.isfile(os.path.join(self.reportConfig[current].simulFolder,str(self.reportConfig[current].mcqAnswer+".csv"))):
                    f.writelines(str("MCQ : " + (os.linesep)))
                    f.write(str(os.linesep))
                    lineMCQ=[]
                    noteMCQ = 0
                    with open(str(os.path.join(self.reportConfig[current].simulFolder,str(self.reportConfig[current].mcqAnswer+".csv"))), 'r', newline='') as csvfile:
                        fileUser = csv.reader(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL) 
                        lineMCQ = [line for line in fileUser]
                        lineMCQ.pop(0)
                        lineMCQ.pop(0)
                        csvfile.close()
                    currentQuestion = 1
                    for elem in lineMCQ:
                        f.writelines(str("   QUESTION " + str(currentQuestion) + " : " + str(elem[0]) + (os.linesep)))
                        f.writelines(str("   USER ANSWER : " + str(elem[1]) + (os.linesep)))
                        if elem[1] == elem[2] :
                            f.writelines(str("   RIGHT ANSWERS" + (os.linesep)))
                            noteMCQ+=1
                        else :
                            f.writelines(str("   WRONG ANSWER => " + str(elem[2]) + (os.linesep)))
                        currentQuestion+=1
                        f.write(str(os.linesep))
                    score = float(noteMCQ/len(lineMCQ))*10
                    f.writelines(str("   Score : " + str(score) + "/10" + (os.linesep)))
                    f.write(str(os.linesep))
                
                f.write(str(os.linesep))
                f.writelines(str("Report validation : " +  os.linesep))

                if self.reportConfig[current].eyeTrackerChecked and self.reportConfig[current].audioChecked:
                    #analyse du report
                    reportPath = os.path.join(Config.ReportFolder,self.reportConfig[0].reportMainName,self.reportConfig[0].reportName)
                    self.analyzer = AnalyzeReport(reportPath)
                    self.analyzer.readTextPosition()

                    for algo in self.reportConfig[current].algorithm:
                
                        self.analyzer.readEyesPosition(algo)
                        self.analyzer.comparePos()

                        prctGazes = 0
                        if str(algo) == "buscher":
                            prctGazes = self.createPage.percentageGazesBuscher
                        elif str(algo) == "nystrom":
                            prctGazes = self.createPage.percentageGazesNystrom

                        result, validFixationInWord, validWordWithFixation, validGazesInFixation = self.isValid(self.analyzer.validPrct, self.analyzer.validPrctWord, prctGazes)

                        self.text.append("Report validation :")

                        reportAlgo = "    Report validation based on " + str(algo)
                        self.text.append(reportAlgo)
                        f.writelines(str(reportAlgo + (os.linesep)))

                        reportFixInWords = "    Fixations in words (%) : " + str(round(self.analyzer.validPrct, 2)) + " - " + validFixationInWord
                        self.text.append(reportFixInWords)
                        f.writelines(str(reportFixInWords + (os.linesep)))

                        reportWordsWithFix = "    Words with at least a fixation (%) : " + str(round(self.analyzer.validPrctWord, 2)) + " - " + validWordWithFixation
                        self.text.append(reportWordsWithFix)
                        f.writelines(str(reportWordsWithFix + (os.linesep)))

                        prctGazes = 0
                        if str(algo) == "buscher":
                            prctGazes = self.createPage.percentageGazesBuscher
                        elif str(algo) == "nystrom":
                            prctGazes = self.createPage.percentageGazesNystrom

                        eyeGazesInFix = "    Eyegazes in fixations (%) : " + str(round(prctGazes, 2)) + " - " + validGazesInFixation
                        self.text.append(eyeGazesInFix)
                        f.writelines(str(eyeGazesInFix + (os.linesep)))

                        validatedRecord = "    Validated record : " + result
                        self.text.append(validatedRecord)
                        f.writelines(str(validatedRecord + (os.linesep) + (os.linesep)))
                        self.text.append("\n")
                        
                    f.write(str(os.linesep))

                f.close()  
            
            self.text.append("Start Export in TXT")
            print("report " + str(os.path.split(self.reportConfig[current].simulFolder)[1]) + " done")
            self.text.append("      report " + str(os.path.split(self.reportConfig[current].simulFolder)[1]) + " done")
        self.text.append("End Export in TXT")
        self.text.append("\n")

        self.text.append("\n")
        self.openFolderWindows()
        #self.end.setEnabled(True)
        self.end.show()
        self.finished = True
        #self.endReport.emit(1)
        print("end Report")

    def isValid(self, fixationInWord, wordWithFixation, gazeInFixation):
        validated = "Record Is Validated"
        validFixationInWord = "Validated"
        validWordWithFixation = "Validated"
        validGazesInFixation = "Validated"
        
        if(gazeInFixation < 70):
            validated = "Record Is Not Validated"
        elif(wordWithFixation < 60):
            validated = "Record Is Not Validated"
        elif(fixationInWord < 80):
            validated = "Record Is Not Validated"

        if(fixationInWord < 80):
            validFixationInWord = "Not Validated"

        if(wordWithFixation < 60):
            validWordWithFixation = "Not Validated"

        if(gazeInFixation < 70):
            validGazesInFixation = "Not Validated"

        return validated,validFixationInWord,validWordWithFixation,validGazesInFixation

    #open Folder at the end
    def openFolderWindows(self):
        if self.reportConfig[0].openFolder:
            FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
            self.text.append("Open Folder")

            if len(self.reportConfig)==1:
                subprocess.run([FILEBROWSER_PATH, os.path.join(Config.ReportFolder,self.reportConfig[0].reportMainName,self.reportConfig[0].reportName)])
            else:
                subprocess.run([FILEBROWSER_PATH, os.path.join(Config.ReportFolder,self.reportConfig[0].reportMainName)])

    #close event
    def closeEvent(self, event):

        if self.finished :
            event.accept()
            self.windows.show()
        else :
            event.ignore()


 ############################################################################################################
 #
 #
 #
 ## GENERATING REPORT
 #
 #
 #
 ############################################################################################################
 
#copy file in report folder
def CopieFile(reportConfig):

    for (root,dirs,files) in os.walk(reportConfig.simulFolder, topdown=True):
        for file in files:
            shutil.copyfile(os.path.join(reportConfig.simulFolder,file),os.path.join(Config.ReportFolder,reportConfig.reportName,file))
            if file == str(reportConfig.eyeTrackerData + "." + Config.eyeTrackerDataFile) or file == str(reportConfig.eyeTrackerHeadData + "." + Config.eyeTrackerDataFile) :
                for algo in reportConfig.algorithm:
                    if not os.path.isdir(os.path.join(Config.ReportFolder,reportConfig.reportName,algo)):
                        os.mkdir(os.path.join(Config.ReportFolder,reportConfig.reportName,algo))
                    shutil.copyfile(os.path.join(reportConfig.simulFolder,file),os.path.join(Config.ReportFolder,reportConfig.reportName,algo,file))


#display word coordinates and save them
class ReportWord(QtWidgets.QWidget):
    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)
    def __init__(self,reportConfig):
        QtWidgets.QWidget.__init__(self)
        self.simulFolder = reportConfig[0].simulFolder
        self.saveFolder = reportConfig[0].reportName
        self.page=0
        self.pageMax = reportConfig[0].pageMax
        self.ready=True
        self.reportConfigMain = reportConfig
        self.reportConfig = reportConfig[0]
        self.width=Config.SCREEN_WIDTH_SIMULATION
        self.height=Config.SCREEN_HEIGHT_SIMULATION
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.i=0
        with open(str(os.path.join(self.simulFolder,str(reportConfig[0].textPosition + ".csv"))), 'r', newline='') as csvfile:
            fileUser = csv.reader(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.word_tab = [line for line in fileUser]
            csvfile.close()
        self.start=False          
        self.show()
         

    def paintEvent(self, event):
        if not self.start:
            self.processing.emit("Start Word position Screenshot")
            self.start=True
        if self.ready:
            if self.page==self.pageMax :

                if self.i == len(self.reportConfigMain) -1 :
                    self.finishReport() 

                else  :
                    self.i +=1
                    self.processing.emit(str("     " + str(os.path.split(self.saveFolder)[1]) + " done"))
                    self.reportConfig = self.reportConfigMain[self.i] 
                    self.simulFolder = self.reportConfig.simulFolder
                    self.saveFolder = self.reportConfig.reportName
                    self.page=0
                    self.pageMax = self.reportConfig.pageMax
                    self.ready=True
                    with open(str(os.path.join(self.saveFolder,str(self.reportConfig.textPosition + ".csv"))), 'r', newline='') as csvfile:
                        fileUser = csv.reader(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        self.word_tab = [line for line in fileUser]
                        csvfile.close()

                    self.hide()
                    self.show()
                                                
            else :
                painter = QtGui.QPainter()
                painter.begin(self)
                self.drawWord(event, painter)
                painter.end()
        else :
            if self.page < self.pageMax:
                self.page+=1
                self.ready = True
                self.hide()
                self.show()
                
    def finishReport(self):

        self.close()
        self.processing.emit(str("     " + str(os.path.split(self.saveFolder)[1]) + " done"))
        self.processing.emit(str("End Word position Screenshot\n"))
        self.finished.emit(1)

        
    def drawWord(self, event, painter):

        if os.path.isfile(os.path.join(self.saveFolder,str(str(self.reportConfig.screenshotName) + "_"+ str(self.page) + ".jpg"))):
            if os.path.isfile(os.path.join(self.simulFolder,str(str(self.reportConfig.screenshotName) + "_"+ str(self.page) + ".jpg"))):
                shutil.copyfile(os.path.join(self.simulFolder,str(self.reportConfig.screenshotName) + "_"+str(self.page)+".jpg"),os.path.join(Config.ReportFolder,self.saveFolder,str(self.reportConfig.screenshotName) + "_"+str(self.page)+".jpg"))

        if os.path.isfile(os.path.join(self.saveFolder,str(str(self.reportConfig.screenshotName) + "_"+ str(self.page) + ".jpg"))):
            pixmap = QtGui.QPixmap(os.path.join(self.saveFolder,str(str(self.reportConfig.screenshotName) + "_"+ str(self.page) + ".jpg")))
            painter.drawPixmap(self.rect(), pixmap)
            
            self.resize(pixmap.width(),pixmap.height())
            self.penRectangle = QtGui.QPen(QtCore.Qt.red)
            self.penRectangle.setWidth(3)
            painter.setPen(self.penRectangle)
            
            painter.setPen(QtGui.QColor(168, 34, 3))
            
            for i in range (2,len(self.word_tab)):
                if int(self.word_tab[i][5])==self.page:                
                    painter.drawRect(int(self.word_tab[i][1]),int(self.word_tab[i][2]),int(self.word_tab[i][3]),int(self.word_tab[i][4]))

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(50,loop.quit)
            loop.exec_()
            
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(self.winId())#screen.grabWindow(QtWidgets.QApplication.desktop().winId(), 0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
            screenshot.save(os.path.join(Config.ReportFolder,self.saveFolder,str(str(self.reportConfig.wordScreenshot)+"_"+ str(self.page)+"."+Config.screenshotExtension)), str(Config.screenshotExtension))
        self.ready=False


def helpHtml():
    webbrowser.open_new_tab('file://'+str(Config.documentationReport))
    
#help windows
class Help(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Help Windows')
        self.width=500
        self.height=300
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.Label = QtWidgets.QLabel("the folder generated will contain:\n\n"
                                      "-the audio and video of the recording\n\n"
                                      "-screenshots of the text alone and with gazes and fixations on top\n\n"
                                      "-csv files of the gazes, velocitygazes, fixations, faces and eyes positions\n\n"
                                      "-a 'Report.txt' file with all the information about the recording")
        self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.Label,0,0)
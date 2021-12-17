#EyeTracker.py => test and capture the data from Eye Tracker
#EyeTrackerRecordThread => EyeTracker record Thread
#TestCalibrationWindows => EyeTracker calibration test
#EyeTrackerTest => choose eyeTracker to test in parameters windows
#EyeTrackerTrace class => display eye tracker data and save them
#CreatePage => Eye Tracker CSV processing

import os, sys, threading, subprocess, csv, time, shutil
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
import Config, VelocityInDeg, Buscher, Nystrom

#eye tracker for simulation
class EyeTrackerRecordThread(threading.Thread):
    def __init__(self,windowsX, windowsY, saveReport, saveReportHead):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):
        threading.Thread.__init__(self)
        self.windowsX = windowsX
        self.windowsY = windowsY
        #self.x0 = x0
        #self.y0 = y0
        #self.appX = appX
        #self.appY = appY
        self.saveReport = saveReport
        self.saveReportHead = saveReportHead
        self._stopevent = threading.Event( )

    #run during thread
    def run(self):
        previous = os.getcwd()
        
        if Config.eyeTrackerSdkPro:
            os.chdir(Config.sdkPro)
            #cmd = str(os.path.join(os.getcwd(),"eye_got_it",str("eye_got_it.exe " + str(self.windowsX) + " "  + str(self.windowsY) + " " + str(self.x0) + " " + str(self.y0 )+ " " + str(self.appX) + " " + str(self.appY) + " "+ str(self.saveReport))))
            cmd = str(os.path.join(os.getcwd(),str("eyeTrackerPro.exe " + str(self.windowsX) + " "  + str(self.windowsY) + " "+ str(self.saveReport) + " " + str(self.saveReportHead))))
        
            self.thread = subprocess.Popen(cmd, shell=False)
        else :
            os.chdir(Config.interactionLibrary)
            #cmd = str(os.path.join(os.getcwd(),"eye_got_it",str("eye_got_it.exe " + str(self.windowsX) + " "  + str(self.windowsY) + " " + str(self.x0) + " " + str(self.y0 )+ " " + str(self.appX) + " " + str(self.appY) + " "+ str(self.saveReport))))
            cmd = str(os.path.join(os.getcwd(),str("eyeTracker.exe " + str(self.windowsX) + " "  + str(self.windowsY) + " "+ str(self.saveReport) + " " + str(self.saveReportHead))))
        
            self.thread = subprocess.Popen(cmd, shell=False)

        os.chdir(previous)
        while self.thread.poll() is None:
            pass
        print("eyetracker thread end")

    #stop
    def stop(self):
        self._stopevent.set( )  
        self.thread.terminate() 

#this window allow the user to test the calibration of the eye tracker
class TestCalibrationWindows(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        #we check if these two temporary files exist and if so we erase them
        if os.path.exists(os.path.join(os.getcwd(),Config.eyeTrackerCalibration)):
            os.remove(os.path.join(os.getcwd(),Config.eyeTrackerCalibration))
        if os.path.exists(os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration)):
            os.remove(os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration))
        
        
        self.drawLines=True
        self.drawGazes=False
        self.gazes=[]
        self.x0=int(Config.SCREEN_WIDTH/2-Config.SCREEN_WIDTH_SIMULATION/2)
        self.y0=int(Config.SCREEN_HEIGHT/2-Config.SCREEN_HEIGHT_SIMULATION/2)

        self.setWindowTitle("calibration test")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setGeometry(Config.SCREEN_WIDTH/2-Config.SCREEN_WIDTH_SIMULATION/2,Config.SCREEN_HEIGHT/2-Config.SCREEN_HEIGHT_SIMULATION/2,Config.SCREEN_WIDTH_SIMULATION,Config.SCREEN_HEIGHT_SIMULATION)
        self.setFixedSize(Config.SCREEN_WIDTH_SIMULATION,Config.SCREEN_HEIGHT_SIMULATION)

        self.instruction = QtWidgets.QLabel('click on start test and follow the lines with your eyes, then click on stop test or press enter',self)
        self.instruction.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.instruction.setGeometry(10,0, 1300, 30)

        self.start = QtWidgets.QPushButton('start test', self)
        self.start.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.start.setGeometry(10, 30, 200, 30)
        self.start.clicked.connect(self.start_click)
        self.start.setEnabled(True)

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.back.setGeometry(10, 610, 200, 30)
        self.back.clicked.connect(self.close)
        self.back.setEnabled(True)

        self.stop = QtWidgets.QPushButton('stop test', self)
        self.stop.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.stop.setGeometry(1160, 610, 200, 30)
        self.stop.clicked.connect(self.stop_click)
        self.stop.setEnabled(False)



    def start_click(self):
        #we check if these two temporary files exist and if so we erase them
        if os.path.exists(os.path.join(os.getcwd(),Config.eyeTrackerCalibration)):
            os.remove(os.path.join(os.getcwd(),Config.eyeTrackerCalibration))
        if os.path.exists(os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration)):
            os.remove(os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration))

        self.stop.setEnabled(True)
        self.start.setEnabled(False)

        saveCSV = os.path.join(os.getcwd(),Config.eyeTrackerCalibration)
        saveCSV = str('"' + saveCSV + '"')
        saveCSV2 = os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration)
        saveCSV2 = str('"' + saveCSV2 + '"')   
        self.thread=EyeTrackerRecordThread(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT,saveCSV,saveCSV2)
        self.thread.start()

        self.drawLines=False
        self.drawGazes=False
        self.update()
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(2700,loop.quit)
        loop.exec_()
        self.drawLines=True
        self.update()

    def stop_click(self):
        self.drawGazes=True
        self.stop.setEnabled(False)
        self.start.setEnabled(True)
        self.thread.stop()
        self.gazes=[]
        if os.path.isfile(os.path.join(os.getcwd(),Config.eyeTrackerCalibration)):
            with open(str(os.path.join(os.getcwd(),Config.eyeTrackerCalibration)), 'r', newline='') as csvfile:
                fileUser = csv.reader(csvfile, delimiter=',') 
                self.gazes = [line for line in fileUser if line[2]=='valid']
                csvfile.close()
        self.update()
        self.instruction.setText("if the red points follow the lines you can click on start recording, if not do the calibration again")
        
    def paintEvent(self, event): # event de type QPaintEvent
        painter = QtGui.QPainter(self) # recupere le QPainter du widget
        painter.setPen(QtGui.QColor(0, 0, 0))

        rect=QtCore.QRect(0,0,Config.SCREEN_WIDTH_SIMULATION,Config.SCREEN_HEIGHT_SIMULATION)
        painter.eraseRect(rect)
        
        if self.drawLines:
            for i in range (0,2):
                painter.drawLine(30,150+370*i,1330,150+370*i)

        if self.drawGazes:
            pen = QtGui.QPen()
            pen.setWidth(2)
            pen.setColor(QtGui.QColor(255,0,0))
            painter.setPen(pen)
            for i in range (0,len(self.gazes)):
                center=QtCore.QPoint( float(self.gazes[i][0])-self.x0 , float(self.gazes[i][1])-self.y0 )
                painter.drawEllipse( center,2,2 )

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return: 
            print("enter pressed")
            self.stop_click()
        event.accept()

    def closeEvent(self,event):
        #we check if these two temporary files exist and if so we erase them
        try:
            self.thread.stop()
            time.sleep(0.1)
        except:
            pass
        try:
            if os.path.exists(os.path.join(os.getcwd(),Config.eyeTrackerCalibration)):
                os.remove(os.path.join(os.getcwd(),Config.eyeTrackerCalibration))
        except:
            pass
        try:
            if os.path.exists(os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration)):
                os.remove(os.path.join(os.getcwd(),Config.eyeTrackerHeadCalibration))
        except:
            pass

#windows to test eye tracker
class EyeTrackerTest(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.testStop=False
        self.testStart = False

        #windows config
        self.setWindowTitle("Eye Tracker Test")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=500
        self.height=200
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.eyeTracker = QtWidgets.QLabel("Choose Eye Tracker",self)
        self.eyeTracker.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.eyeTracker, 0,0)

        self.eyeTrackerEdit = QtWidgets.QComboBox(self)
        self.eyeTrackerEdit.addItems(Config.eyeTrackerList)
        self.eyeTrackerEdit.setCurrentIndex(-1)
        self.eyeTrackerEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.eyeTrackerEdit, 0,1)
        self.eyeTrackerEdit.currentIndexChanged[int].connect(self.on_currentIndexChangedEyeTrackerEdit)
        self.eyeTrackerEditSelect=False
        self.eyeTrackerEdit.setEnabled(True)

        self.test = QtWidgets.QPushButton('Test', self)
        self.test.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.test, 1,0,1,2)
        self.test.clicked.connect(self.test_click)
        self.test.setEnabled(False)


    def on_currentIndexChangedEyeTrackerEdit(self,index):
        if self.eyeTrackerEdit.currentText() != "":
            self.eyeTrackerEditSelect = True
            self.test.setEnabled(True)

        else:
            self.eyeTrackerEditSelect=False
            self.test.setEnabled(False)

    #start the test
    def test_click(self):
        Config.eyeTrackerSdkPro = True if (self.eyeTrackerEdit.currentText() == Config.eyeTrackerList[0]) else False

        self.eyeTrackerTest = TestCalibrationWindows()
        self.eyeTrackerTest.show()

#display eye tracker data and save them
class EyeTrackerTrace(QtWidgets.QWidget):
    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)
    def __init__(self,reportConfig):
        QtWidgets.QWidget.__init__(self)
        self.simulFolder = reportConfig[0].simulFolder
        self.saveFolder = reportConfig[0].reportName
        self.page=0
        self.pageMax = reportConfig[0].pageMax
        self.x0 = reportConfig[0].x0
        self.y0 = reportConfig[0].y0
        self.width=Config.SCREEN_WIDTH_SIMULATION
        self.height=Config.SCREEN_HEIGHT_SIMULATION
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.ready=True
        self.reportConfigMain = reportConfig
        self.reportConfig = reportConfig[0]
        self.algorithmMain = reportConfig[0].algorithm
        self.algorithm = self.algorithmMain[0]
        self.algo=0
        self.show()
        self.i=0
        self.start=False 

    def drawText(self, event, painter):
        if os.path.isfile(os.path.join(self.saveFolder,str(str(self.reportConfig.screenshotName) + "_"+ str(self.page) + ".jpg"))):
            if os.path.isfile(os.path.join(self.simulFolder,str(str(self.reportConfig.screenshotName) + "_"+ str(self.page) + ".jpg"))):
                shutil.copyfile(os.path.join(self.simulFolder,str(self.reportConfig.screenshotName) + "_"+str(self.page)+".jpg"),os.path.join(Config.ReportFolder,self.saveFolder,str(self.reportConfig.screenshotName) + "_"+str(self.page)+".jpg"))

        if (os.path.isfile(os.path.join(self.saveFolder,str(self.reportConfig.screenshotName) + "_"+str(self.page)+".jpg"))):
            pixmap = QtGui.QPixmap(os.path.join(self.saveFolder,str(self.reportConfig.screenshotName) + "_"+str(self.page)+".jpg"))
            painter.drawPixmap(self.rect(), pixmap)
            #self.resize(pixmap.width(),pixmap.height())
            pen = QtGui.QPen()
            painter.setPen(pen)
            
            gazes=[]
            if os.path.isfile(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerData) + "_"+str(self.page)+".csv"))):
                with open(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerData) + "_"+str(self.page)+".csv"))), 'r', newline='') as csvfile:
                        fileUser = csv.reader(csvfile, delimiter=',') 
                        gazes = [line for line in fileUser if line[2]=='valid']
                        csvfile.close()
            fixTab=[]
            if os.path.isfile(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerFixations)+"_"+str(self.page)+".csv")))):
                with open(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerFixations) + "_"+ str(self.page) + ".csv"))), 'r', newline='') as csvfile:
                    fileUser = csv.reader(csvfile, delimiter=',') 
                    fixTab = [line for line in fileUser]
                    fixTab.pop(0)
                    csvfile.close()

            pen.setWidth(2)
            pen.setColor(QtGui.QColor(255,0,0))
            painter.setPen(pen)
            for i in range (0,len(gazes)):
                center=QtCore.QPoint( float(gazes[i][0]) , float(gazes[i][1]) )
                painter.drawEllipse( center,2,2 )

            if self.algorithm=="nystrom":
                if os.path.isfile(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerSaccades)+"_"+str(self.page)+".csv")))):
                    with open(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerSaccades)+"_"+str(self.page)+".csv"))), 'r', newline='') as csvfile:
                        fileUser = csv.reader(csvfile, delimiter=',') 
                        sacTab = [line for line in fileUser]
                        sacTab.pop(0)
                        csvfile.close()

                    center=QtCore.QPoint()
                    temp=QtCore.QPoint()
                    for i in range (0,len(sacTab)):
                        if (float(sacTab[i][0]) >= self.x0 and float(sacTab[i][0]) <= self.x0 + Config.SCREEN_WIDTH_SIMULATION) and (float(sacTab[i][1]) >= self.y0 and float(sacTab[i][1]) <= self.y0 + Config.SCREEN_HEIGHT_SIMULATION) :
                            temp = QtCore.QPoint( float(sacTab[i][0])-self.x0 , float(sacTab[i][1])-self.y0 )
                            center = QtCore.QPoint( float(sacTab[i][2])-self.x0 , float(sacTab[i][3])-self.y0 )

                            pen.setWidth(2)
                            pen.setColor(QtGui.QColor(120,0,255))
                            painter.setPen(pen)
                            painter.drawLines(temp,center)

                if os.path.isfile(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerGlissades)+"_"+str(self.page)+".csv")))):
                    with open(str(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerGlissades)+"_"+str(self.page)+".csv"))), 'r', newline='') as csvfile:
                        fileUser = csv.reader(csvfile, delimiter=',') 
                        gliTab = [line for line in fileUser]
                        gliTab.pop(0)
                        csvfile.close()

                    center=QtCore.QPoint()
                    temp=QtCore.QPoint()
                    for i in range (0,len(gliTab)):
                        if (float(gliTab[i][0]) >= self.x0 and float(gliTab[i][0]) <= self.x0 + Config.SCREEN_WIDTH_SIMULATION) and (float(gliTab[i][1]) >= self.y0 and float(gliTab[i][1]) <= self.y0 + Config.SCREEN_HEIGHT_SIMULATION) :
                            temp = QtCore.QPoint( float(gliTab[i][0])-self.x0 , float(gliTab[i][1])-self.y0 )
                            center = QtCore.QPoint( float(gliTab[i][2])-self.x0 , float(gliTab[i][3])-self.y0 )

                            pen.setWidth(2)
                            pen.setColor(QtGui.QColor(0,255,0))
                            painter.setPen(pen)
                            painter.drawLines(temp,center)

            center=QtCore.QPoint()
            temp=QtCore.QPoint()
            
            for i in range (0,len(fixTab)):
                temp = center
                center=QtCore.QPoint( float(fixTab[i][0]) , float(fixTab[i][1]))
                if self.algorithm=="buscher":
                    pen.setWidth(2)
                    pen.setColor(QtGui.QColor(120,0,255))
                    painter.setPen(pen)
                    painter.drawLines(temp,center)
                pen.setWidth(3)
                pen.setColor(QtGui.QColor(0,0,255))
                painter.setPen(pen)
                painter.drawEllipse(center,int(fixTab[i][2])/10000,int(fixTab[i][2])/10000)

            
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(50,loop.quit)
            loop.exec_()
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(self.winId())#screen.grabWindow(QtWidgets.QApplication.desktop().winId(), 0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
            screenshot.save(os.path.join(Config.ReportFolder,self.saveFolder,self.algorithm,str(str(self.reportConfig.eyeTrackerScreenshot)+"_"+ str(self.page)+"."+Config.screenshotExtension)), str(Config.screenshotExtension))
        self.ready = False
        


    def paintEvent(self, event):
        if not self.start:
            self.processing.emit("Start Eye Tracker Processing")
            self.start=True

        if self.ready:
            if self.page>=self.pageMax :
                if self.algo <len(self.algorithmMain)-1:
                    self.algo+=1
                    self.algorithm = self.algorithmMain[self.algo]
                    self.reportConfig = self.reportConfigMain[self.i] 
                    self.simulFolder = self.reportConfig.simulFolder
                    self.saveFolder = self.reportConfig.reportName
                    self.page=0
                    self.pageMax = self.reportConfig.pageMax
                    self.ready=True
                    self.x0 = self.reportConfig.x0
                    self.y0 = self.reportConfig.y0
                    self.hide()
                    self.show()

                elif self.i == len(self.reportConfigMain) -1 :
                
                    self.processing.emit(str("     " + str(os.path.split(self.saveFolder)[1]) + " done"))
                    self.processing.emit(str("End Eye Tracker Processing\n"))
                    self.finished.emit(1)
                    self.close()

                else:
                    self.i +=1
                    self.algo=0
                    self.algorithm = self.algorithmMain[self.algo]
                    self.processing.emit(str("     " + str(os.path.split(self.saveFolder)[1]) + " done"))
                    self.reportConfig = self.reportConfigMain[self.i] 
                    self.simulFolder = self.reportConfig.simulFolder
                    self.saveFolder = self.reportConfig.reportName
                    self.page=0
                    self.pageMax = self.reportConfig.pageMax
                    self.ready=True
                    self.x0 = self.reportConfig.x0
                    self.y0 = self.reportConfig.y0
                    self.hide()
                    self.show()
            else:    
                painter = QtGui.QPainter()
                painter.begin(self)
                #print("current page " + str(self.page))
                self.drawText(event, painter)
                painter.end()
        
        else :
            
            """
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1000,loop.quit)
            
            print(Function.current_milli_time)
            loop.exec_()
            print(Function.current_milli_time)"""
            if self.page < self.pageMax:
                self.page+=1
                self.ready = True
                self.hide()
                self.show()
                #self.update()
                """
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(1000,loop.quit)
                
                print(Function.current_milli_time)
                loop.exec_()
                print(Function.current_milli_time)"""
    """
    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_D or event.key() == QtCore.Qt.Key_E) and self.ready:
            if self.page <self.pageMax - 1:
                self.page+=1
                self.hide()
                self.show()
                self.ready=False
            else :
                self.close()
                self.reportWordWindows = ReportWord(self,self.simulFolder,self.pageMax,self.saveFolder)
                self.reportWordWindows.show()   
    """

#Eye Tracker CSV processing
class CreatePage (QtCore.QThread):
    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)


    def __init__(self,reportConfig):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):
        self.percentageGazesBuscher = 0
        self.percentageGazesNystrom = 0
        self.reportConfigMain = reportConfig
        super(CreatePage, self).__init__()
        self.reportConfigProcess = []
        
        
    def run(self):
        returnBool = True
        firstTime=""
        firstTime2=""
        self.processing.emit(str("Start Eye Tracker Page Creation"))
        for reportConfig in self.reportConfigMain:
            if  reportConfig.allowEyeTracker:
                if os.path.isfile(str(os.path.join(reportConfig.simulFolder, str(reportConfig.eyeTrackerData + "." + Config.eyeTrackerDataFile)))) and os.path.isfile(str(os.path.join(reportConfig.simulFolder, str(reportConfig.eyeTrackerHeadData + "." + Config.eyeTrackerDataFile)))):
                    for algorithm in reportConfig.algorithm:
                        returnBool = True
                        gazes=[]
                        fixTab=[]
                        firstTime=""
                        firstTime2=""
                        #extract gazes data from csv
                        if os.path.isfile(str(os.path.join(reportConfig.simulFolder, str(reportConfig.eyeTrackerData + "." + Config.eyeTrackerDataFile)))):
                            with open(str(os.path.join(reportConfig.simulFolder, str(reportConfig.eyeTrackerData + "." + Config.eyeTrackerDataFile))), 'r', newline='') as csvfile:
                                fileUser = csv.reader(csvfile, delimiter=',')
                                lines = [line for line in fileUser]
                                headerGazes = lines[0]
                                gazes = [line for line in lines if line[2]=='valid']    
                                #print(headerGazes)
                                csvfile.close()
                        #check if gaze csv is empty
                        if len(gazes) > 1:
                            #create fixation with buscher
                            if algorithm=="buscher":
                                fixTab, self.percentageGazesBuscher = Buscher.fixationBuscher2008(gazes)
                                #print("Le %\ dans eye tracker", self.percentageGazes)

                            #extract head gaze data from csv and create convertedGazes wich hold the velocity and acceleration
                            if os.path.isfile(str(os.path.join(reportConfig.simulFolder, str(reportConfig.eyeTrackerHeadData + "." + Config.eyeTrackerDataFile)))):
                                with open(str(os.path.join(reportConfig.simulFolder, str(reportConfig.eyeTrackerHeadData + "." + Config.eyeTrackerDataFile))), 'r', newline='') as csvfile:
                                    fileUser = csv.reader(csvfile, delimiter=',') 
                                    lines = [line for line in fileUser]
                                    headerHeadGazes = lines[0]
                                    headGazes = [line for line in lines if line[3]=='valid']
                                    convertedGazes = VelocityInDeg.VelocityInDeg(gazes,headGazes)
                                    if not convertedGazes:
                                        reportConfig.headPositionValidity=True
                                    csvfile.close()

                            if convertedGazes:
                                    
                                #create velocityGazes csv
                                with open(str(os.path.join(reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerVelocityGazes)+".csv"))), 'w', newline='') as csvfile:
                                    fileUser = csv.writer(csvfile, delimiter=',',)
                                    headerVelocityGazes = ["x","y","timestamp_us","velocity","acceleration","unix_time_ms"]
                                    fileUser.writerow(headerVelocityGazes)
                                    for i in range(0,len(convertedGazes)):
                                        fileUser.writerow(convertedGazes[i])
                                        #fileUser.writerow([float(convertedGazes[i][0]),float(convertedGazes[i][1]),convertedGazes[i][2],convertedGazes[i][3],convertedGazes[i][4],convertedGazes[i][5]])
                                csvfile.close()
                                
                                #seperate velocityGazes in multiple pages
                                currentTime=1
                                page=[]
                                tempPage=[]
                                
                                for i in range(0,len(convertedGazes)):
                                    if currentTime <= len(reportConfig.timeSimul)-1:
                                        if int(convertedGazes[i][5]) >= (int(reportConfig.timeSimul[currentTime-1])) and int(convertedGazes[i][5]) < int(reportConfig.timeSimul[currentTime]):
                                            tempPage.append(convertedGazes[i])
                                        if int(convertedGazes[i][5]) >= int(reportConfig.timeSimul[currentTime]) or i == len(convertedGazes)-1:
                                            page.append(tempPage)
                                            tempPage=[]
                                            currentTime+=1
                                            tempPage.append(convertedGazes[i])
                            
                                for currentPage in range(0,len(page)):
                                    with open(str(os.path.join(reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerVelocityGazes)+"_"+str(currentPage)+".csv"))), 'w', newline='') as csvfile:
                                        fileUser = csv.writer(csvfile, delimiter=',',)
                                        fileUser.writerow(headerVelocityGazes)
                                        for i in range(0,len(page[currentPage])):
                                            if (float(page[currentPage][i][0]) >= reportConfig.x0 and float(page[currentPage][i][0]) <= reportConfig.x0 + Config.SCREEN_WIDTH_SIMULATION) and (float(page[currentPage][i][0]) >= reportConfig.y0 and float(page[currentPage][i][1]) <= reportConfig.y0 + Config.SCREEN_HEIGHT_SIMULATION):
                                            
                                                fileUser.writerow([float(page[currentPage][i][0]) - reportConfig.x0 , float(page[currentPage][i][1]) - reportConfig.y0 ,page[currentPage][i][2],page[currentPage][i][3],page[currentPage][i][4],page[currentPage][i][5]])
                                    csvfile.close()

                                if algorithm=="nystrom":
                                    sacTab,gliTab,fixTab, self.percentageGazesNystrom = Nystrom.Nystrom(convertedGazes)
                                    """
                                    print('taille tableau de headGazes : ',len(headGazes))
                                    print('taille tableau de saccades : ',len(sacTab))
                                    print('taille tableau de glissades : ',len(gliTab))
                                    print('taille tableau de fixations : ',len(fixTab))
                                    print('taille tableau de convertedGazes : ',len(convertedGazes))
                                    """
                                    #create saccades csv
                                    with open(str(os.path.join(reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerSaccades)+".csv"))), 'w', newline='') as csvfile:
                                        fileUser = csv.writer(csvfile, delimiter=',',)
                                        headerSaccades = ["x1","y1","x2","y2","duration","unix_time_ms"]
                                        fileUser.writerow(headerSaccades)
                                        for i in range(0,len(sacTab)):
                                            fileUser.writerow(sacTab[i])
                                            #fileUser.writerow([sacTab[i][0],sacTab[i][1],sacTab[i][2],sacTab[i][3],sacTab[i][4],sacTab[i][5]])
                                        csvfile.close()
                                    #seperate saccades in multiple pages
                                    if len(sacTab) > 1:
                                        currentTime=1
                                        page=[]
                                        tempPage=[]
                                        header = sacTab[0]
                                        for i in range(1,len(sacTab)):
                                            if currentTime <= len(reportConfig.timeSimul)-1:
                                                if int(sacTab[i][5]) >= (int(reportConfig.timeSimul[currentTime-1])) and int(sacTab[i][5]) <= int(reportConfig.timeSimul[currentTime]):
                                                    tempPage.append(sacTab[i])
                                                if int(sacTab[i][5]) > int(reportConfig.timeSimul[currentTime]) or i == len(sacTab)-1:
                                                    page.append(tempPage)
                                                    tempPage=[]
                                                    tempPage.append(sacTab[i])
                                                    currentTime+=1
                                                
                                        for currentPage in range(0,len(page)):
                                            with open(str(os.path.join(Config.ReportFolder,reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerSaccades) + "_"+ str(currentPage) + "." + Config.eyeTrackerDataFile))), 'w', newline='') as csvfile:
                                                fileUser = csv.writer(csvfile, delimiter=',',)
                                                fileUser.writerow(headerSaccades)
                                                #fileUser.writerow([headerSaccades[0],headerSaccades[1],headerSaccades[2],headerSaccades[3],headerSaccades[4],headerSaccades[5]])
                                                for i in range(0,len(page[currentPage])):
                                                    fileUser.writerow(page[currentPage][i])
                                                    #fileUser.writerow([page[currentPage][i][0],page[currentPage][i][1],page[currentPage][i][2],page[currentPage][i][3],page[currentPage][i][4],page[currentPage][i][5]])
                                    
                                    #else :
                                    #    returnBool = False

                                    #create glissades csv
                                    with open(str(os.path.join(reportConfig.reportName,algorithm,str(reportConfig.eyeTrackerGlissades)+".csv")), 'w', newline='') as csvfile:
                                        fileUser = csv.writer(csvfile, delimiter=',',)
                                        headerGlissades = ["x1","y1","x2","y2","duration","unix_time_ms"]
                                        fileUser.writerow(headerGlissades)
                                        for i in range(0,len(gliTab)):
                                            fileUser.writerow(gliTab)
                                            #fileUser.writerow([gliTab[i][0],gliTab[i][1],gliTab[i][2],gliTab[i][3],gliTab[i][4],gliTab[i][5]])
                                        csvfile.close()
                                    #seperate glissades in multiple pages
                                    if len(gliTab) > 1:
                                        currentTime=1
                                        page=[]
                                        tempPage=[]
                                        header = gliTab[0]
                                        for i in range(1,len(gliTab)):
                                            if currentTime <= len(reportConfig.timeSimul)-1:
                                                if int(gliTab[i][5]) >= (int(reportConfig.timeSimul[currentTime-1])) and int(gliTab[i][5]) <= int(reportConfig.timeSimul[currentTime]):
                                                    tempPage.append(gliTab[i])
                                                if int(gliTab[i][5]) > int(reportConfig.timeSimul[currentTime]) or i == len(gliTab)-1:
                                                    page.append(tempPage)
                                                    tempPage=[]
                                                    tempPage.append(gliTab[i])
                                                    currentTime+=1
                                        for currentPage in range(0,len(page)):
                                            with open(str(os.path.join(Config.ReportFolder,reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerGlissades) + "_"+ str(currentPage) + "." + Config.eyeTrackerDataFile))), 'w', newline='') as csvfile:
                                                fileUser = csv.writer(csvfile, delimiter=',',)
                                                fileUser.writerow(headerGlissades)
                                                #fileUser.writerow([headerGlissades[0],headerGlissades[1],headerGlissades[2],headerGlissades[3],headerGlissades[4],headerGlissades[5]])
                                                for i in range(0,len(page[currentPage])):
                                                    fileUser.writerow(page[currentPage][i])
                                                    #fileUser.writerow([page[currentPage][i][0],page[currentPage][i][1],page[currentPage][i][2],page[currentPage][i][3],page[currentPage][i][4],page[currentPage][i][5]])
                        
                            with open(str(os.path.join(reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerFixations)+".csv"))), 'w', newline='') as csvfile:
                                fileUser = csv.writer(csvfile, delimiter=',',)
                                headerFixations = ["x","y","duration_us","unix_time_ms"]
                                fileUser.writerow(headerFixations)
                                for i in range(0,len(fixTab)):
                                    fileUser.writerow(fixTab[i])
                                    #fileUser.writerow([int(fixTab[i][0]),int(fixTab[i][1]),fixTab[i][2],fixTab[i][3]])
                                csvfile.close()

                            #seperate fixations in multiple pages
                            
                            if len(fixTab) > 1:
                                currentTime=1
                                page=[]
                                tempPage=[]
                                headerFixTab = fixTab[0]

                                for i in range(1,len(fixTab)):
                                    if currentTime <= len(reportConfig.timeSimul)-1:
                                        if int(fixTab[i][3]) >= (int(reportConfig.timeSimul[currentTime-1])) and int(fixTab[i][3]) <= int(reportConfig.timeSimul[currentTime]):
                                            tempPage.append(fixTab[i])
                                        if int(fixTab[i][3]) > int(reportConfig.timeSimul[currentTime]) or i == len(fixTab)-1:
                                            page.append(tempPage)
                                            tempPage=[]
                                            currentTime+=1
                                            tempPage.append(fixTab[i])


                                for currentPage in range(0,len(page)):
                                    with open(str(os.path.join(Config.ReportFolder,reportConfig.reportName,algorithm,str(str(reportConfig.eyeTrackerFixations)+"_"+ str(currentPage) + "." + Config.eyeTrackerDataFile))), 'w', newline='') as csvfile:
                                        fileUser = csv.writer(csvfile, delimiter=',',)
                                        fileUser.writerow([headerFixations[0],headerFixations[1],headerFixations[2],headerFixations[3]])
                                        for i in range(0,len(page[currentPage])):
                                            if (float(page[currentPage][i][0]) >= reportConfig.x0 and float(page[currentPage][i][0]) <= reportConfig.x0 + Config.SCREEN_WIDTH_SIMULATION) and (float(page[currentPage][i][1]) >= reportConfig.y0 and float(page[currentPage][i][1]) <= reportConfig.y0 + Config.SCREEN_HEIGHT_SIMULATION) :
                                                page[currentPage][i][0] = float(page[currentPage][i][0]) - reportConfig.x0
                                                page[currentPage][i][1] = float(page[currentPage][i][1]) - reportConfig.y0
                                                fileUser.writerow(page[currentPage][i])
                                                #fileUser.writerow([float(page[currentPage][i][0]) - reportConfig.x0 ,float(page[currentPage][i][1]) - reportConfig.y0,page[currentPage][i][2],page[currentPage][i][3]])

                            #else :
                            #    returnBool = False

                            

                            #Eye Tracker eye processing separate in page
                            first=True
                            

                            currentTime=1
                            page=[]
                            tempPage=[]
                            #headerGazes = gazes[0]
                            
                            for i in range(1,len(gazes)):

                                if currentTime <= len(reportConfig.timeSimul)-1:
                                    if int(gazes[i][4]) >= (int(reportConfig.timeSimul[currentTime-1])) and int(gazes[i][4]) < int(reportConfig.timeSimul[currentTime]):
                                        tempPage.append(gazes[i])

                                    if int(gazes[i][4]) >= int(reportConfig.timeSimul[currentTime]) or i == len(gazes)-1:
                                        page.append(tempPage)
                                        tempPage=[]
                                        currentTime+=1
                                        tempPage.append(gazes[i])
                            
                            firstTime = page[0][0][4]
                            
                            for currentPage in range(0,len(page)):
                                #print(currentPage)
                                with open(str(os.path.join(Config.ReportFolder,reportConfig.reportName,algorithm,str(reportConfig.eyeTrackerData + "_"+ str(currentPage) + "." + Config.eyeTrackerDataFile))), 'w', newline='') as csvfile:
                                    fileUser = csv.writer(csvfile, delimiter=',',)
                                    fileUser.writerow(headerGazes)
                                    #fileUser.writerow([headerGazes[0],headerGazes[1],headerGazes[2],headerGazes[3],headerGazes[4]])
                                    for i in range(0,len(page[currentPage])):
                                        
                                        if (float(page[currentPage][i][0]) >= reportConfig.x0 and float(page[currentPage][i][0]) <= reportConfig.x0 + Config.SCREEN_WIDTH_SIMULATION) and (float(page[currentPage][i][0]) >= reportConfig.y0 and float(page[currentPage][i][1]) <= reportConfig.y0 + Config.SCREEN_HEIGHT_SIMULATION) and page[currentPage][i][2] == 'valid':
                                            page[currentPage][i][0] = float(page[currentPage][i][0]) - reportConfig.x0
                                            page[currentPage][i][1] = float(page[currentPage][i][1]) - reportConfig.y0
                                            fileUser.writerow(page[currentPage][i])
                                            #fileUser.writerow([float(page[currentPage][i][0]) - reportConfig.x0 ,float(page[currentPage][i][1]) - reportConfig.y0,page[currentPage][i][2],page[currentPage][i][3],page[currentPage][i][4]])
                                        #csvfile.close()
                            

                            #Eye Tracker head processing separate in page
                            first2=True
                            #headerHead = headGazes[0]
                            

                            if len(headGazes) > 1:
                                if headGazes[1] !=[]:
                                    currentTime=1
                                    page=[]
                                    tempPage=[]
                                    
                                    for i in range(1,len(headGazes)):
                                        if currentTime <= len(reportConfig.timeSimul)-1:
                                            if int(headGazes[i][5]) >= (int(reportConfig.timeSimul[currentTime-1])) and int(headGazes[i][5]) <= int(reportConfig.timeSimul[currentTime]):
                                                tempPage.append(headGazes[i])

                                            if int(headGazes[i][5]) > int(reportConfig.timeSimul[currentTime]) or i == len(headGazes)-1:
                                                page.append(tempPage)
                                                tempPage=[]
                                                tempPage.append(headGazes[i])
                                                currentTime+=1

                                    firstTime2 = page[0][0][5]

                                    for currentPage in range(0,len(page)):
                                        with open(str(os.path.join(Config.ReportFolder,reportConfig.reportName,algorithm,str(reportConfig.eyeTrackerHeadData + "_"+ str(currentPage) + "." + Config.eyeTrackerDataFile))), 'w', newline='') as csvfile:
                                            fileUser = csv.writer(csvfile, delimiter=',',)
                                            fileUser.writerow(headerHeadGazes)
                                            #fileUser.writerow([headerHeadGazes[0],headerHeadGazes[1],headerHeadGazes[2],headerHeadGazes[3],headerHeadGazes[4],headerHeadGazes[5],headerHeadGazes[6],headerHeadGazes[7],headerHeadGazes[8],headerHeadGazes[9],headerHeadGazes[10],headerHeadGazes[11]])
                                            for i in range(0,len(page[currentPage])):
                                                if page[currentPage][i][3] == 'valid' and page[currentPage] !=[]:
                                                    fileUser.writerow(page[currentPage][i])
                                                    #fileUser.writerow([page[currentPage][i][0],page[currentPage][i][1],page[currentPage][i][2],page[currentPage][i][3],page[currentPage][i][4],page[currentPage][i][5],page[currentPage][i][6],page[currentPage][i][7],page[currentPage][i][8],page[currentPage][i][9],page[currentPage][i][10],page[currentPage][i][11]])

                        else :
                            returnBool = False
                    self.processing.emit(str("     " + str(os.path.split(reportConfig.simulFolder)[1]) + " done"))
                else :
                    returnBool=False 
                    firstTime=""
                    firstTime2=""
                reportConfig.createPageCSV=returnBool
                reportConfig.timeStartEye=firstTime
                reportConfig.timeStartHead=firstTime2
                
                
                
            self.reportConfigProcess.append(reportConfig)        
        #return returnBool, firstTime, firstTime2
        #self.allGood.emit(returnBool)
        #self.timeStartEye.emit(firstTime)
        #self.timeStartHead.emit(firstTime2)
        self.processing.emit(str("End Eye Tracker Page Creation\n" ))
        self.finished.emit(1)

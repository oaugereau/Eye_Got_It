#MachineLearning.py => Predic word in report mode

import sys, os, csv, time, shutil, threading, subprocess, webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.Qt import *
import Config, ConfigFileManagement
import pandas as pd
import numpy as np
import sklearn
from joblib import load

class MachineLearningProcess (QtCore.QThread):
    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)


    def __init__(self,reportConfig):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):

        super(MachineLearningProcess, self).__init__()#threading.Thread.__init__(self)
        self.reportConfig = reportConfig
      
        
    def run(self):
        if len(self.reportConfig)>0:      
            self.processing.emit("Start machine learning : " + str(self.reportConfig[0].model))

            
            for current in range(0,len(self.reportConfig)):
                process = []
                for algo in self.reportConfig[0].algorithm:
                    
                    for currentModel in range(0,len(self.reportConfig[0].model)):
                        if self.reportConfig[current].allowEyeTracker:
                            if os.path.isdir(os.path.join(self.reportConfig[current].reportName,algo)):

                                if not os.path.isdir(os.path.join(self.reportConfig[current].reportName,algo,self.reportConfig[current].model[currentModel])):
                                    os.mkdir(os.path.join(self.reportConfig[current].reportName,algo,self.reportConfig[current].model[currentModel]))
                                data=[]
                                wordData = []
                                if os.path.isfile(os.path.join(self.reportConfig[current].reportName,str(self.reportConfig[current].textPosition) + ".csv")):
                                    with open(str(os.path.join(self.reportConfig[current].reportName,str(self.reportConfig[current].textPosition) + ".csv")),'r', newline='') as csvfile:
                                            textPosition = csv.reader(csvfile, delimiter=',')
                                            wordData = [line for line in textPosition]

                                for (root,dirs,files) in os.walk(os.path.join(self.reportConfig[current].reportName,algo), topdown=True):
                                    #print('files in report folder: ',files)
                                    
                                    fixationData=[]
                                    eyeTrackerData=[]
                                    velocityData=[]
                                    for file in files:
                                        if str(str(self.reportConfig[current].eyeTrackerFixations) +"_") in file:
                                            print(file)
                                            with open(str(os.path.join(root,file)),'r',newline='') as csvfile:
                                                fixations = csv.reader(csvfile, delimiter=',')
                                                fixationPage = [line for line in fixations]
                                            fixationData.append(fixationPage)

                                        if (str(self.reportConfig[current].eyeTrackerData) + "_") in file:
                                            print(file)
                                            with open(str(os.path.join(root,file)),'r',newline='') as csvfile:
                                                eyeTracker = csv.reader(csvfile, delimiter=',')
                                                gazePage = [line for line in eyeTracker]
                                            eyeTrackerData.append(gazePage)

                                        if str(self.reportConfig[current].eyeTrackerVelocityGazes)+"_" in file:
                                            print(file)
                                            with open(str(os.path.join(root,file)),'r',newline='') as csvfile:
                                                velocityGazes = csv.reader(csvfile, delimiter=',')
                                                velocityPage = [line for line in velocityGazes]
                                            velocityData.append(velocityPage)


                                    for i in range(2,len(wordData)):
                                        temp=[]

                                        first=0
                                        temp.append(root)
                                        temp.append(wordData[i][0])
                                        temp.append(wordData[i][1])
                                        temp.append(wordData[i][2])
                                        temp.append(wordData[i][3])
                                        temp.append(wordData[i][4])
                                        temp.append(wordData[i][5])
                                        if int(wordData[i][1])==2:
                                            first=1
                                        temp.append(first)
                                        
                                        page=int(wordData[i][5])
                                        
                                        nbFixation=0
                                        duration=0
                                        if page<len(fixationData):
                                            for j in range (1,len(fixationData[page])):
                                                x=float(fixationData[page][j][0])
                                                y=float(fixationData[page][j][1])
                                                if x>int(wordData[i][1]) and x<int(wordData[i][1])+int(wordData[i][3]) and y>int(wordData[i][2]) and y<int(wordData[i][2])+int(wordData[i][4]):
                                                    nbFixation+=1
                                                    duration+=int(fixationData[page][j][2])
                                        temp.append(nbFixation)
                                        temp.append(duration)
                                        
                                        backward=0
                                        nbGaze=0
                                        continuous_group=[]
                                        continuous_group_temp=[]
                                        longest_continous_group=[]
                                        first_iteration=True
                                        if page<len(eyeTrackerData):
                                            for j in range (1,len(eyeTrackerData[page])):
                                                x=float(eyeTrackerData[page][j][0])
                                                y=float(eyeTrackerData[page][j][1])
                                                if x>int(wordData[i][1]) and x<int(wordData[i][1])+int(wordData[i][3]) and y>int(wordData[i][2]) and y<int(wordData[i][2])+int(wordData[i][4]):
                                                    nbGaze+=1
                                                    """if not first_iteration:
                                                        if x<float(eyeTrackerData[page][j-1][0]):
                                                            backward=1"""
                                                    continuous_group_temp.append(x)
                                                else:
                                                    if continuous_group_temp:
                                                        continuous_group.append(continuous_group_temp)
                                                        continuous_group_temp=[]
                                                first_iteration=False
                                        if continuous_group:
                                            longest_continous_group = max(continuous_group, key = len)
                                            for j in range(1,len(longest_continous_group)):
                                                if longest_continous_group[j]<longest_continous_group[j-1]:
                                                    backward+=1
                                        temp.append(nbGaze)
                                        temp.append(backward)

                                        nbGaze2=0
                                        velocity=[]
                                        maxVelocity=0
                                        meanVelocity=0
                                        standardDeviationVelocity=0
                                        acceleration=[]
                                        maxAcceleration=0
                                        meanAcceleration=0
                                        standardDeviationAcceleration=0
                                        if page<len(velocityData):
                                            for j in range (1,len(velocityData[page])):
                                                x=float(velocityData[page][j][0])
                                                y=float(velocityData[page][j][1])
                                                if x>int(wordData[i][1]) and x<int(wordData[i][1])+int(wordData[i][3]) and y>int(wordData[i][2]) and y<int(wordData[i][2])+int(wordData[i][4]):
                                                    nbGaze2+=1
                                                    velocity.append(float(velocityData[page][j][3]))
                                                    #meanVelocity+=float(velocityData[page][j][3])
                                                    acceleration.append(float(velocityData[page][j][4]))
                                                    #meanAcceleration+=float(velocityData[page][j][4])
                                        if nbGaze2>0:
                                            maxVelocity=max(velocity)
                                            maxAcceleration=max(acceleration)
                                            v=np.array(velocity)
                                            a=np.array(acceleration)
                                            #meanVelocity=(meanVelocity/nbGaze)
                                            meanVelocity=np.mean(v)
                                            standardDeviationVelocity=np.std(v)
                                            #meanAcceleration=(meanAcceleration/nbGaze)
                                            meanAcceleration=np.mean(a)
                                            standardDeviationAcceleration=np.std(a)
                                        temp.append(maxVelocity)
                                        temp.append(meanVelocity)
                                        temp.append(standardDeviationVelocity)
                                        temp.append(maxAcceleration)
                                        temp.append(meanAcceleration)
                                        temp.append(standardDeviationAcceleration)
                                        temp.append(nbGaze/int(wordData[i][3]))
                                        temp.append(nbFixation/int(wordData[i][3]))
                                        temp.append(duration/int(wordData[i][3]))

                                        data.append(temp)
                                    

                                print ('--------------------------------')
                                
                                with open(str(os.path.join(self.reportConfig[current].reportName,algo,self.reportConfig[current].model[currentModel],'dataFrame.csv')), 'w', newline='') as csvfile:
                                    df = csv.writer(csvfile, delimiter=',')
                                    df.writerow(["report_name","word","pos_x_word","pos_y_word","width_word","height_word","page","line_start","number_of_fixations","total_duration_fixation_us","number_of_gazes","backward_read","max_velocity_gaze","mean_velocity_gaze","standard_deviation_velocity","max_acceleration_gaze","mean_acceleration_gaze","standard_deviation_acceleration","gazes_lenght_ratio","fixations_lenght_ratio","duration_length_ratio"])
                                    for elem in data:
                                        df.writerow(elem)
                                
                                df = pd.read_csv(str(os.path.join(self.reportConfig[current].reportName,algo,self.reportConfig[current].model[currentModel],'dataFrame.csv')),header=0)
                                print(df.head())

                                configParser= ConfigFileManagement.ConfigFileRead(os.path.join(os.getcwd(),"model","modelConfig.ini"))
                                parameters=configParser.GetParameters(self.reportConfig[current].model[currentModel], 'parameters').split(',')
                            
                                X = df[parameters]
                                print(X.head())
                                model=str(self.reportConfig[current].model[currentModel]+'.joblib')
                                clf=load(os.path.join(os.getcwd(),"model",model))

                                y = clf.predict(X)
                                Y = pd.DataFrame(y,columns=['class'])
                                print(Y.head())
                                df_predict=pd.concat([df,Y],axis=1)
                                print(df_predict.head())

                                df_predict.to_csv(str(os.path.join(self.reportConfig[current].reportName,algo,self.reportConfig[current].model[currentModel],'dataFramePredict.csv')),index=False)
                                
                                process.append(True)

                if len(process)>1:
                    print("     " + str(os.path.split(self.reportConfig[current].simulFolder)[1]) + " done")
                    self.processing.emit("      " + str(os.path.split(self.reportConfig[current].simulFolder)[1]) + " done")

            self.processing.emit("End machine learning : " + str(self.reportConfig[0].model) + "\n")

        self.finished.emit(1)


# ----------------------------------- #
import csv
import textgrid
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
import csv
from operator import itemgetter
import requests
import xmltodict
import os
from PyQt5 import QtCore
import urllib
import Config

# ----------------------------------- #

# /!\ WARNING /!\ cette classe a besoin des fichiers de fixations, fichier txt du texte et fichier audio en wav et du textPosition

# cette classe a pour but de generer un graphe afin d'evaluer si l'utilisateur est a l'aise dans la lecture d'un texte
# nous devons donc analyser l'endroit ou ce dernier a posé ces yeux au moment ou il dit un mot
# le nombre de mot d'avance entre les yeux et la voix indiquera a quel point le protagoniste sera a laise 

class EVS(QtCore.QThread):
    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)

    # Constructor
    def __init__(self, reportConfig):
        super(EVS, self).__init__()
        self.reportConfig = reportConfig
        self.evsFolderName = ""
        self.nameFolder = ""
        self.txtFile = ""
        self.wavFile =  0
        self.nbrPages = ""
        self.beginTime = 0.0

    def run(self):
        process= None
        success=None
        if len(self.reportConfig)>0:      
            self.processing.emit("Start EVS generation")
            print("Start EVS generation")
            internetConnection = self.check_connectivity("https://www.google.com")
            for current in range(0,len(self.reportConfig)):
                process = []
                if not internetConnection and len(self.reportConfig) > 0 and self.reportConfig[0].evsChecked :  
                    self.processing.emit("No internet connetion, EVS generation impossible")
                else :    
                    for algorithm in self.reportConfig[current].algorithm:
                        if self.reportConfig[current].allowEyeTracker and self.reportConfig[current].allowAudio:
                            if not os.path.isdir(os.path.join(self.reportConfig[current].reportName, "evs-"+algorithm)):
                                os.mkdir(os.path.join(self.reportConfig[current].reportName,"evs-"+algorithm))
                            self.evsFolderName = "evs-"+algorithm
                            self.nameFolder = os.path.join(self.reportConfig[current].reportName)
                            self.txtFile = os.path.join(self.nameFolder,"text.txt")
                            self.wavFile = os.path.join(self.nameFolder ,"recordedFile.wav")  
                            self.nbrPages = self.getPageNbr()
                            success = self.generateGraphLearning(algorithm)
                    process.append(success)
                    self.processing.emit("EVS generation :" + str(success))
                if len(process)>1:
                    print("     " + str(os.path.split(self.reportConfig[current].simulFolder)[1]) + " done")
                    self.processing.emit("      " + str(os.path.split(self.reportConfig[current].simulFolder)[1]) + " done")
            self.processing.emit("End EVS generation\n")
        self.finished.emit(1)

    def check_connectivity(self,reference):
        try:
            urllib.request.urlopen(reference, timeout=1)
            return True
        except urllib.request.URLError:
            return False
    
    def setBeginTime(self, beginTime):
        self.beginTime = beginTime

    def generateGraphLearning(self, algorithm):

        # generation textgrid pour la partie voix 

        success = self.generateTextGrid()
        if success :
            # maj du temps initial
            self.setBeginTime(self.getBeginTime(algorithm))
            for i in range(self.nbrPages):
                    
                # recuperation de la position des yeux en fonction du temps
                eyePosition = self.getPositionsEyes(i,algorithm)
                # generation du fichier csv (yeux -> mot)
                self.generateCsvEyesWord(eyePosition, i)


                # recuperation des deux fichiers générés
                listVisu, listMaus = self.getData(i)

                # generation EVS data 
                listEVS = self.generateDataGraph(listVisu, listMaus,i)

                # generation du graph 
                if(len(listEVS)>0):
                    self.generateGraph(listEVS,f"graph{i}")
                else:
                    print(f"bad calibration in the page {i}")
            return True        
        return False



    def generateTextGrid(self):
        # TODO: try catch for internet connexion
        if not os.path.isfile(os.path.join(self.nameFolder,"file.txt")) :
            os.rename(self.txtFile, os.path.join(self.nameFolder,"file.txt"))
            
        if not os.path.isfile(os.path.join(self.nameFolder,"file.wav")) :
            os.rename(self.wavFile, os.path.join(self.nameFolder,"file.wav"))
            
        url  = "https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic"
        files = { 'SIGNAL' : ('file.wav', open(os.path.join(self.nameFolder,'file.wav'), 'rb')), 'TEXT':('file.txt', open(os.path.join(self.nameFolder,'file.txt'), 'rb')), 'LANGUAGE':(None,'deu-DE'), 'OUTFORMAT':(None,'TextGrid') }
        self.processing.emit("Accessing the MAUS web service...")
        rpost = requests.post( "https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic", files=files,verify=False)
        dict_data = xmltodict.parse(rpost.content)

        if dict_data['WebServiceResponseLink']['success'] == 'true' :   
            rget = requests.get(dict_data['WebServiceResponseLink']['downloadLink'])
            fichier = open(os.path.join(self.nameFolder,self.evsFolderName,"fichierreponse.TextGrid"),"w+", encoding="utf-8", errors='ignore')
            fichier.write(rget.text)
            fichier.close()
            return True
        self.processing.emit("EVS generation : WebServiceMAus Fail")    
        return False
        #else :
        #    self.processing.emit("Abording EVS generation : Fail WebService")
        #    return False    


    def getBeginTime(self, algorithm):
        with open(os.path.join(self.nameFolder, algorithm,'fixations_0.csv')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if(line_count == 0):
                    line_count +=1
                elif(line_count == 1):
                    s = int(row[3]) / 1000.0
                    secondes = float(datetime.fromtimestamp(s).strftime('%S.%f'))
                    minutes = float(datetime.fromtimestamp(s).strftime('%M'))
                    time = minutes*60.0+secondes
                    return time
    
    def getPositionsEyes(self,val,algorithm):
        
        listPositionEyes = []
        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        with open(os.path.join(self.nameFolder,algorithm,f'fixations_{val}.csv')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            previous_time =self.beginTime
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    s = int(row[3]) / 1000.0
                    secondes = float(datetime.fromtimestamp(s).strftime('%S.%f'))
                    minutes = float(datetime.fromtimestamp(s).strftime('%M'))
                    time = minutes*60.0+secondes
                    
                    final_time = time - previous_time
                    dictPosition = {
                        "x_position" : row[0],
                        "y_position" : row[1],
                        "duration"   : row[2],
                        "time" : final_time,
                    }                               

                    listPositionEyes.append(dictPosition)
                    line_count += 1
            return listPositionEyes

    def generateCsvEyesWord(self,listPosition,val):
        
        #Recuperations information textPosition.csv
        listEyesWords = []

        with open(os.path.join(self.nameFolder,'textPosition.csv')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            #initialisation dict
            for row in csv_reader:
                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    a = float(row[1])
                    b = float(row[2])
                    c = float(row[3])
                    d = float(row[4])
                    id = line_count -1 
                    line_count += 1
                    for elem in listPosition:
                        x_eye = float(elem["x_position"])
                        y_eye = float(elem["y_position"])
                        if(a < x_eye < a+c and b < y_eye < b + d and int(row[5])==val):
                            listElem = [row[0],elem["duration"],elem["time"],id]
                            listEyesWords.append(listElem)
            td = open(os.path.join(self.nameFolder,self.evsFolderName,f"visualisation_{val}.csv") , "w+")
            begin = "word,time,duration_ms,id\n"
            td.write(begin)
            for elem in sorted(listEyesWords, key=itemgetter(2)):
                ligne = f"{elem[0]},{elem[2]},{elem[1]},{elem[3]}\n"
                td.write(ligne)
            td.close()

    def getPageNbr(self):
        nbr = 0
        with open(os.path.join(self.nameFolder,"textPosition.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    nbr = int(row[5])
        return nbr+1 



    # recuperation du data 
    def getData(self,val):
        listVisualisation = []
        listMaus = []
        i = 0
        with open(os.path.join(self.nameFolder,self.evsFolderName,f"visualisation_{val}.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                listVisualisation.append(row)
        tg = textgrid.TextGrid.fromFile(os.path.join(self.nameFolder,self.evsFolderName,"fichierreponse.TextGrid"))
        for j in range (len(tg[0])):
            if(tg[0][j].mark == ""):
                id = 0
            else : 
                id = i+1
                i +=1
            subMaus = [
                tg[0][j].mark,
                tg[0][j].minTime,
                tg[0][j].maxTime,
                id
            ]
            listMaus.append(subMaus)
        return listVisualisation,listMaus

    def generateDataGraph(self,listVisu , listMaus,ligne):
        listEVS = []
        # a besoin de deux listes pour l'exploiter : visuel , audio
        # 1er cas : des lors ou le cobaye cite un mot il faut regarder ce qu'il regarde
        for elemMaus in listMaus : 
            #print(elemMaus[1])
            for i in range(len(listVisu)):
                if(i != 0 and elemMaus[3] != 0 ):
                    elemVisu = listVisu[i]
                    if(elemVisu[0] == "word"):
                        pass
                    else:
                        # nous allons tenter d'arrondir
                        timeBegin = float(elemMaus[1])
                        timeEnd = float(elemMaus[2])
                        nbrWord = int(elemVisu[3]) - int(elemMaus[3])
                        
                        if(round(float(elemVisu[1]),1) == round(float(elemMaus[1]),1)):
                            dictReleve = {
                                "wordVisu" : elemVisu[0],
                                "wordMaus" : elemMaus[0],
                                "time" : elemVisu[1],
                                "nbrWords" : nbrWord
                            }

                            listEVS.append(dictReleve)
                        # creer un interval entre le debut du regard et sa durée
                        elif(timeBegin <= float(elemVisu[1]) <= timeEnd):
                            dictReleve = {
                                "wordVisu" : elemVisu[0],
                                "wordMaus" : elemMaus[0],
                                "time" : elemMaus[1],
                                "nbrWords" : nbrWord
                            }
                            listEVS.append(dictReleve)
            td = open(os.path.join(self.nameFolder,self.evsFolderName,f"evs_data_{ligne}.csv") , "w+")
            for elem in listEVS :
                line = f'{elem}\n'
                td.write(line)
        
        return listEVS

    def generateGraph(self,listEvs , filename):
        maxTime = listEvs[len(listEvs) - 1]["time"]
        lstDuration = []
        lstWord = []
        for elem in listEvs:
            if(10> elem["nbrWords"] >=0):
                lstDuration.append(elem["time"])
                lstWord.append(elem["nbrWords"])
        x=lstDuration
        y=lstWord
        fig = plt.figure()
        fig, ax = plt.subplots()
        plt.plot(x, y, 'ro-')
        every_nth = 5
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            if n % every_nth != 0:
                label.set_visible(False)
        plt.title("graphe d'apprentissage")
        plt.xlabel("durée de lecture")
        plt.ylabel("nombre de mots d'avance (vue -> lecture)")
        plt.savefig(os.path.join(self.nameFolder,self.evsFolderName,f"{filename}.png"))



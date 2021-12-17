#Audio.py => audio section
#getListAudioInput => list all audio input
#ThreadAudioRecord => audio record in simulation
#ThreadAudioRecordTest => audio record for testing
#ThreadAudioPlay => play audio record (for test)
#AudioTestDisplay => audio test windows

import webbrowser
import pyaudio
import wave
import threading
#import python Module
import sys, os
from PyQt5 import QtCore, QtWidgets, QtGui
import time
import Config, Function
import audioop
import numpy as np

#audio format
format = pyaudio.paInt16

#list all audio input
def getListAudioInput():
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        inputAudio=[]
        for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    #print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                    #inputAudio.append([p.get_device_info_by_host_api_device_index(0, i).get('name'),i])
                    inputAudio.append(p.get_device_info_by_host_api_device_index(0, i).get('name'))
        
        Config.audioInput = []
        Config.audioInput = inputAudio
        print(Config.audioInput)

frames = []# audio save for test record and play

#audio record in simulation
class ThreadAudioRecord(threading.Thread):#(QtCore.QThread):
    
    def __init__(self,path,index):#bar
        threading.Thread.__init__(self)#super(ThreadRecord, self).__init__()
        self.rate = Config.rate
        self.chunk = Config.chunk
        self.channels=Config.channels
        self.sound_out= path + ".wav"
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.index=index
        self.stop=False 
        self.startRecording = False 

    #open audio stream
    def init(self):
        self.stream = self.p.open(format = format,
                channels = self.channels,
                rate = self.rate,
                input = True,
                input_device_index=self.index,
                frames_per_buffer = self.chunk,
                output=True)

    #enable start audio record            
    def startRecord(self):
        self.startRecording = True

    #start record audio
    def run(self):
        self.init()

        while not self.startRecording:
            pass
 
        Config.audioUNIXStart = Function.current_milli_time()
        while not self.stop:
            data = self.stream.read(self.chunk,exception_on_overflow = False)
            self.frames.append(data)

        # Close the audio recording stream
        self.stream.close()
        self.p.terminate()

        # write data to WAVE file
        wf = wave.open(self.sound_out, 'wb')

        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))

        wf.close()

        self.frames=[]
        print("stop record audio")


    #stop record audio
    def close(self):
        self.stop=True

#audio record test
class ThreadAudioRecordTest(threading.Thread):#(QtCore.QThread):
    
    def __init__(self,index,rate,chunk,channels):#bar
        threading.Thread.__init__(self)#super(ThreadAudioRecordTest, self).__init__()
        self.rate = rate
        self.chunk = chunk
        self.channels=channels
        self.p = pyaudio.PyAudio()
        self.index=index
        print("index",index)
        self.stop=False  

    #start record audio test    
    def run(self):
        global frames
        frames = []
        self.stream = self.p.open(format = format,
                channels = self.channels,
                rate = self.rate,
                input = True,
                input_device_index=self.index,
                frames_per_buffer = self.chunk,
                output=True)

        while not self.stop:
            data = self.stream.read(self.chunk,exception_on_overflow = False)
            frames.append(data)

        # Close the audio recording stream
        self.stream.close()
        self.p.terminate()

    #stop record audio test
    def close(self):
        self.stop=True
        print("stop record")

#play audio in test mode
class ThreadAudioPlay(QtCore.QThread):#(threading.Thread):
 
    finished = QtCore.pyqtSignal(int)

    def __init__(self,rate,chunk,channels):#bar
        super(ThreadAudioPlay, self).__init__()#threading.Thread.__init__(self)

        self.rate = rate
        self.chunk = chunk
        self.channels=channels
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = format,
                channels = self.channels,
                rate = self.rate,
                output=True)   
        self.end =False

    #play sound
    def run(self):    
        global frames 
        if len(frames) >0:
            i=0   
            while not self.end:

                data = frames[i]
                if i == len(frames) -1 :
                    self.end = True
                    break
                if data != b'' and i<len(frames):
                    self.stream.write(data)
                    i+=1
                else :
                    self.end = True
                    break    
                """
                # Play entire file 
                data = self.wf.readframes(Config.chunk)
                if data != b'':
                    self.stream.write(data)
                else :
                    self.end = True
                    break
                """
            # Close the audio recording stream
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        self.finished.emit(1)
                            
    #stop read
    def close(self):
        self.end = True
        print("close read") 
            
                
#audio test windows     
class AudioTestDisplay(QtWidgets.QWidget):

    def __init__(self,audioTestInput=None):
        global frames
        QtWidgets.QWidget.__init__(self)
        getListAudioInput()
        
        #reset frames tab
        frames = []
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Sound Test')
        self.width=1000
        self.height=250
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets

        #Select Input GroupBox
        self.inputGroupBox = QtWidgets.QGroupBox("Select Audio Input")
        self.inputGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.inputLayout = QtWidgets.QVBoxLayout()

        self.input = QtWidgets.QComboBox(self)
        self.input.addItems(Config.audioInput)
        if audioTestInput != None:
            try:
                self.input.setCurrentIndex(Config.audioInput.index(audioTestInput))
            except:
                self.input.setCurrentIndex(-1)
        else :
            self.input.setCurrentIndex(-1)
        self.input.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.input.currentIndexChanged[int].connect(self.on_currentIndexChangedInput)
        self.inputLayout.addWidget(self.input)
        
        self.inputGroupBox.setLayout(self.inputLayout)

        self.grid.addWidget(self.inputGroupBox,0,0)

        #audio Test Control GroupBox
        self.audioGroupBox = QtWidgets.QGroupBox(self)
        self.audioGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.audioLayout = QtWidgets.QHBoxLayout()

        self.start = QtWidgets.QPushButton('Start', self)
        self.start.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.start.clicked.connect(self.start_click)
        if audioTestInput != None:
            self.start.setEnabled(True)
        else :
            self.start.setEnabled(False)

        self.audioLayout.addWidget(self.start)


        self.stop = QtWidgets.QPushButton('Stop', self)
        self.stop.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.stop.clicked.connect(self.stop_click)
        self.stop.setEnabled(False)
        self.audioLayout.addWidget(self.stop)
        
        self.read = QtWidgets.QPushButton('Read', self)
        self.read.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.read.clicked.connect(self.read_click)
        self.read.setEnabled(False)
        self.audioLayout.addWidget(self.read)

        self.audioGroupBox.setLayout(self.audioLayout)
        self.grid.addWidget(self.audioGroupBox,1,0)

        self.audioLayoutNavigationGroupBox = QtWidgets.QGroupBox(self)
        self.audioLayoutNavigationGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

        self.audioLayoutNavigation = QtWidgets.QHBoxLayout()


        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.audioLayoutNavigation.addWidget(self.back)
        self.back.clicked.connect(self.close)

        if Config.documentationHTML :
            #help section
            self.help = QtWidgets.QPushButton(' ',self)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
            self.help.setIcon(icon)       
            self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"+"}")
            self.audioLayoutNavigation.addWidget(self.help)
            self.help.clicked.connect(self.help_click)

        self.audioLayoutNavigationGroupBox.setLayout(self.audioLayoutNavigation)
        self.grid.addWidget(self.audioLayoutNavigationGroupBox,2,0)
        

        self.recordingDisplay = QtWidgets.QLabel("Recording",self)
        self.recordingDisplay.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str("red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.recordingDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.recordingDisplay, 1,1)
        self.recordingDisplay.hide()

        self.readDisplay = QtWidgets.QLabel("Read",self)
        self.readDisplay.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str("red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.readDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.readDisplay, 1,1)
        self.readDisplay.hide()

        #tempAudio Paramameters Test GroupBox
        self.tempParamGroupBox = QtWidgets.QGroupBox("Test Audio Parameters")
        self.tempParamGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.tempParamLayout = QtWidgets.QFormLayout()

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
        self.tempParamLayout.addRow(self.rate,self.rateEdit)


        self.channels = QtWidgets.QLabel("Channels",self)
        self.channels.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        self.channelsEdit=QtWidgets.QLineEdit(str(Config.channels),self)
        self.channelsEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

        self.channelsEdit.textChanged.connect(lambda:self.IntEdit(self.channelsEdit))
        self.tempParamLayout.addRow(self.channels,self.channelsEdit)

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
        self.tempParamLayout.addRow(self.chunk,self.chunkEdit)

        self.tempParamGroupBox.setLayout(self.tempParamLayout)

        self.grid.addWidget(self.tempParamGroupBox,0,1)
        self.grid.setColumnStretch(0,self.width/2)
        self.grid.setColumnStretch(1,self.width/2)

    #check if temp parameters is integer
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

    #action when choose audio input
    def on_currentIndexChangedInput(self, index):
        if self.input.currentText() != "":
            self.start.setEnabled(True)
            self.stop.setEnabled(False)
            self.read.setEnabled(False)


    #start record to test        
    def start_click(self):

        #get audio index
        index=Config.audioInput.index(self.input.currentText())
        
        if (self.rateEdit.text() !="" and Function.is_integer(self.rateEdit.text())) and (self.chunkEdit.text() != "" and Function.is_integer(self.chunkEdit.text())) and (self.channelsEdit.text() != "" and Function.is_integer(self.channelsEdit.text())) :
            self.audioTestRecordThread = ThreadAudioRecordTest(index,int(self.rateEdit.text()),int(self.chunkEdit.text()),int(self.channelsEdit.text()))

            self.audioTestRecordThread.start()
            self.recordingDisplay.show()
            self.start.setEnabled(False)
            self.stop.setEnabled(True)
            self.read.setEnabled(False)
                
    #stop record or play to test
    def stop_click(self):

        #stop record audio test
        try:
            self.audioTestRecordThread.close()
            self.start.setEnabled(True)
            self.stop.setEnabled(False)
            self.read.setEnabled(True)
            self.recordingDisplay.hide()

        except:
            pass
        
        #stop read audio test
        try:
            self.audioTestPlayThread.close()
            self.start.setEnabled(True)
            self.stop.setEnabled(False)
            self.read.setEnabled(True)
            self.readDisplay.hide()

        except:
            pass
        
    #read audio for test
    def read_click(self):
        self.readDisplay.show()
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        self.read.setEnabled(False)
        self.audioTestPlayThread = ThreadAudioPlay(int(self.rateEdit.text()),int(self.chunkEdit.text()),int(self.channelsEdit.text()))
        self.audioTestPlayThread.start()
        self.audioTestPlayThread.finished.connect(self.closeRead)

    #close read when finish
    def closeRead(self):
        self.readDisplay.hide()
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        self.read.setEnabled(True)

    #help
    def help_click(self):
        if Config.documentationHTML:
            webbrowser.open_new_tab('file://'+str(Config.documentationParametersAudioTest))

    #close windows
    def closeEvent(self, event):
        global frames
        #close record test
        try:
            self.audioTestRecordThread.close()
        except:
            pass

        #close read test
        try:
            self.audioTestPlayThread.close()
        except:
            pass
        
        #reset frames tab :
        frames = []
            
            
    

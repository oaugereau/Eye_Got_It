
#videoOpenCV class => video processing with openCV
#VideoOpenFace class => video processing with OpenFace
import os, sys, threading, subprocess, csv, time, shutil, statistics, datetime, cv2,webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
import Config, Function,ConfigFileManagement
from multiprocessing import Process, Queue
from threading import Thread

#get list of input video
def getListVideoInput():
    try:
        from pygrabber.dshow_graph import FilterGraph

        graph = FilterGraph()
        Config.videoInput = graph.get_input_devices()
        print(graph.get_input_devices())
        
    except:
        Config.videoInput = ["Webcam","USB"]

#capture video for simulation        
class ThreadVideoRecord(threading.Thread):#class ThreadVideoRecord(QtCore.QThread):
    def __init__(self,index,width,height,saveReport):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):
        threading.Thread.__init__(self)#super(ThreadVideoRecord, self).__init__()
        self.index = index
        self.saveReport = str(saveReport + ".avi")
        self.stop = False
        self.startRecording = False

    def init(self):
        print("start init")
        start0 = Function.current_milli_time()
        self.capture = cv2.VideoCapture(self.index)#,cv2.CAP_DSHOW)
        self.ok, _ = self.capture.read()
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        #self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')#MJPG XVID MPEG
        self.currentFrame = 0
        print("Video info :")
        print("width ",self.capture.get(3))
        print("height ",self.capture.get(4))
        print("video FPS ",self.capture.get(cv2.CAP_PROP_FPS))
        self.fpsSource = self.capture.get(cv2.CAP_PROP_FPS)
        #self.out = cv2.VideoWriter(self.saveReport, self.fourcc, 24, (640, 480))
        self.out = cv2.VideoWriter(self.saveReport, self.fourcc, self.fpsSource, (int(self.capture.get(3)), int(self.capture.get(4))))
        #Config.videoUNIXStart = Function.current_milli_time()
        #print(Function.current_milli_time() - start)
        """
        start2 = Function.current_milli_time()
        frame=[]
        start=Function.current_milli_time()
        start2=Function.current_milli_time()
        while (Function.current_milli_time() - start2 < 2100): #self.capture.isOpened() and 
            
            ret, img = self.capture.read()
            
            if ret:
                
                self.out.write(img)
                
            else :
                break
            self.currentFrame += 1
            if Function.current_milli_time() - start > 1000:
                start=Function.current_milli_time()
                print("frame in 1 sec",self.currentFrame )
                frame.append(self.currentFrame)
                self.currentFrame=0
        self.capture.release()
        self.out.release()
        #print("Real fps : ",frame[-1])
        if frame[-1] > self.fpsSource-5 and frame[-1] < self.fpsSource +5:
            self.fps = self.fpsSource
        else:
            self.fps = frame[-1]
        
        print("Real FPS ",self.fps)
        print("test done ",Function.current_milli_time() - start2)
        start3 = Function.current_milli_time()
        self.capture = cv2.VideoCapture(self.index)
        self.out = cv2.VideoWriter(self.saveReport, self.fourcc, self.fps, (int(self.capture.get(3)), int(self.capture.get(4))))
        print("end init ",Function.current_milli_time() - start3)
        """
        print("end all init ",Function.current_milli_time() - start0)

    def startRecord(self):
        
        self.startRecording = True

    #start    
    def run(self):
        self.init()
        while not self.startRecording :
            pass
        if self.ok:
            print("start video record")
            frame=[]
            start=Function.current_milli_time()
            Config.videoUNIXStart = Function.current_milli_time()
            while (not self.stop): #self.capture.isOpened() and 
                
                ret, img = self.capture.read()
                
                if ret:
                    
                    self.out.write(img)
                    
                else :
                    break
                """
                self.currentFrame += 1
                if Function.current_milli_time() - start > 1000:
                    start=Function.current_milli_time()
                    #print("frame in 1 sec",self.currentFrame )
                    frame.append(self.currentFrame)
                    self.currentFrame=0  
                """           

                #if cv2.waitKey(1) & self.stop: #cv2.waitKey(30) & 0xFF == ord('q') or 
                #    break


        self.capture.release()
        
        self.out.release()
        cv2.destroyAllWindows()
        print("stop record video")


    #stop
    def stopRecord(self):
        self.stop=True


#windows to test eye tracker
class videoTestWindows(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        getListVideoInput()

        #windows config
        self.setWindowTitle("Video Test")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=500
        self.height=200
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.video = QtWidgets.QLabel("Choose Video Input",self)
        self.video.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.video, 0,0)

        self.videoEdit = QtWidgets.QComboBox(self)
        self.videoEdit.addItems(Config.videoInput)
        self.videoEdit.setCurrentIndex(-1)
        self.videoEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.videoEdit, 0,1)
        self.videoEdit.currentIndexChanged[int].connect(self.on_currentIndexChangedVideoEdit)
        self.videoEdit.setEnabled(True)

        self.test = QtWidgets.QPushButton('Test', self)
        self.test.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.test, 1,0,1,2)
        self.test.clicked.connect(self.test_click)
        self.test.setEnabled(False)


    def on_currentIndexChangedVideoEdit(self,index):
        if self.videoEdit.currentText() != "":
            self.test.setEnabled(True)

        else:
            self.test.setEnabled(False)

    #start the test
    def test_click(self):
        """
        try:
            cv2.destroyAllWindows()
            #self.videoTest.stop()
        except:
            pass    
        
        """
        self.videoTest = ThreadVideoTest(Config.videoInput.index(self.videoEdit.currentText()))
        self.videoTest.start()
        #self.videoTest.start()

#test the webcam
class ThreadVideoTest(QtCore.QThread):#class Thread(threading.Thread):
    def __init__(self,index):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):
        super(ThreadVideoTest, self).__init__()#threading.Thread.__init__(self)
        self.index = index
        self.winname =str('video Test ' + str(self.index))
        try:
            cv2.destroyWindow(self.winname)
        except :
            pass
        print(index)
        """
        if self.index ==1 :
            try :
                self.capture = cv2.VideoCapture(self.index)#,cv2.CAP_DSHOW)
            except:
                print("error")
                self.index = 0
                self.capture = cv2.VideoCapture(0)
        else :
            self.capture = cv2.VideoCapture(self.index)
        """
        self.capture = cv2.VideoCapture(self.index)
        self.ok, _ = self.capture.read()
        print(self.ok)    
        self.winname =str('video Test ' + str(self.index))
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        self.width = int(self.capture.get(3))
        self.height = int(self.capture.get(4))
        print("Video test info :")
        print("width ",self.capture.get(3))
        print("height ",self.capture.get(4))
        print("video FPS ",self.capture.get(cv2.CAP_PROP_FPS))

        self.face_cascade = cv2.CascadeClassifier(os.path.join("opencv",'haarcascade_frontalface_alt.xml')) # or lbpcascade_frontalface.xml for faster process
        self.eye_cascade = cv2.CascadeClassifier(os.path.join("opencv",'haarcascade_eye_tree_eyeglasses.xml'))

    #start test
    def run(self):
        if self.ok:
            cv2.namedWindow(self.winname)
            while cv2.getWindowProperty(self.winname, cv2.WND_PROP_VISIBLE) >= 1: #(self.capture.isOpened()) or
                #print(cv2.getWindowProperty('video img', 1))
                ret, img = self.capture.read()
                
                if ret:
                    # Convert to grayscale
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # Detect the faces
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4,  minSize = (100,100))
                    
                    # Draw the rectangle around each face
                    for (x, y, w, h) in faces:
                        
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = img[y:y+h, x:x+w]
                        eyes = self.eye_cascade.detectMultiScale(roi_gray,1.1,4,maxSize = (50,50))

                        for (ex,ey,ew,eh) in eyes:
                            #print("ew " + str(ew))
                            #print("eh " + str(eh))
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                            # Create a named window
                    #cv2.moveWindow(self.winname, int(Config.SCREEN_WIDTH/2 - self.width/2),int(Config.SCREEN_HEIGHT/2 - self.height/2))  # Move it to (40,30)
                    cv2.imshow(self.winname, img)
                    
                    k = cv2.waitKey(1) & 0xFF
                    #print(k)
                    if k == 27 or k == 13 :#cv2.waitKey(1) == 27 :#& 0xFF == ord('q') : => 27 : ECHAP, 13 => ENTER
                        break
                else :
                    break
        
        self.capture.release()
        cv2.destroyWindow(self.winname)
        print("end of video test Thread")

    def stop(self):
        self.capture.release()
        cv2.destroyWindow(self.winname)
        #cv2.destroyAllWindows()

#video treatement if not openFace
class ThreadVideoProcessingOpencv (QtCore.QThread):
    processing = QtCore.pyqtSignal(str)
    remainTime = QtCore.pyqtSignal(str)
    timeStart = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)


    def __init__(self,reportConfig):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):
        
        self.reportConfigMain = reportConfig
        super(ThreadProcessing, self).__init__()#threading.Thread.__init__(self)
        # Load the cascade
        self.face_cascade = cv2.CascadeClassifier(os.path.join("opencv",'lbpcascade_frontalface.xml'))
        self.eye_cascade = cv2.CascadeClassifier(os.path.join("opencv",'haarcascade_eye_tree_eyeglasses.xml'))
        
        
        
        
    def run(self):
        if os.path.isfile(os.path.join("opencv",'lbpcascade_frontalface.xml')) and os.path.isfile(os.path.join("opencv",'haarcascade_eye_tree_eyeglasses.xml')):
            self.processing.emit(str("Start video process" ))
            i=0
            for reportConfig in self.reportConfigMain:
                if reportConfig.allowVideo and reportConfig.videoChecked and os.path.isfile(os.path.join(Config.ReportFolder,reportConfig.reportName,str(reportConfig.videoOut + ".avi"))):
                    self.cap = cv2.VideoCapture(os.path.join(Config.ReportFolder,reportConfig.reportName,str(reportConfig.videoOut + ".avi")))
                    self.len_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.image = 1
                    self.duration = float(self.len_frames / self.cap.get(cv2.CAP_PROP_FPS))
                    self.frame_width = int(self.cap.get(3))
                    self.frame_height = int(self.cap.get(4))
                    self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                    self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                    numberFace = 0
                    numberEyes = 0
                    winname = "video"
                    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
                    out = cv2.VideoWriter(os.path.join(Config.ReportFolder,reportConfig.reportName,str(reportConfig.videoOut + "_processed.avi")),self.fourcc, self.fps , (self.frame_width,self.frame_height))
                    previousDone = 0
                    currentFrame = 1
                    Frame=0
                    done = 0
                    start = time.time()
                    previousTimeRemaining = int(time.time())
                    timeRefresh = int(time.time())

                    timeProcessing = []
                    facesList = []
                    eyesList = []
                    self.processing.emit(str("      Video process " + str(i+1) + " / " + str(len(self.reportConfigMain))))
                    while (self.cap.isOpened()):
                        # Read the frame
                        _, img = self.cap.read()
                        if img is None:
                            break
                        
                        if currentFrame == self.len_frames:
                                break

                        if currentFrame == Frame + self.image:
                            Frame = currentFrame
                            videoTime = datetime.timedelta(seconds=(currentFrame*self.duration/self.len_frames))
                            
                            # Convert to grayscale
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            # Detect the faces
                            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4,  minSize = (100,100))
                            

                            # Draw the rectangle around each face
                            for (x, y, w, h) in faces:
                                facesList.append([currentFrame,x,y,w,h,videoTime])
                                numberFace += 1
                                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                                
                                roi_gray = gray[y:y+h, x:x+w]
                                roi_color = img[y:y+h, x:x+w]
                                eyes = self.eye_cascade.detectMultiScale(roi_gray,1.1,4,maxSize = (50,50))

                                for (ex,ey,ew,eh) in eyes:
                                    eyesList.append([currentFrame,ex,ey,ew,eh,videoTime])
                                    numberEyes+=1
                                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                                
                            out.write(img)
                            k = cv2.waitKey(1) & 0xff
                            if k==27:
                                break

                            
                            

                            currentTime = (time.time())
                            timeProcessing.append(currentTime - previousTimeRemaining)

                            self.timeStart.emit("Time " + str(datetime.timedelta(seconds=int(time.time() - start))))
                            
                            if currentTime - timeRefresh >= 0.5 :
                                remain = int((statistics.mean(timeProcessing))*(self.len_frames - currentFrame))#int((currentTime - previousTimeRemaining)*(self.len_frames - currentFrame))
                                self.remainTime.emit("Time remaining (estimated) " + str(datetime.timedelta(seconds=remain)))
                                #print("remain : " + str(remain))
                                
                                timeRefresh = currentTime
                            previousTimeRemaining = currentTime
                            currentFrame+=1
                        else :
                            currentFrame+=1

                
                # Release the VideoCapture object
                reportConfig.timeDuring = datetime.timedelta(seconds=(time.time() - start))
                reportConfig.numberFace = numberFace
                reportConfig.numberEyes = numberEyes

                print("Close")
                self.cap.release()

                out.release()
                with open(str(os.path.join(reportConfig.reportName,"face.csv")), 'w', newline='') as csvfile:
                        fileUser = csv.writer(csvfile, delimiter=',',)
                        fileUser.writerow(["number","x","y","width","height","time"])
                        
                        for i in range(0,len(facesList)):
                            fileUser.writerow([facesList[i][0],facesList[i][1],facesList[i][2],facesList[i][3],facesList[i][4],facesList[i][5]])
                        
                        csvfile.close()

                with open(str(os.path.join(reportConfig.reportName,"eyes.csv")), 'w', newline='') as csvfile:
                        fileUser = csv.writer(csvfile, delimiter=',',)
                        fileUser.writerow(["number","x","y","width","height","time"])
                        for i in range(0,len(eyesList)):
                            fileUser.writerow([eyesList[i][0],eyesList[i][1],eyesList[i][2],eyesList[i][3],eyesList[i][4],eyesList[i][5]])
                        csvfile.close()
                
                i+=1
            self.processing.emit(str("End video process\n" ))
        self.finished.emit(1)

"""
#video processing with openCV
class videoOpenCV(QtWidgets.QWidget):

    def __init__(self,reportConfig):
        super(videoOpenCV,self).__init__()
        self.reportConfig = reportConfig

        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Video Processing')
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.theme = QtWidgets.QLabel("Video processing please wait",self)
        self.theme.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.theme, 0,0)

        #widgets
        self.progressBar = QtWidgets.QProgressBar(self)
        self.grid.addWidget(self.progressBar, 1,0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        self.timeStart = QtWidgets.QLabel(self)
        self.timeStart.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.timeStart, 2,0)

        self.remain = QtWidgets.QLabel(self)
        self.remain.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.remain, 3,0)
        
        self.video = ThreadVideoProcessingOpencv(self.reportConfig)
        self.video.processing.connect(self.progressBar.setValue)
        self.video.finished.connect(self.videoReport)
        self.video.remainTime.connect(self.remain.setText)
        self.video.timeStart.connect(self.timeStart.setText)
        self.video.start()

    #end report
    def videoReport(self):
        self.close()
        #openFolderWindows(self.reportConfig)

"""

#OpenFace
class ThreadVideoProcessingOpenFace(QtCore.QThread): #(threading.Thread):

    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self,reportConfig):#def __init__(self,windowsX, windowsY, x0, y0, appX, appY, saveReport):
        super(ThreadVideoProcessingOpenFace, self).__init__()#threading.Thread.__init__(self)
        self.reportConfigMain = reportConfig
        self.reportConfig = self.reportConfigMain[0]
        self._stopevent = threading.Event( )
        self.current = 0
        

    #run
    def run(self):
        i=0
        self.processing.emit(str("Start video process" ))
        for reportConfig in self.reportConfigMain:
            if self.reportConfig.allowVideo and self.reportConfig.videoChecked and os.path.isfile(os.path.join(Config.ReportFolder,reportConfig.reportName,str(reportConfig.videoOut) + ".avi")):
                source = os.path.join(Config.ReportFolder,reportConfig.reportName,str(reportConfig.videoOut) + ".avi")
                source = str('"' + source + '"')
                destination = os.path.join(Config.ReportFolder,reportConfig.reportName,"video_processed")
                destination = str('"' + destination + '"')
                previous = os.getcwd()
                os.chdir("openFace")
                #cmd = str(os.path.join(os.getcwd(),"eye_got_it",str("eye_got_it.exe " + str(self.windowsX) + " "  + str(self.windowsY) + " " + str(self.x0) + " " + str(self.y0 )+ " " + str(self.appX) + " " + str(self.appY) + " "+ str(self.saveReport))))
                cmd = str("FeatureExtraction.exe -f " + str(source) + " -out_dir " + str(destination))
                
                thread = subprocess.Popen(cmd,shell=False,stdout=subprocess.DEVNULL)#, stdout=subprocess.PIPE,stderr=subprocess.STDOUT  )
                os.chdir(previous)
                self.processing.emit(str("      Video process " + str(i+1) + " / " + str(len(self.reportConfigMain))))
                while thread.poll() is None:
                    
                    pass
                i+=1
        self.processing.emit(str("End video process\n" ))
        self.finished.emit(1)
        

class ActionUnits(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        #windows config        
        self.setWindowTitle('Action Units')
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=800
        self.height=600
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,(Config.SCREEN_HEIGHT/2-self.height/2)/2,self.width,self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.add = QtWidgets.QPushButton('Add', self)
        self.add.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.add, 0,0)
        self.add.clicked.connect(self.add_click)

        self.delete = QtWidgets.QPushButton('Delete last', self)
        self.delete.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.delete, 0,1)
        self.delete.clicked.connect(self.delete_last_click)

        self.actionUnitsTab=[]
        #self.deleteList=[]

        self.numberActionUnits=0

    
        #self.createGroupBox()


        #self.actionUnitsGroupBox.setLayout(self.actionUnitsLayout)

        #self.grid.addWidget(self.actionUnitsGroupBox,1,0,1,2)

        self.save = QtWidgets.QPushButton('Save', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.save, 2,0)
        self.save.clicked.connect(self.save_click)

        self.default = QtWidgets.QPushButton('Add Default Action Units', self)
        self.default.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.default, 2,1)
        self.default.clicked.connect(lambda:self.importConfig(True))

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 3,0)
        self.back.clicked.connect(self.close)

        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 3,1)
        self.help.clicked.connect(self.helpHtml)
        self.help.setEnabled(True) 

        self.importConfig()

    def importConfig(self,defaultImport=False):
        configParser=None
        if not defaultImport:
            if os.path.isfile(os.path.join(Config.EyeGotItFolder,"actionUnits.ini")):
                try:
                    configParser= ConfigFileManagement.ConfigFileRead(os.path.join(Config.EyeGotItFolder,"actionUnits.ini"))
                except:
                    configParser=None
        else :
            if os.path.isfile(os.path.join("actionUnits.ini")):
                try:
                    configParser= ConfigFileManagement.ConfigFileRead(os.path.join("actionUnits.ini"))
                except:
                    configParser=None
        self.createGroupBox()

        if configParser != None:
            for section in configParser.GetSection():
                temp = []
                try:
                    temp.append(section)
                    temp.append(str(configParser.GetParameters(str(section), 'action_units')))
                    #temp.append(str(configParser.GetParameters(str(section), 'intensity')))
                    self.add_click(section,configParser.GetParameters(str(section), 'action_units'))#,configParser.GetParameters(str(section), 'intensity'))
                except:
                    pass

            for au in self.actionUnitsTab:
                self.defaultEdit(au[1])
                self.defaultType(au[3])
        

    @QtCore.pyqtSlot()
    def add_click(self,titleActionUnitGroup="",actionUnits=""):#,intensity=""):
        
        #print("titleActionUnitGroup : " + str(titleActionUnitGroup))
        #print("actionUnits : " + str(actionUnits))
        #print("intensity : " + str(intensity))
        title = QtWidgets.QLabel("Title :",self)
        title.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        titleEdit=QtWidgets.QLineEdit(str(titleActionUnitGroup),self) 
        titleEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont if titleActionUnitGroup !="" else "red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        #videoEdit.textChanged.connect(lambda:self.defaultEdit(self.videoEdit))
        #self.actionUnitsLayout.addRow(title, titleEdit)
        titleEdit.setText(str(titleActionUnitGroup))
        titleEdit.textChanged.connect(lambda:self.defaultEdit(titleEdit))

        actionUnitsNumber = QtWidgets.QLabel("Action Units Number :",self)
        actionUnitsNumber.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        actionUnitsNumberEdit=QtWidgets.QLineEdit(str(actionUnits),self) 
        actionUnitsNumberEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont if actionUnits !="" else "red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        actionUnitsNumberEdit.textChanged.connect(lambda:self.defaultType(actionUnitsNumberEdit))
        #videoEdit.textChanged.connect(lambda:self.defaultEdit(self.videoEdit))
        #self.actionUnitsLayout.addRow(actionUnitsNumber, actionUnitsNumberEdit)
        """
        actionUnitsIntensity  = QtWidgets.QLabel("Action Units intensity :",self)
        actionUnitsIntensity.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        
        actionUnitsIntensityEdit=QtWidgets.QLineEdit(str(intensity),self) 
        actionUnitsIntensityEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        """
        #videoEdit.textChanged.connect(lambda:self.defaultEdit(self.videoEdit))
        #self.actionUnitsLayout.addRow(actionUnitsIntensity, actionUnitsIntensityEdit)
        delete = QtWidgets.QPushButton('Delete', self)
        delete.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        
        

        #delete.clicked.connect(lambda:self.delete_click(self.numberActionUnits))
        temp = [title,titleEdit,actionUnitsNumber,actionUnitsNumberEdit,delete]#,actionUnitsIntensity,actionUnitsIntensityEdit,delete]
        #self.deleteList.append(delete)
        #self.deleteList[-1].clicked.connect(lambda:self.delete_click(self.numberActionUnits))
        self.actionUnitsTab.append(temp)
        self.numberActionUnits +=1
        
        #print(self.numberActionUnits)
        self.updateActionUnits()
        
        if len(self.actionUnitsTab)>=1:
            self.delete.setEnabled(True)

    def delete_click(self, actionUnit):
        #if actionUnit in self.actionUnitsTab:
        #    print("remove index : " + str(self.actionUnitsTab.index(actionUnit)))
        
        self.actionUnitsTab.pop(actionUnit)
        self.numberActionUnits -=1

        self.updateActionUnits()

    def delete_last_click(self):
        #if actionUnit in self.actionUnitsTab:
        #    print("remove index : " + str(self.actionUnitsTab.index(actionUnit)))
        if len(self.actionUnitsTab)>=1:
            self.actionUnitsTab.pop()
            self.numberActionUnits -=1

            self.updateActionUnits()
            if len(self.actionUnitsTab)==0:
                self.delete.setEnabled(False)
        
    def updateActionUnits(self):
        Config.ActionUnitsByColumn

        if len(self.actionUnitsTab) >Config.ActionUnitsByColumn:
            layout = QtWidgets.QHBoxLayout()

            layoutTab = [QtWidgets.QVBoxLayout(),QtWidgets.QVBoxLayout()]
            for i in range(0,Config.ActionUnitsByColumn):
                tempGroupBox = QtWidgets.QGroupBox("Action Units " + str(i+1))
                tempGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";")
                tempLayout = QtWidgets.QFormLayout()
                tempLayout.addRow(self.actionUnitsTab[i][0], self.actionUnitsTab[i][1])
                tempLayout.addRow(self.actionUnitsTab[i][2], self.actionUnitsTab[i][3])
                #tempLayout.addRow(self.actionUnitsTab[i][4], self.actionUnitsTab[i][5])
                tempLayout.addRow(None, self.actionUnitsTab[i][4])
                tempGroupBox.setLayout(tempLayout)
                layoutTab[0].addWidget(tempGroupBox)
                
            current = 1   

            for i in range(Config.ActionUnitsByColumn,len(self.actionUnitsTab)):
                tempGroupBox = QtWidgets.QGroupBox("Action Units " + str(i+1))
                tempGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";")
                tempLayout = QtWidgets.QFormLayout()
                tempLayout.addRow(self.actionUnitsTab[i][0], self.actionUnitsTab[i][1])
                tempLayout.addRow(self.actionUnitsTab[i][2], self.actionUnitsTab[i][3])
                #tempLayout.addRow(self.actionUnitsTab[i][4], self.actionUnitsTab[i][5])
                tempLayout.addRow(None, self.actionUnitsTab[i][4])
                tempGroupBox.setLayout(tempLayout)
                

                if i % Config.ActionUnitsByColumn == 0:
                    #print("change " + str(i))
                    current+=1
                    layoutTab.insert(current,QtWidgets.QVBoxLayout())

                layoutTab[current].addWidget(tempGroupBox)
        
            for elem in layoutTab:
                #elem.setAlignment(QtCore.Qt.AlignTop)
                layout.addLayout(elem)
            
            self.refreshGroupBox(layout)

        else :
            layout = QtWidgets.QFormLayout()
            for i in range(0,len(self.actionUnitsTab)):
                tempGroupBox = QtWidgets.QGroupBox("Action Units " + str(i+1))
                tempGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";")
                tempLayout = QtWidgets.QFormLayout()
                tempLayout.addRow(self.actionUnitsTab[i][0], self.actionUnitsTab[i][1])
                tempLayout.addRow(self.actionUnitsTab[i][2], self.actionUnitsTab[i][3])
                #tempLayout.addRow(self.actionUnitsTab[i][4], self.actionUnitsTab[i][5])
               
                tempLayout.addRow(None, self.actionUnitsTab[i][4])
                
                tempGroupBox.setLayout(tempLayout)
                layout.addWidget(tempGroupBox)
                
            self.refreshGroupBox(layout)
        
        for i in range(0,len(self.actionUnitsTab)):
            try :
                self.actionUnitsTab[i][4].clicked.disconnect()
            except :
                pass

            self.actionUnitsTab[i][4].clicked.connect(lambda ch, i=i: self.delete_click(i))
        
    def refreshGroupBox(self,layout):

        self.actionUnitsGroupBox.close()
        self.createGroupBox()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.actionUnitsGroupBox.setLayout(layout)#(self.answersLayout[self.currentQuestion])
        size = layout.sizeHint()
        self.actionUnitsGroupBox.resize(size)
        self.grid.addWidget(self.actionUnitsGroupBox,1,0,1,2)

    def createGroupBox(self):
        
        self.actionUnitsGroupBox = QtWidgets.QGroupBox("")
        self.actionUnitsGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.actionUnitsGroupBox,1,0,1,2)

    def save_click(self):
        
        saveOk = True
        for actionUnits in self.actionUnitsTab:
            if actionUnits[1].text() == "" or  actionUnits[3].text() == "" or ((actionUnits[3].text() == '') or (len(actionUnits[3].text().split('.')) > 1 or len(actionUnits[3].text().split('/')) > 1 
            or len(actionUnits[3].text().split('-')) > 1 or len(actionUnits[3].text().split("\\")) > 1)) or len([s for s in actionUnits[3].text().split(',') if s.isdigit()]) != len(actionUnits[3].text().split(',')):
                saveOk = False
        if saveOk:
            try:

                configCreate= ConfigFileManagement.ConfigFileWrite()

                for actionUnits in self.actionUnitsTab:
                    configCreate.SetParameters(str(actionUnits[1].text()),"action_units",str(actionUnits[3].text()))
                    #configCreate.SetParameters(str(actionUnits[1].text()),"intensity",str(actionUnits[5].text()))
                if os.path.isfile(os.path.join(Config.EyeGotItFolder,"actionUnits.ini")):
                    os.remove(os.path.join(Config.EyeGotItFolder,"actionUnits.ini"))

                configCreate.CreateFile(os.path.join(Config.EyeGotItFolder,"actionUnits.ini"))

                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Action Units config saved")
                message.setWindowTitle("Action Units")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message=message.exec_()

            except :
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Please close action unit file in :\n" +str(os.path.join(Config.EyeGotItFolder,"actionUnits.ini")))
                message.setWindowTitle("Action Units")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message=message.exec_()

    def defaultType(self,defaultType):

        if (defaultType.text() != '') and (len(defaultType.text().split('.')) > 1 or len(defaultType.text().split('/')) > 1 or len(defaultType.text().split('-')) > 1 or len(defaultType.text().split("\\")) > 1):
            defaultType.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        elif defaultType.text() == '':
            defaultType.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        elif len([s for s in defaultType.text().split(',') if s.isdigit()]) != len(defaultType.text().split(',')) :
            defaultType.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        

        else :
            defaultType.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        if len([s for s in defaultType.text().split(',') if s.isdigit()]) == len(defaultType.text().split(',')) :
            for au in defaultType.text().split(','):
                au = int(au)
                if au not in Config.openFaceActionUnit:
                    defaultType.setStyleSheet("color: " + str(Config.colorText) +";"
                                    "background-color: " + str("red") +";"
                                    "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                    "selection-color: "+ str("") +";")
                                  
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


    def helpHtml(self):
        webbrowser.open_new_tab('file://'+str(Config.documentationActionUnits))

class CheckActionUnits(QtCore.QThread): #(threading.Thread):

    processing = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self,reportConfigMain):
        super(CheckActionUnits, self).__init__()
        self.reportConfigMain = reportConfigMain

        

    #run
    def run(self):
        current = 0
        if os.path.isfile(os.path.join(Config.EyeGotItFolder,"actionUnits.ini")):
            self.processing.emit(str("Start Action Units Detection" ))
            for reportConfig in self.reportConfigMain:
                openFaceCSV = os.path.join(Config.ReportFolder,reportConfig.reportName,"video_processed","video.csv")
                pathVideo = os.path.split(openFaceCSV)[0]
                if os.path.isdir(os.path.join(pathVideo,"action_units")):
                    shutil.rmtree(os.path.join(reportConfig.reportName,"video_processed","action_units"))
                if os.path.isfile(openFaceCSV):
                    self.processing.emit(str("      Video Action Unit process " + str(current+1) + " / " + str(len(self.reportConfigMain))))
                    with open(openFaceCSV, 'r', newline='') as csvfile:
                        fileUser = csv.reader(csvfile, delimiter=',')
                        csvOpenFace = [line for line in fileUser]
                        csvfile.close()
                        header = csvOpenFace[0]
                        csvOpenFace.pop(0)
                    
                    configParser=None
                    if os.path.isfile(os.path.join(Config.EyeGotItFolder,"actionUnits.ini")):
                        try:
                            configParser= ConfigFileManagement.ConfigFileRead(os.path.join(Config.EyeGotItFolder,"actionUnits.ini"))
                        except:
                            configParser=None
                    
                    actionUnitsImport = []
                    actionUnitsCSV =[]
                    if configParser != None:
                        for section in configParser.GetSection():
                            temp = []
                            try:
                                temp.append(section)
                                temp.append((configParser.GetParameters(str(section), 'action_units')).split(','))
                                #temp.append((configParser.GetParameters(str(section), 'intensity')).split(','))
                                temp.append([])
                                #temp.append([])
                                #temp.append([])
                                #temp.append([])
                                
                                for i in range(0, len(temp[1])):
                                    temp[1][i] = int(temp[1][i])
                                for i in range(0, len(temp[2])):
                                    temp[2][i] = float(temp[2][i])
                                actionUnitsImport.append(temp)
                                
                            except:
                                pass
                
                    
                    for currentLine in range(0,len(csvOpenFace)):
                        
                        
                        temp=[]
                        for currentAU in range(0,len(actionUnitsImport)):
                            temp.append([actionUnitsImport[currentAU][0],actionUnitsImport[currentAU][1]])#,actionUnitsImport[currentAU][2]])
                            actionUnitPresence=[]
                            for action in range(0,len(actionUnitsImport[currentAU][1])):
                                    
                                
                                if actionUnitsImport[currentAU][1][action] <10:
                                    actionUnit= str("AU0"+str(actionUnitsImport[currentAU][1][action])+"_c")
                                    indexActionUnit = 0
                                    for i in range(0,len(header)):
                                        if actionUnit in header[i]:
                                            indexActionUnit = header[i] 
                                            actionUnitPresence.append(float(csvOpenFace[currentLine][header.index(indexActionUnit)]))
                                else :
                                    actionUnit= str("AU"+str(actionUnitsImport[currentAU][1][action])+"_c")
                                    indexActionUnit = 0
                                    for i in range(0,len(header)):
                                        if actionUnit in header[i]:
                                            indexActionUnit = header[i] 
                                            actionUnitPresence.append(float(csvOpenFace[currentLine][header.index(indexActionUnit)]))
                            #print(actionUnitPresence)
                            temp[-1].append(actionUnitPresence)

                            validity = True
                            if len(temp[-1][1]) != len(temp[-1][2]):
                                validity=False
                            else :
                                for au in temp[-1][2]:
                                    if au != 1.0:
                                        validity =False
                            temp[-1].append(validity)

                            actionUnitIntensity=[]
                            for intensity in range(0,len(actionUnitsImport[currentAU][1])):
                                if actionUnitsImport[currentAU][1][intensity] <10:
                                    actionUnit= str("AU0"+str(actionUnitsImport[currentAU][1][intensity])+"_r")

                                    for i in range(0,len(header)):
                                        if actionUnit in header[i]:
                                            indexActionUnit = header[i] 
                                            actionUnitIntensity.append(float(csvOpenFace[currentLine][header.index(indexActionUnit)]))
                                else :
                                    actionUnit= str("AU"+str(actionUnitsImport[currentAU][1][intensity])+"_r")

                                    for i in range(0,len(header)):
                                        if actionUnit in header[i]:
                                            indexActionUnit = header[i] 
                                            actionUnitIntensity.append(float(csvOpenFace[currentLine][header.index(indexActionUnit)]))

                            temp[-1].append(actionUnitIntensity)
                            
                            validity = True
                            validity = True
                            if len(temp[-1][1]) != len(temp[-1][4]):
                                validity=False
                            else :
                                for intensity in range(0,len(temp[-1][1])):
                                    if temp[-1][4][intensity] ==0 :#<temp[-1][2][intensity]:
                                        validity =False
                            temp[-1].append(validity)
                        actionUnitsCSV.append(temp)


                            
                    #print(actionUnitsCSV)

                    for au in actionUnitsImport :
                        

                        if not os.path.isdir(os.path.join(pathVideo,"action_units")):
                            os.mkdir(os.path.join(pathVideo,"action_units"))


                        if not os.path.isdir(os.path.join(pathVideo,"action_units",au[0])):
                            os.mkdir(os.path.join(pathVideo,"action_units",au[0]))
                            os.mkdir(os.path.join(pathVideo,"action_units",au[0],"video_aligned"))
                        with open(os.path.join(pathVideo,"action_units",au[0],str(au[0]) + ".csv"), 'w', newline='') as csvfile:
                            csvAU = csv.writer(csvfile, delimiter=',',)
                            csvAU.writerow(header)#header[0:4]
                        csvfile.close()
                    #print(len(actionUnitsCSV))
                    for line in range(0,len(actionUnitsCSV)):
                        for au in range(0,len(actionUnitsCSV[line])):
                            if actionUnitsCSV[line][au][3] == True and actionUnitsCSV[line][au][5] == True:
                                with open(os.path.join(pathVideo,"action_units",actionUnitsCSV[line][au][0],str(actionUnitsCSV[line][au][0]) + ".csv"), 'a', newline='') as csvfile:
                                    csvAU = csv.writer(csvfile, delimiter=',',)
                                    csvAU.writerow(csvOpenFace[line])#csvOpenFace[line][0:4]
                                csvfile.close()

                                face= str(int(csvOpenFace[line][1]))

                                if len(face)<2:
                                    face =  "0" + face

                                frame = str(csvOpenFace[line][0])
                                while (len(frame)) <6:
                                    frame = "0" + frame
                                
                                #print(os.path.join(pathVideo,"video_aligned","frame_det_"+str(face) + "_" + str(frame) + ".bmp"))
                                if os.path.isfile(os.path.join(pathVideo,"video_aligned","frame_det_"+str(face) + "_" + str(frame) + ".bmp")):
                                    shutil.copyfile(os.path.join(pathVideo,"video_aligned","frame_det_"+str(face) + "_" + str(frame) + ".bmp"),os.path.join(pathVideo,"action_units",actionUnitsCSV[line][au][0],"video_aligned","frame_det_"+str(face) + "_" + str(frame) + ".bmp"))

                
                current+=1

            self.processing.emit(str("End Action Units Detection\n" ))
        self.finished.emit(1)


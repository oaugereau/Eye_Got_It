#Welcome.py => Main windows of Eye Got It
#Welcome class => main windows
#DataBase class => main windows for MCQ and database text
#Help class => windows help

#import python Module
import sys, os, webbrowser, shutil, subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
#import others Modules
import About, Function, Config, Parameters, User, Audio, Simulation, Database, Report, Mcq, Video
myApp=None

#Main windows
class Welcome(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        if os.path.isfile("config.ini"):

            if Config.CONFIG_IMPORTED ==False and Config.CONFIG_IMPORTED_ERROR == False:
                Config.ImportConfig()

                if Config.CONFIG_IMPORTED_ERROR == True :
                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("Error in config importation\n Would you like to import default parameters ?")
                    message.setWindowTitle("Config Importation Error")
                    message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)#(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()
                    if message == QtWidgets.QMessageBox.Yes:
                        os.remove("config.ini")
                        shutil.copyfile("config.ini.bak","config.ini")

                        message=QtWidgets.QMessageBox()
                        message.setIcon(QtWidgets.QMessageBox.Critical)
                        message.setText("Default config imported\nPlease restart Eye Got It")
                        message.setWindowTitle("Config Importation Error")
                        message.setStandardButtons(QtWidgets.QMessageBox.Ok)#(QtWidgets.QMessageBox.Ok)
                        message=message.exec_()
                        sys.exit()


                    else:
                        sys.exit()

            if Config.CONFIG_IMPORTED ==True and Config.CONFIG_IMPORTED_ERROR == False and Config.initial_setup == "True":
                print("initial_setup")
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Initial Setup done ! \nYou can add your Database in Eye Got It folder in : \n" + str(Config.EyeGotItFolder))
                message.setWindowTitle("Config Importation")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message=message.exec_()
                Config.configParser.SetParameters("OTHER","initial_setup",False)
                sys.exit() 

            

        else :
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("No config file found")
            message.setWindowTitle("Config Importation")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_()

            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Error in config importation\n Would you like to import default parameters ?")
            message.setWindowTitle("Config Importation Error")
            message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)#(QtWidgets.QMessageBox.Ok)
            message=message.exec_()
            if message == QtWidgets.QMessageBox.Yes:
                try:
                    shutil.copyfile("config.ini.bak","config.ini")

                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("Default config imported\nPlease restart Eye Got It")
                    message.setWindowTitle("Config Importation Error")
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)#(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()
                    sys.exit()
                except :
                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("Error to import default parameters")
                    message.setWindowTitle("Config Importation Error")
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)#(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()
                    sys.exit()


            else:
                sys.exit()
            
                
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Welcome to Eye Got It')
        self.width=250
        self.height=250
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        self.title = QtWidgets.QLabel("Eye Got It",self)
        self.title.setStyleSheet("QLabel"+"{"+"color: " + str("red") +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str("italic") +" " + str(50)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.title, 0,0)


        with open(str(os.path.join(Config.PATH_IMAGE,"eye_got_it.png")),'r') as UseFile:
                pixmap = QtGui.QPixmap(str(os.path.join(Config.PATH_IMAGE,"eye_got_it.png")))
                pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
                self.logo = QtWidgets.QLabel(self)                                                                                                                 
                self.logo.setPixmap(pixmap)  
                self.grid.addWidget(self.logo, 0,1) 

        self.simulation = QtWidgets.QPushButton('Start Recording', self)
        self.simulation.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.simulation, 1,0)
        self.simulation.clicked.connect(self.simulation_click)


        self.report = QtWidgets.QPushButton('Generate Report', self)
        self.report.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.report, 1,1)
        self.report.clicked.connect(self.report_click)

        self.about = QtWidgets.QPushButton('About', self)
        self.about.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.about, 2,0)
        self.about.clicked.connect(self.about_click)

        self.parameters = QtWidgets.QPushButton('Parameters', self)
        self.parameters.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.parameters, 2,1)
        self.parameters.clicked.connect(self.parameters_click)
        

        self.user = QtWidgets.QPushButton('User', self)
        self.user.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.user, 3,0)
        self.user.clicked.connect(self.user_click)

        

        self.database = QtWidgets.QPushButton('Database', self)
        self.database.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.database, 3,1)
        self.database.clicked.connect(self.database_click)

        self.version = QtWidgets.QLabel(str("Version " + Config.VERSION),self)
        self.version.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(18)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.version, 5,0)

        self.quit = QtWidgets.QPushButton('Exit', self)
        self.quit.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.quit, 4,1)
        self.quit.clicked.connect(self.exit)

        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 5,1)
        self.help.clicked.connect(self.help_click)
        self.help.setEnabled(True) 

        if Config.DEBUG:
            self.debug = QtWidgets.QLabel("DEBUG Mode ",self)
            self.debug.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str("red") +";"
                        "font: "+ str(Config.fontType) +" " + str(15)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
            self.grid.addWidget(self.debug, 5,0)

        print("screen resolution:",Config.SCREEN_WIDTH,Config.SCREEN_HEIGHT) 
        print("physical size in mm:",Config.PHYSICAL_SCREEN_WIDTH,Config.PHYSICAL_SCREEN_HEIGHT)

        self.askQuit=True

    #about windows    
    def about_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()

        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        self.aboutWindows = About.About()
        self.aboutWindows.show()

    #parameter windows 
    def parameters_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()

        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        self.parametersWindows = Parameters.Parameters()
        self.askQuit=False
        self.parametersWindows.show()
        self.close()

    def exit(self):
        self.askQuit=True
        self.close()
    #user windows
    def user_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()

        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        self.userWindows = User.UserDisplay()
        self.userWindows.show()

    #simulation windows
    def simulation_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()

        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        self.simulWindows = Simulation.SimulationConfig(self)
        self.simulWindows.show()
        self.hide()

    #report windows
    def report_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()

        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        self.reportWindows = Report.ReportDisplay(self)
        self.reportWindows.show()

    #MCQ and text database windows
    def database_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()

        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        self.dataBaseWindows = DataBase()
        self.dataBaseWindows.show()

    #help windows
    def help_click(self):
        if hasattr(self, "aboutWindows"):
            self.aboutWindows.close()
        
        if hasattr(self, "userWindows"):
            self.userWindows.close()

        if hasattr(self, "dataBaseWindows"):
            self.dataBaseWindows.close()
        
        if hasattr(self, "reportWindows"):
            self.reportWindows.close()

        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

        if Config.documentationHTML:
            helpHtml()
        else:
            self.helpWindows = Help()
            self.helpWindows.show()
    
    #close Eye Got It
    def closeEvent(self, event):
        if self.askQuit:

            reply=QtWidgets.QMessageBox()
            reply.setIcon(QtWidgets.QMessageBox.Question)
            reply.setText("Are you sure you want to exit the program ?")
            reply.setWindowTitle("Quit")
            reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            reply=reply.exec_()

            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
                print("Good Bye !")
                myApp.quit()

            else:
                event.ignore()

#main windows for MCQ and text database
class DataBase(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('DataBase Windows')
        self.width=200
        self.height=150
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        self.database = QtWidgets.QPushButton('Database gestion', self)
        self.database.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.database, 0,0)
        self.database.clicked.connect(self.database_click)

        self.mcq = QtWidgets.QPushButton('MCQ Management', self)
        self.mcq.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.mcq, 0,1)
        self.mcq.clicked.connect(self.mcq_click)

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 1,0)
        self.back.clicked.connect(self.close)

        self.openDatabaseFolder = QtWidgets.QPushButton('Open Database Folder', self)
        self.openDatabaseFolder.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.openDatabaseFolder, 1,1)
        self.openDatabaseFolder.clicked.connect(self.openDatabaseFolder_click)


    #test database windows   
    def database_click(self):
        self.databaseWindows = Database.DatabaseDisplay()
        self.databaseWindows.show()
    
    #MCQ windows
    def mcq_click(self):
        self.mcqWindows = Mcq.McqCreation()
        self.mcqWindows.show()

    def openDatabaseFolder_click(self):
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        subprocess.run([FILEBROWSER_PATH, os.path.join(Config.DatabaseFolder)])


    #close windows
    def closeEvent(self, event):
        if hasattr(self, "mcqWindows"):
            self.mcqWindows.close()

        if hasattr(self, "databaseWindows"):
            self.databaseWindows.close()
def helpHtml():
    webbrowser.open_new_tab('file://'+str(Config.documentationWelcome))
    
#help windows
class Help(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Help Windows')
        self.width=200
        self.height=200
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        self.Label = QtWidgets.QLabel("Recording : record yourself reading different text\n\n"
                                      "Report : generate report from your recording\n\n"
                                      "Database : manage your database, add new ones and add/modify mcq\n\n"
                                      "User : manage users, add new one or modify current users\n\n"
                                      "Parameters : change parameters and test devices(audio,video,eyeTracker)\n\n"
                                      "About : software information")
        self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.Label,0,0)
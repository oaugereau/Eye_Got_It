#Database.py => text database
#database class => import and create the database
#DatabaseDisplay class => Database main windows
#DatabaseManagement class => Database management (create or edit database)
#Help class windows help

#import python Module
import time, sys, os, io, subprocess, webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui
#import others Modules
import ConfigFileManagement, Function, Config

#import and create the database
class Database():

    def __init__(self,databaseName):
        self.databaseName = databaseName
        #self.extensionTxt=""
        self.separator=""
        self.singleFolder=""
        self.folder=""

    #import the database text
    def CreateConfig(self):
        self.config={}
        self.databaseConfig=ConfigFileManagement.ConfigFileRead(os.path.join(Config.DatabaseFolder,self.databaseName,'config.ini'))

        self.config["Language"]=self.databaseConfig.GetParameters("LANGUAGE","language").split(",")
        #self.config["Language"].sort()
        self.config["Level"]=self.databaseConfig.GetParameters("LEVEL","level").split(",")
        #self.config["Level"].sort()
        self.language = self.databaseConfig.GetParameters("LANGUAGE","language")
        self.level = self.databaseConfig.GetParameters("LEVEL","level")
        self.folder=self.databaseConfig.GetParameters("DATABASE","folder")

        self.languageExist = True if self.language != "" else False 
        self.levelExist = True if self.level != "" else False     
        self.separator=self.databaseConfig.GetParameters("DATABASE","separator")

        #fisrt database type
        if self.languageExist and self.levelExist    :   
        
            for language in self.config["Language"]:
                for level in self.config["Level"]:
                    self.config[str(language + "_" + level)]=[]

            self.config["Title"] = []
            for elem in os.listdir(os.path.join(Config.DatabaseFolder,self.databaseName,self.folder)):
                if self.separator == '.':
                    txt=elem.split(self.separator)
                    if not "csv" in txt:
                        for language in self.config["Language"]:
                            for level in self.config["Level"]:
                                if language in txt:
                                    if level in txt:
                                        self.config[str(language + "_" + level)].append(elem)
                                        txt.pop(txt.index(language))
                                        txt.pop(txt.index(level))
                                        txt.pop(txt.index("txt"))
                                        if txt not in self.config["Title"]:
                                            self.config["Title"].append(txt)

                else :
                    txt=elem.split('.')
                    extension = txt[1]
                    txtTemp=txt[0].split(self.separator)
                    txt=[]
                    for i in txtTemp:
                        txt.append(i)
                    txt.append(extension)
                    if not "csv" in txt:
                        for language in self.config["Language"]:
                            for level in self.config["Level"]:
                                if language in txt:
                                    if level in txt:
                                        self.config[str(language + "_" + level)].append(elem)
                                        txt.pop(txt.index(language))
                                        txt.pop(txt.index(level))
                                        txt.pop(txt.index("txt"))
                                        if txt not in self.config["Title"]:
                                            self.config["Title"].append(txt)
           
        #second database type
        if self.languageExist and not self.levelExist    :   
        
            for language in self.config["Language"]:
                self.config[str(language)]=[]

            self.config["Title"] = []
            for elem in os.listdir(os.path.join(Config.DatabaseFolder,self.databaseName,self.folder)):
                if self.separator == '.':
                    txt=elem.split(self.separator)
                    if not "csv" in txt:
                        for language in self.config["Language"]:
                            
                            if language in txt:
                                
                                self.config[str(language)].append(elem)
                                txt.pop(txt.index(language))
                                txt.pop(txt.index("txt"))
                                if txt not in self.config["Title"]:
                                    self.config["Title"].append(txt)

                else :
                    txt=elem.split('.')
                    extension = txt[1]
                    txtTemp=txt[0].split(self.separator)
                    txt=[]
                    for i in txtTemp:
                        txt.append(i)
                    txt.append(extension)
                    if not "csv" in txt:
                        for language in self.config["Language"]:
                            if language in txt:
                                self.config[str(language)].append(elem)
                                txt.pop(txt.index(language))
                                txt.pop(txt.index("txt"))
                                if txt not in self.config["Title"]:
                                    self.config["Title"].append(txt)
        #third database type
        if not self.languageExist and self.levelExist    :   
        
            for level in self.config["Level"]:
                self.config[str(level)]=[]

            self.config["Title"] = []
            for elem in os.listdir(os.path.join(Config.DatabaseFolder,self.databaseName,self.folder)):
                if self.separator == '.':
                    txt=elem.split(self.separator)
                    if not "csv" in txt:
                        for level in self.config["Level"]:
                            if level in txt:
                                self.config[str(level)].append(elem)
                                txt.pop(txt.index(level))
                                txt.pop(txt.index("txt"))
                                if txt not in self.config["Title"]:
                                    self.config["Title"].append(txt)

                else :
                    txt=elem.split('.')
                    extension = txt[1]
                    txtTemp=txt[0].split(self.separator)
                    txt=[]
                    for i in txtTemp:
                        txt.append(i)
                    txt.append(extension)
                    if not "csv" in txt:
                        for level in self.config["Level"]:
                            if level in txt:
                                self.config[str(level)].append(elem)
                                txt.pop(txt.index(level))
                                txt.pop(txt.index("txt"))
                                if txt not in self.config["Title"]:
                                    self.config["Title"].append(txt)

        #fourthly database type
        if not self.languageExist and not self.levelExist    :  
            self.config["Text"] = []
            for elem in os.listdir(os.path.join(Config.DatabaseFolder,self.databaseName,self.folder)):
                txt=elem.split(".")
                if not "csv" in txt:
                    #print(elem)
                    self.config["Text"].append(elem)       

                
    #get database parameter        
    def get(self,key):
        return self.config[key]

#Database main windows
class DatabaseDisplay(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        if not os.path.isdir(Config.DatabaseFolder):
                os.makedirs(Config.DatabaseFolder) 

        Config.databaseListCreate()

        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Database Gestion')
        self.width=350
        self.height=150
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid) 

        #widgets
        self.database = QtWidgets.QLabel("Choose Database :",self)
        self.database.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.database, 0,0)

        self.databaseEdit = QtWidgets.QComboBox(self)
        self.databaseEdit.addItems(Config.DatabaseList)
        self.databaseEdit.setCurrentIndex(-1)
        self.databaseEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.databaseEdit, 0,1,1,2)
        self.databaseEdit.currentIndexChanged[int].connect(self.on_currentIndexChanged)

        self.add = QtWidgets.QPushButton('Add Database', self)
        self.add.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.add, 1,0)
        self.add.clicked.connect(self.add_click)

        self.select = QtWidgets.QPushButton('Select', self)
        self.select.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.select, 1,1)
        self.select.clicked.connect(self.select_click)
        self.select.setEnabled(False)

        self.openDatabaseFolder = QtWidgets.QPushButton('Open Database Folder', self)
        self.openDatabaseFolder.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.openDatabaseFolder, 1,2)
        self.openDatabaseFolder.clicked.connect(self.openDatabaseFolder_click)
        self.openDatabaseFolder.setEnabled(False)

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 2,0)
        self.back.clicked.connect(self.close)

        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 2,1)
        self.help.clicked.connect(self.help_click)
        self.help.setEnabled(True)

    #add database
    def add_click(self):
        self.databaseAddWindows = DatabaseManagement(self.databaseEdit,True)
        self.databaseAddWindows.show()
    
    #select database
    def select_click(self):
        self.databaseView = DatabaseManagement(self.databaseEdit.currentText(),False)
        self.databaseView.show()

    #help windows
    def help_click(self):
        if Config.documentationHTML:
            helpHtml()
        else:
            self.helpWindows = Help()
            self.helpWindows.show()

    #enable select button
    def on_currentIndexChanged(self, index):
        
        if not self.databaseEdit.currentText() =='':
            self.openDatabaseFolder.setEnabled(True)
            self.select.setEnabled(True)

        else :
            self.openDatabaseFolder.setEnabled(False)
            self.select.setEnabled(False)

    def openDatabaseFolder_click(self):
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        subprocess.run([FILEBROWSER_PATH, os.path.join(Config.DatabaseFolder,self.databaseEdit.currentText())])


    #close windows
    def closeEvent(self, event):
        if hasattr(self, "databaseAddWindows"):
            self.databaseAddWindows.close()
        if hasattr(self, "databaseView"):
            self.databaseView.close()
        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

#Database management (create or edit database)
class DatabaseManagement(QtWidgets.QWidget):

    def __init__(self,database,newDatabase):
        QtWidgets.QWidget.__init__(self)
        self.newDatabase = newDatabase
        if not self.newDatabase:
            self.databaseName=database
            self.database=Database(os.path.join(Config.DatabaseFolder,database))
            self.database.CreateConfig()

        else :
            self.databaseList=database
            databaseList=os.listdir(os.path.join(Config.DatabaseFolder))
            databaseList.sort()
            directory_contents = []
            for elem in databaseList:
                if len(elem.split('.'))==1 and not os.path.isfile(os.path.join(Config.DatabaseFolder,elem,"config.ini")):
                    directory_contents.append(elem)
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")

        if not self.newDatabase:
            self.setWindowTitle(str('Database View : ' + self.databaseName))
            self.width=800
            self.height=150
            self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        else :
            self.setWindowTitle(str('Database Creator : '))
            self.width=350
            self.height=100
            self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets
        if self.newDatabase:
            self.chooseNew = QtWidgets.QLabel("Choose New Database :",self)
            self.chooseNew.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
            self.grid.addWidget(self.chooseNew, 0,0)

            self.chooseNewEdit = QtWidgets.QComboBox(self)
            self.chooseNewEdit.addItems(directory_contents)
            self.chooseNewEdit.setCurrentIndex(-1)
            self.chooseNewEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
            self.grid.addWidget(self.chooseNewEdit, 0,1)
            self.chooseNewEdit.currentIndexChanged[int].connect(self.on_currentIndexChanged)


        self.separator = QtWidgets.QLabel("Separator :",self)
        self.separator.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.separator, 1,0)
        if self.newDatabase:
            self.separator.hide()
        
       
        self.separatorEdit=QtWidgets.QLineEdit(self)
        if not self.newDatabase:
            self.separatorEdit.setText(str(self.database.separator))
        self.separatorEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.separatorEdit, 1,1)
        self.separatorEdit.textChanged.connect(self.databaseType)
        self.separatorEdit.setReadOnly(False)
        if self.newDatabase:
            self.separatorEdit.hide()

        self.folder = QtWidgets.QLabel("Folder :",self)
        self.folder.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.folder, 1,2)
        if self.newDatabase:
            self.folder.hide()
        

        self.folderNameEdit=QtWidgets.QLineEdit(self)
        if not self.newDatabase:
            self.folderNameEdit.setText(str(self.database.folder))
        self.folderNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont if not self.newDatabase else "red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.folderNameEdit, 1,3)
        self.folderNameEdit.textChanged.connect(lambda:self.defaultEdit(self.folderNameEdit))
        self.folderNameEdit.setReadOnly(False)
        if self.newDatabase:
            self.folderNameEdit.hide()


        self.language= QtWidgets.QLabel("Language  :",self)
        self.language.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.language, 2,0)
        if self.newDatabase:
            self.language.hide() 

        self.languageEdit=QtWidgets.QLineEdit(self)
        if not self.newDatabase:
            self.languageEdit.setText(str(self.database.language))
        self.languageEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.languageEdit, 2,1)
        self.languageEdit.textChanged.connect(self.databaseType)
        self.languageEdit.setReadOnly(False)
        if self.newDatabase:
            self.languageEdit.hide()

        self.level= QtWidgets.QLabel("Level  :",self)
        self.level.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.level, 2,2)
        if self.newDatabase:
            self.level.hide()
        
        
        self.levelEdit=QtWidgets.QLineEdit(self)
        if not self.newDatabase:
            self.levelEdit.setText(str(self.database.level))
        self.levelEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.levelEdit, 2,3)
        self.levelEdit.textChanged.connect(self.databaseType)
        self.levelEdit.setReadOnly(False)
        if self.newDatabase:
            self.levelEdit.hide()


        self.save = QtWidgets.QPushButton('Save', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.save, 4,1)
        if not self.newDatabase:
            self.save.clicked.connect(self.save_click)#(lambda:save_click(self,False))
        else :self.save.clicked.connect(self.save_click)#(lambda:save_click(self,True))
        if self.newDatabase:
            self.save.hide()

        self.back = QtWidgets.QPushButton('Back', self)
        self.back.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.back, 4,0)
        self.back.clicked.connect(self.close)

        self.help = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.help.setIcon(icon)       
        self.help.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.help, 4,2)
        self.help.clicked.connect(helpHtml)
        self.help.setEnabled(True)

    #clear when choose another new database
    def on_currentIndexChanged(self, index):
        
        if self.chooseNewEdit.currentText() !='':
            self.separator.show()
            self.separatorEdit.show()
            self.separatorEdit.clear()
            self.folder.show()
            self.folderNameEdit.show()
            self.folderNameEdit.clear()
            self.language.show()
            self.languageEdit.show()
            self.languageEdit.clear
            self.level.show()
            self.levelEdit.show()
            self.levelEdit.clear
            self.save.show()

    #change color if not correctly completed
    def databaseType(self):

        if self.separatorEdit.text() == "" and (self.languageEdit.text() != "" or self.levelEdit.text() != ""):
            self.separatorEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str("red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
                        
        elif self.separatorEdit.text() != "" and (self.languageEdit.text() == "" and self.levelEdit.text() == ""):

            self.languageEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str("yellow") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

            self.levelEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str("yellow") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        
        elif len(self.languageEdit.text().split('.')) > 1 or len(self.languageEdit.text().split('/')) > 1 or len(self.languageEdit.text().split('-')) > 1 or len(self.languageEdit.text().split("\\")) > 1:
            self.languageEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        elif len(self.levelEdit.text().split('.')) > 1 or len(self.levelEdit.text().split('/')) > 1 or len(self.levelEdit.text().split('-')) > 1 or len(self.levelEdit.text().split("\\")) > 1:
            self.levelEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";")

        #empty color if no problems
        else :
            self.separatorEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

            self.languageEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

            self.levelEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

    #default database parameters (here text folder)                       
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

    #save database in config file
    def save_click(self):
        if self.newDatabase:
            folder = os.path.isdir(os.path.join(Config.DatabaseFolder,self.chooseNewEdit.currentText(),self.folderNameEdit.text()))
        else :
            folder = os.path.isdir(os.path.join(Config.DatabaseFolder,self.databaseName,self.folderNameEdit.text()))

        if folder:
            if  self.folderNameEdit.text() != '':
                if self.newDatabase :
                    if self.separatorEdit.text() == '' and(self.languageEdit.text() == '' and self.levelEdit.text() == '') or self.separatorEdit.text() != '' and(self.languageEdit.text() != '' or self.levelEdit.text() != ''):
                        configCreate= ConfigFileManagement.ConfigFileWrite()
                        configCreate.SetParameters("DATABASE","separator",self.separatorEdit.text())
                        configCreate.SetParameters("DATABASE","folder",self.folderNameEdit.text())
                        configCreate.SetParameters("LANGUAGE","language",self.languageEdit.text())
                        configCreate.SetParameters("LEVEL","level",self.levelEdit.text())
                        configCreate.CreateFile(os.path.join(Config.DatabaseFolder,self.chooseNewEdit.currentText(),"config.ini"))

                        Config.databaseListCreate()
                        Function.UpdateComboBox(self.databaseList, Config.DatabaseList)

                    
                        self.close()
                        message=QtWidgets.QMessageBox()
                        message.setIcon(QtWidgets.QMessageBox.Information)
                        message.setText(self.chooseNewEdit.currentText()+" config created")
                        message.setWindowTitle("Database")
                        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        message=message.exec_()


                else:
                    if (self.separatorEdit.text() == '' and(self.languageEdit.text() == '' and self.levelEdit.text() == '') or self.separatorEdit.text() != '' and(self.languageEdit.text() != '' or self.levelEdit.text() != '')):
                        configChanged = False

                        if self.languageEdit.text() != self.database.language:
                            self.database.databaseConfig.SetParameters("LANGUAGE","language",self.languageEdit.text())
                            configChanged = True

                        if self.levelEdit.text() != self.database.level:
                            self.database.databaseConfig.SetParameters("LEVEL","level",self.levelEdit.text())
                            configChanged = True
                        
                        if self.separatorEdit.text() != self.database.separator:
                            self.database.databaseConfig.SetParameters("DATABASE","separator",self.separatorEdit.text())
                            configChanged = True
                        
                        if self.folderNameEdit.text() != self.database.folder :
                            self.database.databaseConfig.SetParameters("DATABASE","folder",self.folderNameEdit.text())
                            configChanged = True

                        if  configChanged :
                            message=QtWidgets.QMessageBox()
                            message.setIcon(QtWidgets.QMessageBox.Information)
                            message.setText("New parameters of "+self.databaseName+"saved")
                            message.setWindowTitle("Database")
                            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            message=message.exec_()

                        else :
                            message=QtWidgets.QMessageBox()
                            message.setIcon(QtWidgets.QMessageBox.Information)
                            message.setText("Parameters not saved because you didn't change parameters")
                            message.setWindowTitle("Database")
                            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            message=message.exec_()
                        self.close()
        else:
            print("error")
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText(str("Not folder " + self.folderNameEdit.text() + " in " + (self.chooseNewEdit.currentText() if self.newDatabase else self.databaseName)))
            message.setWindowTitle("Database")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_() 

def helpHtml():
    webbrowser.open_new_tab(Config.documentationDatabase)
                       
#windows help => OLD VERSION
class Help(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Help Windows')
        self.width=1200
        self.height=650
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets

        self.Label = QtWidgets.QLabel("Steps to add a new Database:\n\n"
                                      "-Open the 'Eye Got It' folder in your User folder\n\n"
                                      "-Create a new folder in the Database folder, give it the name of your Database\n\n"
                                      "-Create one last folder inside with all your texts\n\n"
                                      "-Text name rules : there must be a separator( '_' or '.' for example)\nbetween the title, the language and the level of the text(order not important)\n"
                                      "examples : 'title_en_0.txt' / '0_es_title.txt' / 'fr.title.0.txt' / 'title.en.A1.txt'\n"
                                      "texts must be encoded with UTF-8\n\n"
                                      "-Click on 'Add Database' and select the one you just added\n\n"
                                      "-Specify the separator, the name of the folder with all the text\nand the different languages and levels of your texts separated with a ','\n"
                                      "(if you don't have multiple languages or levels just leave the line empty,\n"
                                      "however if you have just a list of text with no precision on the language and level\n"
                                      "leave everything empty apart from the folder name)\n\n"
                                      "-Click on save")
        self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.Label,0,0)

        try:
            with open(str(os.path.join(Config.PATH_IMAGE,"database_example.jpg")),'r') as UseFile:
                pixmap = QtGui.QPixmap(str(os.path.join(Config.PATH_IMAGE,"database_example.jpg")))
                self.example = QtWidgets.QLabel(self)                                                                                                                 
                self.example.setPixmap(pixmap)  
                self.grid.addWidget(self.example, 0,1) 
        except:
            #file no exist or no file chosen
            #self.MessageBox("Image error",str(location + " not found"),"warning","","","")
            pass
#Mcq.py => manage MCQ and answer to MCQ
#McqCreation class => Create or edit MCQ
#Mcq class => answer MCQ

#import python Module
import sys, os, csv, webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui
#import others Modules
import Function, Config, Welcome

#MCQ Management
class McqCreation(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setWindowTitle("MCQ Management")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=500
        self.height=250
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        Config.databaseListCreate()

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

#text selection widgets#

        self.databaseGroupBox = QtWidgets.QGroupBox("Select the Database")
        self.databaseGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.databaseLayout = QtWidgets.QVBoxLayout()

        #self.instructionLabel = QtWidgets.QLabel("Select to wich text you want to add or modify a MCQ",self)
        #self.instructionLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
        #                "background-color: " + str(Config.colorFont) +";"
        #                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
        #                "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.instructionLabel, 0,0,1,2)
        #self.instructionLabel.hide()

        #self.databaseLabel = QtWidgets.QLabel("Select database:",self)
        #self.databaseLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
        #                "background-color: " + str(Config.colorFont) +";"
        #                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
        #                "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.databaseLabel, 1,0)

        self.database = QtWidgets.QComboBox(self)
        self.database.addItems(Config.DatabaseList)
        self.database.setCurrentIndex(-1)
        self.database.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.database, 1,1)
        self.database.activated.connect(self.database_select)
        self.databaseLayout.addWidget(self.database)

        self.databaseGroupBox.setLayout(self.databaseLayout)

        self.grid.addWidget(self.databaseGroupBox,0,0,1,3)


        self.textGroupBox = QtWidgets.QGroupBox("Text")
        self.textGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.textLayout = QtWidgets.QFormLayout()

        self.languageLabel = QtWidgets.QLabel("Language:",self)
        self.languageLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.languageLabel, 2,0)
        self.languageLabel.hide()

        self.languageList = QtWidgets.QComboBox(self)
        self.languageList.addItems([])
        self.languageList.setCurrentIndex(-1)
        self.languageList.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.languageList, 2,1) 
        self.languageList.activated.connect(self.language_select)
        self.languageList.setEnabled(False)
        self.languageList.hide()
        self.textLayout.addRow(self.languageLabel, self.languageList)

        self.levelLabel = QtWidgets.QLabel("Level:",self)
        self.levelLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.levelLabel, 3,0)
        self.levelLabel.hide()

        self.levelList = QtWidgets.QComboBox(self)
        self.levelList.addItems([])
        self.levelList.setCurrentIndex(-1)
        self.levelList.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.levelList, 3,1) 
        self.levelList.activated.connect(self.level_select)
        self.levelList.setEnabled(False)
        self.levelList.hide()
        self.textLayout.addRow(self.levelLabel, self.levelList)

        self.textLabel = QtWidgets.QLabel("Text:",self)
        self.textLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.textLabel, 4,0)
        self.textLabel.hide()

        self.textList = QtWidgets.QComboBox(self)
        self.textList.addItems([])
        self.textList.setCurrentIndex(-1)
        self.textList.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.textList, 4,1) 
        self.textList.activated.connect(self.text_select)
        self.textList.setEnabled(False)
        self.textList.hide()
        self.textLayout.addRow(self.textLabel, self.textList)

        self.textGroupBox.setLayout(self.textLayout)
        self.textGroupBox.hide()
        self.grid.addWidget(self.textGroupBox,1,0,1,3)

        self.ok = QtWidgets.QPushButton('OK', self)
        self.ok.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.ok, 2,2) 
        self.ok.clicked.connect(self.ok_click)
        self.ok.setEnabled(False)

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
        self.help.clicked.connect(self.helpHtml)
        self.help.setEnabled(True) 
        


#questions and answers edit widgets#
        self.mcq = False
        self.answerManagementGroupBox = QtWidgets.QGroupBox("Edit Answers")
        self.answerManagementGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.answerManagementLayout = QtWidgets.QVBoxLayout()

        self.add = QtWidgets.QPushButton('Add', self)
        self.add.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.add, 1,0) 
        self.answerManagementLayout.addWidget(self.add)
        self.add.clicked.connect(lambda:self.add_click(""))
        #self.add.hide()

        self.remove = QtWidgets.QPushButton('Remove', self)
        self.remove.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.remove, 2,0) 
        self.answerManagementLayout.addWidget(self.remove)
        self.remove.clicked.connect(self.remove_click)
        #self.remove.hide()

        self.answerManagementGroupBox.setLayout(self.answerManagementLayout)

        self.grid.addWidget(self.answerManagementGroupBox,3,0)
        self.answerManagementGroupBox.hide()


        self.questionManagementGroupBox = QtWidgets.QGroupBox("Edit Question")
        self.questionManagementGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.questionManagementLayout = QtWidgets.QVBoxLayout()

        self.addQuestion = QtWidgets.QPushButton('Add', self)
        self.addQuestion.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.addQuestion, 3,2) 
        self.questionManagementLayout.addWidget(self.addQuestion)
        self.addQuestion.clicked.connect(lambda:self.addQuestion_click(True))
        #self.addQuestion.setEnabled(False)


        self.deleteQuestion = QtWidgets.QPushButton('Delete', self)
        self.deleteQuestion.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.deleteQuestion, 3,1) 
        self.questionManagementLayout.addWidget(self.deleteQuestion)
        self.deleteQuestion.clicked.connect(self.deleteQuestion_click)
        #self.deleteQuestion.setEnabled(False)

        self.questionManagementGroupBox.setLayout(self.questionManagementLayout)

        self.grid.addWidget(self.questionManagementGroupBox,3,2)
        self.questionManagementGroupBox.hide()

        self.questionGroupBox = QtWidgets.QGroupBox()
        self.questionGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.questionLayout = QtWidgets.QHBoxLayout()
        
        self.previousQuestion = QtWidgets.QPushButton('<-- previous question', self)
        self.previousQuestion.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.previousQuestion, 3,0)
        self.questionLayout.addWidget(self.previousQuestion) 
        self.previousQuestion.clicked.connect(self.previousQuestion_click)
        self.previousQuestion.hide()

        self.nextQuestion = QtWidgets.QPushButton('next question -->', self)
        self.nextQuestion.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.nextQuestion, 3,2) 
        self.questionLayout.addWidget(self.nextQuestion)
        self.nextQuestion.clicked.connect(self.nextQuestion_click)
        self.nextQuestion.hide()

        self.questionGroupBox.setLayout(self.questionLayout)
        self.questionGroupBox.hide()

        self.grid.addWidget(self.questionGroupBox,4,0,1,3)

        self.save = QtWidgets.QPushButton('save MCQ', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.save, 5,2) 
        self.save.clicked.connect(self.save_click)
        self.save.hide()

        self.backMCQ = QtWidgets.QPushButton('Back', self)
        self.backMCQ.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.backMCQ, 5,0)
        self.backMCQ.clicked.connect(self.reset)
        self.backMCQ.hide()

        self.helpMCQ = QtWidgets.QPushButton(' ',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Config.HelpIcon))#(QtGui.QPixmap(os.path.join(Config.PATH_IMAGE,"help.png")))
        self.helpMCQ.setIcon(icon)       
        self.helpMCQ.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.helpMCQ, 5,1)
        self.helpMCQ.clicked.connect(self.helpHtml)
        self.helpMCQ.setEnabled(True) 
        self.helpMCQ.hide()
        
        self.page=[]
        self.questionTab=[]
        
        self.currentQuestion=0

    def helpHtml(self):
        webbrowser.open_new_tab('file://'+str(Config.documentationMCQ))

#text selection functions#

    def database_select(self,index):
        Config.CreateDatabase(self.database.currentText())
        self.textGroupBox.show()
        if Config.database.languageExist and Config.database.levelExist:
            language_contents=Config.database.get("Language")
            Function.UpdateComboBox(self.languageList,language_contents)
            Function.UpdateComboBox(self.levelList,[])
            Function.UpdateComboBox(self.textList,[])
            self.languageLabel.show()
            self.languageList.show()
            self.levelLabel.show()
            self.levelList.show()
            self.textLabel.show()
            self.textList.show()
            self.languageList.setEnabled(True)
            self.levelList.setEnabled(False)
            self.textList.setEnabled(False)
            self.ok.setEnabled(False)

        if Config.database.languageExist and not Config.database.levelExist:
            language_contents=Config.database.get("Language")
            Function.UpdateComboBox(self.languageList,language_contents)
            Function.UpdateComboBox(self.textList,[])
            self.languageLabel.show()
            self.languageList.show()
            self.levelLabel.hide()
            self.levelList.hide()
            self.textLabel.show()
            self.textList.show()
            self.languageList.setEnabled(True)
            self.ok.setEnabled(False)
            self.textList.setEnabled(True)

        if not Config.database.languageExist and Config.database.levelExist:
            level_contents=Config.database.get("Level")
            Function.UpdateComboBox(self.levelList,level_contents)
            Function.UpdateComboBox(self.textList,[])
            self.languageLabel.hide()
            self.languageList.hide()
            self.levelLabel.show()
            self.levelList.show()
            self.textLabel.show()
            self.textList.show()
            self.levelList.setEnabled(True)
            self.textList.setEnabled(False)
            self.ok.setEnabled(False)

        if not Config.database.languageExist and not Config.database.levelExist:
            text_contents=Config.database.get("Text")
            Function.UpdateComboBox(self.textList,text_contents)
            self.textList.setEnabled(True)
            self.languageLabel.hide()
            self.languageList.hide()
            self.levelLabel.hide()
            self.levelList.hide()
            self.textLabel.show()
            self.textList.show()
            self.ok.setEnabled(False)


    def language_select(self):
        if Config.database.levelExist:
            level_contents=Config.database.get("Level")
            Function.UpdateComboBox(self.levelList,level_contents)
            Function.UpdateComboBox(self.textList,[])
            self.levelList.setEnabled(True)
            self.textList.setEnabled(False)
            self.ok.setEnabled(False)
        else :
            text_contents=Config.database.get(str(self.languageList.currentText() ))
            Function.UpdateComboBox(self.textList,text_contents)
            self.textList.setEnabled(True)
            self.ok.setEnabled(False)

    def level_select(self):
        if Config.database.languageExist:
            text_contents=Config.database.get(str(self.languageList.currentText() + "_" + self.levelList.currentText()))
            Function.UpdateComboBox(self.textList,text_contents)
            self.textList.setEnabled(True)
            self.ok.setEnabled(False)

        else :
            text_contents=Config.database.get(str(self.levelList.currentText()))
            Function.UpdateComboBox(self.textList,text_contents)
            self.ok.setEnabled(False)
            self.textList.setEnabled(True)

    def text_select(self):
        self.ok.setEnabled(True)

    def createAnswersGroupBox(self):
        
        self.answersGroupBox = QtWidgets.QGroupBox("Answers")
        self.answersGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.grid.addWidget(self.answersGroupBox,2,0,1,3)

    def refreshAnswersGroupBox(self,layout):
        self.answersGroupBox.close()
        self.createAnswersGroupBox()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.answersGroupBox.setLayout(layout)#(self.answersLayout[self.currentQuestion])
        size = layout.sizeHint()
        self.answersGroupBox.resize(size)
        self.grid.addWidget(self.answersGroupBox,2,0,1,3)
        #self.adjustSize()

    def createQuestionTitleGroupBox(self):
        self.questionTitleGroupBox = QtWidgets.QGroupBox("Question Title")
        self.questionTitleGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

        self.grid.addWidget(self.questionTitleGroupBox,1,0,1,3)
        
        

    def refreshQuestionTitleGroupBox(self,layout):
        self.questionTitleGroupBox.close()
        self.createQuestionTitleGroupBox()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.questionTitleGroupBox.setLayout(layout)#(self.answersLayout[self.currentQuestion])
        size = layout.sizeHint()
        self.questionTitleGroupBox.resize(size)
        #self.grid.addWidget(self.questionTitleGroupBox,1,0,1,3)
        #|self.questionTitleGroupBox.adjustSize()


    def createRightAnswerGroupBox(self):
        self.rightAnswerGroupBox = QtWidgets.QGroupBox("Select the right answer")
        self.rightAnswerGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

        self.grid.addWidget(self.rightAnswerGroupBox,3,1)
        

    def refreshRightAnswerGroupBox(self,layout):
        self.rightAnswerGroupBox.close()
        self.createRightAnswerGroupBox()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.rightAnswerGroupBox.setLayout(layout)#(self.answersLayout[self.currentQuestion])
        size = layout.sizeHint()
        self.rightAnswerGroupBox.resize(size)
        self.grid.addWidget(self.rightAnswerGroupBox,3,1)
        #self.adjustSize()

    def ok_click(self):
        self.page=[]
        self.questionTab=[]
        self.policeSizeHeight = self.policeSize()
        self.currentQuestion=0
        
        self.firstQuestionDone = False
        Config.TXT_IMPORT=os.path.join(Config.DatabaseFolder,Config.databaseName,Config.database.folder,self.textList.currentText())
        textName=os.path.split(Config.TXT_IMPORT)[1]
        textName=os.path.splitext(Config.TXT_IMPORT)[0]
        mcqCsv=str(textName+'.csv')
        databasePath=os.path.join(Config.DatabaseFolder,Config.databaseName,Config.database.folder,mcqCsv)

        #self.createAnswersGroupBox()
        self.answersLayout =[]
        self.exist = False


        self.questionGroupBox.show()
        
        """
        self.instructionLabel.hide()
        self.database.hide()
        self.databaseLabel.hide()
        self.languageList.hide()
        self.languageLabel.hide()
        self.levelList.hide()
        self.levelLabel.hide()
        self.textList.hide()
        self.textLabel.hide()
        """
        self.databaseGroupBox.hide()
        self.textGroupBox.hide()
        self.back.hide()
        self.ok.hide()
        self.help.hide()
        self.answerManagementGroupBox.show()
        #self.rightAnswerGroupBox.show()
        self.save.show()
        self.questionManagementGroupBox.show()
        self.createQuestionTitleGroupBox()
        self.createRightAnswerGroupBox()
        self.createAnswersGroupBox()
        self.backMCQ.show()
        self.helpMCQ.show()

        self.questionLabel = QtWidgets.QLabel(self)
        self.questionLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.questionLabel, 0,0,1,3)

        #if the mcq already exist we append self.page with all the data
        if os.path.isfile(databasePath):
            self.exist = True
            with open(str(databasePath), 'r', newline='') as csvfile:
                fileUser = csv.reader(csvfile,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL) 
                page = [line for line in fileUser]
                page.pop(0)
                page.pop(0)
                csvfile.close()
            
            for i in range(0,len(page)):
                self.questionTab.append(page[i])

            self.addQuestion_click(False)

            #first question
            for i in range(0,len(self.page)):
                for j in range(1,len(self.page[i])-2):
                    
                    self.page[i][j][0].hide()
                    self.page[i][j][1].hide()
           
            
            if len(self.page[self.currentQuestion])-2 >2:
                self.remove.setEnabled(True)
            else:
                self.remove.setEnabled(False)
            if len(self.questionTab)>1:
                self.nextQuestion.show()
                self.addQuestion.setEnabled(True)#self.addQuestion.setEnabled(False)
                self.deleteQuestion.setEnabled(True)
            else:
                self.addQuestion.setEnabled(True)
                self.deleteQuestion.setEnabled(False)
                self.nextQuestion.hide() 
        
        else:
            
            self.addQuestion.setEnabled(True)

            self.addQuestion_click(True)
            self.remove.setEnabled(False)
            
            self.addQuestion.setEnabled(True)
            self.deleteQuestion.setEnabled(False)
            self.previousQuestion.hide()
            self.nextQuestion.hide()


        self.firstQuestionDone = True
        
        
        self.setGeometry(Config.SCREEN_WIDTH/2-self.size().width()/2,50,self.size().width(),3*Config.SCREEN_HEIGHT/4)
        self.mcq = True
        self.updateQuestion()


#mcq creation functions#
    def reset(self):
        self.hide()
        self.__init__()
        self.show()

    def saveMCQ(self):
        
        #print("rdftghjkl")
        empty = False
        for question in range(0,len(self.page)):
            self.questionTab[question][0] = self.page[question][0].toPlainText()
            if self.page[question][0].toPlainText() =="":
                empty = True
            #print(self.page[question][0].toPlainText())
            for i in range(1,len(self.page[question])-1):
                #print(self.page[question][i][1].toPlainText())
                self.questionTab[question][i] = self.page[question][i][1].toPlainText()
                if self.page[question][i][1].toPlainText() == "":
                    empty = True
            self.questionTab[question][len(self.questionTab[question])-1] = self.page[question][len(self.page[question])-1].currentText()
            if self.page[question][len(self.page[question])-1].currentText() == "":
                empty = True
        
        return empty
        
    def policeSize(self):
        font = QtGui.QFont(Config.police, Config.fontSize)
        txt = QtGui.QFontMetrics(font)

        pixelsWide = txt.width("test")
        pixelsHigh = txt.height()
        return pixelsHigh
    
    def resizeEvent(self, event):
        if self.mcq:
            self.updateQuestion()
    
    def updateQuestion(self):
        
        #First Question
        if self.currentQuestion==0:
            self.previousQuestion.hide()
            if len(self.page[self.currentQuestion])-2 >2:
                self.remove.show()
            if len(self.questionTab) > 1:
                self.nextQuestion.show()
                self.deleteQuestion.setEnabled(True)
        #between first and last
        if self.currentQuestion >0 and self.currentQuestion<len(self.questionTab)-1:
            self.nextQuestion.show()
            self.previousQuestion.show()

        #Last Question
        if self.currentQuestion==len(self.questionTab)-1 and self.currentQuestion > 0:
            self.nextQuestion.hide()
            self.previousQuestion.show()

        layoutTitle = QtWidgets.QVBoxLayout()
        layoutTitle.addWidget(self.page[self.currentQuestion][0])
        layoutTitle.setAlignment(QtCore.Qt.AlignTop)
        #self.page[self.currentQuestion][0].setFixedHeight(self.size().height()/3)#(self.policeSizeHeight*4)#(self.size().height()/3)
        
        self.refreshQuestionTitleGroupBox(layoutTitle)
        self.grid.setRowMinimumHeight(1,(self.size().height()/4))
        
        #self.questionTitleGroupBox.adjustSize()#resize(size)

        layoutRightAnswer = QtWidgets.QHBoxLayout()
        layoutRightAnswer.addWidget(self.page[self.currentQuestion][len(self.page[self.currentQuestion])-1])
        self.refreshRightAnswerGroupBox(layoutRightAnswer)

        Config.MCQAnswerByColumn

        if len(self.page[self.currentQuestion])-2 > Config.MCQAnswerByColumn:

            layout = QtWidgets.QHBoxLayout()

            layoutTab = [QtWidgets.QFormLayout(),QtWidgets.QFormLayout()]
            for i in range(1,Config.MCQAnswerByColumn+1):
                
                layoutTab[0].addRow(self.page[self.currentQuestion][i][0], self.page[self.currentQuestion][i][1])

            current = 1    

            for i in range(Config.MCQAnswerByColumn+1,len(self.page[self.currentQuestion])-1 ):
                layoutTab[current].addRow(self.page[self.currentQuestion][i][0], self.page[self.currentQuestion][i][1])
                if i % Config.MCQAnswerByColumn == 0:
                    current+=1
                    layoutTab.insert(current,QtWidgets.QFormLayout())
            
            for elem in layoutTab:
                #elem.setAlignment(QtCore.Qt.AlignTop)
                layout.addLayout(elem)
            
            self.refreshAnswersGroupBox(layout)
        

        else :
            layout = QtWidgets.QFormLayout()
            for i in range(1,len(self.page[self.currentQuestion])-1):
                
                layout.addRow(self.page[self.currentQuestion][i][0], self.page[self.currentQuestion][i][1])
            self.refreshAnswersGroupBox(layout)


        self.page[self.currentQuestion][0].show()
        self.page[self.currentQuestion][len(self.questionTab[self.currentQuestion])-1].show()
        for i in range(1,len(self.questionTab[self.currentQuestion])-2):
            self.page[self.currentQuestion][i][0].show()
            self.page[self.currentQuestion][i][1].show()

        #self.resize(self.sizeHint())#adjustSize()
        self.questionLabel.setText("Question " + str(self.currentQuestion+1) + "/" + str(len(self.questionTab)))


    #add a QLabel and QLineEdit to self.answerWidget and adapt the location of the buttons below the questions
    def add_click(self,notNew = ""):
        temp=[]
        currentAnswer = len(self.page[self.currentQuestion])-1# if self.firstQuestionDone else 1
        temp.append(QtWidgets.QLabel(self))
        temp[0].setText(str(currentAnswer) + " : ")
        temp[0].setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")

        temp.append(QtWidgets.QTextEdit())
        temp[1].setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        temp[1].setFixedHeight(self.policeSizeHeight*2)
        #rightAnswer = range(1,len(self.questionTab[self.currentQuestion])-2)
        
        if notNew == "":
            
            numberAnswer = [str(i) for i in range(1,currentAnswer+1)]#list(str(range(1,currentAnswer)))
            
            
            self.page[self.currentQuestion].insert(len(self.page[self.currentQuestion])-1,temp)
            self.questionTab[self.currentQuestion].insert(len(self.questionTab[self.currentQuestion])-1,"")
            Function.UpdateComboBox(self.page[self.currentQuestion][len(self.page[self.currentQuestion])-1],numberAnswer)

            if len(self.questionTab[self.currentQuestion])-2 > 2:
                self.remove.setEnabled(True)
            else :
                self.remove.setEnabled(False)
            
            if self.firstQuestionDone :
                self.updateQuestion()
            
        else:
            
            temp[1].setText(notNew)
            temp[1].setFixedHeight(self.policeSizeHeight*2)
            self.page[self.currentQuestion].insert(len(self.page[self.currentQuestion])-1,temp)
            

    #remove a Qlabel and QLineEdit from self.answerWidget and adapt the location of the buttons below the questions
    def remove_click(self):
        
        self.page[self.currentQuestion].pop(len(self.page[self.currentQuestion])-2)
        self.questionTab[self.currentQuestion].pop(len(self.questionTab[self.currentQuestion])-2)

        self.updateQuestion()
        if len(self.questionTab[self.currentQuestion])-2 <= 2:
            self.remove.setEnabled(False)

        self.page[self.currentQuestion][len(self.page[self.currentQuestion])-1].removeItem(self.page[self.currentQuestion][len(self.page[self.currentQuestion])-1].count()-1)
        self.page[self.currentQuestion][len(self.page[self.currentQuestion])-1].setCurrentIndex(-1)
        

    #add a new question to the MCQ with 2 empty answers
    def addQuestion_click(self,new = False):
        
        if new == True:
            #self.saveMCQ()
            questionEdit=QtWidgets.QTextEdit()
            questionEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")

            rightAnswer = QtWidgets.QComboBox(self)
            rightAnswer.addItems([])
            rightAnswer.setCurrentIndex(-1)
            rightAnswer.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";" + "}")
            if self.firstQuestionDone:
                self.page[self.currentQuestion][0].hide()
                self.page[self.currentQuestion][len(self.questionTab[self.currentQuestion])-1].hide()
                for i in range(1,len(self.questionTab[self.currentQuestion])-2):
                    self.page[self.currentQuestion][i][0].hide()
                    self.page[self.currentQuestion][i][1].hide()
                self.currentQuestion+=1

            answerCounter=0
            
            self.page.insert(self.currentQuestion,[questionEdit,rightAnswer])
            self.page[self.currentQuestion][0].setText("")
            
            self.questionTab.insert(self.currentQuestion,["",""])
            while answerCounter<2:
                self.add_click('')
                answerCounter+=1
            
            self.updateQuestion()
            
            self.deleteQuestion.setEnabled(True)
            
                
            self.saveMCQ()

        else :
            for i in range(0,len(self.questionTab)):
                
                questionEdit=QtWidgets.QTextEdit()
                questionEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
                
                self.page.insert(i,[questionEdit])
                self.page[i][0].setText(self.questionTab[i][0])
                
                numberAnswer = [str(i) for i in range(1,len(self.questionTab[i])-1)]
                rightAnswer = QtWidgets.QComboBox(self)
                rightAnswer.addItems(numberAnswer)
                rightAnswer.setCurrentIndex(numberAnswer.index(self.questionTab[i][len(self.questionTab[i])-1]))
                rightAnswer.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                                "background-color: " + str(Config.colorFont) +";"
                                "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                                "selection-color: "+ str("") +";" + "}")
                
                self.page[i].append(rightAnswer)#(self.questionTab[i][len((self.questionTab[i]))-1])

                for j in range(1,len(self.questionTab[i])-1):
                    self.add_click(self.questionTab[i][j])
                self.currentQuestion+=1
                         
            self.currentQuestion=0
            
    #delete the current question and go to the previous one
    def deleteQuestion_click(self):

        self.saveMCQ()
        self.page[self.currentQuestion][0].hide()
        self.page[self.currentQuestion][len(self.questionTab[self.currentQuestion])-1].hide()
        for i in range(1,len(self.questionTab[self.currentQuestion])-2):
            self.page[self.currentQuestion][i][0].hide()
            self.page[self.currentQuestion][i][1].hide()

        self.questionTab.pop(self.currentQuestion)
        self.page.pop(self.currentQuestion)

        if self.currentQuestion>0:
            self.currentQuestion-=1

        self.updateQuestion()

        self.saveMCQ()

    def nextQuestion_click(self):
        
        self.saveMCQ()
        
        self.page[self.currentQuestion][0].hide()
        self.page[self.currentQuestion][len(self.questionTab[self.currentQuestion])-1].hide()
        for i in range(1,len(self.questionTab[self.currentQuestion])-2):
            self.page[self.currentQuestion][i][0].hide()
            self.page[self.currentQuestion][i][1].hide()
        
        
        self.currentQuestion +=1

        self.updateQuestion()
        
        
    def previousQuestion_click(self):
        
        self.saveMCQ()

        self.page[self.currentQuestion][0].hide()
        self.page[self.currentQuestion][len(self.questionTab[self.currentQuestion])-1].hide()
        for i in range(1,len(self.questionTab[self.currentQuestion])-2):
            self.page[self.currentQuestion][i][0].hide()
            self.page[self.currentQuestion][i][1].hide()
        
        self.currentQuestion -=1

        self.updateQuestion()

        

    #make sure all the QlineEdit and QComboBox are completed before saving data in the csv file
    def save_click(self):
        empty = self.saveMCQ()

        if empty:
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("some of your case or not completed")
            message.setWindowTitle("Error")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_()

        if not empty :
            textName=os.path.splitext(Config.TXT_IMPORT)[0]
            mcqCsv=str(textName+'.csv')
            databasePath=os.path.join(Config.DatabaseFolder,Config.databaseName,Config.database.folder,mcqCsv)
            """
            with open(str(databasePath), 'w',newline='') as csvfile:
                mcq = csv.writer(csvfile,delimiter='/')
                mcq.writerow([textName])
                for i in range(0,len(self.questionTab)):
                    mcq.writerow(self.questionTab[i])
                csvfile.close()

            """
            textName=os.path.split(Config.TXT_IMPORT)[1]
            with open(str(databasePath), 'w',newline='') as csvfile:
                mcq = csv.writer(csvfile,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                mcq.writerow([textName])
                mcq.writerow(["Question Title","Answers","","Right Answer"])
                for i in range(0,len(self.questionTab)):
                    mcq.writerow(self.questionTab[i])
                csvfile.close()
            
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("MCQ saved")
            message.setWindowTitle("MCQ")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_()

            self.hide()
            self.__init__()
            self.show()

#answer MCQ
class Mcq(QtWidgets.QWidget):
    finishedMcq = QtCore.pyqtSignal(int)
    def __init__(self,user,mcq):
        QtWidgets.QWidget.__init__(self)
        
        self.user=user
        self.mcq=mcq
        self.currentQuestion=0
        self.page=[]
        
        with open(str(self.mcq), 'r', newline='') as csvfile:
            fileUser = csv.reader(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL) 
            self.page = [line for line in fileUser]
            self.page.pop(0)
            self.page.pop(0)
            csvfile.close()
        
        self.answerTab=['']*len(self.page)

        self.setWindowTitle("MCQ")
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.width=200
        self.height=200
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.questionLabel = QtWidgets.QLabel(str(self.page[self.currentQuestion][0]),self)
        self.questionLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.questionLabel,0,0,1,3)


        #add a QRadioButton for each answer of each question and append self.choiceButtonTab with all the widgets
        self.choiceButtonGroupBox = QtWidgets.QGroupBox()
        self.choiceButtonGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.choiceButtonLayout = QtWidgets.QVBoxLayout()
        
        self.choiceButtonTab=[]
        for i in range(0,len(self.page)):
            temp=[]
            temp.append(QtWidgets.QButtonGroup())
            #we start at 1 because 0 is the question and stop at len(self.page[i])-1 because the last element is the right answer
            for j in range(1,len(self.page[i])-1):
                radioButton= QtWidgets.QRadioButton(self.page[i][j])
                radioButton.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
                temp.append(radioButton)
                temp[j].toggled.connect(self.radioButton_click)
                temp[0].addButton(temp[j])
                #temp contain the QButtonGroup and all the QRadioButton
            self.choiceButtonTab.append(temp)

        for i in range(0,len(self.page)):
            for j in range(1,len(self.page[i])-1):
                #self.grid.addWidget(self.choiceButtonTab[i][j],j,0)
                self.choiceButtonLayout.addWidget(self.choiceButtonTab[i][j])
                if(i!=self.currentQuestion):
                    self.choiceButtonTab[i][j].hide()

        self.choiceButtonGroupBox.setLayout(self.choiceButtonLayout)

        self.grid.addWidget(self.choiceButtonGroupBox,1,0,1,3)
        #self.choiceButtonGroupBox.hide()

        
        self.questionGroupBox = QtWidgets.QGroupBox()
        self.questionGroupBox.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        self.questionLayout = QtWidgets.QHBoxLayout()

        self.previous = QtWidgets.QPushButton('<- previous', self)
        self.previous.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.previous.clicked.connect(self.previous_click)
        self.questionLayout.addWidget(self.previous)
        self.previous.hide()

        self.next = QtWidgets.QPushButton('next ->', self)
        self.next.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.next,len(self.choiceButtonTab[self.currentQuestion]),1)
        self.questionLayout.addWidget(self.next)
        self.next.clicked.connect(self.next_click)
        self.next.setEnabled(False)

        
        

        self.save = QtWidgets.QPushButton('Save Answers', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.save,len(self.choiceButtonTab[self.currentQuestion]),1)
        #self.grid.addWidget(self.save,3,0)
        self.questionLayout.addWidget(self.save)
        self.save.clicked.connect(self.saveAnswers_click)
        self.save.hide()
        
        self.questionGroupBox.setLayout(self.questionLayout)

        self.grid.addWidget(self.questionGroupBox,2,0,1,3)

        self.questionNumberLabel = QtWidgets.QLabel(str("Question : " + str(self.currentQuestion+1) + "/" + str(len(self.page))),self)
        self.questionNumberLabel.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.questionNumberLabel,3,0,1,3)

        if len(self.page)==1 :
            self.save.show()
            self.next.hide()
        
        

    #add the selected answer to self.answerTab
    def radioButton_click(self):
        self.next.setEnabled(True)
        self.save.setEnabled(True)
        self.answerTab[self.currentQuestion]=self.choiceButtonTab[self.currentQuestion][0].checkedButton().text()

    #change page
    def previous_click(self):
        if(self.currentQuestion>0):
            
            for i in range(1,len(self.page[self.currentQuestion])-1):
                self.choiceButtonTab[self.currentQuestion][i].hide()
            self.currentQuestion-=1
            self.questionNumberLabel.setText(str("Question : " + str(self.currentQuestion+1) + "/" + str(len(self.page))))
            self.questionLabel.setText(self.page[self.currentQuestion][0])
            for i in range(1,len(self.page[self.currentQuestion])-1):
                self.choiceButtonTab[self.currentQuestion][i].show()
            #self.grid.addWidget(self.previous,len(self.choiceButtonTab[self.currentQuestion]),0)
            #self.grid.addWidget(self.next,len(self.choiceButtonTab[self.currentQuestion]),1)
            if (self.currentQuestion==0):
                self.previous.hide()
            self.next.show()
            self.save.hide()
            self.next.setEnabled(True)
            
    #change page
    def next_click(self):
        if(self.currentQuestion<len(self.page)-1):
            
            for i in range(1,len(self.page[self.currentQuestion])-1):
                self.choiceButtonTab[self.currentQuestion][i].hide()
            self.currentQuestion+=1
            self.questionNumberLabel.setText(str("Question : " + str(self.currentQuestion+1) + "/" + str(len(self.page))))
            self.questionLabel.setText(self.page[self.currentQuestion][0])
            #self.grid.addWidget(self.previous,len(self.choiceButtonTab[self.currentQuestion]),0)
            #self.grid.addWidget(self.next,len(self.choiceButtonTab[self.currentQuestion]),1)
            if (self.currentQuestion==len(self.page)-1):
                self.next.hide()
                #self.grid.addWidget(self.save,len(self.choiceButtonTab[self.currentQuestion]),1)
                self.save.setEnabled(False)
                self.save.show()
            self.previous.show()
            self.next.setEnabled(False)
            for i in range(1,len(self.page[self.currentQuestion])-1):
                self.choiceButtonTab[self.currentQuestion][i].show()
                if self.choiceButtonTab[self.currentQuestion][i].isChecked() == True:
                    self.next.setEnabled(True)
                    self.save.setEnabled(True)
            
    #save the answers in a csv file
    def saveAnswers_click(self):
        textName=os.path.split(Config.TXT_IMPORT)[1]
        answerFileCsv=str(Config.mcqAnswer+".csv")#str('answer.csv')
        reply=QtWidgets.QMessageBox()
        reply.setIcon(QtWidgets.QMessageBox.Question)
        reply.setText("Are you sure of your answers ?")
        reply.setWindowTitle("MCQ")
        reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        reply=reply.exec_()
        if reply == QtWidgets.QMessageBox.Yes:
            with open(str(os.path.join(Config.SAVE_DATA_FOLDER,answerFileCsv)), 'w', newline='') as csvfile:
                answerFile = csv.writer(csvfile,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                answerFile.writerow([textName])
                answerFile.writerow(["Question Title","Answer","Right answer"])
                for i in range(0,len(self.page)):
                    answerFile.writerow([self.page[i][0],self.answerTab[i],self.page[i][int(self.page[i][-1])]])
                csvfile.close()
            self.close()
            self.finishedMcq.emit(1)
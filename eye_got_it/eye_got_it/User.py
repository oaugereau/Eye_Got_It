#User.py => User gestion
#User class => import and export user
#UserDisplay class => User main windows
#UserManagement class => User management (create or edit database)
#Help class windows help

#import python Module
import sys, os, shutil, csv, time, subprocess, webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui
#import others Modules
import Function, Welcome, Config, ConfigFileManagement

genre=["Male","Female","Other",'Not Given']
level=["A0","A1","A2","B1","B2","C1","C2"]
country=['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 
'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 
'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 
'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 
'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 
'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 
'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 
'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 
'French Polynesia', 'French Southern Territories', 'Gabon','Galaxy far, far away', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 
'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 
'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 
'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 
'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 
'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 
'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 
'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 
'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 
'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 
'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 
'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 
'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 
'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 
'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 
'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 
'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 
'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

#import and export user
class User():

    def __init__(self):
        self.user={}       
        self.user["First_name"]=""
        self.user["Last_name"]=""
        self.user["Birthday"]=""
        self.user["Genre"]=""
        self.user["Level"]=""
        self.user["Country"]=""

    def get(self,key):
        return str(self.user[key])

    def Create(self,first_name,last_name,birthday,genre,level,toeic,country):
        first_nameFirst = first_name[0].upper()
        first_nameLast = first_name[1:len(first_name)].lower() 
        first_name = str(first_nameFirst + first_nameLast)

        last_nameFirst = last_name[0].upper()
        last_nameLast = last_name[1:len(last_name)].lower() 
        last_name = str(last_nameFirst + last_nameLast)

        self.user["First_name"]=first_name
        self.user["Last_name"]=last_name
        self.user["Birthday"]=birthday
        self.user["Genre"]=genre
        self.user["Level"]=level
        self.user["Toeic"]=toeic
        self.user["Country"]=country

    def Export(self,new):
        fileUserName=str(self.user["Last_name"] + " " + self.user["First_name"])
        fileUserNameCsv=str(self.user["Last_name"] + " " + self.user["First_name"]+'.csv')
        
        if new == True :
            if not os.path.isdir(Config.UsersFolder):
                os.makedirs(Config.UsersFolder) 
            
            if not os.path.isfile(os.path.join(Config.UsersFolder,fileUserNameCsv)): #not os.path.isdir(os.path.join(Config.UsersFolder,fileUserName)) or 
                if not os.path.isdir(os.path.join(Config.UsersFolder,fileUserName)):
                    os.makedirs(os.path.join(Config.UsersFolder,fileUserName))
                with open(os.path.join(Config.UsersFolder,fileUserName,fileUserNameCsv), 'w', newline='') as csvfile:
                    fileUser = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    fileUser.writerow(["First_name","Last_name","Birthday","Genre","Level","Toeic","Country"])
                    fileUser.writerow([self.user["First_name"],self.user["Last_name"],self.user["Birthday"],self.user["Genre"],self.user["Level"],self.user["Toeic"],self.user["Country"]])
                    csvfile.close()
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText(str(fileUserName + " created"))
                message.setWindowTitle("User Creator")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message=message.exec_()
            else :
                message=QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText(str(fileUserName + " already exist"))
                message.setWindowTitle("User Creator")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message=message.exec_()

        else :
            user = os.path.join(Config.UsersFolder,fileUserName,fileUserNameCsv)
            with open(user, 'w', newline='') as csvfile:
                fileUser = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #for key,value in self.user.items():
                #print(key + " : " + value)
                fileUser.writerow(["First_name","Last_name","Birthday","Genre","Level","Toeic","Country"])
                fileUser.writerow([self.user["First_name"],self.user["Last_name"],self.user["Birthday"],self.user["Genre"],self.user["Level"],self.user["Toeic"],self.user["Country"]])
                csvfile.close()
            message=QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("User Saved")
            message.setWindowTitle("User Edit")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message=message.exec_()

    def Import(self,user):
        if not os.path.isdir(Config.UsersFolder):
                os.makedirs(Config.UsersFolder) 
        with open(str(os.path.join(Config.UsersFolder,user,user+".csv")), 'r', newline='') as csvfile:
            fileUser = csv.reader(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            lines = [line for line in fileUser]    
            csvfile.close()

        self.user["First_name"] = str(lines[1][0])
        self.user["Last_name"] = str(lines[1][1])
        self.user["Birthday"] = str(lines[1][2])
        self.user["Genre"] = str(lines[1][3])
        self.user["Level"] = str(lines[1][4])
        self.user["Toeic"] = str(lines[1][5])
        self.user["Country"] = str(lines[1][6])

#User main windows
class UserDisplay(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        if not os.path.isdir(Config.UsersFolder):
                os.makedirs(Config.UsersFolder) 
        
        Config.userListCreate()

        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('User Gestion')
        self.width=500
        self.height=150
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid) 

        self.user = QtWidgets.QLabel("Choose User :",self)
        self.user.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.user, 0,0)

        self.userEdit = QtWidgets.QComboBox(self)
        self.userEdit.addItems(Config.UsersList)
        self.userEdit.setCurrentIndex(-1)
        self.userEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.userEdit, 0,1,1,3)
        self.userEdit.currentIndexChanged[int].connect(self.on_currentIndexChanged)

        self.add = QtWidgets.QPushButton('Add User', self)
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


        self.userFolder = QtWidgets.QPushButton('User Folder', self)
        self.userFolder.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.userFolder, 1,2)
        self.userFolder.clicked.connect(self.openFolder)
        self.userFolder.setEnabled(False)      

        self.delete = QtWidgets.QPushButton('Delete', self)
        self.delete.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.grid.addWidget(self.delete, 1,3)
        self.delete.clicked.connect(self.delete_click)
        self.delete.setEnabled(False)

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
        self.grid.addWidget(self.help, 2,3)
        self.help.clicked.connect(self.help_click)
        self.help.setEnabled(True) 
              
    #add user
    def add_click(self):
        self.userAddWindows = UserManagement("",True)
        self.userAddWindows.newUserRefresh.connect(self.refreshUserList)
        self.userAddWindows.show()
    
    def refreshUserList(self):
        Config.userListCreate()
        self.userEdit.clear()
        self.userEdit.addItems(Config.UsersList)
        self.userEdit.setCurrentIndex(-1)
        #Function.UpdateComboBox(self.userEdit, Config.UsersList)

    #select user
    def select_click(self):
        
        self.userView = UserManagement(self.userEdit.currentText(),False)
        self.userView.show()
    
    #open user folder
    def openFolder(self):
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        subprocess.run([FILEBROWSER_PATH, os.path.join(Config.UsersFolder,self.userEdit.currentText())])

    #delete user
    def delete_click(self):
        reply=QtWidgets.QMessageBox()
        reply.setIcon(QtWidgets.QMessageBox.Question)
        reply.setText("Are you sure you want to delete " + str(self.userEdit.currentText() + " ?"))
        reply.setWindowTitle("Remove User")
        reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        reply=reply.exec_()    
        if reply == QtWidgets.QMessageBox.Yes:
            shutil.rmtree(os.path.join(Config.UsersFolder,self.userEdit.currentText()))
            directory_contents=os.listdir(os.path.join(Config.UsersFolder))
            directory_contents.sort()
            Function.UpdateComboBox(self.userEdit, directory_contents)

    #enable select, open and delete user buttons
    def on_currentIndexChanged(self, index):
        self.select.setEnabled(True)
        self.userFolder.setEnabled(True)
        self.delete.setEnabled(True)
        if self.userEdit.currentText() =='':
            self.select.setEnabled(False)
            self.userFolder.setEnabled(False)
            self.delete.setEnabled(False)

    #help windows    
    def help_click(self):
        if Config.documentationHTML:
            helpHtml()
        else:
            self.helpWindows = Help()
            self.helpWindows.show()

    #close windows
    def closeEvent(self, event):
        if hasattr(self, "userAddWindows"):
            self.userAddWindows.close()
        if hasattr(self, "userView"):
            self.userView.close()
        if hasattr(self, "helpWindows"):
            self.helpWindows.close()

#User management (create or edit database)
class UserManagement(QtWidgets.QWidget):

    finished = QtCore.pyqtSignal(int)
    newUserRefresh = QtCore.pyqtSignal(int)

    def __init__(self,user,newUser):
        QtWidgets.QWidget.__init__(self)
        self.user=User()
        if not newUser:
            
            self.user.Import(user)
        else :

            self.userList=user
            self.setDate = False
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle(str('User View : ' + user) if not newUser else str("User Creator"))
        self.width=1300
        self.height=600
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)
        #self.setMinimumSize(self.width, self.height)
        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.grid.setColumnMinimumWidth(0,self.width/2)
        self.grid.setColumnMinimumWidth(1,self.width/2)
        
        self.firstNameGroupBox = QtWidgets.QGroupBox("First Name")
        self.firstNameGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.firstNameLayout = QtWidgets.QVBoxLayout()

        self.firstNameEdit=QtWidgets.QLineEdit(self)
        if not newUser :
            self.firstNameEdit.setText(str(self.user.get("First_name")))
        self.firstNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont if not newUser else "red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        #self.grid.addWidget(self.firstNameEdit, 0,1)
        if not newUser:
            self.firstNameEdit.setReadOnly(True)
        else:
            self.firstNameEdit.textChanged.connect(self.defaultEdit)

        self.firstNameLayout.addWidget(self.firstNameEdit)

        self.firstNameGroupBox.setLayout(self.firstNameLayout)

        self.grid.addWidget(self.firstNameGroupBox,0,0)


        self.lastNameGroupBox = QtWidgets.QGroupBox("Last Name")
        self.lastNameGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.lastNameLayout = QtWidgets.QVBoxLayout()

        self.lastNameEdit=QtWidgets.QLineEdit(self)
        if not newUser:
            self.lastNameEdit.setText(str(self.user.get("Last_name")))
        self.lastNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont if not newUser else "red") +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        #self.grid.addWidget(self.lastNameEdit, 0,3)
        if not newUser:
            self.lastNameEdit.setReadOnly(True)
        else:
            self.lastNameEdit.textChanged.connect(self.defaultEdit)

        self.lastNameLayout.addWidget(self.lastNameEdit)

        self.lastNameGroupBox.setLayout(self.lastNameLayout)

        self.grid.addWidget(self.lastNameGroupBox,0,1)

        self.genreGroupBox = QtWidgets.QGroupBox("Genre")
        self.genreGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.genreLayout = QtWidgets.QVBoxLayout()

        self.genreEdit = QtWidgets.QComboBox(self)
        self.genreEdit.addItems(genre)
        if not newUser:
            index = self.genreEdit.findText(self.user.get("Genre"))
            self.genreEdit.setCurrentIndex(index)
        else:
            self.genreEdit.setCurrentIndex(-1)
        self.genreEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.genreEdit, 1,3)

        self.genreLayout.addWidget(self.genreEdit)

        self.genreGroupBox.setLayout(self.genreLayout)

        self.grid.addWidget(self.genreGroupBox,1,0)


        self.countryGroupBox = QtWidgets.QGroupBox("Country")
        self.countryGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.countryLayout = QtWidgets.QVBoxLayout()

        self.countryEdit = QtWidgets.QComboBox(self)
        self.countryEdit.addItems(country)
        if not newUser:
            index = self.countryEdit.findText(self.user.get("Country"))
            self.countryEdit.setCurrentIndex(index)
        else :
            self.countryEdit.setCurrentIndex(-1)
        self.countryEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.countryEdit, 2,3)

        self.countryLayout.addWidget(self.countryEdit)

        self.countryGroupBox.setLayout(self.countryLayout)

        self.grid.addWidget(self.countryGroupBox,1,1)
        #self.countryGroupBox.hide()


        self.levelGroupBox = QtWidgets.QGroupBox("Level")
        self.levelGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.levelLayout = QtWidgets.QVBoxLayout()
        self.levelEdit = QtWidgets.QComboBox(self)
        self.levelEdit.addItems(level)
        if not newUser:
            index = self.levelEdit.findText(self.user.get("Level"))
            self.levelEdit.setCurrentIndex(index)
        else :
            self.levelEdit.setCurrentIndex(-1)
        self.levelEdit.setStyleSheet("QComboBox" + "{" + "color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        #self.grid.addWidget(self.levelEdit, 2,1)

        self.levelLayout.addWidget(self.levelEdit)

        self.levelGroupBox.setLayout(self.levelLayout)

        self.grid.addWidget(self.levelGroupBox,2,0)

        self.toeicGroupBox = QtWidgets.QGroupBox("Toeic Score")
        self.toeicGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        self.toeicLayout = QtWidgets.QVBoxLayout()

        self.toeicEdit=QtWidgets.QLineEdit(self)
        if not newUser:
            self.toeicEdit.setText(str(self.user.get("Toeic")))
        self.toeicEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";")
        #self.grid.addWidget(self.toeicEdit, 3,1)
        self.toeicEdit.textChanged.connect(self.toeicInt)

        self.toeicLayout.addWidget(self.toeicEdit)

        self.toeicGroupBox.setLayout(self.toeicLayout)

        self.grid.addWidget(self.toeicGroupBox,2,1)

        self.birthdayGroupBox = QtWidgets.QGroupBox("Birthday")
        self.birthdayGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.birthdayGroupBox.setFlat(True)
        self.birthdayGroupBox.setStyleSheet("QGroupBox"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        
        self.birthdayLayout = QtWidgets.QHBoxLayout()

        self.enableCalendar = QtWidgets.QPushButton('Select Date', self)
        self.enableCalendar.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")
        #self.grid.addWidget(self.enableCalendar, 1,1)
        self.enableCalendar.clicked.connect(self.enableCalendar_click)
        self.birthdayLayout.addWidget(self.enableCalendar)
        self.enableCalendar.hide()

        self.birthdayEdit = QtWidgets.QCalendarWidget()
        self.birthdayEdit.setGridVisible(True)
        self.birthdayEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                    "background-color: " + str(Config.colorFont) +";"
                    "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                    "selection-color: "+ str("") +";")
        self.birthdayLayout.addWidget(self.birthdayEdit)
        self.birthdayEdit.hide()

        if not newUser:
            if self.user.get("Birthday") !='':
                
                dateExtract=self.user.get("Birthday") .split('/')
                date = QtCore.QDate(int(dateExtract[2]), int(dateExtract[1]), int(dateExtract[0])) 
                self.birthdayEdit.setSelectedDate(date)            
                self.setDate = True
                #self.grid.addWidget(self.birthdayEdit, 1,1)
                self.birthdayEdit.show()              

            else :
                
                self.setDate = False
                self.enableCalendar.show()

        else :
            self.enableCalendar.show()
            self.setDate = False

        self.birthdayGroupBox.setLayout(self.birthdayLayout)

        self.grid.addWidget(self.birthdayGroupBox,3,0,1,2)
        #self.birthdayGroupBox.hide()

        self.save = QtWidgets.QPushButton('Save', self)
        self.save.setStyleSheet("QPushButton"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";"+"}")

                  
        self.grid.addWidget(self.save, 5,0,1,2)
        if not newUser:
            self.save.clicked.connect(lambda:self.save_click(False))
        else :
            self.save.clicked.connect(lambda:self.save_click(True))

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
        self.grid.addWidget(self.help, 4,1)
        self.help.clicked.connect(helpHtml)
        self.help.setEnabled(True)
        

    #display calendar
    def enableCalendar_click(self):
        self.enableCalendar.hide()
        #self.grid.addWidget(self.birthdayEdit, 1,1)
        self.birthdayEdit.show()
        self.setDate=True      

    #save user or new user
    def save_click(self,newUser):
        if self.lastNameEdit.text() !='' and self.firstNameEdit.text() != '' and (Function.is_integer(self.toeicEdit.text()) or self.toeicEdit.text() == ''):
            
            if self.setDate :
                date = self.birthdayEdit.selectedDate()
                fullDate = str(date.day()) + "/" + str(date.month()) + "/" + str(date.year())
            else :
                fullDate=self.user.get("Birthday")
                
            self.user.Create(self.firstNameEdit.text(),self.lastNameEdit.text(),fullDate,self.genreEdit.currentText(),self.levelEdit.currentText(),self.toeicEdit.text(),self.countryEdit.currentText())
            self.user.Export(newUser)
            if newUser : 
                Config.userListCreate()
                #Function.UpdateComboBox(self.userList, Config.UsersList)
                self.newUserRefresh.emit(1)
            self.finished.emit(1)
            self.close()
            

        else :
            if not Function.is_integer(self.toeicEdit.text()) and self.toeicEdit.text() !="":

                if newUser : 
                    
                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Information)
                    message.setText("You must enter a valid Toeic Score !")
                    message.setWindowTitle("User Creator")
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()
                else : 
                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Information)
                    message.setText("You must enter a valid Toeic Score !")
                    message.setWindowTitle("User Edit")
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()
            
            if self.lastNameEdit.text() =='' or self.firstNameEdit.text() == '':

                if newUser : 
                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Information)
                    message.setText("You must enter a Last and First name !")
                    message.setWindowTitle("User Creator")
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()

                else : 
                    message=QtWidgets.QMessageBox()
                    message.setIcon(QtWidgets.QMessageBox.Information)
                    message.setText("You must enter a Last and First name !")
                    message.setWindowTitle("User Edit")
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    message=message.exec_()
    
    #default parameters color (here for first and last name)
    def defaultEdit(self):

        if self.lastNameEdit.text() == '':
            self.lastNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"
                            "border: 1px solid gray;")

        else :
            if self.lastNameEdit.text() != '':
                self.lastNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"
                            "border: 1px solid gray;")

        if self.firstNameEdit.text() == '':
            self.firstNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"
                            "border: 1px solid gray;")

        else :
            if self.firstNameEdit.text() != '':
                self.firstNameEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"
                            "border: 1px solid gray;")

    #check if toeic is only integer (not string) and change color if not integer
    def toeicInt(self):
        if not Function.is_integer(self.toeicEdit.text()) and self.toeicEdit.text() != '':
            self.toeicEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str("red") +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"
                            "border: 1px solid gray;")

        else:
            self.toeicEdit.setStyleSheet("color: " + str(Config.colorText) +";"
                            "background-color: " + str(Config.colorFont) +";"
                            "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                            "selection-color: "+ str("") +";"
                            "border: 1px solid gray;")


def helpHtml():
    webbrowser.open_new_tab(Config.documentationUsers)
    
class Help(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        #windows config
        self.setStyleSheet("background-color:"+ str(Config.background)+";")
        self.setWindowTitle('Help Windows')
        self.width=900
        self.height=200
        self.setGeometry(Config.SCREEN_WIDTH/2-self.width/2,Config.SCREEN_HEIGHT/2-self.height/2,self.width,self.height)

        self.grid=QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #widgets

        self.Label = QtWidgets.QLabel("Click on 'Add User' to create a new user\n\n"
                                      "If you want to change the informations of a user, select it in the list and click on 'Select'\n\n"
                                      "You can access the 'Users' folder containing all the raw recordings by selecting the user in the list and clicking on 'User Folder'\n\n"
                                      "You can delete an existing user by selecting it in the list and clicking on 'Delete'")
        self.Label.setStyleSheet("QLabel"+"{"+"color: " + str(Config.colorText) +";"
                        "background-color: " + str(Config.colorFont) +";"
                        "font: "+ str(Config.fontType) +" " + str(Config.fontSize)+ "px " + str(Config.police) + ";"
                        "selection-color: "+ str("") +";" + "}")
        self.grid.addWidget(self.Label,0,0)


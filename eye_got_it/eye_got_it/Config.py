#Config.py => eye got it param contain global variables used, config import and theme

#import python Module
import time, sys, os, io
from PyQt5 import QtCore, QtWidgets, QtGui
#import others Modules
import ConfigFileManagement, Database, Function, Welcome

DEBUG=False # debug session

def currentTime(): # return the current time
    return str(time.strftime('%H_' '%M_' '%S'))

def currentDate(): # return the current date
    return str(time.strftime('%Y_' '%m_' '%d_'))

#config import
CONFIG_IMPORTED=False
CONFIG_IMPORTED_ERROR=False
configParser= None
initial_setup="" # first run of eye got it

#eye got it folder
EyeGotItFolder=""# main data folder
DatabaseFolder=""
UsersFolder=""
ReportFolder=""
PATH_IMAGE = os.path.join("Pictures")

#eye got it
VERSION=""
LOGO_IMAGE=os.path.join(PATH_IMAGE , "logo.png")

#text choose by user location path
TXT_IMPORT=None

#eyeTracker
eyeTrackerSdkPro = False #eyeTracker gaming (false) or Pro (true)
eyeTrackerList = ["Tobii Pro Nano", "Tobii Gaming"]
interactionLibrary = "eyeTracker"
sdkPro = "eyeTrackerPro"
onlyBuscher = False
eyeTrackerAlgorithm = ['buscher','nystrom']

#test calibration eyeTracker
eyeTrackerCalibration="tempGazes.csv"
eyeTrackerHeadCalibration="tempHeadGazes.csv"

#screen variable
SCREEN_WIDTH=None
SCREEN_HEIGHT=None
SCREEN_WIDTH=None
PHYSICAL_SCREEN_HEIGHT=None
PHYSICAL_SCREEN_WIDTH=None
SCREEN_WIDTH_SIMULATION=1366# DO NOT MODIFY
SCREEN_HEIGHT_SIMULATION=650# DO NOT MODIFY

#video Input
videoInput=[]
actionUnitMinIntensity=2 #minimal to maximal => 1 to 5

#audio Input
audioInput = []

#simulation folder name
SAVE_DATA_FOLDER = ""
SAVE_DATA_MAIN_FOLDER = ""
TIME_FOLDER=currentTime()#init time session
NAME_SAVE_FOLDER = currentDate() + TIME_FOLDER#init saving folder

#Log file
LOG_FILE="eye_got_it.log"
LOG_TYPE="DEBUG"

#theme and police
THEME=""
colorFont = ""
colorText = ""
colorSelect = ""
background=""
#police="Noto Sans"
police=""
fontSize=20
fontSizeText=25
fontType="normal"

#audio parameters
rate=""
channels=""
chunk=""
sound_out=""

#databases
databaseName=""
database=""

#MCQ Answers by column :
MCQAnswerByColumn = 4

#ActionUnits by column :
ActionUnitsByColumn = 4

#parameters
screenshotName=""
screenshotExtension="jpg"
eyeTrackerHeadData=""
eyeTrackerData=""
eyeTrackerDataFile="csv"
videoOut=""
videoUNIXStart=""
audioUNIXStart=""
HelpIcon = ""

#Report files
eyeTrackerGlissades = ""#"glissades"
eyeTrackerSaccades = ""#"saccades"
eyeTrackerFixations = ""#"fixations"
eyeTrackerVelocityGazes = ""#"velocityGazes"
eyeTrackerScreenshot = ""#"EyeTracker"
wordScreenshot = ""#"Word_Page"

#list of database
DatabaseList=[]

#list of users
UsersList=[]

#hardware test
audioTest = True
videoTest = True
eyeTrackerTest = True

#HTML documentation
documentationLocation = os.path.join(os.getcwd(),"docs","html")
documentationHTML=False

#OpenFace => DO NOT EDIT Unless a new version supports other action units 
openFaceActionUnit=[1, 2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 20, 23, 25, 26, 28, 45]

#Eye Got It Documentation
if os.path.isdir(documentationLocation):
    documentationHTML= True
    documentationWelcome = os.path.join(documentationLocation,"welcome.html")
    documentationSimulation = os.path.join(documentationLocation,"simulation.html")
    documentationParameters = os.path.join(documentationLocation,"parameters.html")
    documentationParametersAudioTest = os.path.join(documentationLocation,"parameters.html#audio-test")
    documentationUsers = os.path.join(documentationLocation,"user.html")
    documentationDatabase = os.path.join(documentationLocation,"database.html")
    documentationReport = os.path.join(documentationLocation,"report.html")
    documentationActionUnits = os.path.join(documentationLocation,"actionUnits.html")
    documentationMCQ = os.path.join(documentationLocation,"mcq.html")

#import the config
def ImportConfig():
    global eyeTrackerHeadData,videoOut, VERSION, configParser, screenshotName, screenshotExtension
    global textPart, mcqAnswer, textPosition, THEME, CONFIG_IMPORTED, CONFIG_IMPORTED_ERROR
    global rate, channels, chunk, soundOut,initial_setup, eyeTrackerData, eyeTrackerGlissades, eyeTrackerSaccades
    global eyeTrackerFixations, eyeTrackerVelocityGazes, eyeTrackerScreenshot, wordScreenshot

    try:
        configParser= ConfigFileManagement.ConfigFileRead('config.ini')
        THEME=str(configParser.GetParameters("THEME", 'theme'))
        
        screenshotName = str(configParser.GetParameters('SYSTEM', 'screenshot_name'))
        VERSION = str(configParser.GetParameters('SYSTEM', 'version'))
        theme(THEME)
        rate = int(configParser.GetParameters('SOUND', 'rate'))
        channels = int(configParser.GetParameters('SOUND', 'channels'))
        chunk = int(configParser.GetParameters('SOUND', 'chunk'))
        soundOut = str(configParser.GetParameters('SOUND', 'sound_out'))
        videoOut = str(configParser.GetParameters('VIDEO', 'video_out'))
        mcqAnswer=str(configParser.GetParameters('USER', 'mcq_answer'))
        textPosition=str(configParser.GetParameters('USER', 'text_position'))
        textPart=str(configParser.GetParameters('USER', 'text_part'))
        eyeTrackerHeadData = str(configParser.GetParameters('EYETRACKER', 'eye_tracker_head_data'))
        eyeTrackerData = str(configParser.GetParameters('EYETRACKER', 'eye_tracker_data'))
        initial_setup=(configParser.GetParameters('OTHER', 'initial_setup'))

        eyeTrackerGlissades = str(configParser.GetParameters('REPORT', 'eyeTracker_Glissades'))
        eyeTrackerSaccades = str(configParser.GetParameters('REPORT', 'eyeTracker_Saccades'))
        eyeTrackerFixations = str(configParser.GetParameters('REPORT', 'eyeTracker_Fixations'))
        eyeTrackerVelocityGazes = str(configParser.GetParameters('REPORT', 'eyeTracker_VelocityGazes'))
        eyeTrackerScreenshot = str(configParser.GetParameters('REPORT', 'eyeTracker_Screenshot'))
        wordScreenshot = str(configParser.GetParameters('REPORT', 'word_Screenshot'))

        databaseListCreate()
        userListCreate()
        CONFIG_IMPORTED=True

    except:
        CONFIG_IMPORTED=False
        CONFIG_IMPORTED_ERROR=True
    
    

#import database
def CreateDatabase(Name):
    global database,databaseName
    databaseName=Name
    if os.path.isdir(os.path.join(DatabaseFolder,Name)) :
        database=Database.Database(os.path.join(DatabaseFolder,Name))
        database.CreateConfig()
        return True
    else :
        return False


#import theme
def theme(Theme):
    global colorFont, colorText, colorSelect,background, HelpIcon

    if Theme == "Normal":
        colorFont = "white"
        colorText = "black"
        colorSelect = "black"
        background = "white"
        HelpIcon = os.path.join("Pictures","help.png")
        return True

    if Theme == "Dark":
        colorFont = "black"
        colorText = "white"
        colorSelect = "white"
        background = "black"
        HelpIcon = os.path.join("Pictures","help_dark.png")
        return True
    else :
        return False


def fileExist(fileToTest): # detect if file in folder exist
    try:
        with open(fileToTest,'r',encoding='latin1') as filename:            
            return  True #file exist

    except: #no file
        Log.InfoSaveLog("warning",str(fileToTest + "not exist"))       
        return False # return error file no found


#import list of databases
def databaseListCreate():
    global DatabaseList

    listDatabase = os.listdir(DatabaseFolder)
    DatabaseList=[]
    for elem in listDatabase:
        if len(elem.split('.'))==1 and os.path.isfile(os.path.join(DatabaseFolder,elem,"config.ini")):
            DatabaseList.append(elem)
    DatabaseList.sort()


#import list of users
def userListCreate():
    global UsersList

    listUser = os.listdir(UsersFolder)
    UsersList=[]
    for elem in listUser:
        if len(elem.split('.'))==1 and os.path.isfile(os.path.join(UsersFolder,elem,str(elem + ".csv"))):
            UsersList.append(elem)
    UsersList.sort()
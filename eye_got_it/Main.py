import sys, os, subprocess
system = os.name
sys.path.insert(1,os.path.join( os.getcwd(),'eye_got_it'))
from PyQt5 import QtCore, QtWidgets
import sys,os
#import others Modules
import Config ,Error, Welcome, Function

if len(sys.argv)==2 :
    if sys.argv[1] == "-debug":
        print("enter in debug mode")
        Config.DEBUG=True

print(os.path.join(os.path.expanduser('~'),"Documents"))

Config.EyeGotItFolder=os.path.join(os.path.expanduser('~'),"Eye Got It")
Config.DatabaseFolder=os.path.join(os.path.expanduser('~'),"Eye Got It","Database")
Config.UsersFolder=os.path.join(os.path.expanduser('~'),"Eye Got It","Users")
Config.ReportFolder=os.path.join(os.path.expanduser('~'),"Eye Got It","Report")

if not os.path.isdir(Config.EyeGotItFolder):
    os.makedirs(Config.EyeGotItFolder)
if not os.path.isdir(Config.DatabaseFolder):
    os.makedirs(Config.DatabaseFolder)
if not os.path.isdir(Config.UsersFolder):
    os.makedirs(Config.UsersFolder)

#Config.Log=Error.ErrorLog(os.path.join(Config.EyeGotItFolder,Config.LOG_FILE),Config.LOG_TYPE)

#Config.Log.InfoSaveLog("info",'Start')   


while 1 :
    Welcome.myApp = QtWidgets.QApplication(sys.argv)
    screen_resolution = Welcome.myApp.desktop().screenGeometry()
    Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT = screen_resolution.width(), screen_resolution.height()
    screen = Welcome.myApp.primaryScreen()
    rect = screen.physicalSize()
    Config.PHYSICAL_SCREEN_WIDTH=rect.width()
    Config.PHYSICAL_SCREEN_HEIGHT=rect.height()
    welcome = Welcome.Welcome()
    #welcome.app=app
    welcome.show()
    sys.exit(Welcome.myApp.exec_())

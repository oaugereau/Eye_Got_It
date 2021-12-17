#import python Module
import logging, time
#import others Modules
import Config

class ErrorLog():

    def __init__(self,name,typeLog):

        #name to write in log
        self.name=name

        #log type
        if typeLog == "DEBUG":
            self.typeLog=logging.DEBUG
        if typeLog == "INFO":
            self.typeLog=logging.INFO
        if typeLog == "WARNING":
            self.typeLog=logging.WARNING
        if typeLog == "ERROR":
            self.typeLog=logging.ERROR
        if typeLog == "CRITICAL":
            self.typeLog=logging.CRITICAL

        #create log
        logging.basicConfig(filename=self.name, filemode='w',level=self.typeLog)

    # function to save message in log
    def InfoSaveLog(self,typeError,text):  
        # Save in log (depending of error type)
        if typeError =="info":
            logging.info(Config.currentTime() + " " + text)
            return

        if typeError=="warning":
            logging.warning(Config.currentTime() + " " + text)
            return

        if typeError=="error":
            logging.error(Config.currentTime() + " " + text)
            return

        if typeError=="critical":
            logging.critical(Config.currentTime() + " " + text)
            return

        if typeError=="debug":
            logging.debug(Config.currentTime() + " " + text)
            return

        else:
            print("Problem : error not found")
            logging.error(Config.currentTime() + " error " + text + " not found")
            return

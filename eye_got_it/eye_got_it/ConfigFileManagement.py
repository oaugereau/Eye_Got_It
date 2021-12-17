#ConfigFileManagement.py => create or edit config file
#ConfigFileRead class => read config file
#ConfigFileWrite class  => create config file

#import python Module
import configparser, os

#read and edit config file
class ConfigFileRead():

    def __init__(self,filename):

        self.filename=filename

        self.configParser = configparser.ConfigParser()

        self.configFilePath=os.path.join(self.filename)

        self.configParser.read(self.configFilePath,"utf-8")

    #get value of one parameter
    def GetParameters(self,tab,variable):  
        if(tab != None):
            return self.configParser.get(tab, variable)

        else :
            for section in self.GetSection():
                for option in self.configParser[section]:
                    if (variable == option):
                        return self.configParser.get(str(section), str(variable))
         
    def GetParametersVariable(self,section):  
        variable=[]
        for option in self.configParser[section]:
            variable.append(self.configParser.get(str(section), str(option)))
        return variable

    #get list of section
    def GetSection(self):  
        return self.configParser.sections()

    #edit one parameter
    def SetParameters(self,tab,name,value):  
        cfgfile = open(self.configFilePath,'w') 
        if(tab != None):
            self.configParser.set(str(tab), str(name), str(value))

        else :
            for section in self.GetSection():
                for option in self.configParser[section]:
                    if (name == option):
                        self.configParser.set(str(section), str(name), str(value))

        self.configParser.write(cfgfile)
        cfgfile.close()

#create config file
class ConfigFileWrite():

    def __init__(self):
        self.configParser = configparser.RawConfigParser()

    #get list of section
    def GetSection(self):  
        return self.configParser.sections()

    #add section
    def Add_Section(self,section):
        self.configParser.add_section(section)

    #add one parameter
    def SetParameters(self,section,option,value):
        if not section in self.GetSection():
            self.Add_Section(section)
        self.configParser.set(section,option,value)

    #create config ini file
    def CreateFile(self,filename):
        with open(filename, 'w') as newini:
            self.configParser.write(newini)
        


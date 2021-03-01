'''
* Global functions and constants defined for the AFOF simulation project
*
* - This file must be placed in the folder: <VisualComponents path>\Python\Commands\ 
*
'''

import datetime
# acquiring VC-specific references
from vcScript import *
app = getApplication()

# global constants:
INIT_DELAY = 1; # [sec] defines the waiting time for some scripts in the model 

'''
* Saving log to a file on a hard drive
'''


# function returns the actual date and time formatted so that it can be a valid unix filename
def getTimeStampForFileName():
  now_TS = datetime.datetime.today()
  logPrefix = str(now_TS.year) + "_" + str(now_TS.month) + "_" + str(now_TS.day)
  logPrefix = logPrefix + "_" + str(now_TS.hour) + "_" + str(now_TS.minute)
  return logPrefix
  
  
# default path and filename constants
defaultDirPath = "C:\Users\\JohannesWIN10\\Documents\\nxtSTUDIOProjects\\EnAS 2020 VC\\SkillServer\\nxtSTUDIO\\EnAS 2020 VC with Skills\\traces\\"
defaultFileName = "_trace_log.txt"
defaultFilePath = defaultDirPath + getTimeStampForFileName() + defaultFileName


# class facilitates writing log to a file
class FileLogger:
  def __init__(self, filePath = None):
    self.filePath = filePath
    self.initStatus = self.initNewLog(filePath)

  # handles creating/overwriting the log file 
  def initNewLog(self, filePath = None):
    if filePath is None: # automatically generate a new log file in default path 
        filePath = defaultDirPath + getTimeStampForFileName() + "_log.txt"
	filePath = defaultDirPath + getTimeStampForFileName() + "_log.txt"
        
    try: # attempt opening the file
        with open(filePath, "w") as file:
          file.write("") #initializing an empty file
        return True     
    except: # couldn't open the file specified in filePath
      return False 
  
  
  # automatically generates 
  def reinitializeLogger(self):
    self.initStatus = self.initNewLog(self.filePath) 
  
  # updates the contents of the log file
  # - text : string that is added to the file; new line is added autmatically afterwards
  def appendToFile(self, text):
    with open(self.filePath, "a") as file:
      file.write(text + "\n")
 

# default logger reference for the simulation session:
logger = FileLogger(defaultFilePath);

'''
* Generic log function  that handles the following:
* - Print live log to a VC console
* - Updates the log file if the access to it is working
'''
# logger function that takes text and values and concatenates them in proper format
# comp - reference to the component object that is calling the logger
# msg - string input is a plain text describing the event
# list_of_vals - list of additional data related to the event
def log(component, msg, list_of_vals = []):
  timestamp = app.Simulation.SimTime # datetime.datetime.today()
  str_TS = "%.3f" %(timestamp) # reduce the timestamp resolution down to a millisecond

  sValues = "" # all the values to be appended into one string 
  for i in range(len(list_of_vals)):
    sValues = sValues + ":" + str(list_of_vals[i])
  
  printText = "%s: %s %s %s" %(str_TS, component.Name, msg, sValues)
  print(printText)
  
  if logger.initStatus:
    logger.appendToFile(printText)
  


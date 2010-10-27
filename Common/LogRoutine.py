#Copyright Ken Faulkner 2007.

import logging
import os
import sys
import traceback

logLevelDict = { "DEBUG":logging.DEBUG, "ERROR":logging.ERROR, "INFO":logging.INFO }

log = None

def getLogger(logLevel="DEBUG", logName="linkmenow", fileName=None):
  ''' LogLevel is just a string...   but hell, I can live with that. '''

  
  try:
  
    global log
    
    if log != None:
      return log
      
    if fileName == None:
      fileName = logName+".log"
    
    realLogLevel = logLevelDict.get( logLevel, logging.INFO )
    
    logging.basicConfig(level=realLogLevel,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=fileName)
 
    log = logging.getLogger( logName)
    
    # Make sure log level set...  swear this is actually required.
    log.setLevel( realLogLevel )
                    
  except:
    print "LOGGING ERROR", traceback.format_exc()
    
  return log

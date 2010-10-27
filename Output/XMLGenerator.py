#!/usr/bin/env python
import sys
import traceback
from Common.configobj import ConfigObj
import time
from Common.LogRoutine import *
from DAO import StatusCodes

class XMLGenerator( object ):
  
  def __init__(self):
    self.log = getLogger(  )  
  
    self.reason_dict = { StatusCodes.INVALID_CREATOR:"Please check creator", 
                         StatusCodes.INVALID_SHORT_URL:"Short URL is invalid. Possibly already used or invalid characters", 
                         StatusCodes.INVALID_LONG_URL:"Please check full URL", 
                         StatusCodes.SHORT_URL_TAKEN:"Short URL is already taken"}
       
    self.config = ConfigObj( "Config/linkmenow.cfg" )
    self.short_link_base = self.config['LinkMeNow']['ShortLinkBase']
    self.template_dir = self.config['LinkMeNow']['TemplateDir']
    

  def generate_basic_response( self, status  ):
    """
    Param: status is value from StatusCodes
    
    """
    self.log.info("XMLGenerator::generate_basic_response start")
    
    res = ""
    
    try:
    
      res = r"<response><status>%d</status>%s</response>"%( status, "%s" )
      
    except:
      self.log.error("XMLGenerator::generate_basic_response ex " + traceback.format_exc() )
    
    return res

    
  def generate_successful_get( self, long_url ):
    
    self.log.info("XMLGenerator::generate_successful_get start")
    
    res = ""
    
    try:
    
      res2 =  self.generate_basic_response( StatusCodes.SUCCESSFUL )
      res3 = r"<entries><entry>%s</entry></entries>"%( long_url )
      res = res2%( res3 )
      
    except:
      self.log.error("XMLGenerator::generate_successful_get ex " + traceback.format_exc() )
    
    return res

  def generate_unsuccessful_get( self, short_url ):
    
    self.log.info("XMLGenerator::generate_unsuccessful_get start")
    
    res = ""
    
    try:
    
      res2 =  self.generate_basic_response( StatusCodes.FAILED )
      res = res2%("")
      
    except:
      self.log.error("XMLGenerator::generate_unsuccessful_get ex " + traceback.format_exc() )
    
    return res

  def generate_successful_set( self):
    
    self.log.info("XMLGenerator::generate_successful_set start")
    
    res = ""
    
    try:
    
      res2 =  self.generate_basic_response( StatusCodes.SUCCESSFUL )
      res = res2%( "" )
      
    except:
      self.log.error("XMLGenerator::generate_successful_set ex " + traceback.format_exc() )
    
    return res

  def generate_unsuccessful_set( self, status ):
    
    self.log.info("XMLGenerator::generate_unsuccessful_set start")
    
    res = ""
    
    try:
    
      res2 =  self.generate_basic_response( status )
      res = res2%("")
      
    except:
      self.log.error("XMLGenerator::generate_unsuccessful_set ex " + traceback.format_exc() )
    
    return res
            


  def generate_successful_list( self, entries_list ):
    
    self.log.info("XMLGenerator::generate_successful_list start")
    
    res = ""
    
    try:
    
      res2 =  self.generate_basic_response( StatusCodes.SUCCESSFUL )
      res3 = r"<entries>%s</entries>"
      
      url_list = ""
      for entry in entries_list:
      
        try:
          url_list += r"<entry>%s</entry>" % ( self.short_link_base + str( entry.short_url)  )
        
        except UnicodeEncodeError:
          pass
          # swallowing exception. This is just for some asian characters that I haven't figured out yet.
           
      res3 = res3%( url_list )
        
      res = res2%( res3 )
      
    except:
      self.log.error("XMLGenerator::generate_successful_list ex " + traceback.format_exc() )
    
    return res

  def generate_unsuccessful_list( self, creator ):
    
    self.log.info("XMLGenerator::generate_unsuccessful_list start")
    
    res = ""
    
    try:
    
      res2 =  self.generate_basic_response( StatusCodes.FAILED )
      res = res2%("")
      
    except:
      self.log.error("XMLGenerator::generate_unsuccessful_list ex " + traceback.format_exc() )
    
    return res
    


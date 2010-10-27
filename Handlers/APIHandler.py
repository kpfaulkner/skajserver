from google.appengine.ext import webapp
import traceback
from Common.LogRoutine import *
from DAO.DAO import DAO
from Output.XMLGenerator import XMLGenerator
from DAO import StatusCodes

class APIHandler(webapp.RequestHandler):
    

  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()

    self.dao = DAO()
    
    self.xml_gen = XMLGenerator()
        

        
  def decode_short_url(self, url ):
    """
    Decodes short url.
    This is really duplicated code, which is bad. 
    But its really only a 1 liner.   
    """

    full_url = None

    self.log.info("APIHandler::decode_short_url start")
    
    try:


        self.log.debug("short url " + str( url ) )
        
        if url != None and url != "":
          full_url = self.dao.get_long_url( short_url )
        
          self.log.debug("long url " + str( full_url ) )
          
        
    except:
      self.log.error("APIHandler::decode_short_url ex " + traceback.format_exc() )
    
    return full_url  
      
                      
  def get(self, command ):
    """
    Can issue 3 types of commands.
    1) Get a LONG_URL from a short url
    2) Assign a LONG_URL to a given short_url
    3) Assign a LONG_URL to a random url.   
    """

    try:

      self.log.debug("command is " + str( command ) )
      
      if command == "get":
        url = self.request.get("short_url")
        
        if url != None and url != "":
          full_url = self.dao.get_long_url( url )
        
          if full_url != None and full_url != "":
            res = self.xml_gen.generate_successful_get( full_url )
          else:
            res = self.xml_gen.generate_unsuccessful_get( url )
            
          self.response.out.write( res )
        
      else:
        if command == "set":
          short_url = self.request.get("short_url")
          full_url = self.request.get("full_url")
          creator = self.request.get("creator")
          tags = self.request.get("tags")
          
          if short_url != None and short_url != "" and full_url != None and full_url != "" and creator != None and creator != "" :
            
            result_url, status_code = self.dao.replace_entry( short_url, full_url, creator, tags )
               
            if status_code == StatusCodes.SUCCESSFUL:
              res = self.xml_gen.generate_successful_set(  )
            else:
              res = self.xml_gen.generate_unsuccessful_set( status_code )
              
            self.response.out.write( res )

        
        else:
          if command == "list":
            creator = self.request.get("creator")
            
            if creator != None and creator != "":
              entry_list = self.dao.get_all_entries_for_creator( creator )
            
              self.log.debug("entry list " + str( entry_list ) )
              
              if entry_list != None and entry_list != [] :
                res = self.xml_gen.generate_successful_list( entry_list)
              else:
                res = self.xml_gen.generate_unsuccessful_List( creator )
                
              self.response.out.write( res )
            
    except:
      self.log.error("APIHandler::get ex " + traceback.format_exc() ) 
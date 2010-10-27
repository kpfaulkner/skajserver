from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Output.HTMLGenerator import HTMLGenerator
from Common.configobj import ConfigObj

class CreateUserHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.output_generator = HTMLGenerator()
    self.config = ConfigObj("Config/skajserver.cfg")

 
            
  def get(self, url):
    """
    Create a user... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    
    try:
      
      self.log.debug("CreateUserHandler get")
      
      user_name = self.request.get("user_name")    
      password = self.request.get("password")    

      
      response = self.__process_data( long_url, short_url, creator, tags )
      
    except:
      self.log.error("StoreHandler::get ex " + traceback.format_exc()  ) 
      
    self.response.out.write( response )

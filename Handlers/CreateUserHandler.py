from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Common.configobj import ConfigObj

class CreateUserHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.config = ConfigObj("Config/skajserver.cfg")

 
            
  def get(self, url):
    """
    Create a user... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "success1"
    try:
      
      self.log.debug("CreateUserHandler get")
      data = "success2"
      user_name = self.request.get("user_name")    
      password = self.request.get("password")    
      data = "success3"
      self.log.debug("user URL is " + user_name )

      (status, user ) = self.dao.createUser( user_name, password )
      data = "success4"
      
      #print "fooooooooooooo"

      if status == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY CREATED USER " + user_name )

    except:
      self.log.error("CreateUserHandler::get ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

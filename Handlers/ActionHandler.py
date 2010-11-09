from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Common.configobj import ConfigObj

class ActionHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.config = ConfigObj("Config/skajserver.cfg")


  def canAttack( self, attacking_country, attacked_country ):
    """
    Confirms if countries can attack eachother.
    """

    # FIXME
    return true
  
  def attack( self, attacking_country, attacked_country ):
    """
    Confirms if countries can attack eachother.
    """

    # FIXME
    return true


  def handleAttack(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<action>FAILED</action>"

    try:
      self.log.debug("ActionHandler:handleAttack start")

      name = self.request.get("name")    
      token = self.request.get("token")

      if self.dao.authenticateUser( name, token):
      
        # get country doing the attacking        
        attacking_country = self.request.get("attacking_name")
                
        # get country being attacked.
        attacked_country = self.request.get("attacked_name")

        # confirm they're near eachother.
        if self.canAttack( attacking_country, attacked_country ):

          # attack
          self.attack( attacking_country, attacked_country )

        
    except:
      self.log.error("GameHandler:handleCreateGame  ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def handlePopulate(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<action>FAILED</action>"

    try:
      self.log.debug("ActionHandler:handlePopulate start")

      name = self.request.get("name")    
      token = self.request.get("token")

      if self.dao.authenticateUser( name, token):
      
        # get country doing the attacking        
        country_name = self.request.get("country")
                
        # get country being attacked.
        attacked_country = self.request.get("attacked_name")

        # confirm they're near eachother.
        if self.canAttack( attacking_country, attacked_country ):

    except:
      self.log.error("GameHandler:handlePopulate  ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def get(self, url):
    """
    handle various User based gets
    """

    self.log.debug("URL is " + url)
    
    path = self.request.path
    self.log.debug("path is " + path)

    # dict string --> method.
    # FIXME
    if path == "/1/attack":
      self.handleAttack( url )
    else:
      if path == "/1/populate":
        self.handleModifyGameState( url )






from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Common.configobj import ConfigObj

class GameHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.config = ConfigObj("Config/skajserver.cfg")


  def handleCreateGame(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<game>FAILED</game>"

    try:
      self.log.debug("GameHandler:handleCreateGame start")

      name = self.request.get("name")    
      password = self.request.get("password")
      num_players = int( self.request.get("num_players") )
      
      (stat, game) =  self.dao.createGame( name, password, num_players )
          
      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY CREATED GAME " + name )
        data = "<game name=%s></game>"%( name )

    except:
      self.log.error("GameHandler:handleCreateGame  ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def handleModifyGameState(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<game>FAILED</game>"

    try:
      self.log.debug("GameHandler:handleModifyGameState start")

      name = self.request.get("name")    
      state = self.request.get("state")
  
      
      (stat, game) =  self.dao.modifyGameState( name, state )
          
      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY MODIFIED STATE GAME " + name )
        data = "<game name=%s></game>"%( name )

    except:
      self.log.error("GameHandler:handleModifyGameState  ex " + traceback.format_exc()  ) 
      
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
    if path == "/1/creategame":
      self.handleCreateGame( url )
    else:
      if path == "/1/modifygamestate":
        self.handleModifyGameState( url )





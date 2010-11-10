from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Common.configobj import ConfigObj

class PlayerHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.config = ConfigObj("Config/skajserver.cfg")

  def createPlayerHandler(self, url):
    """
    create player based on user that is logged in. 
    """
    response = "sorry... operation failed"
    data = "<player>FAILED</player>"

    try:
      
      self.log.debug("PlayerHandler:createPlayerHandler")

      user_name = self.request.get("user_name")    
      token = self.request.get("token")    
      
      # need to know which game we're joining.
      game_name = self.request.get("game_name")

      if self.dao.authenticateUser( user_name, token ):

        # check if user has already joined the game.
        ( stat, player ) = self.dao.getPlayerForGame( user_name, game_name )
        
        if stat == StatusCodes.PLAYER_NOT_IN_GAME:

          self.log.debug("player does not exist in game")
          ( user_status, user) = self.dao.getUser( user_name )

          if user_status == StatusCodes.SUCCESSFUL:

            self.log.debug("have user successfully")

            # get the game.
            ( game_stat, game) = self.dao.getGame( game_name )

            self.log.debug("game name is " + game.game_name)
            
            # create the player.
            player = self.dao.createPlayer( user, game )


            data = "<player id=%s game_name=%s></user>"%( user_name, game_name )
        else:
          self.log.debug("player already in game")
          data = "<player id=%s game_name=%s></user>"%( user_name, game_name )
    except:
      self.log.error("PlayerHandler:createPlayerHandler ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )


  def getPlayerHandlerForGame( self, url):
    """
    Retrieve User.
    NO SECURITY YET.....
    MARKS the user as logged in (on the server?)
    """
    response = "sorry... operation failed"
    data = "<player>FAILED</player>"

    try:
      
      self.log.debug("PlayerHandler:getPlayerHandlerForGame")

      user_name = self.request.get("user_name")    
      token = self.request.get("token")    
      game_name = self.request.get("game_name")

      (stat, player ) = self.dao.getPlayerForGame( user_name, game_name )


      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY RETRIEVED PLAYER " + user_name )
        data = "<player id=%s game_name=%s></user>"%( user_name, game_name )

    except:
      self.log.error("PlayerHandler:getPlayerHandlerForGame ex " + traceback.format_exc()  ) 
      
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
    if path == "/1/createplayer":
      self.createPlayerHandler( url )
    else:
      if path == "/1/getplayer":
        self.getPlayerHandlerForGame( url )




